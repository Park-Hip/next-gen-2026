"""Step 6: one grounded Gemini call that returns points with citations, or nothing.

The chat model sees only the retrieved chunks and the asker's unit, which the rules
decided. Its output is one JSON object {points: [{chunks, quote, text}]}; the card and
the sources come from app.rules.card_for_answer (step 7), never from this text.

Run by hand: `python -m app.answer <persona> <as_of> <question>` (needs GEMINI_API_KEY).
"""
from dataclasses import dataclass
from datetime import date
import json
import logging
import os
import sys
import time
from typing import Literal

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langchain_core.rate_limiters import InMemoryRateLimiter
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field, ValidationError, create_model

from appota_kb.config import Llm, Retrieval, load_config
from appota_kb.data import load_documents, load_org, load_personas
from appota_kb.retrieval import Hit, Index, ScopeLeakError, build_index, gemini_embeddings, retrieve
from appota_kb.rules import Point, Scope, card_for_answer, scope as build_scope

logger = logging.getLogger("app.answer")

SYSTEM_INSTRUCTION = """You are a strictly grounded assistant limited to the information provided in the User Context. In your answers, rely **only** on the facts that are directly mentioned in that context. You must **not** access or utilize your own knowledge or common sense to answer. Do not assume or infer from the provided facts; simply report them exactly as they appear. Your answer must be factual and fully truthful to the provided text, leaving absolutely no room for speculation or interpretation. Treat the provided context as the absolute limit of truth; any facts or details that are not directly mentioned in the context must be considered **completely untruthful** and **completely unsupported**. If the exact answer is not explicitly written in the context, you must return an empty list of points.

<task>
The User Context holds clauses of internal HR policies, each in a <chunk> tag with its id, and the unit of the employee who asks.
Every chunk has already been checked to apply to this employee.
Answer the employee's question from these chunks only.
</task>

<output_format>
Return a JSON object with a list "points"; each point is one fact of the answer:
- "chunks": the ids of the chunks that state this fact.
- "quote": a passage copied word for word from one of those chunks that states this fact, without quotation marks and without any change.
- "text": the fact as one short sentence in Vietnamese, addressed to the employee.
If no chunk states the answer, return {"points": []}. This is a correct answer, not a failure: the system then tells the employee whom to contact.
</output_format>"""


class _LoosePoint(BaseModel):
    chunks: list[str]
    quote: str
    text: str


class _LooseAnswer(BaseModel):
    points: list[_LoosePoint]


@dataclass(frozen=True)
class Reply:
    retrieved: tuple[str, ...]          # chunk ids, best first
    points: tuple[Point, ...] | None    # None: the output was not valid JSON of the contract
    raw: str                            # the model's text, for the log


class AnswerUnavailable(RuntimeError):
    """Gemini (answer or query embedding) failed after retries; the page shows a 503, never a card."""


def answer_schema(ids: tuple[str, ...]) -> dict:
    """JSON schema of {points: [{chunks, quote, text}]} with chunks an enum of `ids`, min 1 item.

    A Pydantic model is built per request so the enum is the retrieved set, then its
    model_json_schema is handed to the model as a dict (so the JsonOutputParser stays
    loose and an out-of-enum id reaches step 7 rather than being rejected at parse time).
    """
    if not ids:
        raise ValueError("answer_schema needs at least one retrieved id")
    point = create_model(
        "Point",
        chunks=(tuple[Literal[ids], ...], ...),
        quote=(str, ...),
        text=(str, ...),
    )
    answer = create_model("Answer", points=(list[point], Field(min_length=1)))
    schema = answer.model_json_schema()
    # A single-element Literal turns into JSON-schema `const`, which Gemini's enum-only
    # subset does not name; keep an `enum` so the constraint has the same shape every time.
    chunks_items = schema["$defs"]["Point"]["properties"]["chunks"]["items"]
    chunks_items.pop("const", None)
    chunks_items["enum"] = list(ids)
    return schema


def build_messages(hits: list[Hit], scope: Scope, question: str) -> list[BaseMessage]:
    """SystemMessage(SYSTEM_INSTRUCTION) and the user turn: chunks in hit order, the
    asker line, then the question last (ADR 0003, decision 1)."""
    by_doc = {d.id: d for d in scope.documents}
    lines = ["<context>"]
    for hit in hits:
        chunk = hit.chunk
        document = by_doc[chunk.document_id]
        attrs = [f'id="{chunk.id}"', f'document="{document.title}"']
        if chunk.label:
            attrs.append(f'clause="{chunk.label}"')
        lines.append(f"<chunk {' '.join(attrs)}>{chunk.text}</chunk>")
    lines.append("</context>")
    lines.append(f"<asker>Nhân sự {scope.persona.company}, {scope.persona.unit}.</asker>")
    lines.append("")
    lines.append("Based on the information above, answer this question:")
    lines.append(f"<question>{question}</question>")
    return [SystemMessage(content=SYSTEM_INSTRUCTION), HumanMessage(content="\n".join(lines))]


def _raw_text(raw) -> str:
    content = getattr(raw, "content", None) or ""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for part in content:
            if isinstance(part, str):
                parts.append(part)
            elif isinstance(part, dict) and "text" in part:
                parts.append(part["text"])
        return "".join(parts)
    return str(content)


def _parse_points(parsed) -> tuple[Point, ...] | None:
    if parsed is None:
        return None
    try:
        loose = _LooseAnswer.model_validate(parsed)
    except ValidationError:
        return None
    return tuple(
        Point(chunks=tuple(p.chunks), quote=p.quote, text=p.text) for p in loose.points
    )


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

        raw = _raw_text(result.get("raw"))
        if result.get("parsing_error") is not None:
            points = None
        else:
            points = _parse_points(result.get("parsed"))
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


def gemini_chat(settings: Llm) -> ChatGoogleGenerativeAI:
    """The chat model, with the key read from GEMINI_API_KEY only and no sampling (ADR 0003)."""
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        raise RuntimeError("GEMINI_API_KEY is not set; set it to a Gemini API key to answer questions")
    return ChatGoogleGenerativeAI(
        model=settings.model,
        google_api_key=key,
        thinking_level=settings.thinking_level,
        max_retries=settings.max_retries,
        timeout=settings.timeout_seconds,
        cache=False,
        rate_limiter=InMemoryRateLimiter(requests_per_second=settings.requests_per_minute / 60.0),
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    config = load_config()
    documents = load_documents()
    personas = load_personas(load_org())
    if not os.environ.get("GEMINI_API_KEY"):
        sys.exit("GEMINI_API_KEY is not set; set it to a Gemini API key to run the manual check")
    if len(sys.argv) != 4:
        sys.exit("usage: python -m app.answer <persona> <as_of> <question>")
    persona_id, as_of_text, question = sys.argv[1], sys.argv[2], sys.argv[3]
    if persona_id not in personas:
        sys.exit(f"unknown persona {persona_id}")
    as_of = date.fromisoformat(as_of_text)
    index = build_index(documents, gemini_embeddings(config.retrieval.embedding_model))
    scoped = build_scope(personas[persona_id], as_of, documents)
    answerer = Answerer(index, gemini_chat(config.llm), config.retrieval)
    try:
        reply = answerer(scoped, question)
    except AnswerUnavailable as exc:
        sys.exit(f"unavailable: {exc}")
    print(f"retrieved: {list(reply.retrieved)}")
    print(f"raw: {reply.raw}")
    if reply.points is None:
        print("points: malformed output")
    else:
        for point in reply.points:
            print(f"  chunks={list(point.chunks)} quote={point.quote!r} text={point.text!r}")
    card = card_for_answer(scoped, reply.retrieved, reply.points)
    print(f"card: {card.kind} reason={card.reason!r}")