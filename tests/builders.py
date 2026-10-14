"""Helpers shared by several test files: retrieval settings, chunk texts, scopes and evaluation records."""
from datetime import date
from pathlib import Path

from fakes import ScriptedGemini, SyllableEmbeddings, no_points, reply_citing

from appota_kb.core.config import Retrieval, load_config
from appota_kb.evaluation.report import REPORT_REL, build_report
from appota_kb.evaluation.review import load_reviews
from appota_kb.evaluation.run import run
from appota_kb.evaluation.score import load_run, score_all
from appota_kb.services.answering.answerer import Answerer
from appota_kb.services.chunking import chunks as document_chunks
from appota_kb.services.retrieval.index import build_index
from appota_kb.services.scope import scope as build_scope

RETRIEVAL = Retrieval(top_k=5, rrf_k=60, bm25_k1=1.2, bm25_b=0.75, embedding_model="test")


def chunk_text(documents, chunk_id):
    doc_id, _ = chunk_id.rsplit("#", 1)
    doc = next(d for d in documents if d.id == doc_id)
    return next(c for c in document_chunks(doc) if c.id == chunk_id).text


def fake_meta():
    return {
        "run_id": "test",
        "commit": "c" * 40,
        "dirty": False,
        "cases_sha256": "abc",
        "model": "gemini-3.5-flash-lite",
        "thinking_level": "medium",
        "embedding_model": "gemini-embedding-001",
        "top_k": 5,
        "utc_offset_hours": 7,
    }


def scripted_answerer(documents, replies):
    index = build_index(documents, SyllableEmbeddings())
    return Answerer(index, ScriptedGemini(replies), RETRIEVAL)


def row_by_id(cases, rid):
    return next(c for c in cases if c["id"] == rid)


def minh_scope(personas, documents, as_of=date(2026, 10, 7)):
    return build_scope(personas["minh"], as_of, documents)


def committed_fixture(root: Path, documents, personas, rows, run_id="20261015-1400", cases_sha256=None):
    """Writes a complete fake run, its review YAML and its report under root, as the repository holds them.

    Row 1 gets a correct answer citing LEAVE-GAMECO-v2#2 and Hiep's mark `faithful: yes` with a lesson;
    every other row gets an empty points list. Returns the run id.
    """
    quote = chunk_text(documents, "LEAVE-GAMECO-v2#2")
    first = row_by_id(rows, 1)
    replies = {row["questions"][0]: no_points() for row in rows}
    replies[first["questions"][0]] = reply_citing("LEAVE-GAMECO-v2#2", quote_from={"LEAVE-GAMECO-v2#2": quote})
    meta = {**fake_meta(), "run_id": run_id}
    if cases_sha256 is not None:
        meta["cases_sha256"] = cases_sha256
    results = root / "results" / f"{run_id}.jsonl"
    assert run(scripted_answerer(documents, replies), rows, documents, personas, results, meta) == 0

    review = root / "results" / f"{run_id}.review.yaml"
    review.write_text(
        "- row: 1\n  faithful: yes\n  lesson: Bài học hàng 1.\n  note:\n", encoding="utf-8"
    )
    records = load_run(results)
    scores = score_all(rows, records)
    text = build_report(
        run_id, f"results/{run_id}.jsonl", records, rows, scores, load_reviews(review),
        load_config().eval, personas,
    )
    report = root / REPORT_REL
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(text, encoding="utf-8")
    return run_id
