"""evaluation.run: one record per row, resume and --rows, on scripted fakes."""
from dataclasses import replace
import re

from google.genai.errors import ServerError
from langchain_core.documents import Document as LCDocument
from langchain_core.vectorstores import InMemoryVectorStore
import pytest

from builders import RETRIEVAL, chunk_text, fake_meta, scripted_answerer
from fakes import ScriptedGemini, SyllableEmbeddings, no_points, reply_citing

from appota_kb.core.paths import ROOT
from appota_kb.evaluation.run import _check_resume, _select_rows, ask_row, run, run_meta
from appota_kb.evaluation.run import main as run_main
from appota_kb.evaluation.score import load_run
from appota_kb.services.answering.answerer import Answerer
from appota_kb.services.retrieval.index import build_index


def test_ask_row_1_ok(personas, documents, cases):
    row = next(c for c in cases if c["id"] == 1)
    quote = chunk_text(documents, "LEAVE-GAMECO-v2#2")
    replies = {
        row["questions"][0]: reply_citing(
            "LEAVE-GAMECO-v2#2",
            quote_from={"LEAVE-GAMECO-v2#2": quote},
        )
    }
    record = ask_row(scripted_answerer(documents, replies), row, documents, personas, fake_meta())
    assert record["status"] == "ok"
    assert record["question"] == row["questions"][0]
    assert record["card"]["kind"] == "answer"
    assert "LEAVE-GAMECO-v2#2" in record["retrieved"]
    # The answer text is the model's sentence, and the card puts it above the verified quote.
    claim = f"Theo tài liệu, {quote}"
    assert record["card"]["answer_text"] == claim
    assert record["card"]["lines"][2] == {"kind": "claim", "text": claim}
    assert record["card"]["lines"][3] == {"kind": "quote", "text": f'"{quote}"'}
    assert record["points"] == [{"claim": claim, "quote": quote, "chunks": ["LEAVE-GAMECO-v2#2"]}]
    assert record["retrieved_text"]["LEAVE-GAMECO-v2#2"] == quote
    assert record["points"][0]["chunks"] == ["LEAVE-GAMECO-v2#2"]
    assert record["card"]["lines"]
    assert record["scope_documents"]


def test_ask_row_19_records_the_flag_and_the_model_flagged_card(personas, documents, cases):
    # ADR 0014: the rules form no pair on the edited data; the pair on the card comes from the flag.
    row = next(c for c in cases if c["id"] == 19)
    ids = ("LEAVE-GROUP-v1#1", "LEAVE-PAYCO-v1#1")
    replies = {
        row["questions"][0]: reply_citing(
            *ids, quote_from={cid: chunk_text(documents, cid) for cid in ids}, disagreement=ids,
        )
    }
    record = ask_row(scripted_answerer(documents, replies), row, documents, personas, fake_meta())
    assert record["status"] == "ok"
    assert record["scope_conflicts"] == []
    assert record["disagreement"] == list(ids)
    card = record["card"]
    assert card["kind"] == "conflict" and card["reason"] == "model_flagged"
    assert card["conflicts"] == [["LEAVE-GROUP-v1", "LEAVE-PAYCO-v1"]]
    shown = " ".join(line["text"] for line in card["lines"])
    assert "12 ngày" in shown and "13 ngày" in shown


def test_ask_row_without_a_flag_records_an_empty_one(personas, documents, cases):
    row = next(c for c in cases if c["id"] == 19)
    ids = ("LEAVE-GROUP-v1#1", "LEAVE-PAYCO-v1#1")
    replies = {row["questions"][0]: reply_citing(*ids, quote_from={cid: chunk_text(documents, cid) for cid in ids})}
    record = ask_row(scripted_answerer(documents, replies), row, documents, personas, fake_meta())
    assert record["disagreement"] == []
    assert record["card"]["kind"] == "answer" and record["card"]["reason"] is None


def test_ask_row_15_edited_scope(personas, documents, cases):
    row = next(c for c in cases if c["id"] == 15)
    record = ask_row(
        scripted_answerer(documents, {row["questions"][0]: no_points()}),
        row, documents, personas, fake_meta(),
    )
    assert record["status"] == "ok"
    assert "LEAVE-GAMECO-v2#3" not in record["scope_chunks"]
    assert "LEAVE-GAMECO-v2#2" in record["scope_chunks"]
    assert "LEAVE-GROUP-v1" not in record["scope_documents"]


def test_ask_row_error_is_not_refusal(personas, documents, cases):
    row = next(c for c in cases if c["id"] == 1)
    replies = {row["questions"][0]: ServerError(429, {"error": "rate limit"})}
    record = ask_row(scripted_answerer(documents, replies), row, documents, personas, fake_meta())
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
    record = ask_row(answerer, row, documents, personas, fake_meta())
    assert record["status"] == "leak"
    assert record["error"]["type"] == "ScopeLeakError"
    assert record["card"] is None


def test_run_stops_at_first_error(personas, documents, cases, tmp_path):
    rows = [c for c in cases if c["id"] in (1, 3, 4)]
    quote = chunk_text(documents, "LEAVE-GAMECO-v2#2")
    replies = {
        rows[0]["questions"][0]: reply_citing(
            "LEAVE-GAMECO-v2#2", quote_from={"LEAVE-GAMECO-v2#2": quote}
        ),
        rows[1]["questions"][0]: ServerError(429, {"error": "quota"}),
    }
    chat = ScriptedGemini(replies)
    index = build_index(documents, SyllableEmbeddings())
    answerer = Answerer(index, chat, RETRIEVAL)
    path = tmp_path / "run.jsonl"
    code = run(answerer, rows, documents, personas, path, fake_meta())
    assert code == 3
    records = load_run(path)
    assert [r["row"] for r in records] == [1, 3]
    assert chat.call_count == 2  # rows 1 and 3 only; row 4 never asked


def test_run_resume_skips_ok_rows(personas, documents, cases, tmp_path):
    rows = [c for c in cases if c["id"] in (1, 3)]
    quote1 = chunk_text(documents, "LEAVE-GAMECO-v2#2")
    q1, q3 = rows[0]["questions"][0], rows[1]["questions"][0]
    chat1 = scripted_answerer(
        documents, {q1: reply_citing("LEAVE-GAMECO-v2#2", quote_from={"LEAVE-GAMECO-v2#2": quote1}),
                    q3: ServerError(429, {"error": "quota"})}
    )
    path = tmp_path / "run.jsonl"
    assert run(chat1, rows, documents, personas, path, fake_meta()) == 3
    assert len([r for r in load_run(path) if r["row"] == 1]) == 1

    chat2 = scripted_answerer(documents, {q3: no_points()})
    done = {r["row"] for r in load_run(path) if r["status"] in ("ok", "leak")}
    remaining = [r for r in rows if r["id"] not in done]
    assert run(chat2, remaining, documents, personas, path, fake_meta()) == 0

    records = load_run(path)
    assert [r["row"] for r in records] == [1, 3, 3]
    assert len([r for r in records if r["row"] == 1]) == 1
    assert chat2.chat.call_count == 1  # only the missing row 3


def test_check_resume_refuses_changed_meta():
    meta = fake_meta()
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
    # load_dotenv is stubbed so a developer's real .env cannot put the key back.
    loaded = []
    monkeypatch.setattr("appota_kb.evaluation.run.load_dotenv", lambda path: loaded.append(path))
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    assert run_main(["appota_kb.evaluation.run"]) == 1
    assert loaded == [ROOT / ".env"]


def test_run_meta_from_git_and_cases():
    from appota_kb.core.config import load_config

    meta = run_meta(load_config(), "test-run")
    assert re.fullmatch(r"[0-9a-f]{40}", meta["commit"])
    assert isinstance(meta["dirty"], bool)
    assert re.fullmatch(r"[0-9a-f]{64}", meta["cases_sha256"])
    assert meta["model"] == "gemini-3.5-flash-lite"
    assert meta["top_k"] == load_config().retrieval.top_k
