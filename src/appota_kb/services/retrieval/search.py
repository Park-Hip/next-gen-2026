"""Step 5: hybrid search inside the asker's scope (ADRs 0001 and 0002).

Keyword BM25 over Vietnamese syllables and dense cosine over gemini-embedding-001
are fused with reciprocal rank fusion. Only chunks of the asker's scope are ever
scored, and a runtime check refuses to return anything outside it.
"""
import json
import logging

from appota_kb.core.config import Retrieval
from appota_kb.models.retrieval import Hit
from appota_kb.models.scope import Scope
from appota_kb.services.retrieval.bm25 import bm25_scores, tokens
from appota_kb.services.retrieval.index import Index, index_text

logger = logging.getLogger(__name__)


def rrf(rankings: list[list[str]], k: int) -> dict[str, float]:
    """Reciprocal rank fusion: sum of 1 / (k + rank) over the rankings, rank counted from 1."""
    fused: dict[str, float] = {}
    for ranking in rankings:
        for rank, cid in enumerate(ranking, start=1):
            fused[cid] = fused.get(cid, 0.0) + 1.0 / (k + rank)
    return fused


class ScopeLeakError(RuntimeError):
    """A chunk outside the asker's scope reached the results; retrieval must never return it."""


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
