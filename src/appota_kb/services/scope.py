"""Steps 1-4: the documents in force, applying to the asker and not replaced, then the ones the asker may read.

Deterministic rules decide access, validity, applicability and precedence; nothing here
reads the question and nothing calls an LLM. Ported from adopted_rules.py, with one change
(ADR 0009): access is the last filter, so a document the asker may not read still replaces
its series and never brings the replaced one back.
"""
from datetime import date
from itertools import combinations

from appota_kb.models.document import Document
from appota_kb.models.org import Persona
from appota_kb.models.scope import Scope
from appota_kb.services.chunking import chunks as document_chunks


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


def scope(persona: Persona, as_of: date, documents: list[Document]) -> Scope:
    """Steps 1-4: documents in force, applying to the asker and not replaced, then those the asker
    may read, plus the conflict pairs. Never reads the question.

    Order: validity, applicability, precedence, access (ADR 0009). Access never decides which
    rule applies, so a restricted document that replaces a series leaves the asker with neither."""
    current = [d for d in in_force(documents, as_of) if applies(d, persona)]
    beaten = {d.overrides for d in current if d.overrides is not None}
    winners = sorted([d for d in current if d.series not in beaten and allowed(d, persona)], key=lambda d: d.id)
    pairs = []
    for a, b in combinations(winners, 2):
        if a.topic == b.topic and not declared(a, b):
            pairs.append(tuple(sorted((a, b), key=lambda d: d.id)))
    conflicts = tuple(sorted(pairs, key=lambda p: (p[0].id, p[1].id)))
    scoped = tuple(winners)
    chunk_tuple = tuple(c for d in scoped for c in document_chunks(d))
    return Scope(persona=persona, as_of=as_of, documents=scoped, conflicts=conflicts, chunks=chunk_tuple)
