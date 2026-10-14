"""with_edit: the data_edit of a test case row."""
import pytest

from appota_kb.evaluation.data_edit import with_edit
from appota_kb.services.chunking import chunks


def test_with_edit_removes_the_line(documents):
    v2 = next(d for d in documents if d.id == "LEAVE-GAMECO-v2")
    line = next(l for l in v2.body.splitlines() if l.startswith("Điều 3."))
    edited = with_edit(documents, {"document": "LEAVE-GAMECO-v2", "remove": line})
    new_v2 = next(d for d in edited if d.id == "LEAVE-GAMECO-v2")
    assert line not in new_v2.body.splitlines()
    assert [c.id for c in chunks(new_v2)] == ["LEAVE-GAMECO-v2#1", "LEAVE-GAMECO-v2#2"]


def test_with_edit_raises_on_missing_line(documents):
    with pytest.raises(ValueError, match="not found"):
        with_edit(documents, {"document": "LEAVE-GAMECO-v2", "remove": "Điều không tồn tại."})
