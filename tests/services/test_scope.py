"""Steps 1-4: validity, access, applicability, precedence and the conflict pairs, per test case row."""
from dataclasses import replace
from datetime import date
import inspect

import pytest

from appota_kb.evaluation.data_edit import with_edit
from appota_kb.integrations.data_files import load_test_cases
from appota_kb.models.document import Document
from appota_kb.models.org import Persona
from appota_kb.services.chunking import chunks
from appota_kb.services.citations import pick_card
from appota_kb.services.scope import allowed, applies, in_force, scope

CASES = load_test_cases()


def make_doc(id="DOC", series="SER", topic="topic", access="all_staff", applies_to="Tập đoàn",
             status="published", effective_from=date(2026, 1, 1), effective_to=None,
             overrides=None, complements=(), body="Điều 1. Nội dung.\n"):
    return Document(id=id, title="T", owner="O", series=series, topic=topic, access=access,
                    applies_to=applies_to, status=status, effective_from=effective_from,
                    effective_to=effective_to, overrides=overrides, complements=complements, body=body)


def make_persona(id="p", unit="Studio", company="GameCo", path=("Tập đoàn", "GameCo", "Studio"),
                 roles=("employee",), hr="HR GameCo"):
    return Persona(id=id, name=id, unit=unit, company=company, path=path, roles=roles, hr=hr)


# Limitation rows whose failure is in the rules; the other limitation rows fail only in the LLM's reply,
# so their scope and card must still be right here.
RULES_LIMITATIONS = {
    15: "limitation #24: a one-clause dùng thay drops the whole Group policy (row 15, M1a)",
    17: "limitation #52: citing a document in a conflict pair gives the conflict card, even where both agree",
}


def _case_params():
    params = []
    for row in CASES:
        marks = ()
        if row["id"] in RULES_LIMITATIONS:
            marks = (pytest.mark.xfail(strict=True, reason=RULES_LIMITATIONS[row["id"]]),)
        params.append(pytest.param(row, id=f"row-{row['id']}", marks=marks))
    return params


def test_scope_manual_check(personas, documents):
    as_of = date(2026, 10, 7)
    s = scope(personas["minh"], as_of, documents)
    assert [d.id for d in s.documents] == ["LEAVE-GAMECO-v2", "LEAVE-PROC-GAMECO-v1", "OT-GAMECO-v1", "TRAVEL-GAMECO-v1"]
    assert s.conflicts == ()
    s = scope(personas["lan"], as_of, documents)
    assert [d.id for d in s.documents] == ["LEAVE-GROUP-v1"]
    assert s.conflicts == ()
    s = scope(personas["ha"], as_of, documents)
    assert [d.id for d in s.documents] == ["LEAVE-GROUP-v1", "LEAVE-PAYCO-v1"]
    assert [(a.id, b.id) for a, b in s.conflicts] == [("LEAVE-GROUP-v1", "LEAVE-PAYCO-v1")]


def test_scope_reads_no_question():
    params = list(inspect.signature(scope).parameters)
    assert params == ["persona", "as_of", "documents"]


def test_in_force():
    as_of = date(2026, 7, 1)
    docs = [
        make_doc(id="D", series="SD", status="draft"),
        make_doc(id="F", series="SF", effective_from=date(2027, 1, 1)),
        make_doc(id="N", series="SN", effective_from=None),
        make_doc(id="A", series="SA", effective_from=date(2026, 1, 1)),
        make_doc(id="B", series="SB", effective_from=date(2026, 1, 1), effective_to=date(2026, 6, 30)),
        make_doc(id="C", series="SC", effective_from=date(2026, 1, 1), effective_to=date(2026, 7, 1)),
    ]
    assert {d.id for d in in_force(docs, as_of)} == {"A", "C"}


def test_in_force_effective_to_boundary():
    doc = make_doc(id="B", series="S", effective_from=date(2026, 1, 1), effective_to=date(2026, 6, 30))
    assert [d.id for d in in_force([doc], date(2026, 6, 30))] == ["B"]
    assert in_force([doc], date(2026, 7, 1)) == []


def test_in_force_repeal_leaves_series_empty():
    old = make_doc(id="OLD", series="S", effective_from=date(2025, 1, 1))
    new = make_doc(id="NEW", series="S", effective_from=date(2026, 1, 1), effective_to=date(2026, 6, 30))
    assert in_force([old, new], date(2026, 7, 1)) == []


def test_allowed_forms():
    p = make_persona(roles=("employee",), path=("Tập đoàn", "GameCo", "Studio"))
    assert allowed(make_doc(access="all_staff"), p)
    assert allowed(make_doc(access="unit:GameCo"), p)
    assert not allowed(make_doc(access="unit:PayCo"), p)
    assert allowed(make_doc(access="roles:employee"), p)
    assert not allowed(make_doc(access="roles:hr_gameco"), p)
    assert not allowed(make_doc(access="weird"), p)


def test_applies():
    p = make_persona(path=("Tập đoàn", "GameCo", "Studio"))
    assert applies(make_doc(applies_to="Tập đoàn"), p)
    assert applies(make_doc(applies_to="GameCo"), p)
    assert applies(make_doc(applies_to="Studio"), p)
    assert not applies(make_doc(applies_to="PayCo"), p)


def _override_pair(access="roles:hr_gameco"):
    """A Group policy and a GameCo policy that replaces it, readable only with `access`."""
    group = make_doc(id="GROUP-v1", series="GROUP", applies_to="Tập đoàn")
    company = make_doc(id="CO-v1", series="CO", applies_to="GameCo", access=access, overrides="GROUP")
    return [group, company]


def test_restricted_override_still_replaces_its_series():
    """Issue #48, ADR 0010: access never decides precedence."""
    docs = _override_pair()
    s = scope(make_persona(), date(2026, 10, 7), docs)
    assert s.documents == () and s.conflicts == () and s.chunks == ()
    s = scope(make_persona(roles=("employee", "hr_gameco")), date(2026, 10, 7), docs)
    assert [d.id for d in s.documents] == ["CO-v1"]


def test_restricted_override_leaves_units_it_does_not_cover_alone():
    """Issue 4's constraint, with the overrider hidden too: applicability still comes first."""
    docs = _override_pair()
    payco = make_persona(unit="Kế toán", company="PayCo", path=("Tập đoàn", "PayCo", "Kế toán"),
                         roles=("employee", "hr_gameco"), hr="HR PayCo")
    assert [d.id for d in scope(payco, date(2026, 10, 7), docs).documents] == ["GROUP-v1"]
    hr = make_persona(unit="Nhân sự Tập đoàn", path=("Tập đoàn", "Nhân sự Tập đoàn"))
    assert [d.id for d in scope(hr, date(2026, 10, 7), docs).documents] == ["GROUP-v1"]


def test_hidden_v3_does_not_bring_the_group_policy_back(personas, documents):
    """The snippet of issue #48: Minh on 01/01/2027 with LEAVE-GAMECO-v3 restricted."""
    edited = [replace(d, access="roles:hr_gameco") if d.id == "LEAVE-GAMECO-v3" else d for d in documents]
    s = scope(personas["minh"], date(2027, 1, 1), edited)
    assert [d.id for d in s.documents] == ["LEAVE-PROC-GAMECO-v1", "OT-GAMECO-v1", "TRAVEL-GAMECO-v1"]
    assert s.conflicts == ()
    assert not {c.document_id for c in s.chunks} & {"LEAVE-GROUP-v1", "LEAVE-GAMECO-v3"}


def test_hiding_one_document_removes_only_that_document(personas, dates, documents):
    """Access is the last filter: hiding a document takes it and its conflict pairs out, nothing else."""
    def pairs(s):
        return [(a.id, b.id) for a, b in s.conflicts]

    for hidden in documents:
        edited = [replace(d, access="roles:nobody") if d.id == hidden.id else d for d in documents]
        for persona in personas.values():
            for day in dates:
                full = scope(persona, day, documents)
                part = scope(persona, day, edited)
                where = (hidden.id, persona.id, day)
                assert [d.id for d in part.documents] == [d.id for d in full.documents if d.id != hidden.id], where
                assert pairs(part) == [p for p in pairs(full) if hidden.id not in p], where


@pytest.mark.parametrize("row", _case_params())
def test_case_row(personas, documents, row):
    docs = documents
    if "data_edit" in row:
        docs = with_edit(docs, row["data_edit"])
    s = scope(personas[row["persona"]], row["as_of"], docs)
    in_scope = {d.id for d in s.documents}
    for doc_id in (row.get("must_cite", []) + row.get("may_cite", [])
                   + row.get("conflict_pair", []) + row.get("forbidden_for_llm", [])):
        assert doc_id in in_scope, f"{doc_id} not in scope"
    for doc_id in row.get("forbidden_by_rules", []):
        assert doc_id not in in_scope, f"{doc_id} in scope"
    cited_ids = []
    for doc_id in row.get("must_cite", []) + row.get("conflict_pair", [])[:1]:
        cited_ids += [c.id for c in chunks(next(d for d in docs if d.id == doc_id))]
    assert pick_card(s, s.chunk_ids, cited_ids).kind == row["card"]


def test_leak_no_restricted_chunks(personas, dates, documents):
    for pid in ("minh", "lan", "ha"):
        persona = personas[pid]
        for as_of in dates:
            s = scope(persona, as_of, documents)
            assert not any(c.document_id == "SAL-BAND-GAMECO" for c in s.chunks)
            for c in s.chunks:
                d = next(d for d in documents if d.id == c.document_id)
                readable = d.access == "all_staff" or (
                    d.access.startswith("roles:")
                    and any(role in d.access[6:].split(",") for role in persona.roles)
                )
                assert readable, f"{c.id} leaks {d.access}"


def test_leak_hr_gameco_sees_salary(personas, documents):
    p = replace(personas["minh"], roles=("employee", "hr_gameco"))
    s = scope(p, date(2026, 10, 7), documents)
    assert any(c.document_id == "SAL-BAND-GAMECO" for c in s.chunks)


def test_mutations(personas, documents, mutations):
    by_name = dict(mutations)
    as_of = date(2026, 10, 7)

    s = scope(personas["minh"], as_of, by_name["remove_override_v2"])
    assert "LEAVE-GROUP-v1" in [d.id for d in s.documents]
    assert [(a.id, b.id) for a, b in s.conflicts] == [
        ("LEAVE-GAMECO-v2", "LEAVE-GROUP-v1"), ("LEAVE-GROUP-v1", "LEAVE-PROC-GAMECO-v1"),
    ]
    v2 = next(d for d in by_name["remove_override_v2"] if d.id == "LEAVE-GAMECO-v2")
    assert pick_card(s, s.chunk_ids, [c.id for c in chunks(v2)]).kind == "conflict"

    s = scope(personas["minh"], as_of, by_name["publish_v4"])
    ids = [d.id for d in s.documents]
    assert "LEAVE-GAMECO-v4-DRAFT" in ids and "LEAVE-GAMECO-v2" not in ids

    s = scope(personas["minh"], as_of, by_name["publish_v4_no_date"])
    ids = [d.id for d in s.documents]
    assert "LEAVE-GAMECO-v2" in ids and "LEAVE-GAMECO-v4-DRAFT" not in ids

    s = scope(personas["minh"], date(2027, 1, 1), by_name["v3_delayed"])
    ids = [d.id for d in s.documents]
    assert "LEAVE-GAMECO-v2" in ids and "LEAVE-GAMECO-v3" not in ids

    s = scope(personas["minh"], as_of, by_name["group_v2"])
    assert [d.id for d in s.documents] == ["LEAVE-GAMECO-v2", "LEAVE-PROC-GAMECO-v1", "OT-GAMECO-v1", "TRAVEL-GAMECO-v1"]
    s = scope(personas["lan"], as_of, by_name["group_v2"])
    assert [d.id for d in s.documents] == ["LEAVE-GROUP-v2"]

    s = scope(personas["minh"], as_of, by_name["v2_repealed"])
    ids = [d.id for d in s.documents]
    assert "LEAVE-GROUP-v1" in ids
    assert [(a.id, b.id) for a, b in s.conflicts] == [("LEAVE-GROUP-v1", "LEAVE-PROC-GAMECO-v1")]

    s = scope(personas["minh"], as_of, by_name["remove_complement_proc"])
    assert [(a.id, b.id) for a, b in s.conflicts] == [("LEAVE-GAMECO-v2", "LEAVE-PROC-GAMECO-v1")]
