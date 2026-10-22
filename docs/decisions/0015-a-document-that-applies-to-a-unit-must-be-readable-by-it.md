# 0015. A document that applies to a unit must be readable by everyone in that unit

- Status: Accepted
- Date: 2026-10-21
- Origin: Hiep + AI
- Supersedes: None; it records, as an owner rule, the case that ADR 0010 (access is applied last) leaves open
- Issue: #87
- Research: None

## In short

- **The problem:** The product forms a conflict pair only from documents the asker may read.
  If one of the two documents is restricted, the pair disappears.
  Suppose the PayCo leave policy (13 days) is readable only by PayCo HR, although it applies to all PayCo staff.
  Hà, who works at PayCo, then sees only the Group policy, and she gets a confident answer "12 ngày" instead of being told that another rule applies to her.
- **The decision:** The system does nothing special for this case.
  The owner rule is: a document that applies to a unit must be readable by everyone in that unit, and a document meant only for a role must not share a topic with a policy that applies to everyone.
- **What the employee sees:** In this case, a confident answer that may be wrong.
  In every other case, nothing changes.
- **What we give up:** The product cannot enforce the rule from the document labels, so when an owner gets the access label wrong, the employee gets the wrong answer.
  This is accepted on purpose, and it stays a known limitation.

All data is simulated ("giả lập").

## Context

ADR 0010 made access the last filter, so a document the asker may not read still replaces the policy it overrides.
Conflict pairs are still formed after the access filter, so a restricted document inside an undeclared pair makes the pair disappear.
A probe on edited data shows it: with the PayCo leave policy readable only by PayCo HR, Hà's scope keeps only the Group policy, and a reply citing its Điều 1 gives an answer card "12 ngày", although the PayCo policy (13 days) applies to her.
The first draft of this ADR fixed it by forming pairs before the access filter and refusing when a cited document had a hidden partner.
Hiep rejected that fix on 21/10/2026: the case is an error in the owner's metadata, so the system does not need to fix it.
No document in the data is restricted and inside a pair, so no evaluation case shows the case.

## Options considered

1. **An owner rule, no code** - a document that applies to a unit must be readable by everyone in that unit; a document meant only for a role must not share a topic with a policy that applies to everyone (chosen).
2. **Pairs before access, and the refusal card when the other side is hidden** - the hidden document is never named, but the Mission 2 version has no field for applicability by role (ADR 0010), so an owner can only use the access label to scope a document to a role.
   Such a valid document would still form a hidden pair, and every leave question that cites the Group policy would be refused.
3. **A conflict card with one side and a note that another rule applies** - tells the asker more, but reveals that a document they may not read exists and covers this topic.

The strongest alternative is option 2, which sends the asker to HR in the case where the metadata really is wrong.

## Decision

The rules do nothing for this case: the pair is formed after the access filter, as ADR 0010 left it, and a wrong access label is applied as written, like the other access-label errors.
The owner rule binds the owner:

- A document that applies to a unit must be readable by everyone in that unit.
- A document meant only for a role must not share a topic with a policy that applies to everyone.

## Reasons

"Đây là lỗi của metadata nên hệ thống không cần sửa cho trường hợp này."

Hiep, 21/10/2026.

## Consequences

- No code.
  The fix of the first draft (remembering hidden partners, reordering the rules, a refusal for a hidden conflict) is not built.
- When the metadata really is wrong (the PayCo policy applies to Hà but only PayCo HR may read it), Hà gets a confident answer card "12 ngày" instead of being sent to HR PayCo.
  This is an unsafe answer, accepted on purpose; it stays under the limitation for wrong access labels.
- A document meant only for a role (for example a guide for HR staff readable only by PayCo HR) does not produce a refusal for the employees who cannot read it.
- The Mission 2 version cannot enforce the rule from the metadata, which has no way to say that a document is meant only for a role.
- The leak guarantee is unchanged: a restricted document is never in the asker's scope, so it never reaches search or the AI.
- Two tests pin this down: one records the accepted result, and the older one keeps its original expectation that the pair disappears when one document is hidden.

## Would change if

- Restricted documents inside conflict pairs turn out common, so askers get wrong answers: check when the owner publishes, warning that a document applies to a unit that cannot read it.
- A field for applicability by role is added (ADR 0010), so a restricted document can say whom it is for, and the pair can be formed before the access filter without refusing valid data.

## Evidence

The probe on edited data that shows the case, and the test that records its accepted result (names in Technical detail).
Evidence log line of 21/10/2026.

## Technical detail

- Issue #87; gaps G3.6 (access hides a conflict) and G2.3 (a wrong `access` value is applied as written); limitation [#50](https://github.com/Park-Hip/next-gen-2026/issues/50); probe P8 in `docs/mission3/gaps.md`.
- P8: `LEAVE-PAYCO-v1` with `access: roles:hr_payco`; Hà's scope keeps only `LEAVE-GROUP-v1`; a reply citing its Điều 1 gives an answer card "12 ngày".
  The example of a role-only document is `access: roles:hr_payco`.
- Not built from the first draft: `Scope.hidden_partners`, the reordering in `services/scope.py`, and the `hidden_conflict` refusal.
- `test_p8_a_hidden_partner_is_applied_as_written` in `tests/services/test_citations.py` records the accepted result.
  `test_hiding_one_document_removes_only_that_document` in `tests/services/test_scope.py` keeps its original expectation that the pair disappears.
