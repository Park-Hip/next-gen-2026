# 0015. A conflict with a document the asker may not read gives the refusal card

- Status: Proposed
- Date: 2026-10-21
- Origin: Hiep + AI
- Supersedes: None; it extends ADR 0010 from "dùng thay" to conflict pairs, the case ADR 0010's Consequences name as not covered
- Issue: #87
- Research: None

## Context

ADR 0010 made access the last filter, so a document the asker may not read still replaces its series.
Conflict pairs are still formed after the access filter, so a restricted document inside an undeclared pair makes the pair disappear (gap G3.6).
Probe P8, on edited simulated data ("giả lập"): with `LEAVE-PAYCO-v1` readable only by `hr_payco`, Hà's scope keeps only `LEAVE-GROUP-v1`, and a reply citing its Điều 1 gives an answer card "12 ngày", although the PayCo policy (13 days) applies to her.
Access then decides which rule the asker is told, against the product rule "keep access, validity and applicability separate".
No document in the data is restricted and inside a pair, so no evaluation row shows it.

## Options considered

1. **Pairs before access, and the refusal card when the other side is hidden** - the hidden document is never named or quoted, and the refusal card looks the same as "not found" (chosen).
2. **A conflict card with one side and a note that another rule applies** - tells the asker more, but reveals that a document they may not read exists and covers this topic.
3. **Keep pairs after access** - the asker gets the readable side as the answer (today).

The strongest alternative is option 3, which answers more questions.

## Decision

Conflict pairs are formed among the documents in force, applying to the asker and not replaced, before the access filter.
If the model cites a document whose pair partner the asker may not read, the asker gets the refusal card.
The hidden document is still dropped before chunking and retrieval, so its text never reaches the model or the card.

## Reasons

[chờ Hiệp]

## Consequences

- Access no longer changes which rule an asker is told, for conflict pairs as for "dùng thay".
- The leak guarantee is unchanged: the hidden document is not in the asker's chunks.
- Pairs are per document (G3.2), so every question that cites the readable side is refused, even one the hidden document does not touch; this is over-caution, not a leak.
- `test_hiding_one_document_removes_only_that_document` changes its expected result; P8 becomes a pytest.
- No current evaluation row changes.

## Would change if

- Restricted documents inside conflict pairs turn out common, so askers are refused often: warn the owner at publish time instead.
- A field for applicability by role is added (ADR 0010), so a restricted document can say whom it is for.

## Evidence

To come with #87: the P8 pytest, and a reader with `hr_payco` in PayCo who gets the conflict card.
Evidence log line of 21/10/2026.
