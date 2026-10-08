# Review output: new reader, Phase 5 document

## Run details and limits

- **Prompt:** `docs/mission1/review_prompt_reader.md`, main prompt plus all optional modules A-E.
- **Reviewer:** Claude Opus 5.5 in Claude Code, on 08/10/2026.
- **Input:** `build/mission1_draft.pdf` rendered from the current `docs/mission1/document.md` (5 pages), plus `mission1_brief.md` and `rules.md`.
  Quotes were copied from `document.md`, which has the same text as the PDF.
- **Not independent.**
  The reviewer is the same model family that drafted the document.
  The session had also loaded `AGENTS.md`, which states the core thesis and working rules, so this was not a fully cold read.
  The brief and rules were read in the same step as the document, before Parts 1-3 were written, which the prompt says not to do.
  Run the prompt again on GPT or Gemini for a truly independent review.

---

## Part 1 - Cold read

### 1. First half page

**[Reader]** The document proposes a RAG assistant for internal policies in which deterministic rules over document metadata first decide which documents are allowed, in force and applicable to the asker, and only then does AI search and answer inside that set.
The reason given is that a relevant document is not necessarily allowed, valid or applicable, and when the rules cannot decide, the system says so and points to a person instead of guessing.
The box does not say who the user is or what outcome they get, so a reader does not yet know why this matters to anyone.

### 2. Teach-back

- **Section 1.** **[Reader]** Employees do not know which rule applies to them, and the danger is a confident answer from the wrong document: six leave policies say 12-16 days and only one is right for a GameCo employee today.
  The author separates relevant/allowed, allowed/applicable and newest/in force, and chooses "wrong rule" over "leak" as the problem because leaks can be blocked structurally.
  Main users are employees making a decision; secondary users are HR document owners; scope is annual leave.
- **Section 2.** **[Reader]** Rules build a per-person "search scope" from metadata (version chain, status, dates, access, applicability, declared overrides), then normal RAG runs inside it, and a final rule picks one of three answer cards (answer, conflict, refusal).
  The order of the steps matters, and a new version takes over on its effective date without code changes.
- **Section 3.** **[Reader]** AI only retrieves and writes; everything about access, validity, applicability, precedence and card type is rules.
  The remaining risk is the LLM citing an in-scope document that does not answer the question.
  Data is 10 simulated Markdown documents; people are involved as owners, unit HR and employees who report errors.
- **Section 4.** **[Reader]** Three decisions: owners declare overrides instead of the LLM choosing; retrieval inside the rule scope instead of LLM topic classification first; open to employees directly instead of HR-first.
  Each has a cost and a switch condition.
  Two failure cases: owners declare wrongly, and partial overrides are not supported.
- **Section 5.** **[Reader]** A test set of 10 questions, 3 phrasings, 3 runs each, with thresholds that gate release and an honest note that 0/30 errors only bounds the rate at about 9.5%.
  Build order: rules and tests, then RAG, then a minimal UI, then a naive RAG comparison that is cut first.

### 3. Where attention dropped

- **[Reader]** Section 2, "Thứ tự các bước có lý do": re-read twice and still could not see why "bản 1 không quay lại" depends on the order.
- **[Reader]** Section 2, flow box 4 "Đánh dấu cặp mâu thuẫn chưa khai báo / 0 cặp": it is not clear how the system knows two documents conflict.
- **[Reader]** Section 2, box 7 "Chọn thẻ theo văn bản được trích": "thẻ" is used before the three cards are introduced, so the box was unclear until the table below.
- **[Reader]** Section 3, "Lỗ hổng còn lại" example: had to stop and reconcile it with Section 1, which says HR Tập đoàn can read the GameCo policy.
- **[Reader]** Section 4, Decision 2 example (PayCo overtime leading to a leave conflict card): re-read; the chain of reasoning is compressed into two sentences.
- **[Reader]** Section 5, thresholds table: started skimming; the "Bước" column ("Luật", "Sinh", "Truy xuất, sinh") needs decoding.
- **[Reader]** The flow starts with "10 văn bản" but only 6 are ever named, plus the salary scale; the 4 documents left in scope are never listed.

---

## Part 2 - Hard to understand

### Passages

1. **"Bỏ văn bản đã bị 'dùng thay'"** (Section 2, flow box 3).
   - Type: unnatural Vietnamese, term used inconsistently.
   - "A dùng thay B" means A is used instead of B, so "văn bản đã bị dùng thay" reads as "the document that was used instead", which is the opposite of what is removed.
     The author means: remove the document that another document is declared to replace for this person (here the Tập đoàn policy).
   - Severity: **High**, because this is the step that implements the key precedence idea.
2. **"Bước 1 chạy trước khi lọc theo người hỏi, vì bản nào thay bản nào thì như nhau với mọi người; nhờ vậy, khi bản 3 thay bản 2 vào 01/01/2027, bản 1 không quay lại."** (Section 2).
   - Type: jump in reasoning, example does not support the point.
   - Understood: version selection is global, not per person.
     Not understood: why bản 1 would ever come back; the example needs the other order to be shown failing (for example, if a person could not see bản 2, "latest version they can see" would return bản 1).
   - Severity: **Medium**.
3. **"Đánh dấu cặp mâu thuẫn chưa khai báo"** (Section 2, box 4) and **"chưa khai báo thì hai văn bản cùng áp dụng là mâu thuẫn"** (Section 2, metadata list).
   - Type: missing context (how).
   - Understood, by inference: two in-scope documents with the same "Chủ đề" and no declared "dùng thay" or "bổ sung" relation are a conflict pair.
     This is never stated as a rule, and the role of "Chủ đề" in it is not mentioned.
   - Severity: **High**, since the conflict card and Mandatory Question 3 depend on it.
4. **"Văn bản nguy hiểm nhất là văn bản giống văn bản đúng nhất."** (Section 1).
   - Type: ambiguous Vietnamese.
   - It can be parsed as "most similar to the correct document" or "similar to the most correct document".
     The intended meaning (the first) is a strong line and worth keeping once disambiguated.
   - Severity: **Low**.
5. **"phạm vi"** used for three things (opening box "trong phạm vi đó"; Section 1 "nằm trong phạm vi họ được xem"; Section 2 "phạm vi áp dụng" and "phạm vi tìm kiếm").
   - Type: term used inconsistently.
   - "Phạm vi tìm kiếm" is the central term; "phạm vi áp dụng" is one of its inputs; "phạm vi họ được xem" is another input.
     A reader can mix them up, especially in the test table ("mọi văn bản trong phạm vi của người hỏi").
   - Severity: **Medium**.
6. **"thay thế"** (versions, Section 1 table "đã bị bản 2 thay thế") versus **"dùng thay"** (cross-unit override).
   - Type: term used inconsistently.
   - Two different mechanisms with near-identical Vietnamese words; Section 4 Decision 1 also quotes "quy chế này thay thế quy chế Tập đoàn", which is the override meaning, not the version meaning.
   - Severity: **Medium**.
7. **"Bộ quy định ≤ 4 văn bản nên ngưỡng vô nghĩa"** (Section 5, Context recall row).
   - Type: undefined term.
   - "Bộ quy định" is not defined anywhere; it seems to mean "phạm vi tìm kiếm".
   - Severity: **Low**.
8. **"Ở bước 7, nếu câu trả lời trích một văn bản thuộc cặp mâu thuẫn, hệ thống hiện thẻ mâu thuẫn."** together with **"Quy chế Tập đoàn (từ 01/01/2024): 12 ngày. Quy chế PayCo (từ 01/01/2025): 13 ngày."** (conflict card).
   - Type: missing context.
   - Where do the two numbers on the conflict card come from: the LLM, or a fixed field?
     If the LLM writes them, the conflict card is not purely rule-built, which matters for the "Luật, 100%" threshold.
   - Severity: **Medium**.
9. **"Tôi không chọn nó vì vị trí của lỗi AI."** (Section 4, Decision 2).
   - Type: reads like a translation ("because of where the AI error sits").
   - Severity: **Low**.
10. **"Hai việc này được giao cho AI vì khi AI làm sai, lỗi rơi về phía an toàn hoặc bị luật chặn lại."** (Section 3).
    - Type: calque of "fails safe"; also overclaims, since the next paragraph ("Lỗ hổng còn lại") describes an AI error that is neither safe nor blocked.
    - Severity: **Medium**.
11. **"Ngày"** column header (Section 1 table).
    - Type: ambiguous ("date" or "days").
    - Severity: **Low**.
12. **"Kiểm bằng mã đoạn"** (Section 5 thresholds).
    - Type: undefined term ("chunk ID").
    - Severity: **Low**.
13. **"Lỗi nguy hiểm: trả lời khi phải từ chối, sai ý chính, trích văn bản cấm"** (Section 5).
    - Type: term used inconsistently; the test table calls this list "Không được trích", the threshold calls it "văn bản cấm".
    - Severity: **Low**.
14. **"nhân sự PayCo, Kế toán"**, **"Nhân viên HR Tập đoàn"**, **"chỉ HR GameCo được xem"**.
    - Type: missing context.
    - The profile is "đơn vị và vai trò", but it is not clear whether "Kế toán" and "HR" are units (phòng) or roles; access by "HR GameCo" depends on which.
    - Severity: **Low**.

### Needs more explanation

1. **"Phạm vi tìm kiếm của một người gồm những văn bản họ được xem, đang có hiệu lực và áp dụng cho đơn vị của họ."** (Section 2).
   - Judge's question: "So a person can never ask about another unit's policy, even one they are allowed to read?"
   - Needs: one sentence stating that v1 answers only questions about the asker's own rules, and why.
2. **"Ở bước 7 ... Nếu không còn trích dẫn hợp lệ nào, hệ thống từ chối."** and **"Nếu LLM trích một văn bản nằm ngoài phạm vi tìm kiếm, luật bỏ trích dẫn đó."** (Sections 2-3).
   - Judge's questions: "How can the LLM cite a document outside the scope if it only received in-scope chunks?" and "If one citation is dropped but others remain, what happens to the sentence that relied on the dropped one?"
   - Needs: one sentence.
3. **"Mỗi khi có văn bản mới, cùng bộ luật này chạy cho mọi đơn vị và báo cho chủ sở hữu các cặp mâu thuẫn chưa khai báo, trước khi có ai hỏi."** (Section 2).
   - Judge's question: "Then why does the PayCo accountant still get a conflict card? Is publishing blocked until the owner declares, or only warned?"
   - Needs: one sentence.
4. **"Dùng thay (overrides): 'Nghỉ phép Tập đoàn'."** (Section 2).
   - Judge's question: "Does GameCo override the whole Tập đoàn chain or one version? If Tập đoàn later raises leave to 15 days, do GameCo staff stay at 14?"
   - Needs: one sentence.
5. **"Hệ thống không tự suy ra 'đơn vị cấp dưới thắng'"** (Section 2).
   - Judge's question: "Why not? Most-specific-wins is the common default."
   - Needs: one sentence with a reason, ideally in Section 4.
6. **"bản tương lai không hiển thị trước ngày có hiệu lực"** (Section 4, Giả định).
   - Judge's question: "An employee in October planning leave over the New Year needs bản 3. Why hide an issued version?"
   - Needs: one sentence.
7. **"các yêu cầu xin quyền xem"** (Section 3, HR role).
   - Judge's question: "How does an employee request access to a document the refusal card deliberately does not reveal?"
   - Needs: one sentence, or remove the phrase.
8. **"Khoảng 45 câu trả lời, đọc tay hết"** (Section 5).
   - Judge's question: "Where does 45 come from: 90 runs, of which about half are answer cards?"
   - Needs: a few words.
9. **"quá 1/10 thì nhân sự bỏ dùng"** (Section 5).
   - Judge's question: "Is this measured or assumed?"
   - Needs: label it as an assumption.
10. **"thí điểm"** (Section 4 Decision 3; Section 5).
    - Judge's question: "Who is in the pilot, how long, and what confirms a 'báo sai'?"
    - Needs: one sentence.
11. **"Một retriever đơn giản"** with **"kể cả khi câu hỏi diễn đạt khác hoặc gõ không dấu"** (Section 3).
    - Judge's question: "Which retriever handles unaccented Vietnamese and paraphrase?"
    - Needs: a few words (for example keyword search after removing diacritics, or embeddings).
12. **"Bước 7 ... Luật"** with threshold **"Đúng phạm vi tìm kiếm và loại thẻ | Luật | 100% | Luật luôn cho cùng kết quả"** (Sections 2 and 5).
    - Judge's question: "The card type depends on what the LLM cited, which varies between runs; how is that a deterministic rule result?"
    - Needs: one sentence (the rule is deterministic given the citations; the test fixes the citations).

**Explains more than a reader needs.**
- **[Opinion]** Section 3 "Nếu truy xuất bỏ sót, câu trả lời yếu đi hoặc thành từ chối..." and Section 4 Decision 2 "một lần bỏ sót chỉ làm câu trả lời yếu đi hoặc thành từ chối" say the same thing; keep one.
- **[Opinion]** The Context recall row in Section 5 has no threshold and says itself the threshold is meaningless; it could become half a sentence.
- **[Opinion]** Section 1 "Người dùng chính... làm thêm giờ, đi công tác" lists cases that the scope line then excludes; one example is enough.

### Terms a reader must learn

| Term | Defined? | Where | Clear enough? |
|---|---|---|---|
| naive RAG | Yes | Section 1, in parentheses | Yes |
| RAG, retrieval, generation | Partly | Section 2 | Yes for the audience |
| metadata | No | - | Yes for the audience |
| phạm vi tìm kiếm | Yes | Section 2, first paragraph | Yes, but "phạm vi" is overloaded (Part 2, item 5) |
| chuỗi phiên bản | Yes | Section 2 metadata list | Yes |
| dùng thay (overrides) | Yes | Section 2 metadata list | Definition is clear; flow box 3 phrasing reverses it |
| bổ sung (complements) | Yes | Section 2 metadata list | Yes, but its role in conflict detection is implicit |
| cặp mâu thuẫn (chưa khai báo) | No | Used in Section 2 box 4 | No (Part 2, item 3) |
| thẻ (trả lời / mâu thuẫn / từ chối) | Yes | Section 2 "Ba loại thẻ kết quả" | Yes, but used one box earlier |
| chủ sở hữu văn bản | Yes | Section 1 "Người dùng thứ hai" | Yes |
| văn bản mật | No | Section 2 | Understandable, but no "mật" field exists in the metadata list |
| ca | Implicit | Section 5 | Yes |
| Faithfulness, Context recall | Yes | Section 5 table | Yes |
| thí điểm | No | Sections 4 and 5 | No |
| bộ quy định | No | Section 5 | No |

---

## Part 3 - Controversial points and conflicts

### Controversial points

1. **"Phạm vi tìm kiếm của một người gồm những văn bản họ được xem, đang có hiệu lực và áp dụng cho đơn vị của họ."** with the example **"nhân viên HR Tập đoàn hỏi 'Nhân sự GameCo được nghỉ phép năm bao nhiêu ngày?' ... kết quả đúng là từ chối."** (Sections 2-3) **[Reader]**
   - Counterargument: HR Tập đoàn, managers and people moving between units legitimately need another unit's rules, and the document itself says HR Tập đoàn may read the GameCo policy.
     Refusing a question whose answer the asker is allowed to open looks like a product failure, not safety.
   - Answered? Only partly: the design treats it as correct, but never says why "about another unit" questions are out of scope or how they would be handled later.
2. **"Vì vậy 'không rò rỉ' là điều kiện bắt buộc của mọi phương án, không phải vấn đề để chọn."** (Section 1) **[Opinion]**
   - Counterargument: the brief's core question names "quyền truy cập" explicitly; declaring access solved by one filter could read as sidestepping half the brief, and real access is rarely a clean role check (secondments, project groups, section-level secrecy).
   - Answered? Partly: the filter-before-retrieval argument is sound for leakage, but the access model itself (who sees what, defined how) is one line.
3. **"Một hệ thống naive RAG ... sẽ xếp sáu văn bản này gần ngang nhau ... Vì vậy câu trả lời có thể là 12, 13, 15 hay 16 ngày"** (Section 1) **[Opinion]**
   - Counterargument: a naive RAG whose chunks carry the version and date text, with a capable LLM, may often pick the right one; the motivating failure is predicted, not shown.
   - Answered? Partly: Section 5 plans the comparison, but it is "phần bỏ đầu tiên nếu trễ", so the central claim may never be measured.
4. **Decision 1, owners declare overrides** (Section 4) **[Opinion]**
   - Counterargument: the obvious alternative is not "LLM chooses" but a fixed rule "đơn vị cấp dưới thắng" (most specific wins), which needs no declaration and is deterministic; a second strong alternative is the LLM proposing the relation at publish time and the owner confirming it.
   - Answered? The first is dismissed in Section 2 without a reason ("Hệ thống không tự suy ra..."); the second may be what "LLM được thêm gợi ý" means, but the sentence is ambiguous.
5. **Decision 2, "khi truy xuất trong phạm vi tìm kiếm, một lần bỏ sót chỉ làm câu trả lời yếu đi hoặc thành từ chối"** (Section 4) **[Reader]**
   - Counterargument: the comparison is asymmetric; for classification it counts wrong-topic errors, for retrieval it counts only misses, but retrieval can also return a wrong in-scope document, which is exactly the "Lỗ hổng còn lại" of Section 3.
   - Answered? Not in Decision 2.
6. **Decision 3, "cho nhân sự hỏi trực tiếp ngay từ phiên bản đầu"**, with **"nguồn ghi trên thẻ và nút 'Báo sai' là cách phát hiện"** (Section 4) **[Reader]**
   - Counterargument: Section 1 says the worst errors are the ones where "câu trả lời sai trông giống hệt câu trả lời đúng"; relying on employees to spot them with "Báo sai" contradicts that, and HR-first for a few weeks is a common, low-cost way to gain trust and collect real questions.
   - Answered? Partly: rules cover version and access, and tests gate release; but the document does not say why employees can catch the remaining LLM wording errors, and the HR-first option is described as permanent ("giữ nguyên việc chờ") rather than as a short phase.
7. **"bản tương lai không hiển thị trước ngày có hiệu lực"** (Section 4, Giả định) **[Opinion]**
   - Counterargument: announced changes matter for planning; hiding an issued bản 3 in October can cause the very wrong decision the document fears (planning leave around 01/01/2027 on the old count).
   - Answered? No; stated as an assumption without reason.
8. **"Lỗi này xảy ra hằng ngày"** (Section 1) **[Reader]**
   - Counterargument: no evidence of frequency is given, and the data is simulated.
   - Answered? No; it reads as an observed fact.
9. **"Bổ sung (complements)" declared per pair by the owner** (Sections 2-3) **[Opinion]**
   - Counterargument: if every pair of same-topic documents without a relation becomes a conflict, the number of declarations grows with each new guide or form, and owners may declare "bổ sung" just to silence warnings, which is the first failure case in Section 4.
   - Answered? Partly: the failure case is named, but not the incentive that causes it.

### Conflicts

1. **Section 1 vs Section 3.**
   - "**Được xem ≠ áp dụng cho mình:** nhân viên HR Tập đoàn đọc được quy chế GameCo" vs "Quy chế GameCo không áp dụng cho người này nên không nằm trong phạm vi tìm kiếm của họ, và kết quả đúng là từ chối."
   - Not a logical contradiction, but a reader takes Section 1 as "they can see it" and is surprised that the system refuses to talk about it.
     I think the text is incomplete rather than wrong: Section 2 should say that questions about other units are out of v1.
2. **Section 1 vs Section 4 Decision 3.**
   - "câu trả lời sai trông giống hệt câu trả lời đúng" vs "nguồn ghi trên thẻ và nút 'Báo sai' là cách phát hiện".
   - The second relies on users noticing what the first says they cannot notice.
     I cannot tell which the author would change; at minimum Decision 3 needs a sentence on why the remaining errors are detectable.
3. **Section 3, first paragraph vs "Lỗ hổng còn lại".**
   - "khi AI làm sai, lỗi rơi về phía an toàn hoặc bị luật chặn lại" vs "Luật không chặn được trường hợp LLM trích một văn bản nằm trong phạm vi tìm kiếm nhưng không trả lời câu hỏi".
   - The first sentence is wrong as written; it should say "hầu hết".
4. **Section 2 refusal design vs Section 3 HR role.**
   - "Câu từ chối giống hệt nhau dù lý do là không có quyền hay không có văn bản, để không lộ rằng có một văn bản mật." vs "HR đơn vị của người hỏi nhận ... các yêu cầu xin quyền xem."
   - An employee cannot request access to a document whose existence is hidden.
     I think the access-request phrase is the one to cut or explain.
5. **Section 2 promises vs Section 5 MVP.**
   - "báo cho chủ sở hữu các cặp mâu thuẫn chưa khai báo, trước khi có ai hỏi" and the conflict card's "Đã ghi nhận để HR Tập đoàn và HR PayCo xác nhận" vs the MVP list, which only builds an employee-facing page and a "Báo sai" button.
   - I cannot tell whether the owner notification and the HR queue are in v1.
     If not, the card text promises something v1 does not do.
6. **Section 5 thresholds vs Section 2 step 7.**
   - "Đúng phạm vi tìm kiếm và loại thẻ | Luật | 100% | Luật luôn cho cùng kết quả" vs "7. Chọn thẻ theo văn bản được trích", which depends on the LLM's citations.
   - Likely both are right if the test feeds fixed citations to the rule, but as written they conflict.
7. **Section 5 "Bốn ngưỡng đầu là điều kiện để mở cho nhân sự" vs Decision 3 "nếu bộ test không đạt các ngưỡng ở Phần 5".**
   - Decision 3 refers to all thresholds; Section 5 says only the first four gate release; "Từ chối nhầm ≤ 3/30" is then neither a gate nor clearly tied to Decision 2's switch condition until you cross-read.
   - Minor; I think Decision 3 should say "bốn ngưỡng đầu".
8. **Section 5 test table, rows 1 and 2.**
   - Row 1 lists "Tập đoàn, GameCo bản 1, 3, 4, PayCo" as not-to-cite; row 2 (same question on 01/01/2027) lists only "GameCo bản 2".
   - A reader may think bản 1, bản 4, Tập đoàn and PayCo become citable on 01/01/2027.
     I think row 2 is incomplete.
9. **Opening box vs Sections 3-4.**
   - "Khi luật không xác định được văn bản nào đúng, hệ thống nói rõ và chỉ người cần hỏi" vs refusals that also come from AI ("Nếu truy xuất bỏ sót, câu trả lời yếu đi hoặc thành từ chối").
   - Minor; the box is a simplification.
10. **"Bộ quy định ≤ 4 văn bản"** (Section 5) vs **"Phạm vi tìm kiếm: 4 văn bản"** (Section 2).
    - Same thing, two names (Part 2, item 7).

---

## Part 4 - Match against the brief and rules

### Requirements table

| Requirement (brief or rules) | Where the document answers it | Verdict | Reason |
|---|---|---|---|
| **[Brief]** 01 PDF/DOCX, at most 5 pages | Whole PDF | **Met** | 5 pages; but "Ứng viên: [Họ tên]" is still a placeholder. |
| **[Brief]** Simulated data, not real Appota data | Opening box: "Mọi đơn vị, nhân sự, văn bản và con số trong tài liệu là **giả lập**." | **Met** | Clearly stated. |
| **[Brief]** Tables, diagrams allowed | Section 1 table, Section 2 flow, cards, Section 5 tables | **Met** | Used well. |
| **[Brief]** S1: Vấn đề thực sự là gì? | "nhân sự không biết chắc quy định nào đang áp dụng cho chính mình" | **Met** | Concrete and backed by the six-document example. |
| **[Brief]** S1: Ai gặp vấn đề đó? | "Người dùng chính ... Người dùng thứ hai ..." | **Met** | Two user groups with distinct needs. |
| **[Brief]** S1: Kết quả họ thực sự cần là gì? | "Kết quả họ cần là quyết định đúng ngay lần đầu, không phải chờ HR trả lời." | **Met** | Clear outcome, though never measured later. |
| **[Brief]** S2: Hướng giải quyết | "luật xác định phạm vi tìm kiếm của người hỏi trước, rồi AI mới tìm và trả lời" | **Met** | Stated in one sentence. |
| **[Brief]** S2: Luồng chính của sản phẩm | 7-step flow, three cards | **Partly met** | The system pipeline is clear, but the product flow is not: where the employee asks, how identity is known, what happens after a refusal or conflict, how HR receives the case. |
| **[Brief]** S3: AI làm gì? | "AI làm hai việc, cũng là hai bước của RAG." | **Met** | Precise. |
| **[Brief]** S3: Không nên làm gì? | "AI không làm những việc mà chỉ một lỗi cũng thành câu trả lời sai tự tin" | **Met** | Strong, with reasons. |
| **[Brief]** S3: Cần dữ liệu/công cụ gì? | "10 văn bản giả lập dạng Markdown ... Một retriever đơn giản và một LLM có sẵn" | **Partly met** | Data is clear; the retriever and LLM are not named. |
| **[Brief]** S3: Con người tham gia ở đâu? | "Con người tham gia ở ba chỗ" | **Met** | Three roles, though the access-request role conflicts with the refusal design. |
| **[Brief]** S4: Các lựa chọn quan trọng | Decisions 1-3 | **Met** | Three real decisions. |
| **[Brief]** S4: Trade-off | "Cái giá là ..." in each decision | **Met** | Cost and switch condition each time. |
| **[Brief]** S4: Tình huống có thể khiến giải pháp thất bại | Lỗ hổng (S3), two failure cases (S4), "Giả định rủi ro nhất" (S5) | **Met** | Honest; spread over three sections. |
| **[Brief]** S5: Làm thế nào để biết giải pháp tốt hay chưa? | Test set, thresholds, pilot "tỷ lệ báo sai" | **Partly met** | Strong correctness gate, but no measure of the user outcome from Section 1 (decisions made without waiting for HR, fewer repeat questions to HR). |
| **[Brief]** S5: Phần nào hiện thực hóa trước? | "Nếu chỉ có thời gian ngắn, làm theo thứ tự này" | **Met** | Ordered, with what to cut first. |
| **[Brief]** Core question: đúng thông tin, đúng đơn vị, đúng quyền truy cập | Search scope from unit, access and validity | **Met** | Directly answered; "đúng thông tin mình cần" is narrowed to "rules that apply to me" (Part 3, item 1). |
| **[Brief]** Levels Tập đoàn → Công ty → Phòng ban → Nhóm | "đơn vị (Tập đoàn → GameCo → Studio)" | **Partly met** | Three levels shown; "Nhóm" never appears, though the rules seem to generalise. |
| **[Brief]** "nhiều loại tài liệu và phiên bản" | Scope: HR policies, annual leave | **Partly met** | Versions are covered deeply; document types are deliberately narrowed, with a reason. |
| **[Brief]** Brief example: same leave question, two units, different answers | GameCo vs PayCo, cards | **Met** | Mirrors the brief exactly. |
| **[Brief]** "Ưu tiên chất lượng tư duy, khả năng lựa chọn và lý do" | Sections 1 and 4 | **Met** | Reasons and costs are given throughout. |
| **[Brief]** 40% Khung vấn đề | Section 1, three separations | **Met** | See below. |
| **[Brief]** 35% Thực thi | Sections 2 and 5, rule script | **Partly met** | Buildable and partly run, but the run is not visible to judges. |
| **[Brief]** 25% Chất lượng quyết định | Section 4 | **Met** | Format is strong; see weaknesses below. |
| **[Brief]** Rules 05: Vietnamese + English, clarity first | Throughout | **Met** | English terms are glossed. |
| **[Brief]** Rules 03: no plagiarism, credit sources | No sources cited | **Met** | Nothing appears copied; "Faithfulness" and "Context recall" are common RAG evaluation terms and could be credited in one word if the author took them from a framework. |

Not in scope of this PDF review: the 3 Forced Decision answers and the evidence log, which are submitted separately.
The document does support Mandatory Question 3 well (version step plus conflict card).

### Content the brief did not ask for

- **[Opinion]** Little; almost everything serves a requirement.
  The step-order paragraph and the Context recall row are the weakest uses of space relative to the confusion they create or the value they add.

### Per criterion

- **40% Khung vấn đề.**
  Earns it: the six-document table, "Văn bản nguy hiểm nhất là văn bản giống văn bản đúng nhất", the three separations, and the explicit choice of "wrong rule" over "leak" as the problem.
  Weakest: access is declared solved in one line; the user outcome from Section 1 is never measured; questions about another unit are silently out of scope.
- **35% Thực thi.**
  Earns it: concrete flow with counts, three cards, a test set with forbidden citations, thresholds, build order, and "Phần luật của cả 10 câu đã chạy đúng bằng một script".
  Weakest: judges cannot see the script or its output; the retriever and LLM are unnamed; the product flow (UI, identity, HR queue) is thin; some promises (owner notification) are not in the MVP list.
- **25% Chất lượng quyết định.**
  Earns it: every decision states the rejected option's real advantage, the cost of the choice, and what evidence would make the author switch.
  Weakest: Decision 1 skips "most specific wins"; Decision 2's comparison is asymmetric; Decision 3 is in tension with Section 1 and frames HR-first as permanent.

---

## Part 5 - How to make it easier to read and understand

Ordered by how much each change helps a first-time reader.

1. **Say what v1 answers and what it does not, in Section 2.**
   Fixes Part 3 controversy 1 and conflict 1; Part 2 "Needs more explanation" 1.
   ví dụ: "Phiên bản đầu chỉ trả lời câu hỏi về quy định áp dụng cho chính người hỏi; câu hỏi về quy định của đơn vị khác chuyển cho HR."
   Room: cut the duplicate "Nếu truy xuất bỏ sót..." paragraph in Section 3.
2. **State the conflict rule once, where it is used.**
   Put it in box 4 or right below the flow: two in-scope documents with the same topic and no declared relation form a conflict pair.
   Fixes Part 2 passage 3 and term table "cặp mâu thuẫn".
3. **Fix the wording of flow box 3 and separate "thay thế" from "dùng thay".**
   Fixes Part 2 passages 1 and 6.
   ví dụ: "3. Bỏ văn bản đã có văn bản khác được khai báo dùng thay".
   Use "bản mới thay bản cũ" only for versions and "dùng thay" only for cross-unit overrides, including in Decision 1.
4. **Add one sentence in Decision 1 on why not "đơn vị cấp dưới thắng", and rewrite the switch condition.**
   Fixes Part 3 controversy 4 and Part 2 "Needs more explanation" 5.
   Make clear whether "LLM được thêm gợi ý" means the LLM suggests a relation at publish time for the owner to confirm.
   Room: shorten "Phương án đó có ưu điểm thật: ..." to two advantages.
5. **Resolve the tension between Section 1 and Decision 3.**
   Fixes conflict 2 and controversy 6.
   Say which errors can still reach an employee after the rules and the test gate, why the citation lets them check (article number and number of days on the card), and what the pilot is (who, how long, how a report is confirmed).
6. **Rewrite the step-order paragraph around a failure of the other order.**
   Fixes Part 2 passage 2.
   ví dụ: "Nếu lọc theo người hỏi trước, một người không được xem bản 2 sẽ thấy bản 1 là 'bản mới nhất', dù bản 1 đã hết hiệu lực."
   Only use this if it matches the author's real reason; otherwise state the real one.
7. **Add a user-outcome measure to Section 5.**
   Fixes Part 4 "S5: biết giải pháp tốt" (Partly met).
   For example, during the pilot: share of questions answered without contacting HR, refusal and conflict rate, and confirmed "Báo sai".
   Room: turn the Context recall row into half a sentence.
8. **Align terms across sections.**
   "phạm vi tìm kiếm" only for the scope; "phạm vi xem" and "phạm vi áp dụng" for its inputs; replace "Bộ quy định" with "phạm vi tìm kiếm"; use "Không được trích" in both tables; rename column "Ngày" to "Số ngày phép".
   Fixes Part 2 passages 5, 7, 11, 13.
9. **Close the small logic gaps in one clause each.**
   Partial invalid citations at step 7; where the conflict card's numbers come from; publish-time conflicts warn or block; override applies to a chain or a version; why future versions are hidden; drop or explain "yêu cầu xin quyền xem".
   Fixes conflicts 4 and 6 and "Needs more explanation" 2, 3, 4, 6, 7.
10. **Fix the Section 3 overclaim and the Decision 3 threshold reference.**
    "lỗi rơi về phía an toàn" → "hầu hết lỗi..."; "các ngưỡng ở Phần 5" → "bốn ngưỡng đầu ở Phần 5".
    Fixes conflicts 3 and 7.
11. **Complete row 2 of the test table, or add "(chỉ ghi văn bản dễ nhầm nhất)" to the column header.**
    Fixes conflict 8.
12. **Use "thẻ" only after it is introduced, or add "(xem ba loại thẻ bên dưới)" to box 7.**
    Fixes the attention drop at box 7.
13. **Label predictions and assumptions as such.**
    "Lỗi này xảy ra hằng ngày", "sẽ xếp sáu văn bản này gần ngang nhau", "quá 1/10 thì nhân sự bỏ dùng".
    Fixes Part 3 controversies 3 and 8 and Optional A items.

---

## Part 6 - Summary

### The 5 most important problems

1. **The scope rule silently refuses questions about another unit**, even when the asker may read the document, which a reader feels as a conflict with "Được xem ≠ áp dụng cho mình" (Part 3, controversy 1 and conflict 1).
2. **Decision 3 relies on employees spotting errors that Section 1 says look identical to correct answers**, and the pilot that is meant to catch them is never defined (Part 3, controversy 6 and conflict 2).
3. **The conflict mechanism is named but not shown**: how a conflict pair is detected, where the card's numbers come from, and whether publishing warns or blocks; this is also the core of Mandatory Question 3 (Part 2, passages 3 and 8; "Needs more explanation" 3).
4. **Decision 1 does not argue against the most obvious alternative, "đơn vị cấp dưới thắng"**, and its switch condition is ambiguous (Part 3, controversy 4).
5. **Section 5 measures correctness but not the user outcome promised in Section 1**, and the claim that motivates the whole design (naive RAG mixes the six documents) is a prediction whose measurement is cut first (Part 4; Part 3, controversy 3).

Also fix quickly: flow box 3 reads backwards ("đã bị 'dùng thay'"), and "[Họ tên]" is still a placeholder.

### What works well and should be kept

- The opening box: "Một văn bản liên quan tới câu hỏi chưa chắc đã được phép xem, đang có hiệu lực, hay áp dụng cho người hỏi."
- The six-document leave table with one bold correct row; it makes the problem obvious in ten seconds.
- "Văn bản nguy hiểm nhất là văn bản giống văn bản đúng nhất." (after disambiguating).
- The three separations: "Liên quan ≠ được phép xem", "Được xem ≠ áp dụng cho mình", "Mới nhất ≠ đang có hiệu lực".
- The argument that leakage is a constraint and wrong-rule answers are the problem: "'không rò rỉ' là điều kiện bắt buộc của mọi phương án, không phải vấn đề để chọn."
- The flow diagram with document counts at each step and the split between rule steps and AI steps.
- "Bạn đang hỏi với tư cách" on every card, and the identical refusal text that does not reveal a secret document.
- The decision format: real advantage of the rejected option, "Cái giá là ...", and "Tôi sẽ đổi phương án nếu ...".
- The test table's "Không được trích" column and the bold in-scope documents "nên chỉ LLM tránh được".
- "Bốn ngưỡng đầu là điều kiện để mở cho nhân sự, không phải bằng chứng hệ thống luôn đúng." and the 9.5% bound.
- The build order with the naive RAG comparison named as the first cut.

### What a judge would remember

"Rules choose which documents a person may get an answer from and AI only reads inside them, shown by six near-identical leave policies giving 12 to 16 days where only one is right for a GameCo employee today."

---

## Optional A - Claims that need evidence

| Claim | Source shown? | Verdict | Note |
|---|---|---|---|
| Six documents state annual leave "với câu chữ gần như giống nhau" | No (simulated) | Unsure | Plausible for simulated data; not checkable from the PDF. |
| Leave values 12, 13, 14, 15, 16, 13 | Simulated | Confident correct (internally consistent) | Match the cards and the test table. |
| Dates 01/01/2024, 01/01/2025, 01/01/2026, 01/01/2027, question on 07/10/2026 | Simulated | Confident correct (internally consistent) | |
| "naive RAG ... sẽ xếp sáu văn bản này gần ngang nhau" | No | Unsure | **Prediction stated as fact**; Section 5 step 4 would measure it but is cut first. |
| "Lỗi này xảy ra hằng ngày" | No | Unsure | **Assumption stated as fact.** |
| Flow counts 10 → 7 → 5 → 4, 0 conflict pairs | Partly (removals named) | Confident correct (arithmetic) | The 4 remaining documents are not named, so the last count cannot be checked. |
| "Phần luật của cả 10 câu đã chạy đúng bằng một script" | No | Unsure | A measured claim with no visible evidence; consider a link or appendix reference. |
| 10 questions × 3 phrasings = 30 cases; 3 runs each | Yes | Confident correct | |
| "Khoảng 45 câu trả lời" | No | Unsure | Probably about half of 90 runs are answer cards; not explained. |
| "≤ 3/30" and "quá 1/10 thì nhân sự bỏ dùng" | No | Unsure | 3/30 = 1/10, consistent; the "nhân sự bỏ dùng" part is an **assumption stated as fact**. |
| "Đạt 0 lỗi trên 30 ca chỉ cho biết tỷ lệ lỗi thật dưới khoảng 9,5% (độ tin cậy 95%)" | No method named | Confident correct (math) | 1 - 0.05^(1/30) ≈ 0.095. It assumes independent, representative cases; 30 hand-written variants of 10 questions are neither, so the real bound is weaker. The sentence already hedges with "chỉ cho biết". |
| "trạng thái 'dự thảo / đã ban hành' do tôi thêm, đề bài không nêu" | Brief | Confident correct | The brief says "tài liệu nào đang có hiệu lực" but does not mention drafts. |

## Optional B - Are the decisions real choices?

- **Decision 1 (owner declares vs LLM chooses).**
  The rejected option is real: many RAG products let the LLM reconcile conflicting passages.
  Cost ("chủ sở hữu phải khai báo, và kế toán PayCo phải hỏi HR") and switch condition are stated.
  But the strongest competitor, a fixed "most specific unit wins" rule, is not argued, so the chosen option wins against a weaker field than it should.
- **Decision 2 (rule scope then retrieval vs LLM topic classification first).**
  Real alternative: intent routing is common and easy to measure.
  Cost and switch condition are stated and measurable.
  The comparison is asymmetric (Part 3, controversy 5), which makes the rejected option look worse than it is.
- **Decision 3 (direct to employees vs HR-first).**
  Real alternative and arguably the conventional safe default.
  Cost and switch condition are stated, but "nhiều báo sai được xác nhận" is not quantified.
  Framing HR-first as "giữ nguyên việc chờ" treats it as permanent, which is close to setting it up to lose; a time-boxed HR-first phase is the version a competent team would choose.

## Optional C - Can it be built?

Mostly yes, alone, in a few days: 10 Markdown documents, a metadata filter, a small retriever, one LLM call, a rule over citations, one page.
Flags:

- **Retriever unspecified.** "gõ không dấu" and "bỏ từ khóa" need either diacritic normalisation plus keyword search or an embedding model; decide before building.
- **Per-claim citations.** "trích nguồn cho từng ý" and the step 7 rule need structured LLM output mapping each sentence to chunk IDs; this is the riskiest small piece.
- **Behaviour at step 7 with partly invalid citations** is undefined (drop the sentence, drop the answer, or refuse).
- **Owner notification and HR queue** are described in Section 2 and on the conflict card but are not in the MVP list; either add a minimal version (the rule script printing the conflict list) or soften the card text.
- **Access requests** (Section 3) have no flow at all.
- **Cost of evaluation** is small (90 runs plus 90 baseline runs, about 45 answers read by hand); fits.

## Optional D - Questions a judge would ask

1. **"Why does the HR Tập đoàn employee get a refusal about GameCo's leave if they are allowed to read that document?"**
   A strong answer says what v1 deliberately answers (rules for me), why that boundary keeps the applicability guarantee simple, and how an "about another unit" mode would be added later without breaking it.
2. **"Why not just let the lower unit's policy win by default, instead of asking owners to declare?"**
   A strong answer gives a concrete case where the group rule must still apply (a floor or a mandatory rule), compares the cost of a wrong automatic choice with the cost of a conflict card, and says how many declarations owners would actually face.
3. **"You say wrong answers look identical to right ones, yet you rely on employees pressing 'Báo sai'. Which is it?"**
   A strong answer narrows which errors remain after rules and tests, explains why the citation on the card makes them checkable, and defines the pilot and what confirms a report.
4. **"How exactly does the system decide two documents conflict?"**
   A strong answer gives the rule (scope, topic, declared relations), who sets the topic, and what happens if a topic tag is wrong.
5. **"Your test set is 10 questions you wrote yourself. What does passing it prove?"**
   A strong answer calls it a release gate and regression suite, explains how the cases were chosen to be adversarial, why the 9.5% bound is optimistic, and what real-world signal replaces it.
6. **"Have you shown that naive RAG actually fails on your data?"**
   A strong answer is honest about whether the comparison was run, and why the design still holds if naive RAG does well on these six documents.
7. **"Which retriever and LLM, and how do you handle unaccented Vietnamese?"**
   A strong answer names the stack and the normalisation, and ties the choice to the "từ chối nhầm" threshold.
8. **"If Tập đoàn raises leave to 15 days next year, does a GameCo employee stay at 14?"**
   A strong answer explains whether overrides attach to a chain or a version, and how the publish-time check alerts GameCo's owner when Tập đoàn publishes a new version.

## Optional E - Layout and visuals

- **Page 1.** Clean; the opening box and table work.
  "Ứng viên: [Họ tên]" is an unfinished placeholder on the first thing a judge sees.
- **Page 2.** The flow diagram is the visual centrepiece and reads well, but box text is small and boxes 1-2 wrap to five lines; box 3's wording is the backwards "dùng thay" phrase.
  The colours (blue rules, orange AI, green result) carry meaning but have no legend; the "AI"/"Luật" labels help, but row 1 boxes show counts where row 2 shows "AI"/"Luật", so the label slot means different things in the two rows.
- **Page 3.** The cards table is readable.
  The heading "Con người tham gia ở ba chỗ:" is orphaned at the bottom of page 3, with its list on page 4.
- **Page 4.** The densest page: all prose, three decisions with the same structure.
  The bold lead-ins carry it, but it is where a skimming judge is most likely to lose the thread.
- **Page 5.** Two tables and a list fill the page; the thresholds table is clear.
  Bold inside table cells ("**Tập đoàn**", "**mọi văn bản trong phạm vi của người hỏi**") only makes sense after the sentence below the table; consider moving that sentence above it.
