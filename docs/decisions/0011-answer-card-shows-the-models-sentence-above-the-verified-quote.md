# 0011. The answer card shows the model's sentence above the verified quote

- Status: Accepted
- Date: 2026-10-20
- Origin: Hiep + AI
- Supersedes: Showing only the verified quote, without the AI's sentence (ADR 0009), and the AI's prompt rules (ADR 0003)
- Issue: #75
- Research: None

## In short

- **The problem:** A quote from a policy is faithful, but it does not always answer the question directly, and the employee is left to work out the answer.
  ADR 0009 had removed the AI's own sentence because nothing checked it: in one run, the sentence for Lan's leave question dropped the condition "chính thức", which the quote contained.
- **The decision:** The answer card shows one plain Vietnamese sentence written by the AI, naming the document, above the exact quote and its source.
  The sentence is not checked while the product runs; Hiep reads it against its quote afterwards.
- **What the employee sees:** An answer in a sentence first, then the word-for-word text of the rule that backs it, then where it comes from.
  Conflict cards and refusal cards still contain no AI-written text.
- **What we give up:** The sentence can add a fact, drop a condition or flip a meaning, and no rule catches that.
  The answer card is now the one place where the AI's words appear next to checked words.

## Context

ADR 0009 removed the AI's sentence from the answer card because nothing checked it.
That fixed a real failure: in one run (test case 5), the AI's sentence dropped the condition "chính thức" that was in the quote.
The card then showed only the quote, with its spacing and Unicode form normalised the same way the quote check compares it.
(The quote check is the set of fixed rules that, before any answer is shown, test that every quote matches the document word for word.)
A quote is faithful, but it does not always answer the question directly.
Mission 1 promised an answer in plain Vietnamese, and a quote alone can leave the employee to work out the answer.
Hiep decided on 20/10/2026 that the sentence comes back above the quote, and that it is not checked at run time.

The promise that the AI never decides access, validity, applicability, precedence or the card still has to hold.
The sentence cannot change which documents the asker may read, which citations pass the quote check, or which kind of card is shown.
The quote check still refuses when the AI's output is unreadable, has no points, cites a passage that was not retrieved, or gives a quote that is not in the passage it cites.
Only the fixed rules pick the card.
What changes is narrower: the answer card now contains text the AI wrote, above the text the quote check verified.
The issue names these risks:

- The sentence can decide which rule applies, for example "Quy chế PayCo áp dụng cho bạn".
  When two documents are declared to conflict, the conflict card hides the sentence.
  When two documents disagree in their content and nobody declared it, the sentence is shown.
  That is a known limitation. [#74]
- "One point per document's clause" can make the AI cite a document that belongs to a conflict pair but does not answer the question, turning an answer into a conflict card.
- "Do not return an empty list only because clauses disagree" can weaken the strict-grounding rule, so that a case that must be refused gets an answer.
- Two values from an undeclared content conflict can sit on one answer card, and naming the document in each sentence is the only aid.

## Options considered

1. **Sentence, then the verified quote, then the source line, for each point** - the AI's sentence is shown, and the quote and the source stay under it (chosen).
2. **Keep the quote only** - the card of ADR 0009: the promise holds fully, but the card still does not answer directly.
3. **Show the sentence only after a rule checks its numbers or conditions** - catches a changed number, but not a dropped condition such as "chính thức", and adds rules that only approximate meaning.
4. **Check the sentence with a second AI call** - adds a second model to trust, more delay and cost, and the second model can be wrong in the same way.

The strongest alternative is option 2, because it keeps every word on the card checked.
Option 3 is the strongest safety alternative and the one the issue rules out for v1.

## Decision

Every point of an answer has three parts: the AI's sentence, the exact quote, and the passages it cites.
For each point, the answer card shows the sentence, then the quote in quotation marks (normalised as the quote check compared it), then the source line for the documents that point cites.
The conflict card and the refusal card keep their fixed wording and show no AI text.
The quote check does not read the sentence.
A reply with a point that has no sentence counts as unreadable output, so the existing refusal for unreadable output applies.

The prompt asks for one plain Vietnamese sentence per point, naming the document.
It also asks for:

- one point per document's clause, and both sides when clauses disagree;
- no choosing between documents and no merging them;
- no empty answer only because clauses disagree;
- only values the text states.

It also tells the AI to refuse a personal balance that no clause states, such as how many leave days are left, instead of treating a general yearly entitlement as that balance.

In the evaluation, the recorded answer text is the AI's sentences joined together, so the key-fact check tests the sentence the employee reads.
The review sheet shows each sentence beside its quote and the passages it cites.
Hiep reads every sentence against its quote and names the error of an unfaithful one.

## Reasons

[chờ Hiệp] Hiep's answers, in his own words, to:
- Why bring back a model sentence after ADR 0009 removed it?
- Why is it safe to show that sentence without a run-time check?
- Why not check it with rules or a second model call?
- What should stay on the card under the sentence, and why?

## Consequences

- The answer card answers the question in plain Vietnamese and still shows the verified quote and the source under it.
- A sentence can add a fact, drop a condition or flip a meaning, and no rule catches that while the product runs.
  Hiep's reading for faithfulness, and the quote under the sentence, are the only controls.
- The promise that the AI decides nothing narrows in one place: the rules still decide the kind of card, access, validity, applicability and precedence, but the answer card now contains AI text.
  The conflict card and the refusal card still contain none.
- A content conflict that nobody declared can show two different values on one answer card, and the sentence naming each document is the only aid. [#74]
- "One point per document's clause" can increase over-caution if it makes the AI cite a document in a conflict pair that does not answer the question.
  A new test case (20) measures that risk, and the full run checks the over-caution limit.
- The key-fact check now matches the sentence, not the quote.
  A faithful quote with a wrong sentence fails the test case even when the quote check accepts the quote.
- The run log, the review sheet and the cases page all carry the sentence, so the reading and the video can point to the exact words.
- An older run saved its card lines without a kind; the loader gives them one so the cases page still shows that run until a new run replaces it.
- The output has one more field per point, and an AI reply that omits it is refused as unreadable.

## Would change if

- Hiep's reading finds a sentence that misleads, or a pattern of changed numbers or dropped conditions: add a check, by rule or with a second AI call, and write a new ADR.
- The known limitation shows a content conflict on an answer card often enough to mislead: revisit conflict detection, or hide the sentence when two documents give different values. [#74]
- The over-caution limit fails because "one point per document's clause" makes the AI cite a document that does not answer: revisit that prompt rule.
- The AI omits the sentence often enough that refusals for unreadable output rise: change the output contract or the prompt wording.

## Evidence

- Offline tests cover the sentence on the card, the prompt, the output parser, the citation check, the page, the scoring, the review sheet, the run record and the data edits (files in Technical detail).
- Reference only: this update is not finished, so the full run below and Hiep's reading of it do not count as the evaluation of this decision.
  They show how the first version behaves and are kept for comparison; the evaluation of the finished update is a later run.
- That full run used `gemini-3.5-flash-lite`: 20 test cases, 0 rule failures, 0 leaks, 0 unsafe answers and 0 over-cautious answers in the 15 gated cases; cases 18 and 19 are the two unsafe-answer limitation cases, and case 11 refuses.
- Hiep's review of that run is not finished: the "faithful" and "lesson" fields are still `[chờ Hiệp]`.
- Evidence log line of 21/10/2026.

## Technical detail

- Promises and spec lines: A4 (the AI decides nothing), C2 (the answer line of the Mission 1 document), MVP spec E1 (an answer in plain Vietnamese); SD14 (`docs/system_design.md`); issue #75.
- The "quote check" is step 7, and "the AI" is step 6.
- Every point is `{claim, quote, chunks}`; `claim` is the sentence.
  The card line kinds are `claim`, `quote` and `source`.
  The quote is shown as `fold(point.quote)`.
- A missing `claim` makes `parse_points` return `None`, which step 7 refuses with `reason: "malformed"`.
- Step 7 refusal reasons: `malformed`, `no_points`, `outside_retrieved`, `quote_mismatch`.
- The prompt rules are in `services/answering/prompt.py`.
- `answer_text` in a run record is the claims joined; `key_facts` is matched against it.
- `evaluation/committed.py` (`card_with_line_kinds`) gives older flat card lines their kinds so `/cases` renders them.
- The known limitation is issue #74 (labelled `limitation`).
- Test case 5 is the case where the sentence dropped "chính thức" in run `results/20261014-1317.jsonl`.
- Test case 20 is the over-caution watch.
- Tests: `tests/services/test_card_text.py`, `tests/services/test_ask.py`, `tests/services/answering/test_output.py`, `tests/services/answering/test_prompt.py`, `tests/services/answering/test_answerer.py`, `tests/services/test_citations.py`, `tests/api/test_page.py`, `tests/evaluation/test_score.py`, `tests/evaluation/test_review.py`, `tests/evaluation/test_run.py`, `tests/evaluation/test_data_edit.py`, `tests/evaluation/test_committed.py`.
- Run: `results/20261021-1032.jsonl`; review files `results/20261021-1032.review.yaml` and `results/20261021-1032.review.md`.
