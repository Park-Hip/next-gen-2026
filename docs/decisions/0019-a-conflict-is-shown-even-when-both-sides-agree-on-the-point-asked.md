# 0019. A conflict is shown even when both sides agree on the point asked

- Status: Accepted
- Date: 2026-10-22
- Origin: Hiep
- Supersedes: None; it turns the known failure "the conflict card replaces an answer both documents agree on" into a decision, and confirms Mission 1 R7 and the option ADR 0014 rejected
- Issue: #114
- Research: None

## In short

- **The problem:** The Group leave policy and the PayCo leave policy both apply to Hà and disagree on the days of leave and the days of notice.
  On one point they say the same thing: the request goes to the direct manager ("quản lý trực tiếp").
  When Hà asks who approves her leave request, she gets the conflict card instead of a plain answer.
  Until now the test cases counted this as a known failure.
- **The decision:** Two documents that conflict are always reported as a conflict, even when both say the same thing on the point asked.
  This is the intended behaviour, not a defect.
- **What the employee sees:** Hà gets the conflict card, which quotes the clause of each policy word for word, so she still reads "quản lý trực tiếp" on both sides, and is asked to check with HR PayCo.
- **What we give up:** An employee whose two policies agree on the point asked gets the conflict card and a referral to HR where a plain answer was possible.

All data is simulated ("giả lập").

## Context

The rules pair two documents as a conflict when both apply to the asker, cover the same topic and have no declared relation.
A pair is between whole documents, so any reply that cites one of them gives the conflict card, whatever the question.
Deciding that two clauses say the same thing means reading meaning, which the design leaves to people.
Test case 17 was kept as a known failure: Hà asks "Đơn nghỉ phép gửi cho ai duyệt?", the ideal result was taken to be an answer card, and every run gave the conflict card.

## Options considered

1. **Always show the conflict card for a conflicting pair** - the behaviour the product already has, now the expected result of test case 17 (chosen).
2. **Let the AI say that both sides agree, and then show the answer card** - rejected in ADR 0014, because a wrong "they agree" hides a real conflict and gives a wrong answer with confidence.
3. **Keep it as a known failure** - the behaviour stays, but the test cases keep counting it as a failure.

## Decision

A cited document in a conflict pair gives the conflict card, whatever the question, as Mission 1 R7 says.
Test case 17 now expects the conflict card between the two leave policies, and is counted in the gates like any other case.

## Reasons

Hiep, 22/10/2026: "hai văn bản có mâu thuẫn thì nên được báo cáo là mâu thuẫn, cho dù cả hai văn bản đều đồng ý về một câu trả lời".

## Consequences

- The conflict card is never removed on a reading of meaning, by a rule or by the AI.
- Test case 17 guards the behaviour: a change that gives Hà an answer card on this question now fails the evaluation.
- Every question a PayCo employee asks about leave gets the conflict card until an owner declares how the two policies relate.
- The README lists this under the limits that are decisions, not under the open defects.

## Would change if

- Owners can settle a conflict clause by clause, so that a pair covers only the clauses that really disagree.

## Evidence

- All 9 committed full runs, 4 of the Mission 2 version and 5 of the Mission 3 version, give the conflict card on test case 17, with the clause of each side quoted and "quản lý trực tiếp" visible on both.
- The AI cited only the PayCo clause in the 4 Mission 2 runs and both clauses in the 5 Mission 3 runs; the card quoted both sides every time, so the Mission 2 runs fail only on "does not cite", as test cases 7 and 12 do, which the asker does not see (ADR 0005).
- The automated test of the rules on test case 17 now passes as a normal test instead of an expected failure.

## Technical detail

- Issue #114; closes the limitation issue [#52](https://github.com/Park-Hip/next-gen-2026/issues/52); gap G3.2 of the archived [gap analysis](https://github.com/Park-Hip/next-gen-2026/blob/384f68a/docs/mission3/gaps.md); promise R7; ADR 0014 option 3; ADR 0005 for which clause each side quotes.
- Row 17 of `data/test_cases.yaml`: `kind: hard`, `card: conflict`, `conflict_pair: [LEAVE-GROUP-v1, LEAVE-PAYCO-v1]`, `must_show: [quản lý trực tiếp, 3 ngày làm việc, 5 ngày làm việc]`, `must_cite` equal to the pair as for rows 7 and 12.
- `pick_card` in `services/citations.py` is unchanged; `tests/services/test_scope.py::test_case_row[row-17]` lost its strict xfail.
- Runs `results/20261021-2253.jsonl`, `-2258`, `-2301`, `results/20261022-1432.jsonl` and `results/20261022-1602.jsonl` cite `LEAVE-GROUP-v1#2` and `LEAVE-PAYCO-v1#2`; `results/20261014-2239.jsonl`, `20261021-2311`, `-2315` and `-2319` cite only `LEAVE-PAYCO-v1#2`.
