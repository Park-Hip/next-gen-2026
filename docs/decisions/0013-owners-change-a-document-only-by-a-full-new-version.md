# 0013. Owners change a document only by publishing a full new version

- Status: Accepted
- Date: 2026-10-21
- Origin: Hiep
- Supersedes: None; it confirms Mission 1 M1a ("an overriding policy must be complete on its topic") and extends it to an owner's own policy
- Issue: None; gaps G1.3 and G3.1 in `docs/mission3/gaps.md`, limitations #24 and #50
- Research: None

## Context

Mission 3 asks the product to tell versions and effective dates apart.
The gap analysis found two cases where an owner changes only one clause, and v1 cannot express either:

- G1.3: a separate amendment to some clauses of a version.
  Declared "bổ sung", the old and the new value both stay in the asker's scope with no conflict ([#50](https://github.com/Park-Hip/next-gen-2026/issues/50) example 2); declared as a new version, it drops the clauses it does not amend.
- G3.1: a company that replaces one clause of a Group policy.
  "Dùng thay" drops the whole Group policy, and the asker loses the Group clauses the company kept (row 15, [#24](https://github.com/Park-Hip/next-gen-2026/issues/24)).

Mission 1 M1a chose relations on whole documents, with the rule that an overriding policy must be complete on its topic, and named one-clause changes as a likely Mission 3 change.
All data is simulated ("giả lập").

## Options considered

1. **A change to any clause is a full new document** - the owner copies the current version, changes the clause and publishes it as a new version of the same series; a company that changes one clause of a Group policy publishes its own complete policy, copying the Group clauses it keeps, and declares "dùng thay" (chosen).
2. **Relations per clause** - an amendment document names the clauses it replaces, and the rules merge the clauses of several documents into one answer; under "Deferred" in `docs/scope.md`.
3. **A separate amendment declared "bổ sung"** - what an owner can do today; it leaves both values in the scope with no conflict, so it is not an option, only the failure option 1 forbids.

The strongest alternative is option 2.

## Decision

An owner never changes a single clause on its own.
To change any clause, the owner publishes a new version of the whole document, a copy of the version in force with the clause changed; this holds across owners, so a company that changes one clause of a Group policy publishes a complete policy of its own that declares "dùng thay".

## Reasons

We make a new version of a document even when we change only one clause, because the new version keeps the other, unchanged clauses in the document, so none of them is lost.

Hiep, 21/10/2026.

## Consequences

- No code changes: `in_force` already picks the new version on its start date, and "dùng thay" already replaces the whole Group policy for the company's units.
- Every answer still comes from whole documents, so one source line names the full rule the asker must follow.
- A company's copy of the Group clauses does not follow later Group changes: when the Group changes a clause the company kept, the company's staff keep the old text until the company publishes a new version.
- The rule binds owners, and v1 cannot enforce it from the metadata: the legitimate procedure document `LEAVE-PROC-GAMECO-v1` has the same owner, topic and unit as the leave policy and declares "bổ sung" on it, exactly as a forbidden amendment would.
  An owner who breaks the rule still gives the failures of #50 example 2 and row 15; those stay limitations.
- G1.3 and G3.1 are no longer missing features but owner errors, and the gap analysis marks them so.

## Would change if

- Owners need to amend one clause of a long document without republishing it, for example a long legal text.
- Company copies of Group clauses drift from the Group policy often enough that staff get outdated text.

## Evidence

No new code or test.
`tests/services/test_scope.py` and rows 1 and 2 show that a new version replaces the old one on its start date, and row 1 shows that a complete company policy with "dùng thay" replaces the Group policy.
Evidence log line of 21/10/2026.
