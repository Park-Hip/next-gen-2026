# Prompt - independent review of the 3 mandatory answers (non-Claude model, web chat)

Built on 08/10 from commit `95346e3`: `docs/competition/mission1_brief.md`, `docs/mission1/answers.md` and `docs/mission1/document.md`, embedded verbatim.
If any of these files changes, rebuild the prompt before sending it.
Word counts were computed by script (whitespace split): 114 / 134 / 130.

How to run it:

1. Open a new chat in ChatGPT or Gemini with the strongest reasoning model available; turn off memory or custom instructions if you can, so earlier chats do not colour the review.
2. Send message 1 and wait for the full reply.
3. Send message 2 in the same chat.
4. Save both replies to `docs/mission1/redraft/review_answers_output.md`, noting the tool, model name and date, and log the run in `evidence_log.md`.

The prompt does not say who wrote the answers or that an AI drafted them, so the judge is not led either way.

## Message 1

````text
You are an independent, strict judge for a hiring competition, Appota NextGen AI Talent 2026, test B "Tri thức nội bộ Appota".
A candidate has written three short answers to the mandatory "Forced Decision" questions of Mission 1.
Your job is to find real weaknesses before the answers are submitted.
You did not write them and have no reason to defend them.
Do not be polite or encouraging; a short list of real problems is worth more than praise.
Quote the exact Vietnamese text whenever you point at a problem.

How this review works:

- I will send two messages.
- This first message contains the official brief and the three answers.
- The answers are submitted in a separate field from the candidate's 5-page PDF, so a judge may read them on their own.
  Judge them on their own first.
- Do not ask for the PDF and do not guess its content; I will send it in message 2.
- All companies, people, documents and numbers in this competition are simulated ("giả lập"). Do not judge whether they are realistic facts about Appota.

## 1. Official brief (verbatim, Vietnamese)

# Mission 1 - TRI THỨC NỘI BỘ APPOTA

BỐI CẢNH

**BÀI TEST B - TRI THỨC NỘI BỘ APPOTA**

**MÔ TẢ ĐỀ**

Appota Group cần một sản phẩm sử dụng AI giúp nhân sự **tìm đúng tri thức, trong đúng bối cảnh và đúng phạm vi được phép sử dụng**.

Tri thức tồn tại ở nhiều cấp từ **Tập đoàn → Công ty → Phòng ban → Nhóm**, với nhiều loại tài liệu và phiên bản khác nhau.

Thách thức không chỉ là tìm được tài liệu liên quan, mà còn phải hiểu **ai đang hỏi, họ thuộc đơn vị nào, được phép tiếp cận thông tin gì và tài liệu nào đang có hiệu lực**.

Ví dụ: cùng câu hỏi *“Quy định nghỉ phép của tôi như thế nào?”*, hai nhân sự thuộc hai đơn vị khác nhau có thể cần nhận câu trả lời khác nhau.

Ứng viên **không sử dụng dữ liệu nội bộ thật của Appota**, mà tự xây dựng dữ liệu giả lập phù hợp.

**CÂU HỎI CỐT LÕI**

**Làm thế nào để mỗi nhân sự nhận được đúng thông tin mình cần, đúng với đơn vị và quyền truy cập của mình?**

**MISSION 1 - THẤU HIỂU VẤN ĐỀ**

Hiểu đúng vấn đề, biết ưu tiên và thiết kế hướng giải quyết.

**Trước khi xây sản phẩm, hãy chứng minh rằng bạn hiểu đúng vấn đề cần giải quyết.**

Mission 1 chưa yêu cầu xây sản phẩm. Hãy phân tích bài toán, xác định người dùng, vấn đề quan trọng nhất, hướng giải quyết và cách bạn sẽ kiểm chứng nó.

**THỜI GIAN**

**02 ngày kể từ khi Mission 1 được mở/ứng viên nhận đề.**

**BÀI NỘP MISSION 1**

01 PDF/DOCX, tối đa **5 trang**.

Có thể sử dụng bảng, sơ đồ hoặc hình minh họa.

Tài liệu nên làm rõ 5 nội dung:

**1. Vấn đề & người dùng**

Vấn đề thực sự là gì? Ai gặp vấn đề đó? Kết quả họ thực sự cần là gì?

**2. Giải pháp & luồng hoạt động**

Hướng giải quyết của bạn và luồng chính của sản phẩm.

**3. AI, dữ liệu & con người**

AI làm gì? Không nên làm gì? Cần dữ liệu/công cụ gì? Con người tham gia ở đâu?

**4. Quyết định & rủi ro**

Các lựa chọn quan trọng, trade-off và những tình huống có thể khiến giải pháp thất bại.

**5. Kiểm chứng & MVP**

Làm thế nào để biết giải pháp tốt hay chưa? Nếu chỉ có thời gian ngắn, phần nào cần được hiện thực hóa trước?

Không kỳ vọng một tài liệu hoàn hảo. Hãy ưu tiên chất lượng tư duy, khả năng lựa chọn và lý do đằng sau những quyết định của bạn.

**3 CÂU HỎI BẮT BUỘC**

1. **Nếu chỉ được giải quyết 01 vấn đề quan trọng nhất, bạn chọn vấn đề nào? Người dùng là ai và kết quả họ thực sự cần là gì?**
2. **Nếu chỉ có 03 ngày để xây phiên bản đầu tiên, bạn sẽ làm phần nào trước và chủ động chưa làm những gì? Vì sao?**
3. Nếu hệ thống tìm thấy **hai tài liệu đều liên quan nhưng có nội dung khác nhau hoặc khác phiên bản**, bạn sẽ thiết kế hệ thống xử lý như thế nào trước khi đưa ra câu trả lời?

**Trả lời ngắn gọn, rõ quyết định và lý do. Khuyến nghị 60–150 từ.**

**DEADLINE**

02 ngày kể từ khi Mission 1 được mở/ứng viên nhận đề

**GHI CHÚ**

- Được phép và được khuyến khích sử dụng AI: điều cần đánh giá là khả năng hiểu đúng vấn đề, lựa chọn cách giải quyết hợp lý, biến ý tưởng thành sản phẩm và tiếp tục hoàn thiện khi thực tế thay đổi.
- Tự do chọn ngôn ngữ, framework, model và nhà cung cấp LLM (OpenAI, Gemini, Claude, model open-source...); khuyến khích dùng free tier, chi phí API tự lo.
- Nộp bài theo hướng dẫn của HR/Appota.

## Tiêu chí chấm điểm cho mission 1

40% Khung vấn đề (Problem Framing) - bạn có hiểu đúng vấn đề không?, 35% Thực thi (giải pháp có chạy thật không?), 25% Chất lượng quyết định (lý do chọn A thay vì B có thuyết phục không?).

## Nộp gì cho mission 1

File PDF hoặc link Notion + 3 câu trả lời Quyết định bắt buộc (Forced Decision) + Nhật ký Bằng chứng (công cụ AI, prompt, quyết định). Không cần code ở Mission 1.

## 2. Competition rules that matter for this review (verbatim)

"Làm chủ > Hoàn hảo. Chúng tôi thích một giải pháp chưa hoàn hảo nhưng bạn hiểu tường tận hơn là một giải pháp hoàn hảo mà bạn không thể giải thích. Vòng PITCH sẽ lộ ra."
"Ưu tiên sự rõ ràng hơn là thuần ngôn ngữ."
"Đánh giá: 40% Khung vấn đề (thấu hiểu), 35% Thực thi (có chạy không?), 25% Chất lượng quyết định (lựa chọn bắt buộc). Không có tiêu chí ẩn."

The requirement for these answers is in the brief: "Trả lời ngắn gọn, rõ quyết định và lý do. Khuyến nghị 60–150 từ."
The word counts below were computed by a script that splits on whitespace, so each Vietnamese syllable counts as one word.
Use these counts; do not recount by hand.

## 3. The three answers (verbatim)

Each sentence is on its own line in the original; that is formatting only.

### Câu hỏi 1

Nếu chỉ được giải quyết 01 vấn đề quan trọng nhất, bạn chọn vấn đề nào? Người dùng là ai và kết quả họ thực sự cần là gì?

### Trả lời 1 (114 từ)

Tôi chọn: nhân sự không biết chắc quy định nào đang áp dụng cho chính mình.
Người dùng là nhân sự các công ty thành viên khi cần làm một việc theo quy định, như xin nghỉ phép.
Kết quả họ cần là câu trả lời đúng với đơn vị của họ, từ văn bản họ được xem, theo bản đang có hiệu lực, kèm nguồn để tự kiểm tra mà không chờ HR.
Lý do: quy định của Tập đoàn, của công ty, bản cũ và bản nháp gần giống nhau.
Câu trả lời theo nhầm văn bản trông giống hệt câu đúng, nên người hỏi làm theo mà không biết mình sai.

### Câu hỏi 2

Nếu chỉ có 03 ngày để xây phiên bản đầu tiên, bạn sẽ làm phần nào trước và chủ động chưa làm những gì? Vì sao?

### Trả lời 2 (134 từ)

Tôi làm trước phần quyết định câu trả lời đúng hay sai, vì đó là rủi ro lớn nhất.
Ngày 1: dữ liệu giả lập, luật chọn văn bản cho người hỏi và bộ câu hỏi kiểm thử.
Luật phải đúng mọi ca trước khi thêm AI, để lỗi sau đó chắc chắn do AI.
Ngày 2: AI tìm và trả lời kèm nguồn; kiểm tra AI nói "không tìm thấy" khi không có văn bản phù hợp.
Ngày 3: giao diện web để chọn người hỏi và xem kết quả.
Chủ động chưa làm: đăng nhập thật, kết nối hệ thống nhân sự, tích hợp công cụ chat, đọc file DOCX/PDF.
Lý do: chúng chỉ đổi nơi lấy dữ liệu hoặc nơi hiển thị, không đổi việc câu trả lời đúng hay sai.

### Câu hỏi 3

Nếu hệ thống tìm thấy hai tài liệu đều liên quan nhưng có nội dung khác nhau hoặc khác phiên bản, bạn sẽ thiết kế hệ thống xử lý như thế nào trước khi đưa ra câu trả lời?

### Trả lời 3 (130 từ)

Luật cố định chọn văn bản trước khi AI trả lời; AI không bao giờ tự quyết văn bản nào đúng.
Khác phiên bản: chỉ giữ bản đã ban hành và đang có hiệu lực hôm nay.
Khác đơn vị: chỉ giữ văn bản người hỏi được xem và áp dụng cho đơn vị của họ.
Nếu vẫn còn cả hai, hệ thống làm theo điều HR đã ghi khi đăng văn bản: văn bản này thay văn bản kia, hay hai văn bản dùng cùng nhau.
Nếu HR chưa ghi, hệ thống không chọn mà trích nguyên văn cả hai và chuyển người hỏi tới HR.
Lý do: khi chưa ai xác nhận, chọn một văn bản là đoán, và đoán sai thì người hỏi vẫn tin là đúng.

## 4. Your task for this message

For each answer, report:

1. **Decision first.** Is the first sentence the decision? After reading only that sentence, would a judge know what was chosen?
2. **Reason.** Is there a reason, and does it really justify the decision, or does it only restate it? Is a reason the question asks for missing? (Question 2 asks "Vì sao?" for both what is built first and what is deliberately not built.)
3. **Coverage.** List every sub-question in the brief's wording and say whether the answer covers it: Question 1 (the problem, the user, the outcome they need); Question 2 (what first, what deliberately not yet, why); Question 3 (what the system does before answering, for both "nội dung khác nhau" and "khác phiên bản").
4. **Brevity.** Words, clauses or sentences that can be cut without losing meaning, and anything more detailed than a short answer needs.
5. **Clarity for a new reader.** Any word, phrase or step that is unclear, ambiguous, or sounds like the candidate's internal jargon. For each one, say how you understood it, so the candidate can see if the meaning came through.
6. **Logic.** Any claim that is wrong, overstated, contradicts another answer, or would not hold in a real company.
7. **PITCH attack.** The single strongest question an interviewer would ask about this answer, and what a weak reply would sound like.
8. **Scores**, 1 to 5, each with a one-line reason: decision clarity, quality of the reason, brevity, clarity for a new reader, fit with the scoring criteria above.

Then, for all three together:

- Rank the answers from weakest to strongest, with one line each.
- The one change that would improve each answer most.

Rules for your reply:

- Do not rewrite whole answers. For each issue you may propose at most one replacement sentence in Vietnamese, and the answer must stay within 150 words after the change.
- Do not invent facts, sources or measurements. Write "uncertain" when you are not sure.
- Reply in English; quote Vietnamese text exactly.
- End with: "Ready for message 2."
````

## Message 2

````text
Here is the candidate's 5-page document, the Markdown source of the submitted PDF, verbatim.
The block of HTML tags in Section 2 is a flow diagram: each box is one step, with the rule, the number of documents left, and the result for the example question.
The tables under "Ba loại thẻ kết quả" are mock-ups of the three result cards the user sees.

Now judge the three answers against this document.
Keep your findings from message 1; only change one if the document gives you a concrete reason.

## The document (verbatim)

# TRỢ LÝ TRI THỨC NỘI BỘ:<br>ĐÚNG NGƯỜI, ĐÚNG QUYỀN, ĐÚNG PHIÊN BẢN

**Bài test B - Tri thức nội bộ Appota - Mission 1**<br>
**Ứng viên:** Phạm Bách Hiệp

> Một văn bản liên quan tới câu hỏi chưa chắc đã được phép xem, đang có hiệu lực, hay áp dụng cho người hỏi.
> Giải pháp là một hệ thống RAG có thêm một lớp luật đứng trước: luật dựa trên metadata chọn ra những văn bản đúng với người hỏi, rồi AI mới tìm và trả lời chỉ trong những văn bản đó.
> Khi luật không xác định được văn bản nào đúng, hệ thống nói rõ và chỉ người cần hỏi, thay vì đoán.
> Mọi đơn vị, nhân sự, văn bản và con số trong tài liệu là **giả lập**.

## 1. Vấn đề & người dùng

**Vấn đề quan trọng nhất: nhân sự không biết chắc quy định nào đang áp dụng cho chính mình.**
Tài liệu không thiếu.
Cái thiếu là một câu trả lời đúng với đơn vị của người hỏi, lấy từ văn bản họ được phép xem, và theo phiên bản đang có hiệu lực.

**Ví dụ.** GameCo và PayCo là hai công ty thành viên của Tập đoàn.
Ngày 07/10/2026, một nhân viên phòng Studio của GameCo hỏi: "Phép năm của tôi là bao nhiêu ngày?"
Kho tài liệu có sáu văn bản nêu số ngày phép năm với câu chữ gần như giống nhau, nhưng chỉ một văn bản đúng với người này:

| Văn bản | Số ngày phép | Có đúng với nhân viên GameCo hôm nay không? |
|---|---|---|
| Quy chế nghỉ phép Tập đoàn | 12 | Không: quy chế GameCo được khai báo là dùng thay nó |
| Quy chế GameCo, bản 1 | 13 | Không: bản 2 đã thay bản này |
| **Quy chế GameCo, bản 2** | **14** | **Có: đã ban hành, hiệu lực từ 01/01/2026** |
| Quy chế GameCo, bản 3 | 15 | Chưa: hiệu lực từ 01/01/2027 |
| Dự thảo quy chế GameCo, bản 4 | 16 | Không: dự thảo, chưa ban hành |
| Quy chế nghỉ phép PayCo | 13 | Không: đọc được, nhưng nó chỉ áp dụng cho PayCo |

Một hệ thống naive RAG dễ xếp sáu văn bản này gần ngang nhau.
Độ giống câu chữ không cho biết văn bản đã ban hành chưa, có hiệu lực từ ngày nào, áp dụng cho đơn vị nào, hay đã có bản mới thay.
Vì vậy câu trả lời có thể là 12, 13, 15 hay 16 ngày, với giọng tự tin như nhau.
**Văn bản nguy hiểm nhất là văn bản giống nhất với văn bản đúng.**

Ba cặp khái niệm được tách riêng trong toàn bộ thiết kế:

- **Liên quan ≠ được phép xem:** khung bậc lương GameCo liên quan tới câu hỏi về lương, nhưng chỉ HR GameCo được xem.
- **Được xem ≠ áp dụng cho mình:** nhân viên HR Tập đoàn đọc được quy chế GameCo, nhưng phép năm của họ theo quy chế Tập đoàn.
- **Mới nhất ≠ đang có hiệu lực:** bản 3 và dự thảo bản 4 mới hơn bản 2 nhưng chưa có hiệu lực.

**Vì sao chọn vấn đề này.**
Có hai loại sai lầm.
Loại thứ nhất, để lộ văn bản cho người không được xem, nghiêm trọng nhưng có cách chặn rõ ràng: văn bản người hỏi không được xem không bao giờ được đưa vào bước tìm kiếm.
Vì vậy "không rò rỉ" là điều kiện bắt buộc của mọi phương án, không phải vấn đề để chọn.

Loại thứ hai là trả lời theo nhầm quy định.
Lỗi này khó nhận ra, vì câu trả lời sai trông giống hệt câu trả lời đúng: nhân viên GameCo có thể lên kế hoạch nghỉ 15 ngày theo một bản chưa có hiệu lực.
Ngược lại, câu "chưa chắc, hãy hỏi HR" chỉ đưa người hỏi về tình trạng hiện nay.
Vì vậy thiết kế chấp nhận nói "chưa chắc" để tránh trả lời sai.

**Người dùng chính** là nhân sự các công ty thành viên khi cần ra một quyết định theo quy định, như xin nghỉ phép.
Kết quả họ cần là quyết định đúng ngay lần đầu, không phải chờ HR trả lời.

**Người dùng thứ hai** là chủ sở hữu văn bản, tức bộ phận HR của từng đơn vị.
Họ cần đăng văn bản một lần, bớt trả lời câu hỏi lặp lại, và không bị quy trách nhiệm vì lộ thông tin.
Hệ thống cần họ, vì metadata chỉ đúng khi có người giữ cho nó đúng.

**Phạm vi:** quy định nhân sự, đi sâu vào phép năm, vì riêng chủ đề này đã chứa đủ ba yếu tố đề bài nêu: đơn vị, quyền truy cập và phiên bản.

## 2. Giải pháp & luồng hoạt động

**Ý chính: luật xác định phạm vi tìm kiếm của người hỏi trước, rồi AI mới tìm và trả lời trong phạm vi đó.**
Phạm vi tìm kiếm của một người gồm những văn bản họ được xem, đang có hiệu lực và áp dụng cho đơn vị của họ.
Vì vậy phiên bản đầu chỉ trả lời về quy định áp dụng cho chính người hỏi; câu hỏi về quy định của đơn vị khác nhận thẻ từ chối và được chỉ tới HR.
Luật xác định phạm vi này từ metadata, không đọc câu hỏi và không dùng AI.
Sau đó hệ thống chạy RAG như bình thường: truy xuất các đoạn văn bản liên quan, rồi LLM sinh câu trả lời có trích nguồn.

**Metadata của mỗi văn bản**, lấy quy chế GameCo bản 2 làm ví dụ:

- **Chuỗi phiên bản:** các bản của cùng một quy chế, ở đây là chuỗi "Nghỉ phép GameCo" gồm bản 1, 2, 3 và dự thảo bản 4.
- **Trạng thái và ngày hiệu lực:** đã ban hành, có hiệu lực từ 01/01/2026.
- **Quyền xem và đơn vị áp dụng:** mọi nhân sự được xem; áp dụng cho GameCo và các phòng bên dưới.
- **Dùng thay (overrides):** chuỗi "Nghỉ phép Tập đoàn".
  HR GameCo khai báo trên văn bản của mình rằng, với nhân sự GameCo, nó được dùng thay cho cả chuỗi quy chế Tập đoàn, kể cả các bản ra sau.
  Hệ thống không tự suy ra "đơn vị cấp dưới thắng" (lý do ở Phần 4).
- **Bổ sung (complements):** hai văn bản cùng chủ đề nhưng không mâu thuẫn, như hướng dẫn đăng ký nghỉ phép với quy chế GameCo.
- **Chủ đề:** nghỉ phép.
  Chủ đề chỉ dùng để tìm cặp mâu thuẫn: hai văn bản cùng chủ đề, cùng áp dụng cho một người mà không có quan hệ "dùng thay" hay "bổ sung" là một cặp mâu thuẫn.
- **Chủ sở hữu:** HR GameCo.

Hồ sơ người hỏi chỉ cần hai thông tin: đơn vị (Tập đoàn → GameCo → Studio) và vai trò.

**Luồng 7 bước**, mỗi ô gồm luật chung và kết quả cho câu hỏi của nhân viên GameCo:

<div class="flow">
<div class="lane">Bước 1-4: luật trên metadata, không đọc câu hỏi</div>
<div class="row">
<div class="box start"><b>Kho văn bản</b><span class="n">10 văn bản</span></div>
<div class="arr">→</div>
<div class="box"><b>1. Mỗi quy chế giữ bản đang có hiệu lực</b><span class="n">còn 7</span><span>Loại GameCo bản 1, bản 3, dự thảo bản 4</span></div>
<div class="arr">→</div>
<div class="box"><b>2. Giữ văn bản được xem và áp dụng cho người hỏi</b><span class="n">còn 5</span><span>Loại khung lương (không có quyền), PayCo (không áp dụng)</span></div>
<div class="arr">→</div>
<div class="box"><b>3. Bỏ văn bản đã có văn bản khác "dùng thay"</b><span class="n">còn 4</span><span>Loại quy chế Tập đoàn</span></div>
<div class="arr">→</div>
<div class="box"><b>4. Đánh dấu cặp mâu thuẫn</b><span class="n">0 cặp</span><span>Phạm vi tìm kiếm: 4 văn bản</span></div>
</div>
<div class="lane">Bước 5-6: RAG bên trong phạm vi tìm kiếm. Bước 7: luật chọn một trong ba loại thẻ kết quả (bên dưới)</div>
<div class="row">
<div class="box ai"><b>5. Truy xuất</b><span class="n">AI</span><span>Tìm được Điều 2, quy chế GameCo bản 2</span></div>
<div class="arr">→</div>
<div class="box ai"><b>6. Sinh câu trả lời</b><span class="n">AI</span><span>"14 ngày", trích nguồn từng ý</span></div>
<div class="arr">→</div>
<div class="box"><b>7. Chọn loại thẻ theo văn bản được trích</b><span class="n">Luật</span><span>Trích văn bản hợp lệ, không thuộc cặp mâu thuẫn</span></div>
<div class="arr">→</div>
<div class="box out"><b>Kết quả</b><span class="n">Thẻ trả lời</span><span>14 ngày, nguồn: quy chế GameCo bản 2</span></div>
</div>
</div>

- **Bước 7:** câu trả lời trích một văn bản thuộc cặp mâu thuẫn thì hiện thẻ mâu thuẫn; không có trích dẫn, hoặc trích một đoạn không được truy xuất (LLM bịa nguồn), thì từ chối cả câu trả lời.
- **AI không đưa được văn bản sai vào:** bước 1-4 không đọc câu hỏi, nên lỗi ở bước truy xuất không thể đưa bản cũ, dự thảo hay văn bản mật vào câu trả lời.

**Ba loại thẻ kết quả.** Mỗi thẻ ghi "Bạn đang hỏi với tư cách" để người hỏi thấy hệ thống đang dùng phạm vi tìm kiếm của ai.

| Trả lời: nhân viên GameCo hỏi phép năm | Mâu thuẫn: nhân viên PayCo hỏi phép năm | Từ chối: nhân viên GameCo hỏi khung bậc lương |
|---|---|---|
| *Bạn đang hỏi với tư cách: nhân sự GameCo, Studio.*<br>**Phép năm của bạn là 14 ngày mỗi năm.**<br>Nguồn: Quy chế nghỉ phép GameCo (bản 2), Điều 2, hiệu lực từ 01/01/2026. Hỏi thêm: HR GameCo.<br>**[Báo sai]** | *Bạn đang hỏi với tư cách: nhân sự PayCo, Kế toán.*<br>**Có hai quy định cùng áp dụng cho bạn nhưng chưa được khai báo quan hệ với nhau. Hệ thống không tự chọn.**<br>Tập đoàn, Điều 1 (từ 01/01/2024): "Nhân sự chính thức của Tập đoàn được nghỉ phép năm 12 ngày mỗi năm."<br>PayCo, Điều 1 (từ 01/01/2025): "Nhân sự PayCo được nghỉ phép năm 13 ngày mỗi năm."<br>Vui lòng hỏi HR PayCo. Đã ghi nhận để HR Tập đoàn và HR PayCo xác nhận. | *Bạn đang hỏi với tư cách: nhân sự GameCo, Studio.*<br>**Hệ thống không tìm thấy quy định phù hợp để trả lời câu hỏi này cho bạn.**<br>Hệ thống chỉ trả lời các quy định áp dụng cho bạn. Vui lòng liên hệ HR GameCo. |

- **Thẻ mâu thuẫn:** PayCo chưa khai báo quy chế của mình dùng thay hay bổ sung cho quy chế Tập đoàn, nên hệ thống không chọn. Thẻ chỉ trích nguyên văn hai văn bản, LLM không viết gì trên thẻ.
- **Thẻ từ chối:** cùng một câu dù không có quyền hay không có văn bản, để không lộ rằng có văn bản mật.

## 3. AI, dữ liệu & con người

**AI làm hai việc, cũng là hai bước của RAG.**
Thứ nhất là truy xuất: tìm các đoạn liên quan trong phạm vi tìm kiếm, kể cả khi câu hỏi diễn đạt khác với văn bản.
Thứ hai là sinh câu trả lời: viết chỉ từ các đoạn tìm được, trích nguồn cho từng ý, hoặc nói "không tìm thấy".
Hai việc này được giao cho AI vì khi AI làm sai, hầu hết lỗi rơi về phía an toàn hoặc bị luật chặn lại.

**AI không làm những việc mà chỉ một lỗi cũng thành câu trả lời sai tự tin:** quyết định ai được xem gì, bản nào có hiệu lực, văn bản nào áp dụng cho ai, văn bản nào thắng khi mâu thuẫn, và hiện loại thẻ nào.
Những việc này do luật làm.

**Lỗ hổng còn lại.**
Luật không chặn được trường hợp LLM trích một văn bản nằm trong phạm vi tìm kiếm nhưng không trả lời câu hỏi, vì văn bản đó hợp lệ với người hỏi.
Cùng với việc LLM diễn đạt sai nội dung văn bản, đây là con đường còn lại tới câu trả lời sai tự tin, nên Phần 5 kiểm tra chính nó.

**Dữ liệu và công cụ cho phiên bản đầu:** 10 văn bản giả lập dạng Markdown, chia đoạn theo Điều, kèm metadata.
Bộ chọn người hỏi giả lập thay cho hệ thống nhân sự; bản thật lấy đơn vị từ hệ thống nhân sự, không để người dùng tự khai.
Retriever dùng hybrid search (từ khóa kết hợp embedding) để bắt cả câu hỏi diễn đạt khác văn bản; LLM là một mô hình có sẵn.

**Con người tham gia ở ba chỗ:**

- **Chủ sở hữu văn bản** khai báo "dùng thay", "bổ sung" khi đăng văn bản và xử lý danh sách mâu thuẫn, báo sai.
- **HR đơn vị của người hỏi** nhận các câu hỏi bị từ chối hoặc gặp mâu thuẫn; nếu người hỏi cần một văn bản chưa được xem, HR xét quyền.
- **Nhân sự** đối chiếu nguồn ghi trên thẻ và bấm "Báo sai" khi thấy câu trả lời sai.

## 4. Quyết định & rủi ro

Mỗi cột là một quyết định: A là phương án chọn, B là phương án mạnh nhất bị loại.

| | Quyết định 1: ai chọn văn bản thắng | Quyết định 2: tìm văn bản cho câu hỏi bằng cách nào | Quyết định 3: ai dùng trước |
|---|---|---|---|
| **Chọn (A)** | Chủ sở hữu khai báo "dùng thay", "bổ sung"; chưa khai báo thì hiện thẻ mâu thuẫn. | Luật dựng phạm vi tìm kiếm trước, rồi truy xuất trong phạm vi đó; không cần đoán câu hỏi thuộc chủ đề nào. | Nhân sự hỏi trực tiếp ngay từ phiên bản đầu. |
| **Thay vì (B)** | LLM đọc các văn bản cùng áp dụng và chọn văn bản thắng, hoặc luật cố định "đơn vị cấp dưới thắng". | LLM xếp câu hỏi vào một chủ đề, rồi luật tra văn bản áp dụng ở chủ đề đó. | Vài tuần đầu HR dùng hệ thống soạn câu trả lời, kiểm rồi mới gửi cho nhân sự. |
| **B mạnh ở** | Không ai phải khai báo; người hỏi luôn có ngay một con số. | Chủ đề đúng thì luật trả về đủ văn bản, không sợ truy xuất bỏ sót; độ chính xác của bước phân loại dễ đo. | HR chặn lỗi trước khi tới nhân sự; hệ thống được thử trên câu hỏi thật. |
| **Vì sao chọn A** | Khi PayCo chưa khai báo, không ai biết quy chế nào thắng: cả LLM lẫn luật cố định đều phải đoán, và đoán sai là đúng lỗi ở Phần 1. Với khai báo, cùng dữ liệu luôn cho cùng kết quả. | Với B, xếp nhầm chủ đề đổi cả tập văn bản LLM được thấy: nhân viên PayCo hỏi về làm thêm giờ (PayCo không có quy định này) mà bị xếp vào "nghỉ phép" sẽ nhận thẻ mâu thuẫn về nghỉ phép. Với A, truy xuất bỏ sót chỉ làm câu trả lời yếu đi hoặc thành từ chối, và câu hỏi chạm hai chủ đề vẫn tìm được. | Những gì HR sẽ kiểm (bản nào, có được xem không, có áp dụng không) đã do luật quyết và được kiểm trên bộ test. Lỗi còn lại là LLM diễn đạt sai, mà thẻ ghi rõ văn bản, Điều và ngày hiệu lực để người hỏi tự đối chiếu. |
| **Cái giá** | Chủ sở hữu phải khai báo; người gặp thẻ mâu thuẫn phải hỏi HR. | Truy xuất bỏ sót thì người hỏi bị từ chối và phải hỏi HR, dù có câu trả lời. | Một câu LLM viết sai có thể tới nhân sự trước khi bị "Báo sai". |
| **Đổi khi** | Thẻ mâu thuẫn thường hiện ở những cặp ai cũng biết văn bản nào thắng. Khi đó LLM gợi ý quan hệ lúc đăng văn bản để chủ sở hữu xác nhận, nhưng không chọn khi trả lời. | Từ chối nhầm vượt mục tiêu ở Phần 5 mà chỉnh retriever không giảm được. | Bộ test không đạt bốn điều kiện mở ở Phần 5, hoặc sau khi mở có nhiều báo sai được xác nhận. |

**Ngoài lỗ hổng ở Phần 3, ba tình huống có thể khiến giải pháp thất bại:**

- **Chủ sở hữu khai báo sai:** hai văn bản khác nhau bị khai là "bổ sung" rồi bị ghép thành câu trả lời sai; dữ liệu giả lập không kiểm được, chỉ lộ ra khi dùng thật.
- **Công ty chỉ sửa một điều của quy chế Tập đoàn:** phiên bản đầu chưa hỗ trợ, vì khai "dùng thay" làm mất các điều khác.
- **HR chưa hỏi được về đơn vị khác:** sau này người dùng tự chọn đơn vị cần hỏi, không để AI đoán.

## 5. Kiểm chứng & MVP

**Cách biết giải pháp tốt: cùng câu hỏi, khác người hỏi hay khác ngày phải ra kết quả khác.**
Bộ test gồm các câu hỏi giả lập, mỗi câu ghi kết quả đúng và những văn bản không được trích.
Bộ test kiểm năm tình huống:

- Cùng câu hỏi phép năm, người ở hai đơn vị khác nhau nhận số ngày khác nhau.
- Cùng một người, hỏi trước và sau ngày bản mới có hiệu lực, nhận số ngày khác nhau.
- Hai quy định cùng áp dụng mà chưa khai báo quan hệ thì hiện thẻ mâu thuẫn, không chọn một con số.
- Hỏi về quy định của đơn vị khác thì từ chối, kể cả khi người hỏi được xem văn bản đó.
- Hỏi về văn bản không được xem thì từ chối bằng đúng câu dùng khi không có văn bản.

Phần luật của bộ test đã chạy đúng bằng script trên dữ liệu giả lập; phần AI chưa đo.

| Chỉ số (đo gì) | Bước | Mục tiêu | Lý do |
|---|---|---|---|
| Luật chọn đúng phạm vi tìm kiếm và đúng loại thẻ | Luật | Đúng mọi ca | Luật cho cùng kết quả mỗi lần chạy, nên một ca sai là lỗi lập trình |
| Rò rỉ: đoạn văn bản người hỏi không được xem lọt vào bước truy xuất | Luật | 0 ca | Kiểm bằng mã của từng đoạn |
| Câu trả lời sai nguy hiểm: trả lời khi lẽ ra phải từ chối, nêu sai nội dung, hoặc trích văn bản không được trích | LLM | 0 ca | Chính là vấn đề ở Phần 1 |
| Trung thực với nguồn (faithfulness): mọi ý trong câu trả lời đều có trong đoạn được trích | LLM | Mọi câu trả lời, đọc tay | Bộ test nhỏ nên đọc tay được hết, không cần thêm một mô hình chấm |
| Từ chối nhầm: từ chối hoặc báo mâu thuẫn khi lẽ ra có câu trả lời | Retriever, LLM | Tối đa 10% số ca | Lỗi an toàn; giả định: nhiều hơn thì nhân sự quay lại hỏi HR |
| Context recall: đoạn chứa câu trả lời có nằm trong các đoạn đưa cho LLM | Retriever | Chỉ theo dõi | Phạm vi tìm kiếm chỉ có vài văn bản nên con số này ít ý nghĩa; chỉ dùng để tìm nguyên nhân khi từ chối nhầm |

Mục tiêu tính trên bộ test; bốn dòng đầu là điều kiện để mở cho nhân sự.
Mỗi ca chạy nhiều lần vì LLM không trả lời giống nhau mỗi lần, và một lần sai tính là trượt.
Đạt các mục tiêu này trên một bộ test nhỏ, giả lập chỉ là điều kiện để mở, không phải bằng chứng hệ thống luôn đúng khi dùng thật.

**Giả định rủi ro nhất:** khi phạm vi tìm kiếm không có văn bản trả lời câu hỏi, LLM nói không tìm thấy; khi có, LLM trích đúng văn bản đó.
Chỉ một câu trả lời sai nguy hiểm trên bộ test là đủ bác bỏ giả định này.

**Nếu chỉ có thời gian ngắn, làm theo thứ tự này:**

1. **Phần luật và bộ test:** bước 1-4 và 7 không cần LLM nên làm và kiểm trước; phải đúng mọi ca trước khi thêm LLM, để lỗi sau đó chỉ có thể là lỗi của AI.
2. **Thêm truy xuất và sinh câu trả lời (bước 5-6):** đủ cả luồng 7 bước, chạy bộ test nhiều lần để kiểm giả định rủi ro nhất.
3. **Giao diện tối thiểu:** chọn người hỏi và ngày, ba loại thẻ, nút "Báo sai", danh sách mâu thuẫn và báo sai cho chủ sở hữu.

## Your task for this message

1. **Contradictions.** Any statement in an answer that contradicts the document: its decisions, its scope, its order of steps, or its 3-day priorities. Quote both sides.
2. **Missing essentials.** Anything the document treats as central to a question that the answer leaves out and a judge would expect. The 150-word limit is real, so for each addition say what to cut to make room, or say the omission is acceptable.
3. **Overclaims.** Anything an answer states as done, measured or guaranteed that the document does not support, or anything it promises beyond what the document plans to build.
4. **Wording mismatches.** Places where the answers and the document use different words for the same idea, or the same word for different ideas, in a way that could confuse a judge who reads both.
5. **Changed views.** Which findings from message 1 changed after reading the document, and why.
6. **Verdict per answer:** keep as is, small edit, or rewrite, with the reason in one or two lines.
7. **Top 3 actions** for the candidate across the three answers, most important first.

Same rules as before: quote exactly, at most one replacement sentence per issue, stay within 150 words, write "uncertain" when unsure, reply in English.
````
