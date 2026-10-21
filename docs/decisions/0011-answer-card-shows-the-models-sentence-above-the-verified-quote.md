# 0011. The answer card shows the model's sentence above the verified quote

- Status: Accepted
- Date: 2026-10-20
- Origin: Hiep + AI
- Supersedes: ADR 0009 and the prompt rules of ADR 0003
- Issue: #75
- Research: None

## Context

ADR 0009 removed the model's sentence from the answer card because nothing checked it.
That fixed a real failure: in run `results/20261014-1317.jsonl`, row 5, the model's sentence dropped the condition "chính thức" from the quote.
The card then showed only the quote, folded as step 7 compared it.
A quote is faithful, but it does not always answer the question directly.
Mission 1 promise C2 and the MVP spec E1 ask for an answer in plain Vietnamese, and a quote alone can leave the employee to work out the answer.
Hiep decided on 20/10/2026 (issue #75, SD14) that the sentence comes back above the quote, and that it is not checked at run time.

Promise A4 still has to hold: AI never decides access, validity, applicability, precedence or the card.
The claim cannot change the scope, the citations that pass step 7 or the card kind.
Step 7 still refuses malformed output, no points, a citation outside what was retrieved, or a quote that is not in its chunk.
Only the deterministic rules pick the card.
What changes is narrower: the answer card now contains text the model wrote, above the text step 7 verified.
The risk is named in the issue:
- The sentence can decide which rule applies, for example "Quy chế PayCo áp dụng cho bạn".
  A declared conflict pair hides the sentence on the conflict card; a content conflict nobody declared does not.
  That is limitation #74.
- "One point per document's clause" can make the model cite a document in a conflict pair that does not answer the question, turning an answer into a conflict card.
- "Do not return an empty list only because clauses disagree" can weaken the strict-grounding rule and make a row that must refuse answer instead.
- Two values from an undeclared content conflict can sit on one answer card, and naming the document in each sentence is the only aid.

## Options considered

1. **Sentence, then the verified quote, then the source line, per point** - the model's sentence is shown, and the quote and source stay under it (chosen).
2. **Keep the quote only** - ADR 0009's card; A4 holds fully, but the card still does not answer directly.
3. **Show the sentence only after a rule checks its numbers or conditions** - catches a changed number, but not a dropped condition such as "chính thức", and adds rules that only approximate meaning.
4. **Check the sentence with a second model call** - adds a second model to trust, latency and cost, and the second model can be wrong in the same way.

The strongest alternative is option 2, because it keeps every word on the card checked.
Option 3 is the strongest safety alternative and the one the issue rules out for v1.

## Decision

Every point of an answer is `{claim, quote, chunks}`.
The answer card shows, for each point, the model's claim, then its quote folded as step 7 compared it and in quotation marks, then the source line for the chunks that point cites.
The conflict and refusal cards keep their fixed wording and show no model text.
Step 7 does not read `claim`.
A missing `claim` is malformed output, so the existing step-7 refusal applies.
The prompt asks for one plain Vietnamese sentence per point, naming the document.
It asks for one point per document's clause, both sides when clauses disagree, no choosing or merging, no empty list only because clauses disagree, and only values the text states.
`answer_text` in a run record becomes the model's claims joined, so `key_facts` tests the sentence the employee reads.
The review sheet shows each claim beside its quote and cited chunks.
Hiep reads every claim against its quote and names the error of an unfaithful one.

## Reasons

[chờ Hiệp] Hiep's answers, in his own words, to:
- Why bring back a model sentence after ADR 0009 removed it?
- Why is it safe to show that sentence without a run-time check?
- Why not check it with rules or a second model call?
- What should stay on the card under the sentence, and why?

## Consequences

- The answer card answers the question in plain Vietnamese and still shows the verified quote and the source under it.
- A claim can add a fact, drop a condition or flip a meaning; no rule catches that at run time.
  The Faithfulness reading and the quote under it are the only controls.
- A4 narrows in one place: the rules decide the card kind, access, validity, applicability and precedence, but the answer card now contains model text.
  The conflict and refusal cards still contain no model text.
- A content conflict nobody declared can show two different values on one answer card (#74), and the sentence naming each document is the only aid.
- "One point per document's clause" can increase over-caution if it makes the model cite a document in a conflict pair that does not answer the question.
  The new row 20 measures that risk, and the full run checks the over-caution gate.
- `key_facts` now matches the claim, not the quote.
  A faithful quote with a wrong sentence fails the row even when step 7 accepts the quote.
- The run log, review sheet and `/cases` page all carry the claim, so the reading and the video can point to the exact sentence.
- An older run has flat card lines; `committed.py` gives them line kinds so `/cases` still renders that run until a new run replaces it.
- The output has one more field per point, and a model that omits it is refused as malformed.

## Would change if

- Hiep's Faithfulness reading finds a claim that misleads, or a pattern of changed numbers or dropped conditions: add a check, by rule or with a second model call, and write a new ADR.
- Limitation #74 shows a content conflict on an answer card often enough to mislead: revisit conflict detection or hide the claim when two documents give different values.
- The over-caution gate fails because "one point per document's clause" makes the model cite a document that does not answer: revisit that prompt rule.
- The model omits `claim` often enough that malformed refusals rise: change the contract or the prompt wording.

## Evidence

- `tests/services/test_card_text.py`, `tests/services/test_ask.py`, `tests/services/answering/test_output.py`, `tests/services/answering/test_prompt.py`, `tests/services/answering/test_answerer.py`, `tests/services/test_citations.py`, `tests/api/test_page.py`, `tests/evaluation/test_score.py`, `tests/evaluation/test_review.py`, `tests/evaluation/test_run.py`, `tests/evaluation/test_data_edit.py`, `tests/evaluation/test_committed.py`.
- The full evaluation run on `gemini-3.5-flash-lite`: `[chờ Hiệp]`.
- Hiep's review YAML and review sheet for that run: `[chờ Hiệp]`.
- Evidence log line of 21/10/2026.
