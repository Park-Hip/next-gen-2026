"""Core model rules BEFORE decisions M9-M11 (phase2_prompt.md section 3 as first written), on the old artifacts.md data.

Kept as evidence for production_review.md P1-P4. The adopted rules are in adopted_rules.py."""
from datetime import date
import copy

D = lambda s: date(*reversed([int(x) for x in s.split("/")])) if s else None

DOCS = [
  dict(id="LEAVE-GROUP-v1", topic="nghi_phep", access="all_staff", applies_to="Tập đoàn", status="published", frm="01/01/2024", to="", replaces="", overrides=""),
  dict(id="LEAVE-GAMECO-v1", topic="nghi_phep", access="all_staff", applies_to="GameCo", status="published", frm="01/01/2024", to="", replaces="", overrides=""),
  dict(id="LEAVE-GAMECO-v2", topic="nghi_phep", access="all_staff", applies_to="GameCo", status="published", frm="01/01/2026", to="31/12/2026", replaces="LEAVE-GAMECO-v1", overrides="LEAVE-GROUP-v1"),
  dict(id="LEAVE-GAMECO-v3", topic="nghi_phep", access="all_staff", applies_to="GameCo", status="published", frm="01/01/2027", to="", replaces="LEAVE-GAMECO-v2", overrides="LEAVE-GROUP-v1"),
  dict(id="LEAVE-GAMECO-v4-DRAFT", topic="nghi_phep", access="all_staff", applies_to="GameCo", status="draft", frm="", to="", replaces="LEAVE-GAMECO-v3", overrides="LEAVE-GROUP-v1"),
  dict(id="LEAVE-PAYCO-v1", topic="nghi_phep", access="all_staff", applies_to="PayCo", status="published", frm="01/01/2025", to="", replaces="", overrides=""),
  dict(id="SAL-BAND-GAMECO", topic="luong", access="roles:hr_gameco", applies_to="GameCo", status="published", frm="01/01/2026", to="", replaces="", overrides=""),
  dict(id="OT-GAMECO-v1", topic="lam_them_gio", access="all_staff", applies_to="GameCo", status="published", frm="01/01/2026", to="", replaces="", overrides=""),
  dict(id="TRAVEL-GAMECO-v1", topic="cong_tac_phi", access="all_staff", applies_to="GameCo", status="published", frm="01/01/2026", to="", replaces="", overrides=""),
]
PERSONAS = dict(
  minh=dict(path=["Tập đoàn", "GameCo", "Studio"], roles=["employee"]),
  lan=dict(path=["Tập đoàn", "Nhân sự Tập đoàn"], roles=["employee", "hr_group"]),
  ha=dict(path=["Tập đoàn", "PayCo", "Kế toán"], roles=["employee"]),
)

def allowed(d, p):
    a = d["access"]
    if a == "all_staff": return True
    if a.startswith("roles:"): return any(r in p["roles"] for r in a[6:].split(","))
    if a.startswith("unit:"): return a[5:] in p["path"]
    return False

def in_force(d, asof):
    if d["status"] != "published" or not d["frm"]: return False
    return D(d["frm"]) <= asof and (not d["to"] or asof <= D(d["to"]))

def resolve(docs, persona, topic, asof):
    p = PERSONAS[persona]
    kept = [d for d in docs if allowed(d, p) and in_force(d, asof) and d["applies_to"] in p["path"]]   # rule 2
    ids = {d["id"] for d in kept}
    # rule 4: relations count only among survivors
    removed = {d["replaces"] for d in kept if d["replaces"] in ids} | {d["overrides"] for d in kept if d["overrides"] in ids}
    winners = [d["id"] for d in kept if d["id"] not in removed and d["topic"] == topic]                 # rule 3
    if not winners: return "REFUSAL"
    if len(winners) > 1: return "CONFLICT " + " vs ".join(winners)                                     # rule 5
    return "ANSWER " + winners[0]

def run(label, docs, persona, asof, topic="nghi_phep"):
    print(f"{label:<62} {persona:<5} {asof}  -> {resolve(docs, persona, topic, D(asof))}")

print("== Baseline (old artifacts.md data) ==")
for who in ["minh", "lan", "ha"]: run("baseline", DOCS, who, "07/10/2026")

print("\n== Planned version switch: v3 takes effect as designed ==")
run("01/01/2027, v3 published and in force", DOCS, "minh", "01/01/2027")

print("\n== v3 is delayed (status back to draft) ==")
d = copy.deepcopy(DOCS); next(x for x in d if x["id"] == "LEAVE-GAMECO-v3")["status"] = "draft"
run("01/01/2027, v2 expired, v3 not published", d, "minh", "01/01/2027")

print("\n== Group publishes a new leave policy ==")
d = copy.deepcopy(DOCS); d.append(dict(id="LEAVE-GROUP-v2", topic="nghi_phep", access="all_staff", applies_to="Tập đoàn", status="published", frm="01/07/2026", to="", replaces="LEAVE-GROUP-v1", overrides=""))
run("GROUP-v2 replaces GROUP-v1 from 01/07/2026", d, "minh", "07/10/2026")

print("\n== Complementary document on the same topic ==")
d = copy.deepcopy(DOCS); d.append(dict(id="LEAVE-PROC-GAMECO", topic="nghi_phep", access="all_staff", applies_to="GameCo", status="published", frm="01/01/2026", to="", replaces="", overrides=""))
run("'Quy trình xin nghỉ phép GameCo' (procedure, no conflict)", d, "minh", "07/10/2026")

print("\n== Successor restricted to a narrower unit ==")
d = copy.deepcopy(DOCS); next(x for x in d if x["id"] == "LEAVE-GAMECO-v2")["applies_to"] = "Studio"
PERSONAS["tuan"] = dict(path=["Tập đoàn", "GameCo", "Marketing"], roles=["employee"])
run("v2 narrowed to Studio; GameCo Marketing asks", d, "tuan", "07/10/2026")
