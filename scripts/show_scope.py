"""Print the scope of one asker on one date: documents, conflict pairs and chunk count.

Run by hand: `uv run python scripts/show_scope.py <persona> <as_of>` (no key needed).
"""
from datetime import date
import sys

from appota_kb.integrations.data_files import load_documents, load_org, load_personas
from appota_kb.services.scope import scope


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("usage: python scripts/show_scope.py <persona> <as_of>")
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
