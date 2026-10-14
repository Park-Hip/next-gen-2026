"""Print the scope of one asker on one date: documents, conflict pairs and chunk count.

Run by hand: `uv run python scripts/show_scope.py <persona> <as_of> [--why]` (no key needed).
With --why it also prints, for every document, the step that keeps or drops it and why;
docs/architecture.md copies this output for its trace.
"""
from datetime import date
import sys

from appota_kb.integrations.data_files import load_documents, load_org, load_personas
from appota_kb.models.document import Document
from appota_kb.models.org import Persona
from appota_kb.models.scope import Scope
from appota_kb.services.scope import allowed, applies, in_force, scope


def _step1_reason(d: Document, current: dict[str, Document], as_of: date) -> str:
    """Why step 1 (in_force) left this document out."""
    if d.status != "published":
        return f"status is {d.status}"
    if d.effective_from > as_of:
        return f"not in force until {d.effective_from}"
    if d.series in current:
        return f"replaced by the newer version {current[d.series].id}"
    return f"expired on {d.effective_to}"


def why(persona: Persona, as_of: date, documents: list[Document], s: Scope) -> list[tuple[str, str]]:
    """One (document id, fate) per document, from the same rule functions scope() calls.
    Raises if the documents it keeps differ from the scope's, so the trace cannot drift."""
    current = {d.series: d for d in in_force(documents, as_of)}
    kept_ids = {d.id for d in s.documents}
    lines = []
    for d in sorted(documents, key=lambda d: d.id):
        if current.get(d.series) is not d:
            lines.append((d.id, f"dropped at step 1: {_step1_reason(d, current, as_of)}"))
            continue
        if not applies(d, persona):
            lines.append((d.id, f"dropped at step 2: applies to {d.applies_to}, not to {persona.unit}"))
            continue
        winners = [w.id for w in current.values() if w.overrides == d.series and applies(w, persona)]
        if winners:
            lines.append((d.id, f"dropped at step 3: {', '.join(winners)} declares it overrides {d.series}"))
            continue
        # Access comes last, after "dùng thay", so it never decides precedence (ADR 0010).
        if not allowed(d, persona):
            lines.append((d.id, f"dropped after step 3, access: {d.access} excludes {persona.name}"))
            continue
        lines.append((d.id, "kept"))
    if {i for i, fate in lines if fate == "kept"} != kept_ids:
        raise AssertionError("--why disagrees with scope(); fix the explanation, not the rules")
    return lines


if __name__ == "__main__":
    # Windows consoles default to cp1252, which cannot print Vietnamese.
    sys.stdout.reconfigure(encoding="utf-8")
    args = [a for a in sys.argv[1:] if a != "--why"]
    if len(args) != 2:
        sys.exit("usage: python scripts/show_scope.py <persona> <as_of> [--why]")
    persona_id, as_of_text = args
    as_of = date.fromisoformat(as_of_text)
    personas = load_personas(load_org())
    if persona_id not in personas:
        sys.exit(f"unknown persona {persona_id}")
    documents = load_documents()
    s = scope(personas[persona_id], as_of, documents)
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
    if "--why" in sys.argv[1:]:
        print("why:")
        for doc_id, fate in why(s.persona, as_of, documents, s):
            print(f"  {doc_id}: {fate}")
