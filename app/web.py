"""The FastAPI page: persona and date picker (GET), the three cards, and /healthz.

create_app(config, answerer) builds nothing at import time; main() builds the index and
the chat model and returns the app, so a broken file or a missing key fails the deploy's
health check instead of failing on the first visitor.
"""
from collections import OrderedDict
from datetime import date, datetime, timedelta, timezone
import json
import logging
from pathlib import Path
from typing import Callable

from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.answer import AnswerUnavailable, Answerer, Reply, gemini_chat
from app.cards import show
from app.config import Config, load_config
from app.data import load_documents, load_org, load_personas
from app.retrieval import build_index, gemini_embeddings
from app.rules import Scope, scope as build_scope

logger = logging.getLogger("app.web")

BUSY_MESSAGE = "Hệ thống tạm thời không trả lời được. Vui lòng thử lại sau ít phút."

TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


def create_app(config: Config, answerer: Callable[[Scope, str], Reply]):
    """Data and config are loaded once here; the answerer is injected (the real one needs a key)."""
    documents = load_documents()
    personas = load_personas(load_org())
    cache_size = config.page.answer_cache_size
    cache: OrderedDict = OrderedDict()  # demo LRU of finished Reply objects (decision 5)

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
        key = (persona_id, tuple(sorted(scoped.chunk_ids)), question)
        if key in cache:
            reply = cache.pop(key)
            cache[key] = reply  # mark as most recently used
            cache_hit = True
        else:
            cache_hit = False
            try:
                reply = answerer(scoped, question)
            except AnswerUnavailable:
                return _render(request, {**context, "error": BUSY_MESSAGE}, 503)
            cache[key] = reply
            while len(cache) > cache_size:
                cache.popitem(last=False)

        card, lines = show(scoped, reply.retrieved, reply.points)
        logger.info(
            json.dumps(
                {
                    "persona": persona_id,
                    "as_of": parsed.isoformat(),
                    "question": question,
                    "card": card.kind,
                    "reason": card.reason,
                    "cache_hit": cache_hit,
                },
                ensure_ascii=False,
            )
        )
        context["persona_id"] = persona_id
        context["as_of"] = parsed.isoformat()
        context["card"] = {"kind": card.kind, "lines": lines}
        return _render(request, context, 200)

    return app


def main() -> FastAPI:
    """uvicorn factory: build the index and the chat model eagerly, then the app."""
    logging.basicConfig(level=logging.INFO)
    config = load_config()
    documents = load_documents()
    index = build_index(documents, gemini_embeddings(config.retrieval.embedding_model))
    answerer = Answerer(index, gemini_chat(config.llm), config.retrieval)
    return create_app(config, answerer)


def _render(request: Request, context: dict, status_code: int):
    return templates.TemplateResponse(
        request=request, name="index.html", context=context, status_code=status_code
    )


class _LazyApp:
    """Proxy that builds the real app on first use, so tests can import app.web without GEMINI_API_KEY."""

    def __init__(self) -> None:
        self._app: FastAPI | None = None

    def _get_app(self) -> FastAPI:
        if self._app is None:
            self._app = main()
        return self._app

    def __getattr__(self, name: str):
        return getattr(self._get_app(), name)

    async def __call__(self, scope, receive, send):
        await self._get_app()(scope, receive, send)


app = _LazyApp()
