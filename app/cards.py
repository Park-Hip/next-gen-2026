"""The three cards' lines of text, word for word from the submitted document (Phần 2).

No FastAPI and no LLM here: the page and the templates render these lines.
ADR 0004 drops the "Báo sai" button; #15 later adds the "Đã ghi nhận" line (recorded=True).
"""
from app.data import Chunk, Document, Persona
from app.rules import Card, Scope, conflict_quotes, refusal_text

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


def answer_card(card: Card, scope: Scope, text: str) -> tuple[str, ...]:
    docs = {d.id: d for d in scope.documents}
    lines = [intro(scope.persona), text]
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


def refusal_card(card: Card, scope: Scope) -> tuple[str, ...]:
    return (intro(scope.persona),) + tuple(refusal_text(card).splitlines())


def render(
    card: Card,
    scope: Scope,
    answer_text: str | None,
    retrieved: tuple[Chunk, ...],
    recorded: bool = False,
) -> tuple[str, ...]:
    if card.kind == "answer":
        return answer_card(card, scope, answer_text or "")
    if card.kind == "conflict":
        return conflict_card(card, scope, conflict_quotes(card, retrieved), recorded)
    return refusal_card(card, scope)