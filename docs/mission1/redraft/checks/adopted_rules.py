"""Adopted core model (decisions M9-M12, M14-M15, M18), run on the artifacts.md document set.

- rulebook(): steps 1-4 for one asker; does not read the question.
- answer(): step 7, the post-check on the documents the model cites.
- lint(): the publish-time check (M15). It runs the same resolver for every unit in the org tree,
  on today and on every future effective date, and lists same-topic pairs with no declared relation.
- run_matrix(): the deterministic columns of the Phase 4 test matrix (artifacts.md, V1).
Run: python -I -X utf8 adopted_rules.py
"""
from datetime import date, timedelta
from itertools import combinations
import copy

D = lambda s: date(*reversed([int(x) for x in s.split("/")])) if s else None

# Mirrors the metadata table in artifacts.md (giả lập).
# effective_to is set only when the document really ends (temporary, or repealed with no successor).
DOCS = [
  dict(id="LEAVE-GROUP-v1", series="LEAVE-GROUP", topic="nghi_phep", access="all_staff", applies_to="Tập đoàn", status="published", frm="01/01/2024", to="", overrides="", complements=[]),
  dict(id="LEAVE-GAMECO-v1", series="LEAVE-GAMECO", topic="nghi_phep", access="all_staff", applies_to="GameCo", status="published", frm="01/01/2024", to="", overrides="", complements=[]),
  dict(id="LEAVE-GAMECO-v2", series="LEAVE-GAMECO", topic="nghi_phep", access="all_staff", applies_to="GameCo", status="published", frm="01/01/2026", to="", overrides="LEAVE-GROUP", complements=[]),
  dict(id="LEAVE-GAMECO-v3", series="LEAVE-GAMECO", topic="nghi_phep", access="all_staff", applies_to="GameCo", status="published", frm="01/01/2027", to="", overrides="LEAVE-GROUP", complements=[]),
  dict(id="LEAVE-GAMECO-v4-DRAFT", series="LEAVE-GAMECO", topic="nghi_phep", access="all_staff", applies_to="GameCo", status="draft", frm="", to="", overrides="LEAVE-GROUP", complements=[]),
  dict(id="LEAVE-PROC-GAMECO-v1", series="LEAVE-PROC-GAMECO", topic="nghi_phep", access="all_staff", applies_to="GameCo", status="published", frm="01/01/2026", to="", overrides="", complements=["LEAVE-GAMECO"]),
  dict(id="LEAVE-PAYCO-v1", series="LEAVE-PAYCO", topic="nghi_phep", access="all_staff", applies_to="PayCo", status="published", frm="01/01/2025", to="", overrides="", complements=[]),
  dict(id="SAL-BAND-GAMECO", series="SAL-BAND-GAMECO", topic="luong", access="roles:hr_gameco", applies_to="GameCo", status="published", frm="01/01/2026", to="", overrides="", complements=[]),
  dict(id="OT-GAMECO-v1", series="OT-GAMECO", topic="lam_them_gio", access="all_staff", applies_to="GameCo", status="published", frm="01/01/2026", to="", overrides="", complements=[]),
  dict(id="TRAVEL-GAMECO-v1", series="TRAVEL-GAMECO", topic="cong_tac_phi", access="all_staff", applies_to="GameCo", status="published", frm="01/01/2026", to="", overrides="", complements=[]),
]
PERSONAS = dict(
  minh=dict(path=["Tập đoàn", "GameCo", "Studio"], roles=["employee"]),
  lan=dict(path=["Tập đoàn", "Nhân sự Tập đoàn"], roles=["employee", "hr_group"]),
  ha=dict(path=["Tập đoàn", "PayCo", "Kế toán"], roles=["employee"]),
)
ORG_TREE = [["Tập đoàn"], ["Tập đoàn", "Nhân sự Tập đoàn"], ["Tập đoàn", "GameCo"], ["Tập đoàn", "GameCo", "Studio"],
            ["Tập đoàn", "PayCo"], ["Tập đoàn", "PayCo", "Kế toán"]]
INTENDED_CONFLICTS = {frozenset(("LEAVE-GROUP", "LEAVE-PAYCO"))}  # trap T7, kept on purpose

def allowed(d, roles, path):
    a = d["access"]
    if a == "all_staff": return True
    if a.startswith("roles:"): return any(r in roles for r in a[6:].split(","))
    if a.startswith("unit:"): return a[5:] in path
    return False

def current_versions(docs, asof):
    """Step A (same for every asker): per series, the published version with the latest effective_from <= as-of.
    A series has no current version once that version's effective_to has passed."""
    best = {}
    for d in docs:
        if d["status"] != "published" or not d["frm"] or D(d["frm"]) > asof: continue
        if d["series"] not in best or D(d["frm"]) > D(best[d["series"]]["frm"]): best[d["series"]] = d
    return [d for d in best.values() if not (d["to"] and asof > D(d["to"]))]

def declared(a, b):
    """True if either document lists the other's series in 'complements' (the relation is symmetric)."""
    return b["series"] in a["complements"] or a["series"] in b["complements"]

def winners_and_gaps(docs, path, topic, asof, roles=None):
    kept = [d for d in current_versions(docs, asof)
            if (roles is None or allowed(d, roles, path)) and d["applies_to"] in path]       # Step B
    beaten = {d["overrides"] for d in kept}                                                   # Step C
    winners = [d for d in kept if d["series"] not in beaten and d["topic"] == topic]         # Step D
    gaps = [(a, b) for a, b in combinations(winners, 2) if not declared(a, b)]                # Step E
    return winners, gaps

def rulebook(docs, persona, asof):
    """Steps 1-4 (M18): the documents left for this asker and the conflict pairs, per topic, without the question."""
    p = PERSONAS[persona]
    kept, gaps = [], []
    for topic in sorted({d["topic"] for d in docs}):
        w, g = winners_and_gaps(docs, p["path"], topic, asof, p["roles"])
        kept += w; gaps += g
    return kept, gaps

def answer(docs, persona, asof, cited):
    """Step 7 (M18, RV5): rules decide the outcome from the documents the model cites.
    No citation, or any citation outside what was retrieved, refuses the whole answer (M7):
    the model only sees retrieved chunks, so such a citation means it invented a source.
    Here the rulebook stands in for the retrieved set, since there is no retriever yet.
    A cited document in a conflict pair shows both documents of the pair."""
    kept, gaps = rulebook(docs, persona, asof)
    if not cited or any(i not in {d["id"] for d in kept} for i in cited): return "REFUSAL"
    hit = [(a, b) for a, b in gaps if a["id"] in cited or b["id"] in cited]
    if hit: return "CONFLICT " + "; ".join(f"{a['id']} vs {b['id']}" for a, b in hit)
    return "ANSWER citing " + " + ".join(cited)

def model_cites(docs, persona, asof, subject):
    """Stand-in for steps 5-6 (retriever and LLM), for tests only: a correct model cites the documents
    in the rulebook on the question's subject. The system itself never classifies the question."""
    return [d["id"] for d in rulebook(docs, persona, asof)[0] if d["topic"] == subject]

def lint(docs, today):
    """Publish-time check (M15): undeclared same-topic pairs for any unit, today and on every future date where
    the set of current versions changes (a version starts, or a document ends the day after its effective_to).
    Access is ignored on purpose: a conflict in the data exists whoever reads it."""
    changes = {D(d["frm"]) for d in docs if d["frm"]} | {D(d["to"]) + timedelta(days=1) for d in docs if d["to"]}
    dates = sorted({today} | {x for x in changes if x > today})
    found = set()
    for asof in dates:
        for path in ORG_TREE:
            for topic in sorted({d["topic"] for d in docs}):
                for a, b in winners_and_gaps(docs, path, topic, asof)[1]:
                    found.add((asof, " / ".join(path), a["id"], b["id"], frozenset((a["series"], b["series"])) in INTENDED_CONFLICTS))
    return sorted(found)

def run(label, docs, persona, asof, subject="nghi_phep", cited=None):
    if cited is None: cited = model_cites(docs, persona, D(asof), subject)
    print(f"{label:<45} {persona:<5} {asof} -> {answer(docs, persona, D(asof), cited)}")

# Phase 4 test matrix (artifacts.md). Only the parts rules decide are checked here; the LLM parts need Mission 2.
# cite: what a correct model cites. out_rules: must not be cited and is outside the rulebook, so rules guarantee it.
# out_llm: must not be cited but is inside the rulebook, so only the LLM can avoid it.
TEST_MATRIX = [
  dict(n=1, persona="minh", asof="07/10/2026", expect="ANSWER", cite=["LEAVE-GAMECO-v2"],
       out_rules=["LEAVE-GROUP-v1", "LEAVE-GAMECO-v1", "LEAVE-GAMECO-v3", "LEAVE-GAMECO-v4-DRAFT", "LEAVE-PAYCO-v1"], out_llm=[]),
  dict(n=2, persona="minh", asof="01/01/2027", expect="ANSWER", cite=["LEAVE-GAMECO-v3"],
       out_rules=["LEAVE-GAMECO-v2", "LEAVE-GAMECO-v1", "LEAVE-GAMECO-v4-DRAFT", "LEAVE-GROUP-v1", "LEAVE-PAYCO-v1"], out_llm=[]),
  dict(n=3, persona="minh", asof="07/10/2026", expect="ANSWER", cite=["LEAVE-PROC-GAMECO-v1", "LEAVE-GAMECO-v2"],
       out_rules=["LEAVE-GROUP-v1", "LEAVE-GAMECO-v1"], out_llm=[]),
  dict(n=4, persona="minh", asof="07/10/2026", expect="ANSWER", cite=["OT-GAMECO-v1"],
       out_rules=["LEAVE-GROUP-v1", "LEAVE-GAMECO-v1"], out_llm=[]),
  dict(n=5, persona="lan", asof="07/10/2026", expect="ANSWER", cite=["LEAVE-GROUP-v1"],
       out_rules=["LEAVE-GAMECO-v2", "LEAVE-PAYCO-v1"], out_llm=[]),
  dict(n=6, persona="lan", asof="07/10/2026", expect="REFUSAL", cite=[],
       out_rules=["LEAVE-GAMECO-v2"], out_llm=["LEAVE-GROUP-v1"]),
  dict(n=7, persona="ha", asof="07/10/2026", expect="CONFLICT", cite=["LEAVE-PAYCO-v1"],
       out_rules=["LEAVE-GAMECO-v2", "LEAVE-PROC-GAMECO-v1"], out_llm=[]),
  dict(n=8, persona="ha", asof="07/10/2026", expect="REFUSAL", cite=[],
       out_rules=["OT-GAMECO-v1"], out_llm=["LEAVE-GROUP-v1", "LEAVE-PAYCO-v1"]),
  dict(n=9, persona="ha", asof="07/10/2026", expect="REFUSAL", cite=[],
       out_rules=["TRAVEL-GAMECO-v1"], out_llm=["LEAVE-GROUP-v1", "LEAVE-PAYCO-v1"]),
  dict(n=10, persona="minh", asof="07/10/2026", expect="REFUSAL", cite=[],
       out_rules=["SAL-BAND-GAMECO"], out_llm=["LEAVE-GAMECO-v2", "LEAVE-PROC-GAMECO-v1", "OT-GAMECO-v1", "TRAVEL-GAMECO-v1"]),
]

def run_matrix(docs):
    """Per row: must-cite documents are in the rulebook, out_rules documents are not, out_llm documents are,
    and step 7 gives the expected outcome when the model cites correctly. Also shows what step 7 does
    if the model cites the out_llm documents: that error is the LLM's to avoid (V2), rules cannot stop it."""
    print("\n== Phase 4 test matrix, deterministic part ==")
    passed = 0
    for r in TEST_MATRIX:
        asof = D(r["asof"])
        ids = {d["id"] for d in rulebook(docs, r["persona"], asof)[0]}
        got = answer(docs, r["persona"], asof, r["cite"])
        errors = [f"{i} not in rulebook" for i in r["cite"] + r["out_llm"] if i not in ids]
        errors += [f"{i} in rulebook" for i in r["out_rules"] if i in ids]
        if not got.startswith(r["expect"]): errors.append(f"expected {r['expect']}, got {got}")
        passed += not errors
        print(f"  {r['n']:>2} {r['persona']:<5} {r['asof']}  {'PASS' if not errors else 'FAIL'}  {got}")
        for e in errors: print(f"       {e}")
        if r["out_llm"]: print(f"       if the LLM cites {' + '.join(r['out_llm'])}: {answer(docs, r['persona'], asof, r['out_llm'])}")
    print(f"  {passed}/{len(TEST_MATRIX)} rows pass")
    # Zero failures in n cases only bounds the true failure rate: 95% upper bound = 1 - 0.05^(1/n).
    n = 3 * len(TEST_MATRIX)  # Mission 2 asks every row in 3 phrasings
    print(f"  0 failures in {n} cases: true rate may still be up to {1 - 0.05 ** (1 / n):.1%}")

def show_lint(label, docs):
    print(f"\n== Publish-time check: {label} ==")
    rows = lint(docs, D("07/10/2026"))
    for asof, path, a, b, intended in rows:
        print(f"  {asof:%d/%m/%Y}  {path:<28} {a} vs {b}  {'(intended, T7)' if intended else 'NEEDS A DECLARATION'}")
    if not rows: print("  no undeclared pairs")

if __name__ == "__main__":
    print("== Baseline, 07/10/2026 ==")
    for who in ["minh", "lan", "ha"]: run("leave question", DOCS, who, "07/10/2026")
    run("salary band (T4)", DOCS, "minh", "07/10/2026", subject="luong")

    print("\n== Post-check (M18) ==")
    run("Hà, model cites only the Group policy", DOCS, "ha", "07/10/2026", cited=["LEAVE-GROUP-v1"])
    run("Hà asks about overtime, nothing relevant", DOCS, "ha", "07/10/2026", subject="lam_them_gio")
    run("Minh, model cites a removed version", DOCS, "minh", "07/10/2026", cited=["LEAVE-GAMECO-v1"])
    run("Minh, one valid and one invented citation", DOCS, "minh", "07/10/2026", cited=["LEAVE-GAMECO-v2", "LEAVE-GAMECO-v1"])

    print("\n== Changes that broke the old rules ==")
    run("v3 takes effect as planned", DOCS, "minh", "01/01/2027")
    d = copy.deepcopy(DOCS); next(x for x in d if x["id"] == "LEAVE-GAMECO-v3")["status"] = "draft"
    run("v3 delayed", d, "minh", "01/01/2027")
    d = copy.deepcopy(DOCS); d.append(dict(id="LEAVE-GROUP-v2", series="LEAVE-GROUP", topic="nghi_phep", access="all_staff", applies_to="Tập đoàn", status="published", frm="01/07/2026", to="", overrides="", complements=[]))
    run("Group publishes LEAVE-GROUP-v2", d, "minh", "07/10/2026")
    run("Group publishes LEAVE-GROUP-v2", d, "lan", "07/10/2026")
    d = copy.deepcopy(DOCS); next(x for x in d if x["id"] == "LEAVE-GAMECO-v2")["to"] = "30/06/2026"
    next(x for x in d if x["id"] == "LEAVE-GAMECO-v3")["status"] = "draft"
    run("GameCo repeals its policy after 30/06/2026", d, "minh", "07/10/2026")

    print("\n== Complementary document (T11) ==")
    d = copy.deepcopy(DOCS); next(x for x in d if x["id"] == "LEAVE-PROC-GAMECO-v1")["complements"] = []
    run("procedure, relation not declared", d, "minh", "07/10/2026")
    run("procedure, declared complements", DOCS, "minh", "07/10/2026")

    show_lint("data as in artifacts.md", DOCS)

    d = copy.deepcopy(DOCS); next(x for x in d if x["id"] == "LEAVE-GAMECO-v3")["to"] = "30/06/2027"
    show_lint("GameCo announces it repeals v3 after 30/06/2027", d)

    run_matrix(DOCS)
