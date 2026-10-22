"""Step 6's output contract: the JSON schema handed to the model and the parsing of its reply.

Parsing stays loose so an out-of-enum chunk id reaches step 7 as data rather than failing here,
and a missing or malformed `disagreement` is an empty flag rather than a refusal (ADR 0014).
One answer covers the whole question; the points are only the quotes that support it (ADR 0018).
"""
from typing import Literal

from pydantic import BaseModel, Field, ValidationError, create_model

from appota_kb.models.answer import Point


class _LoosePoint(BaseModel):
    quote: str
    chunks: list[str]


class _LooseAnswer(BaseModel):
    answer: str
    points: list[_LoosePoint]


def answer_schema(ids: tuple[str, ...]) -> dict:
    """JSON schema of {answer, points: [{quote, chunks}], disagreement: [id, ...]} with chunks an enum
    of `ids`, min 1 item; `points` may be empty, which means "không tìm thấy". `disagreement` is
    required, at most 2 ids of the same enum, and empty when no two clauses disagree (ADR 0014).

    A Pydantic model is built per request so the enum is the retrieved set, then its
    model_json_schema is handed to the model as a dict (so the JsonOutputParser stays
    loose and an out-of-enum id reaches step 7 rather than being rejected at parse time).
    """
    if not ids:
        raise ValueError("answer_schema needs at least one retrieved id")
    point = create_model(
        "Point",
        quote=(str, ...),
        chunks=(tuple[Literal[ids], ...], Field(min_length=1)),
    )
    answer = create_model(
        "Answer",
        answer=(str, ...),
        points=(list[point], ...),
        disagreement=(tuple[Literal[ids], ...], Field(max_length=2)),
    )
    schema = answer.model_json_schema()
    # A single-element Literal turns into JSON-schema `const`, which Gemini's enum-only
    # subset does not name; keep an `enum` so the constraint has the same shape every time.
    chunks_items = schema["$defs"]["Point"]["properties"]["chunks"]["items"]
    chunks_items.pop("const", None)
    chunks_items["enum"] = list(ids)
    flag_items = schema["properties"]["disagreement"]["items"]
    flag_items.pop("const", None)
    flag_items["enum"] = list(ids)
    return schema


def raw_text(raw) -> str:
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


def parse_reply(parsed) -> tuple[str, tuple[Point, ...] | None]:
    """The answer and its points, or ("", None) when the reply is malformed.

    A missing `answer`, or an empty one while `points` is not empty, is malformed (ADR 0018):
    the card would otherwise show quotes with no answer. Empty points with an empty answer
    stay a valid "không tìm thấy" reply, which step 7 turns into a refusal.
    """
    if parsed is None:
        return "", None
    try:
        loose = _LooseAnswer.model_validate(parsed)
    except ValidationError:
        return "", None
    answer = loose.answer.strip()
    if not answer and loose.points:
        return "", None
    points = tuple(Point(quote=p.quote, chunks=tuple(p.chunks)) for p in loose.points)
    return answer, points


def parse_disagreement(parsed) -> tuple[str, ...]:
    """The ids of the model's `disagreement`; a missing or malformed field is an empty tuple.

    The list is kept whole, even above two ids: step 7 decides whether the flag is valid.
    """
    if not isinstance(parsed, dict):
        return ()
    flag = parsed.get("disagreement")
    if not isinstance(flag, list) or not all(isinstance(cid, str) for cid in flag):
        return ()
    return tuple(flag)
