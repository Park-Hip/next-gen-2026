"""The evaluation harness, offline: run, scoring and the report, all on fake replies."""
import re
import unicodedata
from dataclasses import replace
from pathlib import Path

import pytest
from google.genai.errors import ServerError
from langchain_core.documents import Document as LCDocument
from langchain_core.vectorstores import InMemoryVectorStore

from fakes import ScriptedGemini, SyllableEmbeddings, no_points, reply_citing

from appota_kb.answer import Answerer
from appota_kb.core.config import Eval, Retrieval
from appota_kb.evaluation.data_edit import with_edit
from appota_kb.services.chunking import chunks as document_chunks
from appota_kb.retrieval import build_index
from appota_kb.rules import scope as build_scope

from appota_kb.evaluation.run import _check_resume, _select_rows, ask_row, run, run_meta
from appota_kb.evaluation.run import main as run_main
from appota_kb.evaluation.score import (
    RowScore,
    faithful_of,
    gates,
    load_run,
    refusals_identical,
    score_all,
    score_row,
    upper_bound,
    verdicts,
)
import appota_kb.evaluation.report as report_mod
from appota_kb.evaluation.report import build_report, load_reviews, review_skeleton
from appota_kb.evaluation.report import main as report_main

RETRIEVAL = Retrieval(top_k=5, rrf_k=60, bm25_k1=1.2, bm25_b=0.75, embedding_model="test")
REPO = Path(__file__).resolve().parent.parent


def _meta():
    return {
        "run_id": "test",
        "commit": "c" * 40,
        "dirty": False,
        "cases_sha256": "abc",
        "model": "gemini-3.8-flash",
        "thinking_level": "low",
        "embedding_model": "gemini-embedding-001",
        "top_k": 5,
        "utc_offset_hours": 7,
    }


def _chunk_text(documents, chunk_id):
    doc_id, _ = chunk_id.rsplit("#", 1)
    doc = next(d for d in documents if d.id == doc_id)
    return next(c for c in document_chunks(doc) if c.id == chunk_id).text


def _answerer(documents, replies):
    index = build_index(documents, SyllableEmbeddings())
    return Answerer(index, ScriptedGemini(replies), RETRIEVAL)


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


# --- eval.run: ask_row ------------------------------------------------


def test_ask_row_1_ok(personas, documents, cases):
    row = next(c for c in cases if c["id"] == 1)
    quote = _chunk_text(documents, "LEAVE-GAMECO-v2#2")
    replies = {
        row["questions"][0]: reply_citing(
            "LEAVE-GAMECO-v2#2",
            quote_from={"LEAVE-GAMECO-v2#2": quote},
            text="Bạn được nghỉ 14 ngày.",
        )
    }
    record = ask_row(_answerer(documents, replies), row, documents, personas, _meta())
    assert record["status"] == "ok"
    assert record["question"] == row["questions"][0]
    assert record["card"]["kind"] == "answer"
    assert "LEAVE-GAMECO-v2#2" in record["retrieved"]
    assert record["card"]["answer_text"] == "Bạn được nghỉ 14 ngày."
    assert record["retrieved_text"]["LEAVE-GAMECO-v2#2"] == quote
    assert record["points"][0]["chunks"] == ["LEAVE-GAMECO-v2#2"]
    assert record["card"]["lines"]
    assert record["scope_documents"]


def test_ask_row_15_edited_scope(personas, documents, cases):
    row = next(c for c in cases if c["id"] == 15)
    record = ask_row(
        _answerer(documents, {row["questions"][0]: no_points()}),
        row, documents, personas, _meta(),
    )
    assert record["status"] == "ok"
    assert "LEAVE-GAMECO-v2#3" not in record["scope_chunks"]
    assert "LEAVE-GAMECO-v2#2" in record["scope_chunks"]
    assert "LEAVE-GROUP-v1" not in record["scope_documents"]


def test_ask_row_error_is_not_refusal(personas, documents, cases):
    row = next(c for c in cases if c["id"] == 1)
    replies = {row["questions"][0]: ServerError(429, {"error": "rate limit"})}
    record = ask_row(_answerer(documents, replies), row, documents, personas, _meta())
    assert record["status"] == "error"
    assert record["card"] is None
    assert record["error"]["type"] == "AnswerUnavailable"


def test_ask_row_leak(personas, documents, cases):
    row = next(c for c in cases if c["id"] == 1)

    class LeakyStore(InMemoryVectorStore):
        def similarity_search_with_score_by_vector(self, embedding, k=4, filter=None, **_):
            return [(LCDocument(id="SAL-BAND-GAMECO#1", page_content="foreign"), 1.0)]

    index = build_index(documents, SyllableEmbeddings())
    leaky = replace(index, store=LeakyStore(index.store.embedding))
    answerer = Answerer(leaky, ScriptedGemini({}), RETRIEVAL)
    record = ask_row(answerer, row, documents, personas, _meta())
    assert record["status"] == "leak"
    assert record["error"]["type"] == "ScopeLeakError"
    assert record["card"] is None


# --- eval.run: run, resume, select -----------------------------------


def test_run_stops_at_first_error(personas, documents, cases, tmp_path):
    rows = [c for c in cases if c["id"] in (1, 3, 4)]
    quote = _chunk_text(documents, "LEAVE-GAMECO-v2#2")
    replies = {
        rows[0]["questions"][0]: reply_citing(
            "LEAVE-GAMECO-v2#2", quote_from={"LEAVE-GAMECO-v2#2": quote}, text="x"
        ),
        rows[1]["questions"][0]: ServerError(429, {"error": "quota"}),
    }
    chat = ScriptedGemini(replies)
    index = build_index(documents, SyllableEmbeddings())
    answerer = Answerer(index, chat, RETRIEVAL)
    path = tmp_path / "run.jsonl"
    code = run(answerer, rows, documents, personas, path, _meta())
    assert code == 3
    records = load_run(path)
    assert [r["row"] for r in records] == [1, 3]
    assert chat.call_count == 2  # rows 1 and 3 only; row 4 never asked


def test_run_resume_skips_ok_rows(personas, documents, cases, tmp_path):
    rows = [c for c in cases if c["id"] in (1, 3)]
    quote1 = _chunk_text(documents, "LEAVE-GAMECO-v2#2")
    q1, q3 = rows[0]["questions"][0], rows[1]["questions"][0]
    chat1 = _answerer(
        documents, {q1: reply_citing("LEAVE-GAMECO-v2#2", quote_from={"LEAVE-GAMECO-v2#2": quote1}, text="x"),
                    q3: ServerError(429, {"error": "quota"})}
    )
    path = tmp_path / "run.jsonl"
    assert run(chat1, rows, documents, personas, path, _meta()) == 3
    assert len([r for r in load_run(path) if r["row"] == 1]) == 1

    chat2 = _answerer(documents, {q3: no_points()})
    done = {r["row"] for r in load_run(path) if r["status"] in ("ok", "leak")}
    remaining = [r for r in rows if r["id"] not in done]
    assert run(chat2, remaining, documents, personas, path, _meta()) == 0

    records = load_run(path)
    assert [r["row"] for r in records] == [1, 3, 3]
    assert len([r for r in records if r["row"] == 1]) == 1
    assert chat2.chat.call_count == 1  # only the missing row 3


def test_check_resume_refuses_changed_meta():
    meta = _meta()
    first = [dict((k, v) for k, v in meta.items() if k != "utc_offset_hours") | {"row": 1}]
    _check_resume(meta, first)  # no raise
    for key, value in (("commit", "d" * 40), ("cases_sha256", "changed"), ("top_k", 6), ("model", "other")):
        bad_first = [dict(first[0], **{key: value})]
        with pytest.raises(ValueError, match="resume refused"):
            _check_resume(meta, bad_first)


def test_select_rows(cases):
    assert [r["id"] for r in _select_rows(cases, "1,7")] == [1, 7]
    assert [r["id"] for r in _select_rows(cases, "7,1")] == [1, 7]
    assert _select_rows(cases, "99") == []


def test_run_main_no_key(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    assert run_main(["eval.run"]) == 1


def test_run_meta_from_git_and_cases():
    from appota_kb.core.config import load_config

    meta = run_meta(load_config(), "test-run")
    assert re.fullmatch(r"[0-9a-f]{40}", meta["commit"])
    assert isinstance(meta["dirty"], bool)
    assert re.fullmatch(r"[0-9a-f]{64}", meta["cases_sha256"])
    assert meta["model"] == "gemini-3.8-flash"
    assert meta["top_k"] == load_config().retrieval.top_k


# --- eval.score: checks and flags ------------------------------------


def _row_by_id(cases, rid):
    return next(c for c in cases if c["id"] == rid)


def test_score_card_check(personas, documents, cases):
    row = _row_by_id(cases, 1)
    scope = _scope_for(row, personas, documents)
    ok = score_row(row, [_make_record(
        row, scope,
        card=_make_card("answer", cited=["LEAVE-GAMECO-v2#2"], answer_text="x"),
    )])
    assert ok.checks["card"] is True
    bad = score_row(row, [_make_record(row, scope, card=_make_card("refusal"))])
    assert bad.checks["card"] is False


def test_score_scope_rules_wrong(personas, documents, cases):
    row = _row_by_id(cases, 1)
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
    row = _row_by_id(cases, 1)
    scope = _scope_for(row, personas, documents)
    record = _make_record(
        row, scope, card=_make_card("answer", cited=["LEAVE-GAMECO-v2#2"]),
        retrieved=["LEAVE-GAMECO-v2#2", "SAL-BAND-GAMECO#1"],
    )
    score = score_row(row, [record])
    assert score.checks["retrieved_in_scope"] is False
    assert score.leak is True


def test_score_cited_forbidden_by_rules_is_leak(personas, documents, cases):
    row = _row_by_id(cases, 10)
    scope = _scope_for(row, personas, documents)
    record = _make_record(
        row, scope, card=_make_card("refusal"),
        retrieved=["SAL-BAND-GAMECO#1"],
    )
    score = score_row(row, [record])
    assert score.checks["no_forbidden_by_rules"] is False
    assert score.leak is True


def test_score_must_not_contain_is_leak(personas, documents, cases):
    row = _row_by_id(cases, 10)
    scope = _scope_for(row, personas, documents)
    record = _make_record(
        row, scope, card=_make_card("refusal", lines=["intro", "lương 8 triệu"]),
    )
    score = score_row(row, [record])
    assert score.checks["must_not_contain"] is False
    assert score.leak is True


def test_score_row6_answer_is_unsafe(personas, documents, cases):
    row = _row_by_id(cases, 6)
    scope = _scope_for(row, personas, documents)
    group1 = _chunk_text(documents, "LEAVE-GROUP-v1#1")
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
    row = _row_by_id(cases, 7)
    scope = _scope_for(row, personas, documents)
    record = _make_record(row, scope, card=_make_card("refusal"))
    score = score_row(row, [record])
    assert score.over_cautious is True  # refusal where conflict was expected
    assert score.unsafe is False


def test_score_row8_leave_conflict_is_unsafe_and_overcautious(personas, documents, cases):
    row = _row_by_id(cases, 8)
    scope = _scope_for(row, personas, documents)
    group1 = _chunk_text(documents, "LEAVE-GROUP-v1#1")
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
    row = _row_by_id(cases, 1)
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
    row = _row_by_id(cases, 1)
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
    row = _row_by_id(cases, 7)
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
    row = _row_by_id(cases, 1)
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
    row = _row_by_id(cases, 10)
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
    row = _row_by_id(cases, 8)
    scope = _scope_for(row, personas, documents)
    group1 = _chunk_text(documents, "LEAVE-GROUP-v1#1")
    record = _make_record(
        row, scope, card=_make_card("refusal", reason="quote_mismatch"),
        points=[{"chunks": ["LEAVE-GROUP-v1#1"], "quote": group1, "text": "x"}],
    )
    score = score_row(row, [record])
    assert score.raw_unsafe is True  # model returned points on a refusal row
    assert score.unsafe is False
    assert score.caught_by_step7 is True


def test_score_errors_only_has_no_verdict(personas, documents, cases):
    row = _row_by_id(cases, 1)
    scope = _scope_for(row, personas, documents)
    error = {
        "row": row["id"], "persona": row["persona"], "status": "error",
        "error": {"type": "AnswerUnavailable", "message": "x"},
    }
    score = score_row(row, [error])
    assert score.record is None
    assert verdicts([score], {})[1] is None
    g = gates([score], {}, Eval(0.10, 0.95), personas)
    assert all(gate.n == 0 for gate in g if gate.unit == "rows")


# --- eval.score: refusals, bound, gates -------------------------------


def test_refusals_identical(personas, documents, cases):
    rows = [_row_by_id(cases, r) for r in (9, 10)]
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
    row = _row_by_id(cases, 1)
    scope = _scope_for(row, personas, documents)
    quote = _chunk_text(documents, "LEAVE-GAMECO-v2#2")
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


# --- eval.report -------------------------------------------------------


def test_report_on_full_fake_run(cases, personas, documents, tmp_path, monkeypatch):
    monkeypatch.setattr(report_mod, "RESULTS", tmp_path)
    monkeypatch.setattr(report_mod, "REPORT_PATH", tmp_path / "test_report.md")

    replies = {row["questions"][0]: no_points() for row in cases}
    answerer = _answerer(documents, replies)
    path = tmp_path / "run.jsonl"
    assert run(answerer, cases, documents, personas, path, _meta()) == 0

    assert report_main(["report", str(path)]) == 0
    review_md = tmp_path / "run.review.md"
    review_yaml = tmp_path / "run.review.yaml"
    assert review_md.exists()
    assert review_yaml.exists()

    # A second call keeps a filled YAML untouched.
    text = review_yaml.read_text(encoding="utf-8")
    filled = text.replace(
        "- row: 1\n  faithful:\n  lesson:\n  note:",
        "- row: 1\n  faithful: yes\n  lesson: Bài học hàng 1.\n  note:",
        1,
    )
    review_yaml.write_text(filled, encoding="utf-8")
    report_main(["report", str(path)])
    assert review_yaml.read_text(encoding="utf-8") == filled

    report_text = (tmp_path / "test_report.md").read_text(encoding="utf-8")
    assert "k of n" in report_text
    assert "95% upper bound" in report_text
    for row in cases:
        assert row["questions"][0] in report_text
    for column in ("Kỳ vọng", "Kết quả thực tế", "Đạt/Chưa đạt", "Điều học được"):
        assert column in report_text
    assert "[chờ Hiệp]" in report_text
    assert "Bài học hàng 1." in report_text


def test_report_incomplete_writes_nothing(cases, personas, documents, tmp_path, monkeypatch):
    monkeypatch.setattr(report_mod, "RESULTS", tmp_path)
    monkeypatch.setattr(report_mod, "REPORT_PATH", tmp_path / "test_report.md")
    row = _row_by_id(cases, 1)
    quote = _chunk_text(documents, "LEAVE-GAMECO-v2#2")
    answerer = _answerer(
        documents,
        {row["questions"][0]: reply_citing("LEAVE-GAMECO-v2#2", quote_from={"LEAVE-GAMECO-v2#2": quote}, text="x")},
    )
    path = tmp_path / "partial.jsonl"
    run(answerer, [row], documents, personas, path, _meta())
    assert report_main(["report", str(path)]) == 0
    assert not (tmp_path / "test_report.md").exists()


def test_review_skeleton_round_trips(tmp_path):
    rows = [{"id": 1}, {"id": 7}]
    text = review_skeleton("run", rows)
    path = tmp_path / "r.yaml"
    path.write_text(text, encoding="utf-8")
    reviews = load_reviews(path)
    assert reviews == {1: {"row": 1, "faithful": None, "lesson": None, "note": None},
                       7: {"row": 7, "faithful": None, "lesson": None, "note": None}}


def test_committed_report_matches_source():
    report_path = REPO / "docs" / "mission2" / "test_report.md"
    if not report_path.exists():
        pytest.skip("no committed report yet; generated after the final run")
    text = report_path.read_text(encoding="utf-8")
    match = re.search(r"`results/([^`]+\.jsonl)`", text)
    assert match, "the report header must name its results file"
    results_path = REPO / "results" / match.group(1)
    run_id = results_path.stem

    from appota_kb.core.config import load_config
    from appota_kb.integrations.data_files import load_org, load_personas, load_test_cases

    rows = load_test_cases()
    personas = load_personas(load_org())

    records = load_run(results_path)
    scores = score_all(rows, records)
    reviews = load_reviews(REPO / "results" / f"{run_id}.review.yaml")
    rebuilt = build_report(
        run_id, f"results/{run_id}.jsonl", records, rows, scores, reviews,
        load_config().eval, personas,
    )
    assert rebuilt == text