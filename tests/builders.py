"""Helpers shared by several test files: retrieval settings, chunk texts, scopes and evaluation records."""
from datetime import date

from fakes import ScriptedGemini, SyllableEmbeddings

from appota_kb.core.config import Retrieval
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
        "model": "gemini-3.8-flash",
        "thinking_level": "low",
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
