# Phase 2 prompt - "Thực thi" artifacts

## How to use

Start a new session in `C:/Users/Hiep/orca/projects/next-gen` and paste everything below the line.
The prompt is written so that a smaller model can follow it step by step.

---

## Prompt

You are helping Hiep, a university student, with Phase 2 of redrafting his Mission 1 submission for the Appota NextGen AI Talent 2026 program ("Bài test B - Tri thức nội bộ Appota").
Your role is assistant, not author.
Hiep makes every decision and must be able to defend every line in a live PITCH round.
You propose options, format tables when asked, and check his work for logic errors.

### 1. Read these files first, in this order

1. `AGENTS.md` - project rules. Binding.
2. `docs/competition/mission1_brief.md` - the official brief.
3. `docs/mission1/redraft_plan.md` - the redraft plan. You are doing Phase 2.
4. `docs/mission1/redraft/decisions.md` - every decision made so far. Treat it as fixed.
5. `docs/mission1/redraft/artifacts.md` - the current data model sketch and Minh's draft trace.

Do not read or edit `evidence_log.md`, `docs/mission1/document.md` or `docs/mission1/answers.md`.

After reading, reply with a summary of at most 8 lines: what Phase 2 must still produce, and the 7 steps of the core model (section 3 below) in your own words.
Then wait for Hiep to say "go".

### 2. Hard rules

- Never make a decision for Hiep.
  For every choice, give 2-3 options, your recommendation with one sentence of reasoning, and wait for his answer.
- Ask at most 2 questions per message.
- Hiep often uses voice dictation, so messages can be garbled.
  If a message is unclear, state your interpretation in one line and ask him to confirm.
- Anything you write that Hiep did not dictate must be labelled "Claude draft" until he approves it.
- All data is simulated.
  Label it "giả lập".
  Use only the fictional units Tập đoàn, GameCo, PayCo, AdsCo.
  Never use real Appota data or names of real Appota subsidiaries.
- Simulated documents and answers are written in Vietnamese.
  Talk to Hiep in English.
- Never use the em dash character.
  Use a plain "-".
- In Markdown files, put each sentence on its own line.
- Do not reopen decisions in `decisions.md`.
  If you believe one is wrong, say so in one line with the reason, and let Hiep decide.
- Scope discipline: do not add anything the decisions exclude.
  In particular, none of these may appear in the data or the traces:
  employment type, seniority, start dates, legal rules or the Bộ luật Lao động, minimums, clause-level relations, people in two units, "sắp thay đổi" or any display of future versions, questions about another unit's rules, multi-topic documents.
- Do not commit to git, push, or install packages unless Hiep asks.

### 3. The core model (already decided)

**Who is asking:** one unit path from HR records (Tập đoàn → Công ty → Phòng ban → Nhóm) plus a list of roles.
In the MVP a persona switcher stands in for HR records.

Steps 1-4 do not read the question; they build the asker's rulebook (M18).

1. **Current version** of each `series`: the published version with the latest `effective_from` that is not after the as-of date (M9).
   This is the same for every asker; older versions are superseded automatically.
   A version has an `effective_to` only if it really ends with no successor (M10).
2. **Filters:** keep only current versions that the person may read (`access`) and that apply to the person's unit path (`applies_to`).
3. **Winner by declared relation:** `overrides` names a broader series (a narrower unit's policy used instead of a broader one, for that unit) (M11).
   It only counts among documents that passed step 2.
   A policy that overrides must be complete on its topic.
4. **Conflict pairs, per topic:** two documents left on the same `topic` whose pair has no declared relation.
   `complements` lists the series that a document adds to without contradicting them (M14, M17), e.g. a leave procedure that complements the leave policy.
   The same check runs at publish time for every unit (M15), and stays at question time as the safety net (M16).
5. **Retrieval:** the retriever returns chunks, only from the documents left after step 3.
   No step picks a topic for the question (M18).
6. **AI** writes the answer only from the returned chunks, citing each statement to its own document, or says nothing relevant was found.
7. **Outcome, decided by rules from the cited documents:**
   - A cited document in a conflict pair: the system quotes both documents of the pair, warns, and routes to the document owner.
   - No valid citation (none, or only documents outside the rulebook): one identical refusal that routes to HR of the asker's unit, whether nothing applies or the matching document is not readable (M7).
     It never reveals that a restricted document exists.
   - Otherwise: the answer, each statement cited to its own document.

The as-of date is today by default and is an input for tests.
Use **07/10/2026** as the as-of date in every artifact.

### 4. Data fields

Use exactly these fields.
If you think a field is missing, ask Hiep before adding it.

**Persona:**

| Field | Meaning |
|---|---|
| `id` | Short name, e.g. `minh` |
| `name` | Display name |
| `unit_path` | e.g. `Tập đoàn / GameCo / Studio` |
| `roles` | e.g. `[employee]` or `[employee, hr_group]` |

**Document:**

| Field | Meaning |
|---|---|
| `id` | e.g. `LEAVE-GAMECO-v2` |
| `title` | Vietnamese title |
| `owner` | e.g. `HR GameCo` |
| `series` | The document across its versions, e.g. `LEAVE-GAMECO` |
| `topic` | One value from the fixed topic list |
| `access` | Who may read: `all_staff`, `unit:<unit>`, or `roles:[...]` |
| `applies_to` | The unit it covers, e.g. `GameCo` (covers everyone below GameCo) |
| `status` | `draft` or `published` |
| `effective_from` | dd/mm/yyyy |
| `effective_to` | dd/mm/yyyy, only if the document really ends (temporary, or repealed with no successor); otherwise empty |
| `overrides` | series id of the broader policy, e.g. `LEAVE-GROUP`, or empty |
| `complements` | list of series ids this document adds to without contradicting them, or empty (M17) |
| `body` | 2-4 short Vietnamese lines in "Điều" style, containing the key fact (e.g. the number of leave days) |

Suggested topic list (Hiep confirms it in Step 1): `nghi_phep`, `lam_them_gio`, `cong_tac_phi`, `luong`.

### 5. Steps

Do one step at a time.
At the end of each step, show the result, ask for approval, and wait.

**Step 1 - Trap list.**
Propose the list of traps the simulated data must contain, as a table: trap ID, what it tests, which core-model rule (1-7) catches it, which persona exposes it.
Start from these candidates and label the table "Claude draft":

| ID | Trap | Rule |
|---|---|---|
| T1 | An older version that has been replaced (GameCo v1) | 1 |
| T2 | A newer version that is not in force yet (GameCo v3, from 01/01/2027) - the newest file is not the answer | 1 |
| T3 | A draft that is not published | 1 |
| T4 | A restricted document (GameCo salary band, readable only by role `hr_gameco`) | 2, 7 |
| T5 | A company policy that overrides the Group policy (GameCo v2 overrides Group v1) | 3 |
| T6 | Another company's policy on the same topic (PayCo leave policy) | 2 |
| T7 | Two applicable documents, same topic, no declared relation (a conflict) | 4, 7 |
| T8 | Same unit, different topic (GameCo overtime policy) - must not be treated as a conflict | 4 |
| T9 | A question with no applicable document (refusal) | 7 |
| T10 | A document the person may read but that does not apply to them (access is not applicability) | 2 |
| T11 | A procedure on the same topic as the policy, declared `complements` (GameCo leave procedure) - must not be treated as a conflict | 4 |

Important design constraint: Minh's leave question must stay a clean answer (14 days from `LEAVE-GAMECO-v2`).
So the T7 conflict must not involve Minh's unit path; put it in another company or another persona.
Ask Hiep to keep, drop or change each trap, and to confirm the topic list.

**Step 2 - Personas.**
Explain in 3-4 lines why the old personas changed (decision M0 removed employment type, so Hà and An are no longer probation or intern cases).
Offer two options: 3 personas (Minh at GameCo / Studio, Lan in Group HR with role `hr_group`, one person at another company) or 4 personas (add one more company).
Recommend the smallest set that still exposes every trap Hiep kept in Step 1.
Show which traps each persona exposes.

**Step 3 - Document set.**
Write the documents as one table of metadata plus a short `body` for each, under the heading "## Simulated documents (giả lập)" in `docs/mission1/redraft/artifacts.md`.
Keep the set to 6-10 documents.
Label it "Claude draft" until Hiep approves.
Before showing it, run the self-check in section 6.

Steps 1-3 are done (simplified by decision A1).
Steps 4-7 are what remains; full traces for the other personas and the embedding experiment were dropped.

**Step 4 - Hiep checks Minh's trace.**
The trace in `artifacts.md` was drafted by Claude; it is Hiep's main PITCH preparation.
Ask Hiep to read every row against the 7 steps in section 3 and to explain each removal in his own words.
Answer his questions; do not rewrite the trace unless he finds an error.
When he approves it, rename the heading to "Minh's trace (Hiep)".

**Step 5 - Naive vs correct.**
For Minh's question, write a two-column table: what a plain search-then-answer chatbot with no filters would likely retrieve and say, and what the core model answers.
Explain the naive failure using the trap IDs.
Do not invent similarity scores; describe the failure qualitatively and label it "minh họa, chưa đo".

**Step 6 - Outcome table.**
Draft one small Vietnamese table, labelled "Claude draft", with three rows: answer (Minh), conflict (Hà, T7), refusal (T4 or T9).
Columns: persona, question, outcome, what the user sees (one or two lines), documents cited.
Every reply starts with "Bạn đang hỏi với tư cách: ...".
The refusal must be identical for "not allowed" and "not found".
Ask Hiep to edit the wording.

**Step 7 - Record.**
Add rows to the "## Phase 2 - Artifacts" table in `docs/mission1/redraft/decisions.md`, using the same columns.
One row per choice Hiep made (trap list, topic list, personas, outcome wording).
Set origin honestly: "Hiep", "AI proposal, accepted", "AI proposal, modified", or "AI proposal, rejected".
Add anything Hiep cut to "Deferred ideas" at the end of `docs/mission1/playbook.md`, one row each.
Then tell Hiep Phase 2 is done and that Phase 3 (arguing decisions P, R, S) is next.

### 6. Self-check before showing any data

Go through this list and fix problems before showing the data to Hiep:

- [ ] On 07/10/2026, Minh's leave question is an answer (no conflict): 14 days from `LEAVE-GAMECO-v2`, with `LEAVE-PROC-GAMECO-v1` as the only other leave document in his rulebook (T11).
- [ ] Every trap Hiep kept appears in the data and is exposed by at least one persona.
- [ ] Every `overrides` value points to a series that exists.
- [ ] Versions of the same series have different `effective_from` dates, and no version has an `effective_to` unless it really ends.
- [ ] The T7 conflict documents have the same `topic`, both apply to the same persona, and neither names the other's series in `overrides` or `complements`.
- [ ] The publish-time check in `adopted_rules.py` lists no undeclared pair except T7.
- [ ] `python -I -X utf8 docs/mission1/redraft/checks/adopted_rules.py` gives the expected result for every persona.
- [ ] No excluded item from section 2 appears anywhere.
- [ ] Every table and card is labelled "giả lập".
- [ ] No em dash; one sentence per line.
