# What Mission 1 promised v1

Every commitment in the submitted document (`docs/mission1/submitted/document.md`) and the 3 answers (`answers.md`), as the acceptance checklist for Mission 2.
Claude draft from the submitted files, 08/10/2026; Hiep checks it against the PDF.
Judges can compare what ships with these lines, so each one is either built and shown, or explicitly reported as not done, with the reason.

Quotes are from the submitted text.
"Shown by" is the planned evidence: a row of the test matrix in `docs/mission1/redraft/artifacts.md`, a demo step, or a code property.
Rows 1-10 keep their numbers in `data/test_cases.yaml`, and their results are in the [test report](test_report.md).

"Status", added on 14/10/2026 as the ledger of Mission 2, says what shipped: "Built", "Changed" with the ADR that changed it, or "Not done" with the reason.
A status that depends on the final evaluation run says so until that run is made.
What v1 simplifies or defers beyond these promises is in [`docs/scope.md`](../scope.md).

## 1. Data and identity

| # | Promise | Where | Shown by | Status |
|---|---|---|---|---|
| D1 | "10 văn bản giả lập dạng Markdown, chia đoạn theo Điều, kèm metadata" | Phần 3 | The 10 files; the procedure document has no Điều, so it is chunked by paragraph (as planned in `artifacts.md`) | Built: 10 files in `data/documents/`, 25 chunks; the procedure is chunked by line |
| D2 | Metadata per document: version series, status and effective date, who may see it, unit it applies to, "dùng thay", "bổ sung", topic, owner | Phần 2 | Front matter of each file, same fields as `adopted_rules.py` | Built: front matter of each file, checked on load |
| D3 | The asker's profile has only unit (path in the org tree) and role | Phần 2 | Persona file: Minh, Lan, Hà | Built: `data/personas.yaml` |
| D4 | "Bộ chọn người hỏi giả lập thay cho hệ thống nhân sự"; the real system takes the unit from HR records, never from the user | Phần 3, Câu 2 | Persona picker on the page; no field where users type their unit | Built: the persona picker on the page; there is no field to type a unit |
| D5 | Every unit, person, document and number is simulated | Header | Labels "giả lập" in the data and on the page | Built: labelled in the data, on every page and in the docs |

## 2. Rules (steps 1-4 and 7)

| # | Promise | Where | Shown by | Status |
|---|---|---|---|---|
| R1 | Steps 1-4 build the scope "từ metadata, không đọc câu hỏi và không dùng AI" | Phần 2 | Code: the scope function takes persona and date only, never the question | Built: `scope()` takes the persona, the date and the documents, never the question |
| R2 | Step 1: each series keeps the version in force: published, latest effective date not after the as-of date; drafts and future versions are out | Phần 2, Câu 3 | Rows 1, 2 | Built: rows 1, 2 |
| R3 | Step 2: keep documents the asker may see and that apply to their unit | Phần 2, Câu 3 | Rows 5, 6, 10 | Changed (ADR 0010): access is applied after step 3, so a document the asker may not read still replaces its series and never brings it back; rows 5, 6, 10 |
| R4 | Step 3: drop a document when another kept document declares "dùng thay" over its whole series, including later versions | Phần 2 | Row 1 (Group rule dropped for Minh) | Built: row 1; a document the asker may not read also counts (ADR 0010) |
| R5 | No default "đơn vị cấp dưới thắng"; precedence exists only where the owner declared it | Phần 2, Phần 4 | Row 7 (PayCo gets a conflict, not the lower unit) | Built: row 7 |
| R6 | Step 4: same topic, both apply, no declared relation means a conflict pair; "bổ sung" documents are not a conflict | Phần 2 | Rows 3, 7 | Built: rows 3, 7 |
| R7 | Step 7: a cited document in a conflict pair gives the conflict card; no citation, or a citation of a chunk that was not retrieved, refuses the whole answer | Phần 2 | Rows 7, 8, 9, 10; a test with an invented citation | Built, and stricter (ADR 0003): citations are checked against the chunks actually retrieved, and each point's quote must be in the chunk it cites |
| R8 | "văn bản người hỏi không được xem không bao giờ được đưa vào bước tìm kiếm" | Phần 1 | Leak check on chunk ids, 0 cases | Built: steps 1-4 run before search, and a runtime check raises an error if a chunk outside the scope is returned; 0 leaks in the 18 rows of the final run `20261014-2239` |
| R9 | v1 answers only rules that apply to the asker; other-unit questions are refused and sent to HR, even when the asker may read the document | Phần 2, Phần 5 | Row 6 | Built: row 6 |
| R10 | One refusal text for "not allowed" and "not found", so a restricted document is never revealed | Phần 2, Phần 5 | Rows 9 and 10 give the same text apart from the unit | Built: rows 9 and 10 |

## 3. AI (steps 5-6)

| # | Promise | Where | Shown by | Status |
|---|---|---|---|---|
| A1 | Hybrid search (keyword plus embedding) only over chunks of documents in the asker's scope | Phần 2, Phần 3 | Code; retrieved chunk ids in the run log | Built (ADRs 0001, 0002) |
| A2 | It also finds questions phrased differently from the document | Phần 3 | Each row asked in 3 phrasings: as written, paraphrase, "văn nói" | Changed (ADR 0006): each row is asked in its main wording only; the other wordings stay in the test file, not run, because of the Gemini free-tier rate limit |
| A3 | An off-the-shelf LLM answers only from retrieved chunks, cites each point, or says "không tìm thấy" | Phần 2, Phần 3, Câu 2 | Rows 8, 9 (nothing to answer), answer rows (citations) | Built (ADRs 0003, 0008): an empty list of points means "không tìm thấy" and gives the refusal card |
| A4 | AI never decides access, validity, applicability, precedence or the card | Phần 3, Câu 3 | Code: the card comes from the step 7 function, not from LLM text | Built: the card comes from `services/citations.py`, never from LLM text |
| A5 | A question touching two topics is still found (choice A of Quyết định 2) | Phần 4 | Row 4 (overtime rest day and annual leave) | Built: row 4 |
| A6 | A PayCo question about overtime does not get a leave conflict card | Phần 4 | Row 8 | Built: row 8 |

## 4. The three cards

| # | Promise | Where | Shown by | Status |
|---|---|---|---|---|
| C1 | Every card shows "Bạn đang hỏi với tư cách" with unit and department | Phần 2 | All three cards | Built |
| C2 | Answer card: the answer, source title and version, Điều, effective date, "Hỏi thêm: HR <unit>", button "Báo sai" | Phần 2 | Row 1 in the demo | Changed (ADRs 0004, 0009): built without the "Báo sai" button, and the answer line is the quote step 7 verified, word for word, not a sentence the model writes |
| C3 | Conflict card: neutral headline, both clauses quoted word for word with Điều and effective date, no LLM text, "Vui lòng hỏi HR <unit>", and "Đã ghi nhận để HR ... xác nhận" | Phần 2, Câu 3 | Row 7 in the demo; the conflict is recorded for the owners | Built, except the line "Đã ghi nhận để HR ... xác nhận": the conflict records file was cut (#15), because records would be lost on every restart of the free host (ADR 0004) |
| C4 | Refusal card: "Hệ thống không tìm thấy quy định phù hợp...", "Hệ thống chỉ trả lời các quy định áp dụng cho bạn", contact HR of the asker's unit | Phần 2 | Rows 6, 9, 10 | Built |

## 5. People

| # | Promise | Where | Shown by | Status |
|---|---|---|---|---|
| P1 | Owners see the conflict and "Báo sai" records | Phần 3, Phần 5 step 3 | Owners' list page; cut first if a day slips, then records stay in a file | Not done (ADR 0004): out of scope for Mission 2, to be revisited; listed in `docs/scope.md` |
| P2 | Employees can press "Báo sai" | Phần 2, Phần 3 | Button on the answer card writes a record | Not done (ADR 0004): adds little value to Mission 2, and records would not survive a restart on the free host; listed in `docs/scope.md` |

## 6. Validation

| # | Promise | Where | Shown by | Status |
|---|---|---|---|---|
| V1 | A test set of simulated questions, each with the right result and the documents that must not be cited | Phần 5 | The 10 rows times 3 phrasings, as a data file | Changed (ADR 0006): 18 rows, rows 1-10, five added for the brief and three limitation rows, each asked in its main wording |
| V2 | The five situations: two units, before and after a new version, undeclared conflict, other unit's rule, restricted document | Phần 5 | Rows 1 and 5; 1 and 2; 7; 6; 10 | Built: same rows |
| V3 | Metrics and targets: rules correct in every case, 0 leaks, 0 unsafe LLM answers, faithfulness read by hand for every answer, at most 10% over-cautious, context recall tracked only | Phần 5 | Results table from the final run | Changed (ADR 0007): context recall is not tracked; the other metrics are gates in the test report, and faithfulness is read by Hiep |
| V4 | "Mỗi ca chạy nhiều lần ... một lần sai tính là trượt" | Phần 5 | Each case run 3 times | Changed (ADR 0006): each case runs once, because of the Gemini free-tier rate limit |
| V5 | The first four metrics are the condition to open to employees; passing them on a small simulated set is not proof | Phần 5, Phần 4 | Stated next to the results | Built: stated under the gates in the test report |
| V6 | Riskiest assumption: with no answering document the LLM says it found nothing; with one, it cites that one; one unsafe answer disproves it | Phần 5 | Rows 8, 9, 10 and the answer rows; report honestly if it fails | Built: unsafe answers are counted on the card and, separately, on the raw model reply; final run `20261014-2239`: 0 unsafe in the 14 gated rows, on the card and in the raw reply; limitation row 18 gave an unsafe answer card for a question about next year (#53) |

## 7. Build order and scope

| # | Promise | Where | Shown by | Status |
|---|---|---|---|---|
| B1 | Rules and tests first, correct in every case before any LLM | Phần 5, Câu 2 | Commit history: rules and tests pass before the retriever lands | Built: the rules and their tests merged on 13/10 at 17:23 (PR #25), before retrieval (PR #28, 21:55) |
| B2 | Then retrieval and generation, the test set run several times | Phần 5, Câu 2 | Run log | Changed (ADR 0006): the test set runs once |
| B3 | Then a minimal page: persona and date picker, three cards, "Báo sai", owners' list | Phần 5, Câu 2 | The page | Changed (ADR 0004): persona and date picker and the three cards are built; "Báo sai" and the owners' list are not |
| B4 | Not doing: real login, HR system connection, chat tool integration, DOCX/PDF reading | Câu 2 | None of them in v1 | Built: none of them is in v1 |

## Tensions to settle when the Mission 2 brief arrives

- **Answer 2 vs Phần 5, step 3:** Answer 2's day 3 says "giao diện web chọn người hỏi, xem kết quả"; Phần 5 adds the date picker, "Báo sai" and the owners' list.
  Building the Phần 5 version satisfies both.
  Settled: the page has the persona and date picker; "Báo sai" and the owners' list were cut by ADR 0004 (B3).
- **Invented citations (R7):** the rule script checks citations against the whole scope, because there is no retriever yet; v1 must check them against the chunks actually retrieved.
  Settled: step 7 checks them against the retrieved chunks, and checks each quote (ADR 0003).
- **Answer line wording (C2, A4):** Phần 2 shows the answer as a sentence the model writes, "Phép năm của bạn là 14 ngày mỗi năm.".
  A4 says the card never comes from LLM text, and nothing checks such a sentence, so v1 shows the quote step 7 verified (ADR 0009).
  The answer, the source line and the contact line are all still on the card.
- **Conflict record (C3):** the conflict card says the conflict "đã ghi nhận", so v1 needs at least a record in a file, even if the owners' page is cut.
  Cut: the records file (#15) was closed as not planned on 14/10/2026, so the card does not say "đã ghi nhận" (C3).
- **Not promised, do not build unless the brief asks:** a measured naive-RAG comparison (Phần 1 only predicts "dễ xếp"), the LLM suggesting relations at publish time (only under "Đổi khi" in Quyết định 1), choosing another unit to ask about, partial overrides of one clause.
  None was built; they are listed under "Deferred" in `docs/scope.md`.
