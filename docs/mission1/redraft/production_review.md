# Production review of the core model (Claude draft)

Claude draft, written at Hiep's request on 07/10/2026.
Nothing here is decided.
Every proposal needs Hiep's decision, recorded in `decisions.md`.
All data is simulated ("giả lập").

## Goal and method

Goal: find where the core model (`phase2_prompt.md` section 3, `decisions.md`, `artifacts.md`) breaks in real production, and propose fixes that stay aligned with the brief.

Method:

1. Read the brief, the decision register, the artifacts and `open_issues.md`.
2. Implemented the 7 rules literally in `checks/current_rules.py` and ran them on the simulated documents.
   The baseline matches Minh's hand trace in `artifacts.md` (Minh gets `LEAVE-GAMECO-v2`, Lan gets `LEAVE-GROUP-v1`, Hà gets the T7 conflict).
3. Ran realistic changes through the same rules: time passing, a delayed version, a Group update, a complementary document, a partial override.
4. Wrote a proposed resolver in `checks/proposed_rules.py` and ran the same scenarios through it.
5. Checked real-world practice with web research (Agnes 2.5 Flash, max reasoning), then a second Agnes pass that opened every URL and checked each quote verbatim.
   Only verified sources are listed at the end.

Run the checks with `python -I -X utf8 docs/mission1/redraft/checks/current_rules.py` (and `proposed_rules.py`).

## Results at a glance

| Scenario | Current rules | Proposed rules | Correct behaviour |
|---|---|---|---|
| Baseline, Minh, 07/10/2026 | `LEAVE-GAMECO-v2` | `LEAVE-GAMECO-v2` | `LEAVE-GAMECO-v2` |
| Baseline, Hà (T7) | Conflict Group-v1 vs PayCo-v1 | Same conflict | Conflict (intended trap) |
| v3 takes effect as planned, 01/01/2027 | **Conflict GameCo-v1 vs GameCo-v3** | `LEAVE-GAMECO-v3` | `LEAVE-GAMECO-v3` |
| v3 delayed, 01/01/2027 | **Conflict Group-v1 vs GameCo-v1** | `LEAVE-GAMECO-v2` | `LEAVE-GAMECO-v2` stays in force |
| v3 delayed, P1 fixed but v2 keeps `effective_to: 31/12/2026` | (not run) | **`LEAVE-GROUP-v1`, 12 days, no warning** | `LEAVE-GAMECO-v2`; shows why P2 is needed |
| Group publishes `LEAVE-GROUP-v2` | **Conflict GameCo-v2 vs Group-v2** | `LEAVE-GAMECO-v2` | `LEAVE-GAMECO-v2` |
| GameCo adds a leave procedure document | **Conflict GameCo-v2 vs procedure** | Each question answered by its own document | No conflict, both usable |
| PayCo changes only the carry-over clause | Not expressible | Addendum answers carry-over, the rest still comes from the parent | Same as proposed |
| GameCo v2 narrowed to Studio, Marketing asks | **Conflict Group-v1 vs GameCo-v1** | `LEAVE-GROUP-v1` | Group policy (the old GameCo v1 must not come back) |

The first bold row needs no change to the data at all.
The date simply reaches 01/01/2027, the switch that decision M6 says the tests should check.

## Findings

Severity: **High** means a wrong answer or a broken trace in the current artifacts.
**Medium** means noisy warnings or a common real-world case that cannot be expressed.
**Low** means a data-shape gap that is cheap to fix now and expensive later.

### P1 - Replaced versions come back ("zombie versions") - High

What happens: `replaces` only counts among documents that passed the filters (Issue 4).
On 01/01/2027, v2 is out of its dates, so its `replaces: LEAVE-GAMECO-v1` no longer counts.
v3 replaces v2, not v1.
So v1 (`effective_to` empty) survives and conflicts with v3.
The same thing happens when v3 is delayed, or when a successor's `applies_to` is narrower than the old version's.

Root cause: whether a version is superseded is a fact about the document's lifecycle, the same for every asker.
The current model computes it per asker, after the asker's filters.

Fix: group versions into a **series** (one document across its versions, e.g. `LEAVE-GAMECO`).
On the as-of date, the current version of a series is the published version with the latest `effective_from` that is not after the as-of date.
This is computed before the asker's filters, because it does not depend on the asker.
Older versions are superseded automatically, so `replaces` no longer needs to be typed by hand (it can stay as a display field).

This keeps both reasons behind Issue 4:

- A future version cannot remove the version in force, because it is not current yet.
- A company policy cannot hide the Group policy from people outside the company, because `overrides` is still applied after the applicability filter.

One deliberate side effect: if the current version is restricted and the old one was public, the asker gets the refusal, never the stale version.

Real-world practice: controlled document systems give every document a lifecycle with separate superseded and obsolete states (Veeva Vault [S5]).
HR systems separate the effective date from the date of data entry (Workday [S6]).
VersionRAG reports 58% accuracy for naive RAG on version-sensitive questions, against 90% for a version-aware pipeline [S7].
That is a technical-documents benchmark, not HR policies, so quote it as a signal and not as a measurement of our case.

Fits: Mission 1 document (it changes the trace) and Mission 2 MVP.
Reopens: Issue 4 (refines it, keeps its constraints).
Status: accepted by Hiep, recorded as M9 and M12, applied to `artifacts.md`.

### P2 - Expiry cliff from `effective_to` - High

What happens: `LEAVE-GAMECO-v2` has `effective_to: 31/12/2026`.
If v3 is late, v2 simply expires.
Today this shows up as the zombie conflict (P1).
Once P1 is fixed, it becomes worse: Minh silently falls back to the Group policy, 12 days instead of 14, with no warning (row 6 of the table above).
That is exactly the confident wrong answer from F1.

Fix: a version ends when the next version takes effect, not on a date typed in advance.
Use `effective_to` only when a document really ends: it is temporary (for example a one-off holiday announcement), or it is repealed with no successor.
In production, alert the owner before an `effective_to` passes with no successor.
A `withdrawn` status was considered and dropped: an `effective_to` set on purpose already says the series ends.

Fits: Mission 2 MVP (data change: remove `effective_to` from v2).
In the Mission 1 document it is one sentence in the risks.
Status: accepted by Hiep, recorded as M10, applied to `artifacts.md`.

### P3 - `overrides` pinned to a version breaks on every parent update - High

What happens: `LEAVE-GAMECO-v2` declares `overrides: LEAVE-GROUP-v1`.
When Group publishes `LEAVE-GROUP-v2`, the override points at a version that is no longer in force.
Every GameCo employee gets a conflict until GameCo HR re-declares.
With N companies, one Group update creates N broken overrides at once.
A new Group version is a very likely Mission 3 change.

Fix: declare `overrides` between **series** (`LEAVE-GAMECO` overrides `LEAVE-GROUP`).

Trade-off: GameCo keeps overriding even if the new Group version changed something GameCo must follow.
Mitigation: when a parent series gets a new version, notify the owners of every series that overrides it to re-confirm.
This is a publish-time notice, not a query-time block, so employees keep getting answers.
A "mandatory, cannot be overridden" flag on parent rules is the production answer to the same risk, but it is new scope (Deferred ideas).

Fits: Mission 2 MVP (data change).
Reopens: M1a (the relation stays, its target changes).
Status: accepted by Hiep, recorded as M11, applied to `artifacts.md`.

### P4 - Same topic is not the same question (false conflicts) - Medium

This is the flaw Hiep raised, and Issue 1 in `open_issues.md`.

What happens: rule 5 calls two applicable documents with the same `topic` and no relation a conflict.
A leave policy and a leave procedure share `nghi_phep`, but they answer different questions.
The run shows a false conflict as soon as the procedure is added.

Root cause: `topic` does two jobs.
It says what a document is about (useful for search), and it is also used as the unit of conflict (which needs "which question does it answer").

Real-world practice: the conflict taxonomy in "DRAGged into Conflicts" [S1] has five categories: no conflict, complementary information, conflicting opinions or research outcomes, conflict due to outdated information, and conflict due to misinformation.
Complementary information is defined as answers that "are mutually compatible, meaning that a single person can reasonably agree with all of them simultaneously".
The current rule 5 cannot tell this category apart from a real conflict.
Enterprise metadata uses managed terms organised "into a hierarchical term set" (SharePoint [S8]), which is the shape proposed here: topics as parents, question keys as children.

Fix: replace the single `topic` with **`covers`**: the list of specific questions a document answers, taken from a small controlled list grouped under the topic.
Example: `nghi_phep.so_ngay`, `nghi_phep.thu_tuc`, `nghi_phep.chuyen_phep`.
Precedence and conflicts are then evaluated per question key:

- Two versions of the same series: the date decides (P1).
- Different series, same key, a declared `overrides`: the overriding one wins for that key only.
- Different series, same key, no relation: conflict, as today (M1b is unchanged).
- Different keys: complementary, both may be cited.

The rule "every answer comes from exactly one document" becomes "every key is answered by exactly one document".
An answer that needs two keys cites two documents.

This also solves Issue 5 (partial overrides) without clause-level relations.
A PayCo addendum that `covers: [nghi_phep.chuyen_phep]` and overrides `LEAVE-GROUP` changes only carry-over.
Everything else is still answered by the Group policy (see the addendum rows in `proposed_rules.py`).

Cost: owners tag each Điều with one key instead of tagging the document with one topic.
The key must sit on the Điều, not on the document, so that search can tell which question a passage answers (see "How `covers` changes the pipeline").
An earlier version of this review said whole-document tags were enough for the MVP; that was wrong.

Fits: Mission 2 MVP, if Hiep accepts.
Reopens: M4 (one topic per document), M1a (the "complete on its topic" rule), and the deferred "multi-topic documents" idea.
Status: `covers` rejected by Hiep (M14): it needs a label on every chunk and does not work on unstructured documents.
Adopted instead: one `topic` per document plus a `complements` relation between series, declared once per pair by the owner, and a publish-time check (M15).
`covers` is kept below as history and parked in Deferred ideas.

### P5 - Per-key inheritance moves the risk to wrong tagging - Medium

P4 has a cost that must be stated honestly.
If GameCo's policy covers carry-over but the owner forgets to tag `nghi_phep.chuyen_phep`, the Group rule answers that question for GameCo staff, silently.
Under the current whole-document override this cannot happen.

Mitigations, all deterministic:

- **Effective rulebook preview at publish time.**
  The resolver runs for every unit and every key, and shows the owner which document answers each key for their unit.
  The owner confirms before publishing.
  It is the same function as the query-time resolver, run over the org tree instead of one person, so it adds no new logic.
- The same run flags every undeclared conflict (Hà's T7 case) before any employee meets it.
  This is the "publish-time conflict check" (X11 and D6), which becomes cheap once conflicts are per key.
- An AI may suggest extra keys from the text, and the owner confirms.
  It may only add keys, never remove them, consistent with the Round 3 principle "AI only where its mistakes are harmless".

Fits: the preview as a test script in Mission 2; the owner-facing screen is Deferred.

### P6 - Picking one topic from the top search hit is fragile - Medium

This is Issue 2.
If the top hit picks the wrong topic, the conflict check runs on the wrong set.

Fix: **resolve first, then search.**

1. Build the asker's effective rulebook: for each key, the winning document or the conflict set (P1, P3, P4).
2. Search only over the passages of that rulebook.
3. The keys of the top passages say which question is being answered.
4. The answer card shows "Bạn đang hỏi về: ..." so a wrong guess is visible, and asks the user to choose when the top keys are close.

Effects:

- Near-duplicate versions can no longer crowd the results, because they are removed before search (this completes the M3b argument).
- A ranking mistake changes which question gets answered, never which document wins for that question.

Real-world practice: vector databases warn that filtering after the vector search can return few or no results even when relevant records exist (Pinecone [S4], Weaviate [S9]).

Fits: Mission 2 MVP.
Consistent with Hiep's Issue 4 order (relations before search).

### P7 - `applies_to` is a single unit name - Low

Real policies often cover several units or exclude one ("toàn Tập đoàn, trừ PayCo").
Unit names also change in a restructure, which is a likely Mission 3 change.

Fix: `applies_to` as a list of stable unit ids, with an optional `exclude` list.
Employment type (deferred in M0) later becomes one more attribute in the same condition.
This is attribute-based applicability, the same shape as ABAC for access (NIST SP 800-162 [S10]), but it stays a separate field from `access`.

Fits: Mission 2 MVP (data shape only).

### P8 - The second user (HR) cannot do their job - Medium

F2 makes the document owner (HR) the second user.
M3a only allows questions about the asker's own rules, so Lan cannot ask "What is GameCo's leave rule?", which is the question HR answers all day.

Option: an explicit "Hỏi cho: [Tôi | đơn vị khác]" selector.
The user picks the target unit from units whose documents they may read.
The resolver runs with that unit path, and access is still checked against the asker.
No AI guesses the target, so M3a's reason (AI stays out of correctness) still holds.

Fits: Hiep decides between "MVP feature" and "known limitation, one line in the document".
Reopens: M3a.
Status: Hiep chose "known limitation", recorded as M13; the selector is in Deferred ideas.

### P9 - Access is typed by hand per document - Low, Deferred

Production systems take permissions from the source system and check them for the signed-in user at query time (Microsoft 365 Copilot [S2], Glean [S3]).
The MVP's hand-typed `access` field is fine for simulated data.
One line in the risks: "in production, access comes from the source system's ACLs, never re-typed".

## What is already right

These choices match production practice, and the sources support them in the PITCH:

| Choice | Support |
|---|---|
| Access, validity and applicability filtered before search (M3b) | Pinecone [S4] and Weaviate [S9] document the empty-result risk of filtering after search |
| Access enforced outside the LLM, for the signed-in user | Microsoft 365 Copilot [S2] and Glean [S3] scope retrieval to the user's permissions |
| As-of date as an input (M6) | Effective dates are stored separately from the date of entry (Workday [S6]) |
| A real conflict is shown, not silently resolved (M1b) | Real conflicts and complementary information are separate categories [S1] |
| Identical reply for "not allowed" and "not found" (M7) | No source checked; it is a design argument, keep it as one |

## Proposed changes to the data

P1-P3 rows applied to `artifacts.md` on 07/10/2026 (M9-M11).
The `topic` row was replaced by M14 (`complements`, applied); the `applies_to` row is not applied.

| Field | Now | Proposed | Finding |
|---|---|---|---|
| `series` | (none) | e.g. `LEAVE-GAMECO` | P1 |
| `replaces` | typed by hand | derived from series and dates; display only | P1 |
| `effective_to` | set on v2 | empty unless the document is temporary | P2 |
| `overrides` | version id | series id | P3 |
| `topic` | one value | `covers`: list of keys under a topic | P4 |
| `applies_to` | one unit name | list of unit ids, optional `exclude` | P7 |

Minh's trace now starts with "current version per series" (applied); with `covers`, Step C would also use `overrides` per key.
His answer stays `LEAVE-GAMECO-v2`, 14 days.

## Suggested priority

| Priority | Findings | Why |
|---|---|---|
| Before submitting Mission 1 | P1, P2, P3 | The current artifacts fail on their own planned date, and Answer 3 is about exactly this ("khác phiên bản") |
| Mission 2 MVP, if accepted | P4, P6, P7, P5 as a test script | Fixes false conflicts and the fragile topic step with data changes and one resolver |
| Known limitation (M13) | P8 | Stated in the risks section; the selector is deferred |
| Deferred ideas | ACL sync, mandatory parent rules, owner preview screen, AI-suggested keys | Real production needs, not needed to prove the core |

## How `covers` changes the pipeline (history, not adopted: see M14)

Written for Hiep's question: what exactly changes if conflicts are checked per question instead of per topic.
All examples are simulated ("giả lập").

### What does not change

- Step A (current version per series, M9) and Step B (access and applicability filters) stay exactly as they are.
- `overrides` still names a series (M11), and a declared relation is still the only way one document beats another.
- Same question, two applicable documents, no relation: still a conflict (M1b).
- Refusal is still one identical reply (M7), and the AI still only writes from what the rules picked.

### What changes, step by step

| Step | Now (M12) | With `covers` |
|---|---|---|
| Data | Each document has one `topic`; an overriding document must be complete on its topic (M1a) | Each Điều has one key from a short controlled list, e.g. `nghi_phep.so_ngay`; a document covers the keys of its Điều; no completeness rule |
| C - relations | A whole document is removed if a kept document overrides its series | Per key: a Điều is removed only if a kept document that overrides its series has a Điều with the same key |
| New: rulebook | - | For each key, the result is one winning Điều or a conflict set; this is the asker's "effective rulebook" |
| D - search | Over the whole documents left; output: one topic | Over the rulebook's Điều only; output: the key or keys the question asks about |
| E - conflict | Two or more documents left with the same topic | The key that was asked has a conflict set |
| Answer | From exactly one document | One Điều per key asked; an answer may cite several documents |
| Refusal | No document left for the topic | No rulebook Điều matches the question |

### Why the key sits on the Điều, not on the document

Search has to say which question is being asked.
`LEAVE-GAMECO-v2` answers two questions (how many days, how to apply), so a hit on the document does not say which one.
A key on each Điều makes the key part of what search returns, and the citation points at the exact Điều.
A Điều with no policy content (for example "Quy chế này thay thế quy chế của Tập đoàn...") gets no key and is never an answer.
In the simulated data this is about 20 Điều to tag.
`checks/proposed_rules.py` tags whole documents to keep the demo short; the resolver logic is the same if each Điều is treated as a small document with its parent's metadata.

### Minh's question with `covers`

As of 07/10/2026, after Steps A and B (unchanged):

| Key | Điều left after Step B | Relation | Rulebook entry |
|---|---|---|---|
| `nghi_phep.so_ngay` | `LEAVE-GROUP-v1` Điều 1, `LEAVE-GAMECO-v2` Điều 2 | `LEAVE-GAMECO` overrides `LEAVE-GROUP` | `LEAVE-GAMECO-v2` Điều 2 |
| `nghi_phep.thu_tuc` | `LEAVE-GROUP-v1` Điều 2, `LEAVE-GAMECO-v2` Điều 3 | Same | `LEAVE-GAMECO-v2` Điều 3 |
| `lam_them_gio.phe_duyet` | `OT-GAMECO-v1` Điều 1 | - | `OT-GAMECO-v1` Điều 1 |
| `lam_them_gio.nghi_bu` | `OT-GAMECO-v1` Điều 2 | - | `OT-GAMECO-v1` Điều 2 |
| `cong_tac_phi.an_uong` | `TRAVEL-GAMECO-v1` Điều 1 | - | `TRAVEL-GAMECO-v1` Điều 1 |
| `cong_tac_phi.di_lai_khach_san` | `TRAVEL-GAMECO-v1` Điều 2 | - | `TRAVEL-GAMECO-v1` Điều 2 |

Search for "Phép năm của tôi là bao nhiêu ngày?" runs over these 6 Điều only.
The Group's near-identical "12 ngày" Điều is not in the search at all, so it cannot outrank the right one.
The top hit is `LEAVE-GAMECO-v2` Điều 2, key `nghi_phep.so_ngay`: 14 days, the same answer as today, now citing the Điều.

### Where the two pipelines give different results

| Case (giả lập) | Now | With `covers` |
|---|---|---|
| GameCo adds "Quy trình đăng ký nghỉ trên hệ thống HR", key `nghi_phep.dang_ky_he_thong` | Every leave question becomes a conflict | New key, no conflict; "Phép năm?" is unaffected |
| PayCo changes only carry-over, in an addendum with key `nghi_phep.chuyen_phep` that overrides `LEAVE-GROUP` | Cannot be expressed | Carry-over from the addendum; every other leave key still from the parent |
| "Tôi được mấy ngày phép và xin nghỉ thế nào?" | One topic, one document | Two keys, two Điều, one answer with two citations |
| A handbook (Nội quy) with Điều on leave and on OT | Not allowed (one topic per document, deferred) | Works: each Điều has its own key |

### New risks and how each is handled

1. **A Điều with the wrong key or no key** (P5): the parent answers that question silently.
   Deterministic checks catch the two common slips: a Điều with policy content but no key, and two Điều in one document with the same key.
   The rulebook script, run for every unit, shows which document answers each key, and test cases cover the expected winner.
2. **A question nobody covers** (for example maternity leave): search may return the closest Điều, such as `nghi_phep.so_ngay`, and answer the wrong question.
   This risk exists today as well (the topic step has the same weakness).
   Mitigations: a similarity threshold below which the reply is the refusal, and the label "Bạn đang hỏi về: Số ngày phép năm" on every answer card so a mismatch is visible.
   An optional AI check "does this Điều answer the question?" may only turn an answer into a refusal, never the reverse.
3. **The key list itself.** Too coarse brings false conflicts back; too fine and owners cannot choose.
   Start with 2-4 keys per topic, owned by Group HR; adding a key is a data change, not code.

### Cost for Mission 2 (Claude estimate, not measured)

- Data: one key per Điều (about 20) and a key list of about 10 entries.
- Code: the resolver loops over keys instead of documents (about the same size as today); the search index is built per Điều, which Điều-level citations need anyway; the answer card shows the key label.
- Tests: about 4 more cases (complementary document, addendum, two-key question, uncovered question).
- About half a day on top of the current plan.
  Per `AGENTS.md`, that is at the threshold where Hiep should decide explicitly.

### Decisions this would reopen

- M4: one `topic` per document becomes one key per Điều; `topic` remains as the parent of the keys.
- M1a: the "complete on its topic" rule is dropped.
- Deferred idea "multi-topic documents": no longer needed as a separate feature.
- Issue 2: the key comes from search over the rulebook, not from the top document.
- Answer 3: gains the "complementary" case (next section).

## How real products keep knowledge consistent (verified sources)

Researched at Hiep's request ("In real production applications what are the best processes that people often use?").
Found by Agnes 2.5 Flash (max reasoning), then checked by a second Agnes pass that fetched each page.
Only claims that passed the check are listed; dropped claims are listed at the end of this section.

### Processes found

| # | Process | Who does it | Sources |
|---|---|---|---|
| 1 | Every document has a named owner or verifier and a review interval; the owner re-confirms it or updates it | Owner, on a schedule | Guru [S11], NAVEX PolicyTech [S16], Confluence [S17], Glean [S12] |
| 2 | A trust status set by people: Verified, Deprecated, Not Validated, Archived | Owner or admin, never the reader | Glean [S12], Confluence [S17], KCS [S14] |
| 3 | A newer version makes the old one outdated; old versions stay for audit but leave search | System, from versioning | ServiceNow [S18, weak], KCS [S14] |
| 4 | Duplicate detection: the system scans for similar content and flags it for a person to review | System flags, person decides | Guru [S11] |
| 5 | True duplicates are merged into one document, not kept side by side | Owner | KCS [S15], Glean [S13] |
| 6 | Some sources are marked as official, which the AI search uses as a trust signal | Admin | SharePoint authoritative sites [S19] |
| 7 | An edit by someone who is not the verifier removes the Verified status until the verifier checks it | System | Guru [S11] |

### What this means for our design

- **The industry fixes conflicts mostly before the question is asked.**
  Every process above acts on the content (owner, review, duplicates, status), not on the answer.
  In the documents checked, no feature was found that decides automatically between two conflicting documents at question time.
  This is an observation from the pages checked, not a proven fact about all products.
- **Our relations match process 4 and 5, if they are declared at publish time.**
  When a document is published, the system lists existing documents on the same topic that apply to the same units, and the owner chooses one: new version of the same series (M9), `overrides` (M11), `complements` (proposed), or duplicate (merge, then archive one).
  The query-time conflict check stays as the safety net for anything not declared.
- **Process 1 answers the staleness problem of `overrides` and `complements`.**
  The owner re-confirms the relations during the periodic review, instead of a special notice for each change.
- **Our design is stricter than general search products on purpose.**
  They use status and authority to rank results and show citations.
  We use access, validity and declared relations as filters, because the brief asks for the rule that applies to this person, not the most trusted document in general.

### Fits

| Item | Mission 1 document | Mission 2 MVP | Deferred |
|---|---|---|---|
| Publish-time triage (new version / overrides / complements / duplicate) | Describe the process in the "AI, dữ liệu & con người" section | A script that lists undeclared same-topic pairs per unit, run on the simulated data | Owner screen |
| `owner` on every document | Already in the data | Shown on the answer card | - |
| Review interval and re-confirmation | One line | - | Yes |
| Similarity scan for duplicates | One line | - | Yes |
| "Báo sai" button (reader flags a wrong answer) | Already planned | Already planned | - |

### Sources for this section

| ID | Source | Verified quote |
|---|---|---|
| S11 | Guru, "Verifying and unverifying cards", https://help.getguru.com/docs/verifying-and-unverifying-cards ; Guru, "Duplicate detection", https://www.getguru.com/features/duplicate-detection | "Guru automatically reviews your account every Monday once you've published over 100 Cards. It compares content using a similarity threshold of 90% to identify potential duplicates." The help page names a verifier and a verification interval per Card; the exact sentence on non-verifier edits is a paraphrase |
| S12 | Glean, "How verification works", https://docs.glean.com/user-guide/knowledge/verification/how-verification-works | "Verify and deprecate documents from there to help your users work from current information." |
| S13 | Glean Community, https://community.glean.com/en/public/resources/why-do-results-improve-after-we-clean-up-source-data-2026-04-23 | "Deduplication reduces ambiguity. When there are fewer competing versions of the same information, the system is less likely to split authority across multiple near-identical docs or surface an outdated copy." (community page, not product docs) |
| S14 | KCS, Technique 5.2 Article State, https://library.serviceinnovation.org/KCS/Knowledge-Centered_Success_Practices_Guide/301-Evolve_Loop/Practice_5_Content_Health/Technique_5.2 | States: Work in Progress, Not Validated, Validated, Archived. "Efficiency - Let reuse of Not Validated articles be the review and drive the article life cycle." |
| S15 | KCS v6 Practices Guide, https://www.serviceinnovation.org/included/docs/KCS_v6_Practices_Guide_2023_06_08.pdf | "When duplicate articles are discovered they should be merged." |
| S16 | NAVEX PolicyTech help, https://help.navexglobal.com/pt/content/admin%20topics/adm_defaultcontentpropsgen.htm | "The default is every 12 month(s) from last reviewed date." |
| S17 | Atlassian Community, Confluence verified pages, https://community.atlassian.com/t5/Confluence-articles/Verified-Pages-Now-Available-in-Confluence/ba-p/2664827 | "only page owners or space/site admins will be able to place and remove this status from any given content." |
| S18 | ServiceNow docs mirror on GitHub, https://github.com/ServiceNow/ServiceNowDocs/blob/australia/markdown/servicenow-platform/knowledge-management/article-versioning-changes.md | "The Workflow column includes the new Outdated state." The live docs pages could not be loaded, so treat this as weak |
| S19 | Microsoft Learn, SharePoint authoritative sites, https://learn.microsoft.com/en-us/sharepoint/sharepoint-authoritative-sites | "Authoritative sites help administrators identify official, organization-managed SharePoint sources." |

Dropped after the check: the Microsoft Copilot sentence that cited sources may disagree (not on the page), Azure AI Search near-duplicate detection (not on the page), ServiceNow "Valid to" hiding articles from search (page not reachable; snippets only).

## A sharper Answer 3 (Claude draft, for discussion)

Updated after M14 and M15.
After the filters (access, in force, applies to the asker), every pair of documents left on the asked topic falls into exactly one case:

1. Same series, different versions: the version in force on the as-of date wins; older versions are superseded automatically.
2. Different series, declared `overrides`: the narrower unit's document is used instead of the broader one.
3. Different series, declared `complements`: both are used, each statement cited to its own document.
4. Different series, no declared relation: a real conflict; quote both, warn, route to the owner.

The owner declares the relation once, at publish time, when the check lists the new pair; the AI never decides the case.
Case 3 is the one the original rules got wrong (a false conflict).

## Sources

Found by Agnes 2.5 Flash (max reasoning), then checked by a second Agnes pass that fetched each URL and compared the quotes word for word.
Claude did not open these pages itself.
Hiep should open each link before quoting it in the document or the PITCH.

| ID | Source | Verified quote | Check |
|---|---|---|---|
| S1 | "DRAGged into Conflicts: Detecting and Addressing Conflicting Sources in Search-Augmented LLMs", Google Research, 2025, https://arxiv.org/abs/2506.08500 | "The retrieved documents provide answers to the query that refer to different real-world concepts but are mutually compatible, meaning that a single person can reasonably agree with all of them simultaneously." | Verbatim. The two passes disagreed on the first author, so cite it by title |
| S2 | Microsoft Learn, "How does Microsoft 365 Copilot work", https://learn.microsoft.com/en-us/microsoft-365/copilot/microsoft-365-copilot-architecture | "Copilot only accesses data that an individual user is authorized to access, based on, for example, existing Microsoft 365 role-based access controls." | Verbatim (full sentence) |
| S3 | Glean, Security principles, https://docs.glean.com/security/security-principles | "Glean mirrors the access controls of every connected source system." | Verbatim |
| S4 | Pinecone, "The Missing WHERE Clause in Vector Search", https://www.pinecone.io/learn/vector-search-filtering/ | "Still, we risk returning very few or even zero results, even though there may be relevant records in the dataset." | Verbatim |
| S5 | Veeva Vault Help, document state types, https://quality.veevavault.help/en/lr/14560/ | State types include Starting, Steady, Superseded, Obsolete and Deleted | Names verbatim |
| S6 | Workday, "Concept: Effective and Entry Dates", https://doc.workday.com/admin-guide/en-us/reporting-and-analytics/custom-reports-and-analytics/set-up-reports/dan1370796621462.html | "Effective dates identify when changes go into effect, which might differ from when data entry occurs." | Verbatim |
| S7 | VersionRAG, https://arxiv.org/abs/2510.08109 | "VersionRAG achieves 90% accuracy, outperforming naive RAG (58%) and GraphRAG (64%)." | Numbers confirmed in the abstract; exact title not confirmed |
| S8 | Microsoft Learn, "Introduction to managed metadata", https://learn.microsoft.com/en-us/sharepoint/managed-metadata | "Term Store administrators organize managed terms into a hierarchical term set." | Verbatim |
| S9 | Weaviate, Filtering, https://docs.weaviate.io/weaviate/concepts/filtering | "... there is a chance that the original vector search does not contain any match at all." | Verbatim |
| S10 | NIST SP 800-162, https://csrc.nist.gov/pubs/sp/800/162/upd2/final | "ABAC is a logical access control methodology where authorization to perform a set of operations is determined by evaluating attributes associated with the subject, object, requested operations, and, in some cases, environment conditions ..." | Verbatim |

Dropped because they could not be verified: ISO 9001:2015 clause 7.5.3 (page blocked), SAP SuccessFactors effective dating (not rechecked), and "managed metadata columns allow multiple values" (not on the cited page).
