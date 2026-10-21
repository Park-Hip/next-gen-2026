# 0014. The model may add a conflict it reads in the text, never remove one

- Status: Proposed
- Date: 2026-10-21
- Origin: Hiep + AI
- Supersedes: The "Deferred" row of `docs/scope.md` "An AI check that may add, never remove, a conflict warning when topics look mis-tagged", brought forward; "no conflict detection at question time" in SD14 of `docs/system_design.md` (Hiep, 20/10/2026)
- Issue: #87
- Research: None

## Context

Mission 3 general requirement 3 asks the product to handle conflicting sources.
v1 forms a conflict pair only from metadata: two documents in the asker's scope with the same `topic` and no declared "bổ sung".
The rules never compare what two documents say, so a disagreement written only in the text gives no conflict card (gap G3.3).
On edited simulated data ("giả lập"), with `LEAVE-PAYCO-v1` tagged `nghi_phep_nam`, Hà gets no conflict pair, and a reply citing only the PayCo clause gives an answer card "13 ngày", although the Group policy that also applies to her says 12 ([#74](https://github.com/Park-Hip/next-gen-2026/issues/74), row 19 planned in #75).
A wrongly declared "bổ sung" hides the conflict the same way ([#50](https://github.com/Park-Hip/next-gen-2026/issues/50) example 1).
Telling that two clauses answer one question differently is reading meaning, which only the model does.
The mirror case, two sides of a declared pair that agree on the point asked, gives the conflict card when an answer was possible (G3.2, row 17, [#52](https://github.com/Park-Hip/next-gen-2026/issues/52)).

## Options considered

1. **A check when the owner publishes** - each clause of a new document is searched against the knowledge base, and an LLM warns the owner of a contradiction, who settles it by declaring a relation or changing the text (Hiep's idea, 21/10/2026); it needs the owners' page, cut by ADR 0004, so it is deferred and stays the long-term fix.
2. **A flag from the model at question time, one way only** - the model lists two cited clauses from different documents that give different answers; a deterministic rule checks the flag and adds the conflict card; the model can never remove a conflict card (chosen, for v1).
3. **Both ways at question time** - the model may also say that two sides of a declared pair agree, and the rule then gives the answer card; it would fix G3.2, but a wrong "they agree" hides a real conflict and gives a wrong answer with confidence.
4. **Keep metadata only** - G3.3 stays a limitation until the publish check exists.

The strongest alternative is option 4, which keeps every card decided without the model.

## Decision

The model's reply carries a required field `disagreement`: a list of at most two retrieved chunk ids, empty when no clauses disagree.
A missing or malformed field is read as an empty list, so a bad flag never refuses an answer that is otherwise valid.
Step 7 reads the flag only after its refusals (malformed output, no points, a citation outside the retrieved chunks, a quote that fails the check).
It accepts the flag only if there are exactly two different ids, both retrieved, each cited by a point whose quote is found in that chunk itself, and the two chunks come from two different documents in the asker's scope.
A valid flag adds the pair of those two documents to the card's conflicts, even when they declare "bổ sung", and the card is the conflict card.
A flag that fails a check is ignored, and nothing the model says can remove a conflict card or change a refusal.
The card records `reason: "model_flagged"` only when the flag adds a pair the declared pairs do not already contain; `reason` is for the log and the results file and is never shown.
Every conflict card uses one headline, true whether the pairs come from the rules or from the flag: "Có {n} quy định cùng áp dụng cho bạn nhưng chưa được khai báo quy định nào được dùng thay quy định nào. Hệ thống không tự chọn.", with n the number of documents on the card, and each document is quoted once.
This changes the fixed wording of Phần 2 of the Mission 1 document, which said "hai quy định" and "chưa được khai báo quan hệ với nhau", a sentence that is false for a flagged pair across a declared "bổ sung".

## Reasons

[chờ Hiệp]

## Consequences

- G3.3 is covered at question time when the model sees both sides and notices; a missed disagreement still gives the answer card, as before.
- A false alarm gives a conflict card where an answer was possible; it counts as over-cautious, with the gate at 10%.
  No error of the flag can give a wrong answer with confidence.
- The rules still decide the card; the model's flag is one more input, checked like a citation.
- G3.2 stays a limitation, on purpose.
- The publish check (option 1) stays deferred with the owners' page and G3.5.
- Built in #87: the `disagreement` field in #75's contract, the prompt instruction, the check in step 7, `reason` on the conflict card, the one headline for every conflict card, and the pytest and evaluation rows listed there.

## Would change if

- False alarms push the over-cautious rate past 10% on the evaluation.
- The publish check is built and owners settle contradictions before publishing.

## Evidence

Built in #87 and checked by pytest: `tests/services/test_citations.py` (a valid flag on the wrong-topic data and across a wrongly declared "bổ sung", each ignored flag, a flag that never changes a refusal or removes a pair), `tests/services/answering/test_output.py` (the schema and the parser), `tests/services/test_card_text.py` (the headline and P9), and `tests/api/test_page.py` (the page on the edited data).
To come: row 19, with rows 3 and 20 as the false-alarm watch, in the shared full run after #83 and #76; the results file is Hiep's to run with his key.
Evidence log line of 21/10/2026.
