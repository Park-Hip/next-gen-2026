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

### 9. Review bản nháp theo `review_prompt.md`

- **Công cụ:** Claude Code (Claude Opus 5.5), có tìm kiếm web.
  Đây là cùng mô hình đã viết bản nháp, nên review này không độc lập và chưa hoàn thành mục 7 ("chạy prompt trên AI khác").
- **Prompt:** nguyên văn phần "Prompt" trong `docs/mission1/review_prompt.md` (Part A-G), chạy trong phiên mới, không có lịch sử hội thoại.
  Phiên này vẫn tự động đọc `AGENTS.md`, nơi có luận điểm cốt lõi của tôi, nên review có thể bị ảnh hưởng bởi luận điểm đó.
- **Đầu ra:** `docs/mission1/review_output.md`.
  Gồm: tiêu chuẩn chấm viết trước khi đọc bản nháp, điểm và nhận xét từng phần, kiểm tra quyết định, lập luận, tính khả thi và dữ kiện, khung cho bản viết lại, nhận xét 3 câu trả lời và nhật ký, 8 câu hỏi PITCH, 5 ưu tiên.
- **Dữ kiện AI tra cứu trên web:**
  - Bộ luật Lao động 2019, Điều 113-114 (hethongphapluat.com): đúng, với lưu ý 12 "ngày làm việc", tính theo tỷ lệ nếu chưa đủ 12 tháng, thâm niên tính "cho một người sử dụng lao động".
  - Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15 (chinhphu.vn): ban hành 26/06/2025, hiệu lực 01/01/2026.
  - Bộ luật Lao động 2019, Điều 118-119: đúng.
  - Theo Điều 2 khoản 1 Luật 91/2025/QH15, dữ liệu cá nhân phải xác định hoặc giúp xác định một người cụ thể, nên "Khung lương GameCo" trong bản nháp không phải dữ liệu cá nhân.
- **Quyết định của tôi:** ⏳ ghi góp ý nào tôi chấp nhận, sửa hoặc bác bỏ, và vì sao.
- **Xác minh:**
  - ⏳ Tự kiểm tra lại các dữ kiện pháp lý trên nguồn chính thức (vbpl.vn, congbao.chinhphu.vn).
  - ⏳ Tự kiểm tra từng lỗi lập luận mà review nêu (ví dụ thứ tự ưu tiên với mức sàn pháp lý) bằng cách chạy tay ví dụ của Minh và Lan.
  - ⏳ Chạy cùng prompt trên một AI khác họ mô hình (GPT hoặc Gemini) và so sánh.

### 10. Tóm tắt review và kế hoạch viết lại

- **Công cụ:** Claude Code (Claude Opus 5.5).
- **Prompt (tóm tắt):** "Tóm tắt `review_output.md`, cho tôi thông tin giá trị nhất." và "Cho tôi kế hoạch viết lại tài liệu, để tôi kiểm soát rõ nội dung và các quyết định."
- **Đầu ra:** bản tóm tắt review trong hội thoại (lỗi logic ở thứ tự ưu tiên, điểm từng phần, khung viết lại, rủi ro của nhật ký); `docs/mission1/redraft_plan.md` gồm 8 giai đoạn (Phase 0-7).
- **Quyết định của tôi:** dùng kế hoạch 8 giai đoạn; quyết định trước khi viết; mọi quyết định ghi vào `docs/mission1/redraft/decisions.md` kèm nguồn gốc; giữ nhật ký này ở dạng thô và hoàn thiện ở Phase 7.
- **Xác minh:**
  - ⏳ Tự đọc `review_output.md` và đối chiếu với bản tóm tắt.

### 11. Phase 0 - Chốt khung bài (F1-F5)

- **Công cụ:** Claude Code (Claude Opus 5.5).
- **Prompt (tóm tắt):** "Sẵn sàng" (bắt đầu Phase 0); Claude đưa lựa chọn và đề xuất cho từng câu F1-F5, tôi quyết định.
- **Đầu ra:** các dòng F1-F5 trong `docs/mission1/redraft/decisions.md`.
- **Quyết định của tôi:**
  - F1, F2, F3, F5: chấp nhận đề xuất của Claude (vấn đề cốt lõi, nhân sự là người dùng chính và chủ sở hữu tài liệu là người dùng thứ hai, phạm vi quy định HR với ví dụ phép năm, bỏ chính sách dùng công cụ AI, phân bổ trang).
  - F4: Claude giải thích bức tranh tổng thể các quyết định; tôi tự chọn R (từ chối hay trả lời kèm cảnh báo) và S (cách tìm kiếm), cùng P (đề xuất của Claude); tạm thời, có thể đổi trong Phase 1-3.
- **Xác minh:**
  - ✅ Nguồn gốc từng quyết định được ghi trong `decisions.md`.

### 12. Phase 1 - Mô hình lõi (M0-M8) và phác thảo dữ liệu

- **Công cụ:** Claude Code (Claude Opus 5.5).
- **Prompt (tóm tắt):** thảo luận từng câu M1-M8; tôi hỏi thêm "Nên xác định metadata tài liệu và nhân sự trước không?", "Mô hình này dựa trên dữ liệu thật, đề bài hay giả định của chúng ta?", "Tài liệu có cần trường chủ đề không?".
- **Đầu ra:** các dòng M0-M8 trong `decisions.md`; phác thảo dữ liệu và bảng lần vết câu hỏi của Minh trong `docs/mission1/redraft/artifacts.md` (Claude viết, chưa chốt); mục "Deferred ideas" trong `docs/mission1/playbook.md`.
- **Quyết định của tôi:**
  - M1c (tự đề xuất): chỉ dùng tài liệu nội bộ, bỏ quy định pháp luật và mức tối thiểu khỏi MVP.
  - M1b: chọn coi hai tài liệu cùng áp dụng mà không khai báo quan hệ là mâu thuẫn.
  - M0: sau khi hỏi nguồn gốc mô hình, chọn chỉ giữ đơn vị, quyền truy cập và phiên bản như đề bài; bỏ loại hợp đồng và thâm niên.
  - M1a: Claude ban đầu đề xuất nhãn theo điều khoản, sau khi tôi nói quá phức tạp thì đổi đề xuất; tôi chọn quan hệ thay thế và ghi đè cho cả văn bản.
  - M3a, M3b, M4-M8: chấp nhận đề xuất của Claude; M4 (trường chủ đề) được thảo luận riêng trước khi chấp nhận.
- **Xác minh:**
  - ✅ Claude phân loại nguồn gốc từng phần mô hình (đề bài, thực tế phổ biến, giả định của chúng tôi) theo nguyên văn đề bài.
  - ⏳ Tự lần vết câu hỏi của Minh bằng tay theo bộ luật (Phase 2).

### 13. Prompt cho Phase 2 (dữ liệu giả lập và lần vết)

- **Công cụ:** Claude Code (Claude Opus 5.5).
- **Prompt (tóm tắt):** "Soạn prompt chi tiết cho Phase 2 để một mô hình đơn giản làm được, tôi sẽ chạy trong phiên mới."
- **Đầu ra:** `docs/mission1/redraft/phase2_prompt.md` (9 bước: danh sách bẫy, persona, tài liệu, lần vết của Minh do tôi tự làm, các persona khác, so sánh RAG đơn giản và mô hình đúng, 3 thẻ trả lời, thí nghiệm embedding, ghi quyết định).
- **Quyết định của tôi:** tôi tự lần vết câu hỏi của Minh; mô hình chỉ được kiểm tra, không viết thay.
- **Xác minh:**
  - ⏳ Chạy prompt trong phiên mới và ghi kết quả thành mục mới.

### 14. Rà soát mô hình lõi theo thực tế vận hành

- **Công cụ:**
  - Claude Code (Claude Opus 5.5): phân tích, viết 2 script kiểm tra luật, viết báo cáo.
  - Agnes 2.5 Flash (mức suy luận tối đa), qua subagent: tìm nguồn trên web, sau đó một lượt thứ hai mở từng URL và so trích dẫn với nguyên văn.
- **Prompt (tóm tắt):** "Đọc dữ liệu và artifact, kiểm tra giả định so với thực tế vận hành ở công ty thật. Hệ thống hiện coi hai tài liệu cùng chủ đề là mâu thuẫn, tôi nghĩ đó là lỗi. Tìm các chỗ hệ thống không chạy tốt khi vận hành thật và best practice để sửa. Chỉ dùng Agnes 2.5 Flash để tìm web."
- **Đầu ra:**
  - `docs/mission1/redraft/production_review.md`: 9 phát hiện (P1-P9), đề xuất thay đổi dữ liệu, thứ tự ưu tiên, nguồn đã kiểm tra.
  - `docs/mission1/redraft/checks/current_rules.py`: cài đúng nguyên văn 7 luật lõi và chạy trên dữ liệu giả lập.
  - `docs/mission1/redraft/checks/proposed_rules.py`: bộ luật đề xuất, chạy trên cùng các kịch bản.
- **Phát hiện chính (do script chạy ra, không phải suy đoán):**
  - Ngày 01/01/2027, khi v3 có hiệu lực đúng kế hoạch, GameCo v1 "sống lại" và mâu thuẫn với v3, vì quan hệ `replaces` chỉ tính giữa các tài liệu còn lại sau bộ lọc.
  - Khi Tập đoàn ra bản mới, `overrides` trỏ vào phiên bản cũ nên mọi nhân sự GameCo nhận cảnh báo mâu thuẫn.
  - Thêm một quy trình xin nghỉ phép cùng chủ đề gây mâu thuẫn giả (vấn đề tôi nêu).
- **Quyết định của tôi:**
  - Chấp nhận P1-P3 (chuỗi phiên bản, không gõ trước ngày hết hiệu lực, `overrides` trỏ vào chuỗi), ghi thành M9-M12 trong `decisions.md`.
  - P8: ghi là giới hạn đã biết của bản v1 (M13), không làm bộ chọn "Hỏi cho" trong MVP.
  - P4 (`covers`): thấy hướng này tốt nhưng cần hiểu rõ thay đổi trong luồng xử lý trước khi quyết định.
- **Xác minh:**
  - ✅ Script luật hiện tại cho đúng kết quả lần vết tay của Minh, Lan và Hà ở ngày 07/10/2026 trước khi chạy các kịch bản mới.
  - ✅ Lượt kiểm tra thứ hai loại 3 nguồn không xác minh được (ISO 9001 mục 7.5.3, SAP SuccessFactors, cột metadata nhiều giá trị của SharePoint) và sửa một trích dẫn bị diễn giải.
  - ⏳ Tự chạy lại 2 script và tự mở từng nguồn S1-S10 trước khi dùng trong bài nộp.

### 15. Áp dụng P1-P3 vào dữ liệu giả lập và giải thích `covers`

- **Công cụ:** Claude Code (Claude Opus 5.5). Không dùng tìm kiếm web.
- **Prompt (tóm tắt):** "Sửa P1 đến P3. Với `covers`, tôi cần hiểu thêm nó thay đổi luồng xử lý thế nào. P8 ghi là giới hạn."
- **Đầu ra:**
  - `decisions.md`: các dòng M9-M13.
  - `artifacts.md`: thêm cột `series`, bỏ cột `replaces`, bỏ `effective_to` của GameCo v2, `overrides` trỏ vào `LEAVE-GROUP`; lần vết của Minh viết lại theo 5 bước (kết quả vẫn là 14 ngày từ `LEAVE-GAMECO-v2`).
  - `phase2_prompt.md`: cập nhật mô hình lõi, bảng trường dữ liệu và danh sách tự kiểm tra.
  - `checks/adopted_rules.py`: chạy bộ luật đã chấp nhận trên đúng bảng dữ liệu mới.
  - `production_review.md`: mục "How `covers` changes the pipeline" (từng bước thay đổi, lần vết của Minh với `covers`, rủi ro mới, chi phí ước tính).
  - `playbook.md`: 4 ý tưởng hoãn lại (thông báo khi tài liệu cấp trên đổi phiên bản, cờ "bắt buộc", cảnh báo trước ngày hết hiệu lực, bộ chọn "Hỏi cho").
- **Quyết định của tôi:** ⏳ quyết định về `covers` sau khi đọc mục giải thích.
- **Xác minh:**
  - ✅ `adopted_rules.py` cho kết quả đúng với 3 persona ở ngày 07/10/2026 và với các thay đổi từng làm hỏng bộ luật cũ (v3 có hiệu lực, v3 bị hoãn, Tập đoàn ra bản mới).
  - ✅ Claude tự sửa 2 đề xuất của chính nó trong quá trình làm: bỏ trạng thái `withdrawn` (trùng với `effective_to`) và sửa nhận định "gắn khóa cho cả văn bản là đủ cho MVP" (cần gắn theo từng Điều).
  - ⏳ Tự lần vết lại câu hỏi của Minh theo 5 bước mới.

### 16. Thảo luận luật mâu thuẫn và quy trình thực tế trong sản phẩm

- **Công cụ:**
  - Claude Code (Claude Opus 5.5): thảo luận, script thử nghiệm quan hệ `complements` (ngoài repo, chưa áp dụng).
  - Agnes 2.5 Flash (mức suy luận tối đa), qua subagent: tìm quy trình thực tế (Guru, Glean, Microsoft, Confluence, ServiceNow, KCS, NAVEX), sau đó lượt thứ hai mở từng trang và so trích dẫn với nguyên văn.
- **Prompt (tóm tắt):**
  - "Có thật sự cần `topic` hoặc `covers` không, có bỏ được bước mâu thuẫn và từ chối không?"
  - "`covers` không linh hoạt: tài liệu không có cấu trúc thì phải gắn nhãn từng đoạn. Hai tài liệu cùng chủ đề nghỉ phép nhưng nội dung khác nhau là tình huống hợp lệ."
  - "Trong sản phẩm thật, người ta thường dùng quy trình nào?"
- **Đầu ra:**
  - Trong hội thoại: giữ bước mâu thuẫn và từ chối (chúng là 3 kết quả của một bộ phân giải); đề xuất bỏ `covers`, giữ `topic` theo tài liệu, thêm quan hệ `complements` khai báo một lần cho mỗi cặp chuỗi tài liệu.
  - `production_review.md`: mục "How real products keep knowledge consistent" với 7 quy trình và nguồn S11-S19.
- **Phần tôi tự làm:** tôi phản biện `covers` (phải gắn nhãn từng đoạn, không dùng được cho tài liệu không có cấu trúc) và nêu tình huống hai tài liệu cùng chủ đề nhưng bổ sung cho nhau; ý tưởng `complements` đã có trong quyết định Round 3 của tôi.
- **Quyết định của tôi:** bỏ `covers`, giữ một `topic` cho mỗi tài liệu, thêm quan hệ `complements`, kiểm tra cặp chưa khai báo lúc đăng tài liệu bằng script, thêm bẫy T11 (ghi thành M14, M15; xem mục 17).
- **Xác minh:**
  - ✅ Lượt kiểm tra thứ hai loại 2 trích dẫn không có trên trang (Microsoft Copilot, Azure AI Search) và đánh dấu nguồn ServiceNow là yếu vì không tải được trang gốc.
  - ⏳ Tự mở các nguồn S11-S19 trước khi dùng trong bài nộp.

### 17. Áp dụng `complements`, kiểm tra lúc đăng tài liệu và bẫy T11

- **Công cụ:** Claude Code (Claude Opus 5.5). Không dùng tìm kiếm web.
- **Prompt (tóm tắt):** "Đồng ý. Nhưng có nên giữ bước kiểm tra mâu thuẫn lúc hỏi không, khi việc này đã được quản lý bên ngoài câu trả lời?"
- **Đầu ra:**
  - `decisions.md`: M14 (`complements`, bỏ `covers`), M15 (kiểm tra cặp chưa khai báo lúc đăng tài liệu).
  - `artifacts.md`: cột `complements`, tài liệu `LEAVE-PROC-GAMECO-v1` (viết dạng các bước, không có "Điều"), bẫy T11, lần vết của Minh cập nhật (trả lời từ GameCo v2 và hướng dẫn, vẫn 14 ngày).
  - `checks/adopted_rules.py`: thêm `complements` và hàm kiểm tra lúc đăng tài liệu, chạy cho mọi đơn vị, hôm nay và mọi ngày phiên bản hiện hành thay đổi trong tương lai.
  - Cập nhật `phase2_prompt.md`, `production_review.md` (Câu 3 viết lại thành 4 trường hợp), `open_issues.md`, Deferred ideas trong `playbook.md`.
- **Phát hiện khi chạy script:**
  - Bản đầu của kiểm tra lúc đăng tài liệu bỏ sót ngày hết hiệu lực (`effective_to`); Claude sửa và chạy lại, giờ nó báo trước 9 tháng khi GameCo bãi bỏ quy chế.
  - Script thử (ngoài repo) cho thấy khi tái cơ cấu tổ chức (Studio chuyển từ GameCo sang PayCo), cặp chưa khai báo xuất hiện mà không có tài liệu nào được đăng, nên kiểm tra lúc đăng tài liệu không chạy.
  - `complements` khai báo theo từng cặp: tài liệu thứ ba cùng chủ đề cần khai báo với từng tài liệu còn lại.
- **Quyết định của tôi:** giữ bước kiểm tra mâu thuẫn lúc hỏi (M16, vì kiểm tra lúc đăng tài liệu chỉ báo cáo, và có cặp xuất hiện khi không có tài liệu nào được đăng); đổi `complements` thành danh sách (M17). `adopted_rules.py` đã cập nhật; script thử cho thấy tài liệu thứ ba cần khai báo cả hai chuỗi mới hết mâu thuẫn.
- **Xác minh:**
  - ✅ `adopted_rules.py` cho đúng kết quả với 3 persona, các kịch bản phiên bản và T11 (khai báo thì trả lời, không khai báo thì báo mâu thuẫn).
  - ⏳ Tự lần vết lại câu hỏi của Minh với T11.

### 18. Rà soát tiến độ, rút gọn Phase 2 và bỏ bước chọn chủ đề cho câu hỏi

- **Công cụ:** Claude Code (Claude Opus 5.5). Không dùng tìm kiếm web.
- **Prompt (tóm tắt):**
  - "Tóm tắt những gì đã làm, trạng thái hiện tại, có nên dọn dẹp dự án không, chúng ta có đi lệch mục tiêu không?"
  - "Rút gọn Phase 2, các bước sau không cần cho bài nộp; xử lý luôn Issue 2."
  - "Vì sao mô hình phải chọn chủ đề? Tôi nghĩ retriever trả về các chunk rồi đưa cho mô hình sinh câu trả lời."
- **Đầu ra:**
  - Trong hội thoại: nhận định "đúng hướng nhưng đào quá sâu": nhiều giờ dành cho M9-M17 trong khi phần 1 (40% điểm) chưa viết; đề xuất chốt mô hình lõi.
  - Claude đề xuất 3 cách chọn chủ đề cho câu hỏi và khuyến nghị để LLM phân loại; tôi không chọn cách nào mà đặt câu hỏi vì sao cần chọn chủ đề.
  - `decisions.md`: A1 (phạm vi Phase 2), V3 (không chạy thử nghiệm embedding), M18 (dựng bộ luật của người hỏi trước, rồi truy xuất; kết quả do luật quyết theo tài liệu được trích dẫn).
  - `checks/adopted_rules.py`: tách thành `rulebook()` (bước 1-4, không đọc câu hỏi) và `answer()` (bước 7, kiểm tra sau theo trích dẫn); thêm 3 kịch bản kiểm tra sau.
  - Cập nhật `artifacts.md` (thứ tự 7 bước, lần vết của Minh bước D-E), `phase2_prompt.md`, `redraft_plan.md`, `open_issues.md` (đóng Issue 2), Deferred ideas trong `playbook.md`.
- **Phần tôi tự làm:** ý tưởng không chọn chủ đề cho câu hỏi, để retriever trả chunk cho mô hình trả lời; quyết định rút gọn Phase 2.
- **Phần AI đề xuất và tôi chấp nhận:** chọn bước nào của Phase 2 để bỏ; đánh dấu cặp mâu thuẫn theo chủ đề trước khi truy xuất (bước 4); kích hoạt thẻ mâu thuẫn theo tài liệu được **trích dẫn** chứ không theo tài liệu được truy xuất (bước 7), và bỏ trích dẫn nằm ngoài bộ luật.
- **Xác minh:**
  - ✅ `adopted_rules.py` cho kết quả như cũ với 3 persona và các kịch bản phiên bản; 3 kịch bản mới đúng: Hà chỉ trích quy chế Tập đoàn vẫn ra mâu thuẫn, Hà hỏi về làm thêm giờ ra từ chối (không phải mâu thuẫn giả), trích dẫn bản đã bị thay thế ra từ chối.
  - ⚠️ Script giả lập bước 5-6 (retriever và LLM) bằng một hàm thay thế, nên chưa kiểm tra được LLM thật có trích dẫn đúng hay không; việc này để Mission 2.
  - ⏳ Tự đọc lại từng dòng lần vết của Minh theo 7 bước.

## Mẫu cho các mục tiếp theo

```
### N. <Việc đã làm>

- **Công cụ:** <tên công cụ và mô hình>
- **Prompt (tóm tắt):** "<nội dung yêu cầu>"
- **Đầu ra:** <file hoặc phần nào trong bài nộp>
- **Quyết định của tôi:** <tôi giữ, sửa hay bỏ gì từ đầu ra, và vì sao>
- **Xác minh:** <đã kiểm tra thế nào, đã tự sửa gì>
```
