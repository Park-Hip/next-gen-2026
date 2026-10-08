# Current design - what is decided now

The single source for the design in force.
Snapshot of 08/10/2026, 20:20, after commit `5fe9edb`; Mission 1 was submitted at about 21:30 the same day with no design change since.
Claude draft from `decisions.md`, `document.md` and `answers.md`; Hiep checks it against his own understanding.

How to read this page:

- It lists only what is in force now, grouped by where it shows in the submission.
- The submitted text (`docs/mission1/submitted/`) is what judges hold; Mission 2 is checked against it through `docs/mission2/mission1_promises.md`.
- `decisions.md` is frozen as the Mission 1 audit trail; old IDs appear here only in the "Trace" column.
- From Mission 2 on, a decision change is made here: edit the row, add a line to "Changes since submission" with the date, the reason and who decided, and add an evidence log entry if AI shaped it.
- Origin uses four plain values: **Hiep** (his idea or his call), **Hiep + AI** (Hiep raised the problem or set the direction, AI shaped the solution), **AI, accepted** (AI proposed, Hiep approved), **AI, not reviewed** (still needs Hiep).

## ID prefixes in `decisions.md`

| Prefix | Meaning |
|---|---|
| F | Frame of the document (Phase 0); F4r replaces F4 |
| M | Core model: documents, filters, relations, the 7 steps (Phase 1-2) |
| A | Artifacts and authorship: data, traps, who drafted what (Phase 2-6) |
| B | The "Báo sai" button |
| V | Validation, metrics, build order (Phase 4) |
| RV | Changes after reviews (Phase 5): RV1-RV7 new-reader review, RV8-RV14 Hiep's batch 3 notes |
| T1-T11 | Traps in the simulated data (`artifacts.md`) |
| P, S, L | The 3 decisions of Section 4: P = Quyết định 1, S = Quyết định 2, L = Quyết định 3 |

## 1. Problem and users (Phần 1, Câu 1)

| Decided now | Trace | Origin |
|---|---|---|
| The one problem: staff do not know for sure which rule applies to them; the outcome is a correct decision the first time, without waiting for HR | F1 | AI, accepted |
| Why this problem over leakage: a leak has a clear block (restricted documents never enter search), so "no leak" is a condition of every option; a wrong-rule answer looks identical to a right one, so it is the real problem | F1 | AI, accepted |
| The design accepts "chưa chắc, hãy hỏi HR" to avoid a confident wrong answer | F1, M1b | Hiep (Round 2: higher refusal rate for safety) |
| Primary user: employees of member companies when they act under a rule; second user: the document owner (HR of each unit), because metadata stays correct only if someone keeps it correct | F2 | AI, accepted |
| Scope: HR policies, one deep example (annual leave); the AI-tool policy and legal rules are out | F3, M1c | AI, accepted (F3); Hiep (M1c, legal rules out) |
| Only three dimensions decide the answer, as in the brief: unit, access, version; no employment type or seniority | M0 | Hiep + AI (Hiep asked whether the model came from the brief or our assumptions) |
| Three separations: relevant ≠ allowed, allowed ≠ applies to me, newest ≠ in force | Core thesis | AI, accepted (playbook, 07/10) |

## 2. Solution and the 7-step flow (Phần 2, Câu 3)

| Decided now | Trace | Origin |
|---|---|---|
| RAG with a rules layer in front: rules build the asker's "phạm vi tìm kiếm" from metadata, without reading the question and without AI; then normal retrieval and generation inside it | M18, M3b, M12 | Hiep + AI (Hiep: apply relations before search, and "why choose a topic at all"; AI: filters first, steps 4 and 7) |
| Step 1: each series keeps its current version: published, latest `effective_from` not after today; a newer version removes the older one, a future version or a draft does not | M9, M10, A4 | AI, accepted (from the production review Hiep asked for) |
| Step 2: keep documents the asker may see (access) and that apply to their unit (applicability) | M3b, M3a | AI, accepted |
| Step 3: drop a document when another kept document declares "dùng thay" (overrides) over its whole series, including later versions | M1a, M11, M12 | Hiep + AI (Hiep: clause-level is too complex, relations before search); AI, accepted (points at the series) |
| No default "lower unit wins": precedence exists only where the owner declared it | M1b | Hiep |
| Step 4: mark conflict pairs: same topic, both apply, no "dùng thay" or "bổ sung" between them | M1b, M4, M14 | Hiep + AI (Hiep: same topic is not always a conflict; AI: `complements`) |
| "Bổ sung" (complements) is a list of series, declared pair by pair by the owner | M14, M17 | Hiep + AI |
| Topic: one per document, set by the owner; its only job is finding conflict pairs | M4, M18 | AI, accepted |
| Step 5-6: hybrid retriever (keyword + embedding) inside the scope; an off-the-shelf LLM answers only from retrieved chunks, cites each point, or says "không tìm thấy" | M18, RV7 | Hiep (hybrid search); AI, accepted (rest) |
| Step 7: rules pick the card from the cited documents: a cited document in a conflict pair gives the conflict card; no citation, or any citation outside the retrieved chunks, refuses the whole answer | M18, RV5 | AI, accepted |
| Keep the question-time conflict check even with the publish-time list, because the list only warns and some pairs appear without any publishing | M15, M16 | Hiep + AI (Hiep asked whether to keep it, decided to keep); AI, accepted (publish-time list) |
| Three cards, each with "Bạn đang hỏi với tư cách": answer (with source, Điều, effective date, "Báo sai"); conflict (neutral headline, both clauses quoted word for word, no LLM text); refusal (one text for "not allowed" and "not found", plus "chỉ trả lời các quy định áp dụng cho bạn") | A8, RV4, RV8, M7, V7, B1 | AI, accepted (RV4, RV8 wording, M7, V7, B1); Hiep raised the RV8 case; A8 base wording: AI, not reviewed |
| v1 answers only the rules that apply to the asker; other-unit questions get the refusal card | M3a, M13, V7 | AI, accepted |
| A future version is not shown before it takes effect | M8 | AI, accepted |

## 3. AI, data and people (Phần 3)

| Decided now | Trace | Origin |
|---|---|---|
| AI does two things only: retrieval and generation, because most of their errors fail safe or are blocked by rules | M18 | AI, accepted |
| AI never decides access, validity, applicability, precedence, or which card to show | Core rule, M1b | Hiep (13:55 on 07/10: no AI judging conflicts, route to a human) |
| Remaining hole: the LLM cites a valid document that does not answer the question, or misstates a passage; Section 5 tests exactly this | V2 | AI, accepted |
| Data: 10 simulated Markdown documents, split by Điều, with metadata; a simulated persona picker instead of the HR system (the real one takes the unit from the HR system) | A2, A6, RV14 | AI, accepted |
| People: owners declare relations and handle the conflict and "Báo sai" list; HR of the asker's unit handles refusals, conflicts and access requests; employees check the source and press "Báo sai" | F2, B1, V4 | AI, accepted |

## 4. The 3 decisions and the risks (Phần 4)

| Decision | A (chosen) | B (strongest alternative) | Trace | Origin |
|---|---|---|---|---|
| 1. Who picks the winning document | Owner declares "dùng thay" / "bổ sung"; undeclared gives the conflict card | LLM picks, or the fixed rule "lower unit wins" | P, M1b, RV1 | Hiep (no AI judging; conflict = undeclared pair); AI, accepted (argument, RV1) |
| 2. How documents are found for the question | Build the scope first, then retrieve inside it; no topic guess | LLM sorts the question into a topic, then a rules lookup | S, M18, batch 5 | Hiep + AI (Hiep's question led to it; B chosen and wording approved 08/10) |
| 3. Who uses it first | Employees ask directly from v1 | HR drafts and checks answers for a few weeks first | L, F4r, RV2 | AI, accepted |

Failure cases in the PDF:

- Owners declare a wrong "bổ sung" and two different rules are merged; simulated data cannot test this (V2 option a).
- A company changes only one clause of a Group rule; v1 cannot express it, because "dùng thay" removes the other clauses (M1a).
- HR cannot yet ask about another unit; later the user picks the unit, never an AI guess (M13).

Assumptions stated in one line instead of argued: refusal without a valid citation (R), filters before search (M3b), one reply for "not allowed" and "not found" (M7), only three dimensions (M0), no future versions (M8), `status` is our assumption (A4).

## 5. Validation and build order (Phần 5, Câu 2)

| Decided now | Trace | Origin |
|---|---|---|
| Test idea: same question, different asker or different date, must give different results | V1, RV11 | AI, accepted |
| Five test situations in words in the PDF; the 10-row matrix and its phrasings (standard, paraphrase, "văn nói") stay internal as the Mission 2 plan | RV11, RV7 | Hiep (no table in the PDF); AI, accepted (văn nói) |
| Metrics with targets on the test set: rules correct in every case, 0 leaks, 0 unsafe LLM answers, faithfulness read by hand, at most 10% over-cautious, context recall tracked only | V1, RV13 | AI, accepted (Hiep asked to tone down confidence) |
| Reaching the targets on a small simulated set is a condition to open, not proof | V1, RV13 | AI, accepted |
| Riskiest assumption: with no answering document the LLM says "không tìm thấy"; with one, it cites that one; one unsafe answer disproves it | V2 | AI, accepted |
| Build order: rules and tests first (100% before any LLM), then retrieval and generation, then a minimal page (persona and date picker, three cards, "Báo sai", owners' list) | V4 | AI, accepted |
| Answer 2's day plan: day 1 data, rules, tests; day 2 AI answers with sources; day 3 web page; not doing: real login, HR system, chat tools, DOCX/PDF | V4, A12, A13 | AI, accepted (after Hiep's review and the ChatGPT/Gemini review) |
| The rule script is not shown to judges; the PDF only says the rules part ran correctly on simulated data | RV6 | Hiep |

## 6. Reversed or dropped

Each line is a change of mind; most are Hiep's calls and belong in the evidence log as evidence of ownership.

| What changed | Why | Trace | Who |
|---|---|---|---|
| An LLM checking whether two passages conflict: rejected | It can hallucinate "no conflict"; route to a human | Round 2, M1b | Hiep |
| Legal rules and legal minimums: dropped from the MVP | Too complex; no new trap | M1c | Hiep |
| Employment type and seniority: dropped | Not in the brief | M0 | Hiep + AI |
| Clause-level relations: dropped | Too complex for v1 | M1a | Hiep |
| Hand-typed `replaces` and pre-set `effective_to`: replaced by series | The old version came back, or a delayed version left no policy | M9, M10 | AI, accepted |
| `overrides` pointing at a version: now points at a series | Every new Group version broke every override | M11 | AI, accepted |
| `covers` (a question key per chunk): rejected | Needs a label on every chunk; fails on unstructured documents | M14 | Hiep |
| Search picks the topic, or the LLM classifies it: replaced by scope first | No AI step should choose a topic | M18 | Hiep + AI |
| Decision "decline vs warn" (R): moved to the assumptions list; L added | After M18 there is no "unsure" state | F4 → F4r | AI, accepted |
| Dropping invalid citations and keeping the answer: now the whole answer is refused | An invented source means the rest cannot be trusted | M18 → RV5 | AI, accepted |
| Keyword search without diacritics and the "không dấu" test phrasing: replaced by hybrid search and "văn nói" | Hiep's call | RV7 | Hiep |
| Pilot paragraph (one company, 4 weeks): removed | The document includes only what the MVP does | RV3 → RV9 | Hiep |
| Naive-RAG baseline in the MVP: removed; Section 1 keeps it as a hedged prediction ("dễ xếp") | Hiep's call; it was the first cut anyway | V5 → RV10 | Hiep |
| Test table and 9.5% bound in the PDF: replaced by five situations in words | Too detailed for a plan | RV11 | Hiep |
| Phase 4 day plan and "not doing" list in the PDF: moved to Answer 2 | Section 5 answers "phần nào làm trước" | Batch 1 | Hiep (note 9) |
| Embedding experiment, full traces for Lan and Hà: not done | Not needed by the PDF | A1, V3, A9 | Hiep (to cut); AI, accepted (what to cut) |
| Overtime clause added for test row 4: kept in the data, unused in the PDF | The cross-topic example was cut for length | V6 | AI, accepted |
| First draft of the 3 answers: rejected | Too long, argued against other options, used internal terms | A12 | Hiep |

## 7. Still open

Found while building this page on 08/10.

1. **A8, card wording:** the register still says "AI proposal, not yet reviewed by Hiep", but the cards in the PDF were reworded under RV4, RV8 and V7, which he accepted. Hiep to confirm the three cards as they are in Section 2.
2. **A11, who drafted the PDF:** still "to be confirmed by Hiep", although he has reviewed four batches since. Hiep to confirm the delegation in one line.
3. **Hiep's own walk-through (PITCH prep):** read sections 1-6 of this page and confirm he can explain each row aloud; mark any row he cannot.

Closed after submission:

- Stale lines in `decisions.md` (Phase 4 header, V5 in the Phase 5 notes) and `artifacts.md` (pilot as the live signal): fixed 08/10.
- Answer 2 vs Section 5 (day 3 without "Báo sai" and the owners' list): kept as submitted; building the Section 5 version satisfies both, see "Tensions" in `docs/mission2/mission1_promises.md`.

## Changes since submission

None yet.
