# Open issues - Mission 1 redraft

Purpose: gaps found while building the Phase 2 artifacts that are not yet resolved.
A later review agent should investigate these against real-world practice.
This file records issues only.
Decisions are made by Hiep and recorded in `decisions.md`.
All data referred to here is simulated ("giả lập").
Review findings for Issues 1, 2, 4 and 5 are in `production_review.md` (Claude draft, not decided).

## Issue 1 - Same topic, separate documents (false conflict)

Status: decided (M14, M15). One `topic` per document plus a `complements` relation between series; undeclared pairs are listed at publish time. `covers` was rejected. Case 2 is in the data as trap T11.
Found: Phase 2, Step 5 discussion.

### The problem

Rule 5 says: if two documents have the same `topic`, both apply to the asker, and neither declares a relation, the system reports a conflict.
This assumes that two documents with the same topic are alternatives to each other.
In real companies, two documents can share a broad topic without contradicting each other.

### Cases

| Case | Example | Current behaviour |
|---|---|---|
| 1. Different scopes that never overlap | Leave policy for Studio and for Marketing | Correct. Only one applies to a person, so there is no conflict. |
| 2. Same broad topic, different subject | "Quy chế nghỉ phép năm" and "Quy trình xin nghỉ phép", both tagged `nghi_phep` | False conflict. Both apply, same topic, no relation. |
| 3. Complementary levels | A Group policy plus a department guideline that adds detail | False conflict if both carry the same topic. |
| 4. A company changes one clause of the Group policy | GameCo changes only the carry-over rule | Not supported. This is the clause-level case deferred in M1a. |

### Why it matters

- It affects the whole system, because rule 5 and the topic field (M4) both depend on how coarse topics are.
- The failure is on the safe side: a warning instead of a wrong answer.
- It can still produce noisy warnings, which makes owners ignore them (the risk named in M1b).
- None of the four cases is in the current simulated data.

### Options discussed (none chosen)

| Option | Idea | Cost |
|---|---|---|
| A | State it as a known limitation. Define a topic as "one question a document answers", so owners pick narrow topics such as `nghi_phep_nam` and `quy_trinh_xin_nghi`. One line in the risks section. | No change to the MVP data. Relies on owners choosing topics well. |
| B | Add a trap to the data: a second GameCo document that complements v2. | One more document and path to defend. |
| C | Add a `complements` relation. | A new relation type that M1a decided not to support. Would go to Deferred ideas. |

### Questions for the review agent

- How do real document systems model "same subject, different document" versus "alternative versions of the same rule"?
- Is a flat, fixed topic list used in practice, or a hierarchy or tags?
- Who assigns topics in practice, and how often are they wrong?

## Issue 2 - How the topic of the question is decided

Status: decided (M18). No step decides the question's topic: the asker's rulebook and its conflict pairs are built without the question, the retriever returns chunks from that rulebook, and rules decide the outcome from the documents the LLM cites.
Found: Phase 2, Step 5 discussion.

The register (M3b, M4) says search "only finds the topic", but does not say how.

| Option | Idea |
|---|---|
| A | Run the query search over the documents that passed the filters, and take the topic of the top hit. |
| B | A language model classifies the question into the fixed topic list. |
| C | The user picks the topic from a list. |

Open risk: an ambiguous question could land on the wrong topic, and a conflict check run on the wrong topic would be wrong.

## Issue 3 - `status` (draft or published) is not from the brief

Status: accepted by Hiep as "our assumption, not from the brief".
Source: first appears in `playbook.md`.
The brief only says "tài liệu nào đang có hiệu lực" and mentions "nhiều phiên bản".
To check in real practice: whether real publishing workflows use a status separate from effective dates.

## Issue 4 - Order of relations and search

Status: decided by Hiep (Phase 2).
Relations (`replaces`, `overrides`) run after the filters and before search.
Search then only finds the topic among the winners.
The earlier order in the core model was filters, search, relations.
Recorded as M12 in `decisions.md`.

Constraint worth checking: relations only count among documents that passed the filters.
Otherwise a future version would delete the version in force, and a company policy would hide the Group policy from people it does not cover.

Update (M9-M11): counting `replaces` only among filtered documents let replaced versions come back (`production_review.md` P1).
`replaces` is now derived from the `series` before the asker's filters, and only `overrides` (between series) is counted after them.
Both constraints above still hold.

Update (M18): search no longer finds a topic.
The conflict pairs are marked per topic before retrieval, and retrieval returns chunks from the documents left.

## Issue 5 - `overrides` assumes complete documents

Status: known limitation (M1a kept). `covers`, which would have allowed partial overrides, was rejected in M14 and parked in Deferred ideas.
An overriding policy must be complete on its topic.
Real company policies often change only one clause.
To check in real practice: how companies actually layer a company policy over a group policy.

## Brief for the review agent

Goal: compare our assumptions, plan and artifacts with real production practice, while staying aligned with the brief.

Rules for the agent:

- The brief (`docs/competition/mission1_brief.md`) stays the source of truth.
  A real-world practice that contradicts it is noted, not adopted.
- Do not edit `decisions.md`, the brief, or any file under `docs/competition/`.
  Write findings to a new file and propose changes to Hiep.
- Scope discipline applies (see `AGENTS.md`).
  Every proposal must say whether it fits the Mission 1 document or the Mission 2 MVP, or goes to Deferred ideas.
- Do not invent research or statistics.
  Every claim about real practice needs a source that Hiep can verify.
- Hiep must be able to defend every change in the PITCH round.

Files to read: `AGENTS.md`, the brief, `redraft_plan.md`, `redraft/decisions.md`, `redraft/artifacts.md`, and this file.
