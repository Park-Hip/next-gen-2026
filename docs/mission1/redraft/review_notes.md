# Hiep's review notes on the Phase 5 draft

Hiep annotated `document.md` (as rendered on 08/10, commit `d5226c8`) in Lavish.
Each note is copied verbatim, with the section and the text it is attached to.
Claude does not change the document while notes are being collected.
After the review, each note is sorted into a wording change (Hiep rewrites) or a decision change (checked against `decisions.md` first).

## Notes

### Batch 1 (08/10)

The text in brackets is Claude's reading of a word that looks like a dictation error; the note itself is unchanged.

1. **Title** ("Trợ lý tri thức nội bộ: đúng người, đúng quyền, đúng phiên bản")
   > make this more noticable and use capitalized letters
2. **Section 1, paragraph on the naive chatbot** ("Một chatbot "tìm rồi trả lời" xếp sáu văn bản gần ngang nhau...")
   > The sentence "mo hinh lon hon," I think it's not necessary. We can replace a normal chatbot like a naive RAG. and remove (minh hoa, chua do)
3. **Section 1, "Vì sao chọn vấn đề này, không phải chống rò rỉ."**
   > This is kind of vague and the vietnamese use of this is not very good.
4. **Section 2, "Dữ liệu." paragraph** (profile and metadata fields)
   > This part is hard to read. It's not scannable.
5. **Section 2, the 7-step trace table** (header "Bước và luật")
   > I think we should use a diagram for this not a table.
6. **Section 3, whole section** ("3. AI, dữ liệu & con người")
   > This part, the language used is not very good. It's very hard to understand. The use of a table is not very stylish or the right choice either.
7. **Section 4, whole section** ("4. Quyết định & rủi ro")
   > The structure of UCG's pull points [bullet points] is not very good. It's not very scalable. The language used is terrible also. We cannot see what A is or what B is. It's not very scalable.
8. **Section 4, decision 1, "Vì sao A"** (the example with Hà)
   > who is Hà reader will wonder this
9. **Section 5, "MVP 3 ngày."**
   > This should answer: Nếu chỉ có thời gian ngắn, phần nào cần được hiện thực hóa trước? Not the plan for the MVP.
10. **Overall** (free-form message)
    > So overall the structure is okay but the way they express it, using tables and bullet points, is not very good. It's very hard to scale and the language use in this is terrible, which makes it very hard to understand. For me as a Vietnamese reader there's also no terminology about G, A, R, A, G [RAG] here, which is very bad because it is a RAG system. I think we need to consider whether to use concrete examples in this PDF or we can use a chiral case [general case].

### How batch 1 was handled (Claude, second draft, 08/10)

Notes 1-10 were all applied; details in `decisions.md`, notes under A11 ("Second draft").
Two were applied partly: note 2 keeps a one-sentence label that the naive-RAG answer is a prediction, because the document must not present it as measured; note 10 keeps the concrete example but states each rule in general terms first (the diagram titles and Section 2 text).


### Batch 2 (08/10, second draft)

Written in Lavish while no poll was running, then pasted into the chat by Hiep; copied here verbatim.

1. **Section 1, naive RAG paragraph** ("Đây là dự đoán, chưa phải số đo; Mission 2 sẽ chạy naive RAG trên cùng bộ test ở Phần 5 để kiểm chứng.")
   > remove this sentence
2. **Section 1, persona line** ("Nhân vật giả lập: Minh làm ở phòng Studio của GameCo, Lan làm ở phòng Nhân sự của Tập đoàn, Hà làm kế toán ở PayCo. Gam…")
   > Should we create fake characters for this? When people read about Lan they have to scroll up and find out who's Lan so this is a hard part. Should  We just create a general description of a person, not just a specific name.
3. **Term "bộ quy định"**
   > this can be hard to understand. Should we use English words for terminologies like this and
4. **Section 2, metadata list, relations** ("Quan hệ do chủ sở hữu khai báo: "dùng thay" (overrides) chuỗi "Nghỉ phép Tập đoàn". Quan hệ còn lại là "bổ sung" (compl…")
   > People will wonder why this override chuỗi nghĩ phép tập đoàn. I mean, what  the order of the override?
5. **Section 2, metadata list** ("Chủ đề và chủ sở hữu: nghỉ phép, HR GameCo.")
   > Why make this one line? You can make it two lines for better readability.
6. **Section 2, flow** ("Luồng 7 bước, minh họa bằng câu hỏi của Minh trên 10 văn bản giả lập:")
   > Again should we use a specific example (a real case) in this or should we use a general description?

### How batch 2 was handled (Claude, 08/10, Hiep: "Apply the recommendations.")

1. Sentence removed; "có thể" in the previous sentence and the "giả lập" note in the opening box keep the claim hedged.
2. Names removed from the document; people are named by role ("nhân viên GameCo", "nhân viên HR Tập đoàn", "kế toán PayCo"), including the cards and the test table. The names stay in internal files and for the pitch.
3. "bộ quy định" replaced by "phạm vi tìm kiếm (của người hỏi)" everywhere, defined once in Section 2.
4. The "dùng thay" bullet now states the direction (HR GameCo declares it on its own document, for GameCo staff) and that the system never assumes "đơn vị cấp dưới thắng"; undeclared pairs are conflicts.
5. "Chủ đề" and "Chủ sở hữu" are separate bullets.
6. The concrete case stays; the flow intro says each box gives the general rule plus the result for the GameCo employee's question.


### Batch 3 (08/10, draft after the new-reader review)

Written in Lavish on the draft after RV1-RV7; the session was ended from the browser.
Each note is copied verbatim, with the text it is attached to.

1. **Section 1, naive RAG definition** ("(tìm văn bản theo độ giống câu chữ, rồi để LLM trả lời)")
   > remove this line
2. **Section 2, "Ý chính" paragraph** ("(retrieval)" and "(generation)")
   > remove
3. **Section 2, step 7, step order and data-change paragraphs** ("Ở bước 7, nếu câu trả lời trích..." to "...người hỏi nhận thẻ mâu thuẫn.")
   > this is hard to read. lengthy paragraph is a pain to read
4. **Section 2, step order and data-change paragraphs** ("Thứ tự các bước có lý do..." to "...người hỏi nhận thẻ mâu thuẫn.")
   > this is kinda hard to read, to lengthy
5. **Section 2, "Khi dữ liệu thay đổi..." paragraph**
   > consider remove the too detailed information to keep the reading flow smooth
6. **Section 2, conflict card** (the card for the PayCo employee)
   > about this can a scenario when a document does not conflicts with each other but the HR forget to label the complement so it end up as conflicts then the explain in the conflicts card can be misleading
7. **Section 2, paragraph under the cards** ("Kế toán PayCo nhận thẻ mâu thuẫn vì...")
   > this explantion is not clear and easy to read also
8. **Section 3, "Lỗ hổng còn lại" example** ("Ví dụ, nhân viên HR Tập đoàn hỏi...")
   > consider remove this also
9. **Section 3, "Dữ liệu và công cụ cho phiên bản đầu"**
   > should we make it markdown now, is changing the document to pdf or doc which is more close to real company a huge cost for us.
10. **Section 4, heading**
    > this use paragraph which is very hard to read, consider using more scanable structure like table, and if the space is scarce consider remove one decision also
11. **Section 4, Decision 1** ("Tôi không chọn nó vì với kế toán PayCo, ...")
    > reader will not understand who is Ke toan Payco
12. **Section 5, test table**
    > consider remove the test set, it add little value and too detail for a plan. maybe describe what we test only.
13. **Section 5, "Mỗi câu được hỏi theo 3 cách..."**
    > remove this also this is too specific and remember to fix the related places also
14. **Section 5, metrics table, column "Ngưỡng"**
    > is setting 100% here too confident
15. **Section 5, pilot paragraph** ("Sau Mission 2, thí điểm đo kết quả người dùng cần...")
    > remove this since we only include things apply to the MVP
16. **Section 5, build order item 4** ("So sánh với naive RAG...")
    > remove this maybe replace it with measure performance metric
17. **Section 5, build order list**
    > remember to change these according to the changes above
18. **Freeform message**
    > remove the "(retrieval)" and "(generation)" in the diagram also. consider remove the too details paragraph or using long text paragraph since it is a pain to read

### How batch 3 was handled (Claude, 08/10)

Claude answered the questions in notes 6, 9, 10, 12-16 with recommendations.
Hiep: "3. remove item 4 and remove anything that mention comparing with naive-RAG. 6. check the other number so we not too confident also ensure the Chỉ số column is easy to understand what we measure. and for the remaininig options choose your recommendations".
Decisions RV8-RV14 in `decisions.md`; wording-only changes are listed under that table.
