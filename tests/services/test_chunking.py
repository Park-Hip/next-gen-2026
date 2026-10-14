"""The chunking rule: one chunk per Điều, or per line for the procedure."""
from datetime import date

import pytest

from appota_kb.models.document import Document
from appota_kb.services.chunking import chunks


def test_chunking(mission1_documents):
    by_id = {d.id: d for d in mission1_documents}
    assert sum(len(chunks(d)) for d in mission1_documents) == 25
    chunk = {c.id: c for c in chunks(by_id["LEAVE-GAMECO-v2"])}["LEAVE-GAMECO-v2#2"]
    assert chunk.label == "Điều 2"
    assert chunk.text == "Nhân sự GameCo được nghỉ phép năm 14 ngày mỗi năm."
    proc = chunks(by_id["LEAVE-PROC-GAMECO-v1"])
    assert [c.id for c in proc] == ["LEAVE-PROC-GAMECO-v1#1", "LEAVE-PROC-GAMECO-v1#2", "LEAVE-PROC-GAMECO-v1#3"]
    assert all(c.label is None for c in proc)


def test_chunks_reject_mixed_lines():
    d = Document(id="DOC", title="T", owner="O", series="S", topic="topic", access="all_staff",
                 applies_to="Tập đoàn", status="published", effective_from=date(2026, 1, 1),
                 effective_to=None, overrides=None, complements=(),
                 body="Điều 1. A.\nmột dòng thường.\n")
    with pytest.raises(ValueError, match="mixes"):
        chunks(d)


def test_chunks_reject_repeated_dieu():
    d = Document(id="DOC", title="T", owner="O", series="S", topic="topic", access="all_staff",
                 applies_to="Tập đoàn", status="published", effective_from=date(2026, 1, 1),
                 effective_to=None, overrides=None, complements=(),
                 body="Điều 1. A.\nĐiều 1. B.\n")
    with pytest.raises(ValueError, match="repeated"):
        chunks(d)
