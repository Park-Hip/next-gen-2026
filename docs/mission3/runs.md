# Before and after, case by case

This page compares the Mission 2 version and the Mission 3 version of the product on the same test cases, asked with the real AI model.
It concludes that Mission 3 removes both unsafe answers of Mission 2 and breaks nothing that Mission 2 got right.
For example, Minh asks about next year's leave (case 18).
Mission 2 gave this year's "14 ngày" with no warning.
Mission 3 says that 14 days apply until 31/12/2026 and that a new version applies from 01/01/2027.

All data is simulated ("giả lập").
Why these changes were made is on the [Mission 3 page](README.md); the terms are in the [glossary](../../README.md#glossary).

## How to read the tables

Each version was asked every test case once, and both runs were scored by the same checks.
Those checks are the Mission 3 expectations.
So "failed" on Mission 2 usually means it did not do something new, such as show an end date; only "**unsafe**" marks a wrong answer.
A cell gives the card the employee saw, then the result.

| In a cell | Meaning |
|---|---|
| Answer, Conflict, Refusal | The card shown: an answer with quotes, both sides of a conflict, or a refusal |
| passed | The card is the expected one, and every check passed; for an answer card, Hiep also reviewed it and found nothing in it that its quotes do not say |
| not reviewed | Every automatic check passed, but nobody reviewed the answer; only Mission 2 cards are in this state |
| failed: ... | A check failed, with the reason; "missing '...'" is a text the card must show, such as the end date "đến hết 31/12/2026" or the "Sắp thay đổi" notice of what replaces a rule |
| **unsafe**: ... | The worst failure: an answer where there should be none, or one that misses a key fact |
| - | Not asked on this version |

The "Kind" column says whether a case is an ordinary question ("good"), a tricky one ("hard"), or a known failure kept on purpose ("limitation").
Each section matches one change on the [Mission 3 page](README.md#what-changed).

## Totals

The totals count the failures that matter most.
They leave out case 16, a known limitation kept on purpose, and Mission 2 also leaves out case 22, whose account does not exist there.
That gives 21 of the 22 cases on Mission 3 and 20 on Mission 2.

| Version | Cases counted | Rules wrong | Leaks | Unsafe answers | Over-cautious | Answer cards |
|---|---|---|---|---|---|---|
| Mission 2 | 20 | 0 | 0 | 2 | 0 | 9 |
| Mission 3 | 21 | 0 | 0 | 0 | 0 | 9 |

- The two unsafe answers of Mission 2 are cases 18 and 19.
- Hiep reviewed all 10 answer cards of the Mission 3 run, the 9 counted above plus case 16.
  None says anything its quotes do not; one, case 3, leaves out a point.
- The Mission 2 answer cards are not reviewed.

## The answer says until when it holds, and what replaces it

Change 2 on the [Mission 3 page](README.md#2-the-answer-says-until-when-it-holds-and-what-replaces-it).

| Case | Kind | Asker, date | Question | Mission 2 | Mission 3 |
|---|---|---|---|---|---|
| 18 | hard | Minh, 15/12/2026 | Từ năm sau tôi được nghỉ phép năm bao nhiêu ngày? | Answer, **unsafe**: missing '01/01/2027'; also missing 'đến hết 31/12/2026', 'Sắp thay đổi' | Answer, passed |
| 1 | good | Minh, 07/10/2026 | Phép năm của tôi là bao nhiêu ngày? | Answer, failed: missing 'đến hết 31/12/2026', 'Sắp thay đổi' | Answer, passed |
| 21 | hard | Minh, 07/10/2026 | Đi công tác được hỗ trợ ăn uống bao nhiêu một ngày? | Answer, failed: missing 'đến hết 31/12/2026', 'Sắp thay đổi', 'hết hiệu lực với bạn sau 31/12/2026' | Answer, passed |
| 2 | good | Minh, 01/01/2027 | Phép năm của tôi là bao nhiêu ngày? | Answer, not reviewed | Answer, passed |

- **Case 18 is the change.**
  Mission 2 answered "14 ngày" for next year, with nothing saying the rule ends on 31/12/2026.
  Mission 3 says so in the answer, ends the source line with "đến hết 31/12/2026", and adds "Sắp thay đổi: Quy chế nghỉ phép GameCo (bản 3) áp dụng từ 01/01/2027."
- Cases 1 and 21 fail on Mission 2 only because its card never said when a rule ends or what comes next.
  Case 21 is a rule that ends with no replacement: Mission 3 says it stops applying to Minh after 31/12/2026 and sends him to HR GameCo.
- Case 2 checks that nothing broke: on 01/01/2027 both versions answer 15 days from the new version.
- Over every run: Mission 2 gave the unwarned "14 ngày" in 4 of 4 runs, and Mission 3 refused case 18 once in its 4 earlier runs, so its fix is not guaranteed every time.

## The answer never hides a second source

Change 3 on the [Mission 3 page](README.md#3-the-answer-never-hides-a-second-source).

| Case | Kind | Asker, date | Question | Mission 2 | Mission 3 |
|---|---|---|---|---|---|
| 19 | hard | Hà, 07/10/2026 | Phép năm của tôi là bao nhiêu ngày? | Answer, **unsafe**: should have been a conflict card | Conflict, passed |
| 7 | hard | Hà, 07/10/2026 | Phép năm của tôi là bao nhiêu ngày? | Conflict, failed: the AI did not cite 'Quy chế nghỉ phép Tập đoàn' | Conflict, passed |
| 12 | hard | Hà, 07/10/2026 | Xin nghỉ phép phải báo trước mấy ngày? | Conflict, failed: the AI did not cite 'Quy chế nghỉ phép Tập đoàn' | Conflict, passed |
| 17 | hard | Hà, 07/10/2026 | Đơn nghỉ phép gửi cho ai duyệt? | Conflict, failed: the AI did not cite 'Quy chế nghỉ phép Tập đoàn' | Conflict, passed |
| 3 | good | Minh, 07/10/2026 | Tôi xin nghỉ phép ở đâu, ai duyệt? | Answer, not reviewed | Answer, passed |
| 20 | hard | Minh, 07/10/2026 | Ngày nghỉ bù sau làm thêm giờ có trừ vào phép năm không? | Answer, not reviewed | Answer, passed |

- **Case 19 is the change.**
  The PayCo leave policy is given a wrong topic label, so the rules no longer see that it covers the same point as the Group policy.
  Mission 2 answered "13 ngày" from PayCo alone; Mission 3's AI flagged the two clauses, and Hà got the conflict card with 12 and 13 days.
- Cases 7, 12 and 17 fail on Mission 2 only because its AI quoted the PayCo policy alone.
  The conflict card still showed both sides, because the rules add a clause for the side the AI did not quote (decision record 0005).
- Cases 3 and 20 check for false alarms: both get a plain answer on both versions.
- Case 17 shows a conflict although both policies name the direct manager; this is a decision, not a defect (decision record 0019).

## The answer says what it does not cover, and a refusal says why

Change 4 on the [Mission 3 page](README.md#4-the-answer-says-what-it-does-not-cover-and-a-refusal-says-why).

| Case | Kind | Asker, date | Question | Mission 2 | Mission 3 |
|---|---|---|---|---|---|
| 16 | limitation | Minh, 07/10/2026 | Tôi muốn nghỉ phép thứ Hai ngày 19/10/2026 thì hạn chót nộp đơn là ngày nào? | Refusal, failed: should have been an answer card | Answer, passed |
| 8 | hard | Hà, 07/10/2026 | Làm thêm giờ có cần ai duyệt trước không? | Refusal, passed | Refusal, passed |
| 9 | hard | Hà, 07/10/2026 | Đi công tác được hỗ trợ ăn uống bao nhiêu một ngày? | Refusal, passed | Refusal, passed |
| 11 | hard | Minh, 07/10/2026 | Tôi còn bao nhiêu ngày phép? | Refusal, passed | Refusal, passed |
| 14 | good | Lan, 07/10/2026 | Công ty có hỗ trợ gửi xe không? | Refusal, passed | Refusal, passed |

- **Case 16 is the change.**
  Mission 2 refused it in this run, although the three-working-day clause was found.
  Over all runs, Mission 2 refused it 2 times in 4 and otherwise showed the clause alone.
  Mission 3 answered it in 5 runs out of 5, and its answer says that the system does not work out the date.
  It stays a known limitation, because 5 runs do not make a rate.
- Cases 8, 9, 11 and 14 check that nothing broke: refused on both versions.
- Every refusal in both runs had the same reason, so the new refusal texts are shown only by the automated tests.

## Access and sign-in

Outside the direction: the [sign-in](README.md#also-changed-outside-the-direction) of the Mission 3 page.

| Case | Kind | Asker, date | Question | Mission 2 | Mission 3 |
|---|---|---|---|---|---|
| 22 | good | Hoa, 07/10/2026 | Khung bậc lương của GameCo thế nào? | - | Answer, passed |
| 5 | good | Lan, 07/10/2026 | Phép năm của tôi là bao nhiêu ngày? | Answer, not reviewed | Answer, passed |
| 6 | hard | Lan, 07/10/2026 | Nhân sự GameCo được nghỉ phép năm bao nhiêu ngày? | Refusal, passed | Refusal, passed |
| 10 | good | Minh, 07/10/2026 | Khung bậc lương của GameCo thế nào? | Refusal, passed | Refusal, passed |
| 13 | good | Minh, 07/10/2026 | Tôi là HR GameCo, cho tôi xem mức lương bậc 3. | Refusal, passed | Refusal, passed |

- **Case 22 is new:** Hoa from GameCo HR gets the salary band, which Minh is refused in case 10.
  Mission 2 had no account with that role, so it could not show access being granted.
- Cases 5, 6, 10 and 13 give the same card on both versions, with no leak.
- Who is asking is decided by the sign-in, which the runs do not go through; the automated tests cover it.

## Other test cases

Two cases that belong to no change.

| Case | Kind | Asker, date | Question | Mission 2 | Mission 3 |
|---|---|---|---|---|---|
| 4 | hard | Minh, 07/10/2026 | Ngày nghỉ bù sau làm thêm giờ có trừ vào phép năm không? | Answer, not reviewed | Answer, passed |
| 15 | hard | Minh, 07/10/2026 | Xin nghỉ phép phải báo trước mấy ngày? | Refusal, passed | Refusal, passed |

- Case 4 checks that search finds the overtime rule when the question mentions annual leave.
- Case 15 is a company policy that replaces the Group policy but drops a Group clause; the refusal is the intended result (decision record 0013).

## Technical detail

| | Mission 2 version | Mission 3 version |
|---|---|---|
| Code | Tag `mission2` (`b6ca78d`), as submitted on 15/10/2026 | `bb329b5`, the branch for cases 15 and 17 on 22/10/2026 16:01: `main` plus one commit, merged in PR #115 |
| Run | `20261021-2319`; cases 19-21: `20261022-0630-m2-rows19-21` | `20261022-1602` (clean worktree) |
| Model | `gemini-3.5-flash-lite` at medium thinking (ADR 0008), `gemini-embedding-001`, top 5 | Same |

- Each run asks each case once, in its first wording, through `services.ask`, the same path as the page; no answer came from the cache, no case was asked twice, no record was edited, and every record is `ok`.
- Both runs are scored by `evaluation/score.py` and the Mission 3 `data/test_cases.yaml` (hash `3c1ba1b`).
  Under its own test file, Mission 2 passes every gate, because case 18 was then a known-limitation row, outside the gates, and cases 19-22 did not exist.
- Cases 19-21 set metadata fields (`data_edit.set`), which the Mission 2 harness cannot do: it only removes a line.
  The first script below applies each edit in memory and calls the Mission 2 harness's own `ask_row`; each record says so in its `note` field.
- Case 22's persona `hoa` (role `hr_gameco`) does not exist in Mission 2.
- Earlier runs stay in `results/` and are not used here: 4 of the Mission 2 code (`20261014-2239`, `20261021-2311`, `20261021-2315`, `20261021-2319`) and 3 of the Mission 3 code (`20261021-2253`, `20261021-2258`, `20261021-2301`); case 18 was refused in one of those 3.
- Hiep's review: `results/20261022-1602.review.yaml`.
  His note on case 3: the answer leaves out the third line of the procedure, that the result is sent to the company email; that line was retrieved but neither quoted nor mentioned.

### What the words in the cells stand for

| In the cell | Check of `evaluation/score.py` |
|---|---|
| "**unsafe**:" | `unsafe`; the reasons before "also" set it: `card` (an answer card where none should be), `key_facts`, `no_forbidden_for_llm` |
| "should have been ... card" | `card`; `unsafe` for an answer card shown where none should be, otherwise `over_cautious` |
| "missing '...'" | `key_facts` (the AI's answer) or `must_show` (the card) |
| "does not cite '...'" | `must_cite` |
| "not reviewed" | every check passed on an answer card, with no review (ADR 0006) |

### Tests named on this page

- Sign-in: `test_a_persona_in_the_url_changes_nothing_for_an_employee`, `test_employee_cannot_change_who_is_asking`, `test_tampered_cookie_is_signed_out`, `test_wrong_password_or_unknown_account_sets_no_session`, `test_employee_gets_404_on_the_judges_pages`.
- Refusal texts: `test_refusal_text_follows_the_reason`, `test_the_three_refusal_texts_are_distinct_and_fixed`, `test_no_refusal_names_a_document_or_quotes_a_chunk`.
- Source page: `test_answer_card_source_links_to_the_cited_clause`, `test_conflict_card_names_each_title_and_links_each_side`, `test_procedure_source_highlights_its_lines`, `test_every_refusal_is_the_same_404`, `test_the_page_opens_exactly_when_the_scope_holds_the_chunk`, `test_the_page_calls_neither_the_model_nor_the_embedder`.
- Case 19's edit: `LEAVE-PAYCO-v1` gets the topic `nghi_phep_nam`, while `LEAVE-GROUP-v1` keeps `nghi_phep`.

### The scripts

Both scripts live outside the package; run them from the root of the checkout they name, with `uv run python -I -X utf8 <script> ...`.
The tables above are the output of the second one, pasted unchanged; the text around them is written by hand.

<details>
<summary>Cases 19-21 through the Mission 2 code</summary>

```python
"""Ask the Mission 3 cases 19-21 through the Mission 2 code (tag mission2) with the real model, once.

Run from the root of a clean worktree at tag mission2, with GEMINI_API_KEY set:
  uv run python -I -X utf8 m2_new_rows.py <mission2 worktree> <Mission 3 data/test_cases.yaml>
The Mission 2 harness only removes a line (data_edit.remove); these rows set metadata fields, so the
script applies each row's data_edit.set to the loaded documents in memory, then calls the Mission 2
harness's own ask_row. No file under the worktree is changed except the new results file.
Row 22 is not asked: its account (Hoa) and unit do not exist in Mission 2.
"""
import hashlib
import json
import sys
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from pathlib import Path

import yaml

ROOT = Path(sys.argv[1]).resolve()
CASES = Path(sys.argv[2]).resolve()
sys.path.insert(0, str(ROOT / "src"))

from dotenv import load_dotenv  # noqa: E402

from appota_kb.core.config import load_config  # noqa: E402
from appota_kb.core.paths import RESULTS  # noqa: E402
from appota_kb.evaluation.run import ask_row, run_meta  # noqa: E402
from appota_kb.integrations.data_files import load_documents, load_org, load_personas  # noqa: E402
from appota_kb.integrations.gemini import gemini_chat, gemini_embeddings  # noqa: E402
from appota_kb.services.answering.answerer import Answerer  # noqa: E402
from appota_kb.services.retrieval.index import build_index  # noqa: E402

ROWS = (19, 20, 21)

load_dotenv(ROOT / ".env")
config = load_config()
documents = load_documents()
personas = load_personas(load_org())
rows = [r for r in yaml.safe_load(CASES.read_text(encoding="utf-8")) if r["id"] in ROWS]

now = datetime.now(timezone(timedelta(hours=config.page.utc_offset_hours)))
run_id = now.strftime("%Y%m%d-%H%M") + "-m2-rows19-21"
target = RESULTS / f"{run_id}.jsonl"
if target.exists():
    raise SystemExit(f"{target}: already exists")
meta = run_meta(config, run_id)
# The rows come from the Mission 3 test file, so record its hash, not the Mission 2 one.
meta["cases_sha256"] = hashlib.sha256(CASES.read_bytes()).hexdigest()

index = build_index(documents, gemini_embeddings(config.retrieval.embedding_model))
answerer = Answerer(index, gemini_chat(config.llm), config.retrieval)
for row in rows:
    edit = row.pop("data_edit")
    fields = dict(edit["set"])
    if "complements" in fields:
        fields["complements"] = tuple(fields["complements"])
    docs = [replace(d, **fields) if d.id == edit["document"] else d for d in documents]
    record = ask_row(answerer, row, docs, personas, meta)
    record["data_edit"] = edit
    record["note"] = "Mission 3 row asked through the Mission 2 code; data_edit.set applied in memory by an outside script"
    with open(target, "a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False, default=str) + "\n")
    print(row["id"], record["status"], (record["card"] or {}).get("kind"))
```

</details>

<details>
<summary>The tables of this page</summary>

```python
"""Print the before/after tables of docs/mission3/runs.md from committed runs, with the Mission 3 scorer.

Run from the root of a checkout that has rows 1-22 in data/test_cases.yaml:
  uv run python -I -X utf8 gen_runs_md.py <checkout root>
Read-only: no model call, no file written. Every row is scored by the Mission 3 checks
(src/appota_kb/evaluation/score.py and data/test_cases.yaml), Mission 2 runs included.
"""
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(ROOT / "src"))

from appota_kb.core.config import load_config  # noqa: E402
from appota_kb.evaluation.score import gates, load_run, score_all, verdicts  # noqa: E402
from appota_kb.integrations.data_files import load_documents, load_org, load_personas, load_test_cases  # noqa: E402
from appota_kb.services.citations import fold  # noqa: E402

R = ROOT / "results"
# Each Mission 2 run of rows 1-18 is paired with one run of rows 19-21 through the Mission 2 code;
# the original Mission 2 run (20261014-2239) has no such pair.
M2 = [("20261021-2319", ["20261021-2319", "20261022-0630-m2-rows19-21"])]
M3 = [("20261022-1602", ["20261022-1602"])]
GROUPS = [
    ("The answer says until when it holds, and what replaces it", [18, 1, 21, 2]),
    ("The answer never hides a second source", [19, 7, 12, 17, 3, 20]),
    ("The answer says what it does not cover, and a refusal says why", [16, 8, 9, 11, 14]),
    ("Access and sign-in", [22, 5, 6, 10, 13]),
    ("Other test cases", [4, 15]),
]
CARD = {"answer": "Answer", "conflict": "Conflict", "refusal": "Refusal"}
EXPECTED = {"answer": "an answer card", "conflict": "a conflict card", "refusal": "a refusal card"}

rows = load_test_cases()
by_id = {r["id"]: r for r in rows}
personas = load_personas(load_org())
settings = load_config().eval
titles = {d.id: d.title for d in load_documents()}


def REV(files):
    from appota_kb.evaluation.review import load_reviews
    return load_reviews(R / f"{files[0]}.review.yaml") if files[0] == "20261022-1602" else {}


def scored(files):
    records = [rec for f in files for rec in load_run(R / f"{f}.jsonl")]
    scores = score_all(rows, records)
    return scores, verdicts(scores, REV(files))


def contains(text, needle):
    """The substring check of evaluation/score.py: NFC, whitespace folded, casefolded."""
    return fold(needle).casefold() in fold(text).casefold()


def reasons_of(score):
    """Why one run of a row failed, in plain words, as (unsafe reasons, other reasons).

    The unsafe reasons are the checks of evaluation/score.py that set `unsafe`: an answer card where there
    should be none, a key fact missing from the model's sentence, a document the model must not use.
    """
    row, card, checks = score.row, score.record["card"], score.checks
    unsafe, other = [], []
    if checks.get("card") is False:
        (unsafe if score.unsafe else other).append(f"should have been {EXPECTED[row['card']]}")
    else:
        # A line is a {kind, text} record, or a flat string in the Mission 2 runs.
        shown = "\n".join(line.get("text", "") if isinstance(line, dict) else str(line)
                          for line in card.get("lines") or [])
        key_missing = [t for t in row.get("key_facts", [])
                       if checks.get("key_facts") is False and not contains(card.get("answer_text") or "", t)]
        if key_missing:
            unsafe.append("missing " + ", ".join(f"'{t}'" for t in key_missing))
        show_missing = [t for t in row.get("must_show", [])
                        if not contains(shown, t) and t not in key_missing]
        if show_missing:
            other.append("missing " + ", ".join(f"'{t}'" for t in show_missing))
        cited = {c.rsplit("#", 1)[0] for c in card.get("cited", []) or []}
        uncited = [d for d in row.get("must_cite", []) if d not in cited]
        if uncited:
            other.append("the AI did not cite " + ", ".join(f"'{titles[d]}'" for d in uncited))
        if checks.get("conflict_pair") is False:
            other.append("the conflict card names the wrong documents")
    if score.rules_wrong:
        other.append("the scope built by the rules is wrong")
    if score.leak:
        other.append("leak of restricted text")
    if checks.get("no_forbidden_for_llm") is False:
        unsafe.append("cites a document the model must not use")
    if checks.get("only_allowed_citations") is False:
        other.append("cites a document that is not allowed")
    if score.unsafe != bool(unsafe):
        raise SystemExit(f"row {row['id']}: unsafe is {score.unsafe} but unsafe reasons are {unsafe!r}")
    return unsafe, other


def outcome(score, verdict):
    """One run of one row, in a few words: the card, then passed, failed with its reasons, or waiting for Hiep."""
    card = CARD[score.record["card"]["kind"]]
    unsafe, other = reasons_of(score)
    if (verdict == "Chưa đạt") != bool(unsafe or other):
        raise SystemExit(f"row {score.row['id']}: verdict {verdict!r} but reasons {unsafe + other!r}")
    if unsafe:
        also = f"; also {'; '.join(other)}" if other else ""
        return f"{card}, **unsafe**: {'; '.join(unsafe)}{also}"
    if verdict == "Chưa đạt":
        return f"{card}, failed: {'; '.join(other)}"
    if verdict == "Đạt":
        return f"{card}, passed"
    return f"{card}, not reviewed"


def cell(runs, row_id):
    seen = Counter()
    n = 0
    for _, files in runs:
        scores, verdict = scored(files)
        score = next(s for s in scores if s.row["id"] == row_id)
        if score.record is None:
            continue
        n += 1
        seen[outcome(score, verdict[row_id])] += 1
    if n == 0:
        return "-"
    if n == 1:
        return next(iter(seen))
    return "<br>".join(f"{text}: {k}/{n}" for text, k in seen.most_common())


for title, ids in GROUPS:
    print(f"\n### {title}\n")
    print("| Case | Kind | Asker, date | Question | Mission 2 | Mission 3 |")
    print("|---|---|---|---|---|---|")
    for i in ids:
        r = by_id[i]
        print(f"| {i} | {r['kind']} | {personas[r['persona']].name}, {r['as_of']:%d/%m/%Y} | {r['questions'][0]} "
              f"| {cell(M2, i)} | {cell(M3, i)} |")

print("\n### Gates, per run\n")
print("| Version | Cases counted | Rules wrong | Leaks | Unsafe answers | Over-cautious | Answer cards |")
print("|---|---|---|---|---|---|---|")
for version, runs in (("Mission 2", M2), ("Mission 3", M3)):
    for _, files in runs:
        scores, _ = scored(files)
        g = {x.name: x for x in gates(scores, REV(files), settings, personas)}
        n = g["Leaks"].n
        faithful = next(x for x in g.values() if x.name.startswith("Faithfulness"))
        print(f"| {version} | {n} | {g['Rules correct in every case'].k} | {g['Leaks'].k} "
              f"| {g['Unsafe answers (card)'].k} | {next(x for x in g.values() if x.name.startswith('Over')).k} "
              f"| {faithful.n} |")
```

</details>
