"""The FastAPI pages: sign-in, the question form with its three cards, the judges' guide, and /healthz.

HTTP only: the server decides who is asking from the signed session (ADR 0016), never from the
request; the route checks the query, builds the scope and hands the question to services.ask.
build_app takes the answerer so the tests can inject one on offline fakes.
/data and /cases are read-only views of data/ and the committed run, open to the judge account
only: they call no model.
/source opens the cited version of a document for the signed-in asker, from the rules only: it calls no
model and shows a chunk only when the asker's scope on that date holds it (#77).
Every unknown path and every refused source gives the same 404 page.
"""
from datetime import date, datetime, timedelta, timezone
import hmac
import json
import logging
from pathlib import Path
from typing import Callable
from urllib.parse import parse_qs, urlencode

from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from appota_kb.core.config import Config
from appota_kb.core.paths import ROOT
from appota_kb.evaluation.committed import committed_run
from appota_kb.integrations.data_files import load_documents, load_org, load_personas, load_test_cases
from appota_kb.models.answer import Reply
from appota_kb.models.org import Persona
from appota_kb.models.scope import Scope
from appota_kb.services.answering.answerer import AnswerUnavailable
from appota_kb.services.ask import ReplyCache, ask
from appota_kb.services.guide import case_views, format_date, org_tree, persona_views, series_views
from appota_kb.services.scope import scope as build_scope
from appota_kb.services.source_view import anchor_of, source_view

logger = logging.getLogger(__name__)

BUSY_MESSAGE = "Hệ thống tạm thời không trả lời được. Vui lòng thử lại sau ít phút."
WRONG_PASSWORD_MESSAGE = "Sai mật khẩu."
EMPLOYEE = "employee"
EVALUATOR = "evaluator"  # the judge account: opens /data and /cases and asks as any employee account

TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


def build_app(
    config: Config,
    answerer: Callable[[Scope, str], Reply],
    *,
    session_secret: str,
    demo_password: str,
    root: Path = ROOT,
) -> FastAPI:
    """Data and config are loaded once here; the answerer is injected (the real one needs a key).

    `session_secret` signs the session cookie and `demo_password` is the password every simulated
    account shares; main.create_app reads both from the environment (ADR 0016).
    `root` is where the committed report and results are read from; a broken committed run
    raises here, so the deploy fails its health check instead of serving a wrong page.
    """
    documents = load_documents()
    org = load_org()
    personas = load_personas(org)
    employees = {p.id: p for p in personas.values() if EMPLOYEE in p.roles}
    rows = load_test_cases()
    featured, other_cases = case_views(rows, personas, documents)
    run_view = committed_run(rows, root)
    cache = ReplyCache(config.page.answer_cache_size)

    app = FastAPI()
    # A browser-session cookie (no max_age), HttpOnly by default. It holds only the account id:
    # the unit and roles are reloaded from data/personas.yaml on every request.
    app.add_middleware(
        SessionMiddleware, secret_key=session_secret, max_age=None, same_site="lax", https_only=False
    )

    def signed_in(request: Request) -> Persona | None:
        """The account in the signed session; a missing, forged or unknown account is signed out."""
        account_id = request.session.get("account")
        return personas.get(account_id) if isinstance(account_id, str) else None

    def is_judge(account: Persona) -> bool:
        return EVALUATOR in account.roles

    def identity(account: Persona, asked_as: Persona | None = None) -> dict:
        return {"account": account, "is_judge": is_judge(account), "asked_as": asked_as}

    def to_sign_in(request: Request) -> RedirectResponse:
        target = request.url.path + ("?" + request.url.query if request.url.query else "")
        return RedirectResponse("/signin?" + urlencode({"next": target}), status_code=303)

    def judge_only(request: Request) -> tuple[Persona | None, Response | None]:
        """(the judge, None), or (None, the response for anyone else): sign-in, or 404 for an employee."""
        account = signed_in(request)
        if account is None:
            return None, to_sign_in(request)
        if not is_judge(account):
            return None, _render(request, "not_found.html", identity(account), 404)
        return account, None

    def sign_in_page(request: Request, next_path: str, account_id: str = "", error: str | None = None, status: int = 200):
        context = {
            "accounts": list(personas.values()),
            "account_id": account_id,
            "next": next_path,
            "error": error,
            "demo_password": demo_password,
        }
        return _render(request, "signin.html", context, status)

    @app.get("/healthz")
    def healthz() -> dict:
        return {"status": "ok"}

    @app.get("/signin", response_class=HTMLResponse)
    def sign_in_form(request: Request, next: str = Query(default="")):
        return sign_in_page(request, _local_path(next))

    @app.post("/signin")
    async def sign_in(request: Request):
        # The body is read with the standard library, so no multipart dependency is needed.
        form = parse_qs((await request.body()).decode("utf-8", errors="replace"), keep_blank_values=True)

        def field(name: str) -> str:
            return form.get(name, [""])[0]

        account_id, password, next_path = field("account"), field("password"), _local_path(field("next"))
        # One message for an unknown account and a wrong password; neither sets a session.
        if account_id not in personas or not hmac.compare_digest(
            password.encode("utf-8"), demo_password.encode("utf-8")
        ):
            return sign_in_page(request, next_path, account_id, WRONG_PASSWORD_MESSAGE, 401)
        request.session.clear()
        request.session["account"] = account_id
        return RedirectResponse(next_path, status_code=303)

    @app.post("/signout")
    def sign_out(request: Request):
        request.session.clear()
        return RedirectResponse("/", status_code=303)

    @app.get("/", response_class=HTMLResponse)
    def index(
        request: Request,
        persona: str = Query(default=""),
        as_of: str = Query(default=""),
        q: str = Query(default=""),
    ):
        account = signed_in(request)
        if account is None:
            return to_sign_in(request)
        # An employee always asks as themselves, whatever the request says; only the judge
        # chooses whom to ask as, and only among the employee accounts.
        asked_as = employees.get(persona.strip()) if is_judge(account) else account
        today = _today(config)
        context = {
            **identity(account, asked_as),
            "active": "ask",
            "employees": list(employees.values()),
            "persona_id": asked_as.id if asked_as else "",
            "as_of": as_of,
            "today": today.isoformat(),
            "question": q,
            "question_max_chars": config.page.question_max_chars,
            "card": None,
            "error": None,
        }
        question = q.strip()
        if not question:
            return _render(request, "index.html", context, 200)

        if asked_as is None:
            return _render(request, "index.html", {**context, "error": "Người hỏi không hợp lệ."}, 400)
        try:
            parsed = date.fromisoformat(as_of.strip())
        except ValueError:
            return _render(request, "index.html", {**context, "error": "Ngày không hợp lệ."}, 400)
        if len(question) > config.page.question_max_chars:
            return _render(request, "index.html", {**context, "error": "Câu hỏi quá dài."}, 400)

        scoped = build_scope(asked_as, parsed, documents)
        try:
            asked = ask(scoped, question, answerer, cache)
        except AnswerUnavailable:
            return _render(request, "index.html", {**context, "error": BUSY_MESSAGE}, 503)
        logger.info(
            json.dumps(
                {
                    "account": account.id,
                    "persona": asked_as.id,
                    "as_of": parsed.isoformat(),
                    "question": question,
                    "card": asked.card.kind,
                    "reason": asked.card.reason,
                    "cache_hit": asked.cache_hit,
                },
                ensure_ascii=False,
            )
        )
        context["as_of"] = parsed.isoformat()
        # The judge's links carry the account asked as; an employee's never do, and the server would ignore it.
        link_as = asked_as.id if is_judge(account) else None
        links = tuple(source_href(line.chunks, parsed, link_as) if line.chunks else "" for line in asked.lines)
        context["card"] = {"kind": asked.card.kind, "lines": asked.lines, "links": links}
        return _render(request, "index.html", context, 200)

    @app.get("/source", response_class=HTMLResponse)
    def source(
        request: Request,
        chunk: list[str] = Query(default=[]),
        as_of: str = Query(default=""),
        persona: str = Query(default=""),
    ):
        account = signed_in(request)
        if account is None:
            return to_sign_in(request)
        # Who is asking is decided as on "/": an employee is always themselves, only the judge picks.
        asked_as = employees.get(persona.strip()) if is_judge(account) else account
        view = None
        if asked_as is not None:
            try:
                parsed = date.fromisoformat(as_of.strip())
            except ValueError:
                parsed = None
            if parsed is not None:
                view = source_view(build_scope(asked_as, parsed, documents), chunk)
        if view is None:
            # One page for a bad date, a bad account, an unknown id and an id outside the scope.
            return _render(request, "not_found.html", identity(account), 404)
        back = {"as_of": view.as_of.isoformat(), **({"persona": asked_as.id} if is_judge(account) else {})}
        context = {**identity(account, asked_as), "active": "ask", "view": view, "back": "/?" + urlencode(back)}
        return _render(request, "source.html", context, 200)

    @app.get("/data", response_class=HTMLResponse)
    def data(request: Request):
        account, early = judge_only(request)
        if early is not None:
            return early
        today = _today(config)
        context = {
            **identity(account),
            "active": "data",
            "today_text": format_date(today),
            "document_count": len(documents),
            "units": org_tree(org, employees),
            "persona_views": persona_views(employees, documents, today),
            "series": series_views(documents, org, today),
        }
        return _render(request, "data.html", context, 200)

    @app.get("/cases", response_class=HTMLResponse)
    def cases(request: Request):
        account, early = judge_only(request)
        if early is not None:
            return early
        context = {
            **identity(account),
            "active": "cases",
            "featured": featured,
            "others": other_cases,
            "run": run_view,
        }
        return _render(request, "cases.html", context, 200)

    @app.exception_handler(404)
    async def not_found(request: Request, exc: Exception):
        account = signed_in(request)
        return _render(request, "not_found.html", identity(account) if account else {}, 404)

    return app


def source_href(chunks: tuple[str, ...], as_of: date, asked_as_id: str | None) -> str:
    """The link of a card line to the version it cites: the chunk ids, the card's date and, for the judge, the
    account asked as. The `#` of a chunk id is percent-encoded; the fragment scrolls to the first chunk."""
    query = [("chunk", cid) for cid in chunks] + [("as_of", as_of.isoformat())]
    if asked_as_id is not None:
        query.append(("persona", asked_as_id))
    return "/source?" + urlencode(query) + "#" + anchor_of(chunks[0])


def _local_path(value: str) -> str:
    """`value` when it is a path on this site, else "/": never an absolute URL, "//host", a backslash or a control character."""
    if (
        value.startswith("/")
        and not value.startswith("//")
        and all(ch != "\\" and ord(ch) >= 32 and ord(ch) != 127 for ch in value)
    ):
        return value
    return "/"


def _today(config: Config) -> date:
    """Today in the product's time zone; the default as-of date of the form and of /data."""
    return (datetime.now(timezone.utc) + timedelta(hours=config.page.utc_offset_hours)).date()


def _render(request: Request, name: str, context: dict, status_code: int):
    return templates.TemplateResponse(
        request=request, name=name, context=context, status_code=status_code
    )
