"""The three cards' wording, word for word from the submitted document (Phần 2)."""
from dataclasses import replace
from datetime import date

import pytest

from appota_kb.evaluation.data_edit import with_edit
from appota_kb.models.answer import Point
from appota_kb.models.card import Card, CardLine
from appota_kb.services.card_text import (
    ANSWER_NOTE,
    REFUSAL_TEXT,
    REFUSAL_TEXT_ERROR,
    REFUSAL_TEXT_NOT_VERIFIED,
    change_text,
    refusal_text,
    render,
)
from appota_kb.services.chunking import chunks
from appota_kb.services.citations import pick_card
from appota_kb.services.scope import scope


def _doc(documents, doc_id):
    return next(d for d in documents if d.id == doc_id)


def _chunk(documents, chunk_id):
    doc_id, number = chunk_id.rsplit("#", 1)
    return next(c for c in chunks(_doc(documents, doc_id)) if c.id == chunk_id)


def test_answer_card_wording(personas, documents):
    persona = personas["minh"]
    s = scope(persona, date(2026, 10, 7), documents)
    c2 = _chunk(documents, "LEAVE-GAMECO-v2#2")
    card = Card("answer", persona.hr, (c2,), ())
    point = Point(
        quote=c2.text,
        chunks=("LEAVE-GAMECO-v2#2",),
    )
    answer = "Theo Quy chế nghỉ phép GameCo (bản 2), bạn được nghỉ phép năm 14 ngày mỗi năm."
    lines = render(card, s, (point,), (c2,), answer=answer)
    assert lines == (
        CardLine("who", "Bạn đang hỏi với tư cách: nhân sự GameCo, Studio."),
        CardLine("note", ANSWER_NOTE),
        CardLine("claim", answer),
        CardLine("quote", '"Nhân sự GameCo được nghỉ phép năm 14 ngày mỗi năm."'),
        CardLine(
            "source",
            "Nguồn: Quy chế nghỉ phép GameCo (bản 2), Điều 2, hiệu lực từ 01/01/2026 đến hết 31/12/2026. Hỏi thêm: HR GameCo.",
            ("LEAVE-GAMECO-v2#2",),
            "Quy chế nghỉ phép GameCo (bản 2), Điều 2",
        ),
        CardLine("notice", "Sắp thay đổi: Quy chế nghỉ phép GameCo (bản 3) áp dụng từ 01/01/2027."),
    )


def test_answer_card_folds_each_points_quote(personas, documents):
    persona = personas["minh"]
    s = scope(persona, date(2026, 10, 7), documents)
    c2 = _chunk(documents, "LEAVE-GAMECO-v2#2")
    card = Card("answer", persona.hr, (c2,), ())
    spaced = "  Nhân sự GameCo được nghỉ phép năm\n14 ngày mỗi năm.  "
    point = Point(quote=spaced, chunks=("LEAVE-GAMECO-v2#2",))
    lines = render(card, s, (point, point), (c2,), answer="Một câu.")
    quotes = [line.text for line in lines if line.kind == "quote"]
    assert quotes == ['"Nhân sự GameCo được nghỉ phép năm 14 ngày mỗi năm."'] * 2


def test_answer_card_gives_each_point_its_own_source_line(personas, documents):
    persona = personas["ha"]
    s = scope(persona, date(2026, 10, 7), documents)
    g1 = _chunk(documents, "LEAVE-GROUP-v1#1")
    p1 = _chunk(documents, "LEAVE-PAYCO-v1#1")
    card = Card("answer", persona.hr, (g1, p1), ())
    points = (
        Point(quote=g1.text, chunks=(g1.id,)),
        Point(quote=p1.text, chunks=(p1.id,)),
    )
    lines = render(card, s, points, (g1, p1), answer="Hai quy định ghi 12 và 13 ngày.")
    assert [line.kind for line in lines] == [
        "who", "note", "claim", "quote", "source", "quote", "source"
    ]
    assert lines[2].text == "Hai quy định ghi 12 và 13 ngày."
    assert lines[4].text.startswith("Nguồn: Quy chế nghỉ phép Tập đoàn")
    assert lines[6].text.startswith("Nguồn: Quy chế nghỉ phép PayCo")


def test_answer_card_has_exactly_one_claim_line_before_every_quote(personas, documents):
    persona = personas["ha"]
    s = scope(persona, date(2026, 10, 7), documents)
    g1 = _chunk(documents, "LEAVE-GROUP-v1#1")
    p1 = _chunk(documents, "LEAVE-PAYCO-v1#1")
    card = Card("answer", persona.hr, (g1, p1), ())
    points = (Point(quote=g1.text, chunks=(g1.id,)), Point(quote=p1.text, chunks=(p1.id,)))
    lines = render(card, s, points, (g1, p1), answer="Một câu trả lời cho cả hai phần.")
    claim_positions = [i for i, line in enumerate(lines) if line.kind == "claim"]
    quote_positions = [i for i, line in enumerate(lines) if line.kind == "quote"]
    assert claim_positions == [2]
    assert all(2 < position for position in quote_positions)
    assert [line.text for line in lines if line.kind == "claim"] == ["Một câu trả lời cho cả hai phần."]


def test_conflict_card_wording(personas, documents):
    persona = personas["ha"]
    s = scope(persona, date(2026, 10, 7), documents)
    group = _doc(documents, "LEAVE-GROUP-v1")
    payco = _doc(documents, "LEAVE-PAYCO-v1")
    g1 = _chunk(documents, "LEAVE-GROUP-v1#1")
    p1 = _chunk(documents, "LEAVE-PAYCO-v1#1")
    card = Card("conflict", persona.hr, (g1,), ((group, payco),))
    marker = Point(
        quote="MODEL QUOTE MUST NOT APPEAR",
        chunks=("LEAVE-GROUP-v1#1",),
    )
    lines = render(card, s, (marker,), (g1, p1), answer="MODEL ANSWER MUST NOT APPEAR")
    assert lines == (
        CardLine("who", "Bạn đang hỏi với tư cách: nhân sự PayCo, Kế toán."),
        CardLine("lead", "Có 2 quy định cùng áp dụng cho bạn nhưng chưa được khai báo quy định nào được dùng thay quy định nào. Hệ thống không tự chọn."),
        CardLine(
            "quote",
            'Quy chế nghỉ phép Tập đoàn, Điều 1 (từ 01/01/2024, áp dụng cho Tập đoàn): "Nhân sự chính thức của Tập đoàn được nghỉ phép năm 12 ngày mỗi năm."',
            ("LEAVE-GROUP-v1#1",),
            "Quy chế nghỉ phép Tập đoàn, Điều 1",
        ),
        CardLine(
            "quote",
            'Quy chế nghỉ phép PayCo, Điều 1 (từ 01/01/2025, áp dụng cho PayCo): "Nhân sự PayCo được nghỉ phép năm 13 ngày mỗi năm."',
            ("LEAVE-PAYCO-v1#1",),
            "Quy chế nghỉ phép PayCo, Điều 1",
        ),
        CardLine("plain", "Vui lòng hỏi HR PayCo."),
    )
    assert all("MODEL" not in line.text for line in lines)
    assert "claim" not in [line.kind for line in lines]


def test_conflict_card_headline_counts_documents_and_quotes_each_once(personas, documents):
    """P9: a third leave policy for Kế toán makes three pairs, and the card says 3 and quotes three documents."""
    payco = _doc(documents, "LEAVE-PAYCO-v1")
    accounting = replace(
        payco, id="LEAVE-KETOAN-v1", series="LEAVE-KETOAN", title="Quy chế nghỉ phép Kế toán",
        applies_to="Kế toán", body="Điều 1. Nhân sự Kế toán được nghỉ phép năm 14 ngày mỗi năm.\n",
    )
    docs = [*documents, accounting]
    s = scope(personas["ha"], date(2026, 10, 7), docs)
    assert len(s.conflicts) == 3
    ids = ("LEAVE-GROUP-v1#1", "LEAVE-KETOAN-v1#1", "LEAVE-PAYCO-v1#1")
    retrieved = tuple(_chunk(docs, cid) for cid in ids)
    card = pick_card(s, ids, list(ids))
    lines = render(card, s, None, retrieved)
    assert lines[1].text.startswith("Có 3 quy định cùng áp dụng cho bạn")
    quotes = [line.text for line in lines if line.kind == "quote"]
    assert len(quotes) == 3
    assert [q.split(",")[0] for q in quotes] == [
        "Quy chế nghỉ phép Tập đoàn", "Quy chế nghỉ phép Kế toán", "Quy chế nghỉ phép PayCo"
    ]
    assert [line.kind for line in lines] == ["who", "lead", "quote", "quote", "quote", "plain"]


def test_model_flagged_conflict_card_uses_the_same_headline(personas, documents):
    docs = with_edit(documents, {"document": "LEAVE-PAYCO-v1", "set": {"topic": "nghi_phep_nam"}})
    s = scope(personas["ha"], date(2026, 10, 7), docs)
    ids = ("LEAVE-GROUP-v1#1", "LEAVE-PAYCO-v1#1")
    retrieved = tuple(_chunk(docs, cid) for cid in ids)
    group, payco = (_doc(docs, "LEAVE-GROUP-v1"), _doc(docs, "LEAVE-PAYCO-v1"))
    card = Card("conflict", s.persona.hr, retrieved, ((group, payco),), reason="model_flagged")
    declared = render(Card("conflict", s.persona.hr, retrieved, ((group, payco),)), s, None, retrieved)
    assert render(card, s, None, retrieved) == declared
    assert declared[1].text.startswith("Có 2 quy định")


def test_refusal_card_wording(personas, documents):
    persona = personas["minh"]
    s = scope(persona, date(2026, 10, 7), documents)
    card = Card("refusal", persona.hr, (), ())
    lines = render(card, s, None, ())
    assert lines == (
        CardLine("who", "Bạn đang hỏi với tư cách: nhân sự GameCo, Studio."),
        CardLine("lead", "Hệ thống không tìm thấy quy định phù hợp để trả lời câu hỏi này cho bạn."),
        CardLine("plain", "Hệ thống chỉ trả lời các quy định áp dụng cho bạn. Vui lòng liên hệ HR GameCo."),
    )


def test_refusal_text(personas, documents, cases):
    as_of = date(2026, 10, 7)
    cards = {}
    for pid, hr in (("ha", "HR PayCo"), ("minh", "HR GameCo")):
        s = scope(personas[pid], as_of, documents)
        card = pick_card(s, s.chunk_ids, [])
        assert card.kind == "refusal"
        assert card.cited == () and card.conflicts == ()
        assert card.hr == hr
        assert refusal_text(card) == REFUSAL_TEXT.format(hr=hr)
        cards[pid] = card
    assert refusal_text(cards["ha"]).replace("HR PayCo", "X") == refusal_text(cards["minh"]).replace("HR GameCo", "X")
    row10 = next(c for c in cases if c["id"] == 10)
    for text in (refusal_text(cards["ha"]), refusal_text(cards["minh"])):
        for d in documents:
            assert d.id not in text and d.title not in text
        for bad in row10["must_not_contain"]:
            assert bad not in text


REASON_TEXTS = {
    "no_points": REFUSAL_TEXT,
    "quote_mismatch": REFUSAL_TEXT_NOT_VERIFIED,
    "outside_retrieved": REFUSAL_TEXT_NOT_VERIFIED,
    "malformed": REFUSAL_TEXT_ERROR,
    # No reason, or a reason added later, falls back to the text that reveals nothing (R10).
    None: REFUSAL_TEXT,
    "a_reason_added_later": REFUSAL_TEXT,
}


@pytest.mark.parametrize("reason", REASON_TEXTS)
def test_refusal_text_follows_the_reason(personas, reason):
    card = Card("refusal", personas["minh"].hr, (), (), reason=reason)
    assert refusal_text(card) == REASON_TEXTS[reason].format(hr="HR GameCo")


def test_the_three_refusal_texts_are_distinct_and_fixed():
    texts = {REFUSAL_TEXT, REFUSAL_TEXT_NOT_VERIFIED, REFUSAL_TEXT_ERROR}
    assert len(texts) == 3
    for text in texts:
        assert "{hr}" in text
        assert text.format(hr="X").count("X") == 1
    assert REFUSAL_TEXT_NOT_VERIFIED.splitlines() == [
        "Hệ thống không đối chiếu được câu trả lời với nguyên văn quy định nên không đưa ra câu trả lời.",
        "Bạn có thể hỏi lại hoặc liên hệ {hr}.",
    ]
    assert REFUSAL_TEXT_ERROR.splitlines() == [
        "Hệ thống gặp lỗi khi tạo câu trả lời.",
        "Vui lòng thử lại; nếu vẫn lỗi, liên hệ {hr}.",
    ]


@pytest.mark.parametrize("reason", REASON_TEXTS)
def test_no_refusal_names_a_document_or_quotes_a_chunk(personas, documents, reason):
    for persona in personas.values():
        s = scope(persona, date(2026, 10, 7), documents)
        lines = render(Card("refusal", persona.hr, (), (), reason=reason), s, None, ())
        text = " ".join(line.text for line in lines[1:])
        assert persona.hr in text
        for d in documents:
            assert d.id not in text and d.title not in text
        for chunk in s.chunks:
            assert chunk.text not in text
        assert [line.kind for line in lines] == ["who", "lead", "plain"]


# The window end and the notices (ADR 0012).

def _row1_card(personas, documents, as_of):
    persona = personas["minh"]
    s = scope(persona, as_of, documents)
    c2 = _chunk(documents, "LEAVE-GAMECO-v2#2") if as_of < date(2027, 1, 1) else _chunk(documents, "LEAVE-GAMECO-v3#2")
    card = Card("answer", persona.hr, (c2,), ())
    point = Point(quote=c2.text, chunks=(c2.id,))
    return render(card, s, (point,), (c2,), answer="Một câu.")


def test_a_notice_follows_the_source_line_on_each_point(personas, documents):
    persona = personas["minh"]
    s = scope(persona, date(2026, 12, 15), documents)
    c2 = _chunk(documents, "LEAVE-GAMECO-v2#2")
    card = Card("answer", persona.hr, (c2,), ())
    point = Point(quote=c2.text, chunks=(c2.id,))
    lines = render(card, s, (point, point), (c2,), answer="Một câu.")
    assert [line.kind for line in lines] == ["who", "note", "claim", "quote", "source", "notice", "quote", "source", "notice"]
    assert lines[4].text.endswith("hiệu lực từ 01/01/2026 đến hết 31/12/2026. Hỏi thêm: HR GameCo.")


def test_no_window_end_and_no_notice_once_the_next_version_applies(personas, documents):
    lines = _row1_card(personas, documents, date(2027, 1, 1))
    assert [line.kind for line in lines] == ["who", "note", "claim", "quote", "source"]
    assert lines[4].text == "Nguồn: Quy chế nghỉ phép GameCo (bản 3), Điều 2, hiệu lực từ 01/01/2027. Hỏi thêm: HR GameCo."


def test_a_document_with_no_change_shows_the_start_only(personas, documents):
    persona = personas["lan"]
    s = scope(persona, date(2026, 10, 7), documents)
    c1 = _chunk(documents, "LEAVE-GROUP-v1#1")
    lines = render(Card("answer", persona.hr, (c1,), ()), s, (Point(c1.text, (c1.id,)),), (c1,), answer="Một câu.")
    assert [line.kind for line in lines] == ["who", "note", "claim", "quote", "source"]
    assert "đến hết" not in lines[4].text


def _edited_scope(personas, documents, edit, as_of=date(2026, 10, 7)):
    edited = [edit(d) for d in documents]
    return edited, scope(personas["minh"], as_of, edited)


def test_notice_for_an_end_date_with_no_successor(personas, documents):
    edited, s = _edited_scope(
        personas, documents, lambda d: replace(d, effective_to=date(2026, 12, 31)) if d.id == "OT-GAMECO-v1" else d
    )
    doc = _doc(edited, "OT-GAMECO-v1")
    assert change_text(doc, s.change_for(doc.id), "HR GameCo") == (
        "quy định này hết hiệu lực với bạn sau 31/12/2026. Vui lòng hỏi HR GameCo về quy định áp dụng từ 01/01/2027."
    )


def test_a_hidden_successor_gives_the_text_of_no_successor(personas, documents):
    """R10, ADR 0010: the notice must not reveal that a restricted document exists."""
    ended = lambda d: replace(d, effective_to=date(2026, 12, 31)) if d.id == "LEAVE-GAMECO-v2" else d  # noqa: E731
    hidden = lambda d: replace(d, access="roles:hr_gameco") if d.id == "LEAVE-GAMECO-v3" else ended(d)  # noqa: E731
    _, none_s = _edited_scope(personas, [d for d in documents if d.id != "LEAVE-GAMECO-v3"], ended)
    _, hidden_s = _edited_scope(personas, documents, hidden)
    doc = _doc(documents, "LEAVE-GAMECO-v2")
    a = change_text(doc, none_s.change_for(doc.id), "HR GameCo")
    b = change_text(doc, hidden_s.change_for(doc.id), "HR GameCo")
    assert a == b
    assert "bản 3" not in b


def test_notice_for_a_dung_thay_by_another_policy(personas, documents):
    persona = personas["lan"]
    group = _doc(documents, "LEAVE-GROUP-v1")
    later = replace(_doc(documents, "LEAVE-GAMECO-v2"), applies_to="Tập đoàn", effective_from=date(2026, 12, 1))
    s = scope(persona, date(2026, 10, 7), [d for d in documents if d.id != "LEAVE-GAMECO-v2"] + [later])
    change = s.change_for(group.id)
    assert change.last_day == date(2026, 11, 30)
    assert change_text(group, change, "HR Tập đoàn") == "từ 01/12/2026, Quy chế nghỉ phép GameCo (bản 2) dùng thay quy định này."


def test_conflict_card_shows_the_window_and_each_sides_notice(personas, documents):
    persona = personas["ha"]
    edited = [replace(d, effective_to=date(2026, 12, 31)) if d.id == "LEAVE-PAYCO-v1" else d for d in documents]
    s = scope(persona, date(2026, 10, 7), edited)
    group = _doc(edited, "LEAVE-GROUP-v1")
    payco = _doc(edited, "LEAVE-PAYCO-v1")
    g1 = _chunk(edited, "LEAVE-GROUP-v1#1")
    p1 = _chunk(edited, "LEAVE-PAYCO-v1#1")
    card = Card("conflict", persona.hr, (g1,), ((group, payco),))
    lines = render(card, s, None, (g1, p1))
    assert [line.kind for line in lines] == ["who", "lead", "quote", "quote", "notice", "plain"]
    assert lines[2].text.startswith("Quy chế nghỉ phép Tập đoàn, Điều 1 (từ 01/01/2024, áp dụng cho Tập đoàn): ")
    assert lines[3].text.startswith("Quy chế nghỉ phép PayCo, Điều 1 (từ 01/01/2025 đến hết 31/12/2026, áp dụng cho PayCo): ")
    assert lines[4].text == (
        "Sắp thay đổi: quy định này hết hiệu lực với bạn sau 31/12/2026. "
        "Vui lòng hỏi HR PayCo về quy định áp dụng từ 01/01/2027."
    )
    assert lines[1].text.startswith("Có 2 quy định cùng áp dụng")


def test_refusal_card_has_no_window_and_no_notice(personas, documents):
    persona = personas["minh"]
    s = scope(persona, date(2026, 12, 15), documents)
    lines = render(Card("refusal", persona.hr, (), ()), s, None, ())
    assert [line.kind for line in lines] == ["who", "lead", "plain"]
    assert all("Sắp thay đổi" not in line.text and "đến hết" not in line.text for line in lines)
