# Scope of v1

What v1 simplifies, what it leaves for later, and where it is known to fail, as three separate lists.
Every unit, person, document and number in this project is simulated ("giả lập").
How the pipeline works is in [`architecture.md`](architecture.md); each design choice since Mission 1 has an ADR in [`decisions/`](decisions/).

The Mission 2 brief asks for a small product that proves the most important part, not a production system.
v1 therefore builds the 7 steps end to end but keeps every part around them as simple as the demo allows.

## Simplified

v1 has these parts, in a form that is enough for a 3-day prototype on simulated data.
The production replacements are candidates named to show the direction; none of them was researched or decided, and none has an ADR.

| Area | v1 | Enough for v1 because | Production replacement (candidate, not researched) | Becomes necessary when |
|---|---|---|---|---|
| Identity | The visitor signs in as one of the simulated accounts (four employees and a judge) with one demo password shared by all, published in the README; the server reads the unit and roles from the account, never from the request, and there is no field to type a unit (ADR 0016) | The rules need only the asker's unit and roles, and the signed session gives exactly those | Company single sign-on, with unit and roles read from the HR system, never typed by the user | Real employees use it |
| As-of date | The ask page has a date picker, labelled as a demo control and defaulting to today in Vietnam | It lets judges see a version change (01/01/2027) without waiting for it | The server's date only; employees always get the rule in force today | Real employees use it |
| Documents | 10 Markdown files in `data/documents/`, with the metadata typed by hand in front matter | Small, readable, and every trap in the test set is visible in one file | The owners' document system, with DOCX or PDF parsing and a publish form where the owner sets the metadata and relations | Owners publish real documents |
| Chunking | One chunk per "Điều", or per line for the one procedure document; 25 chunks in total | Every simulated document is written one clause per line | A parser that follows the heading structure of real documents, including tables and long clauses | Real documents have long clauses, tables or no "Điều" numbering |
| Index | Every chunk embedded once at start-up into LangChain's `InMemoryVectorStore`; BM25 statistics computed per question over the asker's scope (ADRs 0001, 0002) | 25 chunks fit in memory and embed in one call at start-up | A persistent vector database, for example Qdrant or Postgres with pgvector | The documents no longer fit in memory, or start-up embedding takes too long |
| Storage | Files in the repository; nothing is written at run time | v1 keeps no user data and no records | A database for documents, metadata, relations and the records owners act on | "Báo sai" or conflict records must survive a restart |
| Cache and rate limiter | An in-process cache of the last 256 answers for the demo, never used by the evaluation; an in-process limiter at 12 requests a minute, 80% of the free-tier limit (ADR 0008) | One process serves the demo, and the Gemini free tier is the bottleneck | A shared cache and a model gateway that handles limits, retries and fallback models across processes | More than one process serves traffic, or the free tier is replaced |
| Observability | One JSON log line per search, per model answer and per page request, on standard output | Enough to trace one wrong answer back to its retrieved chunks and raw model output | An LLM tracing tool that keeps every step of every question, with alerts on refusals, conflicts and errors | Real traffic, where nobody reads logs line by line |
| Model | `gemini-3.5-flash-lite` at medium thinking for the answer and `gemini-embedding-001` for search, both on the Gemini free tier (ADRs 0002, 0008) | Free, and the test set passes its gates with it (see the [test report](test_report.md)) | A paid tier with a service agreement, with the model chosen by an evaluation on real questions | Real employees use it, or the free tier limits or retires the model |
| Hosting | A Render free web service in Singapore; it sleeps after 15 idle minutes and wakes in about a minute, by Render's documentation (ADR 0004) | Free, with no card, and it runs the same process as local development | An always-on instance on the company's infrastructure, possibly as a container image | Real employees use it, or a dependency needs system packages |
| Evaluation | 22 test rows, each asked once in its main wording; deterministic checks, plus Hiep reading each answer by hand (ADRs 0006, 0018) | The free tier allows about 500 answer calls a day, shared with the demo, and 22 answers can be read by hand | Hundreds of real questions, each asked several times and in several wordings, with context recall and a second reviewer | Real documents and real questions exist |

## Deferred

Ideas that v1 does not build, and the reason; none of them is promised.
New out-of-scope product ideas are added here.

### Answers and rules

| Idea | Why deferred | Revisit when |
|---|---|---|
| "Hỏi cho": the user picks another unit to ask about its rules | Detecting the target unit from the question would put AI into a correctness decision; v1 refuses other-unit questions instead | HR staff need to answer for other units; the unit is then picked by the user, never guessed by AI |
| Clause-level relations: a company replaces one clause of a Group policy and keeps the rest | "Dùng thay" works on the whole policy, which is simpler to declare and check; this is a known failure of v1 (see Known limitations) | A real company overrides only part of a Group policy |
| A question key per clause, so precedence and conflicts work per question | Needs a label on every chunk and fails on unstructured documents; "bổ sung" covers the common case | Clause-level relations are built |
| Answering a question about another period with that period's content ("năm ngoái tôi được bao nhiêu ngày?", "từ năm sau...") | Employees act under today's rule; in v1 the date is a test input, and the model never sees another version's content. The card says until when the version applies and what replaces it (ADR 0012) but does not answer with the next version's content (see Known limitations) | Employees need to check a past decision or plan across a version change |
| Announcing a version before it is published | A notice is built from published versions only, so a draft is never shown (ADR 0012); an announcement state between draft and published would need its own ADR | Owners want to announce changes ahead |
| Multi-turn conversation | Each question is answered on its own, so each answer can be checked on its own | Users ask follow-up questions |
| A document that applies only to some roles of a unit | `access` means only who may read a document, never who it is for (ADR 0010); applicability by role would need its own field | A real policy is written for some roles only |
| Employment type and seniority as dimensions of applicability | The brief names only unit, access and version | A real policy depends on them |
| Legal rules and legal minimums (Bộ luật Lao động) | Adds a relation type and facts that must be verified, without a new kind of trap | The assistant must check a policy against the law |
| A person in two units (kiêm nhiệm) | Not in the brief; needs a rule for choosing between companies | Real staff hold two positions |
| Documents with more than one topic, such as a workplace rulebook covering leave and overtime | Each simulated document has one topic, used only to find conflict pairs | Real documents cover several topics |
| A run-time check on the model's answer, by rules or a second model call | The issue decides against it: a rule catches a number but not a dropped condition, and a second model adds another thing to trust; Hiep reads every answer instead (ADR 0018) | The Faithfulness reading shows answers that mislead often enough to need a check |

### Owners and workflow

| Idea | Why deferred | Revisit when |
|---|---|---|
| "Báo sai" button on the answer card and its records | Adds little value to Mission 2 (Hiep, 13/10/2026), and records would not survive a restart on the free host (ADR 0004) | Real employees use it; records then go to a database |
| Owners' page listing conflict and "Báo sai" records | Dropped with "Báo sai"; to be revisited (Hiep, 13/10/2026; ADR 0004) | "Báo sai" is built |
| Email or chat notices to owners | Needs an integration | Owners have records to act on |
| Owner screen for publish-time checks (new version, "dùng thay", "bổ sung", duplicate) | The Mission 1 check script (`docs/mission1/redraft/checks/adopted_rules.py`) runs the same check on the simulated data | Owners publish real documents |
| Periodic review where owners re-confirm documents and relations | Needs owners and time, not code | Real owners exist |
| Similarity scan that flags near-duplicate documents to the owner | Too few documents to need it | The document set grows |
| Notice to owners of overriding policies when the Group publishes a new version | Needs a publishing workflow | The publish screen is built |
| The LLM suggests "dùng thay" or "bổ sung" to the owner at publish time, for the owner to confirm | Mission 1 names it only as a possible change to who decides precedence; v1 keeps every relation declared by a person | Owners miss relations often enough to need a prompt |
| A "mandatory, cannot be overridden" flag on Group rules | Adds a rule type | The Group must enforce a rule on every company |
| Alert before an `effective_to` date passes with no successor | No simulated document has an end date | Owners set end dates |
| Integration with chat tools | Not needed to prove the core loop | Employees should ask where they already work |

### Evaluation

| Idea | Why deferred | Revisit when |
|---|---|---|
| Asking each test row in three wordings (as written, paraphrase, spoken style) | The Gemini free-tier rate limit; the main wording is tested first (Hiep, 14/10/2026; ADR 0006) | A paid tier, or more daily quota |
| Running each test case three times, one wrong run failing the case | The same rate limit; each case runs once in Mission 2 (Hiep, 14/10/2026; ADR 0006) | As above |
| Context recall: label the chunks that answer each question and measure how many retrieval returns | Too soon to measure on 10 simulated documents (Hiep, 13/10/2026; ADR 0007) | Real documents exist |
| An LLM judge for faithfulness | 20 answers can be read by hand, and a judge adds a second model to trust | Too many answers to read by hand |
| Naive-RAG baseline: the same search and LLM over every document with the rules switched off | Not needed to prove v1; the Mission 1 document keeps the naive-RAG failure as a prediction, not a measurement | A comparison is needed to argue for the rules layer |
| Embedding experiment: how close the near-identical leave documents score for one question | Not needed by the design; the rules remove the wrong versions before search | Retrieval inside a scope ranks the wrong chunk first |
| A latency target | No decision depends on it in v1; latency is only logged | Real users wait for answers |
| A pilot with real employees, measuring answers given without HR, refusal and conflict rates, and confirmed reports | After Mission 2 | The company agrees to a pilot |

### Demo pages

| Idea | Why deferred | Revisit when |
|---|---|---|
| "Simulated data" page: for each asker, every document outside their scope with the reason | It would re-derive the rules on the page and need a test that it agrees with them; the page lists what the rules keep, and `scripts/show_scope.py --why` prints the reasons (Hiep, 14/10/2026) | Judges need the reasons on the page |
| "Test cases" page: one "Thử ngay" link per row, opened in the same tab | Each wording got its own link in a new tab instead, so the case list stays open for comparison (Hiep, 14/10/2026) | - |

## Known limitations

Failures seen in the product.
Four rows are open issues labelled `limitation`; the first row and the last two are decisions with a cost, not open defects.
Each row says where the failure was seen: a test case of the run of 22/10/2026, an earlier run, or an experiment on the simulated data.

| Limitation | Seen in | Tracked in |
|---|---|---|
| The AI's answer is not checked while the product runs: a wrong number, a dropped condition or a wrong caveat above a correct quote reaches the asker, and only a reader catches it | Hiep's review of the 22/10/2026 run: the answer to case 3 leaves out that the approval result is sent to the company email | Decision records [0011](decisions/0011-answer-card-shows-the-models-sentence-above-the-verified-quote.md), [0017](decisions/0017-a-refusal-says-why-and-an-answer-says-what-it-does-not-cover.md) and [0018](decisions/0018-one-answer-per-question-above-the-verified-quotes.md) |
| The rules are only as right as the labels owners write: a wrong "dùng thay" or access label is never caught, and a wrong topic or "bổ sung" is caught only when the AI notices that two clauses disagree | Experiments on edited copies of the simulated data; case 19 for a wrong topic | [#50](https://github.com/Park-Hip/next-gen-2026/issues/50) |
| When no label reveals a conflict and the AI does not notice it, or one side's clause is not found, the asker gets an answer citing one side | Case 19 on the Mission 2 version, which answered from one side; on Mission 3 it passes, but only when the AI notices | [#74](https://github.com/Park-Hip/next-gen-2026/issues/74) |
| A question about another period gets the version in force on the as-of date. About next year ("từ năm sau..."), the card says when it ends and what replaces it, but never gives the next version's numbers. About a past year, it is usually refused, and can get this year's number | Case 18: an unsafe answer on Mission 2, and on Mission 3 an answer with the end date and the notice. Minh's question about his leave in 2025, asked 9 times on Mission 3 on 23/10/2026: refused 8 times, answered "14 ngày" once, when 2025 had 13 | [#53](https://github.com/Park-Hip/next-gen-2026/issues/53) |
| A question that needs a clause applied to a case ("nghỉ thứ Hai 19/10 thì hạn chót nộp đơn là ngày nào?") can be refused, although the right clause was found | Case 16: refused in 2 of 4 runs of the Mission 2 version, answered in 5 of 5 runs of the Mission 3 version; the rate is not measured | [#51](https://github.com/Park-Hip/next-gen-2026/issues/51) |
| When two conflicting policies say the same thing on the point asked, the asker still gets the conflict card and is sent to HR | Case 17, which expects the conflict card | [Decision record 0019](decisions/0019-a-conflict-is-shown-even-when-both-sides-agree-on-the-point-asked.md) |
| A company that changes one clause of a Group policy must publish a complete policy of its own; one that leaves a Group clause out loses it for its employees, who get a refusal | Case 15, on edited data that breaks this owner rule | [Decision record 0013](decisions/0013-owners-change-a-document-only-by-a-full-new-version.md) |

The results of every test case are in the [test report](test_report.md).
