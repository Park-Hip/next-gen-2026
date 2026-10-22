# 0014. The model may add a conflict it reads in the text, never remove one

- Status: Proposed
- Date: 2026-10-21
- Origin: Hiep + AI
- Supersedes: The "Deferred" row of `docs/scope.md` "An AI check that may add, never remove, a conflict warning when topics look mis-tagged", brought forward; "no conflict detection at question time" in SD14 of `docs/system_design.md` (Hiep, 20/10/2026)
- Issue: #87
- Research: None

## In short

- **The problem:** The product finds a conflict only from the labels owners put on documents: two policies in the asker's scope with the same topic and no declared relation.
  If a label is wrong, two policies that disagree are never paired.
  Hà, who works at PayCo, asks how many days of annual leave she has.
  The PayCo policy says 13 and the Group policy, which also applies to her, says 12.
  If the PayCo policy carries a slightly different topic label, Hà gets a confident answer card saying "13 ngày".
- **The decision:** The AI may flag two cited clauses from two different documents that give different answers.
  Fixed rules check the flag and, if it is valid, add the conflict card.
  The AI can add a conflict, but it can never remove one or change a refusal.
- **What the employee sees:** A conflict card where, before, a confident answer card hid the disagreement.
  Every conflict card now uses one headline, whether the conflict came from the labels or from the AI's flag.
- **What we give up:** A false alarm gives a conflict card where an answer was possible, which counts as over-cautious.
  A disagreement the AI misses still gives an answer card, as before.

All data is simulated ("giả lập").

## Context

Mission 3 general requirement 3 asks the product to handle conflicting sources.
The Mission 2 version forms a conflict pair only from labels: two documents in the asker's scope with the same topic and no declared "bổ sung" (addition) relation.
The rules never compare what two documents say, so a disagreement written only in the text gives no conflict card.
On edited data, where the PayCo leave policy carries a topic label that differs slightly from the Group policy's, Hà gets no conflict pair, and a reply citing only the PayCo clause gives an answer card "13 ngày", although the Group policy that also applies to her says 12.
A wrongly declared "bổ sung" (addition) hides the conflict in the same way.
Telling that two clauses answer one question differently is reading meaning, which only the AI does.
The mirror case, where the two sides of a declared pair agree on the point asked, gives the conflict card when an answer was possible.

## Options considered

1. **A check when the owner publishes** - each clause of a new document is searched against the knowledge base, and an AI warns the owner of a contradiction, who settles it by declaring a relation or changing the text (Hiep's idea, 21/10/2026).
   It needs the owners' page, which ADR 0004 cut, so it is deferred and stays the long-term fix.
2. **A flag from the AI at question time, one way only** - the AI lists two cited clauses from different documents that give different answers; a fixed rule checks the flag and adds the conflict card; the AI can never remove a conflict card (chosen, for v1).
3. **Both ways at question time** - the AI may also say that two sides of a declared pair agree, and the rule then gives the answer card.
   It would fix the mirror case, but a wrong "they agree" hides a real conflict and gives a wrong answer with confidence.
4. **Keep the labels only** - the hidden-disagreement problem stays a limitation until the publish check exists.

The strongest alternative is option 4, which keeps every card decided without the AI.

## Decision

The AI's reply carries a required list of at most two clause ids, empty when no clauses disagree.
A missing or malformed list is read as empty, so a bad flag never refuses an answer that is otherwise valid.

The quote check reads the flag only after all its refusals (unreadable output, no points, a citation outside what was retrieved, a quote that fails the check).
It accepts the flag only if all of these hold:

- there are exactly two different ids;
- both were retrieved;
- each is cited by a point whose quote is found in that clause itself;
- the two clauses come from two different documents in the asker's scope.

A valid flag adds the pair of those two documents to the card's conflicts, even when they declare "bổ sung", and the card is the conflict card.
A flag that fails a check is ignored, and nothing the AI says can remove a conflict card or change a refusal.
The card records that the AI's flag added the pair only when the declared pairs did not already contain it; this record is for the log and the results file and is never shown.

Every conflict card uses one headline, true whether the pairs come from the rules or from the flag:
"Có {n} quy định cùng áp dụng cho bạn nhưng chưa được khai báo quy định nào được dùng thay quy định nào. Hệ thống không tự chọn."
Here n is the number of documents on the card, and each document is quoted once.
This changes the fixed wording of Phần 2 of the Mission 1 document, which said "hai quy định" and "chưa được khai báo quan hệ với nhau", a sentence that is false for a flagged pair across a declared "bổ sung".

## Reasons

[chờ Hiệp]

## Consequences

- The hidden-disagreement problem is covered at question time when the AI sees both sides and notices; a missed disagreement still gives the answer card, as before.
- A false alarm gives a conflict card where an answer was possible; it counts as over-cautious, with the limit at 10%.
  No error of the flag can give a wrong answer with confidence.
- The rules still decide the card; the AI's flag is one more input, checked like a citation.
- The mirror case (declared pair, both sides agree) stays a limitation, on purpose.
- The publish check (option 1) stays deferred with the owners' page.
- What was built: the flag in the AI's output contract, the prompt instruction, the check, the record on the conflict card, the one headline for every conflict card, and the tests and evaluation cases listed in the issue.

## Would change if

- False alarms push the over-cautious rate past 10% on the evaluation.
- The publish check is built and owners settle contradictions before publishing.

## Evidence

- Checked by offline tests: a valid flag on the wrong-topic data and across a wrongly declared "bổ sung"; each kind of ignored flag; a flag that never changes a refusal or removes a pair; the output schema and parser; the headline; and the page on the edited data (files in Technical detail).
- To come: test case 19, with cases 3 and 20 as the false-alarm watch, in the shared full run after two related changes are merged; the results file is Hiep's to run with his key.
- Evidence log line of 21/10/2026.

## Technical detail

- Built in #87 (answer contract from #75; related changes #83 and #76); gaps G3.2 (declared pair, both sides agree; case 17, [#52](https://github.com/Park-Hip/next-gen-2026/issues/52)), G3.3 (disagreement hidden by metadata; [#74](https://github.com/Park-Hip/next-gen-2026/issues/74), case 19 planned in #75, [#50](https://github.com/Park-Hip/next-gen-2026/issues/50) example 1) and G3.5 (publish check and owners' page); SD14; Mission 1 Phần 2.
- Pairs come from `topic` and `complements`; the edit gives `LEAVE-PAYCO-v1` the topic `nghi_phep_nam`.
- The field is `disagreement` in the output schema: a list of at most two retrieved chunk ids.
  `parse_disagreement` returns an empty tuple for a missing or malformed field.
  `flagged_pair` in `services/citations.py` applies the four checks after the refusals of `card_for_answer`.
- The card records `reason: "model_flagged"` only when the flag adds a pair that the declared pairs do not already contain; `reason` goes to the log and the results file.
- The headline is `CONFLICT_HEADLINE` in `services/card_text.py`.
- Tests: `tests/services/test_citations.py`, `tests/services/answering/test_output.py`, `tests/services/test_card_text.py` (the headline and P9), `tests/api/test_page.py`.
