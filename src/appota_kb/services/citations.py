"""Step 7: the card from the chunks the model cites, never from LLM text.

Deterministic: it checks citations and quotes against the scope and reads no meaning from
any text. Ported from adopted_rules.py.
"""
import unicodedata

from appota_kb.models.answer import Point
from appota_kb.models.card import Card
from appota_kb.models.document import Chunk, Document
from appota_kb.models.scope import Scope
from appota_kb.services.chunking import chunks as document_chunks


def fold(text: str) -> str:
    """NFC, then every run of whitespace to one space, stripped (ADR 0003)."""
    return " ".join(unicodedata.normalize("NFC", text).split())


def card_for_answer(
    scope: Scope, retrieved, points: tuple[Point, ...] | None, disagreement: tuple[str, ...] = ()
) -> Card:
    """Step 7 for a model reply: refuse on malformed output, no points, a point without
    chunks, a cited id outside `retrieved`, or a quote that is empty or not a substring
    of any chunk the point cites (both sides folded); otherwise pick_card.

    The model's `disagreement` is read only after those refusals pass (ADR 0014): it can add a
    conflict pair, never remove one and never change a refusal."""
    if not set(retrieved) <= scope.chunk_ids:
        raise ValueError("retrieved chunks outside the asker's scope")
    if points is None:
        return Card("refusal", scope.persona.hr, (), (), reason="malformed")
    if not points:
        return Card("refusal", scope.persona.hr, (), (), reason="no_points")
    by_id = {c.id: c for c in scope.chunks}
    cited = []
    quoted = set()  # chunks that hold the quote of a point citing them
    for point in points:
        if not point.chunks:
            return Card("refusal", scope.persona.hr, (), (), reason="outside_retrieved")
        for cid in point.chunks:
            if cid not in retrieved:
                return Card("refusal", scope.persona.hr, (), (), reason="outside_retrieved")
        quote = fold(point.quote)
        if not quote:
            return Card("refusal", scope.persona.hr, (), (), reason="quote_mismatch")
        holders = [cid for cid in point.chunks if quote in fold(by_id[cid].text)]
        if not holders:
            return Card("refusal", scope.persona.hr, (), (), reason="quote_mismatch")
        quoted.update(holders)
        cited.extend(point.chunks)
    return pick_card(scope, retrieved, cited, flagged_pair(scope, retrieved, quoted, disagreement))


def flagged_pair(scope: Scope, retrieved, quoted, disagreement) -> tuple[Document, Document] | None:
    """The pair of documents the model's flag names, or None when any check fails (ADR 0014).

    Exactly two different chunks, both retrieved, each holding the verbatim quote of a point that
    cites it, from two different documents in the scope. Reads no meaning from any text.
    """
    if len(disagreement) != 2 or disagreement[0] == disagreement[1]:
        return None
    if any(cid not in retrieved or cid not in quoted for cid in disagreement):
        return None
    by_id = {c.id: c for c in scope.chunks}
    docs = {d.id: d for d in scope.documents}
    ids = {by_id[cid].document_id for cid in disagreement}
    if len(ids) != 2:
        return None
    first, second = sorted(ids)
    return docs[first], docs[second]


def pick_card(scope: Scope, retrieved, cited, flagged: tuple[Document, Document] | None = None) -> Card:
    """Step 7: the card from the chunks the model cites, never from LLM text.
    No citation, or any citation outside what was retrieved, refuses the whole answer.
    A cited document in a conflict pair shows every pair hit, with the cited chunks.
    A valid `flagged` pair is added to the hits (ADR 0014); the card then has reason "model_flagged"
    if the declared pairs did not already hold it."""
    if not set(retrieved) <= scope.chunk_ids:
        raise ValueError("retrieved chunks outside the asker's scope")
    if not cited:
        return Card("refusal", scope.persona.hr, (), ())
    by_id = {c.id: c for c in scope.chunks}
    order = []
    seen = set()
    for cid in cited:
        if cid not in retrieved:
            return Card("refusal", scope.persona.hr, (), ())
        if cid not in seen:
            seen.add(cid)
            order.append(by_id[cid])
    cited_docs = {c.document_id for c in order}
    hits = tuple(p for p in scope.conflicts if p[0].id in cited_docs or p[1].id in cited_docs)
    reason = None
    if flagged is not None and not any(p[0].id == flagged[0].id and p[1].id == flagged[1].id for p in hits):
        hits = tuple(sorted((*hits, flagged), key=lambda p: (p[0].id, p[1].id)))
        reason = "model_flagged"
    if hits:
        return Card("conflict", scope.persona.hr, tuple(order), hits, reason=reason)
    return Card("answer", scope.persona.hr, tuple(order), ())


def conflict_quotes(card: Card, retrieved: tuple[Chunk, ...]) -> tuple[tuple[Document, tuple[Chunk, ...]], ...]:
    """The chunks each document quotes on the conflict card (ADR 0005, decision 1; ADR 0014).

    Each document of the card's pairs appears once, in the order it first appears in the sorted
    pairs. Its quotes are its cited chunks; if it cites none, its highest-ranked retrieved chunk;
    if none was retrieved, all its chunks. Reads no meaning from any text.
    """
    if card.kind != "conflict":
        return ()
    documents: dict[str, Document] = {}
    for pair in card.conflicts:
        for document in pair:
            documents.setdefault(document.id, document)
    return tuple((d, _quotes_for(d, card.cited, retrieved)) for d in documents.values())


def _quotes_for(document: Document, cited: tuple[Chunk, ...], retrieved: tuple[Chunk, ...]) -> tuple[Chunk, ...]:
    cited_chunks = tuple(c for c in cited if c.document_id == document.id)
    if cited_chunks:
        return cited_chunks
    retrieved_chunks = tuple(c for c in retrieved if c.document_id == document.id)
    if retrieved_chunks:
        return (retrieved_chunks[0],)
    return tuple(document_chunks(document))
