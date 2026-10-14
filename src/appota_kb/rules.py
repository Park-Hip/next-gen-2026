"""Steps 1-4 (scope) and step 7 (pick_card), ported from adopted_rules.py.

Deterministic rules decide access, validity, applicability, precedence and the card;
nothing here reads the question and nothing calls an LLM.
"""
from dataclasses import dataclass
from datetime import date
from itertools import combinations
from typing import Literal
import unicodedata

from appota_kb.data import Chunk, Document, Persona, chunks as document_chunks

REFUSAL_TEXT = (
    "Hệ thống không tìm thấy quy định phù hợp để trả lời câu hỏi này cho bạn.\n"
    "Hệ thống chỉ trả lời các quy định áp dụng cho bạn. Vui lòng liên hệ {hr}."
)


def in_force(documents: list[Document], as_of: date) -> list[Document]:
    """Step 1: per series, the published document with the latest effective_from not after as_of.
    A series has no document in force once that version's effective_to has passed."""
    best: dict[str, Document] = {}
    for d in documents:
        if d.status != "published" or d.effective_from is None or d.effective_from > as_of:
            continue
        if d.series not in best or d.effective_from > best[d.series].effective_from:
            best[d.series] = d
    return [d for d in best.values() if not (d.effective_to is not None and as_of > d.effective_to)]


def allowed(document: Document, persona: Persona) -> bool:
    """Step 2, access: who may read the document."""
    a = document.access
    if a == "all_staff":
        return True
    if a.startswith("roles:"):
        return any(role in persona.roles for role in a[6:].split(","))
    if a.startswith("unit:"):
        return a[5:] in persona.path
    return False


def applies(document: Document, persona: Persona) -> bool:
    """Step 2, applicability: the document covers the persona's unit."""
    return document.applies_to in persona.path


def declared(a: Document, b: Document) -> bool:
    """True if either document lists the other's series in complements (the relation is symmetric)."""
    return b.series in a.complements or a.series in b.complements


@dataclass(frozen=True)
class Scope:
    persona: Persona
    as_of: date
    documents: tuple[Document, ...]
    conflicts: tuple[tuple[Document, Document], ...]
    chunks: tuple[Chunk, ...]

    @property
    def chunk_ids(self) -> frozenset[str]:
        return frozenset(c.id for c in self.chunks)


def scope(persona: Persona, as_of: date, documents: list[Document]) -> Scope:
    """Steps 1-4: documents in force, readable by and applying to the asker, after overrides,
    plus the conflict pairs. Never reads the question."""
    kept = [d for d in in_force(documents, as_of) if allowed(d, persona) and applies(d, persona)]
    beaten = {d.overrides for d in kept if d.overrides is not None}
    winners = sorted([d for d in kept if d.series not in beaten], key=lambda d: d.id)
    pairs = []
    for a, b in combinations(winners, 2):
        if a.topic == b.topic and not declared(a, b):
            pairs.append(tuple(sorted((a, b), key=lambda d: d.id)))
    conflicts = tuple(sorted(pairs, key=lambda p: (p[0].id, p[1].id)))
    scoped = tuple(winners)
    chunk_tuple = tuple(c for d in scoped for c in document_chunks(d))
    return Scope(persona=persona, as_of=as_of, documents=scoped, conflicts=conflicts, chunks=chunk_tuple)


@dataclass(frozen=True)
class Point:
    """One grounded fact from the model: the chunks it cites, a verbatim quote and the sentence."""
    chunks: tuple[str, ...]
    quote: str
    text: str


@dataclass(frozen=True)
class Card:
    kind: Literal["answer", "conflict", "refusal"]
    hr: str
    cited: tuple[Chunk, ...]
    conflicts: tuple[tuple[Document, Document], ...]
    reason: str | None = None  # refusals only, for the log and #14; never shown (R10)


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


def refusal_text(card: Card) -> str:
    return REFUSAL_TEXT.format(hr=card.hr)


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


if __name__ == "__main__":
    import sys

    from appota_kb.data import load_documents, load_org, load_personas

    if len(sys.argv) != 3:
        sys.exit("usage: python -m app.rules <persona> <as_of>")
    persona_id, as_of_text = sys.argv[1], sys.argv[2]
    as_of = date.fromisoformat(as_of_text)
    personas = load_personas(load_org())
    if persona_id not in personas:
        sys.exit(f"unknown persona {persona_id}")
    s = scope(personas[persona_id], as_of, load_documents())
    print(f"persona: {s.persona.id} ({s.persona.name}, {s.persona.unit}, {s.persona.hr})")
    print(f"as_of: {s.as_of}")
    print("documents in scope:")
    for d in s.documents:
        print(f"  {d.id}")
    if s.conflicts:
        print("conflict pairs:")
        for a, b in s.conflicts:
            print(f"  {a.id} vs {b.id}")
    else:
        print("conflict pairs: none")
    print(f"chunks: {len(s.chunks)}")