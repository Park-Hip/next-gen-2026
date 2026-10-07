# Nhật ký Bằng chứng - Bài test B: Tri thức nội bộ Appota

Ghi lại mọi công cụ AI, prompt đã định hình kết quả, quyết định của tôi và cách tôi xác minh đầu ra, theo `ai_policies.md` và mục "Nộp gì cho mission 1" của đề bài.
Trạng thái xác minh: ✅ đã xác minh, ⏳ cần làm trước khi nộp.
Mục 1-7 dùng tên file trước khi thư mục được sắp xếp lại vào `docs/` (xem `AGENTS.md`), ví dụ `mission1_document_draft.md` → `docs/mission1/document.md`.

## Ngày 07/10/2026

### 1. Nghiên cứu cuộc thi và lập kế hoạch Mission 1

- **Công cụ:** Claude Code (mô hình Claude Opus 5.5), có tìm kiếm web.
- **Prompt (tóm tắt):** "Đọc brief Mission 1, cho tôi best practices, cách tiếp cận hiệu quả, giai đoạn suy nghĩ trước khi viết, bức tranh tổng thể của cuộc thi và việc cần làm ngay."
- **Đầu ra:** `mission1_playbook.md`, gồm luận điểm cốt lõi (liên quan ≠ được phép ≠ đang hiệu lực ≠ áp dụng cho tôi), bảng persona giả lập, 8 bài tập tư duy, gợi ý nội dung 5 phần, lịch 48 giờ.
- **Dữ kiện AI tra cứu trên web:**
  - Lộ trình NextGen 2026 (Explore → Build → Become) và tiêu chí tuyển AI intern.
  - Các công ty thành viên công khai của Appota: Gamota, AppotaPay, Adsota, ACheckin, Kdata.
  - Bộ luật Lao động 2019, Điều 113-114: 12 ngày phép năm, cộng 1 ngày cho mỗi 5 năm làm việc.
  - Dự đoán Mission 2 là xây v1, Mission 3 là thích ứng với thay đổi: chỉ là suy đoán, chưa được xác nhận.
- **Xác minh:**
  - ⏳ Tự mở văn bản gốc Bộ luật Lao động 2019 (Điều 113-114) để kiểm tra lại số ngày phép.
  - ⏳ Tự kiểm tra danh sách công ty thành viên trên trang chính thức của Appota.
  - ✅ Toàn bộ dữ liệu tổ chức và persona (GameCo, PayCo, AdsCo, Lan, Minh, Hà, An) là giả lập, không dùng dữ liệu thật của Appota.

### 2. Sổ tay bài tập tư duy (thinking workbook)

- **Công cụ:** Claude Code (Claude Opus 5.5), skill Lavish để tạo trang HTML tương tác, có tìm kiếm web.
- **Prompt (tóm tắt):** "Giúp tôi brainstorm và thảo luận phần 3 (Thinking phase) và các bài tập. Đừng quyết định thay tôi, hãy đưa lựa chọn và thảo luận."
- **Đầu ra:** `.lavish/thinking-workbook.html`, gồm phần "Company 101" cho người chưa đi làm và 8 bài tập (kiểm kê câu hỏi, người dùng, thử phá RAG đơn giản, pre-mortem, nhật ký quyết định, định nghĩa "tốt", cắt phạm vi, kịch bản thay đổi).
- **Dữ kiện AI tra cứu trên web:**
  - Bộ luật Lao động 2019, Điều 118-119: doanh nghiệp từ 10 lao động phải có nội quy bằng văn bản và đăng ký với cơ quan lao động cấp tỉnh.
  - Luật Bảo vệ dữ liệu cá nhân số 91/2025/QH15, hiệu lực từ 01/01/2026.
  - Phương pháp pre-mortem của Gary Klein, Harvard Business Review, tháng 9/2007.
- **Phần tôi tự làm:** tôi tự trả lời tất cả bài tập trong sổ tay. Câu trả lời gốc được lưu nguyên văn trong `thinking_phase_answers.md` (Round 1).
- **Xác minh:**
  - ✅ Các con số minh họa trong sổ tay (điểm tương đồng khi tìm kiếm, số liệu Hệ thống A/B) chỉ dùng để luyện tư duy và không đưa vào bài nộp như dữ liệu thật.
  - ⏳ Tự kiểm tra lại Điều 118-119 và ngày hiệu lực của Luật 91/2025/QH15 trên văn bản gốc.

### 3. Phản biện câu trả lời và chốt quyết định

- **Công cụ:** Claude Code (Claude Opus 5.5).
- **Prompt (tóm tắt):** gửi câu trả lời từ sổ tay và yêu cầu "thảo luận, đưa lựa chọn và lý do, hỏi lại 1-2 câu, không quyết định thay tôi".
- **Đầu ra:** nhận xét từng bài tập và 8 điểm mâu thuẫn giữa các câu trả lời của tôi (ví dụ: tỷ lệ từ chối tối đa 10% mâu thuẫn với việc chọn Hệ thống B từ chối nhiều hơn).
- **Quyết định của tôi (Round 2):** chấp nhận tỷ lệ từ chối cao hơn để đổi lấy độ an toàn; chỉ đánh giá rủi ro cho thiết kế của mình (không có chat nhóm); kiểm tra mâu thuẫn chỉ lúc hỏi trong bản 3 ngày; thu hẹp người dùng chính thành "nhân sự lúc cần ra một quyết định chịu sự điều chỉnh của quy định".
- **Xác minh:** ✅ mỗi quyết định do tôi chọn và ghi lại kèm lý do trong `thinking_phase_answers.md`.

### 4. Bản nháp do AI viết cho các phần còn thiếu

- **Công cụ:** Claude Code (Claude Opus 5.5).
- **Prompt (tóm tắt):** "Hoàn thành các phần còn thiếu giúp tôi và chuyển sang giai đoạn tiếp theo."
- **Đầu ra:** các mục ghi "Claude drafts" trong `thinking_phase_answers.md` (Round 2): lý do và điều kiện đổi ý cho D1-D6, top 3 rủi ro, kịch bản S01-S10, đề xuất nút "Báo sai", phạm vi HR cộng chính sách dùng AI, tách chỉ tiêu thành 95% câu đã trả lời đúng và tối đa 25% từ chối, bổ sung IT/bảo mật và pháp chế làm bên kiểm soát.
- **Xác minh:**
  - ✅ Tôi duyệt chung toàn bộ bản nháp (Round 3), chưa thảo luận từng mục.
  - ✅ Claude liệt kê 7 đề xuất quan trọng chưa được thảo luận (thứ tự ưu tiên tài liệu, chỉ tiêu 95%/25%, phạm vi HR + chính sách dùng AI, nút "Báo sai", bỏ hội thoại nhiều lượt khỏi bản 3 ngày, top 3 rủi ro, một người thuộc nhiều đơn vị). Tôi duyệt cả 7, chưa thảo luận chi tiết.
  - ✅ Tôi bác bỏ một đề xuất của AI: dùng LLM để xác nhận hai tài liệu có mâu thuẫn hay không. Lý do của tôi: LLM có thể ảo giác và nói "không mâu thuẫn" khi thực ra có. Tôi chọn để luật xác định trên metadata coi là mâu thuẫn, trích nguyên văn hai điều khoản và chuyển chủ sở hữu tài liệu quyết định.
  - ⏳ Viết lại các lý do bằng lời của mình để có thể bảo vệ trong vòng PITCH.

### 5. Bản nháp 3 câu hỏi bắt buộc

- **Công cụ:** Claude Code (Claude Opus 5.5).
- **Prompt (tóm tắt):** chuyển sang giai đoạn tiếp theo; AI viết nháp tiếng Việt cho 3 câu hỏi bắt buộc dựa trên các quyết định của tôi.
- **Đầu ra:** `mission1_answers_draft.md`.
- **Xác minh:**
  - ✅ Đếm số từ bằng script Python: Câu 1 = 125, Câu 2 = 130, Câu 3 = 133 từ, nằm trong giới hạn 60-150.
  - ✅ Câu 3 đã sửa theo quyết định của tôi (không dùng AI để phán xét mâu thuẫn).
  - ⏳ Viết lại cả 3 câu bằng giọng của mình và tự giải thích to từng câu.
  - ⏳ Đếm lại số từ sau khi viết lại.

### 6. Bản nháp tài liệu 5 trang

- **Công cụ:** Claude Code (Claude Opus 5.5).
- **Prompt (tóm tắt):** "Bắt đầu viết bản nháp tài liệu Mission 1."
- **Đầu ra:** `mission1_document_draft.md` (tiếng Việt, 5 phần + 3 câu trả lời) và script `tools/render_pdf.py` xuất bản nháp ra PDF A4 bằng Edge headless.
- **Xác minh:**
  - ✅ Xuất PDF và đếm trang bằng script: 5 trang (bản đầu 7 trang; đã đổi sơ đồ sang chiều ngang, gộp bảng để vừa giới hạn).
  - ✅ Kiểm tra từng trang bằng ảnh chụp: dấu tiếng Việt hiển thị đúng, bảng không tràn, chữ trong sơ đồ đọc được.
  - ⏳ Đọc toàn bộ, viết lại bằng lời của mình, tự giải thích được từng quyết định trong bảng ở Phần 4.

### 7. Prompt cho AI review độc lập

- **Công cụ:** Claude Code (Claude Opus 5.5).
- **Prompt (tóm tắt):** "Soạn prompt để một AI khác kiểm tra và review bản nháp, chỉ ra điều quan trọng của Mission 1 và best practice."
- **Đầu ra:** `review_prompt.md`.
- **Xác minh:**
  - ⏳ Chạy prompt trên AI khác; ghi lại công cụ, model, kết quả và góp ý nào được chấp nhận, vì sao.

### 8. Cập nhật theo tiêu chí chấm và yêu cầu nộp bài mới trong đề

- **Công cụ:** Claude Code (Claude Opus 5.5).
- **Prompt (tóm tắt):** "Tôi đã thêm 'Tiêu chí chấm điểm' và 'Nộp gì cho mission 1' vào đề, hãy sửa các chỗ liên quan."
- **Đầu ra:** cập nhật `AGENTS.md`, `docs/mission1/criteria.md`, `docs/mission1/review_prompt.md`, `docs/mission1/playbook.md`; thêm trường "Quyết định của tôi" vào mẫu nhật ký này.
- **Quyết định của tôi:** áp dụng tiêu chí mới cho Mission 1; nhật ký bằng chứng được nộp kèm nên phải ghi rõ quyết định của tôi ở từng mục.
- **Xác minh:**
  - ✅ Đối chiếu nội dung cập nhật với nguyên văn đề trong `docs/competition/mission1_brief.md`.
  - ⏳ Bổ sung "Quyết định của tôi" cho các mục 1-7 bằng lời của mình.

## Mẫu cho các mục tiếp theo

```
### N. <Việc đã làm>

- **Công cụ:** <tên công cụ và mô hình>
- **Prompt (tóm tắt):** "<nội dung yêu cầu>"
- **Đầu ra:** <file hoặc phần nào trong bài nộp>
- **Quyết định của tôi:** <tôi giữ, sửa hay bỏ gì từ đầu ra, và vì sao>
- **Xác minh:** <đã kiểm tra thế nào, đã tự sửa gì>
```
