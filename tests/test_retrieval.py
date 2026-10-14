"""Step 5 retrieval: tokenizer, BM25, RRF, the index, retrieve and its guards.

All tests are offline: a deterministic syllable-hash embedder stands in for Gemini,
so these check the plumbing (scope-only search, the leak proof, the runtime guard),
not the quality of Google's embeddings.
"""
from dataclasses import replace
from datetime import date
import json
import logging
import math
import unicodedata

import pytest

from langchain_core.documents import Document as LCDocument
from langchain_core.vectorstores import InMemoryVectorStore

from fakes import SyllableEmbeddings

from app.config import Retrieval
from app.data import chunks as document_chunks, with_edit
from app.retrieval import (
    ScopeLeakError,
    bm25_scores,
    build_index,
    gemini_embeddings,
    index_text,
    retrieve,
    rrf,
    tokens,
)
from app.rules import allowed, applies, scope as build_scope


class CountingEmbeddings(SyllableEmbeddings):
    """Records how many embed_documents and embed_query calls retrieval makes."""

    def __init__(self):
        super().__init__()
        self.document_calls = 0
        self.query_calls = 0

    def embed_documents(self, texts):
        self.document_calls += 1
        return super().embed_documents(texts)

    def embed_query(self, text):
        self.query_calls += 1
        return super().embed_query(text)


def make_settings(**kwargs) -> Retrieval:
    defaults = dict(top_k=5, rrf_k=60, bm25_k1=1.2, bm25_b=0.75, embedding_model="test")
    defaults.update(kwargs)
    return Retrieval(**defaults)


def _doc_of(documents, hit):
    return next(d for d in documents if d.id == hit.chunk.document_id)


def _questions(cases):
    for row in cases:
        for question in row["questions"]:
            yield row, question


def test_tokens_normalises_and_lowercases():
    assert tokens(unicodedata.normalize("NFD", "nghỉ")) == tokens("nghỉ")
    assert tokens("Leave NĂM") == ["leave", "năm"]
    assert tokens("a.b,c?") == ["a", "b", "c"]
    assert tokens("nghỉ") == ["nghỉ"]
    assert tokens("nghỉ") != tokens("nghi")


def test_bm25_two_texts_checked_by_hand():
    # k1 = 1, b = 0 collapses to score = idf * tf * 2 / (tf + 1); idf(a) over two texts = log(1.2).
    scores = bm25_scores(["a"], [["a"], ["a", "a"]], k1=1.0, b=0.0)
    idf = math.log(1.2)
    assert scores == pytest.approx([idf, idf * 4 / 3])


def test_bm25_common_token_stays_positive():
    # Lucene's IDF log(1 + (N - df + 0.5) / (df + 0.5)) never goes zero or negative.
    scores = bm25_scores(["a"], [["a"], ["a", "b"], ["a", "c"]], k1=1.2, b=0.75)
    assert all(score > 0 for score in scores)


def test_bm25_no_shared_token_scores_zero():
    scores = bm25_scores(["a"], [["a"], ["b"]], k1=1.2, b=0.75)
    assert scores[0] > 0
    assert scores[1] == 0


def test_bm25_query_tokens_counted_once():
    texts = [["a"], ["a", "b"]]
    assert bm25_scores(["a"], texts, 1.2, 0.75) == pytest.approx(bm25_scores(["a", "a"], texts, 1.2, 0.75))


def test_rrf_three_items_checked_by_hand():
    fused = rrf([["a", "b", "c"], ["b", "c", "a"]], k=2)
    assert fused == pytest.approx({"a": 8 / 15, "b": 7 / 12, "c": 9 / 20})


def test_rrf_uses_argument_k():
    assert rrf([["a", "b"]], k=2) == {"a": 1 / 3, "b": 1 / 4}
    assert rrf([["a", "b"]], k=60) == {"a": 1 / 61, "b": 1 / 62}


def test_build_index_one_embed_call_title_in_front(documents):
    embeddings = CountingEmbeddings()
    index = build_index(documents, embeddings)
    chunks = [c for d in documents for c in document_chunks(d)]
    assert embeddings.document_calls == 1
    assert len(index.texts) == len(chunks)
    assert len(index.store.store) == len(chunks)
    v2 = next(d for d in documents if d.id == "LEAVE-GAMECO-v2")
    chunk = next(c for c in document_chunks(v2) if c.id == "LEAVE-GAMECO-v2#2")
    assert index.texts[chunk.id] == index_text(v2, chunk)
    assert index.texts[chunk.id].startswith(v2.title + ". ")


def test_retrieve_row1_target_in_top_five(personas, documents, cases):
    index = build_index(documents, SyllableEmbeddings())
    settings = make_settings()
    scoped = build_scope(personas["minh"], date(2026, 10, 7), documents)
    row1 = next(c for c in cases if c["id"] == 1)
    for question in row1["questions"]:
        hits = retrieve(index, scoped, question, settings)
        assert "LEAVE-GAMECO-v2#2" in {hit.chunk.id for hit in hits}


def test_retrieve_top_k_and_distinct(personas, documents):
    index = build_index(documents, SyllableEmbeddings())
    settings = make_settings()
    scoped = build_scope(personas["minh"], date(2026, 10, 7), documents)
    hits = retrieve(index, scoped, "Phép năm của tôi là bao nhiêu ngày?", settings)
    ids = [hit.chunk.id for hit in hits]
    assert 0 < len(ids) <= settings.top_k
    assert len(set(ids)) == len(ids)


def test_retrieve_scope_smaller_than_top_k(personas, documents):
    index = build_index(documents, SyllableEmbeddings())
    settings = make_settings()
    scoped = build_scope(personas["lan"], date(2026, 10, 7), documents)
    hits = retrieve(index, scoped, "Phép năm của tôi là bao nhiêu ngày?", settings)
    assert len(hits) == len(scoped.chunks) < settings.top_k


def test_retrieve_deterministic(personas, documents):
    index = build_index(documents, SyllableEmbeddings())
    settings = make_settings()
    scoped = build_scope(personas["minh"], date(2026, 10, 7), documents)
    question = "Phép năm của tôi là bao nhiêu ngày?"
    first = [hit.chunk.id for hit in retrieve(index, scoped, question, settings)]
    second = [hit.chunk.id for hit in retrieve(index, scoped, question, settings)]
    assert first == second


def test_retrieve_one_query_one_embed(personas, documents):
    embeddings = CountingEmbeddings()
    index = build_index(documents, embeddings)
    scoped = build_scope(personas["minh"], date(2026, 10, 7), documents)
    retrieve(index, scoped, "Phép năm của tôi là bao nhiêu ngày?", make_settings())
    assert embeddings.document_calls == 1
    assert embeddings.query_calls == 1


def test_retrieve_empty_scope_no_embed(personas, documents):
    embeddings = CountingEmbeddings()
    index = build_index(documents, embeddings)
    scoped = build_scope(personas["ha"], date(2023, 6, 1), documents)
    assert scoped.chunks == ()
    assert retrieve(index, scoped, "Phép năm của tôi là bao nhiêu ngày?", make_settings()) == []
    assert embeddings.document_calls == 1
    assert embeddings.query_calls == 0


def test_retrieve_missing_chunk_raises(personas, documents):
    index = build_index([d for d in documents if d.id != "OT-GAMECO-v1"], SyllableEmbeddings())
    scoped = build_scope(personas["minh"], date(2026, 10, 7), documents)
    assert any(c.id == "OT-GAMECO-v1#1" for c in scoped.chunks)
    with pytest.raises(ValueError, match="missing from the index"):
        retrieve(index, scoped, "Ngày nghỉ bù có trừ phép không?", make_settings())


def test_retrieve_changed_text_raises(personas, documents):
    edited = [replace(d, body=d.body.replace("14 ngày", "15 ngày")) if d.id == "LEAVE-GAMECO-v2" else d for d in documents]
    scoped = build_scope(personas["minh"], date(2026, 10, 7), edited)
    index = build_index(documents, SyllableEmbeddings())
    with pytest.raises(ValueError, match="indexed text differs"):
        retrieve(index, scoped, "Phép năm của tôi là bao nhiêu ngày?", make_settings())


def test_no_chunk_outside_scope_ever_returned(personas, dates, documents, cases, mutations):
    settings = make_settings()

    # Every persona on every boundary date, against every question: nothing outside the
    # scope built by the rules is ever returned, and nothing outside allowed+applies.
    index = build_index(documents, SyllableEmbeddings())
    for persona in personas.values():
        for as_of in dates:
            scoped = build_scope(persona, as_of, documents)
            for _, question in _questions(cases):
                hits = retrieve(index, scoped, question, settings)
                for hit in hits:
                    assert hit.chunk.id in scoped.chunk_ids
                    assert allowed(_doc_of(documents, hit), persona)
                    assert applies(_doc_of(documents, hit), persona)

    # Each row's own persona and date: none of its forbidden_by_rules documents is returned.
    for row in cases:
        docs = with_edit(documents, row["data_edit"]) if "data_edit" in row else documents
        scoped = build_scope(personas[row["persona"]], row["as_of"], docs)
        for question in row["questions"]:
            hits = retrieve(index, scoped, question, settings)
            for bad_doc in row.get("forbidden_by_rules", []):
                assert bad_doc not in {hit.chunk.document_id for hit in hits}

    # The seven trap mutations only need the scope invariant, on the 2026-10-07 date
    # (forbidden_by_rules is an expectation of the unmutated rules).
    for _, mutated in mutations:
        index = build_index(mutated, SyllableEmbeddings())
        for persona in personas.values():
            scoped = build_scope(persona, date(2026, 10, 7), mutated)
            for _, question in _questions(cases):
                hits = retrieve(index, scoped, question, settings)
                for hit in hits:
                    assert hit.chunk.id in scoped.chunk_ids
                    assert allowed(_doc_of(mutated, hit), persona)
                    assert applies(_doc_of(mutated, hit), persona)


def test_runtime_guard_raises_scope_leak(personas, documents):
    class LeakyStore(InMemoryVectorStore):
        """A store whose search drops the scope filter and leaks a foreign chunk first."""

        def similarity_search_with_score_by_vector(self, embedding, k=4, filter=None, **_kwargs):
            return [(LCDocument(id="SAL-BAND-GAMECO#1", page_content="foreign"), 1.0)]

    index = build_index(documents, SyllableEmbeddings())
    leaky = replace(index, store=LeakyStore(index.store.embedding))
    scoped = build_scope(personas["minh"], date(2026, 10, 7), documents)
    with pytest.raises(ScopeLeakError):
        retrieve(leaky, scoped, "Phép năm của tôi là bao nhiêu ngày?", make_settings())


def test_run_log_one_line_per_search(personas, documents, caplog):
    caplog.set_level(logging.INFO, logger="app.retrieval")
    index = build_index(documents, SyllableEmbeddings())
    settings = make_settings()
    scoped = build_scope(personas["minh"], date(2026, 10, 7), documents)
    question = "Phép năm của tôi là bao nhiêu ngày?"
    hits = retrieve(index, scoped, question, settings)

    records = [r for r in caplog.records if r.name == "app.retrieval"]
    assert len(records) == 1
    payload = json.loads(records[0].getMessage())
    assert payload["persona"] == "minh"
    assert payload["as_of"] == "2026-10-07"
    assert payload["question"] == question
    assert payload["scope_size"] == len(scoped.chunks)
    assert [entry["id"] for entry in payload["hits"]] == [hit.chunk.id for hit in hits]
    for entry in payload["hits"]:
        assert set(entry) == {"id", "rrf", "bm25", "bm25_rank", "dense", "dense_rank"}


def test_gemini_embeddings_missing_key(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    with pytest.raises(RuntimeError, match="GEMINI_API_KEY"):
        gemini_embeddings("gemini-embedding-001")


def test_gemini_embeddings_constructs_without_network(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "dummy")
    embeddings = gemini_embeddings("gemini-embedding-001")
    assert embeddings.model == "gemini-embedding-001"