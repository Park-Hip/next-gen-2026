# 0007. Context recall is deferred until we have real documents

- Status: Accepted
- Date: 2026-10-13
- Origin: Hiep
- Supersedes: The "context recall" row of Mission 1 V1 and RV13 ("chỉ theo dõi")
- Issue: #12
- Research: None

## In short

- **The problem:** Mission 1 planned to track "context recall": whether the clause that answers a question is among those given to the AI.
  Measuring it means labelling every test question with the clauses that hold its answer.
  All current documents are simulated: 10 short files and 25 clauses.
- **The decision:** Mission 2 does not measure context recall.
  No such labels are added to the test cases, and neither the search check nor the evaluation report prints a recall figure.
  Hiep reads the ranked clauses for every row by hand instead.
- **What the employee sees:** Nothing; this concerns the test report only.
- **What we give up:** The Mission 2 report has no "context recall" row, which a reader of the Mission 1 table will notice.
  A search miss shows up downstream as a wrong refusal or a wrong citation, not as a separate number.

## Context

The submitted metrics table tracked context recall as a diagnostic with no threshold.
Measuring it needs a label for each test question saying which clauses hold the answer.
The implementation plan for the search work recommended adding those labels to the test file and printing context recall for every row.
Hiep rejected that recommendation on 13/10/2026.
All current documents are simulated ("giả lập"): 10 short files and 25 clauses.

## Options considered

1. **Add the labels and print context recall per row** - the plan's recommendation.
2. **Defer context recall until real documents exist** (chosen).

## Decision

Mission 2 does not measure context recall.
No answer-clause labels are added to the test cases, and neither the manual search check nor the evaluation report prints a recall figure.
The manual check prints the ranked clauses for every row, and Hiep reads them.
The idea is parked under "Deferred ideas" in `docs/mission1/playbook.md`.

## Reasons

Hiep, 13/10/2026: "it is too soon to measure recall in this mission and we should defer this. Revisit when we have real document."

## Consequences

Drafted by Claude from Hiep's decision; approved by Hiep when he merged PR #28 on 13/10/2026.

- The line in the search task "context recall printed for every row" became "the top 5 printed for every row", and the evaluation task no longer tracks context recall.
- A reader of the Mission 1 table will find "context recall" missing from the Mission 2 report; mandatory question 2 can cite this ADR as a change since Mission 1.
- Retrieval quality is still visible: the run log and the manual check show each returned clause with its fused score and its keyword and meaning-based ranks.
- A retrieval miss shows up downstream, as a wrong refusal or a wrong citation in the evaluation, not as a separate number.

## Would change if

- Real Appota documents arrive (Hiep, 13/10/2026: "Revisit when we have real document").

## Evidence

Hiep's answer in the plan comment on the search task.
Evidence log lines of 13/10/2026 (Claude Opus 5.5, Pi).

## Technical detail

- Not added: `answer_chunks` in `data/test_cases.yaml`.
- The check that prints no recall figure was `python -m app.retrieval` when this ADR was written (today `scripts/search.py`); the printed numbers are the RRF score and the BM25 and dense ranks.
- Issues and PRs: the search task is #12 (its plan comment holds Hiep's answer), PR #28 merged the decision, and the evaluation task is #14.
- Mission 1 IDs: V1 (it held the context recall row) and RV13 ("chỉ theo dõi", track only).
