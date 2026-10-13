"""Check that data/ holds exactly the simulated data the Mission 1 rules were checked on.

Loads data/documents/*.md, data/org.yaml, data/personas.yaml and data/test_cases.yaml, then:
1. compares them field by field with DOCS, PERSONAS, ORG_TREE and TEST_MATRIX in adopted_rules.py
   (test cases 1-10 are the rows of TEST_MATRIX; the later rows are new) and checks every test case is well formed,
2. compares each document body with its text in artifacts.md ("Bodies"),
3. runs the rules part of every test case (steps 1-4 and step 7 with correct citations) on the loaded documents;
   a limitation row states the ideal result, so its check must fail, or the limitation no longer reproduces.
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
    if match is None:
        sys.exit(f"{path.name}: no front matter")
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

# 1c. Test cases: every row well formed, and rows 1-10 are the rows of TEST_MATRIX.
ids = [c["id"] for c in cases]
check(len(ids) == len(set(ids)), "test case ids are not unique")
for c in cases:
    tag = f"test case {c['id']}"
    check(c.get("kind") in ("good", "hard", "limitation"), f"{tag}: kind is not good, hard or limitation")
    check(c.get("card") in ("answer", "conflict", "refusal"), f"{tag}: card is not answer, conflict or refusal")
    check(c.get("persona") in ar.PERSONAS and c.get("as_of"), f"{tag}: unknown persona or no as_of")
    check(bool(c.get("questions")) and all(isinstance(q, str) and q for q in c["questions"]), f"{tag}: no questions")
    check(bool(c.get("expected_answer")), f"{tag}: no expected_answer")
    cites = c.get("must_cite", []) + c.get("may_cite", [])
    if c.get("card") == "answer":
        check(bool(c.get("must_cite")) and "conflict_pair" not in c, f"{tag}: an answer row needs must_cite only")
    elif c.get("card") == "conflict":
        check(len(c.get("conflict_pair", [])) == 2 and not cites, f"{tag}: a conflict row needs conflict_pair only")
    else:
        check(not cites and "conflict_pair" not in c, f"{tag}: a refusal row cites nothing")
    if "data_edit" in c:
        # Rules never read the body; the edit matters to retrieval and the LLM, so only check it still applies.
        edit = c["data_edit"]
        body = next((d["body"] for d in docs if d["id"] == edit["document"]), "")
        check(edit["remove"] in body.splitlines(), f"{tag}: data_edit line not found in {edit['document']}")

check(ids[:len(ar.TEST_MATRIX)] == [r["n"] for r in ar.TEST_MATRIX], "rows 1-10 differ from TEST_MATRIX")
for c, r in zip(cases, ar.TEST_MATRIX):
    tag = f"test case {c['id']}"
    check(c["persona"] == r["persona"] and dmy(c["as_of"]) == r["asof"], f"{tag}: persona or as_of differs")
    check(c["card"].upper() == r["expect"], f"{tag}: card differs")
    allowed = set(c.get("must_cite", []) + c.get("may_cite", []) + c.get("conflict_pair", []))
    check(set(c.get("must_cite", [])) <= set(r["cite"]) <= allowed, f"{tag}: citations differ")
    check(c["forbidden_by_rules"] == r["out_rules"] and c["forbidden_for_llm"] == r["out_llm"], f"{tag}: forbidden lists differ")

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

# 3. The rules part of every test case, on the loaded documents.
def correct_citations(c):
    """What a correct model cites: the must-cite documents, or one document of the conflict pair."""
    return c.get("must_cite", []) + c.get("conflict_pair", [])[:1]


print("\n== Test cases, rules part (steps 1-4, and step 7 with correct citations) ==")
failed = 0
for c in cases:
    scope = {d["id"] for d in ar.rulebook(loaded, c["persona"], c["as_of"])[0]}
    got = ar.answer(loaded, c["persona"], c["as_of"], correct_citations(c))
    in_scope = c.get("must_cite", []) + c.get("may_cite", []) + c.get("conflict_pair", []) + c["forbidden_for_llm"]
    problems = [f"{i} not in scope" for i in in_scope if i not in scope]
    problems += [f"{i} in scope" for i in c["forbidden_by_rules"] if i in scope]
    if not got.startswith(c["card"].upper()):
        problems.append(f"expected {c['card'].upper()}, got {got}")
    if c["kind"] == "limitation":
        status = "LIMITATION" if problems else "FAIL"
        if not problems:
            problems = ["the limitation no longer reproduces: update the row and its limitation issue"]
    else:
        status = "FAIL" if problems else "PASS"
    failed += status == "FAIL"
    print(f"  {c['id']:>2} {c['kind']:<10} {c['persona']:<5} {c['as_of']}  {status:<10}  {got}")
    for p in problems:
        print(f"        {p}")
    if c["forbidden_for_llm"]:
        lured = ar.answer(loaded, c["persona"], c["as_of"], c["forbidden_for_llm"])
        print(f"        if the LLM cites {' + '.join(c['forbidden_for_llm'])}: {lured}")

print(f"  {len(cases) - failed}/{len(cases)} test cases as expected")
sys.exit(1 if failed else 0)
