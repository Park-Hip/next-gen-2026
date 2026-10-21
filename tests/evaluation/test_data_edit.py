"""with_edit: the data_edit of a test case row."""
from datetime import date

import pytest

from appota_kb.evaluation.data_edit import with_edit
from appota_kb.services.chunking import chunks


def test_with_edit_removes_the_line(documents):
    v2 = next(d for d in documents if d.id == "LEAVE-GAMECO-v2")
    line = next(ln for ln in v2.body.splitlines() if ln.startswith("Điều 3."))
    edited = with_edit(documents, {"document": "LEAVE-GAMECO-v2", "remove": line})
    new_v2 = next(d for d in edited if d.id == "LEAVE-GAMECO-v2")
    assert line not in new_v2.body.splitlines()
    assert [c.id for c in chunks(new_v2)] == ["LEAVE-GAMECO-v2#1", "LEAVE-GAMECO-v2#2"]


def test_with_edit_raises_on_missing_line(documents):
    with pytest.raises(ValueError, match="not found"):
        with_edit(documents, {"document": "LEAVE-GAMECO-v2", "remove": "Điều không tồn tại."})


def test_with_edit_sets_topic_and_complements(documents):
    edited = with_edit(
        documents,
        {
            "document": "LEAVE-PAYCO-v1",
            "set": {"topic": "nghi_phep_nam", "complements": ["LEAVE-GROUP"]},
        },
    )
    payco = next(d for d in edited if d.id == "LEAVE-PAYCO-v1")
    assert payco.topic == "nghi_phep_nam"
    assert payco.complements == ("LEAVE-GROUP",)
    # A metadata edit leaves the body and every other document alone.
    assert payco.body == next(d.body for d in documents if d.id == "LEAVE-PAYCO-v1")
    assert [d.id for d in edited] == [d.id for d in documents]


def test_with_edit_removes_a_line_and_sets_metadata(documents):
    v2 = next(d for d in documents if d.id == "LEAVE-GAMECO-v2")
    line = next(ln for ln in v2.body.splitlines() if ln.startswith("Điều 3."))
    edited = with_edit(
        documents,
        {"document": "LEAVE-GAMECO-v2", "remove": line, "set": {"complements": []}},
    )
    new_v2 = next(d for d in edited if d.id == "LEAVE-GAMECO-v2")
    assert line not in new_v2.body.splitlines()
    assert new_v2.complements == ()


@pytest.mark.parametrize(
    "field, value, message",
    [
        ("topic", "", "topic must be a non-empty string"),
        ("topic", 3, "topic must be a non-empty string"),
        ("complements", "LEAVE-GROUP", "complements must be a list of strings"),
        ("complements", [1], "complements must be a list of strings"),
        ("status", "draft", "cannot set status"),
    ],
)
def test_with_edit_rejects_bad_metadata(documents, field, value, message):
    with pytest.raises(ValueError, match=message):
        with_edit(documents, {"document": "LEAVE-GAMECO-v2", "set": {field: value}})


def test_with_edit_needs_remove_or_set(documents):
    with pytest.raises(ValueError, match="needs remove or set"):
        with_edit(documents, {"document": "LEAVE-GAMECO-v2"})


def test_with_edit_rejects_an_unknown_document(documents):
    with pytest.raises(ValueError, match="not a loaded document"):
        with_edit(documents, {"document": "NOPE", "set": {"topic": "x"}})


def test_with_edit_sets_effective_to(documents):
    edited = with_edit(documents, {"document": "TRAVEL-GAMECO-v1", "set": {"effective_to": date(2026, 12, 31)}})
    travel = next(d for d in edited if d.id == "TRAVEL-GAMECO-v1")
    assert travel.effective_to == date(2026, 12, 31)
    assert travel.effective_from == date(2026, 1, 1)
    assert [d.id for d in edited] == [d.id for d in documents]


@pytest.mark.parametrize("value, message", [
    ("2026-12-31", "effective_to must be a date"),
    (None, "effective_to must be a date"),
    (date(2025, 12, 31), "before effective_from"),
])
def test_with_edit_rejects_a_bad_effective_to(documents, value, message):
    with pytest.raises(ValueError, match=message):
        with_edit(documents, {"document": "TRAVEL-GAMECO-v1", "set": {"effective_to": value}})


def test_with_edit_accepts_effective_to_on_the_start_day(documents):
    edited = with_edit(documents, {"document": "TRAVEL-GAMECO-v1", "set": {"effective_to": date(2026, 1, 1)}})
    assert next(d for d in edited if d.id == "TRAVEL-GAMECO-v1").effective_to == date(2026, 1, 1)
