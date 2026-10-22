# 0010. Access is the last filter: a document the asker may not read still replaces its series

- Status: Accepted
- Date: 2026-10-14
- Origin: AI, accepted
- Supersedes: The order of step 2 (access) and step 3 ("dùng thay") of Mission 1 (M3b, M12) for a restricted overriding document; R3 and R4 of `docs/mission2/mission1_promises.md`
- Issue: #48
- Research: None

## In short

- **The problem:** Suppose the newest GameCo leave policy is restricted to GameCo HR.
  Minh, a GameCo employee asking on 01/01/2027, may not read it, so under the submitted order it replaced nothing for him, and the older Group leave policy came back into his documents.
  He then got a false conflict card between the Group policy and the GameCo procedure.
- **The decision:** Access only decides who may read a document, never which rule applies.
  The rules first check validity, then applicability, then which document replaces which, and only then access.
  A restricted document that replaces a policy still removes it, and Minh is left with neither.
- **What the employee sees:** The refusal card, which sends the asker to HR, instead of a false conflict or an old policy.
- **What we give up:** An owner who meant "only for this role" now makes everyone else in the unit get the refusal for that question; this fails towards "ask HR".
  Rules that apply only to some roles need their own field, which is a deferred idea.

## Context

The submitted flow filters access and applicability in step 2, then removes a series (a document and its later versions) that a kept document replaces in step 3.
So a document the asker may not read overrode nothing, and the series it replaces came back.
On the simulated data, with version 3 of the GameCo leave policy restricted to GameCo HR, Minh on 01/01/2027 got the Group leave policy back in his scope, and a false conflict card between it and the GameCo leave procedure.
Access changed precedence, against the product rule "keep access, validity and applicability separate".
No Mission 1 decision covers it.
Issue 4's two constraints are about validity and applicability, and P1's "refusal, never the stale version" is written for versions of one series.
The "applies to" field of a document knows only units, so the metadata cannot tell "not for you" from "for you but hidden"; one meaning of access has to be fixed.

## Options considered

1. **access means only who may read** - a document that is in force and applies to the asker's unit replaces its series whether or not the asker may read it; access is applied last (chosen).
2. **access may also mean "applies only to these people"** - a restricted overrider overrides nothing for those who cannot read it (the behaviour until now).
3. **A separate field for applicability by role** - both meanings become expressible; deferred.

The strongest alternative is option 2, as the literal order of the submitted flow.

## Decision

access means only who may read a document and never decides which rule applies.
The order is validity, applicability, precedence, then access.
A restricted document that replaces a series leaves the asker with neither document, so the asker gets the refusal card.

## Reasons

Access decides who may read a document, not which rule applies.
Hiding the current version must not bring back an old one; sending the asker to HR is safer.

Drafted by AI; approved by Hiep on 15/10/2026 (issue #48).

## Consequences

- The scope code applies the replacements before the access check.
  The leak guarantee is unchanged, because a restricted document is still dropped before it is split into clauses and searched.
- On the unmodified data and the 7 traps (deliberate difficult cases built into the simulated data) nothing changes, and the code still gives the same results as the Mission 1 script.
  Only a restricted document that declares a replacement behaves differently, which is the one case where the port departs from the Mission 1 script.
- An owner who meant "only for this role" now makes everyone else in the unit get the refusal for that question; this fails towards "ask HR", the same direction as #24.
- Applicability by role needs its own field; it is a deferred idea.
- Not covered here: a restricted document inside an undeclared conflict pair still makes the pair disappear (the conflict-marking step).

## Would change if

- An owner needs a role-specific override on real documents: add the applicability field instead of reading access that way.
- A restricted overrider turns out common in practice: warn the owner at publish time.

## Evidence

Four tests in `tests/services/test_scope.py` show it; the first, third and fourth fail on the commit before the change.
The plan and the checks behind it are in the comment on #48; evidence log line of 14/10/2026.

## Technical detail

- Code: `scope()` and `_winners()` in `src/appota_kb/services/scope.py` apply `overrides` before `allowed`.
  `docs/mission1/redraft/checks/adopted_rules.py` is the Mission 1 script whose results `tests/test_parity.py` compares against.
- Data: `LEAVE-GAMECO-v3` set to `access: roles:hr_gameco`; the false conflict was between `LEAVE-GROUP-v1` and `LEAVE-PROC-GAMECO-v1`.
- Tests: `test_restricted_override_still_replaces_its_series`, `test_restricted_override_leaves_units_it_does_not_cover_alone`, `test_hidden_v3_does_not_bring_the_group_policy_back`, `test_hiding_one_document_removes_only_that_document`.
  The first, third and fourth fail on `53e393d`.
- Fields: `applies_to` knows only units; `access` is `all_staff`, `roles:...` or `unit:...`; the deferred separate field would carry applicability by role.
- Mission 1 and plan IDs: M3b (access filter), M12 (step 3, "dùng thay"), M0 (the three dimensions: unit, access, version), R3 and R4 (the promises of step 2 and step 3), and P7 and P1 as cited in the original text for the deferred field and for "refusal, never the stale version".
- #24 is the earlier change that also fails towards "ask HR".
