"""The three cards' wording, word for word from the submitted document (Phần 2)."""
from datetime import date

from app.cards import render
from app.data import chunks
from app.rules import Card, Point, scope


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
    point = Point(chunks=("LEAVE-GAMECO-v2#2",), quote=c2.text, text="Nhân sự GameCo được nghỉ phép năm 14 ngày mỗi năm.")
    lines = render(card, s, (point,), (c2,))
    assert lines == (
        "Bạn đang hỏi với tư cách: nhân sự GameCo, Studio.",
        "Nhân sự GameCo được nghỉ phép năm 14 ngày mỗi năm.",
        "Nguồn: Quy chế nghỉ phép GameCo (bản 2), Điều 2, hiệu lực từ 01/01/2026. Hỏi thêm: HR GameCo.",
    )


def test_conflict_card_wording(personas, documents):
    persona = personas["ha"]
    s = scope(persona, date(2026, 10, 7), documents)
    group = _doc(documents, "LEAVE-GROUP-v1")
    payco = _doc(documents, "LEAVE-PAYCO-v1")
    g1 = _chunk(documents, "LEAVE-GROUP-v1#1")
    p1 = _chunk(documents, "LEAVE-PAYCO-v1#1")
    card = Card("conflict", persona.hr, (g1,), ((group, payco),))
    marker = Point(chunks=("LEAVE-GROUP-v1#1",), quote=g1.text, text="LLM TEXT MUST NOT APPEAR")
    lines = render(card, s, (marker,), (g1, p1))
    assert lines == (
        "Bạn đang hỏi với tư cách: nhân sự PayCo, Kế toán.",
        "Có hai quy định cùng áp dụng cho bạn nhưng chưa được khai báo quan hệ với nhau. Hệ thống không tự chọn.",
        'Tập đoàn, Điều 1 (từ 01/01/2024): "Nhân sự chính thức của Tập đoàn được nghỉ phép năm 12 ngày mỗi năm."',
        'PayCo, Điều 1 (từ 01/01/2025): "Nhân sự PayCo được nghỉ phép năm 13 ngày mỗi năm."',
        "Vui lòng hỏi HR PayCo.",
    )
    assert all("LLM TEXT" not in line for line in lines)


def test_refusal_card_wording(personas, documents):
    persona = personas["minh"]
    s = scope(persona, date(2026, 10, 7), documents)
    card = Card("refusal", persona.hr, (), ())
    lines = render(card, s, None, ())
    assert lines == (
        "Bạn đang hỏi với tư cách: nhân sự GameCo, Studio.",
        "Hệ thống không tìm thấy quy định phù hợp để trả lời câu hỏi này cho bạn.",
        "Hệ thống chỉ trả lời các quy định áp dụng cho bạn. Vui lòng liên hệ HR GameCo.",
    )