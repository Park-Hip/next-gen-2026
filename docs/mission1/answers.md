# Mission 1 - 3 câu hỏi bắt buộc (bản nháp)

Bản nháp do Claude viết từ các quyết định trong `thinking/thinking_phase_answers.md`.
Hãy đọc, viết lại bằng giọng của mình, và ghi vào Nhật ký Bằng chứng trước khi nộp.

## Câu 1 - Vấn đề quan trọng nhất

Tôi chọn vấn đề: nhân sự không biết chắc quy định nào đang áp dụng cho chính mình.
Người dùng là nhân sự các công ty thành viên, vào lúc cần ra một quyết định do quy định điều chỉnh: xin nghỉ, đăng ký OT, thanh toán công tác phí.
Họ tìm được tài liệu, nhưng bản của Tập đoàn, của công ty và bản cũ gần giống nhau, nên dễ dùng nhầm hoặc phải chờ HR.
Kết quả họ cần: một câu trả lời đúng với đơn vị, loại hợp đồng và thời điểm hiện tại, kèm nguồn, phiên bản và ngày hiệu lực để tự hành động ngay.
Ràng buộc không thương lượng: không bao giờ lộ thông tin ngoài quyền truy cập.

## Câu 2 - Ba ngày đầu: làm gì, chưa làm gì

Tôi chỉ xây phần kiểm chứng giả định rủi ro nhất: đúng quy định, đúng phiên bản, đúng người, không rò rỉ.
Gồm: dữ liệu giả lập có bẫy (bản cũ, dự thảo, quy định chồng chéo, tài liệu mật); lọc quyền trước khi tìm kiếm; luật xác định hiệu lực và phạm vi; trả lời kèm trích dẫn, từ chối khi không chắc; chuyển persona thay đăng nhập; nút báo sai; bộ test persona × câu hỏi có kiểm tra rò rỉ tự động.
Chủ động chưa làm: SSO/HRIS thật, giao diện quản trị, OCR, tích hợp Lark/Slack, tra cứu dữ liệu cá nhân, hội thoại nhiều lượt, fine-tune.
Lý do: đó là bài toán tích hợp và mở rộng; nếu phần lõi sai, mọi thứ khác vô nghĩa.

## Câu 3 - Hai tài liệu liên quan nhưng khác nhau

Thứ tự ưu tiên do luật trên metadata quyết định, không để LLM tự chọn.
Cả hai tài liệu đã qua bộ lọc quyền.
Khác phiên bản: dùng bản đang hiệu lực hôm nay, báo trước nếu có bản sắp hiệu lực.
Khác phạm vi: quy định của đơn vị cụ thể nhất được áp dụng, trừ khi quy định cấp trên được đánh dấu bắt buộc, ví dụ mức tối thiểu theo luật.
Cùng phạm vi, cùng chủ đề, cùng hiệu lực: coi là mâu thuẫn, không để AI phán xét vì AI có thể ảo giác.
Hệ thống không chọn, không trộn: trích nguyên văn hai điều khoản, cảnh báo và chuyển chủ sở hữu tài liệu quyết định.
Quyết định đó được lưu lại để lần sau trả lời đúng.
