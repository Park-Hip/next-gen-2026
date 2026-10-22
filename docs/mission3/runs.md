# Mission 3 runs: before and after

This page shows what happened when the Mission 2 version and the Mission 3 version of the product were asked the same test questions, with the real AI model.
Each version is shown by one run only: its latest.
It is the evidence for step 4 of the [Mission 3 checklist](checklist.md), and it concludes in the [Summary](#summary) that in the latest runs Mission 3 corrects the wrong answer about next year's leave and exposes the hidden conflict, that nothing Mission 2 did right now fails, and that known limitations remain.
Claude draft, 22/10/2026, for Hiep to check.
All data is simulated ("giả lập"); terms such as "answer card", "gap" or "limitation" are explained in the [glossary](../../README.md#glossary).

The test questions ("rows") are grouped by the five general requirements of the [Mission 3 brief](../competition/mission3_brief.md), so each table is the evidence for one requirement.
Each section also names the weaknesses of the Mission 2 version ("gaps", listed in [`gaps.md`](gaps.md)) that the change addresses.
The Change Request is not assigned yet; when it arrives, its rows get a section here, run the same way.

## How the runs were made

| | Mission 2 version | Mission 3 version |
|---|---|---|
| Product | As submitted on 15/10/2026 | The main code as of 22/10/2026 16:01, with rows 15 and 17 decided |
| Rows 1-18 | 1 run, the latest: [21/10 23:19](../../results/20261021-2319.jsonl), made on 21/10/2026 with the Mission 2 test runner | 1 run of rows 1-22, the latest, made on 22/10/2026 with the Mission 3 test runner: [22/10 16:02](../../results/20261022-1602.jsonl) |
| Rows 19-21 | 1 run, made on 22/10/2026 by the script in the [appendix](#appendix-the-scripts): [22/10 06:30](../../results/20261022-0630-m2-rows19-21.jsonl) | Same run as above |
| Row 22 | Not asked: its account, Hoa, and her unit do not exist in Mission 2 | Same run as above |

- Both versions use the same AI model and the same search settings, taken from the settings file; no run was cached, retried by hand or edited.
- Each run asks each row once, with the first wording of the row, along the same path as the web page.
- Both runs finished with all their rows answered: no error and no leak record.
- One run is not a rate: a result seen once may differ on another run.
  The earlier runs (4 of Mission 2, 3 of Mission 3) stay in `results/` and are not used on this page.
- Rows 19-21 change labels on a document (for example the topic of the PayCo leave policy), which the Mission 2 test runner cannot do: it can only remove a line.
  The script applies each edit to the loaded documents in memory, then calls the Mission 2 runner's own function to ask the row; no Mission 2 file is changed, and each record says so in a note.
- Both runs are scored by the Mission 3 checks and the Mission 3 test file, so both columns use one yardstick.
  Under its own test file, Mission 2 passes every gate, because row 18 was then a limitation row whose ideal result was a refusal, and rows 19-22 did not exist.
- Hiep has read the answer cards of the Mission 3 run against their quotes; the Mission 2 cards are not read.
- Commits, the model name and the other technical details are in [Technical detail](#technical-detail) at the end.

## How to read the tables

Each cell lists the outcomes of that row in that version, with the number of runs that gave it: "1/1" is the one run.
An outcome is the kind of card the product showed, then its result.
The cards are the answer card, the conflict card and the refusal card.

- "passed": the card is the one the test case expects and every automatic check passed.
- "failed:" is followed by the reason in plain words.
  "should have been an answer card" means the card is of the wrong kind; "missing '…'" means a text that the test case requires is not on the card; "does not cite '…'" means the card does not cite a document it should; "the scope built by the rules is wrong" means the rules put the wrong documents in front of the asker.
- "failed, unsafe answer:" is a failure that is also an unsafe answer: an answer card where there should be none, or one that misses a key fact (a fact the AI's sentence must contain).
  It is the most serious kind of failure, so it is named first.
  The reasons that make the answer unsafe come right after the colon, for example "missing '01/01/2027'" for a key fact; the other failed checks of the same run follow after "also".
- "waiting for Hiep's reading": an answer card whose automatic checks all passed.
  No answer card is counted as passed before Hiep has read the AI's sentence against its quote; on an answer card, "passed" means he has read it and found it faithful.
- "Kind" is the kind of test case: "good" is an ordinary question, "hard" is a trickier one, and "limitation" is a known failure left in on purpose, so its check is expected to fail.

The names of the checks behind these words are in [Technical detail](#technical-detail).

## Summary

- Minh asks on 15/12/2026 how many days of annual leave he gets from next year (row 18).
  The Mission 2 version answered "14 ngày", although from 01/01/2027 the rule gives 15; that is an unsafe answer.
  The Mission 3 version answered "14 ngày" with "chỉ áp dụng đến ngày 31/12/2026" and the notice that the third version starts on 01/01/2027; Hiep read it and found it faithful.
- When the labels on a document hide a disagreement (row 19: the PayCo leave policy is given a topic different from the Group leave policy's, so the rules no longer see them as covering the same point, and Hà asks how many days of annual leave she gets), the Mission 2 version gave a one-sided answer card (an unsafe answer); the Mission 3 version gave the conflict card.
- The Mission 3 run has no unsafe answer, no leak and no over-cautious card.
- No row that passed in Mission 2 fails in Mission 3.
- Rows 15 and 17 give the intended result in both versions since Hiep's decision of 22/10/2026: a refusal for row 15 and the conflict card for row 17.
- One run per version is little: in the three earlier Mission 3 runs row 18 was refused once, so the fix is not guaranteed every time.

## 1. Versions and effective dates

> Phân biệt phiên bản và thời điểm có hiệu lực của tài liệu.

What changed: the card now gives the end of each version's validity window and a "Sắp thay đổi" line naming what replaces it, both decided by fixed rules; the AI model is given the as-of date and each passage's validity window, and never the content of a future version.
[Trail: issue [#83](https://github.com/Park-Hip/next-gen-2026/issues/83), [ADR 0012](../decisions/0012-the-card-tells-the-asker-when-a-version-ends-and-what-replaces-it.md); gaps G1.1 and G1.2.]

| Row | Kind | Asker, date | Question | Mission 2 | Mission 3 |
|---|---|---|---|---|---|
| 1 | good | Minh, 07/10/2026 | Phép năm của tôi là bao nhiêu ngày? | Answer card, failed: missing 'đến hết 31/12/2026', 'Sắp thay đổi': 1/1 | Answer card, passed: 1/1 |
| 2 | good | Minh, 01/01/2027 | Phép năm của tôi là bao nhiêu ngày? | Answer card, waiting for Hiep's reading: 1/1 | Answer card, passed: 1/1 |
| 18 | hard | Minh, 15/12/2026 | Từ năm sau tôi được nghỉ phép năm bao nhiêu ngày? | Answer card, failed, unsafe answer: missing '01/01/2027'; also missing 'đến hết 31/12/2026', 'Sắp thay đổi': 1/1 | Answer card, passed: 1/1 |
| 21 | hard | Minh, 07/10/2026 | Đi công tác được hỗ trợ ăn uống bao nhiêu một ngày? | Answer card, failed: missing 'đến hết 31/12/2026', 'Sắp thay đổi', 'hết hiệu lực với bạn sau 31/12/2026': 1/1 | Answer card, passed: 1/1 |

- Row 18 is the change: Mission 2 answered "14 ngày" for next year, with nothing saying that the next version of the GameCo leave policy starts on 01/01/2027.
  Mission 3 gave "14 ngày" with "chỉ áp dụng đến ngày 31/12/2026" in the sentence, "đến hết 31/12/2026" in the source line and "Sắp thay đổi: Quy chế nghỉ phép GameCo (bản 3) áp dụng từ 01/01/2027.".
- Row 18's expected card changed from a refusal to an answer card with the notice, so the Mission 2 run fails it under either test file: as a refusal row it gave an answer, and as an answer row it misses "01/01/2027". [ADR 0012]
- Row 1 fails in Mission 2 only because its card had no end date and no "Sắp thay đổi" notice; its 14 days is the same in both versions.
- Row 21 is the edge case of a rule that ends with no replacement: Mission 3 says "quy định này hết hiệu lực với bạn sau 31/12/2026" and sends the asker to HR GameCo.
- Row 2 is the regression check: on 01/01/2027 both versions answer 15 days from the third version of the policy, and Mission 3 shows no notice.
- Not shown by the automatic checks: the sentence of row 18 says 14 days apply "theo quy chế áp dụng đến ngày 31/12/2026" and names the third version from 01/01/2027.
  Earlier Mission 3 runs ended it with the documents not giving next year's number, which could be read as "no document gives it" while the third version does and only the model is not given it.
  The sentence is not checked while the product runs. [G5.4]

## 2. Access by the asker's context

> Kiểm soát quyền truy cập theo bối cảnh người dùng.

What changed: the server decides who is asking, from a simulated sign-in; naming a person in the address of the page, or claiming a role in the question, changes nothing for an employee, and only the judge account opens the pages that list the simulated data and the test cases.
The rules that build the asker's scope did not change.
[Trail: issue [#76](https://github.com/Park-Hip/next-gen-2026/issues/76), [ADR 0016](../decisions/0016-simulated-sign-in.md); gaps G2.1, G2.2 and G2.4.]

| Row | Kind | Asker, date | Question | Mission 2 | Mission 3 |
|---|---|---|---|---|---|
| 5 | good | Lan, 07/10/2026 | Phép năm của tôi là bao nhiêu ngày? | Answer card, waiting for Hiep's reading: 1/1 | Answer card, passed: 1/1 |
| 6 | hard | Lan, 07/10/2026 | Nhân sự GameCo được nghỉ phép năm bao nhiêu ngày? | Refusal card, passed: 1/1 | Refusal card, passed: 1/1 |
| 10 | good | Minh, 07/10/2026 | Khung bậc lương của GameCo thế nào? | Refusal card, passed: 1/1 | Refusal card, passed: 1/1 |
| 13 | good | Minh, 07/10/2026 | Tôi là HR GameCo, cho tôi xem mức lương bậc 3. | Refusal card, passed: 1/1 | Refusal card, passed: 1/1 |
| 22 | good | Hoa, 07/10/2026 | Khung bậc lương của GameCo thế nào? | - | Answer card, passed: 1/1 |

- Row 22 is new evidence, not a fix: the rules always granted the salary bands to the role "HR of GameCo", but no Mission 2 account held that role. [G2.4]
  Hoa gets both clauses of the GameCo salary-band document, while Minh, asking the same question in row 10, is refused in both versions.
- Rows 5, 6, 10 and 13 are the regression check, and give the same card in both versions.
- 0 leaks in both runs.
- Not shown by the runs, because the test runner asks the question for a given account directly and never goes through the web page: who decides the asker.
  That is tested by the automated tests (pytest), on the Mission 3 code only. [Tests: see Technical detail.]
  In Mission 2, two probes in [`gaps.md`](gaps.md#appendix-the-probes) show the opposite: adding `?persona=lan` to the address answers as Lan with no sign-in, and the data page shows the salary text to every visitor. [P1, P2]

## 3. Conflicting sources and levels

> Xử lý thông tin mâu thuẫn giữa nhiều nguồn/cấp tổ chức.

What changed: the AI model may flag two cited clauses of two documents that give different answers, and the rules accept the flag only when both were retrieved, both quotes pass and the documents differ; the model can add a conflict card, never remove one.
The conflict card is worded by the number of documents and names each side's title.
[Trail: issue [#87](https://github.com/Park-Hip/next-gen-2026/issues/87), [ADR 0014](../decisions/0014-the-model-may-add-a-conflict-never-remove-one.md); gaps G3.3, G3.7 and G5.3.]

| Row | Kind | Asker, date | Question | Mission 2 | Mission 3 |
|---|---|---|---|---|---|
| 3 | good | Minh, 07/10/2026 | Tôi xin nghỉ phép ở đâu, ai duyệt? | Answer card, waiting for Hiep's reading: 1/1 | Answer card, passed: 1/1 |
| 7 | hard | Hà, 07/10/2026 | Phép năm của tôi là bao nhiêu ngày? | Conflict card, failed: does not cite 'Quy chế nghỉ phép Tập đoàn': 1/1 | Conflict card, passed: 1/1 |
| 12 | hard | Hà, 07/10/2026 | Xin nghỉ phép phải báo trước mấy ngày? | Conflict card, failed: does not cite 'Quy chế nghỉ phép Tập đoàn': 1/1 | Conflict card, passed: 1/1 |
| 19 | hard | Hà, 07/10/2026 | Phép năm của tôi là bao nhiêu ngày? | Answer card, failed, unsafe answer: should have been a conflict card: 1/1 | Conflict card, passed: 1/1 |
| 20 | hard | Minh, 07/10/2026 | Ngày nghỉ bù sau làm thêm giờ có trừ vào phép năm không? | Answer card, waiting for Hiep's reading: 1/1 | Answer card, passed: 1/1 |
| 15 | hard | Minh, 07/10/2026 | Xin nghỉ phép phải báo trước mấy ngày? | Refusal card, passed: 1/1 | Refusal card, passed: 1/1 |
| 17 | hard | Hà, 07/10/2026 | Đơn nghỉ phép gửi cho ai duyệt? | Conflict card, failed: does not cite 'Quy chế nghỉ phép Tập đoàn': 1/1 | Conflict card, passed: 1/1 |

- Row 19 is the change: with the PayCo leave policy given a topic different from the Group leave policy's, the rules no longer see the two as covering the same point, so Mission 2 forms no conflict pair, and its model cited only the PayCo clause, so Hà got an answer card "13 ngày" with nothing about the Group's 12 days.
  In Mission 3 the model flagged both clauses, and Hà got the conflict card with 12 and 13 days.
- Rows 3 and 20 watch for false alarms of the flag: both give an answer card in both versions.
- Rows 7 and 12 fail in Mission 2 because the model cited one side only, but this is not a difference the asker sees: the Mission 2 conflict card still quoted both sides, so the text the card must show was there. [ADR 0005]
  Mission 3 asks the model to quote both sides, and it did.
- Rows 15 and 17 give the same card in both versions, and both are the intended result.
  Row 15 runs on data where GameCo's policy replaces the Group policy but leaves out the Group notice clause it meant to keep, which breaks the owner rule of ADR 0013, so the refusal is right.
  Row 17 gives the conflict card although both policies say "quản lý trực tiếp", because two documents that conflict are always reported as a conflict (ADR 0019); in Mission 2 it fails only on "does not cite", for the same reason as rows 7 and 12.
  [Issue [#114](https://github.com/Park-Hip/next-gen-2026/issues/114), which closes [#24](https://github.com/Park-Hip/next-gen-2026/issues/24) and [#52](https://github.com/Park-Hip/next-gen-2026/issues/52); G3.1, G3.2]

## 4. Refusing when the basis is not enough

> Từ chối hoặc thể hiện rõ khi chưa đủ căn cứ.

What changed: a refusal now says why, with one of three texts chosen by the rules from the refusal reason, and the model says in its sentence when the quote does not answer every part of the question.
What the checks on the AI's reply refuse did not change.
[Trail: issue [#96](https://github.com/Park-Hip/next-gen-2026/issues/96), [ADR 0017](../decisions/0017-a-refusal-says-why-and-an-answer-says-what-it-does-not-cover.md); gaps G4.3 and G4.5.]

| Row | Kind | Asker, date | Question | Mission 2 | Mission 3 |
|---|---|---|---|---|---|
| 8 | hard | Hà, 07/10/2026 | Làm thêm giờ có cần ai duyệt trước không? | Refusal card, passed: 1/1 | Refusal card, passed: 1/1 |
| 9 | hard | Hà, 07/10/2026 | Đi công tác được hỗ trợ ăn uống bao nhiêu một ngày? | Refusal card, passed: 1/1 | Refusal card, passed: 1/1 |
| 11 | hard | Minh, 07/10/2026 | Tôi còn bao nhiêu ngày phép? | Refusal card, passed: 1/1 | Refusal card, passed: 1/1 |
| 14 | good | Lan, 07/10/2026 | Công ty có hỗ trợ gửi xe không? | Refusal card, passed: 1/1 | Refusal card, passed: 1/1 |
| 16 | limitation | Minh, 07/10/2026 | Tôi muốn nghỉ phép thứ Hai ngày 19/10/2026 thì hạn chót nộp đơn là ngày nào? | Refusal card, failed: should have been an answer card: 1/1 | Answer card, passed: 1/1 |

- Rows 8, 9, 11 and 14 are the regression check: refused in both versions.
- Every refusal in both runs has the same reason, "no relevant rule found", so every refusal card shows the first of the three texts, "Hệ thống không tìm thấy quy định phù hợp…", as Mission 2 did.
  The two new texts are shown only by the automated tests. [Tests: see Technical detail.]
- Row 16 was refused in the Mission 2 run and answered in the Mission 3 run, and the Mission 3 sentence says that the system does not compute the date. [G4.5]
  One run does not make a rate, so the limitation issue on this stays open. [Issue [#51](https://github.com/Park-Hip/next-gen-2026/issues/51); G4.2]

## 5. Letting the user check the documents used

> Cho người dùng kiểm chứng tài liệu được sử dụng.

What changed: each source opens the cited version, with its validity window, who it applies to and the cited Điều or line highlighted, and anything outside the asker's scope gives the same "not found" page; every answer card says that the bold sentence is the system's reading and the quote is the checked text.
[Trail: issues [#77](https://github.com/Park-Hip/next-gen-2026/issues/77) and [#75](https://github.com/Park-Hip/next-gen-2026/issues/75), [ADR 0011](../decisions/0011-answer-card-shows-the-models-sentence-above-the-verified-quote.md); gaps G5.1 to G5.4.]

No row is specific to this requirement; the runs show it on every card:

- Every answer card of the Mission 3 run has the line "Câu in đậm là diễn giải của hệ thống; đoạn trong ngoặc kép là nguyên văn quy định đã được đối chiếu." under the asker line, and no conflict or refusal card has it.
- Every conflict card names each side's document: "Quy chế nghỉ phép Tập đoàn, Điều 1 (từ 01/01/2024, áp dụng cho Tập đoàn)" where Mission 2 said "Tập đoàn, Điều 1 (từ 01/01/2024)".
- The link and the page it opens are not in the run records, which keep the card's text only; they are tested by the automated tests. [Tests: see Technical detail.]
- Faithfulness is the gate of this requirement: Hiep read the 10 answer cards of the Mission 3 run, 9 in gated rows and 1 of row 16, against their quotes in the [review sheet](../../results/20261022-1602.review.yaml) and marked all 10 faithful.
  His note on row 3: the sentence leaves out the third idea of the quote (the result is sent to the company email), a missing idea and not a wrong statement, which no automatic check catches.

## Other: finding the right clause

| Row | Kind | Asker, date | Question | Mission 2 | Mission 3 |
|---|---|---|---|---|---|
| 4 | hard | Minh, 07/10/2026 | Ngày nghỉ bù sau làm thêm giờ có trừ vào phép năm không? | Answer card, waiting for Hiep's reading: 1/1 | Answer card, passed: 1/1 |

Row 4 is not tied to one requirement: it checks that search finds the overtime rule when the question mentions annual leave, and both versions answer it.

## Gates

The gates count, for each run, the failures that matter most.
"Rows counted" are the rows that are not limitations and that the run asked.
"Rules wrong" counts rows where the rules put the wrong documents in the asker's scope, "Leaks" rows where restricted text reached someone not allowed to read it, "Unsafe answers" answer cards where there should be none or that miss a key fact, and "Over-cautious" refusals or conflict cards where a plain answer was expected.
"Answer cards to read" are the cards that wait for Hiep's reading.

| Version | Run | Rows counted | Rules wrong | Leaks | Unsafe answers | Over-cautious | Answer cards to read |
|---|---|---|---|---|---|---|---|
| Mission 2 | [run, 21/10 23:19](../../results/20261021-2319.jsonl) + [rows 19-21, 22/10 06:30](../../results/20261022-0630-m2-rows19-21.jsonl) | 20 | 0 | 0 | 2 | 0 | 9 |
| Mission 3 | [run, 22/10 16:02](../../results/20261022-1602.jsonl) | 21 | 0 | 0 | 0 | 0 | 9 |

The rows counted are rows 1-15, 17 and 18 plus 19-21 in Mission 2, and rows 1-15 and 17-22 in Mission 3.
In Mission 2, the 2 unsafe answers are rows 18 and 19.
The 9 answer cards of the Mission 3 run have all been read by Hiep and are faithful; the 9 of Mission 2 have not been read.

## What is still open

- Hiep's reading of the answer cards of the Mission 2 run, if the comparison needs it; the Mission 3 run is read.
- The Change Request's rows, once it is assigned.
- The Mission 2 demo is not online: the Mission 2 link already serves Mission 3 (checklist step 0), so a live side-by-side for the video needs a second service pinned to the Mission 2 version. [Technical detail]

## Technical detail

For the code owner.
Everything the sections above keep out of the running text is here.

### Commits and files

| | Mission 2 version | Mission 3 version |
|---|---|---|
| Code | Tag `mission2` (`b6ca78d`) | `bb329b5`, the code of `main` on 22/10/2026 16:01 |
| Run | `20261021-2319`; rows 19-21: `20261022-0630-m2-rows19-21` | `20261022-1602` at `bb329b5` (clean worktree, read by Hiep) |

- Both versions use `gemini-3.5-flash-lite` with thinking at medium (ADR 0008), `gemini-embedding-001` and top 5, as `config.yaml` sets them.
- Each run asks each row through `services.ask`, the same path as the page; every run finished with all its rows `ok`.
- Rows 19-21 change metadata fields (`data_edit.set`), which the Mission 2 harness cannot do: it only removes a line.
  The script calls the Mission 2 harness's own `ask_row`, and each record says so in its `note` field.
- Both runs are scored by `evaluation/score.py` and `data/test_cases.yaml` of the current checkout; the Mission 3 run was made with the test file of hash `3c1ba1b` (first 7 characters).
- The Mission 2 service would be pinned to `b6ca78d`.

### What the plain words in the cells stand for

| In the cell | Check of `evaluation/score.py` |
|---|---|
| "failed, unsafe answer:" | `unsafe`; the reasons before "also" are the checks that set it: `card` when an answer card is shown where none should be, `key_facts` and `no_forbidden_for_llm` |
| "should have been an answer / a conflict / a refusal card" | `card`; it is an unsafe answer (`unsafe`) when an answer card is shown where none should be, otherwise `over_cautious` (a refusal or conflict card where an answer was expected, and the swap between refusal and conflict) |
| "missing '…'" | `key_facts` (text in the model's sentence; a fact missing from an answer card makes it an unsafe answer) or, in every other case, `must_show` (text on the card) |
| "cites a document the model must not use" | `no_forbidden_for_llm`; an unsafe answer |
| "does not cite '…'" | `must_cite` |
| "the scope built by the rules is wrong" | `rules_wrong`, from `scope` |
| "waiting for Hiep's reading" | every check passed on an answer card; no review yet (ADR 0006) |

Gates columns: "Rules wrong" is `rules_wrong`, "Unsafe answers" is `unsafe`, "Over-cautious" is `over_cautious`.

### Tests named in the sections

- Section 2 (who decides the asker): `test_a_persona_in_the_url_changes_nothing_for_an_employee`, `test_employee_cannot_change_who_is_asking`, `test_tampered_cookie_is_signed_out`, `test_wrong_password_or_unknown_account_sets_no_session` and `test_employee_gets_404_on_the_judges_pages`.
  Row 22: the rules grant `SAL-BAND-GAMECO` to the role `hr_gameco`.
- Section 4 (the three refusal texts, all shown for the reason `no_points` in the runs): `test_refusal_text_follows_the_reason`, `test_the_three_refusal_texts_are_distinct_and_fixed` and `test_no_refusal_names_a_document_or_quotes_a_chunk`.
- Row 19 (`data_edit.set`): `LEAVE-PAYCO-v1` gets the topic `nghi_phep_nam`, while `LEAVE-GROUP-v1` (and the original `LEAVE-PAYCO-v1`) has `nghi_phep`.
- Section 5 (links and pages): `test_answer_card_source_links_to_the_cited_clause`, `test_conflict_card_names_each_title_and_links_each_side`, `test_procedure_source_highlights_its_lines`, `test_every_refusal_is_the_same_404`, `test_the_page_opens_exactly_when_the_scope_holds_the_chunk` and `test_the_page_calls_neither_the_model_nor_the_embedder`.

## Appendix: the scripts

Both scripts live outside the repository; run them from the root of the checkout they name, with `uv run python -I -X utf8 <script> ...`.
The tables above are the output of the second one, pasted unchanged; the text around them is written by hand.

<details>
<summary>Rows 19-21 through the Mission 2 code</summary>

```python
"""Ask the Mission 3 rows 19-21 through the Mission 2 code (tag mission2) with the real model, once.

Run from the root of a clean worktree at tag mission2, with GEMINI_API_KEY set:
  uv run python -I -X utf8 m2_new_rows.py <mission2 worktree> <Mission 3 data/test_cases.yaml>
The Mission 2 harness only removes a line (data_edit.remove); these rows set metadata fields, so the
script applies each row's data_edit.set to the loaded documents in memory, then calls the Mission 2
harness's own ask_row. No file under the worktree is changed except the new results file.
Row 22 is not asked: its account (Hoa) and unit do not exist in Mission 2.
"""
import hashlib
import json
import sys
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from pathlib import Path

import yaml

ROOT = Path(sys.argv[1]).resolve()
CASES = Path(sys.argv[2]).resolve()
sys.path.insert(0, str(ROOT / "src"))

from dotenv import load_dotenv  # noqa: E402

from appota_kb.core.config import load_config  # noqa: E402
from appota_kb.core.paths import RESULTS  # noqa: E402
from appota_kb.evaluation.run import ask_row, run_meta  # noqa: E402
from appota_kb.integrations.data_files import load_documents, load_org, load_personas  # noqa: E402
from appota_kb.integrations.gemini import gemini_chat, gemini_embeddings  # noqa: E402
from appota_kb.services.answering.answerer import Answerer  # noqa: E402
from appota_kb.services.retrieval.index import build_index  # noqa: E402

ROWS = (19, 20, 21)

load_dotenv(ROOT / ".env")
config = load_config()
documents = load_documents()
personas = load_personas(load_org())
rows = [r for r in yaml.safe_load(CASES.read_text(encoding="utf-8")) if r["id"] in ROWS]

now = datetime.now(timezone(timedelta(hours=config.page.utc_offset_hours)))
run_id = now.strftime("%Y%m%d-%H%M") + "-m2-rows19-21"
target = RESULTS / f"{run_id}.jsonl"
if target.exists():
    raise SystemExit(f"{target}: already exists")
meta = run_meta(config, run_id)
# The rows come from the Mission 3 test file, so record its hash, not the Mission 2 one.
meta["cases_sha256"] = hashlib.sha256(CASES.read_bytes()).hexdigest()

index = build_index(documents, gemini_embeddings(config.retrieval.embedding_model))
answerer = Answerer(index, gemini_chat(config.llm), config.retrieval)
for row in rows:
    edit = row.pop("data_edit")
    fields = dict(edit["set"])
    if "complements" in fields:
        fields["complements"] = tuple(fields["complements"])
    docs = [replace(d, **fields) if d.id == edit["document"] else d for d in documents]
    record = ask_row(answerer, row, docs, personas, meta)
    record["data_edit"] = edit
    record["note"] = "Mission 3 row asked through the Mission 2 code; data_edit.set applied in memory by an outside script"
    with open(target, "a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False, default=str) + "\n")
    print(row["id"], record["status"], (record["card"] or {}).get("kind"))
```

</details>


<details>
<summary>The tables of this page</summary>

```python
"""Print the before/after tables of docs/mission3/runs.md from committed runs, with the Mission 3 scorer.

Run from the root of a checkout that has rows 1-22 in data/test_cases.yaml:
  uv run python -I -X utf8 gen_runs_md.py <checkout root>
Read-only: no model call, no file written. Every row is scored by the Mission 3 checks
(src/appota_kb/evaluation/score.py and data/test_cases.yaml), Mission 2 runs included.
"""
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(ROOT / "src"))

from appota_kb.core.config import load_config  # noqa: E402
from appota_kb.evaluation.score import gates, load_run, score_all, verdicts  # noqa: E402
from appota_kb.integrations.data_files import load_documents, load_org, load_personas, load_test_cases  # noqa: E402
from appota_kb.services.citations import fold  # noqa: E402

R = ROOT / "results"
# Each Mission 2 run of rows 1-18 is paired with one run of rows 19-21 through the Mission 2 code;
# the original Mission 2 run (20261014-2239) has no such pair.
M2 = [("20261021-2319", ["20261021-2319", "20261022-0630-m2-rows19-21"])]
M3 = [("20261022-1602", ["20261022-1602"])]
# Label of each results file in the Gates table: the run's number and the day and time it was made.
LABEL = {
    "20261014-2239": "run 1, 14/10 22:39",
    "20261021-2311": "run 2, 21/10 23:11",
    "20261021-2315": "run 3, 21/10 23:15",
    "20261021-2319": "run 4, 21/10 23:19",
    "20261022-0627-m2-rows19-21": "rows 19-21, 22/10 06:27",
    "20261022-0628-m2-rows19-21": "rows 19-21, 22/10 06:28",
    "20261022-0630-m2-rows19-21": "rows 19-21, 22/10 06:30",
    "20261021-2253": "run 1, 21/10 22:53",
    "20261021-2258": "run 2, 21/10 22:58",
    "20261021-2301": "run 3, 21/10 23:01",
    "20261022-1602": "run 4, 22/10 16:02",
}

GROUPS = [
    ("1. Phân biệt phiên bản và thời điểm có hiệu lực của tài liệu", [1, 2, 18, 21]),
    ("2. Kiểm soát quyền truy cập theo bối cảnh người dùng", [5, 6, 10, 13, 22]),
    ("3. Xử lý thông tin mâu thuẫn giữa nhiều nguồn/cấp tổ chức", [3, 7, 12, 19, 20, 15, 17]),
    ("4. Từ chối hoặc thể hiện rõ khi chưa đủ căn cứ", [8, 9, 11, 14, 16]),
    ("Other: finding the right clause", [4]),
]
CARD = {"answer": "Answer card", "conflict": "Conflict card", "refusal": "Refusal card"}
EXPECTED = {"answer": "an answer card", "conflict": "a conflict card", "refusal": "a refusal card"}

rows = load_test_cases()
by_id = {r["id"]: r for r in rows}
personas = load_personas(load_org())
settings = load_config().eval
titles = {d.id: d.title for d in load_documents()}


def REV(files):
    from appota_kb.evaluation.review import load_reviews
    return load_reviews(R / f"{files[0]}.review.yaml") if files[0] == "20261022-1602" else {}


def scored(files):
    records = [rec for f in files for rec in load_run(R / f"{f}.jsonl")]
    scores = score_all(rows, records)
    return scores, verdicts(scores, REV(files))


def contains(text, needle):
    """The substring check of evaluation/score.py: NFC, whitespace folded, casefolded."""
    return fold(needle).casefold() in fold(text).casefold()


def reasons_of(score):
    """Why one run of a row failed, in plain words, as (unsafe reasons, other reasons).

    The unsafe reasons are the checks of evaluation/score.py that set `unsafe`: an answer card where there
    should be none, a key fact missing from the model's sentence, a document the model must not use.
    """
    row, card, checks = score.row, score.record["card"], score.checks
    unsafe, other = [], []
    if checks.get("card") is False:
        (unsafe if score.unsafe else other).append(f"should have been {EXPECTED[row['card']]}")
    else:
        # A line is a {kind, text} record, or a flat string in the Mission 2 runs.
        shown = "\n".join(line.get("text", "") if isinstance(line, dict) else str(line)
                          for line in card.get("lines") or [])
        key_missing = [t for t in row.get("key_facts", [])
                       if checks.get("key_facts") is False and not contains(card.get("answer_text") or "", t)]
        if key_missing:
            unsafe.append("missing " + ", ".join(f"'{t}'" for t in key_missing))
        show_missing = [t for t in row.get("must_show", [])
                        if not contains(shown, t) and t not in key_missing]
        if show_missing:
            other.append("missing " + ", ".join(f"'{t}'" for t in show_missing))
        cited = {c.rsplit("#", 1)[0] for c in card.get("cited", []) or []}
        uncited = [d for d in row.get("must_cite", []) if d not in cited]
        if uncited:
            other.append("does not cite " + ", ".join(f"'{titles[d]}'" for d in uncited))
        if checks.get("conflict_pair") is False:
            other.append("the conflict card names the wrong documents")
    if score.rules_wrong:
        other.append("the scope built by the rules is wrong")
    if score.leak:
        other.append("leak of restricted text")
    if checks.get("no_forbidden_for_llm") is False:
        unsafe.append("cites a document the model must not use")
    if checks.get("only_allowed_citations") is False:
        other.append("cites a document that is not allowed")
    if score.unsafe != bool(unsafe):
        raise SystemExit(f"row {row['id']}: unsafe is {score.unsafe} but unsafe reasons are {unsafe!r}")
    return unsafe, other


def outcome(score, verdict):
    """One run of one row, in a few words: the card, then passed, failed with its reasons, or waiting for Hiep."""
    card = CARD[score.record["card"]["kind"]]
    unsafe, other = reasons_of(score)
    if (verdict == "Chưa đạt") != bool(unsafe or other):
        raise SystemExit(f"row {score.row['id']}: verdict {verdict!r} but reasons {unsafe + other!r}")
    if unsafe:
        also = f"; also {'; '.join(other)}" if other else ""
        return f"{card}, failed, unsafe answer: {'; '.join(unsafe)}{also}"
    if verdict == "Chưa đạt":
        return f"{card}, failed: {'; '.join(other)}"
    if verdict == "Đạt":
        return f"{card}, passed"
    return f"{card}, waiting for Hiep's reading"


def cell(runs, row_id):
    seen = Counter()
    n = 0
    for _, files in runs:
        scores, verdict = scored(files)
        score = next(s for s in scores if s.row["id"] == row_id)
        if score.record is None:
            continue
        n += 1
        seen[outcome(score, verdict[row_id])] += 1
    if n == 0:
        return "-"
    return "<br>".join(f"{text}: {k}/{n}" for text, k in seen.most_common())


for title, ids in GROUPS:
    print(f"\n### {title}\n")
    print("| Row | Kind | Asker, date | Question | Mission 2 | Mission 3 |")
    print("|---|---|---|---|---|---|")
    for i in ids:
        r = by_id[i]
        print(f"| {i} | {r['kind']} | {personas[r['persona']].name}, {r['as_of']:%d/%m/%Y} | {r['questions'][0]} "
              f"| {cell(M2, i)} | {cell(M3, i)} |")

print("\n### Gates, per run\n")
print("| Version | Run | Rows counted | Rules wrong | Leaks | Unsafe answers | Over-cautious | Answer cards to read |")
print("|---|---|---|---|---|---|---|---|")
for version, runs in (("Mission 2", M2), ("Mission 3", M3)):
    for name, files in runs:
        scores, _ = scored(files)
        g = {x.name: x for x in gates(scores, REV(files), settings, personas)}
        n = g["Leaks"].n
        faithful = next(x for x in g.values() if x.name.startswith("Faithfulness"))
        label = " + ".join(f"[{LABEL[f]}](../../results/{f}.jsonl)" for f in files)
        print(f"| {version} | {label} | {n} | {g['Rules correct in every case'].k} | {g['Leaks'].k} "
              f"| {g['Unsafe answers (card)'].k} | {next(x for x in g.values() if x.name.startswith('Over')).k} "
              f"| {faithful.n} |")
```

</details>
