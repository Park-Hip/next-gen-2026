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
