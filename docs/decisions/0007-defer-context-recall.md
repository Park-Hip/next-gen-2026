# 0007. Context recall is deferred until we have real documents

- Status: Accepted
- Date: 2026-10-13
- Origin: Hiep
- Supersedes: The "context recall" row of Mission 1 V1 and RV13 ("chỉ theo dõi")
- Issue: #12
- Research: None

## Context

The submitted metrics table tracked context recall as a diagnostic with no threshold (Mission 1 V1 and RV13).
Measuring it needs a label for each test question saying which chunks hold the answer.
The implementation plan for #12 recommended adding those labels (`answer_chunks`) to `data/test_cases.yaml` and printing context recall for every row.
Hiep rejected that recommendation on 13/10/2026.
All current documents are simulated ("giả lập"): 10 short files and 25 chunks.

## Options considered

1. **Add `answer_chunks` and print context recall per row** - the plan's recommendation.
2. **Defer context recall until real documents exist** (chosen).

## Decision

Mission 2 does not measure context recall.
No `answer_chunks` are added to the test cases, and neither `python -m app.retrieval` nor the evaluation report prints a recall figure.
The manual check prints the ranked chunks for every row, and Hiep reads them.
The idea is parked under "Deferred ideas" in `docs/mission1/playbook.md`.

## Reasons

Hiep, 13/10/2026: "it is too soon to measure recall in this mission and we should defer this. Revisit when we have real document."

## Consequences

Drafted by Claude from Hiep's decision; approved by Hiep when he merged PR #28 on 13/10/2026.

- The issue #12 line "context recall printed for every row" became "the top 5 printed for every row", and #14 no longer tracks context recall.
- A reader of the Mission 1 table will find "context recall" missing from the Mission 2 report; mandatory question 2 can cite this ADR as a change since Mission 1.
- Retrieval quality is still visible: the run log and the manual check show each returned chunk with its RRF score and its BM25 and dense ranks.
- A retrieval miss shows up downstream, as a wrong refusal or a wrong citation in the #14 evaluation, not as a separate number.

## Would change if

- Real Appota documents arrive (Hiep, 13/10/2026: "Revisit when we have real document").

## Evidence

Hiep's answer in the plan comment on issue #12.
Evidence log lines of 13/10/2026 (Claude Opus 5.5, Pi).
