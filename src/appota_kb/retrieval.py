"""Step 5: hybrid search inside the asker's scope (ADRs 0001 and 0002).

Keyword BM25 over Vietnamese syllables and dense cosine over gemini-embedding-001
are fused with reciprocal rank fusion. Only chunks of the asker's scope are ever
scored, and a runtime check refuses to return anything outside it.

Run by hand: `python -m app.retrieval <persona> <as_of> <question>` (needs GEMINI_API_KEY).
"""
from dataclasses import dataclass
from datetime import date
import json
import logging
import math
import os
import re
import sys
import unicodedata

from langchain_core.documents import Document as LCDocument
from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import InMemoryVectorStore

from appota_kb.core.config import Retrieval, load_config
from appota_kb.evaluation.data_edit import with_edit
from appota_kb.integrations.data_files import load_documents, load_org, load_personas, load_test_cases
from appota_kb.integrations.gemini import gemini_embeddings
from appota_kb.models.document import Chunk, Document
from appota_kb.models.retrieval import Hit
from appota_kb.models.scope import Scope
from appota_kb.rules import scope as build_scope
from appota_kb.services.chunking import chunks as document_chunks

logger = logging.getLogger("app.retrieval")


def tokens(text: str) -> list[str]:
    """NFC, lowercased, split into syllables on \\w+; diacritics are kept (ADR 0002)."""
    return re.findall(r"\w+", unicodedata.normalize("NFC", text).lower())


def index_text(document: Document, chunk: Chunk) -> str:
    """The text indexed for both BM25 and embeddings: the document title in front of the chunk."""
    return f"{document.title}. {chunk.text}"


def bm25_scores(query: list[str], texts: list[list[str]], k1: float, b: float) -> list[float]:
    """Okapi BM25 with Lucene's IDF log(1 + (N - df + 0.5) / (df + 0.5)).

    Each distinct query token counts once; statistics (N, df, average length) are
    computed over the given texts only, which is the asker's scope (ADR 0002).
    """
    n = len(texts)
    avgdl = sum(len(t) for t in texts) / n
    df: dict[str, int] = {}
    for t in texts:
        for word in set(t):
            df[word] = df.get(word, 0) + 1
    scores = []
    for t in texts:
        tf: dict[str, int] = {}
        for word in t:
            tf[word] = tf.get(word, 0) + 1
        score = 0.0
        for word in dict.fromkeys(query):
            if word not in tf:
                continue
            idf = math.log(1 + (n - df[word] + 0.5) / (df[word] + 0.5))
            length = len(t)
            score += idf * tf[word] * (k1 + 1) / (tf[word] + k1 * (1 - b + b * length / avgdl))
        scores.append(score)
    return scores


def rrf(rankings: list[list[str]], k: int) -> dict[str, float]:
    """Reciprocal rank fusion: sum of 1 / (k + rank) over the rankings, rank counted from 1."""
    fused: dict[str, float] = {}
    for ranking in rankings:
        for rank, cid in enumerate(ranking, start=1):
            fused[cid] = fused.get(cid, 0.0) + 1.0 / (k + rank)
    return fused


class ScopeLeakError(RuntimeError):
    """A chunk outside the asker's scope reached the results; retrieval must never return it."""


@dataclass(frozen=True)
class Index:
    store: InMemoryVectorStore
    texts: dict[str, str]
    tokens: dict[str, tuple[str, ...]]


def build_index(documents: list[Document], embeddings: Embeddings) -> Index:
    """Embed every chunk of every loaded document once; the scope is applied at search time."""
    pairs = [(document, chunk) for document in documents for chunk in document_chunks(document)]
    texts: dict[str, str] = {}
    indexed_tokens: dict[str, tuple[str, ...]] = {}
    lc_docs = []
    ids = []
    for document, chunk in pairs:
        text = index_text(document, chunk)
        texts[chunk.id] = text
        indexed_tokens[chunk.id] = tuple(tokens(text))
        lc_docs.append(LCDocument(id=chunk.id, page_content=text))
        ids.append(chunk.id)
    store = InMemoryVectorStore(embeddings)
    store.add_documents(lc_docs, ids=ids)
    return Index(store=store, texts=texts, tokens=indexed_tokens)


def retrieve(index: Index, scope: Scope, question: str, settings: Retrieval) -> list[Hit]:
    """Rank the scope's chunks by RRF over BM25 and dense cosine; the top_k go to step 6.

    A chunk that is in the scope but missing from the index, or whose indexed text no
    longer matches the current chunk, raises ValueError naming the chunk.
    """
    if not scope.chunks:
        _log(scope, question, [])
        return []

    by_document = {document.id: document for document in scope.documents}
    for chunk in scope.chunks:
        if chunk.id not in index.texts:
            raise ValueError(f"{chunk.id}: in the scope but missing from the index")
        if index.texts[chunk.id] != index_text(by_document[chunk.document_id], chunk):
            raise ValueError(f"{chunk.id}: indexed text differs from the current chunk")

    position = {chunk.id: i for i, chunk in enumerate(scope.chunks)}

    # Keyword ranking: statistics over the scope's chunks only (ADR 0002).
    scope_tokens = [index.tokens[chunk.id] for chunk in scope.chunks]
    scores = bm25_scores(tokens(question), scope_tokens, settings.bm25_k1, settings.bm25_b)
    bm25_by_id = {chunk.id: scores[i] for i, chunk in enumerate(scope.chunks)}
    bm25_order = sorted(scope.chunks, key=lambda c: (-bm25_by_id[c.id], position[c.id]))
    bm25_ids = [chunk.id for chunk in bm25_order]
    bm25_rank = {cid: rank for rank, cid in enumerate(bm25_ids, start=1)}

    # Dense ranking: the scope is passed to the vector store as a filter (ADR 0001, R8).
    query = index.store.embedding.embed_query(question)
    results = index.store.similarity_search_with_score_by_vector(
        query,
        k=len(scope.chunks),
        filter=lambda d: d.id in scope.chunk_ids,
    )
    ordered = sorted(results, key=lambda item: (-item[1], position.get(item[0].id, len(scope.chunks))))
    dense_ids = [doc.id for doc, _ in ordered]
    dense_by_id = {doc.id: score for doc, score in ordered}
    dense_rank = {cid: rank for rank, cid in enumerate(dense_ids, start=1)}

    fused = rrf([bm25_ids, dense_ids], settings.rrf_k)
    ranked = sorted(fused, key=lambda cid: (-fused[cid], position.get(cid, len(scope.chunks))))
    top = ranked[: settings.top_k]

    for cid in top:
        if cid not in scope.chunk_ids:
            raise ScopeLeakError(f"{cid}: outside the asker's scope, but returned by the vector store")

    by_chunk = {chunk.id: chunk for chunk in scope.chunks}
    hits = [
        Hit(
            chunk=by_chunk[cid],
            score=fused[cid],
            bm25=bm25_by_id[cid],
            bm25_rank=bm25_rank[cid],
            dense=dense_by_id[cid],
            dense_rank=dense_rank[cid],
        )
        for cid in top
    ]
    _log(scope, question, hits)
    return hits


def _log(scope: Scope, question: str, hits: list[Hit]) -> None:
    """One JSON line per search: persona, as-of date, question, scope size and each result."""
    logger.info(
        json.dumps(
            {
                "persona": scope.persona.id,
                "as_of": scope.as_of.isoformat(),
                "question": question,
                "scope_size": len(scope.chunks),
                "hits": [
                    {
                        "id": hit.chunk.id,
                        "rrf": hit.score,
                        "bm25": hit.bm25,
                        "bm25_rank": hit.bm25_rank,
                        "dense": hit.dense,
                        "dense_rank": hit.dense_rank,
                    }
                    for hit in hits
                ],
            },
            ensure_ascii=False,
        )
    )


def _print_hits(hits: list[Hit]) -> None:
    for hit in hits:
        print(
            f"  {hit.chunk.id}  rrf={hit.score:.4f}  bm25={hit.bm25:.4f}#{hit.bm25_rank}"
            f"  dense={hit.dense:.4f}#{hit.dense_rank}"
        )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    if not os.environ.get("GEMINI_API_KEY"):
        sys.exit("GEMINI_API_KEY is not set; set it to a Gemini API key to run the manual check")
    config = load_config()
    documents = load_documents()
    personas = load_personas(load_org())
    if len(sys.argv) == 1:
        index = build_index(documents, gemini_embeddings(config.retrieval.embedding_model))
        for row in load_test_cases():
            docs = with_edit(documents, row["data_edit"]) if "data_edit" in row else documents
            persona = personas[row["persona"]]
            as_of = row["as_of"]
            for question in row["questions"]:
                scoped = build_scope(persona, as_of, docs)
                print(f"row {row['id']} {row['kind']} | {persona.id} {as_of} | {question}")
                _print_hits(retrieve(index, scoped, question, config.retrieval))
    elif len(sys.argv) == 4:
        persona_id, as_of_text, question = sys.argv[1], sys.argv[2], sys.argv[3]
        if persona_id not in personas:
            sys.exit(f"unknown persona {persona_id}")
        index = build_index(documents, gemini_embeddings(config.retrieval.embedding_model))
        scoped = build_scope(personas[persona_id], date.fromisoformat(as_of_text), documents)
        print(f"{persona_id} {as_of_text} | {question}")
        _print_hits(retrieve(index, scoped, question, config.retrieval))
    else:
        sys.exit("usage: python -m app.retrieval [<persona> <as_of> <question>]")