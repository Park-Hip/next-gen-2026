"""Loading and validating the simulated data in data/: documents, org, personas, test cases."""
from datetime import date
import unicodedata

from conftest import MISSION1_IDS
import pytest

from appota_kb.integrations.data_files import load_documents
from appota_kb.services.citations import fold


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


def test_mission1_documents_loaded(documents):
    ids = {d.id for d in documents}
    for expected in MISSION1_IDS:
        assert expected in ids


def test_bodies_are_nfc(documents):
    for d in documents:
        assert unicodedata.is_normalized("NFC", d.body), d.id


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


def test_load_raises_on_versions_tied_on_effective_from(tmp_path):
    _write(tmp_path, "S-v1.md", "S-v1")
    _write(tmp_path, "S-v1-fix.md", "S-v1-fix")
    with pytest.raises(ValueError, match="S-v1, S-v1-fix") as error:
        load_documents(tmp_path)
    assert "2026-01-01" in str(error.value)


def test_load_accepts_a_tie_that_is_not_two_published_dates(tmp_path):
    _write(tmp_path, "S-v1.md", "S-v1")
    _write(tmp_path, "S-v2.md", "S-v2", effective_from=date(2026, 6, 1))
    _write(tmp_path, "S-v3-DRAFT.md", "S-v3-DRAFT", status="draft", effective_from=None)
    _write(tmp_path, "S-v4-DRAFT.md", "S-v4-DRAFT", status="draft", effective_from=None)
    _write(tmp_path, "T-v1.md", "T-v1", series="S-T")
    assert len(load_documents(tmp_path)) == 5


def test_load_raises_on_self_override(tmp_path):
    _write(tmp_path, "X.md", "X", series="S-X", overrides="S-X")
    with pytest.raises(ValueError, match="X: overrides names its own series S-X"):
        load_documents(tmp_path)


def test_load_raises_on_override_cycle(tmp_path):
    _write(tmp_path, "A.md", "A", series="S-A", overrides="S-B")
    _write(tmp_path, "B.md", "B", series="S-B", overrides="S-A")
    with pytest.raises(ValueError, match=r"overrides cycle: S-A -> S-B -> S-A \(A, B\)"):
        load_documents(tmp_path)


def test_load_raises_on_longer_override_cycle(tmp_path):
    _write(tmp_path, "A.md", "A", series="S-A", overrides="S-B")
    _write(tmp_path, "B.md", "B", series="S-B", overrides="S-C")
    _write(tmp_path, "C.md", "C", series="S-C", overrides="S-A")
    with pytest.raises(ValueError, match=r"overrides cycle: S-A -> S-B -> S-C -> S-A \(A, B, C\)"):
        load_documents(tmp_path)


def test_load_accepts_an_override_chain_and_a_draft_cycle(tmp_path):
    _write(tmp_path, "A.md", "A", series="S-A", overrides="S-B")
    _write(tmp_path, "B.md", "B", series="S-B", overrides="S-C")
    _write(tmp_path, "C.md", "C", series="S-C")
    # A draft is not checked until it is published.
    _write(tmp_path, "C-DRAFT.md", "C-DRAFT", series="S-C", status="draft", effective_from=None, overrides="S-A")
    assert len(load_documents(tmp_path)) == 4


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
        if "rules_card" in c:
            assert c["kind"] == "limitation", tag
            assert c["rules_card"] in ("answer", "conflict", "refusal"), tag
        if "conflict_from" in c:
            assert c["conflict_from"] == "model", tag
            assert c["card"] == "conflict" and "rules_card" not in c and "data_edit" in c, tag
        assert c["persona"] in personas, tag
        assert c["as_of"], tag
        assert c["questions"] and all(isinstance(q, str) and q for q in c["questions"]), tag
        assert c["expected_answer"], tag
        # A purpose says what is set up, what must happen and what counts as a failure: not one line.
        assert isinstance(c["purpose"], str) and ". " in c["purpose"], tag
        cites = c.get("must_cite", []) + c.get("may_cite", [])
        if c["card"] == "answer":
            assert c.get("must_cite") and "conflict_pair" not in c, tag
        elif c["card"] == "conflict":
            pair = c.get("conflict_pair", [])
            assert len(pair) == 2 and not c.get("may_cite"), tag
            assert set(c.get("must_cite", [])) == set(pair), tag
            assert c.get("must_show"), tag
        else:
            assert not cites and "conflict_pair" not in c, tag
        for field in ("must_cite", "may_cite", "conflict_pair", "forbidden_by_rules", "forbidden_for_llm"):
            for doc_id in c.get(field, []):
                assert doc_id in doc_ids, f"{tag}: {doc_id} is not a loaded document"
        if "data_edit" in c:
            edit = c["data_edit"]
            assert "remove" in edit or edit.get("set"), f"{tag}: data_edit changes nothing"
            body = next(d.body for d in documents if d.id == edit["document"])
            if "remove" in edit:
                assert edit["remove"] in body.splitlines(), f"{tag}: data_edit line not found"
            for key in (edit.get("set") or {}):
                assert key in ("topic", "complements"), f"{tag}: data_edit cannot set {key}"


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
