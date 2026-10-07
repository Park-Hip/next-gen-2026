"""Proposed per-question ("covers") resolver. NOT ADOPTED: rejected by Hiep in M14, kept as history for production_review.md P4."""
from datetime import date
import copy

D = lambda s: date(*reversed([int(x) for x in s.split("/")])) if s else None

# series = one document across its versions; covers = the specific questions a document answers
DOCS = [
  dict(id="LEAVE-GROUP-v1", series="LEAVE-GROUP", covers=["nghi_phep.so_ngay", "nghi_phep.thu_tuc"], access="all_staff", applies_to=["Tập đoàn"], status="published", frm="01/01/2024", overrides=[]),
  dict(id="LEAVE-GAMECO-v1", series="LEAVE-GAMECO", covers=["nghi_phep.so_ngay", "nghi_phep.thu_tuc"], access="all_staff", applies_to=["GameCo"], status="published", frm="01/01/2024", overrides=[]),
  dict(id="LEAVE-GAMECO-v2", series="LEAVE-GAMECO", covers=["nghi_phep.so_ngay", "nghi_phep.thu_tuc"], access="all_staff", applies_to=["GameCo"], status="published", frm="01/01/2026", overrides=["LEAVE-GROUP"]),
  dict(id="LEAVE-GAMECO-v3", series="LEAVE-GAMECO", covers=["nghi_phep.so_ngay", "nghi_phep.thu_tuc"], access="all_staff", applies_to=["GameCo"], status="published", frm="01/01/2027", overrides=["LEAVE-GROUP"]),
  dict(id="LEAVE-GAMECO-v4-DRAFT", series="LEAVE-GAMECO", covers=["nghi_phep.so_ngay"], access="all_staff", applies_to=["GameCo"], status="draft", frm="", overrides=["LEAVE-GROUP"]),
  dict(id="LEAVE-PAYCO-v1", series="LEAVE-PAYCO", covers=["nghi_phep.so_ngay", "nghi_phep.thu_tuc"], access="all_staff", applies_to=["PayCo"], status="published", frm="01/01/2025", overrides=[]),
  dict(id="SAL-BAND-GAMECO", series="SAL-BAND-GAMECO", covers=["luong.khung"], access="roles:hr_gameco", applies_to=["GameCo"], status="published", frm="01/01/2026", overrides=[]),
]
PERSONAS = dict(
  minh=dict(path=["Tập đoàn", "GameCo", "Studio"], roles=["employee"]),
  lan=dict(path=["Tập đoàn", "Nhân sự Tập đoàn"], roles=["employee", "hr_group"]),
  ha=dict(path=["Tập đoàn", "PayCo", "Kế toán"], roles=["employee"]),
  tuan=dict(path=["Tập đoàn", "GameCo", "Marketing"], roles=["employee"]),
)

def allowed(d, p):
    a = d["access"]
    if a == "all_staff": return True
    if a.startswith("roles:"): return any(r in p["roles"] for r in a[6:].split(","))
    return False

def current_versions(docs, asof):
    """Step 1, independent of the asker: per series, the published version with the latest effective date <= as-of.
    Older versions are superseded automatically; a future or draft version never removes the current one."""
    best = {}
    for d in docs:
        if d["status"] != "published" or not d["frm"] or D(d["frm"]) > asof: continue
        if d["series"] not in best or D(d["frm"]) > D(best[d["series"]]["frm"]): best[d["series"]] = d
    # effective_to is set only when a document really ends: once it passes, the series has no current version
    return [d for d in best.values() if not (d.get("to") and asof > D(d["to"]))]

def resolve(docs, persona, key, asof):
    p = PERSONAS[persona]
    cur = current_versions(docs, asof)
    # Step 2: asker filters on the current version only (a stale version can never come back)
    ok = [d for d in cur if allowed(d, p) and any(u in p["path"] for u in d["applies_to"])]
    # Step 3: per question key, an applicable source that overrides another source's series removes it
    cands = [d for d in ok if key in d["covers"]]
    beaten = {s for d in cands for s in d["overrides"]}
    winners = [d["id"] for d in cands if d["series"] not in beaten]
    if not winners: return "REFUSAL"
    if len(winners) > 1: return "CONFLICT " + " vs ".join(winners)
    return "ANSWER " + winners[0]

def run(label, docs, persona, asof, key="nghi_phep.so_ngay"):
    print(f"{label:<55} {persona:<5} {asof} {key:<26} -> {resolve(docs, persona, key, D(asof))}")

print("== Baseline ==")
for who in ["minh", "lan", "ha"]: run("baseline", DOCS, who, "07/10/2026")
run("restricted doc", DOCS, "minh", "07/10/2026", key="luong.khung")

print("\n== Version switch on 01/01/2027 ==")
run("v3 in force", DOCS, "minh", "01/01/2027")
d = copy.deepcopy(DOCS); next(x for x in d if x["id"] == "LEAVE-GAMECO-v3")["status"] = "draft"
run("v3 delayed", d, "minh", "01/01/2027")

d = copy.deepcopy(DOCS); next(x for x in d if x["id"] == "LEAVE-GAMECO-v3")["status"] = "draft"
next(x for x in d if x["id"] == "LEAVE-GAMECO-v2")["to"] = "31/12/2026"
run("v3 delayed, v2 keeps effective_to 31/12/2026 (P2)", d, "minh", "01/01/2027")

print("\n== Group publishes a new version ==")
d = copy.deepcopy(DOCS); d.append(dict(id="LEAVE-GROUP-v2", series="LEAVE-GROUP", covers=["nghi_phep.so_ngay", "nghi_phep.thu_tuc"], access="all_staff", applies_to=["Tập đoàn"], status="published", frm="01/07/2026", overrides=[]))
run("GROUP-v2 from 01/07/2026", d, "minh", "07/10/2026")
run("GROUP-v2 from 01/07/2026", d, "lan", "07/10/2026")

print("\n== Complementary procedure document ==")
d = copy.deepcopy(DOCS); d.append(dict(id="LEAVE-PROC-GAMECO", series="LEAVE-PROC-GAMECO", covers=["nghi_phep.dang_ky_he_thong"], access="all_staff", applies_to=["GameCo"], status="published", frm="01/01/2026", overrides=[]))
run("procedure added", d, "minh", "07/10/2026")
run("procedure added", d, "minh", "07/10/2026", key="nghi_phep.dang_ky_he_thong")

print("\n== Addendum changes one clause of the Group policy ==")
d = copy.deepcopy(DOCS); d.append(dict(id="LEAVE-ADDENDUM-PAYCO", series="LEAVE-ADDENDUM-PAYCO", covers=["nghi_phep.chuyen_phep"], access="all_staff", applies_to=["PayCo"], status="published", frm="01/01/2026", overrides=["LEAVE-GROUP"]))
next(x for x in d if x["id"] == "LEAVE-GROUP-v1")["covers"].append("nghi_phep.chuyen_phep")
run("PayCo addendum covers only carry-over", d, "ha", "07/10/2026", key="nghi_phep.chuyen_phep")
run("PayCo addendum covers only carry-over", d, "ha", "07/10/2026", key="nghi_phep.so_ngay")

print("\n== Successor narrowed to Studio ==")
d = copy.deepcopy(DOCS); next(x for x in d if x["id"] == "LEAVE-GAMECO-v2")["applies_to"] = ["Studio"]
run("v2 applies to Studio only; Marketing asks", d, "tuan", "07/10/2026")
