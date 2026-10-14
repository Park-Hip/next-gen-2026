"""Step 6: one grounded Gemini call that returns points with citations, or nothing.

The chat model sees only the retrieved chunks and the asker's unit, which the rules
decided. Its output is one JSON object {points: [{chunks, quote, text}]}; the card and
the sources come from step 7 (services/citations.py), never from this text.
"""
import json
import logging
import time

from langchain_core.language_models.chat_models import BaseChatModel

from appota_kb.core.config import Retrieval
from appota_kb.models.answer import Reply
from appota_kb.models.scope import Scope
from appota_kb.services.answering.output import answer_schema, parse_points, raw_text
from appota_kb.services.answering.prompt import build_messages
from appota_kb.services.retrieval.index import Index
from appota_kb.services.retrieval.search import ScopeLeakError, retrieve

logger = logging.getLogger(__name__)


class AnswerUnavailable(RuntimeError):
    """Gemini (answer or query embedding) failed after retries; the page shows a 503, never a card."""


class Answerer:
    """Steps 5-6: retrieve, ask the model once, and return the points it cited."""

    def __init__(self, index: Index, chat: BaseChatModel, settings: Retrieval):
        self.index = index
        self.chat = chat
        self.settings = settings

    def __call__(self, scope: Scope, question: str) -> Reply:
        started = time.perf_counter()
        try:
            hits = retrieve(self.index, scope, question, self.settings)
        except (ScopeLeakError, ValueError):
            raise
        except Exception as exc:
            raise AnswerUnavailable(f"retrieval failed: {exc}") from exc

        if not hits:
            self._log(scope, question, (), (), "", started)
            return Reply(retrieved=(), points=(), raw="")

        ids = tuple(hit.chunk.id for hit in hits)
        try:
            structured = self.chat.with_structured_output(
                answer_schema(ids), method="json_schema", include_raw=True
            )
            result = structured.invoke(build_messages(hits, scope, question))
        except (ScopeLeakError, ValueError):
            raise
        except Exception as exc:
            raise AnswerUnavailable(f"the model call failed: {exc}") from exc

        raw = raw_text(result.get("raw"))
        if result.get("parsing_error") is not None:
            points = None
        else:
            points = parse_points(result.get("parsed"))
        self._log(scope, question, ids, points, raw, started)
        return Reply(retrieved=ids, points=points, raw=raw)

    def _log(self, scope: Scope, question: str, retrieved, points, raw: str, started) -> None:
        latency_ms = round((time.perf_counter() - started) * 1000)
        logger.info(
            json.dumps(
                {
                    "persona": scope.persona.id,
                    "as_of": scope.as_of.isoformat(),
                    "question": question,
                    "model": getattr(self.chat, "model", None),
                    "retrieved": list(retrieved),
                    "points": None if points is None else [
                        {"chunks": list(p.chunks), "quote": p.quote, "text": p.text}
                        for p in points
                    ],
                    "raw": raw,
                    "latency_ms": latency_ms,
                },
                ensure_ascii=False,
            )
        )
