# Trợ lý tri thức nội bộ: đúng người, đúng quyền, đúng phiên bản

**Bài test B - Tri thức nội bộ Appota - Mission 1**
**Ứng viên:** [Họ tên]

> Một văn bản liên quan chưa chắc đã được phép xem, đang có hiệu lực, hay áp dụng cho người hỏi.
> Thiết kế này giao ba phép kiểm tra đó cho luật trên metadata; AI chỉ tìm đoạn văn bản và viết câu trả lời có trích nguồn; khi luật không biết văn bản nào đúng, hệ thống nói rõ thay vì đoán.
> Mọi đơn vị, nhân sự, văn bản và con số trong tài liệu là **giả lập**.

## 1. Vấn đề & người dùng

**Vấn đề quan trọng nhất: nhân sự không biết chắc quy định nào đang áp dụng cho chính mình.**
Họ không thiếu tài liệu; họ thiếu một câu trả lời đúng với đơn vị của mình, trong phạm vi mình được xem, theo phiên bản có hiệu lực hôm nay.

**Ví dụ xuyên suốt.** Minh làm ở phòng Studio của GameCo, một công ty thành viên.
Ngày 07/10/2026, Minh hỏi: "Phép năm của tôi là bao nhiêu ngày?"
Kho tài liệu có sáu văn bản nêu số ngày phép năm, câu chữ gần như giống nhau, nhưng chỉ một văn bản đúng với Minh:

| Văn bản | Ngày | Có đúng với Minh hôm nay không? |
|---|---|---|
| Quy chế nghỉ phép Tập đoàn | 12 | Không: quy chế GameCo được khai báo là dùng thay nó |
| Quy chế GameCo, bản 1 | 13 | Không: đã bị bản 2 thay thế |
| **Quy chế GameCo, bản 2** | **14** | **Có: đã ban hành, hiệu lực từ 01/01/2026** |
| Quy chế GameCo, bản 3 | 15 | Chưa: hiệu lực từ 01/01/2027 |
| Dự thảo quy chế GameCo, bản 4 | 16 | Không: dự thảo, chưa ban hành |
| Quy chế nghỉ phép PayCo | 13 | Không: Minh đọc được, nhưng nó chỉ áp dụng cho PayCo |

Một chatbot "tìm rồi trả lời" xếp sáu văn bản gần ngang nhau, vì độ tương đồng câu chữ không thấy trạng thái, ngày hiệu lực, đơn vị áp dụng hay quan hệ giữa văn bản.
Nó có thể trả lời 12, 13, 15 hay 16 ngày, hoặc "12 đến 16 ngày tùy quy chế", với giọng tự tin như nhau (minh họa, chưa đo).
Mô hình lớn hơn cũng không sửa được: thông tin còn thiếu nằm ở việc ai đang hỏi và ở metadata, không nằm trong câu chữ.
**Văn bản nguy hiểm nhất là văn bản giống văn bản đúng nhất.**

Ba phân biệt giữ xuyên suốt tài liệu:

- **Liên quan ≠ được phép xem:** Minh hỏi về khung bậc lương GameCo, nhưng chỉ HR GameCo được xem văn bản đó.
- **Được xem ≠ áp dụng cho mình:** Lan (Nhân sự Tập đoàn) đọc được quy chế GameCo, nhưng phép năm của Lan theo quy chế Tập đoàn: 12 ngày.
- **Mới nhất ≠ đang hiệu lực:** bản 3 và dự thảo bản 4 mới hơn bản 2, nhưng hôm nay chưa có hiệu lực.

**Vì sao chọn vấn đề này, không phải chống rò rỉ.** Rò rỉ phải bằng 0 trong mọi thiết kế, nên đó là điều kiện để phát hành, không phải vấn đề để chọn.
Áp dụng nhầm quy định là lỗi hằng ngày và vô hình: câu trả lời sai trông y như câu đúng, và người hỏi hành động theo nó, ví dụ lên kế hoạch nghỉ 15 ngày theo một bản chưa có hiệu lực.
Hai loại lỗi có giá khác nhau: câu trả lời sai mà người dùng tin thì đắt; câu "chưa chắc, hãy hỏi HR" chỉ đưa họ về tình trạng hiện nay.
Thiết kế chấp nhận lỗi thứ hai để tránh lỗi thứ nhất.

**Người dùng chính** là nhân sự các công ty thành viên, vào lúc cần ra một quyết định do quy định điều chỉnh (xin nghỉ, làm thêm giờ, đi công tác).
Kết quả họ cần: quyết định đúng ngay lần đầu, không phải chờ HR.
**Người dùng thứ hai** là chủ sở hữu văn bản (HR từng đơn vị): đăng văn bản một lần, bớt trả lời câu hỏi lặp lại, không bao giờ bị quy trách nhiệm vì lộ thông tin.
Không có họ, metadata không được cập nhật và hệ thống sai dần.

**Phạm vi:** quy định nhân sự, đi sâu vào phép năm vì chủ đề này đã chứa mọi cái bẫy trên; câu trả lời phụ thuộc đúng ba yếu tố đề bài nêu: đơn vị, quyền truy cập, phiên bản có hiệu lực.

## 2. Giải pháp & luồng hoạt động

**Ý chính: dựng bộ quy định của người hỏi trước, rồi mới tìm và trả lời bên trong bộ đó.**
Bộ quy định của một người là các văn bản họ được xem, đang có hiệu lực và áp dụng cho họ, sau khi xét văn bản nào dùng thay văn bản nào; mọi bước dựng bộ này là luật tất định trên metadata.

**Dữ liệu.** Hồ sơ người hỏi gồm đường đơn vị (Tập đoàn → GameCo → Studio) và vai trò.
Metadata của quy chế GameCo bản 2: **chuỗi phiên bản** (series) "Nghỉ phép GameCo"; **trạng thái** đã ban hành, **hiệu lực** từ 01/01/2026, không đặt sẵn ngày hết hạn; **quyền xem** mọi nhân sự; **áp dụng cho** GameCo và mọi đơn vị bên dưới; **dùng thay** (overrides) chuỗi "Nghỉ phép Tập đoàn"; **chủ đề** nghỉ phép, trong một danh sách cố định; **chủ sở hữu** HR GameCo.
Quan hệ thứ ba là **bổ sung** (complements): hướng dẫn đăng ký nghỉ phép bổ sung cho chuỗi "Nghỉ phép GameCo", cùng chủ đề mà không mâu thuẫn.

**Luồng 7 bước, lần vết với câu hỏi của Minh** trên 10 văn bản giả lập: bước 1-4 là luật và không đọc câu hỏi, bước 5-6 là AI, bước 7 là luật.

| Bước và luật | Với Minh, 07/10/2026 |
|---|---|
| 1. Mỗi chuỗi giữ bản đã ban hành có ngày hiệu lực muộn nhất, không sau hôm nay | Loại GameCo bản 1, bản 3, dự thảo bản 4 |
| 2. Giữ văn bản người hỏi được xem và áp dụng cho đơn vị của họ | Loại khung bậc lương (không có quyền), quy chế PayCo (không áp dụng) |
| 3. "Dùng thay", chỉ xét giữa các văn bản còn lại sau bước 2 | Loại quy chế Tập đoàn |
| 4. Đánh dấu cặp cùng chủ đề không có quan hệ khai báo là mâu thuẫn | Không có cặp nào; bộ quy định còn 4 văn bản: quy chế GameCo bản 2, hướng dẫn đăng ký nghỉ, làm thêm giờ, công tác phí |
| 5-6. AI tìm đoạn trong bộ quy định, trả lời có trích nguồn hoặc nói không tìm thấy | "14 ngày", trích Điều 2 quy chế GameCo bản 2 |
| 7. Trích văn bản thuộc cặp mâu thuẫn: thẻ mâu thuẫn; không còn trích dẫn hợp lệ: từ chối; còn lại: trả lời | Thẻ trả lời |

Bước 1 chạy trước bộ lọc vì bản nào thay bản nào thì như nhau với mọi người; nhờ vậy bản 1 không "sống lại" khi bản 3 thay bản 2.
Bước 3 chạy sau bộ lọc để quy chế GameCo không che quy chế Tập đoàn với người ngoài GameCo như Lan.
Vì bước 1-4 không đọc câu hỏi, lỗi tìm kiếm không thể đưa bản cũ, dự thảo hay văn bản mật vào câu trả lời.

**Khi dữ liệu thay đổi, không sửa code:** ngày 01/01/2027 bản 3 tự thành bản hiện hành, bản 3 bị hoãn thì bản 2 vẫn có hiệu lực; Tập đoàn ra quy chế mới thì quy chế GameCo vẫn dùng thay nó, vì quan hệ trỏ tới chuỗi chứ không tới một bản.
**Kiểm tra lúc đăng:** cùng bộ luật chạy cho mọi đơn vị, hôm nay và mỗi ngày có bản mới bắt đầu hiệu lực, để liệt kê cặp mâu thuẫn chưa khai báo trước khi có ai hỏi; chủ sở hữu ra bản mới, khai "dùng thay", "bổ sung" hoặc gộp văn bản trùng.
Trong MVP đây là một script; bước 4 là cùng hàm đó, giữ lại làm lưới an toàn.

**Ba thẻ kết quả.** Mỗi thẻ ghi "Bạn đang hỏi với tư cách" để người hỏi thấy hệ thống dùng bộ quy định của ai.

| Trả lời: Minh hỏi phép năm | Mâu thuẫn: Hà (PayCo, Kế toán) hỏi phép năm | Từ chối: Minh hỏi khung bậc lương |
|---|---|---|
| *Bạn đang hỏi với tư cách: nhân sự GameCo, Studio.*<br>**Phép năm của bạn là 14 ngày mỗi năm.**<br>Nguồn: Quy chế nghỉ phép GameCo (bản 2), Điều 2, hiệu lực từ 01/01/2026. Hỏi thêm: HR GameCo.<br>**[Báo sai]** | *Bạn đang hỏi với tư cách: nhân sự PayCo, Kế toán.*<br>**Có hai quy định cùng áp dụng cho bạn và chúng khác nhau. Hệ thống không tự chọn.**<br>Quy chế Tập đoàn (từ 01/01/2024): 12 ngày. Quy chế PayCo (từ 01/01/2025): 13 ngày.<br>Vui lòng hỏi HR PayCo. Đã ghi nhận để HR Tập đoàn và HR PayCo xác nhận. | *Bạn đang hỏi với tư cách: nhân sự GameCo, Studio.*<br>**Hệ thống không tìm thấy quy định phù hợp để trả lời câu hỏi này cho bạn.**<br>Hệ thống chỉ trả lời các quy định áp dụng cho bạn. Vui lòng liên hệ HR GameCo. |

Với Hà, PayCo chưa khai báo quan hệ với quy chế Tập đoàn, nên luật không có căn cứ để chọn.
Câu từ chối giống hệt nhau cho "không có quyền" và "không có văn bản", nên không để lộ rằng có văn bản mật.

## 3. AI, dữ liệu & con người

**Nguyên tắc: AI chỉ làm những việc mà khi nó sai, lỗi rơi về phía an toàn hoặc bị luật chặn lại.**

| AI làm | Nếu AI sai | AI không làm |
|---|---|---|
| Tìm đoạn liên quan trong bộ quy định, kể cả câu diễn đạt khác hay không dấu | Tìm sót: câu trả lời yếu đi hoặc thành từ chối, người hỏi quay về hỏi HR như hiện nay | Quyết định ai được xem gì, bản nào có hiệu lực, văn bản nào áp dụng cho ai |
| Viết câu trả lời chỉ từ đoạn tìm được, trích nguồn từng ý, hoặc nói "không tìm thấy" | Trích văn bản ngoài bộ quy định: luật bỏ trích dẫn đó | Chọn văn bản thắng, phán xét mâu thuẫn, đoán chủ đề hay đơn vị câu hỏi nhắm tới, chọn thẻ |

**Lỗ hổng còn lại: LLM trích một văn bản trong bộ quy định nhưng không trả lời câu hỏi**; luật không chặn được, vì văn bản đó hợp lệ với người hỏi.
Ví dụ: Lan hỏi "Nhân sự GameCo được nghỉ phép năm bao nhiêu ngày?", LLM trích quy chế Tập đoàn và trả lời "12 ngày".
Cùng với lỗi diễn đạt sai nội dung (đo bằng độ trung thành), đây là đường còn lại tới câu trả lời sai tự tin, nên nó là giả định rủi ro nhất ở Phần 5.

**Dữ liệu và công cụ cho v1:** bộ chọn persona thay cho hệ thống nhân sự (bản thật không để người dùng tự khai đơn vị); 10 văn bản Markdown chia đoạn theo Điều; một retriever đơn giản và một LLM, không fine-tune vì văn bản đổi theo phiên bản và phải trích được nguồn.

**Con người tham gia ở đâu:**

- **Chủ sở hữu văn bản** là người duy nhất quyết định văn bản nào dùng thay hay bổ sung cho văn bản nào, một lần cho mỗi cặp, lúc đăng; họ xử lý danh sách của kiểm tra lúc đăng, nhận báo sai và các trường hợp mâu thuẫn.
- **HR đơn vị của người hỏi** nhận câu hỏi bị từ chối hoặc gặp mâu thuẫn, và yêu cầu xin quyền xem.
- **Nhân sự** đối chiếu nguồn trên thẻ và bấm "Báo sai"; báo cáo gồm câu hỏi, câu trả lời, văn bản được trích và người hỏi.

## 4. Quyết định & rủi ro

**Quyết định 1 - Ai quyết định văn bản nào thắng khi nhiều văn bản cùng áp dụng.**

- **A, chọn:** luật trên quan hệ do chủ sở hữu khai báo; hai văn bản cùng chủ đề, cùng áp dụng, không có quan hệ là mâu thuẫn: hiện cả hai.
  **B:** vẫn lọc bằng luật, nhưng khi còn nhiều văn bản thì LLM đọc nội dung, chọn văn bản thắng hoặc ghép câu trả lời.
- **B tốt hơn ở:** không cần ai khai báo; đọc được câu "quy chế này thay thế quy chế Tập đoàn" trong văn bản; xử lý được công ty chỉ sửa một điều; Hà có ngay một con số.
- **Vì sao A:** với Hà, không văn bản nào nói văn bản nào thắng, nhưng B vẫn đưa ra một con số, tự tin như nhau dù đúng hay sai: chính là lỗi ở Phần 1.
  A cho cùng kết quả với cùng dữ liệu nên kiểm thử được từng dòng; người quyết định là chủ sở hữu, một lần, chứ không phải LLM ở mỗi câu hỏi.
- **Cái giá:** chủ sở hữu phải khai báo (kiểm tra lúc đăng chỉ ra cặp còn thiếu); Hà phải hỏi HR; quy chế công ty phải đầy đủ về chủ đề của nó.
- **Đổi sang B khi:** thẻ mâu thuẫn hay hiện ở những cặp ai cũng biết văn bản nào thắng, hoặc công ty thường chỉ sửa một điều; khi đó LLM chỉ được thêm cảnh báo, không được chọn.

**Quyết định 2 - Câu hỏi gặp văn bản như thế nào.**

- **A, chọn:** luồng ở Phần 2: dựng bộ quy định không cần câu hỏi, tìm trong bộ đó, luật chọn thẻ theo văn bản được trích.
  **B:** LLM xếp câu hỏi vào danh sách chủ đề cố định, rồi luật tra văn bản áp dụng ở chủ đề đó; B cũng lọc bằng metadata.
- **B tốt hơn ở:** sau bước phân loại, việc chọn văn bản hoàn toàn tất định, và lỗi khoanh vào một bước đo được.
- **Vì sao A:** trong B, lỗi của AI (phân loại sai) quyết định LLM được thấy văn bản nào; trong A, lỗi của AI (tìm sót) chỉ làm câu trả lời yếu đi hoặc thành từ chối.
  Hà hỏi về làm thêm giờ, PayCo không có quy định này: A chỉ ra thẻ mâu thuẫn giả nếu LLM trích văn bản nghỉ phép, một lỗi trích dẫn mà bộ test bắt được; B chỉ cần xếp nhầm câu hỏi vào "nghỉ phép".
- **Cái giá:** retriever bỏ sót thì hệ thống từ chối dù có câu trả lời; kết quả phụ thuộc việc LLM trích đúng văn bản.
  **Đổi sang B khi:** lỗi thận trọng vượt ngưỡng ở Phần 5 mà sửa retriever không giảm được, hoặc LLM thường trích văn bản không trả lời câu hỏi.

**Quyết định 3 - Nhân sự hỏi trực tiếp, hay HR dùng trước.**

- **A, chọn:** nhân sự hỏi trực tiếp từ v1; thẻ ghi nguồn, ngày hiệu lực, người cần hỏi, có nút "Báo sai".
  **B:** HR dùng hệ thống để soạn câu trả lời, kiểm rồi mới gửi; mở cho nhân sự khi HR đã tin.
- **B tốt hơn ở:** lỗi bị HR chặn trước khi tới nhân sự; HR tin hệ thống qua trải nghiệm của chính mình và thấy metadata sai trong việc hằng ngày.
- **Vì sao A:** người dùng cần không phải chờ HR, mà B giữ nguyên việc chờ.
  Những gì HR sẽ kiểm (bản nào, được xem không, áp dụng không) là phần luật, kiểm thử được trên toàn bộ bộ test trước khi mở; khi luật không có đáp án, hệ thống tự chuyển về HR.
- **Cái giá:** câu LLM viết sai có thể tới nhân sự trước khi ai phát hiện, và lỗi không ai báo thì không ai biết; v1 chỉ trả lời quy định áp dụng cho chính người hỏi, nên HR chưa dùng được để trả lời hộ đơn vị khác.
- **Đổi sang B khi:** bộ test không qua các cổng ở Phần 5, HR không chấp nhận mở khi chưa tự kiểm, hoặc thí điểm có nhiều báo sai được xác nhận.

**Giả định:** trạng thái "dự thảo / đã ban hành" là của tôi, đề bài không nêu; bản tương lai không hiển thị trước ngày hiệu lực; mỗi người thuộc một đơn vị.

**Tình huống thất bại khác**, ngoài lỗ hổng ở Phần 3:

- **Chủ sở hữu khai báo sai:** hai văn bản khác nhau ở một điểm bị khai "bổ sung" và bị ghép thành câu trả lời sai; dữ liệu giả lập không kiểm được, chỉ thí điểm mới lộ ra.
- **Công ty chỉ sửa một điều của quy chế Tập đoàn:** "dùng thay" làm mất các điều còn lại; v1 chưa hỗ trợ.

## 5. Kiểm chứng & MVP

**Cách đánh giá: cùng câu hỏi, khác người hỏi hoặc khác ngày thì phải ra kết quả khác nhau.**
Bộ test có 10 dòng giả lập, ngày hỏi 07/10/2026 nếu không ghi khác; chữ đậm là văn bản trong bộ quy định của người hỏi, luật không loại được, chỉ LLM tránh trích được.

| Ai | Câu hỏi | Mong đợi | Không được trích |
|---|---|---|---|
| Minh | Phép năm của tôi là bao nhiêu ngày? | 14 ngày, GameCo bản 2 | Tập đoàn, GameCo bản 1, 3, 4, PayCo |
| Minh | Như trên, ngày 01/01/2027 | 15 ngày, GameCo bản 3 | GameCo bản 2 |
| Lan | Nhân sự GameCo được nghỉ phép năm bao nhiêu ngày? | Từ chối | GameCo, **Tập đoàn** |
| Hà | Phép năm của tôi là bao nhiêu ngày? | Thẻ mâu thuẫn | GameCo |
| Hà | Làm thêm giờ có cần ai duyệt trước không? | Từ chối, không phải mâu thuẫn | Làm thêm giờ GameCo, **hai quy chế nghỉ phép** |
| Minh | Khung bậc lương của GameCo thế nào? | Từ chối, như khi không có văn bản | Khung bậc lương, **mọi văn bản của Minh** |

Mỗi dòng hỏi theo 3 cách (nguyên văn, bỏ từ khóa, không dấu), thành 30 ca; mỗi ca chạy 3 lần, trượt nếu một lần trượt; phần luật của cả 10 dòng đã chạy đúng bằng một script nhỏ, phần AI chưa đo.

| Chỉ số | Ngưỡng | Lý do |
|---|---|---|
| Luật: đúng bộ quy định, đúng loại thẻ | 100% | Luật tất định: một lỗi là bug, không phải nhiễu |
| Luật: rò rỉ đoạn ngoài quyền xem | 0 | Đối chiếu mã đoạn với quyền xem |
| AI, lỗi nguy hiểm: trả lời khi phải từ chối, sai ý chính, trích văn bản cấm | 0 | Chính là vấn đề ở Phần 1 |
| AI, trung thành: mọi ý có trong đoạn được trích | 100% | Khoảng 45 câu trả lời, đọc tay hết |
| AI, lỗi thận trọng: từ chối khi đáng lẽ trả lời | ≤ 3/30 | Lỗi an toàn, nhưng quá 1/10 thì nhân sự bỏ dùng |

**Giả định rủi ro nhất:** khi không văn bản nào trong bộ quy định trả lời câu hỏi, LLM nói không tìm thấy thay vì dùng một văn bản không liên quan; khi có, LLM trích đúng văn bản đó; một lỗi nguy hiểm ở các ô chữ đậm là đủ bác bỏ giả định này.
Bốn ngưỡng đầu là cổng: qua cổng là điều kiện để mở cho nhân sự, không phải bằng chứng hệ thống luôn đúng: 0 lỗi trên 30 ca chỉ cho biết tỷ lệ lỗi thật dưới khoảng 9,5% (độ tin cậy 95%); tín hiệu thật là tỷ lệ báo sai được xác nhận khi thí điểm, chưa đo.

**MVP 3 ngày.** Ngày 1: văn bản, persona, luật bước 1-4 và 7, bộ 30 ca; xong khi các cổng phần luật đạt mà chưa có LLM, nên lỗi ngày 2 chỉ có thể do AI.
Ngày 2: retriever và LLM, chạy 30 ca × 3 lần, sửa prompt đến khi qua cổng hoặc ghi rõ lỗi.
Ngày 3: trang web có chọn persona và ngày, ba thẻ, nút "Báo sai", danh sách cho chủ sở hữu; cuối cùng chạy chatbot "tìm rồi trả lời" trên cùng 30 ca để so sánh.
Nếu trễ, bỏ phần so sánh trước, rồi đến trang danh sách; không bỏ bộ test và các cổng.
**Chủ động chưa làm** hệ thống nhân sự thật, tải văn bản lên, đọc PDF/DOCX, email cho chủ sở hữu, tích hợp công cụ chat, hội thoại nhiều lượt, số ngày phép còn lại: chúng không đổi văn bản, metadata hay danh tính, nên không làm yếu phép thử giả định rủi ro nhất.
