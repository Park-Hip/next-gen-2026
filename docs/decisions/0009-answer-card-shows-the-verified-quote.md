# 0009. The answer card shows the quote that step 7 verified, not the model's sentence

- Status: Accepted
- Date: 2026-10-14
- Origin: AI, accepted
- Supersedes: The `text` field of ADR 0003's output contract, and the answer line wording of Mission 1 C2 (Phần 2)
- Issue: #47
- Research: None

## Context

ADR 0003 made every point `{text, quote, chunks}` and step 7 checks `quote` against the cited chunks.
The answer card showed `text`, which nothing checks (`citations.py` only needs a non-empty quote that is a substring of a cited chunk).
Offline, with no model, a point citing `LEAVE-GAMECO-v2#2` with quote "ngày" and an invented sentence gave an answer card with that sentence and a real source line.
In the real run `results/20261014-1317.jsonl`, row 5, the quote had "chính thức" and the card sentence did not.
The persona data has no employment status, so rules cannot check a condition written inside a clause; the employee has to read it.
The prompt also told the model "Every chunk has already been checked to apply to this employee", which is true only for the unit.

## Options considered

1. **Show the verified quote word for word** - the card line is the quote in quotation marks, as the conflict card already does.
2. **Show the quote and the model's `text`** - the unchecked sentence stays on the card.
3. **Keep `text` and refuse when a number in it is not in its quote** - does not catch a dropped condition such as "chính thức".
4. **Set a minimum quote length** - needs a config key and a rule; with option 1 a short quote shows as a short quote and invents nothing.

## Decision

The answer card shows each verified quote, folded as step 7 compared it, in quotation marks, once per distinct quote, then the source lines.
`text` is removed from `Point`, the JSON schema, the prompt, the run log and the review sheet.
The prompt no longer says the chunks were checked to apply to the employee; it says they were selected by unit only, and asks for the whole sentence that states the fact.
There is no minimum quote length.

## Reasons

The card shows only what step 7 checked.
If the model's sentence sat next to the quote, it could still add a fact or drop a condition such as "chính thức".

Drafted by AI; approved by Hiep on 15/10/2026 (issue #47).

## Consequences

- Every fact on an answer card is text that step 7 checked against its cited chunk, so A4 holds for all three cards.
- The answer line reads "Nhân sự GameCo được nghỉ phép năm 14 ngày mỗi năm." instead of the submitted "Phép năm của bạn là 14 ngày mỗi năm."; the Mission 1 document stays frozen.
- A condition written in the clause, such as "chính thức", reaches the employee on the card; the rules still do not decide it.
- A true quote that does not answer the question still passes step 7, as ADR 0003 already noted; only the manual reading catches it.
- `key_facts` in the evaluation now match against the quotes, which are the words the employee reads.
- The output has one fewer field per point, so a call costs fewer tokens.

## Would change if

- Hiep or a judge finds the quoted line too stiff for employees and wants a paraphrase: it must then be checked by a rule, not shown as is.
- A run shows quotes so short that cards mislead: add a minimum with a config key and a new ADR.

## Evidence

- `tests/services/test_ask.py::test_ask_never_shows_text_the_model_added` and the card tests in `tests/services/test_card_text.py`.
- The run `results/20261014-2102.jsonl` (15 rows): row 5 shows "chính thức" on the card, and every row passes its checks except limitation row 15.
- Evidence log line of 14/10/2026.
