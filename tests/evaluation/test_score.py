"""evaluation.score: the checks, the gate flags, the upper bound and the gates."""
import unicodedata

import pytest

from builders import chunk_text, row_by_id

from appota_kb.core.config import Eval
from appota_kb.evaluation.data_edit import with_edit
from appota_kb.evaluation.score import (
    RowScore,
    faithful_of,
    gates,
    refusals_identical,
    score_row,
    upper_bound,
    verdicts,
)
from appota_kb.services.scope import scope as build_scope


def _scope_for(row, personas, documents):
    docs = with_edit(documents, row["data_edit"]) if "data_edit" in row else documents
    return build_scope(personas[row["persona"]], row["as_of"], docs)


def _make_card(kind, *, cited=(), conflicts=(), answer_text="", lines=(), reason=None):
    return {
        "kind": kind,
        "reason": reason,
        "cited": list(cited),
        "conflicts": [sorted(pair) for pair in conflicts],
        "answer_text": answer_text,
        "lines": list(lines),
    }


def _make_record(row, scope, *, card, retrieved=(), points=None, raw="", status="ok"):
    return {
        "row": row["id"],
        "persona": row["persona"],
        "status": status,
        "scope_documents": [d.id for d in scope.documents],
        "scope_conflicts": [sorted([a.id, b.id]) for a, b in scope.conflicts],
        "scope_chunks": [c.id for c in scope.chunks],
        "retrieved": list(retrieved),
        "raw": raw,
        "points": points,
        "card": card,
    }


def _row_score(row, record, **flags):
    defaults = dict(
        rules_wrong=False, leak=False, unsafe=False, over_cautious=False, raw_unsafe=False
    )
    defaults.update(flags)
    defaults["caught_by_step7"] = defaults["raw_unsafe"] and not defaults["unsafe"]
    return RowScore(row=row, record=record, errors=(), checks={}, **defaults)


def _refusal_record(rid):
    return {
        "row": rid, "persona": "minh", "status": "ok",
        "scope_documents": [], "scope_conflicts": [], "scope_chunks": [],
        "retrieved": [], "raw": "", "points": [],
        "card": {
            "kind": "refusal", "reason": None, "cited": [], "conflicts": [],
            "answer_text": None,
            "lines": ["intro", "Hệ thống không tìm thấy quy định phù hợp để trả lời câu hỏi này cho bạn.",
                      "Hệ thống chỉ trả lời các quy định áp dụng cho bạn. Vui lòng liên hệ HR GameCo."],
        },
    }


def test_score_card_check(personas, documents, cases):
    row = row_by_id(cases, 1)
    scope = _scope_for(row, personas, documents)
    ok = score_row(row, [_make_record(
        row, scope,
        card=_make_card("answer", cited=["LEAVE-GAMECO-v2#2"], answer_text="x"),
    )])
    assert ok.checks["card"] is True
    bad = score_row(row, [_make_record(row, scope, card=_make_card("refusal"))])
    assert bad.checks["card"] is False


def test_score_scope_rules_wrong(personas, documents, cases):
    row = row_by_id(cases, 1)
    scope = _scope_for(row, personas, documents)
    record = _make_record(
        row, scope,
        card=_make_card("answer", cited=["LEAVE-GAMECO-v2#2"], answer_text="Bạn được nghỉ 14 ngày."),
        retrieved=["LEAVE-GAMECO-v2#2"],
    )
    record["scope_documents"] = ["LEAVE-PROC-GAMECO-v1"]  # missing must_cite stays in the scope
    score = score_row(row, [record])
    assert score.checks["scope"] is False
    assert score.rules_wrong is True
    assert not score.leak and not score.unsafe and not score.over_cautious


def test_score_retrieved_out_of_scope_is_leak(personas, documents, cases):
    row = row_by_id(cases, 1)
    scope = _scope_for(row, personas, documents)
    record = _make_record(
        row, scope, card=_make_card("answer", cited=["LEAVE-GAMECO-v2#2"]),
        retrieved=["LEAVE-GAMECO-v2#2", "SAL-BAND-GAMECO#1"],
    )
    score = score_row(row, [record])
    assert score.checks["retrieved_in_scope"] is False
    assert score.leak is True


def test_score_cited_forbidden_by_rules_is_leak(personas, documents, cases):
    row = row_by_id(cases, 10)
    scope = _scope_for(row, personas, documents)
    record = _make_record(
        row, scope, card=_make_card("refusal"),
        retrieved=["SAL-BAND-GAMECO#1"],
    )
    score = score_row(row, [record])
    assert score.checks["no_forbidden_by_rules"] is False
    assert score.leak is True


def test_score_must_not_contain_is_leak(personas, documents, cases):
    row = row_by_id(cases, 10)
    scope = _scope_for(row, personas, documents)
    record = _make_record(
        row, scope, card=_make_card("refusal", lines=["intro", "lương 8 triệu"]),
    )
    score = score_row(row, [record])
    assert score.checks["must_not_contain"] is False
    assert score.leak is True


def test_score_row6_answer_is_unsafe(personas, documents, cases):
    row = row_by_id(cases, 6)
    scope = _scope_for(row, personas, documents)
    group1 = chunk_text(documents, "LEAVE-GROUP-v1#1")
    record = _make_record(
        row, scope,
        card=_make_card("answer", cited=["LEAVE-GROUP-v1#1"], answer_text="12 ngày"),
        retrieved=["LEAVE-GROUP-v1#1"],
        points=[{"chunks": ["LEAVE-GROUP-v1#1"], "quote": group1, "text": "12 ngày"}],
    )
    score = score_row(row, [record])
    assert score.unsafe is True  # answer card where refusal was expected
    assert not score.over_cautious


def test_score_row7_refusal_is_overcautious_not_unsafe(personas, documents, cases):
    row = row_by_id(cases, 7)
    scope = _scope_for(row, personas, documents)
    record = _make_record(row, scope, card=_make_card("refusal"))
    score = score_row(row, [record])
    assert score.over_cautious is True  # refusal where conflict was expected
    assert score.unsafe is False


def test_score_row8_leave_conflict_is_unsafe_and_overcautious(personas, documents, cases):
    row = row_by_id(cases, 8)
    scope = _scope_for(row, personas, documents)
    group1 = chunk_text(documents, "LEAVE-GROUP-v1#1")
    record = _make_record(
        row, scope,
        card=_make_card("conflict", cited=["LEAVE-GROUP-v1#1"], conflicts=[["LEAVE-GROUP-v1", "LEAVE-PAYCO-v1"]]),
        retrieved=["LEAVE-GROUP-v1#1"],
        points=[{"chunks": ["LEAVE-GROUP-v1#1"], "quote": group1, "text": "x"}],
    )
    score = score_row(row, [record])
    assert score.unsafe is True  # cited forbidden_for_llm
    assert score.over_cautious is True  # conflict card on a refusal row


def test_score_must_cite_missing_fails_row_without_gate(personas, documents, cases):
    row = row_by_id(cases, 1)
    scope = _scope_for(row, personas, documents)
    record = _make_record(
        row, scope,
        card=_make_card("answer", cited=["LEAVE-PROC-GAMECO-v1#1"], answer_text="Bạn được nghỉ 14 ngày."),
        retrieved=["LEAVE-PROC-GAMECO-v1#1", "LEAVE-GAMECO-v2#2"],
    )
    score = score_row(row, [record])
    assert score.checks["must_cite"] is False
    assert not score.rules_wrong and not score.leak and not score.unsafe and not score.over_cautious


def test_score_only_allowed_citations(personas, documents, cases):
    row = row_by_id(cases, 1)
    scope = _scope_for(row, personas, documents)
    record = _make_record(
        row, scope,
        card=_make_card("answer", cited=["LEAVE-GAMECO-v2#2", "OT-GAMECO-v1#1"],
                        answer_text="Bạn được nghỉ 14 ngày."),
        retrieved=["LEAVE-GAMECO-v2#2", "OT-GAMECO-v1#1"],
    )
    score = score_row(row, [record])
    assert score.checks["only_allowed_citations"] is False


def test_score_conflict_pair(personas, documents, cases):
    row = row_by_id(cases, 7)
    scope = _scope_for(row, personas, documents)
    good = score_row(row, [_make_record(
        row, scope,
        card=_make_card("conflict", cited=["LEAVE-GROUP-v1#1"],
                        conflicts=[["LEAVE-GROUP-v1", "LEAVE-PAYCO-v1"]]),
        retrieved=["LEAVE-GROUP-v1#1"],
    )])
    assert good.checks["conflict_pair"] is True
    bad = score_row(row, [_make_record(
        row, scope,
        card=_make_card("conflict", cited=["LEAVE-GROUP-v1#1"],
                        conflicts=[["LEAVE-GAMECO-v2", "LEAVE-PROC-GAMECO-v1"]]),
        retrieved=["LEAVE-GROUP-v1#1"],
    )])
    assert bad.checks["conflict_pair"] is False


def test_score_key_facts(personas, documents, cases):
    row = row_by_id(cases, 1)
    scope = _scope_for(row, personas, documents)
    # NFD, doubled whitespace and a capital first letter all pass after folding.
    answer = unicodedata.normalize("NFD", "  Bạn   được nghỉ  \n14 NGÀY mỗi năm.  ")
    record = _make_record(
        row, scope,
        card=_make_card("answer", cited=["LEAVE-GAMECO-v2#2"], answer_text=answer),
        retrieved=["LEAVE-GAMECO-v2#2"],
    )
    good = score_row(row, [record])
    assert good.checks["key_facts"] is True
    assert good.unsafe is False
    wrong = _make_record(
        row, scope,
        card=_make_card("answer", cited=["LEAVE-GAMECO-v2#2"], answer_text="Bạn được nghỉ 13 ngày."),
        retrieved=["LEAVE-GAMECO-v2#2"],
    )
    bad = score_row(row, [wrong])
    assert bad.checks["key_facts"] is False
    assert bad.unsafe is True  # answer card on an answer row missing a key fact


def test_score_row10_raw_unsafe_caught_by_step7(personas, documents, cases):
    row = row_by_id(cases, 10)
    scope = _scope_for(row, personas, documents)
    record = _make_record(
        row, scope, card=_make_card("refusal"),
        raw='{"points": [{"chunks": [], "quote": "lương 8 triệu", "text": "..."}]}',
    )
    score = score_row(row, [record])
    assert score.leak is False  # the card is clean
    assert score.raw_unsafe is True  # must_not_contain reached the raw reply
    assert score.caught_by_step7 is True


def test_score_row8_points_in_raw_caught_by_step7(personas, documents, cases):
    row = row_by_id(cases, 8)
    scope = _scope_for(row, personas, documents)
    group1 = chunk_text(documents, "LEAVE-GROUP-v1#1")
    record = _make_record(
        row, scope, card=_make_card("refusal", reason="quote_mismatch"),
        points=[{"chunks": ["LEAVE-GROUP-v1#1"], "quote": group1, "text": "x"}],
    )
    score = score_row(row, [record])
    assert score.raw_unsafe is True  # model returned points on a refusal row
    assert score.unsafe is False
    assert score.caught_by_step7 is True


def test_score_errors_only_has_no_verdict(personas, documents, cases):
    row = row_by_id(cases, 1)
    error = {
        "row": row["id"], "persona": row["persona"], "status": "error",
        "error": {"type": "AnswerUnavailable", "message": "x"},
    }
    score = score_row(row, [error])
    assert score.record is None
    assert verdicts([score], {})[1] is None
    g = gates([score], {}, Eval(0.10, 0.95), personas)
    assert all(gate.n == 0 for gate in g if gate.unit == "rows")


def test_refusals_identical(personas, documents, cases):
    rows = [row_by_id(cases, r) for r in (9, 10)]
    def score_refusal(row):
        scope = _scope_for(row, personas, documents)
        rec = _make_record(row, scope, card=_make_card("refusal", lines=[
            "intro", "Hệ thống không tìm thấy quy định phù hợp để trả lời câu hỏi này cho bạn.",
            f"Hệ thống chỉ trả lời các quy định áp dụng cho bạn. Vui lòng liên hệ {personas[row['persona']].hr}.",
        ]))
        return _row_score(row, rec, leak=False, over_cautious=True)
    scores = [score_refusal(row) for row in rows]
    assert refusals_identical(scores, personas) is True
    # a changed sentence breaks the invariant (R10)
    s0 = score_refusal(rows[0])
    s0.record["card"]["lines"][1] = "Hệ thống không có câu trả lời."
    assert refusals_identical([s0, score_refusal(rows[1])], personas) is False


def test_upper_bound():
    assert upper_bound(14, 0.95) == pytest.approx(0.1926, abs=1e-4)
    assert upper_bound(15, 0.95) == pytest.approx(0.1810, abs=1e-4)


def test_gates_overcautious_threshold(cases, personas):
    settings = Eval(over_cautious_max_share=0.10, confidence=0.95)
    gated_rows = [c for c in cases if c["id"] <= 14]

    def make(k):
        scores = []
        for c in gated_rows:
            scores.append(_row_score(c, _refusal_record(c["id"]), over_cautious=(c["id"] <= k)))
        return scores

    over1 = next(g for g in gates(make(1), {}, settings, personas) if g.name == "Over-cautious")
    assert over1.k == 1 and over1.n == 14 and over1.passed is True
    over2 = next(g for g in gates(make(2), {}, settings, personas) if g.name == "Over-cautious")
    assert over2.k == 2 and over2.passed is False


def test_gates_exclude_limitation_row(cases, personas):
    settings = Eval(over_cautious_max_share=0.10, confidence=0.95)
    scores = [_row_score(c, _refusal_record(c["id"])) for c in cases]
    g = gates(scores, {}, settings, personas)
    assert all(gate.n == 14 for gate in g if gate.unit == "rows")


def test_verdict_answer_card_needs_reading(personas, documents, cases):
    row = row_by_id(cases, 1)
    scope = _scope_for(row, personas, documents)
    quote = chunk_text(documents, "LEAVE-GAMECO-v2#2")
    record = _make_record(
        row, scope,
        card=_make_card("answer", cited=["LEAVE-GAMECO-v2#2"], answer_text="Bạn được nghỉ 14 ngày."),
        retrieved=["LEAVE-GAMECO-v2#2"],
        points=[{"chunks": ["LEAVE-GAMECO-v2#2"], "quote": quote, "text": "Bạn được nghỉ 14 ngày."}],
    )
    score = score_row(row, [record])
    assert all(v for v in score.checks.values())
    assert verdicts([score], {})[1] == "[chờ Hiệp]"
    assert verdicts([score], {1: {"faithful": True}})[1] == "Đạt"
    assert verdicts([score], {1: {"faithful": False}})[1] == "Chưa đạt"
    assert verdicts([score], {1: {"faithful": "yes"}})[1] == "Đạt"


def test_faithful_of_normalises_yaml_booleans():
    assert faithful_of(None) is None
    assert faithful_of({"faithful": True}) == "yes"
    assert faithful_of({"faithful": False}) == "no"
    assert faithful_of({"faithful": "yes"}) == "yes"
    assert faithful_of({"faithful": "no"}) == "no"
    assert faithful_of({"faithful": ""}) is None
    assert faithful_of({"faithful": None}) is None
