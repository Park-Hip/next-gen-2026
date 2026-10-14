"""Loading, chunking and the data checks of the rules engine."""
from datetime import date
import unicodedata

import pytest

from appota_kb.evaluation.data_edit import with_edit
from appota_kb.integrations.data_files import load_documents
from appota_kb.models.document import Document
from appota_kb.services.chunking import chunks
from appota_kb.rules import fold
from conftest import MISSION1_IDS


def test_mission1_documents_loaded(documents):
    ids = {d.id for d in documents}
    for expected in MISSION1_IDS:
        assert expected in ids


def test_bodies_are_nfc(documents):
    for d in documents:
        assert unicodedata.is_normalized("NFC", d.body), d.id


def test_chunking(mission1_documents):
    by_id = {d.id: d for d in mission1_documents}
    assert sum(len(chunks(d)) for d in mission1_documents) == 25
    chunk = {c.id: c for c in chunks(by_id["LEAVE-GAMECO-v2"])}["LEAVE-GAMECO-v2#2"]
    assert chunk.label == "Điều 2"
    assert chunk.text == "Nhân sự GameCo được nghỉ phép năm 14 ngày mỗi năm."
    proc = chunks(by_id["LEAVE-PROC-GAMECO-v1"])
    assert [c.id for c in proc] == ["LEAVE-PROC-GAMECO-v1#1", "LEAVE-PROC-GAMECO-v1#2", "LEAVE-PROC-GAMECO-v1#3"]
    assert all(c.label is None for c in proc)


def _write(tmp_path, name, meta_id, body="Điều 1. Dòng.\n", series="S-X", **meta_overrides):
    docs = tmp_path / "documents"
    docs.mkdir(parents=True, exist_ok=True)
    meta = {
        "id": meta_id,
        "title": "T",
        "owner": "O",
        "series": series,
        "topic": "topic",
        "access": "all_staff",
        "applies_to": "Tập đoàn",
        "status": "published",
        "effective_from": date(2026, 1, 1),
        "effective_to": None,
        "overrides": None,
        "complements": [],
    }
    meta.update(meta_overrides)
    lines = ["---"]
    for key, value in meta.items():
        if value is None:
            lines.append(f"{key}: null")
        else:
            lines.append(f"{key}: {value}")
    lines.append("---")
    lines.append("")
    (docs / name).write_text("\n".join(lines) + "\n" + body, encoding="utf-8")
    return tmp_path


def test_load_raises_without_front_matter(tmp_path):
    docs = tmp_path / "documents"
    docs.mkdir()
    (docs / "X.md").write_text("Điều 1. Không có front matter.\n", encoding="utf-8")
    with pytest.raises(ValueError, match="no front matter"):
        load_documents(tmp_path)


def test_load_raises_on_missing_field(tmp_path):
    docs = tmp_path / "documents"
    docs.mkdir()
    text = "---\nid: X\nseries: S-X\nstatus: published\n---\n\nĐiều 1. Dòng.\n"
    (docs / "X.md").write_text(text, encoding="utf-8")
    with pytest.raises(ValueError, match="front matter keys"):
        load_documents(tmp_path)


def test_load_raises_on_file_name_mismatch(tmp_path):
    _write(tmp_path, "X.md", "Y")
    with pytest.raises(ValueError, match="file name is not the id"):
        load_documents(tmp_path)


def test_load_raises_on_unknown_overrides(tmp_path):
    _write(tmp_path, "X.md", "X", overrides="NOPE")
    with pytest.raises(ValueError, match="overrides names an unknown series"):
        load_documents(tmp_path)


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


def test_org_paths_and_hr(org):
    assert org.path("Studio") == ("Tập đoàn", "GameCo", "Studio")
    assert org.hr_unit("Studio") == "GameCo"
    assert org.hr_unit("Kế toán") == "PayCo"
    assert org.hr_unit("Nhân sự Tập đoàn") == "Tập đoàn"
    assert org.hr_for("Studio") == "HR GameCo"
    assert org.hr_for("Kế toán") == "HR PayCo"
    assert org.hr_for("Nhân sự Tập đoàn") == "HR Tập đoàn"


def test_personas(personas):
    assert personas["minh"].name == "Minh"
    assert personas["minh"].unit == "Studio"
    assert personas["minh"].company == "GameCo"
    assert personas["minh"].roles == ("employee",)
    assert personas["lan"].unit == "Nhân sự Tập đoàn"
    assert personas["lan"].company == "Tập đoàn"
    assert personas["lan"].roles == ("employee", "hr_group")
    assert personas["ha"].name == "Hà"
    assert personas["ha"].unit == "Kế toán"
    assert personas["ha"].company == "PayCo"
    assert personas["ha"].roles == ("employee",)


def test_cases_well_formed(cases, documents, personas):
    ids = [c["id"] for c in cases]
    assert len(ids) == len(set(ids))
    doc_ids = {d.id for d in documents}
    for c in cases:
        tag = f"test case {c['id']}"
        assert c["kind"] in ("good", "hard", "limitation"), tag
        assert c["card"] in ("answer", "conflict", "refusal"), tag
        assert c["persona"] in personas, tag
        assert c["as_of"], tag
        assert c["questions"] and all(isinstance(q, str) and q for q in c["questions"]), tag
        assert c["expected_answer"], tag
        cites = c.get("must_cite", []) + c.get("may_cite", [])
        if c["card"] == "answer":
            assert c.get("must_cite") and "conflict_pair" not in c, tag
        elif c["card"] == "conflict":
            assert len(c.get("conflict_pair", [])) == 2 and not cites, tag
        else:
            assert not cites and "conflict_pair" not in c, tag
        for field in ("must_cite", "may_cite", "conflict_pair", "forbidden_by_rules", "forbidden_for_llm"):
            for doc_id in c.get(field, []):
                assert doc_id in doc_ids, f"{tag}: {doc_id} is not a loaded document"
        if "data_edit" in c:
            edit = c["data_edit"]
            body = next(d.body for d in documents if d.id == edit["document"])
            assert edit["remove"] in body.splitlines(), f"{tag}: data_edit line not found"


def test_cases_key_facts(cases):
    for c in cases:
        tag = f"test case {c['id']}"
        if c["card"] == "answer":
            facts = c.get("key_facts", [])
            assert facts, tag
            for fact in facts:
                assert fold(fact).casefold() in fold(c["expected_answer"]).casefold(), tag
        else:
            assert "key_facts" not in c, tag


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