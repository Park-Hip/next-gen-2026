"""The FastAPI page: persona and date picker (GET), the three cards, and /healthz.

This module owns the route logic, the answerer seam and the legal scope choices.
The HTML lives in app/templates/ (the "HTML and UI" part); the templates render the
lines produced by app.cards.render.
"""
from datetime import date, datetime, timedelta, timezone
from functools import partial
from pathlib import Path

from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.cards import render as render_card
from app.config import Config, load_config
from app.data import load_documents, load_org, load_personas
from app.rules import pick_card, scope as build_scope
from app.stub import Answerer, answer as stub_answer

TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


def create_app(config: Config, answerer: Answerer | None = None):
    """Data and config are loaded once here, so a broken file fails the deploy's health check."""
    documents = load_documents()
    personas = load_personas(load_org())
    if answerer is None:
        answerer = partial(stub_answer, config=config)

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
        today = (datetime.now(timezone.utc) + timedelta(hours=config.page.utc_offset_hours)).date()
        context = {
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
            return _render(request, context, 200)

        persona_id = persona.strip()
        if persona_id not in personas:
            return _render(request, {**context, "error": "Người hỏi không hợp lệ."}, 400)
        try:
            parsed = date.fromisoformat(as_of.strip())
        except ValueError:
            return _render(request, {**context, "error": "Ngày không hợp lệ."}, 400)
        if len(question) > config.page.question_max_chars:
            return _render(request, {**context, "error": "Câu hỏi quá dài."}, 400)

        persona_obj = personas[persona_id]
        scoped = build_scope(persona_obj, parsed, documents)
        reply = answerer(scoped, question)
        card = pick_card(scoped, reply.retrieved, reply.cited)
        by_id = {c.id: c for c in scoped.chunks}
        retrieved_chunks = tuple(by_id[cid] for cid in reply.retrieved)
        lines = render_card(card, scoped, reply.text, retrieved_chunks)
        context["persona_id"] = persona_id
        context["as_of"] = parsed.isoformat()
        context["card"] = {"kind": card.kind, "lines": lines}
        return _render(request, context, 200)

    return app


def _render(request: Request, context: dict, status_code: int):
    return templates.TemplateResponse(
        request=request, name="index.html", context=context, status_code=status_code
    )


app = create_app(load_config())