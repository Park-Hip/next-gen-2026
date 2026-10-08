# Phase 3 - The 3 decisions (Claude draft, Hiep revises)

Claude wrote this first draft at Hiep's request (A10 in `decisions.md`); Hiep revises it in his own words.
Every point traces to a row in `decisions.md` or to the output of `checks/adopted_rules.py`.
Examples are simulated ("giả lập"); nothing here was measured.
Thresholds are not set here: they come from Phase 4 (V1).
Each decision ends with "Điểm giám khảo sẽ hỏi" (what a judge would press on), so the revision can fix it or answer it.

## P - Ai quyết định văn bản nào thắng khi hai văn bản cùng áp dụng

Rows: M1a, M1b, M9-M17; Hà's conflict card (T7).

**A - Chọn**

- Luật trên metadata quyết định, dựa trên quan hệ do chủ sở hữu văn bản khai báo.
- Phiên bản mới thay bản cũ trong cùng `series` (M9); quy chế công ty thay quy chế Tập đoàn bằng `overrides` (M11); văn bản bổ sung khai báo `complements` (M14, M17).
- Hai văn bản cùng chủ đề, cùng áp dụng cho người hỏi mà không có quan hệ khai báo là mâu thuẫn: hệ thống trích cả hai, không chọn, chuyển người hỏi về HR đơn vị mình và báo hai chủ sở hữu (M1b).

**B - Phương án thay thế mạnh nhất**

- Các bộ lọc vẫn là luật như A: quyền truy cập, phiên bản hiện hành, phạm vi áp dụng.
  - Chỉ bước cuối khác: khi còn nhiều văn bản cùng áp dụng, LLM đọc nội dung và quyết định văn bản nào thắng, hoặc ghép chúng thành một câu trả lời.
- Đây là cách phần lớn hệ thống RAG xử lý, nên là phương án giám khảo sẽ so sánh.

**B làm tốt hơn ở đâu**

- Không cần ai khai báo quan hệ, nên dùng được ngay với kho tài liệu cũ chưa có metadata quan hệ.
- Đọc được câu thay thế viết ngay trong văn bản, ví dụ Điều 1 của `LEAVE-GAMECO-v2`: "Quy chế này thay thế quy chế nghỉ phép của Tập đoàn".
- Xử lý được trường hợp công ty chỉ sửa một điều của quy chế Tập đoàn, điều A chưa hỗ trợ (M1a).
- Với Hà, B trả lời ngay một con số thay vì bắt Hà chờ HR.

**Tiêu chí - vì sao A thắng**

- Vấn đề đã chọn (F1) là câu trả lời sai mà người dùng tin và hành động theo, không phải câu tìm không ra.
- Với Hà, quy chế Tập đoàn (12 ngày) và quy chế PayCo (13 ngày) không văn bản nào nói văn bản nào thắng; B vẫn sẽ chọn một con số, và câu trả lời trông tự tin như nhau dù chọn đúng hay sai.
- A cho cùng một kết quả với cùng dữ liệu, nên kiểm thử được đến từng dòng; khi luật không biết, người dùng thấy rõ là không biết (thẻ mâu thuẫn) thay vì nhận một phán đoán.
- Người đọc hai văn bản và quyết định quan hệ là chủ sở hữu, một lần, lúc đăng tài liệu; không phải LLM, mỗi lần có người hỏi.
- Nguyên tắc: AI chỉ làm những việc mà lỗi của nó vô hại (Round 3).

**Cái giá của A**

- Chủ sở hữu phải khai báo: `overrides` một lần cho mỗi series, `complements` theo từng cặp văn bản (M17).
- Hà không nhận được con số mà phải hỏi HR PayCo, kể cả khi quy chế PayCo có lẽ là quy chế đúng (cái giá của M1b).
- Quy chế công ty phải đầy đủ về chủ đề của nó; công ty chỉ sửa một điều thì chưa mô hình hoá được (M1a, Issue 5).
- Khai báo sai thì luật làm theo cái sai: một cặp khác nhau ở một điểm mà bị khai `complements` sẽ cho câu trả lời ghép sai (điều kiện đổi của M14).
- Giảm cái giá: kiểm tra lúc đăng (M15) liệt kê các cặp chưa khai báo trước khi có ai hỏi, nên thẻ mâu thuẫn chỉ còn là lưới an toàn (M16).

**B thắng khi**

- Kiểm thử cho thấy thẻ mâu thuẫn xuất hiện nhiều ở những cặp mà ai cũng biết văn bản nào thắng, và chủ sở hữu không xử lý danh sách của kiểm tra lúc đăng (điều kiện đổi của M1b).
- Công ty thường chỉ sửa một điều của quy chế Tập đoàn (điều kiện đổi của M1a, có thể là thay đổi ở Mission 3).
- Khi đó LLM vào như một bộ phát hiện: được thêm cảnh báo mâu thuẫn, không được gỡ cảnh báo, không được chọn văn bản thắng.

**Kiểm thử ở Mission 2**

- Bước luật phải cho đúng kết quả mong đợi ở mọi dòng của bộ test persona × câu hỏi × ngày (tất định, ngưỡng ở V1).
- Các dòng bắt buộc, đã chạy trong `adopted_rules.py`:
  - Minh, 07/10/2026: 14 ngày theo `LEAVE-GAMECO-v2` (T5).
  - Hà, 07/10/2026: thẻ mâu thuẫn `LEAVE-GROUP-v1` và `LEAVE-PAYCO-v1` (T7).
  - Minh, 01/01/2027: v3 có hiệu lực thì trả lời theo v3; v3 bị hoãn thì vẫn là v2 (M10).
  - Tập đoàn ban hành bản mới: Minh vẫn nhận GameCo v2 (M11).
  - Quy trình xin nghỉ chưa khai `complements`: thẻ mâu thuẫn (T11).
- Nếu V5 chọn có baseline: chạy B trên câu hỏi của Hà vài lần và ghi lại B chọn gì, có nói là không chắc hay không.

**Điểm giám khảo sẽ hỏi**

- "Nếu chủ sở hữu không bao giờ khai báo thì sao?" Câu trả lời phải dẫn tới M15 và người chịu trách nhiệm xử lý danh sách.
- "Hà bị bắt chờ HR, vậy hệ thống có ích gì cho Hà?" Cần nói rõ: chờ HR trên một câu hỏi thật sự chưa có đáp án vẫn rẻ hơn hành động theo con số sai.
- P trùng nội dung với Câu 3 bắt buộc: Phần 4 nên nói vì sao, Câu 3 nói làm thế nào (Phase 6).

## S - Câu hỏi gặp tài liệu như thế nào (M18)

Rows: M3b, M18; Minh's trace (Steps D-E); the naive-vs-correct table.

**A - Chọn**

- Dựng bộ luật của người hỏi trước, không đọc câu hỏi: phiên bản hiện hành, lọc quyền và phạm vi, `overrides`, đánh dấu cặp mâu thuẫn theo chủ đề (bước 1-4).
- Retriever chỉ tìm chunk trong bộ luật đó (bước 5); LLM trả lời từ các chunk, trích dẫn từng ý (bước 6).
- Luật quyết định kết quả theo văn bản được trích dẫn: văn bản thuộc cặp mâu thuẫn thì ra thẻ mâu thuẫn, không có trích dẫn hợp lệ thì từ chối, còn lại là câu trả lời (bước 7).

**B - Phương án thay thế mạnh nhất**

- LLM phân loại câu hỏi vào danh sách chủ đề cố định (`nghi_phep`, `lam_them_gio`, `cong_tac_phi`, `luong`).
- Luật tra văn bản áp dụng cho người hỏi ở đúng chủ đề đó, rồi đưa cho LLM viết câu trả lời.
- B cũng loại văn bản sai bằng metadata như A, nên không phải là RAG ngây thơ.

**B làm tốt hơn ở đâu**

- Sau bước phân loại, việc chọn văn bản hoàn toàn tất định; không phụ thuộc retriever xếp hạng chunk.
- Kiểm tra mâu thuẫn chạy đúng chủ đề được hỏi.
- Lỗi được khoanh vào một bước và đo được bằng độ chính xác phân loại.
- Đưa cho LLM ít văn bản hơn.

**Tiêu chí - vì sao A thắng**

- Trong B, lỗi của AI (phân loại sai) quyết định LLM được thấy văn bản nào; trong A, lỗi của AI (retriever bỏ sót) chỉ làm câu trả lời yếu đi hoặc thành "không tìm thấy", vì mọi văn bản trong bộ luật đều đã hợp lệ.
- Thẻ mâu thuẫn chạy theo văn bản được trích dẫn, không theo chủ đề đoán từ câu hỏi: Hà hỏi về làm thêm giờ nhận câu từ chối, không nhận thẻ mâu thuẫn giả về nghỉ phép (đã chạy trong `adopted_rules.py`); trong B, chỉ cần câu đó bị xếp vào `nghi_phep` là ra thẻ mâu thuẫn giả.
- Câu hỏi chạm hai chủ đề, ví dụ "Ngày nghỉ bù sau làm thêm giờ có tính vào phép năm không?", vẫn được tìm trong cả `OT-GAMECO-v1` lẫn `LEAVE-GAMECO-v2`; B chỉ đưa văn bản của một chủ đề (ví dụ minh hoạ, chưa đo).
- Danh sách chủ đề chỉ còn một việc là đánh dấu cặp mâu thuẫn; không phải mở rộng danh sách cho mỗi kiểu câu hỏi mới.

**Cái giá của A**

- Retriever có thể bỏ sót chunk đúng trong bộ luật, và Minh bị từ chối dù câu trả lời có sẵn (từ chối sai).
- Kết quả phụ thuộc LLM trích dẫn đúng: LLM trích một văn bản của cặp mâu thuẫn mà câu trả lời cần cả hai, hoặc trích sai văn bản (điều kiện đổi của M18).
- Bộ luật của một người lớn dần theo số văn bản áp dụng cho họ, và tìm kiếm trong đó có thể nhiễu (điều kiện đổi của M3b).

**B thắng khi**

- Kiểm thử Mission 2 cho thấy tỷ lệ từ chối sai trong bộ luật vượt ngưỡng V1 và sửa retriever không giảm được.
- LLM thường trích sai văn bản hoặc chỉ trích một phía của cặp cần cả hai (M18).
- Bộ luật của mỗi người lớn đến mức tìm kiếm trong đó không còn tách được các văn bản (M3b).

**Kiểm thử ở Mission 2**

- Không câu trả lời nào được trích văn bản ngoài bộ luật: tất định, phải đạt mọi dòng (`adopted_rules.py`: trích bản đã bị thay thế thì ra từ chối).
- Dòng mong đợi có câu trả lời phải trích đúng văn bản "must cite"; đếm số dòng bị từ chối ở đây để ra tỷ lệ từ chối sai.
- Thêm dòng hỏi diễn đạt khác không có từ khoá, ví dụ "Năm nay tôi được nghỉ mấy ngày?", và dòng chạm hai chủ đề.
- Dòng chéo chủ đề: Hà hỏi về làm thêm giờ phải ra từ chối, không ra thẻ mâu thuẫn.

**Điểm giám khảo sẽ hỏi**

- Lợi thế của A so với B nhỏ hơn so với RAG ngây thơ: cả A và B đều loại phiên bản sai bằng metadata, nên không thể dùng bảng "naive vs correct" để bảo vệ S. Lập luận phải đứng trên chỗ lỗi AI rơi vào, không phải trên việc lọc metadata.
- S và P có thể đọc như cùng một ý "luật thay AI". Bài viết nên mở S bằng sự đánh đổi riêng của nó: phủ được câu hỏi bất ngờ, đổi lấy việc chọn văn bản kém tất định hơn.
- Ví dụ câu hỏi chạm hai chủ đề là minh hoạ; Hiep cần tự tin rằng nó đúng với dữ liệu giả lập, hoặc thay bằng ví dụ khác.

## L - Nhân sự hỏi trực tiếp hay HR dùng trước

Rows: F1, F2, M3a, M13, B1.

**A - Chọn**

- Nhân sự hỏi trực tiếp từ v1.
- Mỗi câu trả lời ghi nguồn, phiên bản, ngày hiệu lực và chủ sở hữu, kèm nút "Báo sai" gửi câu hỏi, câu trả lời, văn bản được trích và persona tới chủ sở hữu văn bản được trích (B1).
- Thẻ mâu thuẫn và câu từ chối chuyển người hỏi về HR đơn vị mình.

**B - Phương án thay thế mạnh nhất**

- HR dùng trước: nhân sự vẫn hỏi HR như hiện nay; HR dùng hệ thống để soạn câu trả lời, kiểm tra rồi mới gửi.
- Khi HR đã tin hệ thống thì mới mở cho nhân sự.

**B làm tốt hơn ở đâu**

- Lỗi bị HR chặn trước khi tới nhân sự, nên giai đoạn đầu không ai hành động theo câu trả lời sai.
- HR, người dùng thứ hai và người gác cổng (F2), tin hệ thống qua việc tự thấy câu trả lời, không chỉ qua số liệu kiểm thử.
- HR phát hiện metadata sai (thiếu quan hệ, sai chủ đề) ngay trong công việc hằng ngày.

**Tiêu chí - vì sao A thắng**

- Kết quả người dùng cần (F1) là quyết định đúng ngay lần đầu, không phải chờ HR; B giữ nguyên việc chờ HR, nên chỉ giảm việc soạn thảo cho HR chứ không giải quyết vấn đề.
- Những gì HR sẽ kiểm tra (phiên bản nào, có được xem không, có áp dụng không) chính là phần do luật quyết, và phần này kiểm thử được trên toàn bộ bộ test trước khi mở (P).
- Phần còn lại là lời văn của LLM; nhân sự tự đối chiếu được vì mỗi câu trả lời ghi nguồn và ngày hiệu lực.
- Khi luật không có đáp án, hệ thống không đoán mà chuyển về HR (thẻ mâu thuẫn, từ chối), nên HR chỉ nhận những câu thật sự cần HR.

**Cái giá của A**

- Câu trả lời mà LLM viết sai so với văn bản có thể tới nhân sự trước khi ai phát hiện; chỉ kiểm thử trước khi mở và nút "Báo sai" chặn được.
- Lỗi không ai báo thì không ai biết.
- Niềm tin của HR phải xây từ kết quả kiểm thử, không phải từ trải nghiệm.
- v1 chỉ trả lời quy định áp dụng cho chính người hỏi (M3a, M13), nên HR chưa dùng được hệ thống để trả lời hộ nhân sự đơn vị khác; muốn làm B cần thêm bước chọn đơn vị được hỏi.

**B thắng khi**

- Trên bộ test của Mission 2, độ trung thành của câu trả lời (lời văn đúng với văn bản được trích) dưới ngưỡng V1: khi đó không mở cho nhân sự mà cho HR dùng trước.
- HR không chấp nhận mở cho nhân sự khi chưa tự kiểm câu trả lời.
- Trong thí điểm, nhiều báo cáo "Báo sai" được chủ sở hữu xác nhận là đúng.

**Kiểm thử ở Mission 2**

- Mission 2 chỉ kiểm được điều kiện tiên quyết của A: trên bộ test, bước luật đúng mọi dòng, không rò rỉ, độ trung thành đạt ngưỡng V1; đây là cổng quyết định mở cho nhân sự.
- Nút "Báo sai" chạy hết luồng: một báo cáo tới đúng chủ sở hữu văn bản được trích (cách nhận do V4 quyết định).
- Tín hiệu thật, tỷ lệ "Báo sai" được xác nhận, cần thí điểm; bài viết phải nói rõ là chưa đo.

**Điểm giám khảo sẽ hỏi**

- "Ngưỡng độ trung thành bao nhiêu thì đủ để mở?" Chưa có số; Phase 4 (V1) phải đặt ngưỡng kèm lý do, không thì lập luận của L thiếu chân.
- "Nhân sự có thật sự bấm Báo sai không?" Đây là giả định chưa kiểm chứng; nên nói thẳng.
- Có thể trả lời bằng lộ trình thay vì chọn một: kiểm thử là cổng, B là phương án dự phòng khi cổng không qua. Bản nháp này đã viết theo hướng đó; Hiep quyết định có giữ không.

