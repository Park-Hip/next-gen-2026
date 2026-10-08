# Mission 1 redraft plan

## Principles

- **Decide before writing.** Every decision is settled and recorded before any section that depends on it is written.
- **Hiep decides and writes.** Claude proposes options, critiques, and checks logic; it does not make decisions or write final text unless asked, and anything it drafts is labelled.
- **Artifacts before prose.** The worked trace, sample data and test matrix are built first; the sections then describe them.
- **Write the opener last.** Page 1 summarises the document, so it is written once the rest is stable.
- **Evidence log:** kept as a raw AI-written artifact for now; polished in Phase 7.

## Control mechanism

1. **Decision register:** `docs/mission1/redraft/decisions.md`.
   One row per decision: ID, question, options, chosen, reason, what would change it, origin.
   Origin is one of: "Hiep", "AI proposal, accepted", "AI proposal, modified", "AI proposal, rejected".
   Nothing enters the document unless it traces to a row here.
2. **Artifacts:** `docs/mission1/redraft/artifacts.md` (sample data, trace, test matrix).
3. **Sections:** written into `docs/mission1/document.md`, one section at a time.
4. **One commit per phase**, so the history shows how the thinking developed.

## Phases

### Phase 0 - Lock the frame (30 min)

Decide what stays fixed, so later phases do not reopen it.

| ID | Question | Current position |
|---|---|---|
| F1 | The one problem | "Nhân sự không biết chắc quy định nào đang áp dụng cho chính mình" |
| F2 | Primary user; is the document owner a second user? | Employee at a member company; owner listed only as gatekeeper |
| F3 | Scope of the worked example | HR policies + AI-tool policy; reviewer suggests going deep on annual leave only |
| F4 | The 3 decisions argued in full in Section 4 | Reviewer suggests: precedence and conflicts, decline vs caveat, launch model |
| F5 | Page budget | Reviewer suggests 1.25 / 1.25 / 0.75 / 1.0 / 0.75 |

Output: rows F1-F5 in the decision register.

### Phase 1 - Fix the core model (1.5-2 h)

The reviewer found that the precedence rule fails on the draft's own examples.
Everything in Section 2, Section 3 and Answer 3 depends on this phase.

| ID | Question |
|---|---|
| M1 | Which relations between documents exist (replaces, overrides, adds to, sets a minimum), and which ones v1 supports |
| M2 | Who computes entitlements such as 12 + 1 days: a rules function or the LLM |
| M3 | Are validity and company-level applicability filtered before search or after |
| M4 | Where the topic of a document comes from: assigned at publish time, or judged by AI |
| M5 | What happens for a person who belongs to two units or companies |
| M6 | Is "in force" judged on today's date, or on the date the question is about |
| M7 | Are "not allowed" and "not found" refusals worded identically |
| M8 | Are future versions shown before they take effect, and who decides |

Output: rows M1-M8, plus a one-page resolution spec (relation types and evaluation order as a small table).
Check: run Minh, Lan and Hà through the spec by hand; if any answer contradicts the persona table, fix the spec, not the table.

### Phase 2 - Build the "Thực thi" artifacts (2 h)

These are what make "giải pháp có chạy thật không?" believable without code.
Hiep defines the traps; Claude can format tables on request.

Simplified on 07/10 (decision A1): only what the PDF and the answers use.

1. Simulated documents with metadata (done).
2. Personas with an as-of date: Minh, Lan, Hà (done).
3. **Worked trace of Minh's question:** drafted by Claude, checked row by row by Hiep.
4. Naive-vs-correct contrast: what plain RAG would retrieve and say, next to the correct answer.
5. One outcome table: answer (Minh), conflict (Hà, T7), refusal.

Dropped: full traces for the other personas (their expected results become rows of the Phase 4 test matrix) and the embedding experiment V3 (Deferred ideas).

Output: `artifacts.md`.
The trace is the most important PITCH preparation in the whole plan.

### Phase 3 - Argue the 3 decisions (1.5 h)

For each decision from F4, fill this template in your own words (Vietnamese bullets are fine):

| Field | Content |
|---|---|
| A | What we choose |
| B | The strongest real alternative, not a strawman |
| What B does better | Honest strengths of B |
| Criterion | Why A wins, tied to the problem framing |
| Cost of A | What we give up |
| B wins when | The evidence that would flip the decision |
| Test | How Mission 2 checks it |

Claude critiques each argument as a judge would.
Decisions that do not make the cut become one line in an assumptions list.

Decided on 08/10 (F4r, B1): the three decisions are P (precedence and conflicts), S redefined as M18 (rulebook first, then retrieval) and L (employees ask directly vs HR first).
R becomes one line in the assumptions list in `decisions.md`.
The "Báo sai" button (B1) is on the answer card.

### Phase 4 - Validation and MVP (1 h)

| ID | Question |
|---|---|
| V1 | Metrics split by stage (deterministic: must be 100% on the test set; probabilistic: interpretation, retrieval, faithfulness), each threshold with a reason |
| V2 | The riskiest assumption, as one sentence that can be proven false |
| V4 | The 3-day plan and the "not doing" list, with why each cut does not affect testing V2 |
| V5 | Whether to commit to a naive-RAG baseline in Mission 2 |

Output: an 8-10 row test matrix excerpt (persona, question, as-of date, expected behaviour, must cite, must not cite) in `artifacts.md`.

Drafted on 08/10 by Claude, accepted by Hiep on 08/10: rows V1, V2, V4-V7 in `decisions.md`; the 10-row test matrix, metrics, 3-day plan and "not doing" list in `artifacts.md`; the deterministic part of the matrix runs in `checks/adopted_rules.py` (10/10 pass).
Two gaps were found and proposed as V6 (one clause added to `OT-GAMECO-v1`) and V7 (one line on the refusal card for M3a).

### Phase 5 - Write the sections (3-4 h)

Order: 2 → 3 → 4 → 5 → 1 → page-1 opener.
For each section:

1. Hiep writes it, from the decision register and artifacts.
2. Claude reviews it as a strict judge: logic, gaps, claims without evidence, anything not traceable to the register.
3. Hiep revises.

Drafted on 08/10 by Claude (A11, to be confirmed by Hiep): all five sections and the opener in `document.md`, 5 pages when rendered, with no internal IDs in the text.
The draft depends on the Phase 4 rows (accepted 08/10) and on A8, still pending Hiep; the notes under A11 in `decisions.md` list what was cut for length and one corrected claim.
Next: Hiep revises section by section in the order above, then Claude reviews each section as a strict judge.

### Phase 6 - Align the 3 answers (45 min)

Rewrite the answers so they match the new model.
Known changes: Answer 3 (relation types instead of "most specific wins unless mandatory"), Answer 2 (as-of date, remove "Lark/Slack"), Answer 1 (the cost asymmetry, why this problem beats leakage).
After Hiep's review on 08/10, Answer 1 no longer compares with leakage (that stays in Section 1 of the PDF), and Answer 2 does not mention the as-of date.

Requirement from the brief, quoted: "Trả lời ngắn gọn, rõ quyết định và lý do. Khuyến nghị 60–150 từ."
So each answer:

- opens with the decision;
- states the reason, not only what is done;
- is 60-150 words, counted by whitespace (each Vietnamese syllable is one word), answer text only;
- gives the reason only for the choice made, not for rejecting other options;
- is short: one idea per sentence, no detailed lists;
- uses plain words a reader who has not seen the PDF understands, with no internal terms or IDs.

Drafted on 08/10 by Claude (A12), accepted by Hiep on 08/10: `answers.md`, 147 / 148 / 145 words; revised the same day after Hiep's review (shorter, plain words, no internal terms), now 114 / 134 / 130 words.
Done; the answers are final unless Phase 7 changes the document they summarise.

### Phase 7 - Assemble and verify (2 h)

1. Render, fit to 5 pages, check every page.
2. Run `review_prompt.md` on a different model family (GPT or Gemini) for a truly independent review.
3. Hiep verifies the legal citations on an official source (vbpl.vn), or removes them.
4. Polish the evidence log: origin table, verbatim key prompts, honest verification statuses, ownership statement consistent with the PDF.
5. Copy the submitted files to `docs/mission1/submitted/` and tag the commit.

## Suggested schedule

Assuming the deadline is Friday 09/10 morning (to be confirmed with HR).

| When | Phases |
|---|---|
| Wed evening | 0, 1 |
| Thu morning | 2, 3 |
| Thu afternoon | 4, 5 |
| Thu evening | 6, 7 |
| Fri morning | Buffer, submit early |
