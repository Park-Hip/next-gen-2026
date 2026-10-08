# What Mission 1 promised v1

Every commitment in the submitted document (`docs/mission1/submitted/document.md`) and the 3 answers (`answers.md`), as the acceptance checklist for Mission 2.
Claude draft from the submitted files, 08/10/2026; Hiep checks it against the PDF.
Judges can compare what ships with these lines, so each one is either built and shown, or explicitly reported as not done, with the reason.

Quotes are from the submitted text.
"Shown by" is the planned evidence: a row of the test matrix in `docs/mission1/redraft/artifacts.md`, a demo step, or a code property.

## 1. Data and identity

| # | Promise | Where | Shown by |
|---|---|---|---|
| D1 | "10 văn bản giả lập dạng Markdown, chia đoạn theo Điều, kèm metadata" | Phần 3 | The 10 files; the procedure document has no Điều, so it is chunked by paragraph (as planned in `artifacts.md`) |
| D2 | Metadata per document: version series, status and effective date, who may see it, unit it applies to, "dùng thay", "bổ sung", topic, owner | Phần 2 | Front matter of each file, same fields as `adopted_rules.py` |
| D3 | The asker's profile has only unit (path in the org tree) and role | Phần 2 | Persona file: Minh, Lan, Hà |
| D4 | "Bộ chọn người hỏi giả lập thay cho hệ thống nhân sự"; the real system takes the unit from HR records, never from the user | Phần 3, Câu 2 | Persona picker on the page; no field where users type their unit |
| D5 | Every unit, person, document and number is simulated | Header | Labels "giả lập" in the data and on the page |

## 2. Rules (steps 1-4 and 7)

| # | Promise | Where | Shown by |
|---|---|---|---|
| R1 | Steps 1-4 build the scope "từ metadata, không đọc câu hỏi và không dùng AI" | Phần 2 | Code: the scope function takes persona and date only, never the question |
| R2 | Step 1: each series keeps the version in force: published, latest effective date not after the as-of date; drafts and future versions are out | Phần 2, Câu 3 | Rows 1, 2 |
| R3 | Step 2: keep documents the asker may see and that apply to their unit | Phần 2, Câu 3 | Rows 5, 6, 10 |
| R4 | Step 3: drop a document when another kept document declares "dùng thay" over its whole series, including later versions | Phần 2 | Row 1 (Group rule dropped for Minh) |
| R5 | No default "đơn vị cấp dưới thắng"; precedence exists only where the owner declared it | Phần 2, Phần 4 | Row 7 (PayCo gets a conflict, not the lower unit) |
| R6 | Step 4: same topic, both apply, no declared relation means a conflict pair; "bổ sung" documents are not a conflict | Phần 2 | Rows 3, 7 |
| R7 | Step 7: a cited document in a conflict pair gives the conflict card; no citation, or a citation of a chunk that was not retrieved, refuses the whole answer | Phần 2 | Rows 7, 8, 9, 10; a test with an invented citation |
| R8 | "văn bản người hỏi không được xem không bao giờ được đưa vào bước tìm kiếm" | Phần 1 | Leak check on chunk ids, 0 cases |
| R9 | v1 answers only rules that apply to the asker; other-unit questions are refused and sent to HR, even when the asker may read the document | Phần 2, Phần 5 | Row 6 |
| R10 | One refusal text for "not allowed" and "not found", so a restricted document is never revealed | Phần 2, Phần 5 | Rows 9 and 10 give the same text apart from the unit |

## 3. AI (steps 5-6)

| # | Promise | Where | Shown by |
|---|---|---|---|
| A1 | Hybrid search (keyword plus embedding) only over chunks of documents in the asker's scope | Phần 2, Phần 3 | Code; retrieved chunk ids in the run log |
| A2 | It also finds questions phrased differently from the document | Phần 3 | Each row asked in 3 phrasings: as written, paraphrase, "văn nói" |
| A3 | An off-the-shelf LLM answers only from retrieved chunks, cites each point, or says "không tìm thấy" | Phần 2, Phần 3, Câu 2 | Rows 8, 9 (nothing to answer), answer rows (citations) |
| A4 | AI never decides access, validity, applicability, precedence or the card | Phần 3, Câu 3 | Code: the card comes from the step 7 function, not from LLM text |
| A5 | A question touching two topics is still found (choice A of Quyết định 2) | Phần 4 | Row 4 (overtime rest day and annual leave) |
| A6 | A PayCo question about overtime does not get a leave conflict card | Phần 4 | Row 8 |

## 4. The three cards

| # | Promise | Where | Shown by |
|---|---|---|---|
| C1 | Every card shows "Bạn đang hỏi với tư cách" with unit and department | Phần 2 | All three cards |
| C2 | Answer card: the answer, source title and version, Điều, effective date, "Hỏi thêm: HR <unit>", button "Báo sai" | Phần 2 | Row 1 in the demo |
| C3 | Conflict card: neutral headline, both clauses quoted word for word with Điều and effective date, no LLM text, "Vui lòng hỏi HR <unit>", and "Đã ghi nhận để HR ... xác nhận" | Phần 2, Câu 3 | Row 7 in the demo; the conflict is recorded for the owners |
| C4 | Refusal card: "Hệ thống không tìm thấy quy định phù hợp...", "Hệ thống chỉ trả lời các quy định áp dụng cho bạn", contact HR of the asker's unit | Phần 2 | Rows 6, 9, 10 |

## 5. People

| # | Promise | Where | Shown by |
|---|---|---|---|
| P1 | Owners see the conflict and "Báo sai" records | Phần 3, Phần 5 step 3 | Owners' list page; cut first if a day slips, then records stay in a file |
| P2 | Employees can press "Báo sai" | Phần 2, Phần 3 | Button on the answer card writes a record |

## 6. Validation

| # | Promise | Where | Shown by |
|---|---|---|---|
| V1 | A test set of simulated questions, each with the right result and the documents that must not be cited | Phần 5 | The 10 rows times 3 phrasings, as a data file |
| V2 | The five situations: two units, before and after a new version, undeclared conflict, other unit's rule, restricted document | Phần 5 | Rows 1 and 5; 1 and 2; 7; 6; 10 |
| V3 | Metrics and targets: rules correct in every case, 0 leaks, 0 unsafe LLM answers, faithfulness read by hand for every answer, at most 10% over-cautious, context recall tracked only | Phần 5 | Results table from the final run |
| V4 | "Mỗi ca chạy nhiều lần ... một lần sai tính là trượt" | Phần 5 | Each case run 3 times |
| V5 | The first four metrics are the condition to open to employees; passing them on a small simulated set is not proof | Phần 5, Phần 4 | Stated next to the results |
| V6 | Riskiest assumption: with no answering document the LLM says it found nothing; with one, it cites that one; one unsafe answer disproves it | Phần 5 | Rows 8, 9, 10 and the answer rows; report honestly if it fails |

## 7. Build order and scope

| # | Promise | Where | Shown by |
|---|---|---|---|
| B1 | Rules and tests first, correct in every case before any LLM | Phần 5, Câu 2 | Commit history: rules and tests pass before the retriever lands |
| B2 | Then retrieval and generation, the test set run several times | Phần 5, Câu 2 | Run log |
| B3 | Then a minimal page: persona and date picker, three cards, "Báo sai", owners' list | Phần 5, Câu 2 | The page |
| B4 | Not doing: real login, HR system connection, chat tool integration, DOCX/PDF reading | Câu 2 | None of them in v1 |

## Tensions to settle when the Mission 2 brief arrives

- **Answer 2 vs Phần 5, step 3:** Answer 2's day 3 says "giao diện web chọn người hỏi, xem kết quả"; Phần 5 adds the date picker, "Báo sai" and the owners' list.
  Building the Phần 5 version satisfies both.
- **Invented citations (R7):** the rule script checks citations against the whole scope, because there is no retriever yet; v1 must check them against the chunks actually retrieved.
- **Conflict record (C3):** the conflict card says the conflict "đã ghi nhận", so v1 needs at least a record in a file, even if the owners' page is cut.
- **Not promised, do not build unless the brief asks:** a measured naive-RAG comparison (Phần 1 only predicts "dễ xếp"), the LLM suggesting relations at publish time (only under "Đổi khi" in Quyết định 1), choosing another unit to ask about, partial overrides of one clause.
  They stay in "Deferred ideas" in `docs/mission1/playbook.md`.
