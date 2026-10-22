# 0005. The conflict card quotes one clause per side, chosen without reading meaning

- Status: Accepted
- Date: 2026-10-13
- Origin: Hiep + AI
- Supersedes: None
- Issue: #11
- Research: None

## In short

- **The problem:** Hà's two leave policies, the Group's and PayCo's, disagree, so Hà gets a conflict card that quotes both.
  But the AI may cite a clause from only one of the two policies, and the card still has to show a clause from the other side.
  Mission 1 did not say how to choose it.
- **The decision:** For each policy in the conflict, the card quotes the clauses the AI cited from it.
  If the AI cited none, the card quotes the policy's best-matching clause from the search.
  If the search found none either, the card quotes all of the policy's clauses.
  The choice never reads the text and never asks the AI.
- **What the employee sees:** A conflict card with a quoted clause from each side, whichever side the AI happened to cite.
- **What we give up:** The rule is untested for three or more documents in one conflict, and for a conflict document with no clauses at all.

## Context

Step 7, the fixed rules that pick the card, already returns the cited clauses and the conflict pairs.
But the submitted conflict card quotes one clause from each document in the pair (Tập đoàn Điều 1 and PayCo Điều 1).
When only one side is cited, the rules must still choose a clause for the other side, deterministically and without reading meaning.
Mission 1 did not spell out how to choose it, so this is a step 7 detail that needs a decision.

## Options considered

1. **Per document: cite, then retrieve, then everything** - quote its cited clauses; if it cites none, its highest-ranked retrieved clause; if none was retrieved, all its clauses (chosen).
2. **Only the cited side** - quote only the clauses the answerer cited and leave the uncited side out.
3. **The AI picks a clause** for the uncited side.

The strongest alternative is option 2, as the smallest change from what the step 7 function already returns.

## Decision

For each conflict pair, the conflict card quotes one clause per document by this rule: its cited clauses if any, otherwise its highest-ranked retrieved clause, otherwise all its clauses.
The choice never reads the text of any document and never calls the AI.

## Reasons

The rule is deterministic, which fits the pipeline description.

## Consequences

- Two functions carry the rule: one chooses the clauses to quote (`conflict_quotes`) and one writes them on the card; both lived under `app/` when this ADR was written.
- The rule is deterministic and needs no AI text.
- It produces the submitted card for row 7 and row 12.

## Would change if

A case appears with three or more documents in one conflict, or a conflict document with no clauses at all.

## Evidence

Tests cover the cited, retrieved and all-clauses choices, and check the row 7 wording word for word.

## Technical detail

- `pick_card` returns the cited chunks and the conflict pairs.
- `conflict_quotes` is in `services/citations.py` (now `src/appota_kb/services/citations.py`); `services/card_text.py` renders the chosen clauses.
- Tests: `tests/test_rules.py` covers the cited / retrieved / all-chunks choices and `tests/test_cards.py` checks the row 7 wording (both as named when this ADR was written; today `tests/services/test_citations.py::test_conflict_quotes` and `tests/services/test_card_text.py::test_conflict_card_wording`).
- A4 is the Mission 1 promise that the AI never decides access, validity, applicability, precedence or the card; rows 7 and 12 are test cases in `data/test_cases.yaml`.
