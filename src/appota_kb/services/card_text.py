"""The three cards' lines of text, word for word from the submitted document (Phần 2).

No FastAPI and no LLM here: the page and the templates render these lines.
ADR 0004 drops the "Báo sai" button; #15 later adds the "Đã ghi nhận" line (recorded=True).
"""
from appota_kb.models.answer import Point
from appota_kb.models.card import Card
from appota_kb.models.document import Chunk, Document
from appota_kb.models.org import Persona
from appota_kb.models.scope import Scope
from appota_kb.services.citations import card_for_answer, conflict_quotes

REFUSAL_TEXT = (
    "Hệ thống không tìm thấy quy định phù hợp để trả lời câu hỏi này cho bạn.\n"
    "Hệ thống chỉ trả lời các quy định áp dụng cho bạn. Vui lòng liên hệ {hr}."
)

CONFLICT_HEADLINE = (
    "Có hai quy định cùng áp dụng cho bạn nhưng chưa được khai báo quan hệ với nhau. "
    "Hệ thống không tự chọn."
)


def intro(persona: Persona) -> str:
    return f"Bạn đang hỏi với tư cách: nhân sự {persona.company}, {persona.unit}."


def _dmy(doc: Document) -> str:
    return doc.effective_from.strftime("%d/%m/%Y")


def _source_line(doc: Document, doc_chunks: tuple[Chunk, ...], hr: str) -> str:
    line = f"Nguồn: {doc.title}"
    labels = [c.label for c in doc_chunks if c.label]
    if labels:
        line += ", " + ", ".join(labels)
    return f"{line}, hiệu lực từ {_dmy(doc)}. Hỏi thêm: {hr}."


def _quote_line(doc: Document, chunk: Chunk) -> str:
    label = f", {chunk.label}" if chunk.label else ""
    return f'{doc.applies_to}{label} (từ {_dmy(doc)}): "{chunk.text}"'


def _group_cited(cited: tuple[Chunk, ...]) -> list[tuple[str, tuple[Chunk, ...]]]:
    order: list[str] = []
    by_doc: dict[str, list[Chunk]] = {}
    for chunk in cited:
        if chunk.document_id not in by_doc:
            by_doc[chunk.document_id] = []
            order.append(chunk.document_id)
        by_doc[chunk.document_id].append(chunk)
    return [(doc_id, tuple(by_doc[doc_id])) for doc_id in order]


def answer_card(card: Card, scope: Scope, points: tuple[Point, ...]) -> tuple[str, ...]:
    docs = {d.id: d for d in scope.documents}
    answer = " ".join(p.text.strip() for p in points)
    lines = [intro(scope.persona), answer]
    for doc_id, doc_chunks in _group_cited(card.cited):
        lines.append(_source_line(docs[doc_id], doc_chunks, card.hr))
    return tuple(lines)


def conflict_card(card: Card, scope: Scope, quotes, recorded: bool) -> tuple[str, ...]:
    lines = [intro(scope.persona), CONFLICT_HEADLINE]
    for (a, b), (left, right) in zip(card.conflicts, quotes):
        for doc, doc_chunks in ((a, left), (b, right)):
            for chunk in doc_chunks:
                lines.append(_quote_line(doc, chunk))
    lines.append(f"Vui lòng hỏi {card.hr}.")
    if recorded:
        owners: list[str] = []
        for a, b in card.conflicts:
            for doc in (a, b):
                if doc.owner not in owners:
                    owners.append(doc.owner)
        lines.append("Đã ghi nhận để " + " và ".join(owners) + " xác nhận.")
    return tuple(lines)


def refusal_text(card: Card) -> str:
    return REFUSAL_TEXT.format(hr=card.hr)


def refusal_card(card: Card, scope: Scope) -> tuple[str, ...]:
    return (intro(scope.persona),) + tuple(refusal_text(card).splitlines())


def render(
    card: Card,
    scope: Scope,
    points: tuple[Point, ...] | None,
    retrieved: tuple[Chunk, ...],
    recorded: bool = False,
) -> tuple[str, ...]:
    if card.kind == "answer":
        return answer_card(card, scope, tuple(points or ()))
    if card.kind == "conflict":
        return conflict_card(card, scope, conflict_quotes(card, retrieved), recorded)
    return refusal_card(card, scope)


def show(scope: Scope, retrieved: tuple[str, ...], points: tuple[Point, ...] | None) -> tuple[Card, tuple[str, ...]]:
    """Step 7 and the card's lines, exactly as the page shows them; used by app.web and eval.run."""
    card = card_for_answer(scope, retrieved, points)
    by_id = {c.id: c for c in scope.chunks}
    return card, render(card, scope, points, tuple(by_id[cid] for cid in retrieved))
