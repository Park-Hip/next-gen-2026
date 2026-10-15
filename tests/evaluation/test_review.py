"""evaluation.review: Hiep's review YAML round-trips and the review sheet's rows."""
from appota_kb.evaluation.review import build_review_sheet, load_reviews, review_skeleton
from appota_kb.evaluation.score import RowScore


def test_review_skeleton_round_trips(tmp_path):
    rows = [{"id": 1}, {"id": 7}]
    text = review_skeleton("run", rows)
    path = tmp_path / "r.yaml"
    path.write_text(text, encoding="utf-8")
    reviews = load_reviews(path)
    assert reviews == {1: {"row": 1, "faithful": None, "lesson": None, "note": None},
                       7: {"row": 7, "faithful": None, "lesson": None, "note": None}}


def _sheet_score(row_id: int, card_kind: str) -> RowScore:
    """A RowScore for the review sheet, with the given actual card kind."""
    row = {
        "id": row_id,
        "kind": "hard",
        "card": "answer" if card_kind == "answer" else card_kind,
        "questions": ["câu hỏi?"],
        "expected_answer": "kỳ vọng",
    }
    record = {
        "row": row_id,
        "status": "ok",
        "card": {
            "kind": card_kind,
            "reason": None,
            "cited": [],
            "conflicts": [],
            "answer_text": "14 ngày" if card_kind == "answer" else None,
            "lines": ["intro", "thẻ"],
        },
        "raw": '{"points": []}',
        "points": [],
        "retrieved_text": {},
    }
    return RowScore(
        row=row, record=record, errors=(), checks={},
        rules_wrong=False, leak=False, unsafe=False, over_cautious=False,
        raw_unsafe=False, caught_by_step7=False,
    )


def test_review_sheet_faithful_dash_for_non_answer_cards():
    scores = [_sheet_score(6, "refusal"), _sheet_score(7, "conflict"), _sheet_score(1, "answer")]
    text = build_review_sheet("run", scores, {})
    assert "- Faithful: -" in text
    assert "- Faithful: [chờ Hiệp]" in text


def test_review_sheet_faithful_filled_for_answer_card():
    scores = [_sheet_score(1, "answer")]
    reviews = {1: {"row": 1, "faithful": True, "lesson": "ok", "note": None}}
    text = build_review_sheet("run", scores, reviews)
    assert "- Faithful: yes" in text
    assert "- Faithful: -" not in text
