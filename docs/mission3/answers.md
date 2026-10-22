# Mission 3 - 3 câu hỏi bắt buộc

Bản nháp của Claude, 21/10/2026, để Hiệp viết lại bằng lời của mình.
Mọi dữ liệu là giả lập.

## Cách nộp

Ba câu trả lời được dán vào một ô văn bản trên portal, không giới hạn số từ (Hiệp, 21/10/2026); đề Mission 3 cũng không nêu độ dài.
Vì vậy mỗi câu trả lời dưới đây là văn bản thuần, nằm trong một khối để sao chép nguyên văn: không bảng, không Markdown, đường dẫn viết đầy đủ.
Mỗi khối mở đầu bằng câu hỏi nguyên văn của đề, nên ba khối dán chung một ô hay ba ô riêng đều đọc được.
Sau khi dán, xem lại ô văn bản để chắc rằng xuống dòng và thụt lề được giữ.

Trước khi dán, mọi chỗ trống phải được điền hoặc bỏ:

- "[chờ Hiệp]": lý do Hiệp chưa nói bằng lời của mình.
- "[chờ lần chạy cuối]": kết quả chỉ có sau lần chạy chung trên mã Mission 3; không điền bằng ước lượng.
- "[chờ đề]": Change Request, chưa được giao.
- "(AI đề xuất)": lý do do AI viết, Hiệp chưa duyệt; Hiệp duyệt rồi xoá dấu này, hoặc viết lại.

Các lý do còn lại đã được Hiệp duyệt trong [`gaps.md`](gaps.md) hoặc [`choices.md`](choices.md).
"M2" là bản đã nộp (tag `mission2`) và lần chạy [`20261014-2239`](../../results/20261014-2239.jsonl); "M3" là `main` ngày 21/10/2026 (`0f5ca43`).

## Câu 1

```text
Câu 1. Sau khi nhận yêu cầu mới, bạn đã ưu tiên thay đổi điều gì và chủ động chưa làm điều gì? Vì sao?

ƯU TIÊN: những gì nhân sự thấy trên thẻ trả lời, cho cả 5 yêu cầu chung.
AI được giao thêm việc về ngôn ngữ, là viết câu trả lời và báo mâu thuẫn, nhưng luật vẫn quyết định quyền xem, hiệu lực, phạm vi áp dụng, quy định nào được dùng thay quy định nào, và loại thẻ.
Mỗi thay đổi bắt đầu từ một khoảng trống có bằng chứng, là một câu hỏi kiểm thử trượt hoặc một phép thử trên mô hình giả, không bắt đầu từ một tính năng.

1. Câu trả lời bằng lời
   Trước: thẻ chỉ hiện nguyên văn điều khoản đã kiểm, nên nhân sự phải tự suy ra câu trả lời.
   Sau: AI viết một câu trả lời thẳng câu hỏi, đặt ngay trên nguyên văn đã kiểm; thẻ ghi rõ câu in đậm là diễn giải, đoạn trong ngoặc kép là nguyên văn đã đối chiếu.
   Vì sao: nguyên văn trung thực nhưng không phải lúc nào cũng trả lời thẳng câu hỏi, trong khi sản phẩm hứa câu trả lời bằng tiếng Việt thường (AI đề xuất); [chờ Hiệp].

2. Phiên bản và hiệu lực
   Trước: thẻ chỉ ghi ngày bắt đầu hiệu lực, và AI không được biết ngày nào.
   Sau: thẻ ghi bản đang dùng áp dụng đến hết ngày nào và bản nào thay nó, do luật tính; AI nhận ngày áp dụng và khoảng hiệu lực của từng đoạn, để câu trả lời nói được quy định áp dụng đến khi nào.
   Vì sao: câu hỏi kiểm thử số 18, Minh hỏi số ngày phép năm sau, là câu trả lời nguy hiểm duy nhất của Mission 2: hỏi năm sau nhưng nhận 14 ngày của năm nay.

3. Mâu thuẫn giữa nhiều nguồn
   Trước: chỉ luật tìm mâu thuẫn, từ chủ đề và quan hệ mà chủ sở hữu khai.
   Sau: AI cũng được báo khi hai đoạn trích của hai văn bản nói khác nhau; luật kiểm lời báo rồi mới hiện thẻ mâu thuẫn, và AI không bao giờ bỏ được thẻ mâu thuẫn.
   Vì sao: một chủ đề khai sai đã cho ra một thẻ trả lời có cả 12 và 13 ngày (câu hỏi kiểm thử số 19, Hà hỏi số ngày phép năm, lần chạy 21/10/2026).

4. Quyền truy cập
   Trước: người hỏi là một tham số trên đường dẫn, nên ai cũng hỏi được với tư cách người khác.
   Sau: máy chủ quyết định người hỏi qua đăng nhập bằng tài khoản giả lập; thêm tài khoản Hoa để thấy quyền được cấp, không chỉ bị từ chối.
   Vì sao: kiểm quyền theo người hỏi chỉ có nghĩa khi người hỏi không tự khai được (AI đề xuất).

5. Từ chối khi chưa đủ căn cứ
   Trước: mọi lý do từ chối ra cùng một câu "không tìm thấy quy định".
   Sau: ba câu từ chối theo lý do, do luật chọn; câu trả lời nói phần nào của câu hỏi nó không trả lời.
   Vì sao: "không tìm thấy quy định" có thể bị hiểu là không có quy định, trong khi AI đã trả lời nhưng câu trả lời không kiểm được.

6. Kiểm chứng nguồn
   Trước: nhân sự chỉ thấy câu trích.
   Sau: từ thẻ mở được nguyên phiên bản được trích, đoạn trích được tô sáng; máy chủ kiểm lại quyền của người hỏi trước khi mở.
   Vì sao: nhân sự không xem được phần còn lại của điều khoản, kể cả ý mà câu trả lời bỏ sót (câu hỏi kiểm thử số 3, Minh hỏi xin nghỉ phép ở đâu, ai duyệt).

7. Change Request: [chờ đề]

CHỦ ĐỘNG CHƯA LÀM: toàn bộ phía chủ sở hữu văn bản, và mọi thay đổi giúp trả lời được nhiều hơn nhưng kém an toàn hơn.
Nguyên tắc đứng sau phần này: khi còn nghi quy định nào áp dụng thì chuyển HR, không chọn một bên.

- Trang cho chủ sở hữu ban hành văn bản, và kiểm tra mâu thuẫn lúc ban hành.
  Thay vào đó: văn bản vẫn là tệp viết tay, và quy tắc cho chủ sở hữu được ghi thành quyết định thiết kế: sửa một điều thì ban hành bản mới đầy đủ; văn bản áp dụng cho một đơn vị thì mọi người trong đơn vị phải được xem.
  Vì sao: 5 yêu cầu chung đều nói về điều nhân sự nhận được (AI đề xuất); [chờ Hiệp].

- Cho AI bỏ thẻ mâu thuẫn khi hai bên nói giống nhau ở điểm được hỏi (câu hỏi kiểm thử số 17, Hà hỏi đơn nghỉ phép gửi cho ai duyệt).
  Thay vào đó: thẻ mâu thuẫn giữ nguyên và chuyển HR; AI chỉ được thêm mâu thuẫn, không được bỏ.
  Vì sao: một lần đọc sai sẽ thành một câu trả lời sai được đưa ra một cách tự tin.

- Trả lời câu hỏi về năm sau bằng nội dung của bản năm sau.
  Thay vào đó: thẻ nói bản hiện tại hết hạn khi nào và bản nào thay.
  Vì sao: chọn bản theo câu hỏi là để AI quyết định hiệu lực.

- Kiểm câu AI viết lúc chạy, bằng luật về con số hay bằng một lệnh gọi mô hình thứ hai.
  Thay vào đó: một dòng cố định trên thẻ nói câu in đậm là diễn giải, đoạn trong ngoặc kép là nguyên văn đã đối chiếu; Hiệp đọc từng câu của lần chạy.
  Vì sao: luật về con số sẽ từ chối cả câu đúng có nêu ngày hiệu lực, mà vẫn không bắt được một điều kiện bị bỏ; mô hình thứ hai là thêm một thứ phải tin.

- Code tự phát hiện và sửa lỗi khai báo của chủ sở hữu.
  Thay vào đó: luật áp dụng đúng như được khai.
  Vì sao: đây là lỗi của thông tin chủ sở hữu khai nên hệ thống không cần sửa cho trường hợp này.

Danh sách đầy đủ, với rủi ro được chấp nhận và khi nào làm lại: https://github.com/Park-Hip/next-gen-2026/blob/main/docs/mission3/choices.md
```

## Câu 2

```text
Câu 2. Thay đổi nào tạo ra khác biệt lớn nhất giữa sản phẩm Mission 2 và Mission 3? Bạn dùng bằng chứng nào để kết luận phiên bản mới tốt hơn?

THAY ĐỔI LỚN NHẤT: AI không chỉ chọn và trích điều khoản nữa, mà viết câu trả lời và báo mâu thuẫn; luật vẫn kiểm mọi đoạn trích và vẫn quyết định loại thẻ.

Ở Mission 2, AI chọn điều khoản và trích nguyên văn.
Thẻ chỉ hiện nguyên văn đã kiểm, nên nhân sự phải tự suy ra câu trả lời, và mâu thuẫn chỉ do luật tìm, từ thông tin chủ sở hữu khai.

Mission 3 giao cho AI hai việc mới, và mỗi việc có một luật chặn phía sau:

1. AI viết câu trả lời
   AI viết một câu tiếng Việt trả lời thẳng câu hỏi, đặt ngay trên nguyên văn đã kiểm.
   Ngoài ra, AI còn nhận ngày áp dụng và khoảng hiệu lực của từng đoạn, nên câu trả lời nói được quy định áp dụng đến khi nào.
   Luật chặn: một đoạn trích không khớp từng chữ với văn bản thì cả câu trả lời bị từ chối; câu của AI không đổi được loại thẻ; thẻ mâu thuẫn và thẻ từ chối không hiện câu của AI; thẻ trả lời ghi rõ câu in đậm là diễn giải, đoạn trong ngoặc kép là nguyên văn đã đối chiếu.

2. AI báo mâu thuẫn
   AI được báo khi hai đoạn trích của hai văn bản trả lời câu hỏi khác nhau, kể cả khi thông tin chủ sở hữu khai không cho thấy mâu thuẫn.
   Luật chặn: lời báo chỉ được nhận khi cả hai đoạn đã được tìm thấy, được trích đúng nguyên văn và thuộc hai văn bản khác nhau trong phạm vi của người hỏi.
   Lời báo chỉ thêm được thẻ mâu thuẫn; AI không bao giờ bỏ được thẻ mâu thuẫn, và không đổi được một lần từ chối thành câu trả lời.

Đây là khác biệt lớn nhất vì nó đổi mọi thẻ trả lời: nhân sự đọc một câu trả lời, không còn phải tự suy ra từ nguyên văn.
Và lần đầu tiên AI thêm được một mâu thuẫn mà luật không tự thấy, nhưng chỉ theo hướng an toàn hơn: chuyển nhân sự tới HR (AI đề xuất).

TRƯỚC VÀ SAU, CÙNG MỘT CÂU HỎI

Câu hỏi kiểm thử số 18. Minh, ngày 15/12/2026: "Từ năm sau tôi được nghỉ phép năm bao nhiêu ngày?"
- Mission 2 (lần chạy 14/10/2026 lúc 22:39): thẻ chỉ có nguyên văn "Nhân sự GameCo được nghỉ phép năm 14 ngày mỗi năm." và nguồn "hiệu lực từ 01/01/2026", không nói gì về năm sau, nên người đọc hiểu năm sau cũng 14 ngày. Kết quả: Chưa đạt; đây là câu trả lời nguy hiểm duy nhất của Mission 2.
- Mission 3: câu của AI phải nói 14 ngày chỉ áp dụng đến hết 31/12/2026: [chờ lần chạy cuối]. Dưới câu đó, luật luôn thêm nguồn "hiệu lực từ 01/01/2026 đến hết 31/12/2026" và dòng "Sắp thay đổi: Quy chế nghỉ phép GameCo (bản 3) áp dụng từ 01/01/2027.", dù AI viết gì. Kết quả: [chờ lần chạy cuối].

Câu hỏi kiểm thử số 19. Hà, ngày 07/10/2026: "Phép năm của tôi là bao nhiêu ngày?", trên dữ liệu đã sửa: quy chế PayCo bị khai sai chủ đề, nên luật không thấy nó mâu thuẫn với quy chế Tập đoàn.
- Trước khi AI được báo mâu thuẫn (lần chạy 21/10/2026): một thẻ trả lời có cả 12 ngày của Tập đoàn và 13 ngày của PayCo, không nói quy định nào áp dụng cho Hà.
- Mission 3: AI báo hai đoạn nói khác nhau, luật kiểm lời báo rồi hiện thẻ mâu thuẫn trích cả hai bên và mời hỏi HR PayCo: [chờ lần chạy cuối].

BẰNG CHỨNG, TỪ CHẮC NHẤT
1. Luật, lặp lại được, không gọi mạng: bộ kiểm thử chứng minh câu của AI không đổi được loại thẻ và không hiện trên thẻ mâu thuẫn hay thẻ từ chối; mọi kiểu lời báo mâu thuẫn sai (một mã, ba mã, đoạn chưa được tìm thấy, đoạn ngoài phạm vi của người hỏi, đoạn được tìm thấy mà không được trích, hai đoạn của cùng một văn bản) đều bị bỏ qua; lời báo không bỏ được thẻ mâu thuẫn và không đổi được một lần từ chối; dòng hạn và dòng "Sắp thay đổi" có mặt dù AI viết gì. Bộ kiểm thử tăng từ 232 bài đạt ở bản nộp Mission 2 lên 434 bài đạt ở bản Mission 3 ngày 21/10/2026.
2. Đọc tay: Hiệp đọc từng câu AI viết, so với nguyên văn ngay dưới nó, và gọi tên lỗi khi câu thêm ý, bỏ điều kiện hay đổi số: [chờ lần chạy cuối]. Đây là bằng chứng chính cho việc câu trả lời bằng lời vẫn trung thực, vì không luật nào kiểm câu đó lúc chạy.
3. Lần chạy thật: 18 câu hỏi kiểm thử của Mission 2 chạy lại trên mã Mission 3, qua cùng bộ chạy với bản demo và cùng các cổng của Mission 2 (luật đúng, 0 rò rỉ, 0 câu trả lời nguy hiểm, từ chối nhầm trong mục tiêu): [chờ lần chạy cuối]. Câu hỏi kiểm thử số 3 (Minh hỏi xin nghỉ phép ở đâu, ai duyệt) và số 20 (Minh hỏi ngày nghỉ bù sau làm thêm giờ có trừ vào phép năm không) canh lời báo mâu thuẫn nhầm. Bảng trước/sau của từng câu hỏi kiểm thử được sinh từ hai lần chạy đã lưu trong kho mã, không sửa tay.

GIỚI HẠN CỦA BẰNG CHỨNG
- Câu của AI không được kiểm lúc chạy: bộ kiểm thử ghi rõ rằng một câu sai số đặt trên một đoạn trích đúng vẫn ra thẻ trả lời. Chỗ dựa là nguyên văn ngay dưới câu và việc đọc tay.
- Khi AI không nhận ra mâu thuẫn, hoặc một bên không được tìm thấy, nhân sự vẫn nhận thẻ trả lời trích một bên.
- Mỗi câu hỏi kiểm thử chỉ được hỏi một lần, vì giới hạn của gói miễn phí Gemini, nên phần do AI làm chưa có tỷ lệ; phần chắc chắn là phần do luật tính.

Chi tiết từng khoảng trống và cách sửa: https://github.com/Park-Hip/next-gen-2026/blob/main/docs/mission3/gaps.md
```

## Câu 3

```text
Câu 3. Nếu sản phẩm này được đưa cho người dùng thật vào ngày mai, rủi ro hoặc giới hạn lớn nhất còn lại là gì? Bạn sẽ ưu tiên xử lý nó như thế nào?

RỦI RO LỚN NHẤT: thông tin chủ sở hữu khai cho văn bản. Mọi bảo đảm của sản phẩm, từ 0 rò rỉ tới đúng bản và thẻ mâu thuẫn, chỉ đúng khi thông tin đó đúng, và Mission 3 chưa có chỗ nào kiểm nó.
Luật áp dụng đúng như được khai, từ bốn thông tin: văn bản áp dụng cho đơn vị nào, ai được xem, chủ đề, và quan hệ "dùng thay" hay "bổ sung".
Hôm nay các thông tin này được gõ tay trong tệp và không ai kiểm.
Khai sai thì thẻ vẫn trông như đúng, nên nhân sự khó nhận ra.

Khai sai ở đâu, nhân sự nhận được gì:
- Ai được xem, rộng hơn thật: nội dung bị hạn chế lộ ra, lần nào cũng lộ. Đã thấy trong phép thử: mở bảng lương cho mọi nhân sự thì Minh nhận cả hai đoạn về lương.
- Chủ đề, hoặc "bổ sung": thẻ trả lời trích một bên của một mâu thuẫn; chỉ được chặn khi AI nhận ra hai bên nói khác nhau và luật nhận lời báo đó. Đã thấy ở câu hỏi kiểm thử số 19 (Hà hỏi số ngày phép năm).
- "Dùng thay": mất cả một quy định hoặc dùng nhầm quy định, không có dấu hiệu nào trên thẻ. Đã thấy ở câu hỏi kiểm thử số 15 (Minh hỏi xin nghỉ phép phải báo trước mấy ngày).

Rủi ro này lớn hơn rủi ro của câu do AI viết, vì câu của AI luôn có đoạn trích đã kiểm ngay dưới để đối chiếu, còn thông tin khai sai thì không hiện ra ở đâu trên thẻ (AI đề xuất).

XỬ LÝ, THEO THỨ TỰ
1. Trước khi mở: thay đăng nhập giả lập bằng tài khoản công ty, với đơn vị và vai trò lấy từ hệ thống nhân sự. Mỗi chủ sở hữu duyệt lại bốn thông tin trên của từng văn bản thật, cùng với phạm vi mà luật tạo ra cho từng đơn vị; công cụ in phạm vi này, kèm lý do giữ hay bỏ từng văn bản, đã có sẵn.
2. Việc xây đầu tiên: trang ban hành cho chủ sở hữu, có kiểm tra lúc ban hành.
   Bắt đầu từ quyền xem: cảnh báo khi một bản mới mở rộng hơn bản trước, hoặc khi nội dung trông như hạn chế mà lại mở cho mọi nhân sự, vì nội dung đã lộ thì không rút lại được (AI đề xuất).
   Sau đó là kiểm tra mâu thuẫn lúc ban hành: mỗi điều khoản mới được tìm với các điều khoản giống nó trong kho, một mô hình AI so sánh, và chủ sở hữu quyết bằng cách khai quan hệ hoặc sửa văn bản. Người có thẩm quyền quyết, còn luật lúc hỏi vẫn cố định.
3. Khi đã mở: báo cho hai chủ sở hữu mỗi khi nhân sự gặp thẻ mâu thuẫn, ghi vết từng câu hỏi để giải thích được một câu trả lời sai, và chạy lại bộ kiểm thử trên văn bản thật.

Các hạn chế còn mở, mỗi hạn chế một issue: https://github.com/Park-Hip/next-gen-2026/issues?q=is%3Aissue+is%3Aopen+label%3Alimitation
```
