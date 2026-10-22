# 0013. Owners change a document only by publishing a full new version

- Status: Accepted
- Date: 2026-10-21
- Origin: Hiep
- Supersedes: None; it confirms Mission 1 decision M1a ("an overriding policy must be complete on its topic") and extends it to an owner's own policy
- Issue: None; gaps G1.3 and G3.1 in `docs/mission3/gaps.md`, limitations #24 and #50
- Research: None

## In short

- **The problem:** Sometimes an owner wants to change only one clause of a policy, and the product cannot handle that.
  If an owner publishes a separate note that changes some clauses of a policy, the old value and the new value both stay visible with no warning.
  If a company replaces one clause of a Group policy, the whole Group policy is dropped, and its employees lose the Group clauses the company meant to keep.
- **The decision:** An owner never changes a single clause on its own.
  To change any clause, the owner publishes a new version of the whole document, a copy of the version in force with that clause changed.
  This holds across owners: a company that changes one clause of a Group policy publishes a complete policy of its own that declares it replaces the Group policy.
- **What the employee sees:** Every answer still comes from whole documents, so one source line names the full rule the employee must follow.
- **What we give up:** The rule binds owners, and the product cannot enforce it.
  A company's copy of the Group clauses does not follow later Group changes, and an owner who breaks the rule still produces the two failures above.

All data is simulated ("giả lập").

## Context

Mission 3 asks the product to tell versions and effective dates apart.
The gap analysis found two cases where an owner changes only one clause, and the Mission 2 version cannot express either:

- **A separate amendment to some clauses of a version.**
  Declared as an addition ("bổ sung"), the old and the new value both stay in the asker's scope with no conflict.
  Declared as a new version, it drops the clauses it does not amend. [G1.3, #50 example 2]
- **A company that replaces one clause of a Group policy.**
  A declared replacement ("dùng thay") drops the whole Group policy, and the asker loses the Group clauses the company kept.
  In test case 15, on edited data, Minh asks how many days in advance he must ask for leave, and is refused instead of getting the Group's rule. [G3.1, #24]

Mission 1 chose relations between whole documents, with the rule that an overriding policy must be complete on its topic, and named one-clause changes as a likely Mission 3 change.

## Options considered

1. **A change to any clause is a full new document** - the owner copies the current version, changes the clause and publishes it as a new version of the same policy; a company that changes one clause of a Group policy publishes its own complete policy, copying the Group clauses it keeps, and declares that it replaces the Group policy (chosen).
2. **Relations per clause** - an amendment document names the clauses it replaces, and the rules merge the clauses of several documents into one answer; parked as a deferred idea in `docs/scope.md`.
3. **A separate amendment declared as an addition ("bổ sung")** - what an owner can do today; it leaves both values in the scope with no conflict, so it is not a real option, only the failure that option 1 forbids.

The strongest alternative is option 2.

## Decision

An owner never changes a single clause on its own.
To change any clause, the owner publishes a new version of the whole document, a copy of the version in force with the clause changed.
This holds across owners: a company that changes one clause of a Group policy publishes a complete policy of its own that declares it replaces the Group policy.

## Reasons

We make a new version of a document even when we change only one clause, because the new version keeps the other, unchanged clauses in the document, so none of them is lost.

Hiep, 21/10/2026.

## Consequences

- No code changes: the rules already pick the new version on its start date, and a declared replacement already replaces the whole Group policy for the company's units.
- Every answer still comes from whole documents, so one source line names the full rule the asker must follow.
- A company's copy of the Group clauses does not follow later Group changes: when the Group changes a clause the company kept, the company's staff keep the old text until the company publishes a new version.
- The rule binds owners, and the Mission 2 version cannot enforce it from the metadata.
  The legitimate procedure document for GameCo leave has the same owner, topic and unit as the leave policy and declares itself an addition to it, exactly as a forbidden amendment would.
  An owner who breaks the rule still produces the two failures described above; they stay limitations.
- G1.3 and G3.1 are no longer missing features but owner errors, and the gap analysis marks them so.

## Would change if

- Owners need to amend one clause of a long document without republishing it, for example a long legal text.
- Company copies of Group clauses drift from the Group policy often enough that staff get outdated text.

## Evidence

No new code or test.
Existing tests and test cases 1 and 2 show that a new version replaces the old one on its start date, and case 1 shows that a complete company policy that declares it replaces the Group policy does so.
Evidence log line of 21/10/2026.

## Technical detail

- Gaps G1.3 and G3.1 in `docs/mission3/gaps.md`; limitations [#24](https://github.com/Park-Hip/next-gen-2026/issues/24) (test case 15) and [#50](https://github.com/Park-Hip/next-gen-2026/issues/50) (example 2); Mission 1 decision M1a.
- "Deferred" row for relations per clause: `docs/scope.md`.
- `in_force` picks the new version on its start date; `overrides` ("dùng thay") replaces the whole Group policy.
- The legitimate procedure document is `LEAVE-PROC-GAMECO-v1`, which declares `complements: [LEAVE-GAMECO]` ("bổ sung").
- Evidence: `tests/services/test_scope.py`; test cases 1 and 2 (a new version on its start date) and test case 1 (a company policy replaces the Group policy).
