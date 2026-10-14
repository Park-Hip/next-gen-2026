"""The FastAPI pages: the question form with its three cards, the judges' guide, and /healthz.

HTTP only: the route checks the query, builds the scope and hands the question to
services.ask; build_app takes the answerer so the tests can inject one on offline fakes.
/data and /cases are read-only views of data/ and the committed run: they call no model.
"""
from datetime import date, datetime, timedelta, timezone
import json
import logging
from pathlib import Path
from typing import Callable

from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from appota_kb.core.config import Config
from appota_kb.core.paths import ROOT
from appota_kb.evaluation.committed import committed_run
from appota_kb.integrations.data_files import load_documents, load_org, load_personas, load_test_cases
from appota_kb.models.answer import Reply
from appota_kb.models.scope import Scope
from appota_kb.services.answering.answerer import AnswerUnavailable
from appota_kb.services.ask import ReplyCache, ask
from appota_kb.services.guide import case_views, format_date, org_tree, persona_views, series_views
from appota_kb.services.scope import scope as build_scope

logger = logging.getLogger(__name__)

BUSY_MESSAGE = "Hệ thống tạm thời không trả lời được. Vui lòng thử lại sau ít phút."

TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


def build_app(config: Config, answerer: Callable[[Scope, str], Reply], root: Path = ROOT) -> FastAPI:
    """Data and config are loaded once here; the answerer is injected (the real one needs a key).

    `root` is where the committed report and results are read from; a broken committed run
    raises here, so the deploy fails its health check instead of serving a wrong page.
    """
    documents = load_documents()
    org = load_org()
    personas = load_personas(org)
    rows = load_test_cases()
    featured, other_cases = case_views(rows, personas, documents)
    run_view = committed_run(rows, root)
    cache = ReplyCache(config.page.answer_cache_size)

    app = FastAPI()

    @app.get("/healthz")
    def healthz() -> dict:
        return {"status": "ok"}

    @app.get("/", response_class=HTMLResponse)
    def index(
        request: Request,
        persona: str = Query(default=""),
        as_of: str = Query(default=""),
        q: str = Query(default=""),
    ):
        today = _today(config)
        context = {
            "active": "ask",
            "personas": list(personas.values()),
            "persona_id": persona,
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

        persona_id = persona.strip()
        if persona_id not in personas:
            return _render(request, "index.html", {**context, "error": "Người hỏi không hợp lệ."}, 400)
        try:
            parsed = date.fromisoformat(as_of.strip())
        except ValueError:
            return _render(request, "index.html", {**context, "error": "Ngày không hợp lệ."}, 400)
        if len(question) > config.page.question_max_chars:
            return _render(request, "index.html", {**context, "error": "Câu hỏi quá dài."}, 400)

        persona_obj = personas[persona_id]
        scoped = build_scope(persona_obj, parsed, documents)
        try:
            asked = ask(scoped, question, answerer, cache)
        except AnswerUnavailable:
            return _render(request, "index.html", {**context, "error": BUSY_MESSAGE}, 503)
        logger.info(
            json.dumps(
                {
                    "persona": persona_id,
                    "as_of": parsed.isoformat(),
                    "question": question,
                    "card": asked.card.kind,
                    "reason": asked.card.reason,
                    "cache_hit": asked.cache_hit,
                },
                ensure_ascii=False,
            )
        )
        context["persona_id"] = persona_id
        context["as_of"] = parsed.isoformat()
        context["card"] = {"kind": asked.card.kind, "lines": asked.lines}
        return _render(request, "index.html", context, 200)

    @app.get("/data", response_class=HTMLResponse)
    def data(request: Request):
        today = _today(config)
        context = {
            "active": "data",
            "today_text": format_date(today),
            "units": org_tree(org, personas),
            "persona_views": persona_views(personas, documents, today),
            "series": series_views(documents, org, today),
        }
        return _render(request, "data.html", context, 200)

    @app.get("/cases", response_class=HTMLResponse)
    def cases(request: Request):
        context = {
            "active": "cases",
            "featured": featured,
            "others": other_cases,
            "run": run_view,
        }
        return _render(request, "cases.html", context, 200)

    return app


def _today(config: Config) -> date:
    """Today in the product's time zone; the default as-of date of the form and of /data."""
    return (datetime.now(timezone.utc) + timedelta(hours=config.page.utc_offset_hours)).date()


def _render(request: Request, name: str, context: dict, status_code: int):
    return templates.TemplateResponse(
        request=request, name=name, context=context, status_code=status_code
    )
