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


def test_hiding_one_document_removes_only_that_document(employees, dates, documents):
    """Access is the last filter: hiding a document takes it and its conflict pairs out, nothing else."""
    def pairs(s):
        return [(a.id, b.id) for a, b in s.conflicts]

    for hidden in documents:
        edited = [replace(d, access="roles:nobody") if d.id == hidden.id else d for d in documents]
        for persona in employees.values():
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
    # conflict_from: model rows are found by the model's flag, so the rules alone give the answer card.
    expected = "answer" if row.get("conflict_from") == "model" else row.get("rules_card", row["card"])
    assert pick_card(s, s.chunk_ids, cited_ids).kind == expected


def test_leak_no_restricted_chunks(employees, dates, documents):
    for persona in employees.values():
        for as_of in dates:
            s = scope(persona, as_of, documents)
            if "hr_gameco" not in persona.roles:
                assert not any(c.document_id == "SAL-BAND-GAMECO" for c in s.chunks)
            for c in s.chunks:
                d = next(d for d in documents if d.id == c.document_id)
                readable = d.access == "all_staff" or (
                    d.access.startswith("roles:")
                    and any(role in d.access[6:].split(",") for role in persona.roles)
                )
                assert readable, f"{c.id} leaks {d.access}"


def test_hoa_sees_the_salary_band_and_minh_does_not(personas, documents):
    """G2.4: the simulated HR GameCo account is granted the restricted document."""
    day = date(2026, 10, 7)
    assert personas["hoa"].roles == ("employee", "hr_gameco")
    assert "SAL-BAND-GAMECO" in [d.id for d in scope(personas["hoa"], day, documents).documents]
    assert "SAL-BAND-GAMECO" not in [d.id for d in scope(personas["minh"], day, documents).documents]


@pytest.mark.parametrize("access", ["roles:hr_gamco", "roles:hr_gameco ", "roles:HR_GAMECO", "unit:Studoi", "unit:Nhân sự GameCoo"])
def test_a_misspelt_role_or_unit_in_access_hides_the_document_from_everyone(employees, documents, access):
    """A typo fails closed: no account is granted a document whose access names nothing real (G2.3 stays open)."""
    edited = [replace(d, access=access) if d.id == "SAL-BAND-GAMECO" else d for d in documents]
    for persona in employees.values():
        assert "SAL-BAND-GAMECO" not in [d.id for d in scope(persona, date(2026, 10, 7), edited).documents], persona.id


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


def _changes(s):
    return {c.document_id: (c.last_day, tuple(d.id for d in c.successors)) for c in s.changes}


def test_next_change_of_minh(personas, documents):
    """ADR 0012: v2 leaves Minh's scope after 31/12/2026 and v3 replaces it; nothing else changes."""
    for day in (date(2026, 10, 7), date(2026, 12, 15), date(2026, 12, 31)):
        s = scope(personas["minh"], day, documents)
        assert _changes(s) == {"LEAVE-GAMECO-v2": (date(2026, 12, 31), ("LEAVE-GAMECO-v3",))}
    assert scope(personas["minh"], date(2027, 1, 1), documents).changes == ()


def test_next_change_of_the_other_askers(personas, documents):
    assert scope(personas["ha"], date(2026, 10, 7), documents).changes == ()
    assert scope(personas["lan"], date(2026, 10, 7), documents).changes == ()


def test_change_for(personas, documents):
    s = scope(personas["minh"], date(2026, 10, 7), documents)
    change = s.change_for("LEAVE-GAMECO-v2")
    assert change.next_day == date(2027, 1, 1)
    assert s.change_for("OT-GAMECO-v1") is None


def test_an_end_date_without_a_successor(personas, documents):
    edited = [replace(d, effective_to=date(2026, 12, 31)) if d.id == "OT-GAMECO-v1" else d for d in documents]
    s = scope(personas["minh"], date(2026, 10, 7), edited)
    assert _changes(s)["OT-GAMECO-v1"] == (date(2026, 12, 31), ())
    # The boundary: the last day is still in the scope and carries the change; the next day it is gone.
    assert "OT-GAMECO-v1" in {d.id for d in scope(personas["minh"], date(2026, 12, 31), edited).documents}
    assert "OT-GAMECO-v1" not in {d.id for d in scope(personas["minh"], date(2027, 1, 1), edited).documents}


def test_a_change_on_the_as_of_date_is_not_a_change(personas, documents):
    """v3 starts on 01/01/2027: asked that day it is in the scope, so nothing about it is upcoming."""
    s = scope(personas["minh"], date(2027, 1, 1), documents)
    assert "LEAVE-GAMECO-v3" in {d.id for d in s.documents}
    assert s.change_for("LEAVE-GAMECO-v3") is None


def test_a_future_dung_thay_by_another_policy():
    group = make_doc(id="GROUP-v1", series="GROUP")
    later = make_doc(id="CO-v1", series="CO", applies_to="GameCo", overrides="GROUP",
                     effective_from=date(2026, 12, 1))
    s = scope(make_persona(), date(2026, 10, 7), [group, later])
    assert _changes(s) == {"GROUP-v1": (date(2026, 11, 30), ("CO-v1",))}


def test_a_restricted_successor_is_never_named():
    v2 = make_doc(id="CO-v2", series="CO")
    v3 = make_doc(id="CO-v3", series="CO", access="roles:hr_gameco", effective_from=date(2027, 1, 1))
    s = scope(make_persona(), date(2026, 10, 7), [v2, v3])
    assert _changes(s) == {"CO-v2": (date(2026, 12, 31), ())}
    hr = scope(make_persona(roles=("employee", "hr_gameco")), date(2026, 10, 7), [v2, v3])
    assert _changes(hr) == {"CO-v2": (date(2026, 12, 31), ("CO-v3",))}


def test_a_draft_is_never_a_successor():
    v2 = make_doc(id="CO-v2", series="CO")
    draft = make_doc(id="CO-v3", series="CO", status="draft", effective_from=date(2027, 1, 1))
    assert scope(make_persona(), date(2026, 10, 7), [v2, draft]).changes == ()


def test_the_group_policy_coming_back_is_not_a_successor():
    group = make_doc(id="GROUP-v1", series="GROUP")
    co = make_doc(id="CO-v2", series="CO", applies_to="GameCo", overrides="GROUP",
                  effective_from=date(2026, 6, 1), effective_to=date(2026, 12, 31))
    s = scope(make_persona(), date(2026, 10, 7), [group, co])
    assert _changes(s) == {"CO-v2": (date(2026, 12, 31), ())}
    assert [d.id for d in scope(make_persona(), date(2027, 1, 1), [group, co]).documents] == ["GROUP-v1"]


def test_only_the_first_change_of_a_document_counts():
    v1 = make_doc(id="CO-v1", series="CO")
    v2 = make_doc(id="CO-v2", series="CO", effective_from=date(2027, 1, 1))
    v3 = make_doc(id="CO-v3", series="CO", effective_from=date(2028, 1, 1))
    s = scope(make_persona(), date(2026, 10, 7), [v1, v2, v3])
    assert _changes(s) == {"CO-v1": (date(2026, 12, 31), ("CO-v2",))}
