"""evaluation.review: Hiep's review YAML round-trips."""
from appota_kb.evaluation.review import load_reviews, review_skeleton


def test_review_skeleton_round_trips(tmp_path):
    rows = [{"id": 1}, {"id": 7}]
    text = review_skeleton("run", rows)
    path = tmp_path / "r.yaml"
    path.write_text(text, encoding="utf-8")
    reviews = load_reviews(path)
    assert reviews == {1: {"row": 1, "faithful": None, "lesson": None, "note": None},
                       7: {"row": 7, "faithful": None, "lesson": None, "note": None}}
