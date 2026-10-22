# 0018. One answer per question, above the verified quotes

- Status: Accepted
- Date: 2026-10-22
- Origin: Hiep + AI
- Supersedes: ADR 0011's point contract and answer card layout
- Issue: #112
- Research: None

## Context

ADR 0011 put the model's sentence back on the answer card, one sentence per point, above the quote that point cites.
That made the card answer directly, but it also made the model write a separate sentence for every clause it cited.
For "Tôi xin nghỉ phép ở đâu, ai duyệt?" (row 3, Minh, 07/10/2026) the card showed three claims, each repeating its own quote almost word for word.
One of them, "trước ít nhất 3 ngày làm việc", answered a part the question did not ask.
No claim stated the whole answer: "tạo đơn trên hệ thống HR nội bộ, trưởng nhóm duyệt".

The cause was the prompt and the card together: the prompt asked for one point per clause, for a claim that names the document, and for the clauses to be reported exactly as they appear, and `card_text.answer_card` then printed a claim, a quote and a source line per point.
The rules were not the cause: step 7 never read `claim`, and it still does not read the answer.
Promise A4 still has to hold, and the risk ADR 0011 named does not go away: the answer can add a fact, drop a condition or decide which rule applies, and no rule checks it at run time.
What changes is how much model text the reader sees and whether it answers the question as a whole.

## Options considered

1. **One answer above all the verified quotes** - the model writes one answer that covers every part of the question, and the card shows it once above the quotes that support it (chosen).
2. **Keep one claim per clause** - ADR 0011's layout; every claim rests on one quote, but the card repeats the quotes and can answer parts the question did not ask.
3. **One answer checked by rules or a second model call** - would catch a changed number or a dropped condition only approximately, adds a second model to trust, latency and cost, and is out of scope for v1.
4. **Show no model text** - ADR 0009's card; every word is checked, but the employee has to work out the answer from the quotes.

Option 2 is the strongest alternative because it keeps a one-to-one link between each sentence and the quote a rule verified.
Option 4 is the strongest safety alternative, and the issue rules it out for v1 as ADR 0011 did.

## Decision

The model returns `{answer, points: [{quote, chunks}], disagreement}`.
`answer` is the only claim: it answers every part of the question.
A typical answer is one sentence; it uses two or three short sentences only when the question has several parts.
`points` holds only the quotes that support the answer, so a clause the question does not ask about is not cited.
The answer names no document, except when two documents give different answers that no metadata declares as a conflict: then it states both values and names each document, and never chooses between them.

The answer card shows who, the note, the answer in bold once, then each verified quote with its source line and notice line.
The conflict and refusal cards are unchanged and show no model text.
The note becomes: "Đoạn in đậm là câu trả lời của hệ thống; đoạn trong ngoặc kép là nguyên văn quy định đã được đối chiếu."

Step 7 keeps every check on quotes and chunks.
A missing `answer`, or an empty `answer` while `points` is not empty, is malformed output, so the existing refusal applies.
An empty `answer` with empty `points` stays the "no_points" refusal.
The answer is not checked by a rule or by a second model call.

`answer_text` in a run record becomes the top-level `answer`.
The review sheet shows the answer above its quotes, and `committed.py` keeps rendering older runs that stored one claim per point.
Hiep reads the answer against all the quotes under it and names the error of an unfaithful one.

## Reasons

[chờ Hiệp] Hiep's answers, in his own words, to:
- Why one answer for the whole question instead of one sentence per clause?
- Why may the answer name no document except when two documents give different values?
- Why is it still safe to show the answer without a run-time check?
- Why show the verified quotes under the answer at all?

## Consequences

- The card answers the question once instead of repeating each quote, and row 3 no longer shows the "3 ngày" deadline it did not ask about.
- The answer can rest on several quotes, so the Faithfulness reading compares it with all of them, not with one quote per sentence.
- A wrong answer can still mislead: it can add a fact, drop a condition or flip a meaning, and no rule catches that at run time.
  The verified quotes under it and Hiep's reading are the only controls.
- `key_facts` now matches the single answer, so a row passes only when that answer states every key fact.
- A model that omits `answer`, or returns an empty one with points, is refused as malformed.
- The run log, review sheet and `/cases` page carry the answer once, so the reading and the video can point to it.
- An older run keeps its per-point claims and still renders; `review.answer_of` falls back to the joined claims for those records.
- The prompt and the schema change together, so a model that still returns the old per-point `claim` is refused as malformed.

## Would change if

- Hiep's Faithfulness reading finds an answer that its quotes do not support, or a pattern of combined facts going wrong: add a check, by rule or with a second model call, and write a new ADR.
- The model keeps citing clauses the question does not ask about, or the over-caution gate fails: revisit the "only quotes that support the answer" rule.
- The model omits `answer` often enough that malformed refusals rise: change the contract or the prompt wording.
- Two undeclared values on one answer card mislead readers even when both documents are named: revisit conflict detection or hide the answer in that case (#74).

## Evidence

- `tests/services/answering/test_output.py`, `tests/services/answering/test_prompt.py`, `tests/services/answering/test_answerer.py`, `tests/services/test_card_text.py`, `tests/services/test_ask.py`, `tests/services/test_citations.py`, `tests/api/test_page.py`, `tests/api/test_source_page.py`, `tests/evaluation/test_run.py`, `tests/evaluation/test_review.py`, `tests/evaluation/test_committed.py`.
- The full evaluation run on `gemini-3.5-flash-lite`: `results/20261022-1432.jsonl`, 22 rows, 0 rules failures, 0 leaks, 0 unsafe answers and 0 over-cautious answers in the 19 gated rows; rows 15, 16 and 17 are the limitation rows, rows 15 and 17 fail as expected, and Hiep's Faithfulness reading of the 9 answer cards is pending.
- The manual check as Minh on 07/10/2026 for "Tôi xin nghỉ phép ở đâu, ai duyệt?" gave one answer that covers both where and who approves, and the card cited `LEAVE-PROC-GAMECO-v1#1` and `#2` with no "3 ngày" quote.
- The review sheet for that run: `results/20261022-1432.review.md` and `results/20261022-1432.review.yaml`; `faithful` and `lesson` are `[chờ Hiệp]`.
- Evidence log line of 22/10/2026.
