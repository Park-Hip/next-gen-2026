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


def card_for_answer(scope: Scope, retrieved, points: tuple[Point, ...] | None) -> Card:
    """Step 7 for a model reply: refuse on malformed output, no points, a point without
    chunks, a cited id outside `retrieved`, or a quote that is empty or not a substring
    of any chunk the point cites (both sides folded); otherwise pick_card."""
    if not set(retrieved) <= scope.chunk_ids:
        raise ValueError("retrieved chunks outside the asker's scope")
    if points is None:
        return Card("refusal", scope.persona.hr, (), (), reason="malformed")
    if not points:
        return Card("refusal", scope.persona.hr, (), (), reason="no_points")
    by_id = {c.id: c for c in scope.chunks}
    cited = []
    for point in points:
        if not point.chunks:
            return Card("refusal", scope.persona.hr, (), (), reason="outside_retrieved")
        for cid in point.chunks:
            if cid not in retrieved:
                return Card("refusal", scope.persona.hr, (), (), reason="outside_retrieved")
        quote = fold(point.quote)
        if not quote:
            return Card("refusal", scope.persona.hr, (), (), reason="quote_mismatch")
        if not any(quote in fold(by_id[cid].text) for cid in point.chunks):
            return Card("refusal", scope.persona.hr, (), (), reason="quote_mismatch")
        cited.extend(point.chunks)
    return pick_card(scope, retrieved, cited)


def pick_card(scope: Scope, retrieved, cited) -> Card:
    """Step 7: the card from the chunks the model cites, never from LLM text.
    No citation, or any citation outside what was retrieved, refuses the whole answer.
    A cited document in a conflict pair shows every pair hit, with the cited chunks."""
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
    if hits:
        return Card("conflict", scope.persona.hr, tuple(order), hits)
    return Card("answer", scope.persona.hr, tuple(order), ())


def conflict_quotes(card: Card, retrieved: tuple[Chunk, ...]) -> tuple[tuple[tuple[Chunk, ...], tuple[Chunk, ...]], ...]:
    """The chunks each of the two documents quotes on the conflict card (ADR 0005, decision 1).

    For each document in a pair: quote its cited chunks; if it cites none, its highest-ranked
    retrieved chunk; if none was retrieved, all its chunks. Reads no meaning from any text.
    Returns one entry per conflict pair, each entry a (left, right) tuple of quoted chunks.
    """
    if card.kind != "conflict":
        return ()
    return tuple(
        (_quotes_for(a, card.cited, retrieved), _quotes_for(b, card.cited, retrieved))
        for a, b in card.conflicts
    )


def _quotes_for(document: Document, cited: tuple[Chunk, ...], retrieved: tuple[Chunk, ...]) -> tuple[Chunk, ...]:
    cited_chunks = tuple(c for c in cited if c.document_id == document.id)
    if cited_chunks:
        return cited_chunks
    retrieved_chunks = tuple(c for c in retrieved if c.document_id == document.id)
    if retrieved_chunks:
        return (retrieved_chunks[0],)
    return tuple(document_chunks(document))
