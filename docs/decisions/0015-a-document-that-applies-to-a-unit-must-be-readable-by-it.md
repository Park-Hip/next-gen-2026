# 0015. A document that applies to a unit must be readable by everyone in that unit

- Status: Accepted
- Date: 2026-10-21
- Origin: Hiep + AI
- Supersedes: None; it records, as an owner rule, the case ADR 0010 leaves open
- Issue: #87
- Research: None

## Context

ADR 0010 made access the last filter, so a document the asker may not read still replaces its series.
Conflict pairs are still formed after the access filter, so a restricted document inside an undeclared pair makes the pair disappear (gap G3.6).
Probe P8, on edited simulated data ("giả lập"): with `LEAVE-PAYCO-v1` readable only by `hr_payco`, Hà's scope keeps only `LEAVE-GROUP-v1`, and a reply citing its Điều 1 gives an answer card "12 ngày", although the PayCo policy (13 days) applies to her.
The first draft of this ADR fixed it by forming pairs before the access filter and refusing when a cited document had a hidden partner.
Hiep rejected that fix on 21/10/2026: the case is an error in the owner's metadata, so the system does not need to fix it.
No document in the data is restricted and inside a pair, so no evaluation row shows the case.

## Options considered

1. **An owner rule, no code** - a document that applies to a unit must be readable by everyone in that unit; a document meant only for a role must not share a topic with a policy that applies to everyone (chosen).
2. **Pairs before access, and the refusal card when the other side is hidden** - the hidden document is never named, but v1 has no field for applicability by role (ADR 0010), so an owner can only use `access` to scope a document to a role; such a valid document would still form a hidden pair, and every leave question that cites the Group policy would be refused.
3. **A conflict card with one side and a note that another rule applies** - tells the asker more, but reveals that a document they may not read exists and covers this topic.

The strongest alternative is option 2, which sends the asker to HR in the case where the metadata really is wrong.

## Decision

The rules do nothing for this case: the pair is formed after the access filter, as ADR 0010 left it, and a wrong `access` is applied as written, like G2.3 and [#50](https://github.com/Park-Hip/next-gen-2026/issues/50).
The owner rule binds the owner:

- A document that applies to a unit must be readable by everyone in that unit.
- A document meant only for a role must not share a topic with a policy that applies to everyone.

## Reasons

"Đây là lỗi của metadata nên hệ thống không cần sửa cho trường hợp này."

Hiep, 21/10/2026.

## Consequences

- No code.
  `Scope.hidden_partners`, the reordering in `services/scope.py` and the `hidden_conflict` refusal of the first draft are not built.
- When the metadata really is wrong (P8: `LEAVE-PAYCO-v1` applies to Hà but only `hr_payco` may read it), Hà gets a confident answer card "12 ngày" instead of being sent to HR PayCo.
  This is an unsafe answer, accepted on purpose; it stays under limitation #50.
- A document meant only for a role (for example a guide for HR staff, `access: roles:hr_payco`) does not produce a refusal for the employees who cannot read it.
- v1 cannot enforce the rule from the metadata, which has no way to say that a document is meant only for a role.
- The leak guarantee is unchanged: a restricted document is never in the asker's chunks.
- `test_p8_a_hidden_partner_is_applied_as_written` in `tests/services/test_citations.py` records the accepted result; `test_hiding_one_document_removes_only_that_document` keeps its original expectation that the pair disappears.

## Would change if

- Restricted documents inside conflict pairs turn out common, so askers get wrong answers: check when the owner publishes, warning that a document applies to a unit that cannot read it.
- A field for applicability by role is added (ADR 0010), so a restricted document can say whom it is for, and the pair can be formed before the access filter without refusing valid data.

## Evidence

Probe P8 in `docs/mission3/gaps.md`, and `test_p8_a_hidden_partner_is_applied_as_written`.
Evidence log line of 21/10/2026.
