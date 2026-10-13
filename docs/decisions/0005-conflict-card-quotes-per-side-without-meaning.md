# 0005. The conflict card quotes one clause per side, chosen without reading meaning

- Status: Proposed
- Date: 2026-10-13
- Origin: AI, not reviewed
- Supersedes: None
- Issue: #11
- Research: None

## Context

`pick_card` returns the cited chunks and the conflict pairs, but the submitted conflict card quotes one clause from each document in the pair (Tập đoàn Điều 1 and PayCo Điều 1).
When only one side is cited, the rules must still choose a clause for the other side, deterministically and without reading meaning.
Mission 1 did not spell out how to choose it, so this is a step 7 detail that needs a decision.

## Options considered

1. **Per document: cite, then retrieve, then everything** - quote its cited chunks; if it cites none, its highest-ranked retrieved chunk; if none was retrieved, all its chunks (chosen).
2. **Only the cited side** - quote only the chunks the answerer cited and leave the uncited side out.
3. **The LLM picks a clause** for the uncited side.

The strongest alternative is option 2, as the smallest change from what `pick_card` already returns.

## Decision

For each conflict pair, the conflict card quotes one clause per document by this rule: its cited chunks if any, otherwise its highest-ranked retrieved chunk, otherwise all its chunks.
The choice never reads the text of any document and never calls the LLM.

## Reasons

[chờ Hiệp] - Hiep writes his own reasons.

## Consequences

- `app/rules.py` gains `conflict_quotes`, and `app/cards.py` renders the chosen clauses.
- The rule is deterministic and needs no LLM text, in line with promise A4.
- It produces the submitted card for row 7 and row 12.

## Would change if

A case appears with three or more documents in one conflict, or a conflict document with no chunks at all.

## Evidence

`tests/test_rules.py` covers the cited / retrieved / all-chunks choices; `tests/test_cards.py` checks the row 7 wording word for word.