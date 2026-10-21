"""The three cards' wording, word for word from the submitted document (Phần 2)."""
from dataclasses import replace
from datetime import date

from appota_kb.evaluation.data_edit import with_edit
from appota_kb.models.answer import Point
from appota_kb.models.card import Card, CardLine
from appota_kb.services.card_text import REFUSAL_TEXT, change_text, refusal_text, render
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
        claim="Theo Quy chế nghỉ phép GameCo (bản 2), bạn được nghỉ phép năm 14 ngày mỗi năm.",
        quote=c2.text,
        chunks=("LEAVE-GAMECO-v2#2",),
    )
    lines = render(card, s, (point,), (c2,))
    assert lines == (
        CardLine("who", "Bạn đang hỏi với tư cách: nhân sự GameCo, Studio."),
        CardLine("claim", "Theo Quy chế nghỉ phép GameCo (bản 2), bạn được nghỉ phép năm 14 ngày mỗi năm."),
        CardLine("quote", '"Nhân sự GameCo được nghỉ phép năm 14 ngày mỗi năm."'),
        CardLine("source", "Nguồn: Quy chế nghỉ phép GameCo (bản 2), Điều 2, hiệu lực từ 01/01/2026 đến hết 31/12/2026. Hỏi thêm: HR GameCo."),
        CardLine("notice", "Sắp thay đổi: Quy chế nghỉ phép GameCo (bản 3) áp dụng từ 01/01/2027."),
    )


def test_answer_card_folds_each_points_quote(personas, documents):
    persona = personas["minh"]
    s = scope(persona, date(2026, 10, 7), documents)
    c2 = _chunk(documents, "LEAVE-GAMECO-v2#2")
    card = Card("answer", persona.hr, (c2,), ())
    spaced = "  Nhân sự GameCo được nghỉ phép năm\n14 ngày mỗi năm.  "
    point = Point(claim="Theo quy chế, 14 ngày.", quote=spaced, chunks=("LEAVE-GAMECO-v2#2",))
    lines = render(card, s, (point, point), (c2,))
    quotes = [line.text for line in lines if line.kind == "quote"]
    assert quotes == ['"Nhân sự GameCo được nghỉ phép năm 14 ngày mỗi năm."'] * 2


def test_answer_card_gives_each_point_its_own_source_line(personas, documents):
    persona = personas["ha"]
    s = scope(persona, date(2026, 10, 7), documents)
    g1 = _chunk(documents, "LEAVE-GROUP-v1#1")
    p1 = _chunk(documents, "LEAVE-PAYCO-v1#1")
    card = Card("answer", persona.hr, (g1, p1), ())
    points = (
        Point(claim="Theo quy chế Tập đoàn, 12 ngày.", quote=g1.text, chunks=(g1.id,)),
        Point(claim="Theo quy chế PayCo, 13 ngày.", quote=p1.text, chunks=(p1.id,)),
    )
    lines = render(card, s, points, (g1, p1))
    assert [line.kind for line in lines] == [
        "who", "claim", "quote", "source", "claim", "quote", "source"
    ]
    assert lines[1].text == "Theo quy chế Tập đoàn, 12 ngày."
    assert lines[3].text.startswith("Nguồn: Quy chế nghỉ phép Tập đoàn")
    assert lines[4].text == "Theo quy chế PayCo, 13 ngày."
    assert lines[6].text.startswith("Nguồn: Quy chế nghỉ phép PayCo")


def test_conflict_card_wording(personas, documents):
    persona = personas["ha"]
    s = scope(persona, date(2026, 10, 7), documents)
    group = _doc(documents, "LEAVE-GROUP-v1")
    payco = _doc(documents, "LEAVE-PAYCO-v1")
    g1 = _chunk(documents, "LEAVE-GROUP-v1#1")
    p1 = _chunk(documents, "LEAVE-PAYCO-v1#1")
    card = Card("conflict", persona.hr, (g1,), ((group, payco),))
    marker = Point(
        claim="MODEL CLAIM MUST NOT APPEAR",
        quote="MODEL QUOTE MUST NOT APPEAR",
        chunks=("LEAVE-GROUP-v1#1",),
    )
    lines = render(card, s, (marker,), (g1, p1))
    assert lines == (
        CardLine("who", "Bạn đang hỏi với tư cách: nhân sự PayCo, Kế toán."),
        CardLine("lead", "Có 2 quy định cùng áp dụng cho bạn nhưng chưa được khai báo quy định nào được dùng thay quy định nào. Hệ thống không tự chọn."),
        CardLine("quote", 'Tập đoàn, Điều 1 (từ 01/01/2024): "Nhân sự chính thức của Tập đoàn được nghỉ phép năm 12 ngày mỗi năm."'),
        CardLine("quote", 'PayCo, Điều 1 (từ 01/01/2025): "Nhân sự PayCo được nghỉ phép năm 13 ngày mỗi năm."'),
        CardLine("plain", "Vui lòng hỏi HR PayCo."),
    )
    assert all("MODEL" not in line.text for line in lines)


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
    assert [q.split(",")[0] for q in quotes] == ["Tập đoàn", "Kế toán", "PayCo"]
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


# The window end and the notices (ADR 0012).

def _row1_card(personas, documents, as_of):
    persona = personas["minh"]
    s = scope(persona, as_of, documents)
    c2 = _chunk(documents, "LEAVE-GAMECO-v2#2") if as_of < date(2027, 1, 1) else _chunk(documents, "LEAVE-GAMECO-v3#2")
    card = Card("answer", persona.hr, (c2,), ())
    point = Point(claim="Một câu.", quote=c2.text, chunks=(c2.id,))
    return render(card, s, (point,), (c2,))


def test_a_notice_follows_the_source_line_on_each_point(personas, documents):
    persona = personas["minh"]
    s = scope(persona, date(2026, 12, 15), documents)
    c2 = _chunk(documents, "LEAVE-GAMECO-v2#2")
    card = Card("answer", persona.hr, (c2,), ())
    point = Point(claim="Một câu.", quote=c2.text, chunks=(c2.id,))
    lines = render(card, s, (point, point), (c2,))
    assert [line.kind for line in lines] == ["who", "claim", "quote", "source", "notice", "claim", "quote", "source", "notice"]
    assert lines[3].text.endswith("hiệu lực từ 01/01/2026 đến hết 31/12/2026. Hỏi thêm: HR GameCo.")


def test_no_window_end_and_no_notice_once_the_next_version_applies(personas, documents):
    lines = _row1_card(personas, documents, date(2027, 1, 1))
    assert [line.kind for line in lines] == ["who", "claim", "quote", "source"]
    assert lines[3].text == "Nguồn: Quy chế nghỉ phép GameCo (bản 3), Điều 2, hiệu lực từ 01/01/2027. Hỏi thêm: HR GameCo."


def test_a_document_with_no_change_shows_the_start_only(personas, documents):
    persona = personas["lan"]
    s = scope(persona, date(2026, 10, 7), documents)
    c1 = _chunk(documents, "LEAVE-GROUP-v1#1")
    lines = render(Card("answer", persona.hr, (c1,), ()), s, (Point("Một câu.", c1.text, (c1.id,)),), (c1,))
    assert [line.kind for line in lines] == ["who", "claim", "quote", "source"]
    assert "đến hết" not in lines[3].text


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
    assert lines[2].text.startswith("Tập đoàn, Điều 1 (từ 01/01/2024): ")
    assert lines[3].text.startswith("PayCo, Điều 1 (từ 01/01/2025 đến hết 31/12/2026): ")
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
