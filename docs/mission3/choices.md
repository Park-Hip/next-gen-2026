# Mission 3 choices

Step 2 of the [Mission 3 checklist](checklist.md), and the source of mandatory question 1 of the [Mission 3 brief](../competition/mission3_brief.md): "Sau khi nhận yêu cầu mới, bạn đã ưu tiên thay đổi điều gì và chủ động chưa làm điều gì? Vì sao?".
Claude draft, 21/10/2026, for Hiep to check.
All data is simulated ("giả lập").

This page holds the second half of the question, what Mission 3 chose not to do; the first half, what it prioritised, is added later.
The Change Request is not assigned yet; when it arrives, every row below is checked against it, and a row it needs moves out of this list.

Each row is a real alternative that was weighed and left out, not work that ran out of time.
For each one: what is not built, what Mission 3 does instead, the reason, the risk accepted, and when to revisit it.
A reason in quotes is Hiep's own words, with its date; a reason without quotes is recorded in the linked document and was approved by Hiep; "[chờ Hiệp]" marks a reason still to come from Hiep.
The gap IDs (G1.1 to G5.4) are those of [`gaps.md`](gaps.md); the requirement IDs (E, H, S) are those of [`mvp_spec.md`](../mvp_spec.md).

## 1. The owners' side

The main cut.
[`mvp_spec.md`](../mvp_spec.md) and [`system_design.md`](../system_design.md), written on 20/10/2026, describe an MVP with two users: the employee who asks, and the owner who publishes documents.
Mission 3 builds only the employee's side: the 5 general requirements of the brief are all about what the employee gets.
The owners' side is the future fix of most of the limitations that remain, so it is also the first answer to question 3 (see [How this links to question 3](#how-this-links-to-question-3)).

| Not built | Mission 3 does instead | Reason | Risk accepted | Revisit when |
|---|---|---|---|---|
| The owner console: publish a document or a new version, declare "dùng thay" or "bổ sung", see the unit's documents and their state, the impact preview (H1-H5; `system_design.md` section 7) | Documents and their metadata are Markdown files typed by hand in `data/documents/`; the owners' rules are written down: a change is a full new version ([ADR 0013](../decisions/0013-owners-change-a-document-only-by-a-full-new-version.md)), and a document that applies to a unit is readable by it ([ADR 0015](../decisions/0015-a-document-that-applies-to-a-unit-must-be-readable-by-it.md)) | For Mission 2, Hiep, 13/10/2026: "drop the page too, we will revisit later" ([ADR 0004](../decisions/0004-render-free-singapore-no-bao-sai.md)); for Mission 3: [chờ Hiệp] | Nothing enforces the owners' rules: a wrong topic, relation or `access` reaches employees as written ([#50](https://github.com/Park-Hip/next-gen-2026/issues/50)) | Owners publish real documents |
| A check when an owner publishes: each clause of the new document is searched against the knowledge base, an LLM compares it with the similar clauses found, and the owner settles any contradiction (SD15; Hiep's idea, 21/10/2026) | The model may flag a disagreement between two cited chunks at question time, and the rules then show the conflict card; the model can add a conflict card, never remove one ([ADR 0014](../decisions/0014-the-model-may-add-a-conflict-never-remove-one.md)) | It needs the owners' page, so it is the long-term direction, not a Mission 3 change (Hiep, 21/10/2026, [`gaps.md`](gaps.md#3-conflicting-sources-and-levels-1)) | A disagreement the model does not notice, or whose other side is not retrieved, gives an answer card citing one side (G3.3); two sides that agree still give the conflict card (G3.2); a too wide `access` still leaks (G2.3) | The owner console is built |
| Published documents that survive a restart, and where they are stored (S4; SD1, SD2) | Nothing is written at run time; the documents are files in the repository | A Render free service loses its local files on every spin-down, restart or redeploy ([ADR 0004](../decisions/0004-render-free-singapore-no-bao-sai.md)), so storage needs a research issue and possibly a new host; for Mission 3: [chờ Hiệp] | None while documents come only from the repository | The owner console is built |
| Telling the two owners of a conflict that an employee met it (G3.5) | The conflict card sends the employee to HR, and nothing is recorded | It needs the owners' page ([ADR 0004](../decisions/0004-render-free-singapore-no-bao-sai.md)) | The same conflict reaches every employee who asks, until an owner notices it some other way | The owner console is built |

## 2. Changes left out because they would make an answer less safe

Each of these would give an answer in more cases, and each could then give a wrong one that looks right.
The principles behind them are Hiep's, from the sections of [`gaps.md`](gaps.md#how-mission-3-fixes-the-gaps): any doubt about which rule applies sends the asker to HR, never to one side; and refuse only when nothing can be verified.

| Not built | Mission 3 does instead | Reason | Risk accepted | Revisit when |
|---|---|---|---|---|
| Letting the model remove a conflict card when it reads that both sides agree on the point asked (G3.2) | The conflict card stays for every pair, and row 17 expects it | A wrong reading would become a wrong answer given with confidence; the conflict card is the safe direction ([`gaps.md`](gaps.md#3-conflicting-sources-and-levels-1)); Hiep, 22/10/2026: "hai văn bản có mâu thuẫn thì nên được báo cáo là mâu thuẫn, cho dù cả hai văn bản đều đồng ý về một câu trả lời" ([ADR 0019](../decisions/0019-a-conflict-is-shown-even-when-both-sides-agree-on-the-point-asked.md)) | An asker who could have been answered is sent to HR | The check when an owner publishes is built |
| Answering a question about another period with that period's version, such as "từ năm sau..." (G1.1) | The rules still pick the version in force on the as-of date; the card says until when it applies and what replaces it, and the prompt tells the model to say so ([ADR 0012](../decisions/0012-the-card-tells-the-asker-when-a-version-ends-and-what-replaces-it.md)) | The model never sees another version's content; picking the period from the question would let AI decide validity | The sentence is not checked at run time, so the model can still present today's value as next year's ([#53](https://github.com/Park-Hip/next-gen-2026/issues/53)) | Employees need to plan across a version change; the user then picks the period, never the AI |
| A run-time check on the model's sentence, by a rule on numbers or by a second model call (G5.4) | One fixed line on every answer card tells the reader that the bold sentence is the system's reading and the quoted text is the checked one; Hiep reads every sentence of a run | A rule on numbers would refuse correct sentences that give the dates of ADR 0012, and would not catch a dropped condition; a second model adds another thing to trust ([`gaps.md`](gaps.md#5-letting-the-user-check-the-documents-used-1), [ADR 0011](../decisions/0011-answer-card-shows-the-models-sentence-above-the-verified-quote.md)) | A misleading sentence is caught only by a reader | The reading of a run shows sentences that mislead often enough to need a check |
| Code that detects or repairs an owner's metadata error: a hidden side of a conflict (G3.6), a one-clause amendment (G1.3, G3.1), a too wide `access` (G2.3) | Owner rules, written down (ADR 0013, ADR 0015), applied as written | G3.6, Hiep, 21/10/2026: "đây là lỗi của metadata nên hệ thống không cần sửa cho trường hợp này"; a fix would refuse valid data, since v1 has no field for applicability by role | The rules are only as right as the metadata ([#50](https://github.com/Park-Hip/next-gen-2026/issues/50)) | The check when an owner publishes is built |
| A check that a verified quote answers the question asked (G4.1) | The time case is fixed by #83; for other questions the model's own refusal is the only guard | Hiep, 21/10/2026: "phần thời gian do #83, còn lại là limitation" | A quote that exists but does not answer the question still gives an answer card ([#53](https://github.com/Park-Hip/next-gen-2026/issues/53)) | A run shows such an answer outside time questions |
| Loosening the grounding instruction so that a clause is applied to a case more often (G4.2) | The prompt stays strict; row 16 is run on the Mission 3 code, and what to do next is decided from that result | Measure before changing anything ([`gaps.md`](gaps.md#4-refusing-when-the-basis-is-not-enough-1)); a looser prompt can turn refusals into unsupported answers | A practical question can still be refused although its clause was retrieved ([#51](https://github.com/Park-Hip/next-gen-2026/issues/51)) | Repeated runs of row 16 give a refusal rate |

## 3. Simplifications kept from Mission 2

Each is listed under "Simplified" or "Deferred" in [`scope.md`](../scope.md), with its production replacement; Mission 3 leaves them as they are.

| Not built | Mission 3 does instead | Reason | Risk accepted | Revisit when |
|---|---|---|---|---|
| Real sign-in, with unit and roles read from an HR system | Simulated accounts and one demo password shared by all, published in the README; the server, not the request, decides who is asking ([ADR 0016](../decisions/0016-simulated-sign-in.md)) | The rules need only the asker's unit and roles, and the data is simulated; ADR 0016 reasons: [chờ Hiệp] | Whoever has the password can sign in as anyone, including the judge | Real employees use it |
| The server's date as the only as-of date (G1.4) | The date picker stays, labelled as a demo control | It lets judges see the version change of 01/01/2027 without waiting for it (Hiep, 21/10/2026, [#76](https://github.com/Park-Hip/next-gen-2026/issues/76) decision 4) | Any visitor can read a published version before it is in force | Real employees use it |
| DOCX and PDF documents, and integration with chat tools | Markdown files; a web page | Kept from Mission 1, question 2: simulated data still gives the rules what they need to test the hardest part | None for the demo | Owners publish real documents; employees should ask where they already work |
| A version field on each document (G1.5) | The card shows the start and end of the validity window, which identify the version | AI proposal, approved by Hiep on 21/10/2026 | A source line names no version when the owner's title does not | Owners need to cite a version by its number |
| A simulated document issued below company level (G3.4) | `test_applies` and probe P9 show that the rules handle a lower level | Hiep, 21/10/2026: skip; reason: [chờ Hiệp] | No row shows a department rule that adds to or replaces a company rule | The Change Request or a judge asks for it |
| Employment type and seniority as conditions of applicability (G4.4) | The sentence and the quote keep the condition word for word ("nhân sự chính thức"), for the asker to read | The brief names only unit, access and version ([`scope.md`](../scope.md)) | Whether a condition covers the asker is left to the asker | A real policy depends on them |
| A trace record per question asked on the page (S3; SD12) | One JSON log line per search, model answer and page request; each evaluation run is recorded in `results/` | [chờ Hiệp] | A wrong answer seen on the demo can be explained only from the server logs | Real traffic |

## How this links to question 3

Question 3 asks for the biggest remaining risk if real users had the product tomorrow, and how it would be handled first.
Every guarantee of this product, from 0 leaks to the right version and the conflict card, holds only while the owners' metadata is right (assumption A1 of [`mvp_spec.md`](../mvp_spec.md)).
Section 1 is where that metadata would be checked, and Mission 3 chose not to build it, so the cut of question 1 is the first fix of question 3.
The wording of question 3 is Hiep's to settle.

## Open

- The reasons marked "[chờ Hiệp]": the owners' side and its storage for Mission 3, G3.4, the trace record, and ADR 0016.
- The first half of question 1, what Mission 3 prioritised.
- The Change Request, once assigned.
