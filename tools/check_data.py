"""Check that data/ holds exactly the simulated data the Mission 1 rules were checked on.

Loads data/documents/*.md, data/org.yaml, data/personas.yaml and data/test_cases.yaml, then:
1. compares them field by field with DOCS, PERSONAS, ORG_TREE and TEST_MATRIX in adopted_rules.py,
2. compares each document body with its text in artifacts.md ("Bodies"),
3. reruns the deterministic test matrix of adopted_rules.py on the loaded documents.
Run: python -I -X utf8 tools/check_data.py
"""
from pathlib import Path
import importlib.util
import re
import sys

import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
CHECKS = ROOT / "docs/mission1/redraft/checks/adopted_rules.py"
ARTIFACTS = ROOT / "docs/mission1/redraft/artifacts.md"

spec = importlib.util.spec_from_file_location("adopted_rules", CHECKS)
ar = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ar)

errors = []


def check(ok, message):
    if not ok:
        errors.append(message)


def dmy(value):
    """ISO date from YAML -> the dd/mm/yyyy string adopted_rules.py uses; None -> ''."""
    return value.strftime("%d/%m/%Y") if value else ""


def load_document(path):
    text = path.read_text(encoding="utf-8")
    match = re.match(r"---\n(.*?)\n---\n\n(.*)", text, re.S)
    check(match is not None, f"{path.name}: no front matter")
    meta = yaml.safe_load(match.group(1))
    meta["body"] = match.group(2).strip()
    return meta


docs = [load_document(p) for p in sorted((DATA / "documents").glob("*.md"))]
org = yaml.safe_load((DATA / "org.yaml").read_text(encoding="utf-8"))
personas = yaml.safe_load((DATA / "personas.yaml").read_text(encoding="utf-8"))
cases = yaml.safe_load((DATA / "test_cases.yaml").read_text(encoding="utf-8"))

# 1a. Documents: same fields as adopted_rules.DOCS, and the file name is the id.
loaded = [dict(id=d["id"], series=d["series"], topic=d["topic"], access=d["access"], applies_to=d["applies_to"],
               status=d["status"], frm=dmy(d["effective_from"]), to=dmy(d["effective_to"]),
               overrides=d["overrides"] or "", complements=d["complements"]) for d in docs]
expected = {d["id"]: d for d in ar.DOCS}
check(sorted(expected) == sorted(d["id"] for d in loaded), "document ids differ from adopted_rules.DOCS")
for d in loaded:
    check(d == expected.get(d["id"]), f"{d['id']}: metadata differs from adopted_rules.DOCS")
for p, d in zip(sorted((DATA / "documents").glob("*.md")), docs):
    check(p.stem == d["id"], f"{p.name}: file name is not the id {d['id']}")

# 1b. Org tree and personas: unit paths rebuilt from org.yaml match ORG_TREE and PERSONAS.
parent = {u["name"]: u["parent"] for u in org}


def path_of(unit):
    path = []
    while unit:
        path.insert(0, unit)
        unit = parent[unit]
    return path


check(sorted(path_of(u) for u in parent) == sorted(ar.ORG_TREE), "org.yaml differs from ORG_TREE")
for u in org:
    nearest = next((x for x in reversed(path_of(u["name"])) if any(o["name"] == x and o.get("hr") for o in org)), None)
    check(nearest is not None, f"{u['name']}: no HR contact on its path")
check(sorted(p["id"] for p in personas) == sorted(ar.PERSONAS), "persona ids differ from PERSONAS")
for p in personas:
    want = ar.PERSONAS.get(p["id"], {})
    check(path_of(p["unit"]) == want.get("path") and p["roles"] == want.get("roles"), f"persona {p['id']} differs")

# 1c. Test cases: same rows as TEST_MATRIX.
check([c["n"] for c in cases] == [r["n"] for r in ar.TEST_MATRIX], "test case numbers differ from TEST_MATRIX")
for c, r in zip(cases, ar.TEST_MATRIX):
    tag = f"test case {c['n']}"
    check(c["persona"] == r["persona"] and dmy(c["as_of"]) == r["asof"], f"{tag}: persona or as_of differs")
    check(c["expected"].upper() == r["expect"], f"{tag}: expected differs")
    allowed = set(c["must_cite"]) | set(c.get("may_cite", []))
    check(set(c["must_cite"]) <= set(r["cite"]) <= allowed, f"{tag}: citations differ")
    check(c["forbidden_by_rules"] == r["out_rules"] and c["forbidden_for_llm"] == r["out_llm"], f"{tag}: forbidden lists differ")
    check(c.get("question"), f"{tag}: no question")

# 2. Bodies match artifacts.md word for word.
section = ARTIFACTS.read_text(encoding="utf-8").split("### Bodies", 1)[1].split("\n## ", 1)[0]
bodies = {m.group(1): m.group(2).strip() for m in
          re.finditer(r"\*\*`([A-Za-z0-9-]+)`\*\*\n\n(.*?)(?=\n\n\*\*`|\Z)", section, re.S)}
for d in docs:
    want = bodies.get(d["id"], "").split("\n\nĐiều 3 was added")[0]  # editorial note after the OT body
    check(d["body"] == want, f"{d['id']}: body differs from artifacts.md")

if errors:
    print("\n".join(errors))
    sys.exit(1)
print(f"data/ matches adopted_rules.py and artifacts.md: {len(docs)} documents, {len(org)} units, "
      f"{len(personas)} personas, {len(cases)} test cases")

# 3. The deterministic test matrix, on the loaded documents.
ar.run_matrix(loaded)
