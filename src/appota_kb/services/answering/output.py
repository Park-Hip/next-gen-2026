"""Step 6's output contract: the JSON schema handed to the model and the parsing of its reply.

Parsing stays loose so an out-of-enum chunk id reaches step 7 as data rather than failing here.
"""
from typing import Literal

from pydantic import BaseModel, Field, ValidationError, create_model

from appota_kb.models.answer import Point


class _LoosePoint(BaseModel):
    chunks: list[str]
    quote: str
    text: str


class _LooseAnswer(BaseModel):
    points: list[_LoosePoint]


def answer_schema(ids: tuple[str, ...]) -> dict:
    """JSON schema of {points: [{chunks, quote, text}]} with chunks an enum of `ids`, min 1 item;
    `points` may be empty, which means "không tìm thấy".

    A Pydantic model is built per request so the enum is the retrieved set, then its
    model_json_schema is handed to the model as a dict (so the JsonOutputParser stays
    loose and an out-of-enum id reaches step 7 rather than being rejected at parse time).
    """
    if not ids:
        raise ValueError("answer_schema needs at least one retrieved id")
    point = create_model(
        "Point",
        chunks=(tuple[Literal[ids], ...], Field(min_length=1)),
        quote=(str, ...),
        text=(str, ...),
    )
    answer = create_model("Answer", points=(list[point], ...))
    schema = answer.model_json_schema()
    # A single-element Literal turns into JSON-schema `const`, which Gemini's enum-only
    # subset does not name; keep an `enum` so the constraint has the same shape every time.
    chunks_items = schema["$defs"]["Point"]["properties"]["chunks"]["items"]
    chunks_items.pop("const", None)
    chunks_items["enum"] = list(ids)
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


def parse_points(parsed) -> tuple[Point, ...] | None:
    if parsed is None:
        return None
    try:
        loose = _LooseAnswer.model_validate(parsed)
    except ValidationError:
        return None
    return tuple(
        Point(chunks=tuple(p.chunks), quote=p.quote, text=p.text) for p in loose.points
    )
