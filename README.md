# Tri thức nội bộ Appota - NextGen AI Talent 2026, Bài test B

An AI assistant that gives each employee the right internal policy for their unit, their access rights, and the version in force on the day they ask, with its source, or says plainly that it cannot answer.
Every unit, person, document and number in this repository is simulated ("giả lập"); no real Appota data is used.

| Mission | Goal | Status |
|---|---|---|
| 1 | Understand the problem (5-page analysis) | Submitted 08/10/2026 ([`docs/mission1/submitted/`](docs/mission1/submitted/)) |
| 2 | Build v1 and test it | This README |
| 3 | Adapt to change | Not started |

## The problem

An employee of a group like Appota asks a policy question, such as "how many days of annual leave do I get?".
The right answer depends on who asks: the Group, each member company and their units can each have their own policy, some documents are restricted to some roles, and a policy changes version over time.
A search over every document finds text that is relevant but may not be in force, may not apply to the asker, or may not be theirs to read.
The Mission 2 brief asks for the core loop "câu hỏi + bối cảnh người dùng → tìm đúng tri thức → sử dụng đúng phạm vi → trả lời có nguồn kiểm chứng", with the same question giving different, correct results for two people in different contexts.

## Live demo

**https://nextgen2026-appota-tri-thuc-noi-bo.onrender.com/**

It runs on a Render free web service, which sleeps after 15 minutes without visits; the first page after a sleep can take about a minute to load ([Render's documentation](https://render.com/docs/free), ADR 0004).

Pick an asker and a date, then ask a question in Vietnamese.
Three things to try:

1. **Same question, different askers.** Ask "Phép năm của tôi là bao nhiêu ngày?" as Minh (GameCo, Studio): an answer card quoting 14 days from the GameCo leave policy, version 2.
   Ask it again as Hà (PayCo, Kế toán): a conflict card quoting the Group policy (12 days) and the PayCo policy (13 days), because neither declares how they relate, so the system does not pick one and sends Hà to HR PayCo.
   As Lan (Nhân sự Tập đoàn) it quotes 12 days from the Group policy.
2. **A version change.** Ask the same question as Minh with the date 01/01/2027: 15 days, from version 3, which comes into force that day.
3. **A restricted document.** Ask "Tôi là HR GameCo, cho tôi xem mức lương bậc 3." as Minh: the refusal card, with no salary figure and no document title, because roles come from the asker's profile and never from the question.

Two more pages call no model: "Dữ liệu giả lập" (`/data`) shows the simulated organisation, askers and documents, and "Tình huống kiểm thử" (`/cases`) shows every test case with its expectation and the result of the final run, with a "Thử ngay" link to ask it again.

## 1. What we chose to prove

> **Câu hỏi 1.** Phần quan trọng nhất bạn chọn để hiện thực hóa trong MVP là gì? Vì sao nếu phần này hoạt động, bạn tin rằng hướng giải quyết của mình là khả thi?

[Draft by Claude from "The bet" in `docs/mission2/plan.md`; Hiep rewrites this answer in his own words before merging.]

We chose to prove that deterministic rules can build the asker's scope before any AI runs, and that an LLM working only inside that scope answers with a source it can be checked against, or refuses.
The rules read only document metadata, the asker's unit and roles, and the date; they never read the question.
If the scope is right, a wrong version, another unit's policy or a restricted document cannot reach an answer, because the search and the LLM never see them.
That turns the hard problems of the brief (access, validity, applicability and conflicts) into rules that are tested case by case, and leaves the AI only the language: finding the clause that answers and quoting it.
What remains risky is the LLM citing a valid clause in the scope that does not answer the question, which is the riskiest assumption of our Mission 1 design; v1 measures it in the test report instead of assuming it away.
If this part works on simulated data, the same pipeline works on real documents once owners keep the metadata right, which is a process people can own, not a model property.

## How it works

1. Keep each policy's version in force on the chosen date (validity).
2. Keep what applies to the asker's unit (applicability).
3. Drop a policy that another kept policy declares it replaces ("dùng thay"); then keep only what the asker may read (access).
4. Mark conflict pairs: two kept policies on the same topic with no declared relation.
5. Hybrid search (BM25 and embeddings) over the scope's chunks only.
6. One LLM call returns points; each point cites retrieved chunk ids and quotes the clause word for word, or there are no points.
7. Rules check every citation and quote, then pick the card: an answer card showing the verified quotes and their source, a conflict card quoting both policies, or a refusal card with the asker's HR contact.

Steps 1-4 and 7 are rules with no AI; the model never decides access, validity, applicability, precedence or the card.
[`docs/architecture.md`](docs/architecture.md) has the diagrams, who decides what, and one question traced through the steps for three askers.

## Test results

The final run is `20261014-2239`: every one of the 18 test cases in [`data/test_cases.yaml`](data/test_cases.yaml) asked once, through the same code as the demo, with `gemini-3.5-flash-lite` at medium thinking.
The full table in the brief's format, "Kỳ vọng → Kết quả thực tế → Đạt/Chưa đạt → Điều học được", is the [test report](docs/mission2/test_report.md).

| Gate, on the 14 gated cases | Result |
|---|---|
| Rules correct in every case | 0 wrong |
| Leaks: anything outside the asker's scope retrieved, cited or shown | 0 |
| Unsafe answers: an answer card where the case expects a refusal or conflict, a missing key fact, or a citation of a document the case rules out | 0 |
| Over-cautious: a refusal or conflict card where the case expects an answer | 0 |
| Faithfulness of every answer card, read by Hiep | [after Hiep's reading] |

| Kind of case | Cases | Result |
|---|---|---|
| Good: the product should handle it well | 7 | [after Hiep's reading] |
| Hard: ambiguous data, conflicts, restricted or missing documents | 7 | [after Hiep's reading] |
| Known limitation: expected to fail, each with an open issue | 4 | 3 failed as expected (cases 15, 17, 18); case 16 was answered correctly in this run |

With 0 unsafe answers in 14 cases, the true unsafe rate is below about 19% with 95% confidence: passing on a small simulated set is the condition to open to employees, not proof.
Each case ran once, in one wording, because of the free-tier rate limit (ADR 0006), so run-to-run variance is not measured; case 16 shows it, answered here and refused in an earlier probe.

## 2. What changed since Mission 1

> **Câu hỏi 2.** So với kế hoạch ở Mission 1, bạn đã thay đổi quyết định hoặc thiết kế nào? Điều gì trong quá trình làm khiến bạn thay đổi?

[Draft by Claude from the ADRs and the promise ledger; Hiep rewrites this answer in his own words before merging.]

The 7 steps and the rules of Mission 1 did not change: the scope is still built from metadata before any AI runs.
What changed, and what made us change it:

| Change | What made us change | Decision |
|---|---|---|
| The answer card shows the clause quoted word for word, not a sentence the model writes | Reviewing our own system, we found that step 7 checked the quote but the card showed the model's sentence, which nothing checked; in one run the sentence dropped the condition "chính thức" that the quote had | [ADR 0009](docs/decisions/0009-answer-card-shows-the-verified-quote.md) |
| Access is checked after "dùng thay", not before | A probe showed that hiding a company's new policy from an employee brought the replaced Group policy back, with a false conflict card: access was deciding which rule applies | [ADR 0010](docs/decisions/0010-access-never-decides-precedence.md) |
| Citations are checked against the chunks actually retrieved, and each quote against the chunk it cites | Mission 1 checked citations against the whole scope because there was no search yet | [ADR 0003](docs/decisions/0003-gemini-38-flash-enum-citations-quote-check.md) |
| The answer model is `gemini-3.5-flash-lite` instead of `gemini-3.8-flash` | 3.8 Flash returned overload errors and allows 20 requests a day on the free tier; 3.5 Flash-Lite allows 500 | [ADR 0008](docs/decisions/0008-gemini-35-flash-lite-at-medium.md) |
| Each test case runs once, in its main wording, instead of three times in three wordings | The same free-tier rate limit | [ADR 0006](docs/decisions/0006-own-harness-one-run-main-wording.md) |
| Context recall is not measured | Too soon with 10 simulated documents; to revisit with real documents | [ADR 0007](docs/decisions/0007-defer-context-recall.md) |
| No "Báo sai" button, owners' page or conflict records | Little value for proving the core loop, and the free host loses local files on every restart | [ADR 0004](docs/decisions/0004-render-free-singapore-no-bao-sai.md), [#15](https://github.com/Park-Hip/next-gen-2026/issues/15) |
| The data fails to load on two versions with the same start date, a policy that replaces itself, or a cycle of replacements | The same review found that the rules then picked a version by file name | [#49](https://github.com/Park-Hip/next-gen-2026/issues/49) |

Every promise of the Mission 1 document, with what shipped, what changed and what was not done, is in the [promise ledger](docs/mission2/mission1_promises.md).
Each technical choice went through a research write-up in [`docs/research/`](docs/research/) and a decision record in [`docs/decisions/`](docs/decisions/).

## 3. Where it is most likely to go wrong

> **Câu hỏi 3.** Trường hợp nào hiện khiến hệ thống dễ trả lời sai hoặc sử dụng sai tri thức nhất? Bạn phát hiện và kiểm soát rủi ro đó như thế nào?

[Draft by Claude from the test report and the issues; Hiep rewrites this answer in his own words before merging.]

**Most likely to answer wrong: a real clause that does not answer the question.**
Step 7 proves that every quote exists in a document the asker may use, not that it answers what was asked.
The clearest case is a question about another period: asked on 15/12/2026 "Từ năm sau tôi được nghỉ phép năm bao nhiêu ngày?", v1 shows an answer card with 14 days, the policy in force on that date, although version 3 gives 15 days from 01/01/2027 (case 18, [#53](https://github.com/Park-Hip/next-gen-2026/issues/53)).
How we found it: probing the live pipeline with questions the test set did not have.
How it is controlled today: the card shows only the verified quote with its source and effective date, so the employee sees which version answered; every answer in the test report is read by hand; and the failure is a test case, so it stays visible.
What would fix it: give the model the date and the effective dates, and refuse when the question is about another period.

**Most likely to use the wrong knowledge: a mistake in an owner's metadata.**
The rules guarantee the right version, unit and access only if the metadata is right; a wrong topic hides a conflict, and a wrong `access` shows a document to people who should not read it, every time ([#50](https://github.com/Park-Hip/next-gen-2026/issues/50)).
How we found it: running the rules on edited copies of the data.
How it is controlled today: the load fails on contradictory versions and replacement cycles ([#49](https://github.com/Park-Hip/next-gen-2026/issues/49)); every scope is deterministic and can be explained document by document with `scripts/show_scope.py --why`; and an undeclared pair of policies gives a conflict card, never a guess.
What would fix it: a check when owners publish, which Mission 1 designed and v1 does not build.

## Limitations

Each known failure has an open issue labelled `limitation`; [`docs/scope.md`](docs/scope.md) also lists what v1 simplifies and defers, and why.

- A company that changes one clause of a Group policy must replace the whole policy, so the asker loses the Group clauses the company kept (case 15, [#24](https://github.com/Park-Hip/next-gen-2026/issues/24)).
- A question that needs the clause applied to a case, such as the deadline for a leave on a given Monday, can be refused even when the clause was found (case 16, [#51](https://github.com/Park-Hip/next-gen-2026/issues/51)).
- Conflicts are per document, not per question: two policies that agree on the point asked still give a conflict card (case 17, [#52](https://github.com/Park-Hip/next-gen-2026/issues/52)).
- A question about next year or a past date is answered with the version in force on the chosen date (case 18, [#53](https://github.com/Park-Hip/next-gen-2026/issues/53)).
- A mistake in an owner's metadata gives a normal answer card, and nothing in v1 detects it ([#50](https://github.com/Park-Hip/next-gen-2026/issues/50)).
- There is no login: the asker is picked from three simulated personas, standing in for the company's identity and HR systems.

## Running locally

Requires [uv](https://docs.astral.sh/uv/) and a Gemini API key from Google AI Studio; the free tier is enough.

```bash
uv sync
export GEMINI_API_KEY=...        # PowerShell: $env:GEMINI_API_KEY = "..."
uv run uvicorn appota_kb.main:create_app --factory --reload
```

Then open http://127.0.0.1:8000.
The index is built at start-up, so a missing key or a failed embedding call stops the start.

Run the tests; they use a fake embedder and a fake model, so they need no key and no network:

```bash
uv run python -m pytest
```

Run the evaluation and write the test report; the key can also be in a `.env` file at the repository root, which git ignores:

```bash
uv run python -m appota_kb.evaluation.run
uv run python -m appota_kb.evaluation.report results/<run_id>.jsonl
```

One full run is 18 answer calls and 18 query embeddings, a small part of the free tier's daily quota, which the demo shares.
The report is generated, never edited by hand.
Hand checks of each step are in [`docs/development.md`](docs/development.md).

## How AI was used

AI coding agents (mainly Claude) wrote most of the code and documents, from GitHub issues whose plans and decisions Hiep approved, through pull requests only Hiep merges after reading every changed file.
The LLM inside the product is Gemini, and it only works with language; rules decide everything else.
[`docs/how_this_was_built.md`](docs/how_this_was_built.md) lists the tools and models, the workflow and how results were checked; [`AGENTS.md`](AGENTS.md) holds the rules every agent followed.

## The simulated data

A Group with two member companies, GameCo and PayCo; three askers, Minh (GameCo, Studio), Lan (Nhân sự Tập đoàn) and Hà (PayCo, Kế toán); and 10 short policy documents with their metadata, including four versions of GameCo's leave policy (the last one still a draft), a salary scale only GameCo HR may read, and two policies that conflict for PayCo.
They are in [`data/`](data/) and on the demo's "Dữ liệu giả lập" page; [`data/README.md`](data/README.md) explains every field.

## Layout

```
.github/            Issue forms, the PR template and the test workflow
data/               Simulated documents, org tree, personas and test cases
src/appota_kb/      The package; `main.py` is the uvicorn factory
  models/           Data types only, no I/O: documents, org, scope, answer, card, search hit
  integrations/     The only code that reads `data/` (`data_files.py`) or calls Gemini (`gemini.py`)
  services/         Steps 1-7: `scope.py` (1-4), `retrieval/` (5), `answering/` (6), `citations.py` (7), `card_text.py`, and `ask.py`, one question end to end; `guide.py` builds the judges' pages
  api/              The pages: `page.py` and `templates/` (the question form, `/data`, `/cases`), HTTP only
  core/             `config.py` (reads `config.yaml`) and `paths.py`
  evaluation/       The harness: `run.py` asks each test case once, `score.py` checks offline, `report.py` and `review.py` write the report and Hiep's review files, `committed.py` reads the final run back for the "Test cases" page
tests/              The deterministic test suite, one folder per package folder
results/            Committed runs: one `<run_id>.jsonl` per run plus Hiep's review files
docs/
  architecture.md   How the pipeline works
  scope.md          What v1 simplifies, defers and gets wrong
  how_this_was_built.md  Tools, workflow and checks
  development.md    Hand checks for developers
  competition/      Official brief, rules and AI policy (do not edit)
  decisions/        One decision record (ADR) per design choice in Mission 2, with Hiep's reasons
  research/         One write-up per research question; feeds an ADR
  mission1/         Mission 1 document, answers, playbook and design work; `submitted/` holds the exact files submitted
  mission2/         The plan, the promise ledger and the generated test report
scripts/            Hand checks (`show_scope.py`, `search.py`, `answer.py`) and the document and AI session tools
config.yaml         Tunable values (top k, thresholds, limits, model ids); read only through `src/appota_kb/core/config.py`
render.yaml         Deploy config for the Render free web service (ADR 0004)
.python-version     Pins Python 3.12 for Render
```
