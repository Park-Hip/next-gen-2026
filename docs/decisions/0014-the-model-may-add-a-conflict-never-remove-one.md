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

The model's reply may name two cited chunks, from two different documents in the asker's scope, that give different answers to the question.
Step 7 accepts the flag only if both chunks were retrieved, both are cited with quotes that pass the quote check, and they come from two different documents; it then shows the conflict card for those two documents, even when they declare "bổ sung".
A flag that fails a check is ignored, and nothing the model says can remove a conflict card.
The card uses the same headline as a declared conflict and records `reason: "model_flagged"`.

## Reasons

[chờ Hiệp]

## Consequences

- G3.3 is covered at question time when the model sees both sides and notices; a missed disagreement still gives the answer card, as before.
- A false alarm gives a conflict card where an answer was possible; it counts as over-cautious, with the gate at 10%.
  No error of the flag can give a wrong answer with confidence.
- The rules still decide the card; the model's flag is one more input, checked like a citation.
- G3.2 stays a limitation, on purpose.
- The publish check (option 1) stays deferred with the owners' page and G3.5.
- To build in #87: the `disagreement` field in #75's contract, the prompt instruction, the check in step 7, `reason` on the conflict card, and the pytest and evaluation rows listed there.

## Would change if

- False alarms push the over-cautious rate past 10% on the evaluation.
- The publish check is built and owners settle contradictions before publishing.

## Evidence

To come with #87: row 19, rows 3 and 20 as the false-alarm watch, and the pytest cases for each ignored flag.
Evidence log line of 21/10/2026.
