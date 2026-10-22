# 0018. One answer per question, above the verified quotes

- Status: Accepted
- Date: 2026-10-22
- Origin: Hiep + AI
- Supersedes: ADR 0011's point contract and answer card layout
- Issue: #112
- Research: None

## In short

- **The problem:** The answer card showed one sentence per clause.
  For "Tôi xin nghỉ phép ở đâu, ai duyệt?" (Minh, 07/10/2026) it showed three sentences, each repeating its own quote almost word for word, and one of them answered a part the question did not ask: the "trước ít nhất 3 ngày làm việc" deadline.
  No sentence stated the whole answer: "tạo đơn trên hệ thống HR nội bộ, trưởng nhóm duyệt".
- **The decision:** The AI writes one answer that covers every part of the question, and the card shows it once in bold above the quotes that support it.
  The quotes are the only text the rules check; Hiep reads the answer afterwards.
- **What the employee sees:** One bold answer first, then each word-for-word quote with its source line and, when a version ends, the "Sắp thay đổi" notice.
  Conflict and refusal cards keep their fixed wording and show no AI text.
- **What we give up:** The answer can add a fact, drop a condition or decide which rule applies, and no rule catches that while the product runs.
  The verified quotes under it and Hiep's reading are the only controls.

## Context

ADR 0011 put the AI's sentence back on the answer card, one sentence per point, above the quote that point cites.
That made the card answer directly, but it also made the AI write a separate sentence for every clause it cited.
For the leave-request question above, the card showed three sentences, and the questions "where do I request leave" and "who approves it" were split across them.
The sentence about the deadline also cited a clause the employee had not asked about, so the card answered a question that was not asked.
No sentence said the whole answer in one place.

The cause was the prompt and the card together.
The prompt asked for one point per clause, for a sentence that names the document, and for the clauses to be reported exactly as they appear.
The card then printed a sentence, a quote and a source line for each point.
The rules were not the cause: the check in step 7 never read the sentence, and it does not read the answer.
The promise that the AI never decides access, validity, applicability, precedence or the card still holds, and the risk ADR 0011 named does not go away: the answer can add a fact, drop a condition or decide which rule applies.
What changes is how much AI text the reader sees and whether that text answers the question as a whole.

## Options considered

1. **One answer above all the verified quotes** - the AI writes one answer that covers every part of the question, and the card shows it once above the quotes that support it (chosen).
2. **Keep one sentence per clause** - the layout of ADR 0011; every sentence rests on one quote, but the card repeats the quotes and can answer parts the question did not ask.
3. **One answer checked by rules or a second AI call** - would catch a changed number or a dropped condition only approximately, adds a second model to trust, latency and cost, and is out of scope for v1.
4. **Show no AI text** - the card of ADR 0009; every word is checked, but the employee has to work out the answer from the quotes.

Option 2 is the strongest alternative because it keeps a one-to-one link between each sentence and the quote a rule verified.
Option 4 is the strongest safety alternative, and the issue rules it out for v1 as ADR 0011 did.

## Decision

The AI returns one answer, a list of points that each hold a quote and the passages it cites, and the disagreement flag.
The answer is the only claim, and it answers every part of the question.
A typical answer is one sentence; it uses two or three short sentences only when the question has several parts.
The points hold only the quotes that support the answer, so a clause the question does not ask about is not cited.
The answer names no document, except when two documents give different answers that no metadata declares as a conflict: then it states both values and names each document, and never chooses between them.

The answer card shows who, the note, the answer in bold once, then each verified quote with its source line and notice line.
The conflict and refusal cards are unchanged and show no AI text.
The note becomes: "Đoạn in đậm là câu trả lời của hệ thống; đoạn trong ngoặc kép là nguyên văn quy định đã được đối chiếu."

Step 7 keeps every check on quotes and passages.
A missing answer, or an empty answer while points are not empty, is malformed output, so the existing refusal applies.
An empty answer with empty points stays the "nothing found" refusal.
The answer is not checked by a rule or by a second AI call.

The run record stores the answer once, and the review sheet shows it above its quotes.
Older runs that stored one sentence per point still render.
Hiep reads the answer against all the quotes under it and names the error of an unfaithful one.

## Reasons

[chờ Hiệp] Hiep's answers, in his own words, to:

- Why one answer for the whole question instead of one sentence per clause?
- Why may the answer name no document except when two documents give different values?
- Why is it still safe to show the answer without a run-time check?
- Why show the verified quotes under the answer at all?

## Consequences

- The card answers the question once instead of repeating each quote, and the leave-request question no longer shows the "3 ngày" deadline it did not ask about.
- The answer can rest on several quotes, so the Faithfulness reading compares it with all of them, not with one quote per sentence.
- A wrong answer can still mislead: it can add a fact, drop a condition or flip a meaning, and no rule catches that while the product runs.
  The verified quotes under it and Hiep's reading are the only controls.
- The key-fact check now matches the single answer, so a case passes only when that answer states every key fact.
- An AI that omits the answer, or returns an empty one with points, is refused as malformed.
- The run log, the review sheet and the test-case page carry the answer once, so the reading and the video can point to it.
- An older run keeps its per-point sentences and still renders; the review sheet joins them for those records.
- The prompt and the output schema change together, so an AI that still returns the old per-point sentence is refused as malformed.

## Would change if

- Hiep's Faithfulness reading finds an answer that its quotes do not support, or a pattern of combined facts going wrong: add a check, by rule or with a second AI call, and write a new ADR.
- The AI keeps citing clauses the question does not ask about, or the over-cautious gate fails: revisit the "only quotes that support the answer" rule.
- The AI omits the answer often enough that malformed refusals rise: change the contract or the prompt wording.
- Two undeclared values on one answer card mislead readers even when both documents are named: revisit conflict detection or hide the answer in that case (#74).

## Evidence

- The automated tests cover the output schema, the parsing, the prompt, the step 7 malformed refusal, the card, the run record, the review sheet and the older runs that stored one sentence per point.
  The test files are listed in Technical detail.
- The full run on the configured model on 22/10/2026 asked all 22 test cases: 0 rules failures, 0 leaks, 0 unsafe answers and 0 over-cautious answers in the 19 gated cases.
  The two known-failure cases failed as expected and the third limitation case answered; Hiep's Faithfulness reading of the 9 answer cards is pending.
- The manual check as Minh on 07/10/2026 for "Tôi xin nghỉ phép ở đâu, ai duyệt?" gave one answer that covers both where and who approves.
  The card cited the two clauses of the leave-request procedure and showed no "3 ngày" quote.
- The review sheet for that run and its answer slots are in the run folder; `faithful` and `lesson` are still `[chờ Hiệp]`.
- The evidence log line of 22/10/2026 records the tools, the decision and how the result was checked.

## Technical detail

- Issue #112, PR #113, commit `ba7c2d0`.
- Supersedes ADR 0011's `Point.claim` field, its one-sentence-per-point prompt rules and its answer card layout; ADR 0011 keeps the rest of its decision.
- Output schema `{answer, points: [{quote, chunks}], disagreement}` in `answer_schema`; `Point` loses `claim`; `Reply` gains `answer`.
- `parse_reply` in `services/answering/output.py`: a missing `answer`, or a blank one while `points` is non-empty, returns `("", None)`; an empty answer with empty points returns `("", ())`.
- Prompt rules in `services/answering/prompt.py`; `SYSTEM_INSTRUCTION` asks for one answer, quotes that support it, and document names only for an undeclared disagreement.
- `ANSWER_NOTE` and `answer_card` in `services/card_text.py`; `render` takes `answer`.
- `evaluation/run.py` stores top-level `answer` and keeps `card.answer_text` for `score.py` and `report.py`.
- `evaluation/review.py` has `answer_of`, which falls back to the joined per-point `claim` values of older runs.
- Tests: `tests/services/answering/test_output.py`, `test_prompt.py`, `test_answerer.py`, `tests/services/test_card_text.py`, `test_ask.py`, `test_citations.py`, `tests/api/test_page.py`, `tests/api/test_source_page.py`, `tests/evaluation/test_run.py`, `test_review.py`, `test_committed.py`.
- Run `results/20261022-1432.jsonl`; review files `results/20261022-1432.review.md` and `results/20261022-1432.review.yaml`; report `docs/mission2/test_report.md`.
- Promise C2 and MVP spec E1 in `docs/mission2/mission1_promises.md`; cache key and card kind unchanged in `services/ask.py`.
