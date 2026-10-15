# 0010. Access is the last filter: a document the asker may not read still replaces its series

- Status: Accepted
- Date: 2026-10-14
- Origin: AI, accepted
- Supersedes: The order of step 2 (access) and step 3 ("dùng thay") of Mission 1 (M3b, M12) for a restricted overriding document; R3 and R4 of `docs/mission2/mission1_promises.md`
- Issue: #48
- Research: None

## Context

The submitted flow filters access and applicability in step 2, then removes a series that a kept document replaces in step 3.
So a document the asker may not read overrode nothing, and the series it replaces came back.
On the simulated data, with `LEAVE-GAMECO-v3` set to `roles:hr_gameco`, Minh on 01/01/2027 got `LEAVE-GROUP-v1` back in his scope and a false conflict card between it and `LEAVE-PROC-GAMECO-v1`.
Access changed precedence, against the product rule "keep access, validity and applicability separate".
No Mission 1 decision covers it: Issue 4's two constraints are about validity and applicability, and P1's "refusal, never the stale version" is written for versions of one series.
`applies_to` knows only units, so the metadata cannot tell "not for you" from "for you but hidden"; one meaning of `access` has to be fixed.

## Options considered

1. **`access` means only who may read** - a document that is in force and applies to the asker's unit replaces its series whether or not the asker may read it; access is applied last (chosen).
2. **`access` may also mean "applies only to these people"** - a restricted overrider overrides nothing for those who cannot read it (the behaviour until now).
3. **A separate field for applicability by role** - both meanings become expressible; deferred (M0, P7).

The strongest alternative is option 2, as the literal order of the submitted flow.

## Decision

`access` means only who may read a document and never decides which rule applies.
The order is validity, applicability, precedence, then access.
A restricted document that replaces a series leaves the asker with neither document, so the asker gets the refusal card.

## Reasons

Access decides who may read a document, not which rule applies.
Hiding the current version must not bring back an old one; sending the asker to HR is safer.

Drafted by AI; approved by Hiep on 15/10/2026 (issue #48).

## Consequences

- `services/scope.py` applies `overrides` before `allowed`; the leak guarantee is unchanged, because a restricted document is still dropped before chunking and retrieval.
- On the unmodified data and the 7 traps nothing changes (parity with `adopted_rules.py` holds); only a restricted document that declares `overrides` behaves differently, which is the one case where the port departs from the Mission 1 script.
- An owner who meant "only for this role" now makes everyone else in the unit get the refusal for that question; this fails towards "ask HR", the same direction as #24.
- Applicability by role needs its own field; it is a deferred idea.
- Not covered here: a restricted document inside an undeclared conflict pair still makes the pair disappear (step 4).

## Would change if

- An owner needs a role-specific override on real documents: add the applicability field instead of reading `access` that way.
- A restricted overrider turns out common in practice: warn the owner at publish time.

## Evidence

`tests/services/test_scope.py`: `test_restricted_override_still_replaces_its_series`, `test_restricted_override_leaves_units_it_does_not_cover_alone`, `test_hidden_v3_does_not_bring_the_group_policy_back`, `test_hiding_one_document_removes_only_that_document`.
The first, third and fourth fail on `53e393d`.
The plan and the checks behind it are in the comment on #48; evidence log line of 14/10/2026.
