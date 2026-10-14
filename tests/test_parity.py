"""Same results as adopted_rules.py for the 10 Mission 1 documents."""
import importlib.util
from pathlib import Path

from appota_kb.services.chunking import chunks
from appota_kb.services.citations import pick_card
from appota_kb.services.scope import scope


def _load_adopted_rules():
    path = Path(__file__).resolve().parent.parent / "docs/mission1/redraft/checks/adopted_rules.py"
    spec = importlib.util.spec_from_file_location("adopted_rules", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ar = _load_adopted_rules()


def to_ar_doc(d):
    return dict(
        id=d.id,
        series=d.series,
        topic=d.topic,
        access=d.access,
        applies_to=d.applies_to,
        status=d.status,
        frm=d.effective_from.strftime("%d/%m/%Y") if d.effective_from else "",
        to=d.effective_to.strftime("%d/%m/%Y") if d.effective_to else "",
        overrides=d.overrides or "",
        complements=list(d.complements),
    )


def scope_ids_and_pairs(persona, as_of, documents):
    s = scope(persona, as_of, documents)
    ids = sorted(d.id for d in s.documents)
    pairs = sorted(tuple(sorted((a.id, b.id))) for a, b in s.conflicts)
    return ids, pairs


def rulebook_ids_and_pairs(ar_docs, persona_id, as_of):
    kept, gaps = ar.rulebook(ar_docs, persona_id, as_of)
    ids = sorted(d["id"] for d in kept)
    pairs = sorted(tuple(sorted((a["id"], b["id"]))) for a, b in gaps)
    return ids, pairs


def test_parity_scope(personas, mission1_documents, dates):
    ar_docs = [to_ar_doc(d) for d in mission1_documents]
    for pid in ("minh", "lan", "ha"):
        for as_of in dates:
            assert scope_ids_and_pairs(personas[pid], as_of, mission1_documents) == rulebook_ids_and_pairs(ar_docs, pid, as_of)


def test_parity_mutations(personas, dates, mutations):
    for name, mutated in mutations:
        ar_docs = [to_ar_doc(d) for d in mutated]
        for pid in ("minh", "lan", "ha"):
            for as_of in dates:
                assert scope_ids_and_pairs(personas[pid], as_of, mutated) == rulebook_ids_and_pairs(
                    ar_docs, pid, as_of
                ), (name, pid, as_of)


def test_parity_cards(personas, mission1_documents, cases):
    ar_docs = [to_ar_doc(d) for d in mission1_documents]
    for row in (c for c in cases if c["id"] <= 10):
        persona = personas[row["persona"]]
        as_of = row["as_of"]
        s = scope(persona, as_of, mission1_documents)
        cited_docs = row.get("must_cite", []) + row.get("conflict_pair", [])[:1]
        cited = [c.id for doc_id in cited_docs for c in chunks(next(d for d in mission1_documents if d.id == doc_id))]
        ar_card = ar.answer(ar_docs, row["persona"], as_of, cited_docs).split()[0].lower()
        assert pick_card(s, s.chunk_ids, cited).kind == ar_card