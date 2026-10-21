"""The three cards' lines: fixed wording from the submitted document (Phần 2), plus each answer point's sentence.

No FastAPI and no LLM here: the page and the templates render these lines.
Each answer point shows the model's sentence above the quote that step 7 checked (ADR 0011).
The conflict and refusal cards keep fixed wording and show no model text.
A refusal's wording is picked from the card's reason by a fixed mapping, never from model text (ADR 0017).
A document that leaves the asker's scope later gets the end of its window on the source line and a
"Sắp thay đổi" notice under it, from the rules only (ADR 0012).
A source line and a conflict quote carry the ids of the chunks they cite, so the page can link them to the
cited version (#77); the conflict quote names its document's title.
ADR 0004 drops the "Báo sai" button; #15 later adds the "Đã ghi nhận" line (recorded=True).
"""
from datetime import date

from appota_kb.models.answer import Point
from appota_kb.models.card import Card, CardLine
from appota_kb.models.document import Chunk, Document
from appota_kb.models.org import Persona
from appota_kb.models.scope import Change, Scope
from appota_kb.services.citations import conflict_quotes, fold

# Text 1: no points. The same for "not allowed" and "not found", and it reveals nothing (R10).
REFUSAL_TEXT = (
    "Hệ thống không tìm thấy quy định phù hợp để trả lời câu hỏi này cho bạn.\n"
    "Hệ thống chỉ trả lời các quy định áp dụng cho bạn. Vui lòng liên hệ {hr}."
)
# Text 2: the model answered and step 7 could not verify the answer. It never says that a rule exists.
REFUSAL_TEXT_NOT_VERIFIED = (
    "Hệ thống không đối chiếu được câu trả lời với nguyên văn quy định nên không đưa ra câu trả lời.\n"
    "Bạn có thể hỏi lại hoặc liên hệ {hr}."
)
# Text 3: the model's output could not be read.
REFUSAL_TEXT_ERROR = (
    "Hệ thống gặp lỗi khi tạo câu trả lời.\n"
    "Vui lòng thử lại; nếu vẫn lỗi, liên hệ {hr}."
)
# Any other reason, including None and one added later, reads text 1, the text that reveals nothing.
REFUSAL_TEXT_BY_REASON = {
    "quote_mismatch": REFUSAL_TEXT_NOT_VERIFIED,
    "outside_retrieved": REFUSAL_TEXT_NOT_VERIFIED,
    "malformed": REFUSAL_TEXT_ERROR,
}

CONFLICT_HEADLINE = (
    "Có {n} quy định cùng áp dụng cho bạn nhưng chưa được khai báo quy định nào được dùng thay quy định nào. "
    "Hệ thống không tự chọn."
)


def intro(persona: Persona) -> str:
    return f"Bạn đang hỏi với tư cách: nhân sự {persona.company}, {persona.unit}."


NOTICE_LABEL = "Sắp thay đổi: "

ANSWER_NOTE = "Câu in đậm là diễn giải của hệ thống; đoạn trong ngoặc kép là nguyên văn quy định đã được đối chiếu."


def dmy(day: date) -> str:
    return day.strftime("%d/%m/%Y")


def validity_window(doc: Document, change: Change | None) -> str:
    """"từ 01/01/2026", plus " đến hết 31/12/2026" when the document leaves this asker's scope later."""
    text = f"từ {dmy(doc.effective_from)}"
    if change is not None:
        text += f" đến hết {dmy(change.last_day)}"
    return text


def change_text(doc: Document, change: Change, hr: str) -> str:
    """What happens after the last day, without the label. Names only documents in the asker's scope,
    so a successor the asker may not read gives the same text as no successor (R10, ADR 0010)."""
    day = dmy(change.next_day)
    if not change.successors:
        return (
            f"quy định này hết hiệu lực với bạn sau {dmy(change.last_day)}. "
            f"Vui lòng hỏi {hr} về quy định áp dụng từ {day}."
        )
    versions = " và ".join(s.title for s in change.successors if s.series == doc.series)
    others = " và ".join(s.title for s in change.successors if s.series != doc.series)
    parts = []
    if versions:
        parts.append(f"{versions} áp dụng từ {day}")
    if others:
        parts.append(f"từ {day}, {others} dùng thay quy định này")
    return "; ".join(parts) + "."


def _notice_lines(doc: Document, scope: Scope, hr: str) -> tuple[CardLine, ...]:
    change = scope.change_for(doc.id)
    if change is None:
        return ()
    return (CardLine("notice", NOTICE_LABEL + change_text(doc, change, hr)),)


def _ref(doc: Document, labels: list[str]) -> str:
    """"Quy chế nghỉ phép GameCo (bản 2), Điều 2": the title and the Điều, the part a line links from."""
    return ", ".join([doc.title, *labels])


def _source_line(doc: Document, doc_chunks: tuple[Chunk, ...], scope: Scope, hr: str) -> CardLine:
    ref = _ref(doc, [c.label for c in doc_chunks if c.label])
    text = f"Nguồn: {ref}, hiệu lực {validity_window(doc, scope.change_for(doc.id))}. Hỏi thêm: {hr}."
    return CardLine("source", text, tuple(c.id for c in doc_chunks), ref)


def _quote_line(doc: Document, chunk: Chunk, scope: Scope) -> CardLine:
    ref = _ref(doc, [chunk.label] if chunk.label else [])
    window = validity_window(doc, scope.change_for(doc.id))
    text = f'{ref} ({window}, áp dụng cho {doc.applies_to}): "{chunk.text}"'
    return CardLine("quote", text, (chunk.id,), ref)


def _group_cited(cited: tuple[Chunk, ...]) -> list[tuple[str, tuple[Chunk, ...]]]:
    order: list[str] = []
    by_doc: dict[str, list[Chunk]] = {}
    for chunk in cited:
        if chunk.document_id not in by_doc:
            by_doc[chunk.document_id] = []
            order.append(chunk.document_id)
        by_doc[chunk.document_id].append(chunk)
    return [(doc_id, tuple(by_doc[doc_id])) for doc_id in order]


def answer_card(card: Card, scope: Scope, points: tuple[Point, ...]) -> tuple[CardLine, ...]:
    """One claim, its folded quote and its source line(s) per point, in the model's order."""
    docs = {d.id: d for d in scope.documents}
    by_id = {c.id: c for c in scope.chunks}
    lines = [CardLine("who", intro(scope.persona)), CardLine("note", ANSWER_NOTE)]
    for point in points:
        lines.append(CardLine("claim", point.claim))
        lines.append(CardLine("quote", f'"{fold(point.quote)}"'))
        cited = tuple(by_id[cid] for cid in dict.fromkeys(point.chunks))
        for doc_id, doc_chunks in _group_cited(cited):
            lines.append(_source_line(docs[doc_id], doc_chunks, scope, card.hr))
            lines.extend(_notice_lines(docs[doc_id], scope, card.hr))
    return tuple(lines)


def conflict_card(card: Card, scope: Scope, quotes, recorded: bool) -> tuple[CardLine, ...]:
    headline = CONFLICT_HEADLINE.format(n=len(quotes))
    lines = [CardLine("who", intro(scope.persona)), CardLine("lead", headline)]
    for doc, doc_chunks in quotes:
        for chunk in doc_chunks:
            lines.append(_quote_line(doc, chunk, scope))
        lines.extend(_notice_lines(doc, scope, card.hr))
    lines.append(CardLine("plain", f"Vui lòng hỏi {card.hr}."))
    if recorded:
        owners: list[str] = []
        for a, b in card.conflicts:
            for doc in (a, b):
                if doc.owner not in owners:
                    owners.append(doc.owner)
        lines.append(CardLine("plain", "Đã ghi nhận để " + " và ".join(owners) + " xác nhận."))
    return tuple(lines)


def refusal_text(card: Card) -> str:
    return REFUSAL_TEXT_BY_REASON.get(card.reason, REFUSAL_TEXT).format(hr=card.hr)


def refusal_card(card: Card, scope: Scope) -> tuple[CardLine, ...]:
    text = refusal_text(card).splitlines()
    return (
        CardLine("who", intro(scope.persona)),
        CardLine("lead", text[0]),
        *(CardLine("plain", line) for line in text[1:]),
    )


def render(
    card: Card,
    scope: Scope,
    points: tuple[Point, ...] | None,
    retrieved: tuple[Chunk, ...],
    recorded: bool = False,
) -> tuple[CardLine, ...]:
    if card.kind == "answer":
        return answer_card(card, scope, tuple(points or ()))
    if card.kind == "conflict":
        return conflict_card(card, scope, conflict_quotes(card, retrieved), recorded)
    return refusal_card(card, scope)
