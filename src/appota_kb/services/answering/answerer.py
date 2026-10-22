"""Step 6: one grounded Gemini call that returns one answer, its quotes and citations, or nothing.

The chat model sees only the retrieved chunks and the asker's unit, which the rules
decided. Its output is one JSON object {answer, points: [{quote, chunks}], disagreement: [id, id]};
the card kind and the sources come from step 7 (services/citations.py), never from this text.
The answer is shown once above the verified quotes (ADR 0018); the disagreement is a flag
step 7 checks (ADR 0014).
"""
import json
import logging
import time

from langchain_core.language_models.chat_models import BaseChatModel

from appota_kb.core.config import Retrieval
from appota_kb.models.answer import Reply
from appota_kb.models.scope import Scope
from appota_kb.services.answering.output import answer_schema, parse_disagreement, parse_reply, raw_text
from appota_kb.services.answering.prompt import build_messages
from appota_kb.services.retrieval.index import Index
from appota_kb.services.retrieval.search import ScopeLeakError, retrieve

logger = logging.getLogger(__name__)


class AnswerUnavailable(RuntimeError):
    """Gemini (answer or query embedding) failed after retries; the page shows a 503, never a card."""


class Answerer:
    """Steps 5-6: retrieve, ask the model once, and return the answer and the points it cited."""

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
            self._log(scope, question, (), "", (), (), "", started)
            return Reply(retrieved=(), answer="", points=(), raw="")

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
            answer, points = "", None
            disagreement = ()
        else:
            answer, points = parse_reply(result.get("parsed"))
            disagreement = parse_disagreement(result.get("parsed"))
        self._log(scope, question, ids, answer, points, disagreement, raw, started)
        return Reply(retrieved=ids, answer=answer, points=points, raw=raw, disagreement=disagreement)

    def _log(self, scope: Scope, question: str, retrieved, answer, points, disagreement, raw: str, started) -> None:
        latency_ms = round((time.perf_counter() - started) * 1000)
        logger.info(
            json.dumps(
                {
                    "persona": scope.persona.id,
                    "as_of": scope.as_of.isoformat(),
                    "question": question,
                    "model": getattr(self.chat, "model", None),
                    "retrieved": list(retrieved),
                    "answer": answer,
                    "points": None if points is None else [
                        {"quote": p.quote, "chunks": list(p.chunks)} for p in points
                    ],
                    "disagreement": list(disagreement),
                    "raw": raw,
                    "latency_ms": latency_ms,
                },
                ensure_ascii=False,
            )
        )
