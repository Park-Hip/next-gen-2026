# System design - Tri thức nội bộ Appota

Status: draft by Claude (Opus 5.5), 20/10/2026, for Hiep to review.
Items marked **[to decide]** are open; every option marked "proposed" is Claude's proposal, not a decision.
All Appota data in this project is simulated ("giả lập").

## 0. How to read this document

This document describes how the whole MVP in [`mvp_spec.md`](mvp_spec.md) is built: the employee side, the document owner side and the system around them.
It is not limited to v1, and it is not limited to one mission.

| Document | Answers |
|---|---|
| [`mvp_spec.md`](mvp_spec.md) | What the MVP must do, and how it is tested |
| This document | How the system is built to do it: components, flows, data, decisions |
| [`architecture.md`](architecture.md) | How v1 answers one question, step by step, as built |
| [`scope.md`](scope.md) | What v1 simplifies, defers and gets wrong |
| [`decisions/`](decisions/README.md) | Why each design choice was made, and who made it |
| [`mission1/redraft/current_design.md`](mission1/redraft/current_design.md) | The Mission 1 design, frozen as the baseline |

Each component carries one of three markers against v1:

- **Built**: in v1 and unchanged by this design.
- **Changed**: in v1, but this design changes it.
- **New**: not in v1.

A choice with real alternatives is shown as **[to decide]** with its options; it is decided by Hiep, through a research issue when it needs one, and recorded in an ADR.
This document never gives the reasons for a decision on Hiep's behalf.

## 1. Scope

In scope, from the spec:

- An employee asks a question and gets an answer, a conflict notice or a refusal (spec 3.1).
- A document owner publishes documents and versions, declares relations and sees the state of the unit's documents (spec 3.2).
- The system keeps what was published, records every answer and runs in a browser in Vietnamese (spec 3.3).
- The evaluation of spec section 6, for both test questions and owner scenarios.

Out of scope: everything listed under "Deferred" in [`scope.md`](scope.md), such as real single sign-on, DOCX and PDF documents, multi-turn conversation and "Báo sai".
The inputs and their form are fixed by spec section 4; the assumptions A1-A4 of spec section 5 hold throughout.

The expected size is the size of the simulated data: tens of documents, a handful of simulated accounts and one server process.
No number in this document is a measurement unless it names its source.

## 2. Design goals and principles

### 2.1 Goals, in order of priority

When two goals conflict, the higher one wins.

| # | Goal | Requirements |
|---|---|---|
| G1 | Nothing from a document the asker may not read is used, shown or hinted at | E4, E8 |
| G2 | An answer comes only from the rule that applies to the asker on that date, or no answer is given | E2, E3, E5, S1 |
| G3 | When in doubt, refuse or flag, and name who to ask | S2, E6 |
| G4 | Every answer can be checked by the employee and traced afterwards | E7, S3 |
| G5 | Owners change the rules themselves, and the change reaches employees on its effective date | H1-H5, S4 |
| G6 | It runs in a browser, in Vietnamese, on free tiers | S5 |

### 2.2 Principles

| # | Principle | Where it comes from |
|---|---|---|
| P1 | **Rules before AI.** Which documents the asker may use is decided from document metadata, the asker's account and the date, before the question is read | Mission 1 design; [`architecture.md`](architecture.md) |
| P2 | **The AI only handles language.** It ranks passages and picks and quotes the clauses that answer; it never decides access, validity, applicability, precedence or the card | AGENTS.md product rules |
| P3 | **No AI text on a card.** The answer card shows the quote that the rules verified; the conflict and refusal cards use fixed wording. **[to decide]**: E1 asks for an answer "in plain Vietnamese that answers it directly", which a quote does not always give; changing this needs a new ADR that supersedes ADR 0009 (SD14) | ADR 0009 |
| P4 | **Access never decides precedence.** A document the asker may not read still replaces its series | ADR 0010 |
| P5 | **The system never chooses between undeclared policies.** Only a relation an owner declared resolves two policies on the same topic | Mission 1 design; E5, H2 |
| P6 | **Fail closed.** A failed check gives a refusal or an error page, never a card | S2 |
| P7 | **One path for the page and the evaluation.** Both call the same ask function, so the evaluation tests what employees get | v1 (`services/ask.py`) |
| P8 | **Published is permanent (proposed).** A published version is never edited or deleted; a change is a new version | S4 |

## 3. System context

```mermaid
flowchart LR
    employee([Employee])
    owner([Document owner])
    hr([HR contact of a unit])
    evaluator([Evaluator: Hiep, judges])

    system["Tri thức nội bộ Appota<br/>web app"]

    gemini[[Google Gemini API<br/>embeddings and answers]]
    host[[Host<br/>Render free web service today]]
    seed[("Simulated data<br/>in the repository")]

    employee -- "asks, reads the source" --> system
    owner -- "publishes, relates, checks state" --> system
    evaluator -- "runs test questions and owner scenarios" --> system
    system -- "names as the person to ask" --> hr
    system --> gemini
    system -- "runs on" --> host
    seed -- "organisation, accounts, first documents" --> system
```

| Outside the system | Role |
|---|---|
| Employee | Signs in as a simulated account and asks questions (spec 2) |
| Document owner | Signs in as a simulated owner account and manages the unit's documents (spec 2) |
| HR contact | Named on refusal and conflict cards; whether the HR contact also *receives* those questions is open (section 19) |
| Evaluator | Runs the evaluation and reads the results; in the demo, the judges |
| Gemini API | The only external service: embeddings for search, one LLM call per question |
| Host | Runs the one server process; its limits shape storage (section 11) |
| Simulated data | The organisation tree, accounts, first documents and test cases, kept in `data/` |

## 4. High-level design

### 4.1 Components

```mermaid
flowchart TB
    subgraph people[" "]
        direction LR
        employee([Employee])
        owner([Document owner])
        evaluator([Evaluator])
        employee ~~~ owner ~~~ evaluator
    end

    subgraph web["Pages"]
        direction LR
        askpage["Ask page<br/>(Changed)"]
        console["Owner console<br/>(New)"]
        guide["Data and<br/>test-case pages<br/>(Built)"]
        askpage ~~~ console ~~~ guide
    end

    subgraph sessionbox[" "]
        direction LR
        session["Sign-in and session<br/>(New)"]
        evalh["Evaluation harness<br/>(Built; owner scenarios New)"]
        session ~~~ evalh
    end

    subgraph answering["Answering a question"]
        direction LR
        scoperules["Scope rules<br/>(Built)"]
        search["Hybrid search<br/>(Built)"]
        answerer["Answerer, LLM<br/>(Built)"]
        checks["Answer checks<br/>and card (Built)"]
        tracer["Trace recorder<br/>(New)"]
        scoperules --> search --> answerer --> checks --> tracer
    end

    subgraph publishing["Publishing a document"]
        direction LR
        pubsvc["Publish service: authorize,<br/>validate, preview impact<br/>(New)"]
        chunker["Chunker<br/>(Built)"]
        pubsvc --> chunker
    end

    subgraph stores["Stores"]
        direction LR
        directory[("Directory<br/>org tree, HR contacts,<br/>accounts (Changed)")]
        registry[("Document registry<br/>versions, relations, history<br/>(Changed: persistent)")]
        index[("Search index<br/>all chunks of all versions<br/>(Changed: updated on publish)")]
        traces[("Trace store<br/>one record per question<br/>(New)")]
        directory ~~~ registry ~~~ index ~~~ traces
    end

    gemini[["Gemini API:<br/>embeddings, answers"]]

    people --> web
    web --> sessionbox
    sessionbox --> answering
    sessionbox --> publishing
    publishing -. "the preview uses<br/>the same scope rules" .-> answering
    answering --> stores
    publishing --> stores
    answering --> gemini
    publishing --> gemini

    classDef rule fill:#e8f5e9,stroke:#2e7d32,color:#1b1b1b
    classDef llm fill:#fff3e0,stroke:#ef6c00,color:#1b1b1b
    classDef new fill:#e3f2fd,stroke:#1565c0,color:#1b1b1b
    class scoperules,checks,chunker rule
    class search,answerer llm
    class console,session,pubsvc,tracer new
    style people fill:transparent,stroke:transparent
    style sessionbox fill:transparent,stroke:transparent
```

Green components are deterministic rules, orange components use an AI model, and blue components are new.
The arrows join layers; which component reads or writes which store is in section 11.1.

### 4.2 What each component does

| Component | Responsibility | Decided by | Requirements | Status | v1 code |
|---|---|---|---|---|---|
| Ask page | The question form, the three cards, and the cited clause | Rules render fixed or verified text | E1, E7, S5 | **Changed**: the asker comes from the session instead of the persona picker; the cited clause can be opened (section 8.5) | `api/page.py`, `api/templates/` |
| Owner console | The unit's documents with their state today, the publish form, drafts | Rules | H1-H4 | **New** | - |
| Data and test-case pages | Read-only views of the simulated data and of the committed evaluation run, calling no model | Rules | Evaluation | **Built**; visibility to decide (section 10.3) | `api/page.py`, `services/guide.py` |
| Sign-in and session | Turns a signed-in simulated account into the principal: unit, roles, owned unit | Rules | E8, H5 | **New**: v1 has a persona picker | - |
| Directory | The org tree, each unit's HR contact, the accounts | Data | E2, E6, E8 | **Changed**: accounts gain the unit they own | `data/org.yaml`, `data/personas.yaml`, `integrations/data_files.py` |
| Document registry | Every version of every document with its metadata, relations and publish events; only appended to | Data | H1, H2, S4 | **Changed**: files in the repository become a persistent store (section 11) | `data/documents/`, `integrations/data_files.py` |
| Publish service | Checks the owner may publish for the unit, validates the document, shows its impact, saves it and indexes it | Rules | H1, H2, H3, H5 | **New**; the load checks of v1 are its starting point | `integrations/data_files.py` (checks only) |
| Chunker | One chunk per "Điều", or per line for a document without "Điều" | Rules | E7 | **Built** | `services/chunking.py` |
| Search index | Every chunk of every version, with its embedding and its BM25 tokens | Data | E1 | **Changed**: built at start-up in v1; also updated on publish | `services/retrieval/index.py` |
| Scope rules | The documents the asker may use on the date: in force, applying to the asker's unit, not replaced, readable by the asker; and the conflict pairs | Rules | E2-E5 | **Built** | `services/scope.py` |
| Hybrid search | Ranks only the asker's chunks by BM25 and embeddings, fused by RRF, and raises an error on any chunk outside the scope | AI ranks, rules guard | E1, E4 | **Built** | `services/retrieval/` |
| Answerer | One LLM call that cites only retrieved chunk ids and quotes each clause word for word, or returns nothing | AI | E1, S1 | **Built** | `services/answering/`, `integrations/gemini.py` |
| Answer checks and card | Verifies every citation and quote, picks the answer, conflict or refusal card, and fills in its fixed wording | Rules | S1, S2, E5, E6, E7 | **Built** | `services/citations.py`, `services/card_text.py` |
| Trace recorder | One record per question: who, when, scope, retrieved passages, raw model reply, checks, card | Rules | S3 | **New**: v1 has JSON log lines on standard output and the evaluation's JSONL files | `evaluation/run.py` (record shape) |
| Evaluation harness | Runs the test questions through the ask function and scores them; runs the owner scenarios | Rules, plus Hiep's reading | Spec 6 | **Built** for test questions; **New** for owner scenarios | `evaluation/`, `tests/` |

### 4.3 What stays and what is added

The answering half of the system is built and stays as it is: the scope rules, search, the answerer and the answer checks, with the guarantees described in [`architecture.md`](architecture.md).
The design adds three things around it:

1. **Who is asking comes from a signed-in account.** The rules already need only a unit and roles, so only the source of the principal changes.
2. **Owners publish through the system instead of editing files.** Publishing writes to a persistent registry and to the search index; the scope rules read the registry instead of `data/documents/`.
3. **Every answer leaves a record.** The page writes the same kind of record the evaluation already writes.

The answering half never writes and the publishing half never answers, so they meet only in the registry and the index.

## 5. Main flows

### 5.1 An employee asks a question

```mermaid
sequenceDiagram
    actor E as Employee
    participant P as Ask page
    participant S as Session
    participant R as Scope rules
    participant H as Hybrid search
    participant A as Answerer
    participant G as Gemini
    participant C as Answer checks
    participant T as Trace recorder

    E->>P: question
    P->>S: who is signed in?
    S-->>P: unit, roles
    P->>R: unit, roles, date
    Note over R: reads the registry and the directory,<br/>never the question
    R-->>P: the asker's scope and conflict pairs
    P->>H: question, scope
    H->>G: embed the question
    H-->>A: top chunks, all inside the scope
    A->>G: chunks, asker's unit, question
    G-->>A: points: cited chunk ids and quotes
    A->>C: retrieved chunks, points
    C-->>P: answer, conflict or refusal card
    P->>T: the record of this question
    P-->>E: the card
```

- The question first enters at search; everything before that is the same for every question the same asker asks on the same date.
- The date is today in Vietnam in production; the demo and the evaluation set it on purpose to show a version change (section 10.4).
- The internal order of the rules and checks is described in [`architecture.md`](architecture.md#the-7-steps).

### 5.2 An owner publishes a document or a new version

```mermaid
sequenceDiagram
    actor O as Owner
    participant K as Owner console
    participant S as Session
    participant U as Publish service
    participant R as Scope rules
    participant X as Chunker and index
    participant D as Registry

    O->>K: new document, or new version of a series
    K->>S: who is signed in?
    S-->>K: owner of unit U
    O->>K: text, dates, applies to, may read, topic, relations
    K->>U: the draft
    U->>U: authorize: issuing unit is U, applies within U
    U->>U: validate: fields, clauses, versions, relations
    U->>R: impact: scopes and conflict pairs before and after
    R-->>U: what changes, for which units, from which date
    U-->>K: errors, or the impact preview with its warnings
    O->>K: confirm
    K->>U: publish
    U->>X: chunk and embed the new version
    U->>D: append the version and the publish event
    U-->>K: published, in force from its effective date
```

- Errors block publishing; warnings are shown and the owner decides (section 9.4).
- The new version is indexed before it is saved, so the registry never names a chunk that the index does not have (proposed; section 5.6).
- Saving a draft runs the same checks except the impact preview, and never reaches employees.

### 5.3 An owner checks the state of the unit's documents

The owner console lists every series of the owner's unit with each version and its state today: draft, published but not yet in force, in force, replaced, or ended.
The state comes from the same rule function that decides validity for employees, so the console cannot disagree with what employees are told (proposed).
In v1, the "Dữ liệu giả lập" page computes these states in `services/guide.py`, separately from the rules.

### 5.4 An effective date arrives

Nothing runs on that day.
Which version is in force is computed for every question from the date, and the version was indexed when it was published, so the new rule reaches employees from its effective date and not before (H3).
The demo's answer cache is keyed by the scope's chunk ids, so a scope that changes with the date never reuses an old answer.

### 5.5 Start-up and restart

1. Load `config.yaml` through `core/config.py`.
2. Connect to the registry; if it is empty, load the simulated documents of `data/documents/` into it once (proposed).
3. Load the directory from `data/org.yaml` and the accounts file.
4. Build or load the search index **[to decide]**: v1 embeds every chunk at start-up; a persistent store could keep the vectors (section 11).
5. Load the committed evaluation run for the test-case page.

Any invalid data stops the start-up, so the deploy fails its health check instead of serving wrong answers, as in v1.
A restart must keep every published document and its history (S4, Owner scenarios).

### 5.6 When something fails

| Failure | What happens | Status |
|---|---|---|
| Gemini fails after retries, or the rate limit is reached | The page shows "Hệ thống tạm thời không trả lời được..." and no card; the trace records the error | Built (trace New) |
| Search returns a chunk outside the scope | `ScopeLeakError`; no card | Built |
| A chunk of the scope is missing from the index | Search raises an error naming the chunk; no card | Built |
| The model's output is malformed, cites nothing, cites outside what was retrieved, or quotes text not in the cited chunk | Refusal card | Built |
| A publish fails validation | Nothing is saved; the console shows the errors | New |
| Indexing fails during a publish | Nothing is saved; the owner retries (proposed: index first, then save) | New |
| The registry is unreachable | Error page for questions and publishing; never an answer from stale data (proposed) | New |

## 6. Data model

### 6.1 Entities

```mermaid
erDiagram
    UNIT ||--o{ UNIT : "parent of"
    UNIT ||--o{ ACCOUNT : "employs"
    UNIT |o--o{ ACCOUNT : "owned by"
    UNIT ||--o{ SERIES : "issues"
    SERIES ||--|{ VERSION : "has"
    VERSION ||--|{ CHUNK : "split into"
    VERSION }o--o| SERIES : "replaces (dùng thay)"
    VERSION }o--o{ SERIES : "adds to (bổ sung)"
    VERSION ||--|{ PUBLISH_EVENT : "recorded by"
    ACCOUNT ||--o{ PUBLISH_EVENT : "performs"
    ACCOUNT ||--o{ TRACE : "asks"
    TRACE }o--o{ CHUNK : "retrieved and cited"
```

| Entity | What it is | Status |
|---|---|---|
| Unit | A node of the fixed org tree, with an optional HR contact; a unit without one uses the nearest unit above | Built |
| Account | A simulated person: name, unit, roles, and the unit they own if they are an owner | Changed: v1 personas have no owned unit and no sign-in |
| Series | One document across its versions, issued by one unit | Built, as the `series` field |
| Version | One edition of a series with its metadata and text; what v1 calls a document | Built |
| Relation | "Dùng thay" or "bổ sung" from a version to another series | Built, as fields of a version |
| Chunk | One "Điều" of a version, or one line of a document without "Điều" | Built |
| Publish event | Who published or saved which version, and when | New |
| Trace | The record of one question (section 12) | New |

### 6.2 The information an owner sets for each document

This section answers the first open question of the spec (section 4): the exact list.
The list below is v1's metadata plus the fields publishing needs; it is a proposal **[to decide]**.

| Field | Meaning | Set by | v1 |
|---|---|---|---|
| `id` | The version's identifier | The system, from the series and a version number (proposed) | Typed by hand |
| `series` | The document across versions | The system: a new series, or the series the owner chose to add a version to | Typed by hand |
| `title` | The title shown on the card | Owner | Same |
| `issuer` | The unit that issues the document | The system: the owner's unit (proposed) | Not a field; `owner` holds the HR contact's name |
| `topic` | One subject from a fixed list, used only to find conflict pairs | Owner, from the list **[to decide: who maintains the list]** | Same, free text |
| `status` | `draft` or `published` | Owner, by saving or publishing | Same |
| `effective_from` | The first day it is in force | Owner | Same |
| `effective_to` | The last day, only when the rule really ends | Owner, optional | Same |
| `applies_to` | The unit it applies to, with every unit below it | Owner, within the owner's unit | Same |
| `access` | Who may read it: all staff, one unit, or some roles; never who it is for (ADR 0010) | Owner | Same |
| `overrides` | The series it is used instead of, for the units it applies to ("dùng thay") | Owner | Same |
| `complements` | The series it adds to without contradicting them ("bổ sung") | Owner | Same |
| `published_by`, `published_at` | Who published it, and when | The system | New |
| Body | Markdown text, each clause on its own line starting with "Điều n." | Owner | Same |

### 6.3 Checks when publishing

**Errors** stop the publish; the first group already stops v1's start-up (`integrations/data_files.py`, `services/chunking.py`).

| Check | v1 |
|---|---|
| `status` is `draft` or `published`; `access` has a known form | Built |
| `effective_to` is not before `effective_from` | Built |
| No two published versions of a series start on the same day | Built |
| `overrides` does not name its own series, and no chain of overrides forms a cycle | Built |
| `overrides` and `complements` name series that exist | Built |
| The body does not mix "Điều" lines with plain lines, and repeats no "Điều" number | Built |
| The issuing unit is the owner's unit, and `applies_to` is that unit or a unit below it (H5) | New |
| The roles and units in `access` exist | New |
| A published version may not start before today **[to decide]**; otherwise a publish rewrites what employees were told in the past | New |
| `overrides` may name only a series of a unit above the issuing unit **[to decide]** | New |

**Warnings** are shown in the impact preview, and the owner decides:

- A new conflict pair: a document on the same topic applies to some of the same units and no relation is declared, so those employees will get the conflict card.
- A new version that fewer people may read than the version it replaces: by ADR 0010, the employees who lose access get a refusal, not the older rule.
- A version that replaces another series takes away every clause of that series for the units it applies to ([#24](https://github.com/Park-Hip/next-gen-2026/issues/24)).

### 6.4 The life of a version

```mermaid
stateDiagram-v2
    [*] --> Draft: saved
    Draft --> Published: published
    Published --> InForce: effective_from arrives
    InForce --> Replaced: a later version comes into force
    InForce --> Ended: effective_to passes
    Replaced --> [*]
    Ended --> [*]
```

Only "draft" and "published" are stored.
"Published but not yet in force", "in force", "replaced" and "ended" are computed from the dates of the series' versions and the date asked, so no job has to change them on the day.
How a mistake in a published version is corrected is open (section 9.5).

## 7. Scope rules

The rules are built and tested; [`architecture.md`](architecture.md#who-decides-what) gives each rule, its code and what happens when it goes wrong.
In short, for one account and one date:

1. Keep, per series, the published version in force on that date.
2. Keep the versions that apply to the asker's unit or a unit above it.
3. Drop the series that a kept version declares it is used instead of.
4. Keep what the asker may read; access comes last, so it never decides precedence (ADR 0010).
5. Mark as conflict pairs the kept documents on the same topic with no declared relation.

The full design changes the rules' inputs, not the rules:

- The documents come from the registry instead of `data/documents/`.
- The unit and roles come from the session instead of the persona picker.
- The publish service and the owner console call the same functions to preview impact and to show state, so there is one definition of "in force" and "applies" (proposed).

## 8. Search, answer and checks

### 8.1 Chunking and the index

- One chunk per "Điều", or per line for a document without "Điều"; a chunk's id is the version id and its number (`LEAVE-GAMECO-v2#2`).
- The text indexed is the document title followed by the chunk, for both BM25 and embeddings.
- The index holds every chunk of every version, including drafts, future and replaced versions; the scope is applied at search time, so a version needs no re-indexing when it comes into force.
- Changed: v1 embeds everything at start-up; in the full design, publishing adds the new version's chunks (section 5.2).

### 8.2 Search

- BM25 over Vietnamese syllables, with its statistics computed over the asker's scope only, and cosine similarity over `gemini-embedding-001`, fused by reciprocal rank fusion (ADRs 0001, 0002).
- The top 5 chunks go to the answerer (`retrieval.top_k` in `config.yaml`).
- Only chunks of the asker's scope are scored, and a final check raises `ScopeLeakError` on any other chunk.

### 8.3 The answerer

- One call to `gemini-3.5-flash-lite` at medium thinking (ADR 0008), with no sampling and with structured output.
- The model sees only the retrieved chunks, the asker's unit and the question.
- It returns `{points: [{chunks, quote}]}`: each point cites retrieved chunk ids, from an enumerated list, and quotes the clause word for word; or it returns no points (ADR 0003).

### 8.4 The checks and the card

- The whole answer is refused if the output is malformed, has no points, has a point with no citation, cites a chunk that was not retrieved, or quotes text that is not in a chunk it cites, after Unicode and whitespace folding.
- If a cited document is in a conflict pair, the card is the conflict card, quoting one clause per side chosen without reading meaning (ADR 0005).
- Otherwise the card is the answer card, showing the verified quotes, never a sentence the model wrote (ADR 0009).
- Every card starts with who the asker is asking as, and the answer card names the document, the "Điều", the effective date and the HR contact (E7).
- "Not allowed" and "not found" give the same refusal text (E4).

### 8.5 Reading the cited part (E7)

The spec asks that the employee "can read that part".
v1 shows the quote, which can be only part of a clause.
Proposed **[to decide]**: the answer card links to the full cited "Điều" of that version; the server checks that the chunk is in the asker's scope for that date before showing it, so the link cannot be used to read another document (section 13).

### 8.6 The demo cache

An in-process cache of the last 256 replies, keyed by the account, the scope's chunk ids and the question; the checks still run on every hit, and the evaluation never uses it.
In the full design the key uses the account id instead of the persona id.

## 9. Owner side

All of this section is **New**.
It covers H1-H5; approval workflows, notifications and periodic review stay deferred ([`scope.md`](scope.md#owners-and-workflow)).

### 9.1 What an owner can do

An owner owns exactly one unit, and may publish and see only that unit's documents (H5).
Whether an owner also sees the documents of units below their unit is open (section 17).

### 9.2 The owner console

| Page | Shows or does | Requirement |
|---|---|---|
| The unit's documents | Each series with its versions, each version's state today, its dates, who it applies to, who may read it and its relations | H4 |
| One version | The full text, its metadata and its publish events | H4, S4 |
| Publish | The form of section 9.3, then the impact preview, then confirm | H1, H2 |
| Drafts | Saved drafts, which employees never see | H1 |

### 9.3 Declaring relations (H2)

The owner should not have to know other units' series ids.
Proposed: when the owner picks a topic and the units the document applies to, the form lists the documents of other units on the same topic that also apply to some of those units, and for each one the owner chooses:

- **Dùng thay**: this document replaces it for the units it applies to.
- **Bổ sung**: this document adds to it without contradicting it.
- **Not declared**: the employees of those units will get the conflict card, and the preview says so.

The list is built by the scope rules from metadata only; no AI suggests a relation (P2, [`scope.md`](scope.md#owners-and-workflow)).

### 9.4 The impact preview

Before confirming, the owner sees, for each unit the document applies to, on today's date and on its effective date:

- which documents employees of that unit will use, and which ones leave their scope;
- the new conflict pairs;
- the warnings of section 6.3.

The preview shows only documents the owner may read, so it cannot reveal another unit's restricted document (proposed).
It partly mitigates [#50](https://github.com/Park-Hip/next-gen-2026/issues/50): a wrong topic or a wrong relation becomes visible before employees see it, but nothing proves the owner reads it.

### 9.5 Correcting a mistake **[to decide]**

Options:

- a) Only by a new version; the wrong version stays in force until the new one starts.
- b) Withdraw a version that is not yet in force, which keeps its record but removes it from the rules.
- c) Withdraw any version, including one in force, with the same record.

Whatever is chosen, the record of what was published and when is never deleted (S4).

## 10. Identity and authorization

### 10.1 Accounts

A simulated account has an id, a name, a unit, a set of roles, and optionally the unit it owns.
Accounts replace `data/personas.yaml`; Minh, Lan and Hà remain as employees, and one owner account is added per unit that issues documents (proposed).

### 10.2 Sign-in **[to decide]**

Options:

- a) A sign-in page lists the simulated accounts; the user picks one, and the server keeps the account id in a signed session cookie (proposed).
- b) Each simulated account has a password.
- c) Real single sign-on, which stays deferred ([`scope.md`](scope.md#simplified)).

In a and b the server reads the unit and roles from the account, never from the request or the question, which is what E8 requires.

### 10.3 Who may do what

Every check runs on the server for every request; hiding a button is not a check.

| Action | Employee | Owner of unit U | Evaluator |
|---|---|---|---|
| Ask a question | Yes | Yes, as an employee of their own unit | Through the evaluation harness |
| Open a cited clause | Only a chunk in their scope on that date | Same | Same |
| See unit U's documents and their state | No | Yes | **[to decide]** |
| Publish or save a draft for U | No | Yes | No |
| See the "Dữ liệu giả lập" page | **[to decide]** | **[to decide]** | Yes |
| See the "Tình huống kiểm thử" page | **[to decide]** | **[to decide]** | Yes |

The "Dữ liệu giả lập" page lists every document with its title, including restricted ones such as "Khung bậc lương GameCo".
That is right for judges looking at simulated data, but in a product where employees sign in it would break E4, which forbids even showing a document's title.

### 10.4 The as-of date

In production the date is always today in Vietnam.
v1 lets the user pick the date so that judges can see a version change without waiting for it.
Whether the signed-in demo keeps the date picker for everyone, only for the evaluator, or not at all is **[to decide]**.

## 11. Storage and persistence

### 11.1 What is stored

| Data | Written by | Read by | Survives a restart |
|---|---|---|---|
| Versions, their text and metadata, publish events | Publish service | Scope rules, owner console, data page | Required (S4) |
| Org tree and accounts | Nobody at run time: loaded from `data/` | Session, scope rules, cards | From the repository |
| Search index | Start-up and publish service | Search | Can be rebuilt from the versions |
| Traces | Trace recorder | Evaluator | Required (S3) |
| Evaluation runs | Evaluation harness | Report, test-case page | Committed to the repository, as in v1 |

### 11.2 Where it is stored **[to decide]**

The requirement that published documents survive a restart conflicts with today's host: by ADR 0004, a Render free web service loses its local files on every spin-down, restart or redeploy.
This needs a research issue and an ADR.
Options to research; none of their limits or prices has been checked for this document:

- a) A hosted Postgres database, such as Neon, Supabase or Render Postgres, the options ADR 0004 listed for "Báo sai" records; possibly with pgvector to keep the embeddings too.
- b) A SQLite file on a host with a persistent disk, which means changing host.
- c) Published documents committed to the GitHub repository through its API.
- d) Keep files and accept the loss, which fails S4 and the restart scenario.

Two questions follow from the choice:

- Whether the embeddings are stored or recomputed at every start-up; recomputing costs embedding calls on the Gemini free tier as documents grow.
- How two publishes at the same time are kept apart; with one process, a single lock is enough (proposed).

## 12. Traceability and observability

### 12.1 The trace record (S3)

Proposed: the page writes one record per question in the same shape the evaluation already writes in `results/*.jsonl`, so the same scoring and reading tools work on both.
The evaluation record today holds the run id, the asker, the date, the question, the status and error, the commit, the model, thinking level, embedding model and top k, the scope's documents, conflict pairs and chunks, the retrieved chunks and their text, the raw model reply, the points, the card and the latency.
The page's record adds a trace id, the account id instead of the persona, and whether the cache answered.

Open **[to decide]**:

- Whether the card shows the trace id, so an employee can quote it to HR.
- How long traces are kept; the questions are simulated now, but a real question can be personal.

### 12.2 Logs

v1 writes one JSON log line per search, per model answer and per page request on standard output; the design keeps them for operating the server, and the trace store becomes the record that S3 relies on.

### 12.3 Explaining a wrong answer

From a trace, the evaluator sees which documents the rules kept, which chunks search returned, what the model replied and which check decided the card, without calling any model.
Rescoring a saved run without calling the API already works for the evaluation (ADR 0006).

## 13. Security and privacy

### 13.1 How nothing outside the asker's rights gets out (E4, E8)

1. The scope rules remove what the asker may not read before the question is read.
2. Search scores only the scope's chunks, and raises an error on any other chunk.
3. The model sees only the retrieved chunks, so it cannot quote anything else.
4. The checks refuse any citation outside what was retrieved and any quote not in the cited chunk.
5. "Not allowed" and "not found" give the same refusal, so a refusal does not reveal that a document exists.
6. Unit and roles come from the account; a role claimed in the question changes nothing.

Tests already check that no restricted chunk reaches any asker's scope for every asker, every boundary date and every test question, and with seven trap edits to the data (`tests/services/test_scope.py`).

### 13.2 New surfaces this design adds

| Surface | Risk | Control |
|---|---|---|
| The cited-clause link | Opening a chunk id of another document | The server checks the chunk is in the asker's scope for that date (section 8.5) |
| The owner console | Reading or publishing for another unit | Server-side check of the owned unit on every request (section 10.3) |
| The impact preview | Showing another unit's restricted document | The preview shows only what the owner may read (section 9.4) |
| The data and test-case pages | Showing restricted titles to employees | Visibility to decide (section 10.3) |
| The session cookie | A forged account | Signed with a secret from the environment |
| Document text written by owners | Instructions to the model inside a document | The model's output can only cite and quote retrieved chunks, so at worst it gives a refusal or a real but unhelpful quote |

### 13.3 Secrets and data

- The Gemini key, the session secret and any database URL come from the environment only, never from `config.yaml` or the repository.
- The repository is public; all data is simulated.

## 14. Failure modes and limitations

The two failures that look like right answers matter most, because the employee cannot tell them from a right answer; the safe ones send the employee to HR.

| Failure | Looks like | Caught by | In this design |
|---|---|---|---|
| The model quotes a real clause in scope that does not answer the question | A right answer | Hiep's reading in the evaluation; the employee reads the quote and its source | Unchanged |
| An owner sets wrong metadata, such as a wrong topic or a wrong relation ([#50](https://github.com/Park-Hip/next-gen-2026/issues/50)) | A right answer | Nothing in v1 | Partly mitigated by the relation list and the impact preview (sections 9.3, 9.4) |
| A question about another period gets the rule in force on the date asked ([#53](https://github.com/Park-Hip/next-gen-2026/issues/53)) | A right answer | The evaluation | Unchanged; see section 18 |
| A company replaces only one clause of a Group policy, and the whole Group policy drops out ([#24](https://github.com/Park-Hip/next-gen-2026/issues/24)) | A refusal | The evaluation | A warning in the impact preview (section 6.3); clause-level relations stay deferred |
| Two policies in a conflict pair agree on the point asked, and the employee still gets the conflict card ([#52](https://github.com/Park-Hip/next-gen-2026/issues/52)) | A conflict notice | The evaluation | Unchanged |
| A question that needs a clause applied to a case is refused although the clause was found ([#51](https://github.com/Park-Hip/next-gen-2026/issues/51)) | A refusal | The evaluation | Unchanged |
| The registry or the host loses published documents | Answers from the old rules | The restart scenario | Depends on section 11.2 |

Each of the five issues stays open with the `limitation` label until it is fixed.

## 15. Deployment and operations

| Area | Today | Source |
|---|---|---|
| Host | A Render free web service in Singapore, auto-deploying from a Blueprint; it sleeps after 15 idle minutes and wakes in about a minute | ADR 0004 |
| Process | One uvicorn process; the index and the model clients are built at start-up, so invalid data or a missing key fails the health check | `main.py` |
| Models | `gemini-3.5-flash-lite` at medium thinking, `gemini-embedding-001` | `config.yaml`; ADRs 0002, 0008 |
| Limits | 12 requests a minute, 80% of the free-tier limit; 6 retries; 30 seconds per attempt; questions up to 300 characters | `config.yaml`; ADR 0008 |
| Secrets | `GEMINI_API_KEY`, set only in the Render dashboard | ADR 0004 |
| Configuration | Every tunable value in `config.yaml`, read only through `core/config.py` | AGENTS.md |

The full design adds a session secret and, depending on section 11.2, a database URL, both from the environment.
New `config.yaml` keys are added by the change whose code first reads them.

## 16. Evaluation

How each metric of spec section 6.2 is measured:

| Metric | How | Status |
|---|---|---|
| Right sources and right kind | Each test question's scope and card compared with its expected documents and kind; gate "Rules correct in every case" | Built |
| Leaks | Gate "Leaks", plus the exhaustive scope test of section 13.1 | Built |
| Unsafe answers | Gates on the card and on the raw model reply, confirmed by hand (ADR 0006) | Built |
| Faithfulness | Hiep reads every answer, statement by statement, in a review file next to the run | Built |
| Over-caution | At most 10% of the questions that expect an answer (`eval.over_cautious_max_share`) | Built |
| Readability | Read by a person; the criterion is open in the spec | **[to decide]** |
| Source shown | Each answer card names the document, the part, the version and its date, and the part can be opened | Changed: the card already names them; opening the part is section 8.5; whether this is checked automatically today is to be checked |
| Traceable answers | Every question has a trace with its scope, retrieved chunks and reply | New: v1 has this for evaluation runs only |
| Owner scenarios | Automated tests on fake models: publish, then ask before and on the effective date; publish for another unit and be stopped; see the state; restart and ask again | New |

Owner scenarios need no LLM to decide pass or fail, because the scope rules decide which documents an answer may use; they can run in `python -m pytest` with the fake embedder and the fake model the tests already use.

## 17. Decisions

### 17.1 Decisions already made

The ADRs in [`decisions/`](decisions/README.md) hold for the full design; the ones it relies on most are:

- ADRs 0001, 0002: search on LangChain core, with our own Vietnamese BM25, `gemini-embedding-001` and RRF.
- ADRs 0003, 0008, 0009: one model call that cites retrieved ids and quotes; the card shows the verified quote.
- ADR 0004: the host, and leaving "Báo sai" and the owners' page out of Mission 2; the owner console of this design reverses the second part and needs a new ADR.
- ADR 0005: the conflict card.
- ADR 0010: access is checked last.

### 17.2 Decisions this design needs

| # | Decision | Options | Needs research | Section |
|---|---|---|---|---|
| SD1 | Where published documents and traces are stored, and on which host | Section 11.2 a-d | Yes | 11.2 |
| SD2 | Whether embeddings are stored or recomputed at start-up | Store; recompute | With SD1 | 5.5, 11.2 |
| SD3 | How a user signs in | Section 10.2 a-c | No | 10.2 |
| SD4 | The information an owner sets for each document | Section 6.2 | No | 6.2 |
| SD5 | Who maintains the list of topics | Owners; one central owner; a fixed list in the data | No | 6.2 |
| SD6 | Whether a published version may start before today | Allow; refuse | No | 6.3 |
| SD7 | Which series `overrides` may name | Any; only a series of a unit above | No | 6.3 |
| SD8 | How a mistake in a published version is corrected | Section 9.5 a-c | No | 9.5 |
| SD9 | Whether an owner also sees and publishes for units below their unit | Own unit only; own unit and below | No | 9.1 |
| SD10 | Whether the card links to the full cited clause | Link; quote only | No | 8.5 |
| SD11 | Who sees the data and test-case pages, and the date picker | Everyone; evaluator only | No | 10.3, 10.4 |
| SD12 | Whether the card shows a trace id, and how long traces are kept | - | No | 12.1 |
| SD13 | Whether the HR contact receives unanswered questions or is only named | Section 19 | No | 19 |
| SD14 | Whether the answer card keeps showing only the verified quote, or also a sentence the model words | Keep ADR 0009; a worded answer shown with its verified quote | Possibly | 2.2, 8.4 |

## 18. Change readiness

Where a likely change lands, and what stays as it is.
The rows are candidates from the Mission 1 decisions and the deferred list, not commitments.

| Change | Lands in | Stays |
|---|---|---|
| A person in two units (kiêm nhiệm) | Accounts hold several units; the scope rules run once per unit, or the user picks the unit they ask for | Search, the answerer, the checks |
| A company replaces one clause of a Group policy ([#24](https://github.com/Park-Hip/next-gen-2026/issues/24)) | Relations point at chunks instead of series; the scope rules drop chunks instead of documents | Search, the answerer, the cards |
| Employment type or seniority decides applicability | A new field on versions and accounts, and one more rule in the scope rules | Everything after the scope |
| Questions about another period ([#53](https://github.com/Park-Hip/next-gen-2026/issues/53)) | The user picks the period, never the AI, and the scope rules run on that date | The rules themselves |
| DOCX or PDF documents | A parser in the publish service that produces the same chunks | Everything after chunking |
| A new kind of access rule | `allowed` in the scope rules and the publish checks | The order of the rules (ADR 0010) |
| Real single sign-on | The sign-in component only | The rules need only unit and roles |
| Many more documents | The index moves to a persistent vector store | The rules, the answerer, the checks |
| Another model | `config.yaml` and a new ADR | Everything else |
| "Báo sai" and the owners' records | A new record type in the registry's store and a page in the owner console | The answering half |

## 19. Open questions

- The exact information an owner sets for each document (spec section 4): proposed in section 6.2, decision SD4.
- The criterion for Readability (spec section 6.2).
- The spec's Users table says the HR contact "receives the questions of their unit's employees that the system cannot answer", but no requirement covers it: E6 only names who to ask.
  Either a requirement is added, with a way to forward questions, or the row is changed to say the HR contact is named (SD13).
- Decisions SD1-SD12 and SD14 of section 17.2.

## Appendix A. Requirements traceability

| Req | Components | Flow | Status | Tested by |
|---|---|---|---|---|
| E1 | Ask page, hybrid search, answerer | 5.1 | Built | Readability |
| E2 | Scope rules, directory | 5.1 | Built | Right sources and right kind |
| E3 | Scope rules, registry | 5.1, 5.4 | Built | Right sources and right kind |
| E4 | Scope rules, hybrid search, answer checks, card text | 5.1 | Built; new surfaces in 13.2 | Leaks |
| E5 | Scope rules, answer checks | 5.1 | Built | Right sources and right kind |
| E6 | Answer checks, card text, directory | 5.1 | Built | Right sources and right kind; Unsafe answers |
| E7 | Answer checks, card text, ask page | 5.1 | Changed (8.5) | Source shown |
| E8 | Sign-in and session, directory | 5.1 | New | Leaks |
| H1 | Owner console, publish service, registry | 5.2 | New | Owner scenarios |
| H2 | Owner console, publish service | 5.2, 9.3 | New | Owner scenarios |
| H3 | Registry, search index, scope rules | 5.4 | Changed (index updated on publish) | Owner scenarios |
| H4 | Owner console, scope rules | 5.3 | New | Owner scenarios |
| H5 | Sign-in and session, publish service | 5.2 | New | Owner scenarios |
| S1 | Answerer, answer checks | 5.1 | Built | Faithfulness |
| S2 | Answer checks, card text | 5.1, 5.6 | Built | Unsafe answers; Over-caution |
| S3 | Trace recorder, trace store | 5.1 | New | Traceable answers |
| S4 | Registry and its store | 5.2, 5.5 | Changed (11.2) | Owner scenarios |
| S5 | Pages | All | Built | Run through the web page |
