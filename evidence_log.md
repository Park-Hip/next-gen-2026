# Nhật ký Bằng chứng - Bài test B: Tri thức nội bộ Appota (Mission 1)

**Ứng viên:** Phạm Bách Hiệp

Nhật ký gồm hai phần.
Phần A tóm tắt việc dùng AI: ai làm gì, tôi đã bác bỏ hoặc đổi những gì, và dữ kiện nào đã được kiểm chứng.
Phần B ghi từng lần dùng AI theo thời gian, kèm prompt nguyên văn, đầu ra, quyết định của tôi và cách xác minh.

# Phần A - Tóm tắt

## A1. Tuyên bố trách nhiệm

> **[Hiệp tự viết, 4-6 câu, rồi xoá khung gợi ý này.]**
> Gợi ý các ý nên có, không phải câu chữ:
>
> - Phần việc của AI: viết gần như toàn bộ câu chữ của tài liệu 5 trang và 3 câu trả lời, đề xuất phần lớn chi tiết kỹ thuật, viết script kiểm tra luật.
> - Phần việc của tôi: chọn và duyệt mọi quyết định, nêu các ý chính ở mục A4, review bản nháp qua nhiều đợt và gửi lại khi chưa đạt.
> - Tôi giải thích được và chịu trách nhiệm cho mọi câu trong bài nộp.
> - Dữ liệu đều là giả lập; tôi không đưa dữ liệu thật hay dữ liệu cá nhân cho AI.

## A2. Công cụ

| Công cụ | Mô hình | Dùng để | Mục |
|---|---|---|---|
| Pi, agent chạy trong terminal, gọi mô hình Claude qua tiện ích claude-bridge (gói đăng ký Claude) | Claude Opus 5.5 | Thảo luận, đề xuất phương án, viết nháp tài liệu và câu trả lời, viết script kiểm tra luật, tìm kiếm web, review | 1-28, 30-37 |
| Pi, như trên | Claude Sonnet 5.5 | Chạy prompt Phase 2; phần cuối mục 18; 2 phiên phụ | 14, 18 |
| Pi, qua subagent | Agnes 2.5 Flash | Tìm nguồn web và kiểm tra lại trích dẫn; không nguồn nào vào bài nộp | 15, 17 |
| Claude Code (CLI) | Claude Opus 5.5 | Review "người đọc mới" cho tài liệu; một phiên brainstorm chỉ đọc file | 29 |
| ChatGPT web, Gemini web | ChatGPT `gpt-5-6-t-mini` (theo trang chia sẻ); Gemini 3 Pro (chưa chắc) | Review độc lập 3 câu trả lời | 36 |
| Lavish | Không | Tôi ghi chú review trực tiếp lên tài liệu | 26, 28, 31 |
| Wispr Flow | Nhận dạng giọng nói | Nhập prompt bằng giọng nói; không tạo nội dung | Nhiều mục |
| Orca CLI | Không | Quản lý dự án và phiên làm việc; không tạo nội dung | - |

Ở một phiên bị ngắt (08/10, 12:47), Pi tự khởi chạy subagent với GPT-5.5, GPT-6 (OpenAI) và Claude Fable 5.1; tôi dừng phiên và yêu cầu chỉ dùng Claude.
Không subagent nào trả về nội dung, và phiên không đổi file nào (mục 29).
Ngoài các công cụ trên, tôi không dùng công cụ AI nào khác cho Mission 1.

## A3. Nguồn gốc từng phần bài nộp

Câu chữ của mọi phần do Claude viết; tôi review, yêu cầu sửa và duyệt bản cuối.
Bảng dưới tách ý của tôi với đề xuất của AI mà tôi duyệt.

| Phần | Ý của tôi hoặc tôi quyết | AI đề xuất, tôi duyệt | Kiểm chứng |
|---|---|---|---|
| 1. Vấn đề & người dùng | Chấp nhận từ chối nhiều hơn để tránh trả lời sai (mục 3); chỉ giữ 3 yếu tố đề bài nêu: đơn vị, quyền, phiên bản (mục 12); gọi người hỏi theo vị trí thay vì tên nhân vật (mục 28) | Vấn đề cốt lõi, hai nhóm người dùng, phạm vi phép năm (mục 11); ba cặp khái niệm tách riêng (mục 1) | Số ngày phép và ngày hiệu lực trong bảng khớp văn bản giả lập |
| 2. Giải pháp & luồng | Không để AI phán mâu thuẫn (mục 4); hai văn bản chưa khai báo quan hệ là mâu thuẫn (mục 12); áp quan hệ thay thế trước khi tìm kiếm (mục 14); hỏi "vì sao phải chọn chủ đề", dẫn tới luật dựng phạm vi tìm kiếm trước (mục 19); hybrid search (mục 30) | Chuỗi phiên bản, quan hệ "bổ sung", bước đánh dấu cặp mâu thuẫn và bước chọn thẻ theo trích dẫn (mục 15-19); câu chữ trên ba thẻ | Script chạy bước 1-4 và 7 trên dữ liệu giả lập; câu trích trên thẻ mâu thuẫn khớp nguyên văn |
| 3. AI, dữ liệu & con người | AI không quyết quyền xem, hiệu lực, thứ tự ưu tiên (mục 4) | Phân vai AI, lỗ hổng còn lại, ba nhóm người tham gia | Đối chiếu với Phần 2 |
| 4. Quyết định & rủi ro | Quyết định 1 dựa trên lựa chọn ở mục 4 và 12; quyết định 2 từ câu hỏi ở mục 19; trình bày A cạnh B trong một bảng (mục 31) | Chọn 3 quyết định này (mục 21) và lập luận A-B (mục 22, 30) | Không có dữ kiện bên ngoài; ví dụ trên dữ liệu giả lập là suy luận, chưa đo |
| 5. Kiểm chứng & MVP | Bỏ bảng test chi tiết, thí điểm, so sánh với naive RAG; giảm độ tự tin của mục tiêu (mục 31); bỏ phần fine-tune (mục 32) | Chỉ số, giả định rủi ro nhất, thứ tự làm (mục 23, duyệt ở mục 25) | Phần luật chạy bằng script; phần AI chưa đo, bài nộp ghi rõ |
| 3 câu trả lời | Gửi lại bản đầu vì dài, lập luận về phương án khác và dùng thuật ngữ nội bộ (mục 33); duyệt các chỗ sửa sau review của ChatGPT và Gemini (mục 36) | Bản nháp và các chỗ sửa (mục 33, 36) | Số từ: 115 / 146 / 130 |
| Dữ liệu giả lập | Giữ trạng thái "dự thảo / đã ban hành" sau khi hỏi và xác nhận đây là giả định của chúng tôi; nêu tình huống hai văn bản cùng chủ đề không mâu thuẫn (mục 14) | 10 văn bản, persona, các bẫy, lần vết câu hỏi của nhân viên GameCo (mục 14-19) | Script dùng chính bảng dữ liệu này |

## A4. Những lần tôi bác bỏ hoặc đổi hướng AI

1. Bác bỏ đề xuất dùng LLM đọc hai đoạn văn bản để xác nhận có mâu thuẫn hay không, vì AI có thể ảo giác và nói "không mâu thuẫn"; chuyển cho người thật (mục 4).
   Đây là gốc của Quyết định 1 ở Phần 4.
2. Bỏ quy định pháp luật và mức tối thiểu theo luật khỏi MVP vì quá phức tạp (mục 12).
3. Hỏi mô hình dữ liệu dựa trên đề bài hay giả định của chúng tôi, rồi bỏ loại hợp đồng và thâm niên vì đề bài không nêu (mục 12).
4. Chỉ ra lỗi của thiết kế: hai văn bản cùng chủ đề bị coi là mâu thuẫn, dù chúng có thể bổ sung cho nhau; yêu cầu rà soát lại cả mô hình (mục 14-15).
5. Bác bỏ cách gắn nhãn câu hỏi cho từng đoạn văn bản (`covers`), vì phải gắn nhãn mọi đoạn và không dùng được cho văn bản không có cấu trúc (mục 17).
6. Khi Claude khuyến nghị để LLM xếp câu hỏi vào một chủ đề, tôi hỏi vì sao phải chọn chủ đề; câu hỏi này dẫn tới thiết kế dựng phạm vi tìm kiếm trước rồi mới truy xuất (mục 19).
7. Thay đề xuất tìm theo từ khóa sau khi bỏ dấu bằng hybrid search (mục 30).
8. Bỏ thí điểm và so sánh với naive RAG khỏi tài liệu, dù đã duyệt trước đó cùng ngày, vì tài liệu chỉ nêu những gì MVP làm (mục 31).
9. Không duyệt bản đầu của 3 câu trả lời và gửi lại kèm nhận xét cụ thể (mục 33).
10. Dừng Phase 2 sớm vì các bước sau không thêm giá trị cho bài nộp (mục 14).

## A5. Lỗi của AI đã phát hiện và sửa

- Script kiểm tra luật cho thấy bộ luật ban đầu sai: khi bản 3 có hiệu lực, bản 1 "sống lại"; khi Tập đoàn ra bản mới, mọi nhân sự GameCo nhận cảnh báo mâu thuẫn (mục 15).
- Bản đầu của bước kiểm tra lúc đăng văn bản bỏ sót ngày hết hiệu lực; Claude sửa và chạy lại (mục 18).
- Lượt kiểm tra thứ hai loại 3 nguồn web không xác minh được và 2 câu trích không có trên trang được dẫn (mục 15, 17); không nguồn web nào vào bài nộp.
- Bản nháp tài liệu có 2 khẳng định quá mức, Claude sửa khi đọc lại (mục 24).
- Lý do "chưa làm" ở Câu 2 ban đầu sai, vì hệ thống nhân sự quyết định đơn vị của người hỏi; ChatGPT phát hiện, đã sửa (mục 36).
- Chính nhật ký này: 3 khẳng định sai về việc ai làm gì, 1 phiên bị bỏ sót và 1 mô hình bị thiếu (sửa ở mục 20); các mục 30-36 ghi nhầm công cụ là Claude Code trong khi là Pi, và thiếu 4 phiên phụ (sửa ở mục 37).

## A6. Kiểm chứng dữ kiện trong bài nộp

**[Tôi]** tôi tự kiểm; **[AI]** AI kiểm bằng script hoặc đối chiếu file, tôi chưa tự kiểm lại.

| Dữ kiện | Cách kiểm | Kết quả | Ai kiểm |
|---|---|---|---|
| Bảng Phần 1: 12, 13, 14, 15, 16, 13 ngày phép và ngày hiệu lực | So với nội dung và metadata của 10 văn bản giả lập | Khớp | [AI], [Chưa] tôi kiểm |
| Hai câu trích trên thẻ mâu thuẫn (Phần 2) | So nguyên văn với Điều 1 của hai văn bản giả lập | Khớp | [AI], [Chưa] tôi kiểm |
| Luồng 7 bước cho nhân viên GameCo: 10, 7, 5, 4 văn bản, 0 cặp mâu thuẫn, kết quả 14 ngày | Lần vết từng bước, so với script | Khớp | [AI], [Chưa] tôi đọc từng dòng |
| "Phần luật của bộ test đã chạy đúng bằng script" (Phần 5) | Chạy script luật trên dữ liệu giả lập, ngày 08/10 | 10/10 tình huống đạt | [AI], [Chưa] tôi tự chạy |
| Số từ 3 câu trả lời, giới hạn 60-150 | Đếm theo khoảng trắng bằng script, chỉ phần trả lời | 115 / 146 / 130 | [AI], [Chưa] tôi đếm lại |
| Tài liệu tối đa 5 trang | Xuất PDF, đếm trang, xem ảnh từng trang | 5 trang | [AI] |
| Bài nộp không dẫn luật, số liệu thống kê hay nguồn bên ngoài | Đọc và tìm trong tài liệu và 3 câu trả lời | Không có; các dữ kiện pháp lý và nguồn web ở Phần B vì vậy được ghi [Không dùng] | [AI] |

Giới hạn đã biết:

- Script kiểm tra luật cũng do AI viết; nó chỉ kiểm phần luật, còn bước truy xuất và LLM được thay bằng một hàm giả lập, nên phần AI chưa được đo.
- Tài liệu 5 trang chỉ được review bởi mô hình cùng họ với mô hình viết nháp (Claude, mục 29); ChatGPT và Gemini chỉ đọc tài liệu để đối chiếu với 3 câu trả lời.
- Nhận định trong Phần 1 và Phần 4 về cách naive RAG hoặc phương án B có thể sai là suy luận trên dữ liệu giả lập, chưa đo; tài liệu ghi "dễ xếp", không đưa con số.

## A7. Dữ liệu và quyền riêng tư

Mọi đơn vị, nhân sự, văn bản và con số trong bài nộp là giả lập.
Prompt gửi cho AI chỉ chứa đề bài, ghi chú của tôi và dữ liệu giả lập; tôi không gửi dữ liệu thật của Appota hay dữ liệu cá nhân cho công cụ AI nào.
Đề bài trong dự án do tôi tự sao chép từ portal; bản AI thu thập từ portal đã bị xoá và không được dùng.

<div style="page-break-before: always"></div>

# Phần B - Nhật ký chi tiết

## Cách lập nhật ký này

- Nhật ký bắt đầu lúc 13:59 ngày 07/10 với prompt "First add today's AI use to the evidence log."
  Sau đó, cuối mỗi phiên, Claude ghi nháp mục mới.
- Lúc 17:16 tôi quyết định tạm giữ nhật ký ở dạng thô do AI viết và hoàn thiện sau ("For now keep the evidence log AI written, we should treat it as raw artifact and we will adjust them and polish later").
- Lúc 23:28 (mục 20), Claude đối chiếu nhật ký với lịch sử của cả 15 phiên Pi bằng script `tools/ai_sessions.py`, đọc trực tiếp file lưu phiên thay vì dựa vào trí nhớ của AI.
  Kết quả: thiếu một phiên định hình nội dung (nay là mục 14) và 9 phiên phụ (mục "Phiên AI không định hình nội dung bài nộp"); 3 khẳng định sai đã được sửa (mục 13, 15, 17); mục 18 thiếu Claude Sonnet 5.5; các ghi chép Round 2-3 do Claude viết thay tôi (mục 3).
- Lúc 20:30 ngày 08/10 (mục 37), Claude đối chiếu lại với file phiên của cả Pi và Claude Code, rồi viết Phần A, sửa công cụ và thời gian của các mục 25-36, thêm 4 phiên phụ và cập nhật các nhãn kiểm chứng.
- Prompt được trích nguyên văn từ lịch sử phiên, bằng tiếng Anh và giữ nguyên lỗi do nhập bằng giọng nói, kèm "Ý chính" bằng tiếng Việt.
  Đoạn dài được cắt bằng "[...]".
- Thời gian là giờ Việt Nam; mục 1-20 là ngày 07/10/2026, từ mục 21 là ngày 08/10/2026.
- Tên file là file làm việc trong dự án, không nộp kèm; các file nộp là tài liệu 5 trang, 3 câu trả lời và nhật ký này.
  Mục 1-7 dùng tên file trước khi thư mục được sắp xếp lại vào `docs/`, ví dụ `mission1_document_draft.md` → `docs/mission1/document.md`.
- Các mã như F1, M18, RV10 là mã dòng trong sổ quyết định làm việc (`decisions.md`): F là khung bài, M là mô hình lõi, A là dữ liệu và phân công viết, V là kiểm chứng, RV là thay đổi sau review.
  T1-T11 là các bẫy trong dữ liệu giả lập.
  P, S, L là 3 quyết định ở Phần 4 của tài liệu: P là Quyết định 1 (ai chọn văn bản thắng), S là Quyết định 2 (tìm văn bản cho câu hỏi bằng cách nào), L là Quyết định 3 (ai dùng trước); R (từ chối hay trả lời kèm cảnh báo) bị thay bằng L ở mục 21.

## Nhãn kiểm chứng

- **[Tôi]** tôi tự kiểm chứng; ghi rõ cách.
- **[AI]** AI kiểm chứng (chạy script, mở nguồn, đếm trang); tôi chưa tự kiểm lại.
- **[Duyệt]** tôi đọc và đồng ý, chưa kiểm chứng độc lập.
- **[Chưa]** chưa làm.
- **[Không dùng]** dữ kiện không có trong bài nộp, hoặc bản nháp đã bị thay, nên không cần kiểm chứng.

Trước khi nộp, mỗi mục [Chưa] phải được làm xong, hoặc dữ kiện liên quan bị bỏ khỏi bài nộp và chuyển thành [Không dùng].

## Phiên AI không định hình nội dung bài nộp

Liệt kê để nhật ký đầy đủ; các phiên này không tạo hoặc thay đổi nội dung bài nộp.

- **07/10, 08:31-09:07, Agnes 2.5 Flash:** thử thu thập đề từ portal.
  Prompt: "scrape this website and paste every information to this project https://portal.agentlize.dev/mission/1, remember to scan every buttons, sites, that it support and visible".
  Tôi yêu cầu xoá các file đã tạo ("Actually first remove all files that you created."), rồi dán văn bản đề và nhờ AI tóm tắt lại.
  Bản do AI viết này không được dùng: từ phiên đầu tiên lúc 09:43, mọi phiên đọc bản đề tôi tự sao chép trong `docs/competition/`, và không có lệnh ghi nào của AI tạo ra các file đó.
- **07/10, 09:08-09:42:** các phiên thử cài đặt Pi và kết nối mô hình (Claude Opus 5.5, Claude Sonnet 5, Agnes 2.5 Flash), ví dụ "Say hello in one sentence."; không tạo file trong dự án.
- **07/10, 09:15-09:28, Claude Code (CLI), Claude Opus 5.5:** hỏi cốt lõi của cuộc thi và cách làm trước khi viết.
  Prompt: "I want you to first read the relevant files to understand that I'm in a competition and this is a preparation phase of the task so there's no coding need but I need to implement a plan according to the rules. Do not make the PDF first. First tell me: what are the core things of this competition, these requirements? What should I do right now? [...]".
  Claude chỉ đọc đề bài và mẫu nộp bài rồi trả lời trong hội thoại; không tạo file.
  Tôi chuyển sang Pi và hỏi lại ý tương tự ở mục 1, nên phiên này có thể ảnh hưởng gián tiếp tới cách tôi đặt câu hỏi.
- **07/10, 11:31-11:35, Claude Opus 5.5:** tạo `AGENTS.md`, file hướng dẫn cho AI agent trong dự án, và thảo luận cách kiểm soát việc dùng AI.
  Prompt: "1. Read all the documents in the project. 2. I want you to create an agents.md or a Claude.md for this project. Make it short and brief and I will improve it later. 3. This composition requires a lock for AI usage so I want you to discuss this with me. How should we do that? [...]".
  `AGENTS.md` không thuộc bài nộp nhưng định hướng mọi phiên sau, ví dụ luận điểm cốt lõi và các quy tắc làm việc.
  Phiên này đã khuyên AI chỉ được ghi nháp mục nhật ký, không được tự đánh dấu đã xác minh; các phiên sau chưa làm theo, đến mục 20 mới sửa.
- **07/10, 14:53-14:56, Claude Opus 5.5 (trong phiên của mục 1-13):** sắp xếp thư mục và quản lý phiên bản bằng git ("I want to organize and set up for this project this like using github and clean up the file structure tell me what can I do now"); không đổi nội dung.
- **07/10, 16:05-16:11, Claude Sonnet 5.5, Lavish:** chuyển `review_output.md` thành trang HTML để tôi dễ đọc ("transform this into html do not add or change anything [...]"); không đổi nội dung.
- **07/10, 18:10-18:17, Claude Sonnet 5.5:** thêm mục "Scope discipline (MVP first)" vào `AGENTS.md`.
  Prompt: "I want to add this part to the agents.md. when AI giving some suggestions that sound cool but It's not suitable for the scope of the MVP and complicated or over-engineer for the current stage, which may delay our shipping time, so I want you to add something in agents.md to handle that."
  Quy tắc này ảnh hưởng gián tiếp: từ đó, ý tưởng ngoài phạm vi được đưa vào danh sách hoãn lại thay vì vào bài.
  Cùng phiên, AI ghi một ghi chú vào sổ tay cá nhân của tôi, ngoài dự án.
- **08/10, 12:38-12:40, Claude Opus 5.5:** tôi dán ghi chú review đợt 2 vào nhầm một phiên mới ("I'm writing my review notes for the lavish. Check in the documents. Write it down for me and change them also. [...]"); phiên không đổi file, tôi gửi lại ở mục 28.
- **08/10, 12:47-12:56, Claude Opus 5.5:** lần chạy đầu của prompt review "người đọc mới", bị ngắt; Pi tự khởi chạy subagent với các mô hình khác (xem mục 29); không có đầu ra nào được dùng.
- **08/10, 15:34-15:48, Claude Opus 5.5:** hỏi kế hoạch viết lại đã xong chưa ("is C:/Users/Hiep/orca/projects/next-gen/docs/mission1/redraft_plan.md done ?") và commit ("commit"); không đổi nội dung.

## Các mục định hình nội dung

### 1. Nghiên cứu cuộc thi và lập kế hoạch Mission 1

- **Thời gian:** 09:44.
- **Công cụ:** Claude Opus 5.5 qua Pi, có tìm kiếm web.
- **Prompt (nguyên văn):** "I want you to read the competition rules in the files I provided. I want best practices, an effective approach, and a thinking phase that I can do before the competition. I want to be very outstanding and impressive among the candidates so give me a big picture and outline of the direction of the competition. What should I do now?"
  Ý chính: đọc luật thi, cho tôi cách làm hiệu quả, giai đoạn suy nghĩ trước khi viết, bức tranh tổng thể và việc cần làm ngay.
- **Đầu ra:** `mission1_playbook.md`, gồm luận điểm cốt lõi (liên quan ≠ được phép ≠ đang hiệu lực ≠ áp dụng cho tôi), bảng persona giả lập, 8 bài tập tư duy, gợi ý nội dung 5 phần, lịch 48 giờ.
- **Dữ kiện AI tra cứu trên web:**
  - Lộ trình NextGen 2026 (Explore → Build → Become) và tiêu chí tuyển AI intern.
  - Các công ty thành viên công khai của Appota: Gamota, AppotaPay, Adsota, ACheckin, Kdata.
  - Bộ luật Lao động 2019, Điều 113-114: 12 ngày phép năm, cộng 1 ngày cho mỗi 5 năm làm việc.
  - Dự đoán Mission 2 là xây v1, Mission 3 là thích ứng với thay đổi: chỉ là suy đoán, chưa được xác nhận.
- **Quyết định của tôi:** dùng sổ tay này làm kế hoạch và làm bài tập tư duy trước khi viết (mục 2); luận điểm cốt lõi được giữ đến bản cuối.
- **Xác minh:**
  - **[Không dùng]** Bộ luật Lao động 2019, Điều 113-114: bài nộp không dẫn luật (quyết định M1c ở mục 12 bỏ quy định pháp luật khỏi MVP).
  - **[Không dùng]** Danh sách công ty thành viên của Appota và lộ trình NextGen.
  - Ghi chú: toàn bộ dữ liệu tổ chức và persona (GameCo, PayCo, AdsCo, Lan, Minh, Hà, An) là giả lập, không dùng dữ liệu thật của Appota.

### 2. Sổ tay bài tập tư duy (thinking workbook)

- **Thời gian:** 11:37 đến 13:48.
- **Công cụ:** Claude Opus 5.5 qua Pi, skill Lavish để tạo trang HTML tương tác, có tìm kiếm web.
- **Prompt (nguyên văn):** "I want you to brainstorm and discuss with me about this section and these exercises. 3. Thinking phase (do this before writing)I'm still a university student so I have no experience working in a company. My knowledge about this section is very, very limited. I want your help with this so you don't need to decide all the things for me. Just help me along, give me the options, discuss, and help me go along with these exercises."
  Ý chính: cùng brainstorm phần 3 (Thinking phase) và các bài tập; tôi chưa đi làm nên cần giúp đỡ, nhưng AI chỉ đưa lựa chọn và thảo luận, không quyết định thay tôi.
- **Đầu ra:** `.lavish/thinking-workbook.html`, gồm phần "Company 101" cho người chưa đi làm và 8 bài tập (kiểm kê câu hỏi, người dùng, thử phá RAG đơn giản, pre-mortem, nhật ký quyết định, định nghĩa "tốt", cắt phạm vi, kịch bản thay đổi).
- **Dữ kiện AI tra cứu trên web:**
  - Bộ luật Lao động 2019, Điều 118-119: doanh nghiệp từ 10 lao động phải có nội quy bằng văn bản và đăng ký với cơ quan lao động cấp tỉnh.
  - Luật Bảo vệ dữ liệu cá nhân số 91/2025/QH15, hiệu lực từ 01/01/2026.
  - Phương pháp pre-mortem của Gary Klein, Harvard Business Review, tháng 9/2007.
- **Phần tôi tự làm:** tôi tự trả lời tất cả bài tập trong sổ tay.
  Câu trả lời gốc được lưu nguyên văn trong `thinking_phase_answers.md` (Round 1).
- **Quyết định của tôi:** tự trả lời mọi bài tập; AI chỉ đưa lựa chọn và phản biện (mục 3).
- **Xác minh:**
  - **[Không dùng]** Điều 118-119, Luật 91/2025/QH15 và nguồn pre-mortem: bài nộp không dẫn các nguồn này.
  - Ghi chú: các con số minh họa trong sổ tay (điểm tương đồng khi tìm kiếm, số liệu Hệ thống A/B) chỉ dùng để luyện tư duy, không đưa vào bài nộp như dữ liệu thật.

### 3. Phản biện câu trả lời và chốt quyết định

- **Thời gian:** 13:48.
- **Công cụ:** Claude Opus 5.5 qua Pi.
- **Prompt (nguyên văn, nhập bằng giọng nói):** "A power detention, a higher decline rate. I choose that. After one salary leak I think that the HR is going to stop that. I'm not very sure about this question but that's my answer. Yes there is no group chat in my desire. It is for our own design. The group chat is not included in the scope. [...] Yes the chat conflicts will be decided later, in Ask time only in the third-day version. [...] I think that we should narrow them by just a decision that a policy governs. [...]"
  Ý chính: trả lời các câu hỏi phản biện của Claude về sổ tay: chấp nhận tỷ lệ từ chối cao hơn để đổi lấy an toàn, vì chỉ một lần lộ bảng lương là HR sẽ dừng hệ thống; thiết kế không có chat nhóm; kiểm tra mâu thuẫn chỉ lúc hỏi trong bản 3 ngày; thu hẹp người dùng chính.
- **Đầu ra:** nhận xét từng bài tập và 8 điểm mâu thuẫn giữa các câu trả lời của tôi (ví dụ: tỷ lệ từ chối tối đa 10% mâu thuẫn với việc chọn Hệ thống B từ chối nhiều hơn).
- **Quyết định của tôi (Round 2):** chấp nhận tỷ lệ từ chối cao hơn để đổi lấy độ an toàn; chỉ đánh giá rủi ro cho thiết kế của mình (không có chat nhóm); kiểm tra mâu thuẫn chỉ lúc hỏi trong bản 3 ngày; thu hẹp người dùng chính thành "nhân sự lúc cần ra một quyết định chịu sự điều chỉnh của quy định".
- **Nguồn gốc ghi chép:** ghi chép Round 2 và Round 3 trong `thinking_phase_answers.md` do Claude viết ở ngôi thứ nhất, dựa trên câu trả lời của tôi lúc 13:48 và 13:55.
  Phần mở rộng trong đó (ví dụ thứ bậc loại tài liệu, quan hệ `complements`, điều kiện đổi ý) là đề xuất của Claude mà tôi duyệt chung ở mục 4.
- **Xác minh:** không có dữ kiện cần kiểm chứng; đây là thảo luận và quyết định.

### 4. Bản nháp do AI viết cho các phần còn thiếu

- **Thời gian:** 13:48-14:14.
- **Trạng thái:** bản nháp tài liệu dựa trên các mục này đã được thay bằng bản viết lại (mục 10 trở đi); phần còn dùng được ghi lại thành quyết định trong `decisions.md`.
- **Công cụ:** Claude Opus 5.5 qua Pi.
- **Prompt (nguyên văn):**
  - "Complete the remaining and missing parts for me and let's move to the next stage." (cuối prompt 13:48)
  - "For the remaining decision that you chose for me, I approve that." (13:55)
  - "[...] On the decisions, the choice that you make has been verified by me because I think there are some decisions that you just gave your recommendation on and we have not discussed them further. If that's the case tell me" (14:06)
  - "For the seven items I approve it." (14:14)
  - Ý chính: nhờ AI hoàn thành phần còn thiếu; hỏi lại những quyết định AI chỉ đề xuất mà chưa thảo luận với tôi; duyệt 7 mục đó.
- **Đầu ra:** các mục ghi "Claude drafts" trong `thinking_phase_answers.md` (Round 2): lý do và điều kiện đổi ý cho D1-D6, top 3 rủi ro, kịch bản S01-S10, đề xuất nút "Báo sai", phạm vi HR cộng chính sách dùng AI, tách chỉ tiêu thành 95% câu đã trả lời đúng và tối đa 25% từ chối, bổ sung IT/bảo mật và pháp chế làm bên kiểm soát.
  Claude cũng liệt kê 7 đề xuất quan trọng chưa được thảo luận (thứ tự ưu tiên tài liệu, chỉ tiêu 95%/25%, phạm vi HR + chính sách dùng AI, nút "Báo sai", bỏ hội thoại nhiều lượt khỏi bản 3 ngày, top 3 rủi ro, một người thuộc nhiều đơn vị).
- **Quyết định của tôi:**
  - Duyệt chung toàn bộ bản nháp và 7 đề xuất trên, chưa thảo luận từng mục.
  - Bác bỏ một đề xuất của AI: dùng LLM để xác nhận hai tài liệu có mâu thuẫn hay không.
    Lý do của tôi (13:55, nguyên văn): "it would be good if there's an alert about the conflict in the documents but an AI who read the two passages thought that would be very effective because I can hallucinate. Should we direct them to a real human?"
    Ý chính: nên cảnh báo mâu thuẫn, nhưng không để AI đọc hai đoạn rồi phán xét vì AI có thể ảo giác và nói "không mâu thuẫn" khi thực ra có; chuyển cho người thật.
    Claude cụ thể hoá thành luật: luật xác định trên metadata coi là mâu thuẫn, trích nguyên văn hai điều khoản và chuyển chủ sở hữu tài liệu quyết định; tôi duyệt.
- **Xác minh:**
  - **[Duyệt]** Toàn bộ bản nháp và 7 đề xuất.
  - **[Không dùng]** Bản nháp này đã được thay; lý do của các quyết định còn dùng được viết lại ở mục 22 và tôi review qua các mục 26-34.

### 5. Bản nháp 3 câu hỏi bắt buộc

- **Thời gian:** từ 14:14.
- **Trạng thái:** đã được thay bằng bản viết lại ở Phase 6 (mục 33).
- **Công cụ:** Claude Opus 5.5 qua Pi.
- **Prompt (nguyên văn):** "Now I think that we can start drafting the draft right now." (14:14)
  Ý chính: bắt đầu viết nháp; AI viết nháp tiếng Việt cho 3 câu hỏi bắt buộc dựa trên các quyết định của tôi.
- **Đầu ra:** `mission1_answers_draft.md`.
- **Xác minh:**
  - **[AI]** Đếm số từ bằng script Python: Câu 1 = 125, Câu 2 = 130, Câu 3 = 133 từ, nằm trong giới hạn 60-150.
  - **[AI]** Câu 3 đã sửa theo quyết định của tôi (không dùng AI để phán xét mâu thuẫn).
  - **[Không dùng]** Bản nháp này đã được thay bằng bản viết lại ở mục 33; kiểm chứng bản nộp ở mục 33, 36 và Phần A6.

### 6. Bản nháp tài liệu 5 trang

- **Thời gian:** từ 14:14.
- **Trạng thái:** đã được thay bằng bản viết lại (mục 10 trở đi).
- **Công cụ:** Claude Opus 5.5 qua Pi.
- **Prompt (nguyên văn):** cùng prompt 14:14 ở mục 5.
- **Đầu ra:** `mission1_document_draft.md` (tiếng Việt, 5 phần + 3 câu trả lời) và script `tools/render_pdf.py` xuất bản nháp ra PDF A4 bằng Edge headless.
- **Quyết định của tôi:** giao Claude viết bản nháp đầu; sau khi đọc, tôi thấy bản nháp nhồi quá nhiều thông tin mà thiếu lập luận (mục 8), dẫn tới bản viết lại.
- **Xác minh:**
  - **[AI]** Xuất PDF và đếm trang bằng script: 5 trang (bản đầu 7 trang; đã đổi sơ đồ sang chiều ngang, gộp bảng để vừa giới hạn).
  - **[AI]** Kiểm tra từng trang bằng ảnh chụp: dấu tiếng Việt hiển thị đúng, bảng không tràn, chữ trong sơ đồ đọc được.

### 7. Prompt cho AI review độc lập

- **Thời gian:** 14:51.
- **Công cụ:** Claude Opus 5.5 qua Pi.
- **Prompt (nguyên văn):** "I want you to draft a prompt so a seperated AI can check and review the draft. I want it to point out what are the important things in the mission 1 that we should keep in mind, what are the best practices of doing them"
  Ý chính: soạn prompt để một AI khác review bản nháp, chỉ ra điều quan trọng của Mission 1 và best practice.
- **Đầu ra:** `review_prompt.md` (cập nhật theo tiêu chí mới ở mục 8).
- **Quyết định của tôi:** chạy prompt này trên Claude (mục 9), không chạy trên AI khác họ.
- **Xác minh:**
  - **[Không dùng]** Bản nháp được review đã bị thay toàn bộ.
  - Giới hạn: review khác họ mô hình chỉ được làm cho 3 câu trả lời (mục 35-36); tài liệu 5 trang chỉ có review cùng họ (mục 29).

### 8. Cập nhật theo tiêu chí chấm và yêu cầu nộp bài mới trong đề

- **Thời gian:** 14:44-15:14.
- **Công cụ:** Claude Opus 5.5 qua Pi.
- **Prompt (nguyên văn):**
  - "First remove the answers for three questions of the PDF because there's a separate submission section for those. read the @mission1_brief.md again to see the updated criterias, note down what are important for the submission. tell me what are the criterias for the mission 1 and how can we do it well. After reading the draft pdf, I realize that we try to dump so many information to it but there is no deep dive into them and no good reasoning." (14:44)
  - "I also add Tiêu chí chấm điểm cho mission 1 [...] to the @docs/competition/mission1_brief.md did you see that if yes change the relevant places also this is applied for mission 1" (14:57)
  - "not yet. about the new criterias, should we redraft the PDF files given the new criterias or should we review first. And if we need to review first please update the prompt also" (15:14)
  - Ý chính: bỏ 3 câu trả lời khỏi PDF vì nộp riêng; đọc lại tiêu chí chấm tôi đã thêm vào đề và sửa các chỗ liên quan; hỏi nên review trước hay viết lại trước.
- **Đầu ra:** bỏ 3 câu trả lời khỏi bản nháp PDF; cập nhật `AGENTS.md`, `docs/mission1/criteria.md`, `docs/mission1/review_prompt.md`, `docs/mission1/playbook.md`; thêm trường "Quyết định của tôi" vào mẫu nhật ký này.
- **Phần tôi tự làm:** sau khi đọc PDF nháp, tôi nhận xét bản nháp nhồi quá nhiều thông tin mà không đi sâu và thiếu lập luận.
  Nhận xét này dẫn tới review (mục 9) và kế hoạch viết lại (mục 10).
- **Quyết định của tôi:** áp dụng tiêu chí mới cho Mission 1; review trước khi viết lại; nhật ký bằng chứng được nộp kèm nên phải ghi rõ quyết định của tôi ở từng mục.
- **Xác minh:**
  - **[AI]** Đối chiếu nội dung cập nhật với nguyên văn đề trong `docs/competition/mission1_brief.md`.
  - **[AI]** Trường "Quyết định của tôi" của các mục 1, 2, 6, 7 được Claude điền ở mục 37 theo lịch sử phiên; tôi kiểm khi đọc lại nhật ký (mục 20).

### 9. Review bản nháp theo `review_prompt.md`

- **Thời gian:** 15:31-15:49.
- **Công cụ:** Claude Opus 5.5 qua Pi, có tìm kiếm web.
  Đây là cùng mô hình đã viết bản nháp, nên review này không độc lập và chưa hoàn thành mục 7 ("chạy prompt trên AI khác").
- **Prompt:** tôi chỉ gửi đường dẫn file `docs/mission1/review_prompt.md`; prompt thực tế là nguyên văn phần "Prompt" (Part A-G) trong file đó, chạy trong phiên mới, không có lịch sử hội thoại.
  Phiên này vẫn tự động đọc `AGENTS.md`, nơi có luận điểm cốt lõi của tôi, nên review có thể bị ảnh hưởng bởi luận điểm đó.
- **Đầu ra:** `docs/mission1/review_output.md`.
  Gồm: tiêu chuẩn chấm viết trước khi đọc bản nháp, điểm và nhận xét từng phần, kiểm tra quyết định, lập luận, tính khả thi và dữ kiện, khung cho bản viết lại, nhận xét 3 câu trả lời và nhật ký, 8 câu hỏi PITCH, 5 ưu tiên.
- **Dữ kiện AI tra cứu trên web:**
  - Bộ luật Lao động 2019, Điều 113-114 (hethongphapluat.com): đúng, với lưu ý 12 "ngày làm việc", tính theo tỷ lệ nếu chưa đủ 12 tháng, thâm niên tính "cho một người sử dụng lao động".
  - Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15 (chinhphu.vn): ban hành 26/06/2025, hiệu lực 01/01/2026.
  - Bộ luật Lao động 2019, Điều 118-119: đúng.
  - Theo Điều 2 khoản 1 Luật 91/2025/QH15, dữ liệu cá nhân phải xác định hoặc giúp xác định một người cụ thể, nên "Khung lương GameCo" trong bản nháp không phải dữ liệu cá nhân.
- **Quyết định của tôi:** không xử lý từng góp ý; nhờ Claude tóm tắt (mục 10) rồi viết lại toàn bộ tài liệu theo kế hoạch mới.
  Lỗi lập luận chính mà review nêu (thứ tự ưu tiên với mức sàn pháp lý) được xử lý bằng việc bỏ quy định pháp luật khỏi MVP (M1c, mục 12).
- **Xác minh:**
  - **[AI]** Claude đối chiếu các dữ kiện pháp lý trên với các trang ở trên; đây chưa phải nguồn chính thức.
  - **[Không dùng]** Các dữ kiện pháp lý trên: bài nộp không dẫn luật.
  - Giới hạn: không chạy lại trên AI khác họ (mục 7).

### 10. Tóm tắt review và kế hoạch viết lại

- **Thời gian:** 17:09-17:16.
- **Công cụ:** Claude Opus 5.5 qua Pi.
- **Prompt (nguyên văn):**
  - "summarize C:/Users/Hiep/orca/projects/next-gen/docs/mission1/review_output.md give me the most valuable information" (17:09)
  - "tell me a plan or road so I can redraft this document. I want a clear control of what is written and the decisions. For now keep the evidence log AI written, we should treat it as raw artifact and we will adjust them and polish later" (17:16)
  - Ý chính: tóm tắt review; cho tôi kế hoạch viết lại để tôi kiểm soát rõ nội dung và các quyết định; tạm giữ nhật ký ở dạng thô.
- **Đầu ra:** bản tóm tắt review trong hội thoại (lỗi logic ở thứ tự ưu tiên, điểm từng phần, khung viết lại, rủi ro của nhật ký); `docs/mission1/redraft_plan.md` gồm 8 giai đoạn (Phase 0-7).
- **Quyết định của tôi:** dùng kế hoạch 8 giai đoạn; quyết định trước khi viết; mọi quyết định ghi vào `docs/mission1/redraft/decisions.md` kèm nguồn gốc; giữ nhật ký này ở dạng thô và hoàn thiện ở Phase 7.
- **Xác minh:**
  - **[Không dùng]** Bản nháp được review đã bị thay toàn bộ; các review sau ở mục 29 và 36.

### 11. Phase 0 - Chốt khung bài (F1-F5)

- **Thời gian:** 17:26-17:39.
- **Công cụ:** Claude Opus 5.5 qua Pi.
- **Prompt (nguyên văn):**
  - "ready" (17:26)
  - "approve your lean for all questions except for F4. we need to discuss this further. I have limited knowledge about what decisions we have right now and the big picture is not clear to me so I can't answer this." (17:32)
  - "choose R and S and note that this can be opened for changes during the exploration" (17:39)
  - Ý chính: duyệt đề xuất của Claude cho F1-F5 trừ F4; nhờ giải thích bức tranh tổng thể; chọn R và S, có thể đổi sau.
- **Đầu ra:** các dòng F1-F5 trong `docs/mission1/redraft/decisions.md`.
- **Quyết định của tôi:**
  - F1, F2, F3, F5: chấp nhận đề xuất của Claude (vấn đề cốt lõi, nhân sự là người dùng chính và chủ sở hữu tài liệu là người dùng thứ hai, phạm vi quy định HR với ví dụ phép năm, bỏ chính sách dùng công cụ AI, phân bổ trang).
  - F4: Claude giải thích bức tranh tổng thể các quyết định; tôi tự chọn R (từ chối hay trả lời kèm cảnh báo) và S (cách tìm kiếm), cùng P (đề xuất của Claude); tạm thời, có thể đổi trong Phase 1-3.
- **Xác minh:** không có dữ kiện cần kiểm chứng; nguồn gốc từng quyết định được ghi trong `decisions.md`.

### 12. Phase 1 - Mô hình lõi (M0-M8) và phác thảo dữ liệu

- **Thời gian:** 17:47-18:29.
- **Công cụ:** Claude Opus 5.5 qua Pi.
- **Prompt (nguyên văn, chọn lọc):**
  - "is sets a minimum needed I do not want the legal rules to be included in this MVP it is to complicated we should include the internal document only. choose option b for M1b. And for M1a explain your lean, now I think it is too complicated" (17:54)
  - "should we decide the metadata of documents and the accessment metadata of employees first so we can I have a clearer understaning. Correct me if i am wrong" (18:01)
  - "Are the models based on real data in real life, in the competition descriptions or just an assumption created by us? I mean, in real life, do we filter, and divide the document by employment type, should we make this complicated like this at first?" (18:06)
  - "Approve the five blends except for M4. I want to see if there's a topic needed for the document. Should we include it in the metadata?" (18:24)
  - Các prompt còn lại là lựa chọn ngắn ("option b", "a", "Use your recommendation option. I approve them.").
  - Ý chính: bỏ quy định pháp luật khỏi MVP; hỏi mô hình dựa trên thực tế, đề bài hay giả định của chúng ta; hỏi có cần trường chủ đề không.
- **Đầu ra:** các dòng M0-M8 trong `decisions.md`; phác thảo dữ liệu và bảng lần vết câu hỏi của Minh trong `docs/mission1/redraft/artifacts.md` (Claude viết, chưa chốt); mục "Deferred ideas" trong `docs/mission1/playbook.md`.
- **Quyết định của tôi:**
  - M1c (tự đề xuất): chỉ dùng tài liệu nội bộ, bỏ quy định pháp luật và mức tối thiểu khỏi MVP.
  - M1b: chọn coi hai tài liệu cùng áp dụng mà không khai báo quan hệ là mâu thuẫn.
  - M0: sau khi hỏi nguồn gốc mô hình, chọn chỉ giữ đơn vị, quyền truy cập và phiên bản như đề bài; bỏ loại hợp đồng và thâm niên.
  - M1a: Claude ban đầu đề xuất nhãn theo điều khoản, sau khi tôi nói quá phức tạp thì đổi đề xuất; tôi chọn quan hệ thay thế và ghi đè cho cả văn bản.
  - M3a, M3b, M4-M8: chấp nhận đề xuất của Claude; M4 (trường chủ đề) được thảo luận riêng trước khi chấp nhận.
- **Xác minh:**
  - **[AI]** Claude phân loại nguồn gốc từng phần mô hình (đề bài, thực tế phổ biến, giả định của chúng tôi) theo nguyên văn đề bài.
  - Lần vết câu hỏi của Minh: xem mục 14.

### 13. Prompt cho Phase 2 (dữ liệu giả lập và lần vết)

- **Thời gian:** 19:20-19:26.
- **Công cụ:** Claude Opus 5.5 qua Pi.
- **Prompt (nguyên văn):**
  - "craft a prompt for this I will start a new session for this. Make the prompt detailed so that a simple worker model can do that" (19:20)
  - "is the previous saved in the evidence log" (19:24)
  - Ý chính: soạn prompt chi tiết cho Phase 2 để một mô hình đơn giản làm được, tôi sẽ chạy trong phiên mới; kiểm tra nhật ký đã ghi các việc trước chưa.
- **Đầu ra:** `docs/mission1/redraft/phase2_prompt.md` (9 bước: danh sách bẫy, persona, tài liệu, lần vết của Minh do tôi tự làm, các persona khác, so sánh RAG đơn giản và mô hình đúng, 3 thẻ trả lời, thí nghiệm embedding, ghi quyết định).
- **Quyết định của tôi:** lúc soạn prompt, tôi định tự lần vết câu hỏi của Minh và chỉ để mô hình kiểm tra.
  Khi chạy prompt ở mục 14, tôi đổi ý và giao bước này cho AI.
- **Xác minh:** prompt đã được chạy ở mục 14.

### 14. Chạy Phase 2: bẫy, persona, tài liệu giả lập và lần vết của Minh

- **Thời gian:** 19:25-20:18 và 21:58.
- **Công cụ:** Claude Sonnet 5.5 qua Pi. Không dùng tìm kiếm web.
- **Prompt (nguyên văn, chọn lọc):**
  - "implement C:/Users/Hiep/orca/projects/next-gen/docs/mission1/redraft/phase2_prompt.md" (19:25)
  - "i still don't understand T8 and check whether the status is derived from what, is there any source in the competition requires it for we assumpt it" (19:41)
  - "1A and why Lan does not have field like GameCo or PayCO and Minhs is Studio (is this a department) ?" (19:49)
  - "Approve. Actually about step 4, I need you to do that for me." (19:54)
  - "First where are the rules that you mention and why is that there is search topic? I think that it is a R.A.G. system and is supposed to search the query not the topic or am I misunderstanding something? In step C why are the documents filtered? Are they supposed to be filtered in step A instead, about the replace and override things?" (20:03)
  - "Let's clear up my understanding. I want to ask about the filter. We can filter the data (like who applies to the role) and override and replace based on the employee's metadata in the first place before the search, right? [...]" (20:09)
  - "I choose option A for question 1. And for the conflicts and the refusal, in realistic: is there a case when there are two documents about the same topic but they are separated? Do we think about those scenarios?" (20:13)
  - "I want you to note this down because it affects the whole system as a bug and I will send an agent to investigate this later. [...] I want our assumptions to align with the problem brief but I also want it to be applicable in real-life scenarios, not just a synthetic system." (20:18)
  - "I want to wrap this phase here since those next step do not really add values and I want to finish this quickly [...]" (21:58)
  - Các prompt còn lại là lựa chọn ngắn ("go", "Use option A for question 1.", "Approve.", "use your recommendation.").
  - Ý chính: chạy Phase 2; hỏi trường `status` có trong đề bài không; giao bước lần vết cho AI; chất vấn vì sao tìm theo chủ đề thay vì theo câu hỏi; đề xuất lọc và áp quan hệ theo metadata nhân sự trước khi tìm kiếm; nêu tình huống hai tài liệu cùng chủ đề nhưng tách biệt.
- **Đầu ra:**
  - `artifacts.md`: danh sách bẫy T1-T9 (Claude gộp T6 với T10 và siết T1), danh sách chủ đề, 3 persona (Minh, Lan, Hà; bỏ An vì M0 đã bỏ loại hợp đồng), bộ tài liệu giả lập, lần vết câu hỏi của Minh do Claude viết (ghi "Claude draft, pending Hiep's review").
  - `open_issues.md`: 5 vấn đề mở, trong đó vấn đề 1 là mâu thuẫn giả giữa hai tài liệu cùng chủ đề, kèm đề bài cho một agent rà soát (dẫn tới mục 15).
- **Quyết định của tôi:**
  - Chấp nhận danh sách bẫy, danh sách chủ đề và 3 persona theo đề xuất của Claude.
  - Giữ trường `status` và bẫy T3 sau khi hỏi nguồn gốc; Claude xác nhận đây là giả định của chúng tôi, không có trong đề bài.
  - Giao bước 4 (lần vết của Minh) cho AI, khác với kế hoạch ở mục 13.
    Ngày 07/10, tôi quyết định giữ bản lần vết do AI viết và khai báo ở đây thay vì tự làm lại.
  - Tự đề xuất: lọc và áp quan hệ `replaces`/`overrides` theo metadata nhân sự trước khi tìm kiếm; Claude xác nhận kết quả của Minh không đổi.
  - Tự nêu tình huống hai tài liệu cùng chủ đề nhưng không mâu thuẫn, và yêu cầu ghi lại như một lỗi của hệ thống để rà soát (mục 15).
  - Dừng Phase 2 sau bước 4; các bước 5-9 được rút gọn ở mục 19.
- **Xác minh:**
  - **[AI]** Claude đối chiếu trường `status` với đề bài và các file, xác nhận đây là giả định của chúng tôi.
  - **[AI]** Script kiểm tra luật ở mục 15-19 cho cùng kết quả với bản lần vết (14 ngày từ `LEAVE-GAMECO-v2`); script này cũng do AI viết.
  - **[Chưa]** Tôi đọc từng dòng bản lần vết cuối (7 bước, mục 19) và tự giải thích được, để chuẩn bị vòng PITCH.
    Sổ quyết định (A7) và tiêu đề bản lần vết đang ghi "Hiep checked every row"; câu này chỉ đúng sau khi tôi làm xong bước này.

### 15. Rà soát mô hình lõi theo thực tế vận hành

- **Thời gian:** 20:24-20:47.
- **Công cụ:**
  - Claude Opus 5.5 qua Pi: phân tích, viết 2 script kiểm tra luật, viết báo cáo.
  - Agnes 2.5 Flash (mức suy luận tối đa), qua 2 lượt subagent: tìm nguồn trên web, sau đó lượt thứ hai mở từng URL và so trích dẫn với nguyên văn.
- **Prompt (nguyên văn):** "I want you to read the data and the artifacts that we just created. My goal is to create artifacts and assumptions about the company that are most aligned with the competition's brief but I also want my system to be usable in real production with real companies. I do not want it to be constrained too much by the brief. [...] For example the current systems allow only one document for one topic after the RAG search. They would raise a warning or an alert whenever there are two documents retrieved about the same topic, which is a flaw, I think Because there can be two separate documents that both talk about the same topic but their contents do not contradict and conflict with each other . I want you to investigate and find out about some conflicts and some things that our current systems do not work well in real production. And find me the best practices or the solution so that I can solve it. You may use websearch if you need it and only use Agnes 2.5 Flash with max reasoning level for it. Only use it if you need it." (20:24)
  Ý chính: kiểm tra giả định và dữ liệu so với vận hành thật ở công ty; hệ thống hiện coi hai tài liệu cùng chủ đề là mâu thuẫn, tôi cho đó là lỗi; tìm chỗ hệ thống không chạy tốt và cách sửa; chỉ dùng Agnes 2.5 Flash để tìm web.
- **Đầu ra:**
  - `docs/mission1/redraft/production_review.md`: 9 phát hiện (P1-P9), đề xuất thay đổi dữ liệu, thứ tự ưu tiên, nguồn đã kiểm tra.
  - `docs/mission1/redraft/checks/current_rules.py`: cài đúng nguyên văn 7 luật lõi và chạy trên dữ liệu giả lập.
  - `docs/mission1/redraft/checks/proposed_rules.py`: bộ luật đề xuất, chạy trên cùng các kịch bản.
- **Phát hiện chính (do script chạy ra, không phải suy đoán):**
  - Ngày 01/01/2027, khi v3 có hiệu lực đúng kế hoạch, GameCo v1 "sống lại" và mâu thuẫn với v3, vì quan hệ `replaces` chỉ tính giữa các tài liệu còn lại sau bộ lọc.
  - Khi Tập đoàn ra bản mới, `overrides` trỏ vào phiên bản cũ nên mọi nhân sự GameCo nhận cảnh báo mâu thuẫn.
  - Thêm một quy trình xin nghỉ phép cùng chủ đề gây mâu thuẫn giả (vấn đề tôi nêu).
- **Quyết định của tôi (prompt 20:47 ở mục 16):**
  - Chấp nhận P1-P3 (chuỗi phiên bản, không gõ trước ngày hết hiệu lực, `overrides` trỏ vào chuỗi), ghi thành M9-M12 trong `decisions.md`.
  - P8: ghi là giới hạn đã biết của bản v1 (M13), không làm bộ chọn "Hỏi cho" trong MVP.
  - P4 (`covers`): thấy hướng này tốt nhưng cần hiểu rõ thay đổi trong luồng xử lý trước khi quyết định.
- **Xác minh:**
  - **[AI]** Script luật hiện tại cho cùng kết quả với bảng lần vết và kết quả mong đợi của Minh, Lan và Hà ở ngày 07/10/2026 (do AI viết, mục 14) trước khi chạy các kịch bản mới.
  - **[AI]** Lượt kiểm tra thứ hai của Agnes loại 3 nguồn không xác minh được (ISO 9001 mục 7.5.3, SAP SuccessFactors, cột metadata nhiều giá trị của SharePoint) và sửa một trích dẫn bị diễn giải.
  - **[Không dùng]** Nguồn S1-S10: bài nộp không dẫn nguồn web.
    2 script này là lịch sử; script đang dùng (`adopted_rules.py`) được kiểm ở Phần A6.

### 16. Áp dụng P1-P3 vào dữ liệu giả lập và giải thích `covers`

- **Thời gian:** 20:47-21:07.
- **Công cụ:** Claude Opus 5.5 qua Pi. Không dùng tìm kiếm web.
- **Prompt (nguyên văn):** "Yeah fix P1 to P3. For decision 2 I think covers are good but I think I need to understand more about how it will change the pipeline. For p8 note, add it as a limitation." (20:47)
  Ý chính: sửa P1-P3; với `covers`, cần hiểu thêm nó thay đổi luồng xử lý thế nào; P8 ghi là giới hạn.
- **Đầu ra:**
  - `decisions.md`: các dòng M9-M13.
  - `artifacts.md`: thêm cột `series`, bỏ cột `replaces`, bỏ `effective_to` của GameCo v2, `overrides` trỏ vào `LEAVE-GROUP`; lần vết của Minh viết lại theo 5 bước (kết quả vẫn là 14 ngày từ `LEAVE-GAMECO-v2`).
  - `phase2_prompt.md`: cập nhật mô hình lõi, bảng trường dữ liệu và danh sách tự kiểm tra.
  - `checks/adopted_rules.py`: chạy bộ luật đã chấp nhận trên đúng bảng dữ liệu mới.
  - `production_review.md`: mục "How `covers` changes the pipeline" (từng bước thay đổi, lần vết của Minh với `covers`, rủi ro mới, chi phí ước tính).
  - `playbook.md`: 4 ý tưởng hoãn lại (thông báo khi tài liệu cấp trên đổi phiên bản, cờ "bắt buộc", cảnh báo trước ngày hết hiệu lực, bộ chọn "Hỏi cho").
- **Quyết định của tôi:** quyết định về `covers` ở mục 17 (bỏ).
- **Xác minh:**
  - **[AI]** `adopted_rules.py` cho kết quả đúng với 3 persona ở ngày 07/10/2026 và với các thay đổi từng làm hỏng bộ luật cũ (v3 có hiệu lực, v3 bị hoãn, Tập đoàn ra bản mới).
  - **[AI]** Claude tự sửa 2 đề xuất của chính nó trong quá trình làm: bỏ trạng thái `withdrawn` (trùng với `effective_to`) và sửa nhận định "gắn khóa cho cả văn bản là đủ cho MVP" (cần gắn theo từng Điều).
  - Lần vết của Minh: xem mục 14.

### 17. Thảo luận luật mâu thuẫn và quy trình thực tế trong sản phẩm

- **Thời gian:** 21:07-21:37.
- **Công cụ:**
  - Claude Opus 5.5 qua Pi: thảo luận, script thử nghiệm quan hệ `complements` (ngoài repo, chưa áp dụng).
  - Agnes 2.5 Flash (mức suy luận tối đa), qua 2 lượt subagent: tìm quy trình thực tế (Guru, Glean, Microsoft, Confluence, ServiceNow, KCS, NAVEX), sau đó lượt thứ hai mở từng trang và so trích dẫn với nguyên văn.
- **Prompt (nguyên văn):**
  - "I want to discuss the rules relating to every conflict rule. Do we really need topic or covers and can we safely remove the refusal and conflict step?" (21:07)
  - "Using covers is not that flexible. If there's a document without a structure, then it would be very bad and we have to label every chunk. I have to label the covers for each chunk. If we use the covers also and there's a case in the conflicting scenarios, there's a case where we retrieve two documents. They are both related to the same topic, like nghỉ phép, but they include different information about that. I think that is a valid scenario." (21:13)
  - "In real production applications what are the best processes that people often use?" (21:19)
  - Ý chính: có thật sự cần `topic` hoặc `covers`, có bỏ được bước mâu thuẫn và từ chối không; `covers` không linh hoạt vì phải gắn nhãn từng đoạn; hai tài liệu cùng chủ đề nhưng nội dung khác nhau là tình huống hợp lệ; sản phẩm thật dùng quy trình nào.
- **Đầu ra:**
  - Trong hội thoại: giữ bước mâu thuẫn và từ chối (chúng là 3 kết quả của một bộ phân giải); đề xuất bỏ `covers`, giữ `topic` theo tài liệu, thêm quan hệ `complements` khai báo một lần cho mỗi cặp chuỗi tài liệu.
  - `production_review.md`: mục "How real products keep knowledge consistent" với 7 quy trình và nguồn S11-S19.
- **Phần tôi tự làm:** tôi phản biện `covers` (phải gắn nhãn từng đoạn, không dùng được cho tài liệu không có cấu trúc) và nêu tình huống hai tài liệu cùng chủ đề có nội dung khác nhau là hợp lệ.
  Quan hệ `complements` là đề xuất của Claude, lần đầu xuất hiện trong ghi chép Round 3 do Claude viết (mục 3); tôi chấp nhận.
- **Quyết định của tôi:** bỏ `covers`, giữ một `topic` cho mỗi tài liệu, thêm quan hệ `complements`, kiểm tra cặp chưa khai báo lúc đăng tài liệu bằng script, thêm bẫy T11 (ghi thành M14, M15; xem mục 18).
- **Xác minh:**
  - **[AI]** Lượt kiểm tra thứ hai của Agnes loại 2 trích dẫn không có trên trang (Microsoft Copilot, Azure AI Search) và đánh dấu nguồn ServiceNow là yếu vì không tải được trang gốc.
  - **[Không dùng]** Nguồn S11-S19: bài nộp không dẫn nguồn web.

### 18. Áp dụng `complements`, kiểm tra lúc đăng tài liệu và bẫy T11

- **Thời gian:** 21:37-21:56.
- **Công cụ:** Claude Opus 5.5 qua Pi; phần cuối (đổi `complements` thành danh sách, chạy lại script, ghi M16-M17) do Claude Sonnet 5.5. Không dùng tìm kiếm web.
- **Prompt (nguyên văn):**
  - "approve but then should we keep the conflicts check now that it is governed by outside the answer" (21:37)
  - "continue" (21:45)
  - "record the decisoins keep the conflict and make complements a list" (21:56)
  - Ý chính: đồng ý, nhưng có nên giữ bước kiểm tra mâu thuẫn lúc hỏi khi việc này đã được quản lý bên ngoài câu trả lời; ghi quyết định, giữ bước kiểm tra, đổi `complements` thành danh sách.
- **Đầu ra:**
  - `decisions.md`: M14 (`complements`, bỏ `covers`), M15 (kiểm tra cặp chưa khai báo lúc đăng tài liệu), M16, M17.
  - `artifacts.md`: cột `complements`, tài liệu `LEAVE-PROC-GAMECO-v1` (viết dạng các bước, không có "Điều"), bẫy T11, lần vết của Minh cập nhật (trả lời từ GameCo v2 và hướng dẫn, vẫn 14 ngày).
  - `checks/adopted_rules.py`: thêm `complements` và hàm kiểm tra lúc đăng tài liệu, chạy cho mọi đơn vị, hôm nay và mọi ngày phiên bản hiện hành thay đổi trong tương lai.
  - Cập nhật `phase2_prompt.md`, `production_review.md` (Câu 3 viết lại thành 4 trường hợp), `open_issues.md`, Deferred ideas trong `playbook.md`.
- **Phát hiện khi chạy script:**
  - Bản đầu của kiểm tra lúc đăng tài liệu bỏ sót ngày hết hiệu lực (`effective_to`); Claude sửa và chạy lại, giờ nó báo trước 9 tháng khi GameCo bãi bỏ quy chế.
  - Script thử (ngoài repo) cho thấy khi tái cơ cấu tổ chức (Studio chuyển từ GameCo sang PayCo), cặp chưa khai báo xuất hiện mà không có tài liệu nào được đăng, nên kiểm tra lúc đăng tài liệu không chạy.
  - `complements` khai báo theo từng cặp: tài liệu thứ ba cùng chủ đề cần khai báo với từng tài liệu còn lại.
- **Quyết định của tôi:** giữ bước kiểm tra mâu thuẫn lúc hỏi (M16, vì kiểm tra lúc đăng tài liệu chỉ báo cáo, và có cặp xuất hiện khi không có tài liệu nào được đăng); đổi `complements` thành danh sách (M17).
- **Xác minh:**
  - **[AI]** `adopted_rules.py` cho đúng kết quả với 3 persona, các kịch bản phiên bản và T11 (khai báo thì trả lời, không khai báo thì báo mâu thuẫn); script thử cho thấy tài liệu thứ ba cần khai báo cả hai chuỗi mới hết mâu thuẫn.
  - Lần vết của Minh: xem mục 14.

### 19. Rà soát tiến độ, rút gọn Phase 2 và bỏ bước chọn chủ đề cho câu hỏi

- **Thời gian:** 23:22-23:51.
- **Công cụ:** Claude Opus 5.5 qua Pi. Không dùng tìm kiếm web.
- **Prompt (nguyên văn):**
  - "summarize what have we did, what is our current state, should we clean up and organize the project, update the readme now, do we drifted with our goal" (23:22)
  - "simplify phase two some later steps does not needed for writing the submission file open isse 2 also" (23:27)
  - "1 approve 2, why the model need to choose topic in the first place. I am thinking of the retriever gives the chunks and return it to the model to generate a response." (23:31)
  - "explain - Origin: "Hiep (AI refined the conflict trigger)". I approve the remaining next" (23:38)
  - "yes do that now. and explain to me how the conflicts are handled now" (23:45)
  - "tell me about series and complements and gives me examples" (23:51)
  - Ý chính: tóm tắt tiến độ và kiểm tra có đi lệch mục tiêu không; rút gọn Phase 2; hỏi vì sao mô hình phải chọn chủ đề khi retriever có thể trả chunk cho mô hình trả lời; hỏi lại nhãn nguồn gốc của một quyết định; nhờ giải thích cách xử lý mâu thuẫn, `series` và `complements`.
- **Đầu ra:**
  - Trong hội thoại: nhận định "đúng hướng nhưng đào quá sâu": nhiều giờ dành cho M9-M17 trong khi phần 1 (40% điểm) chưa viết; đề xuất chốt mô hình lõi.
  - Claude đề xuất 3 cách chọn chủ đề cho câu hỏi và khuyến nghị để LLM phân loại; tôi không chọn cách nào mà đặt câu hỏi vì sao cần chọn chủ đề.
  - `decisions.md`: A1 (phạm vi Phase 2), V3 (không chạy thử nghiệm embedding), M18 (dựng bộ luật của người hỏi trước, rồi truy xuất; kết quả do luật quyết theo tài liệu được trích dẫn).
  - `checks/adopted_rules.py`: tách thành `rulebook()` (bước 1-4, không đọc câu hỏi) và `answer()` (bước 7, kiểm tra sau theo trích dẫn); thêm 3 kịch bản kiểm tra sau.
  - Cập nhật `artifacts.md` (thứ tự 7 bước, lần vết của Minh bước D-E), `phase2_prompt.md`, `redraft_plan.md`, `open_issues.md` (đóng Issue 2), Deferred ideas trong `playbook.md`.
  - 2 commit: toàn bộ việc Phase 2 (M9-M18); cập nhật README và `AGENTS.md`.
- **Phần tôi tự làm:** ý tưởng không chọn chủ đề cho câu hỏi, để retriever trả chunk cho mô hình trả lời; quyết định rút gọn Phase 2.
- **Phần AI đề xuất và tôi chấp nhận:** chọn bước nào của Phase 2 để bỏ; đánh dấu cặp mâu thuẫn theo chủ đề trước khi truy xuất (bước 4); kích hoạt thẻ mâu thuẫn theo tài liệu được **trích dẫn** chứ không theo tài liệu được truy xuất (bước 7), và bỏ trích dẫn nằm ngoài bộ luật.
- **Xác minh:**
  - **[AI]** `adopted_rules.py` cho kết quả như cũ với 3 persona và các kịch bản phiên bản; 3 kịch bản mới đúng: Hà chỉ trích quy chế Tập đoàn vẫn ra mâu thuẫn, Hà hỏi về làm thêm giờ ra từ chối (không phải mâu thuẫn giả), trích dẫn bản đã bị thay thế ra từ chối.
  - Giới hạn: script giả lập bước 5-6 (retriever và LLM) bằng một hàm thay thế, nên chưa kiểm tra được LLM thật có trích dẫn đúng hay không; việc này để Mission 2.
  - Lần vết của Minh: xem mục 14.

### 20. Best practice cho nhật ký và đối chiếu nhật ký với lịch sử phiên

- **Thời gian:** từ 23:28.
- **Công cụ:** Claude Opus 5.5 qua Pi, có tìm kiếm web.
- **Prompt (nguyên văn):**
  - "I want to find the best practices about writing an AI logging, up to now I only dump the raw AI usage log in to the file without supervision. Tell me what can I do so I can prepare the best submission for it. What should I polish and refine. Discuss this with me" (23:28)
  - "1. keep AI version 2/ the judges should not see the repo now, I think it should be a pdf file. 3. I use WisprFlow and Orca CLI for my workflow only and I use PI Harness that use models from Claude subscriptions 4. ok"
  - Ý chính: tìm best practice viết nhật ký dùng AI và những gì cần hoàn thiện; sau đó trả lời 4 câu hỏi của Claude.
- **Đầu ra:**
  - Trong hội thoại: tiêu chí giám khảo dùng nhật ký (đủ, có xác minh, làm chủ được), đối chiếu với 3 khung công bố: AID Framework (Weaver, 2024), IBM AI Attribution Toolkit, AI Usage Cards (Wahle và cộng sự, JCDL 2023); đề xuất nhật ký 2 lớp (1 trang tóm tắt cho giám khảo và các mục chi tiết).
  - `tools/ai_sessions.py`: liệt kê mọi phiên Pi của dự án (thời gian, mô hình, prompt, file đã sửa) và in nguyên văn prompt của một phiên.
  - Nhật ký này: thêm phần cách lập nhật ký, nhãn kiểm chứng, bảng công cụ, các phiên phụ, mục 14, prompt nguyên văn và thời gian cho mọi mục; đổi nhãn kiểm chứng theo người thực sự kiểm tra.
  - Sửa 3 khẳng định sai: mục 13 (tôi tự lần vết), mục 15 ("lần vết tay" của Minh, thực ra do AI viết), mục 17 và dòng M14 trong `decisions.md` (`complements` là ý tưởng của tôi, thực ra là đề xuất của Claude).
- **Quyết định của tôi:** giữ bản lần vết do AI viết và khai báo trung thực; nhật ký nộp dạng PDF vì giám khảo không xem repo; khai báo Wispr Flow, Orca CLI và Pi; trích prompt nguyên văn tiếng Anh kèm ý chính tiếng Việt.
- **Xác minh:**
  - **[AI]** Script đọc trực tiếp file lưu phiên của Pi; mô hình của từng phiên lấy từ trường `model` trong file, không từ trí nhớ của AI.
  - **[AI]** Claude mở trực tiếp trang của 3 khung tham khảo (trang hướng dẫn AID Framework của University of Waterloo, blog IBM Research, tóm tắt trên arXiv) trước khi dẫn.
  - **[Chưa]** Tôi đọc lại toàn bộ nhật ký đã sửa và xác nhận phần đề bài trong `docs/competition/` do tôi tự sao chép từ portal.

### 21. Phase 3 - Chọn lại 3 quyết định cho phần 4

- **Thời gian:** 00:00-00:15, ngày 08/10.
- **Công cụ:** Claude Opus 5.5 qua Pi. Không dùng tìm kiếm web.
- **Prompt (nguyên văn):**
  - "start phase 3 of C:/Users/Hiep/orca/projects/next-gen/docs/mission1/redraft_plan.md. I want you to read the updated document first and decide whether should we still choose these 3 decisions"
  - "approve"
  - Ý chính: bắt đầu Phase 3; đọc lại các quyết định đã cập nhật và đánh giá 3 quyết định tạm chọn ở F4 (P, R, S) có còn đúng không.
- **Đầu ra:**
  - Trong hội thoại: Claude đề xuất giữ P, định nghĩa lại S thành quyết định M18, bỏ R (sau M18 không còn trạng thái "không chắc"; nửa về mâu thuẫn chính là M1b nằm trong P, nửa về từ chối không có phương án B mạnh), thay bằng L (nhân sự hỏi trực tiếp hay HR dùng trước).
  - `decisions.md`: F4r (3 quyết định mới), B1 (nút "Báo sai"), danh sách giả định mỗi dòng một câu.
  - `artifacts.md`: thêm nút "[Báo sai]" vào thẻ trả lời; `redraft_plan.md`: ghi kết quả Phase 3.
  - 1 commit riêng cho phần còn lại của Phase 2 (A1-A9, thẻ kết quả, đối chiếu nhật ký) trước khi sửa.
- **Quyết định của tôi:** chấp nhận toàn bộ đề xuất.
- **Xác minh:**
  - **[Duyệt]** Tôi đọc lập luận và đồng ý; không có dữ kiện bên ngoài cần kiểm chứng.
  - Giới hạn đã ghi trong F4r: Mission 2 chỉ kiểm tra được điều kiện tiên quyết của L, tín hiệu thật (tỷ lệ "Báo sai") cần thí điểm.

### 22. Phase 3 - Bản nháp lập luận A-vs-B cho P, S, L

- **Thời gian:** sau mục 21, cùng phiên, ngày 08/10.
- **Công cụ:** Claude Opus 5.5 qua Pi. Không dùng tìm kiếm web.
- **Prompt (nguyên văn):** "you need to do this for me and I will revise it"
  Ý chính: nhờ Claude viết nháp 3 bảng lập luận của Phase 3 thay vì tôi tự điền mẫu trống; tôi sẽ sửa lại.
- **Đầu ra:** `docs/mission1/redraft/phase3_decisions.md`, bản nháp tiếng Việt cho P, S, L theo 7 trường (A, B, B làm tốt hơn, tiêu chí, cái giá, B thắng khi, kiểm thử), mỗi quyết định kèm "Điểm giám khảo sẽ hỏi"; dòng A10 trong `decisions.md` ghi việc giao cho AI viết nháp.
- **Quyết định của tôi:** giao viết nháp; nội dung chưa sửa.
- **Xác minh:**
  - **[AI]** Các kết quả trích từ `adopted_rules.py` (Minh 14 ngày, Hà ra thẻ mâu thuẫn, Hà hỏi về làm thêm giờ ra từ chối, các kịch bản phiên bản) được Claude chạy lại script trong phiên này trước khi viết.
  - **[Không dùng]** Bản nháp này được đưa vào Phần 4 và tôi review ở các mục 30, 31, 34.
  - Ví dụ câu hỏi chạm hai chủ đề còn trong Phần 4 dưới dạng suy luận, chưa đo (Phần A6).

### 23. Phase 4 - Bản nháp kiểm chứng và MVP

- **Thời gian:** 00:11-00:20 và 07:48-07:55, ngày 08/10 (phiên bị ngắt giữa chừng, tiếp tục bằng "continue").
- **Công cụ:** Claude Opus 5.5 qua Pi. Không dùng tìm kiếm web.
- **Prompt (nguyên văn):**
  - "implement Phase 4 - Validation and MVP (1 h) in C:/Users/Hiep/orca/projects/next-gen/docs/mission1/redraft_plan.md"
  - "continue"
  - Ý chính: thực hiện Phase 4 của kế hoạch viết lại: chỉ số, giả định rủi ro nhất, kế hoạch 3 ngày, baseline và bảng test.
- **Đầu ra:**
  - `decisions.md`: các dòng V1, V2, V4-V7, đều ghi "AI proposal, pending Hiep".
  - `artifacts.md`: bảng test 10 dòng (persona, câu hỏi, ngày, hành vi mong đợi, văn bản phải trích, văn bản cấm trích chia hai cột "luật" và "LLM"), bảng chỉ số, kế hoạch 3 ngày, danh sách chưa làm; thêm Điều 3 vào `OT-GAMECO-v1` (V6) và ghi chú dòng mới cho thẻ từ chối (V7).
  - `checks/adopted_rules.py`: hàm `run_matrix` chạy phần tất định của 10 dòng.
  - `playbook.md`: 3 ý tưởng hoãn (thông báo email/chat cho chủ sở hữu, LLM chấm độ trung thành, mục tiêu độ trễ).
  - Phát hiện của Claude khi chạy bảng test: ở các dòng 6, 8, 9, 10, văn bản không được trích vẫn nằm trong bộ luật của người hỏi, nên luật không chặn được; đây là cơ sở cho đề xuất V2.
- **Quyết định của tôi:** duyệt ở mục 25.
- **Xác minh:**
  - **[AI]** Claude chạy `adopted_rules.py`: 10/10 dòng đạt; khi bỏ `overrides` khỏi `LEAVE-GAMECO-v2` hoặc ban hành bản nháp v4, 3/10 dòng trượt (chạy một lần trong phiên, không lưu vào script).
  - **[Không dùng]** Cận trên 9,5% cho "0 lỗi trên 30 ca" (công thức 1 - 0,05^(1/30), Claude tính bằng Python): đã bỏ khỏi bài nộp ở mục 31.
  - **[Không dùng]** Bảng test 10 dòng không còn trong bài nộp (mục 31); bài nộp chỉ nêu năm tình huống test bằng lời.

### 24. Phase 5 - Bản nháp tài liệu 5 trang

- **Thời gian:** 08:00-08:30, ngày 08/10.
- **Công cụ:** Claude Opus 5.5 qua Pi. Không dùng tìm kiếm web.
- **Prompt (nguyên văn):**
  - "start phase 5 in C:/Users/Hiep/orca/projects/next-gen/docs/mission1/redraft_plan.md"
  - "remember to not to use our internal notations for this project"
  - Ý chính: bắt đầu Phase 5 (viết 5 phần của tài liệu); không dùng ký hiệu nội bộ của dự án trong bài.
- **Đầu ra:**
  - `docs/mission1/document.md`: Claude viết lại toàn bộ 5 phần và đoạn mở đầu theo thứ tự của kế hoạch, từ `decisions.md`, `artifacts.md` và `phase3_decisions.md`; không còn mã quyết định, mã bẫy hay mã văn bản, văn bản được gọi bằng tên, quan hệ được gọi bằng tiếng Việt kèm tên trường tiếng Anh một lần.
  - Bản đầu dài 8 trang; Claude cắt còn 5 trang bằng cách bỏ sơ đồ luồng (hiển thị quá nhỏ, không đọc được), bỏ bảng persona, đưa ba thẻ kết quả vào một bảng, rút gọn các phần 3-5.
  - `decisions.md`: dòng A11 (giao viết nháp) và ghi chú những gì bị cắt, những dòng còn chờ duyệt mà bản nháp phụ thuộc.
  - `phase3_decisions.md`: sửa một khẳng định quá mức ở phần S (xem Xác minh).
- **Quyết định của tôi:** giao viết nháp (A11, cần tôi xác nhận); nội dung chưa sửa.
- **Xác minh:**
  - **[AI]** Claude render PDF bằng `tools/render_pdf.py` (5 trang), xem ảnh từng trang, và tìm bằng `grep` để chắc không còn dấu gạch dài và ký hiệu nội bộ.
  - **[AI]** Mọi con số và kết quả trong bài (14, 15, 12 ngày; thẻ mâu thuẫn của Hà; các câu từ chối; 10/10 dòng phần luật; cận trên 9,5%) lấy từ `artifacts.md` và kết quả chạy `adopted_rules.py` trong phiên này.
  - **[AI]** Khi đọc lại, Claude phát hiện và sửa hai khẳng định quá mức: câu từ chối cho câu hỏi làm thêm giờ của Hà vẫn phụ thuộc LLM, không do luật bảo đảm; và việc LLM trích văn bản không liên quan không phải "con đường duy nhất" tới câu trả lời sai, vì còn lỗi diễn đạt sai nội dung.
  - **[Tôi]** Tôi review bản nháp qua 4 đợt ghi chú (mục 26, 28, 31, 32) và mục 34; V1-V7 được duyệt ở mục 25; câu chữ vẫn do Claude viết.
  - **[Chưa]** Xác nhận câu chữ của ba thẻ kết quả (A8) và việc giao Claude viết nháp (A11), hai dòng còn ghi "chờ tôi xác nhận" trong sổ quyết định.

### 25. Phase 4 - Duyệt bộ test, chỉ số và kế hoạch 3 ngày

- **Thời gian:** 09:38-11:44, ngày 08/10.
- **Công cụ:** Claude Opus 5.5 qua Pi.
- **Prompt (nguyên văn):**
  - "how can I check and approve the result of phase 3 and 4 in the @docs/mission1/redraft_plan.md" (09:38)
  - "tell me the result of phase 4 I want to confirm and approve it"
  - "I think that's good so I approve them but I wonder why there are no metrics relating to RAG performance in this."
  - Ý chính: hỏi cách kiểm và duyệt kết quả Phase 3 và 4; xem tóm tắt Phase 4 để duyệt; duyệt và hỏi vì sao chưa có chỉ số về hiệu năng RAG.
- **Đầu ra:** Claude tóm tắt kết quả Phase 4 (bộ test 10 dòng, chỉ số, giả định rủi ro nhất, kế hoạch 3 ngày, so sánh với chatbot thường, điều 3 thêm vào quy chế làm thêm giờ, câu thêm trên thẻ từ chối), mỗi mục kèm phản biện mạnh nhất; sau khi tôi duyệt, Claude ghi "accepted by Hiep 08/10" vào `decisions.md`, `artifacts.md` và `redraft_plan.md`.
- **Quyết định của tôi:** chấp nhận V1, V2, V4, V5, V6, V7 và bộ test như đề xuất.
- **Xác minh:**
  - **[AI]** Claude chạy lại `adopted_rules.py` trước khi tóm tắt: 10/10 dòng phần luật đạt.
  - **[Tôi]** Đọc bản tóm tắt và các phản biện, duyệt từng mục.

### 26. Phase 5 - Review bằng Lavish và bản nháp thứ hai

- **Thời gian:** 11:48-12:37, ngày 08/10.
- **Công cụ:** Claude Opus 5.5 qua Pi; Lavish (`lavish-axi`, chạy cục bộ) chỉ để tôi ghi chú trực tiếp lên tài liệu, không sinh nội dung.
- **Prompt (nguyên văn):**
  - "Yes commit. I want to check this. Should I do the AI judge on the current PDF file first or will I review it and after that send it to the judge? I have some ideas in my mind now."
  - "I want to inspect each element and write down my notes there. Should I use the lavish skill?"
  - "Yes do that setup."
  - "I wonder whether we should keep or remove 6-row test excerpt. And also is Markdown a good choice for the submission? I think that your cut-down list is good.  you do the draft for me I will revise it."
- **Đầu ra:**
  - Claude tách phần việc chưa commit thành 3 commit theo phase (3, 4, 5).
  - Claude viết `tools/render_review.py` để mở tài liệu trong Lavish với cùng font, độ rộng và vị trí ngắt trang như PDF.
  - Tôi ghi 10 ghi chú; Claude chép nguyên văn vào `docs/mission1/redraft/review_notes.md`.
  - Claude viết lại toàn bộ `document.md` theo các ghi chú: văn xuôi thay cho gạch đầu dòng, thuật ngữ RAG, sơ đồ luồng 7 bước, phần 4 viết theo "chọn X thay vì Y", phần 5 trả lời "phần nào làm trước"; bỏ `nl2br` trong `tools/render_pdf.py` để các câu chảy thành đoạn văn.
- **Quyết định của tôi:** review trước rồi mới chạy AI judge; giữ bảng test rút gọn; nộp PDF dựng từ Markdown; đồng ý danh sách cắt; giao Claude viết bản nháp thứ hai, tôi sửa sau.
- **Xác minh:**
  - **[Tôi]** Review bản nháp đầu, ghi 10 ghi chú (`review_notes.md`).
  - **[AI]** Claude render lại (5 trang), xem ảnh từng trang, kiểm tra không còn dấu gạch dài và ký hiệu nội bộ; các con số không đổi so với bản đầu.
  - **[Tôi]** Tôi review bản nháp thứ hai qua các đợt ghi chú ở mục 28, 31, 32 và mục 34; câu chữ vẫn do Claude viết.

### 27. Phase 5 - Prompt review "người đọc mới"

- **Thời gian:** 12:37, phần bổ sung lúc 12:45, ngày 08/10.
- **Công cụ:** Claude Opus 5.5 qua Pi.
- **Prompt (nguyên văn):** "I want you to craft the review prompts for a reviewer AI agent. I want it to act as a new reader who reads this. I want it to find out: - what is controversial - what are the conflicts - what is very hard to understand - what can be changed so it's more readable and more understandable It should check whether this document matches the competition's brief and requirements also. Besides that you need to tell me to add more things to the prompts so it checks the things besides what I recommend."
- **Đầu ra:** `docs/mission1/review_prompt_reader.md`: prompt 6 phần (đọc lần đầu, khó hiểu, gây tranh cãi và mâu thuẫn, đối chiếu đề bài, cách sửa cho dễ đọc, tóm tắt) và 5 module tùy chọn do Claude đề xuất thêm (nguồn của con số, quyết định có phải lựa chọn thật, khả năng xây dựng, câu hỏi khi pitch, trình bày trang).
- **Bổ sung sau (theo yêu cầu của tôi):** thêm mục "Needs more explanation" vào phần 2 của prompt: tìm chỗ nêu kết luận mà thiếu lý do, thiếu ví dụ hoặc nhảy bước.
- **Quyết định của tôi:** 4 yêu cầu chính và việc đối chiếu đề bài là của tôi; các module tùy chọn là đề xuất của AI, tôi chọn module nào khi chạy.
- **Xác minh:**
  - Prompt được chạy trên Claude ở mục 29.
  - Giới hạn: không chạy lại trên mô hình khác họ (Phần A6).

### 28. Phase 5 - Ghi chú review đợt 2 và chỉnh sửa

- **Thời gian:** 12:39-12:42, ngày 08/10 (lần gửi nhầm lúc 12:38 ở mục "Phiên AI không định hình nội dung bài nộp").
- **Công cụ:** Claude Opus 5.5 qua Pi.
- **Prompt (nguyên văn):** 6 ghi chú của tôi trên Lavish (chép nguyên văn trong `docs/mission1/redraft/review_notes.md`, đợt 2), rồi "Write them down." và "Apply the recommendations."
- **Đầu ra:** Claude trả lời 4 câu hỏi trong ghi chú bằng đề xuất, rồi sửa `document.md`: bỏ câu "Đây là dự đoán..."; gọi người hỏi theo vị trí thay vì tên; đổi "bộ quy định" thành "phạm vi tìm kiếm"; nói rõ chiều của quan hệ "dùng thay" và việc hệ thống không tự cho đơn vị cấp dưới thắng; tách dòng chủ đề và chủ sở hữu.
- **Quyết định của tôi:** 6 ghi chú là của tôi; tôi chấp nhận cả 6 đề xuất của Claude.
- **Xác minh:**
  - **[AI]** Claude render lại (5 trang), xem ảnh trang 2 và 5, kiểm tra không còn tên riêng, "bộ quy định" hay dấu gạch dài.
  - **[Tôi]** Tôi đọc lại bản đã sửa trong đợt review 3 (mục 31).

### 29. Phase 5 - Chạy prompt review "người đọc mới" (cùng họ mô hình)

- **Thời gian:** 12:47-13:07, ngày 08/10.
- **Công cụ:** Claude Code (CLI), mô hình Claude Opus 5.5, từ 12:57.
  Lần chạy đầu trên Pi (12:47-12:56) bị ngắt: Pi tự khởi chạy subagent với `gpt-5.5`, `gpt-6-sol`, `gpt-6.1-sol` (OpenAI Codex), `claude-fable-5-1` và `claude-opus-5-5`.
  Tôi yêu cầu "Only use Claude models in this section.", hỏi "what are you doing and why you use subagent", rồi dừng phiên.
  Theo file lưu phiên, không subagent nào trả về nội dung và phiên không đổi file nào; tôi chạy lại prompt trong Claude Code.
- **Prompt (nguyên văn):** "C:/Users/Hiep/orca/projects/next-gen/docs/mission1/review_prompt_reader.md do this"
  Ý chính: chạy prompt review trong `review_prompt_reader.md` trên bản PDF hiện tại.
- **Đầu ra:** `docs/mission1/redraft/review_reader_output.md`: đủ 6 phần và cả 5 module tùy chọn A-E.
  5 vấn đề lớn nhất: luật phạm vi từ chối câu hỏi về đơn vị khác dù người hỏi được xem văn bản; quyết định 3 dựa vào nút "Báo sai" trong khi Phần 1 nói câu trả lời sai trông giống câu đúng; cơ chế phát hiện cặp mâu thuẫn chưa được nói rõ; quyết định 1 chưa phản biện phương án "đơn vị cấp dưới thắng"; Phần 5 chưa đo kết quả người dùng nêu ở Phần 1.
- **Giới hạn:** cùng họ mô hình với bản nháp; phiên đã nạp `AGENTS.md` nên không đọc "lạnh" hoàn toàn; đề bài và quy định được đọc cùng lúc với tài liệu, trước khi viết Phần 1-3, trái với hướng dẫn trong prompt.
- **Quyết định của tôi:** xem mục 30.
- **Xác minh:**
  - **[AI]** Claude render PDF (5 trang), xem ảnh từng trang, trích nguyên văn từ `document.md`, kiểm tra không có dấu gạch dài trong file kết quả.
  - **[Tôi]** Đọc bản tóm tắt kết quả và chọn mục cần sửa (mục 30).
  - Giới hạn: không chạy lại trên mô hình khác họ (Phần A6).

### 30. Phase 5 - Quyết định và chỉnh sửa sau review "người đọc mới"

- **Thời gian:** 13:25-14:04, ngày 08/10.
- **Công cụ:** Claude Opus 5.5 qua Pi.
- **Prompt (nguyên văn):**
  - "tell me the findings of C:/Users/Hiep/orca/projects/next-gen/docs/mission1/redraft/review_reader_output.md"
  - "are there any conflicts or decisions that need me now"
  - "approve the recommendations. my name is Phạm Bách Hiệp. do not show the scripts. I think the diacritics parts should be remove now and the retriever may include hybrid search"
- **Đầu ra:**
  - Claude tóm tắt kết quả review, rồi đối chiếu từng phát hiện với `decisions.md`: phần đã có quyết định chỉ cần sửa câu chữ; 6 điểm cần tôi quyết, mỗi điểm kèm đề xuất.
  - Ghi các quyết định RV1-RV7 vào `decisions.md`.
  - Sửa `document.md`: nói rõ phiên bản đầu chỉ trả lời quy định áp dụng cho người hỏi; nêu luật tìm cặp mâu thuẫn; quyết định 1 phản biện "đơn vị cấp dưới thắng"; quyết định 3 so với phương án HR dùng trước vài tuần; thẻ mâu thuẫn trích nguyên văn; bước 7 từ chối cả câu trả lời khi có trích dẫn bịa; thí điểm sau Mission 2 đo kết quả người dùng; retriever hybrid search; bỏ phần "không dấu"; điền tên ứng viên; các chỗ sửa câu chữ khác liệt kê trong `decisions.md`.
  - Sửa `adopted_rules.py` theo RV5 và `artifacts.md` theo RV4, RV5, RV7.
  - `tools/render_pdf.py`: giữ tiêu đề và câu dẫn cùng trang với danh sách hoặc bảng theo sau.
- **Quyết định của tôi:** chấp nhận các đề xuất của Claude; không công bố script cho giám khảo; bỏ phần "không dấu" và dùng hybrid search cho retriever (thay cho đề xuất tìm theo từ khóa sau khi bỏ dấu của Claude).
  Hai chi tiết do Claude tự chọn khi áp dụng: cách hỏi thứ ba "văn nói" thay cho "không dấu", và quy mô thí điểm "một công ty, 4 tuần".
- **Xác minh:**
  - **[AI]** Chạy lại `adopted_rules.py`: 10/10 dòng phần luật đạt; so với bản trước, đầu ra chỉ thêm một ca mới (một trích dẫn hợp lệ kèm một trích dẫn bịa thì từ chối).
  - **[AI]** Render PDF đúng 5 trang, xem ảnh từng trang; câu trích trên thẻ mâu thuẫn khớp nguyên văn Điều 1 của hai văn bản giả lập trong `artifacts.md`; không còn dấu gạch dài.
  - **[Tôi]** Tôi đọc lại bản đã sửa trong đợt review 3, đổi Phần 4 thành bảng (mục 31) và xem lại quyết định 2 (mục 34).
  - Giới hạn: không chạy lại trên mô hình khác họ (Phần A6).

### 31. Phase 5 - Ghi chú review đợt 3 và chỉnh sửa

- **Thời gian:** 14:04-15:18, ngày 08/10.
- **Công cụ:** Claude Opus 5.5 qua Pi; Lavish (`lavish-axi`, chạy cục bộ) chỉ để tôi ghi chú lên tài liệu.
- **Prompt (nguyên văn):**
  - "open it in lavish"
  - 18 ghi chú của tôi trên Lavish (chép nguyên văn trong `docs/mission1/redraft/review_notes.md`, đợt 3).
  - "3. remove item 4 and remove anything that mention comparing with naive-RAG. 6. check the other number so we not too confident also ensure the Chỉ số column is easy to understand what we measure. and for the remaininig options choose your recommendations"
- **Đầu ra:**
  - Claude chép ghi chú, trả lời các câu hỏi (thẻ mâu thuẫn khi chủ sở hữu quên khai báo "bổ sung", Markdown hay DOCX/PDF, ngưỡng 100% có quá tự tin không, Phần 4 dạng bảng) kèm đề xuất.
  - Ghi các quyết định RV8-RV14 vào `decisions.md`; đưa thí điểm, so sánh với naive RAG và DOCX/PDF vào "Deferred ideas" trong `playbook.md`.
  - Sửa `document.md`: Phần 4 thành một bảng (mỗi cột một quyết định, A và B cạnh nhau); Phần 5 mô tả năm tình huống test thay cho bảng test, bỏ thí điểm và so sánh naive RAG, viết lại bảng chỉ số bằng lời dễ hiểu và mục tiêu ít tự tin hơn; thẻ mâu thuẫn dùng câu trung tính; rút gọn các đoạn dài ở Phần 2 và 3.
  - Sửa `artifacts.md` cho khớp (thẻ mâu thuẫn, ngưỡng 10%, bỏ so sánh naive RAG khỏi kế hoạch 3 ngày); `tools/render_pdf.py` giữ cột nhãn của bảng Phần 4 trên một dòng.
- **Quyết định của tôi:** 18 ghi chú là của tôi; tôi tự quyết việc bỏ so sánh với naive RAG (RV10) và yêu cầu kiểm lại các con số (RV13); phần còn lại tôi chọn theo đề xuất của Claude.
  Bỏ thí điểm (RV9) đảo lại RV3 mà tôi đã duyệt trước đó cùng ngày, vì tài liệu chỉ nêu những gì MVP làm.
- **Xác minh:**
  - **[AI]** Render PDF đúng 5 trang, xem ảnh từng trang; kiểm tra không còn "retrieval", "generation", "kế toán PayCo", "thí điểm", "30 ca", "9,5%" và dấu gạch dài.
  - **[Tôi]** Tôi đọc lại Phần 5 và gửi thêm ghi chú (mục 32), đọc lại quyết định 2 ở Phần 4 (mục 34).

### 32. Phase 5 - Chỉnh sửa đợt 4 trong chat

- **Thời gian:** 15:18-15:28, ngày 08/10.
- **Công cụ:** Claude Opus 5.5 qua Pi.
- **Prompt (nguyên văn):** "consider remove this sentence Dữ liệu đổi, code không đổi: đến 01/01/2027, bản 3 tự trở thành bản hiện hành, remove the fine-tune part we don't need it. in quyeet dinh 2, is there any other alternative option B ? remove this Giả định: trạng thái "dự thảo / đã ban hành" do tôi thêm, đề bài không nêu; mỗi người thuộc một đơn vị; bản tương lai chưa hiển thị vì có thể chưa công bố. also explain why choosing Chỉ theo dõi for context recall which is the current document is limited so measuring brings little meanings. why include this phase Giả định rủi ro nhất: ... and why we only do step 1-4 and 7 but not the full pipeline"
- **Đầu ra:** Claude bỏ ba chỗ tôi yêu cầu, ghi lý do cho dòng context recall, viết lại thứ tự làm để rõ bước 5-6 được thêm ở mục 2; trả lời trong chat về các phương án B khác cho quyết định 2 và vì sao giữ "Giả định rủi ro nhất". Ghi lại trong `decisions.md` (batch 4).
- **Quyết định của tôi:** các chỗ bỏ là của tôi; phương án B của quyết định 2 được chốt ở mục 34.
- **Xác minh:**
  - **[AI]** Render PDF đúng 5 trang, xem ảnh trang 5.

### 33. Phase 6 - Viết lại 3 câu hỏi bắt buộc

- **Thời gian:** 14:56-15:40, ngày 08/10, trong một phiên Pi chạy song song với mục 31-32.
- **Công cụ:** Claude Opus 5.5 qua Pi.
- **Prompt (nguyên văn):** "start phase 6 of C:/Users/Hiep/orca/projects/next-gen/docs/mission1/redraft_plan.md. note that trả lời ngắn gọn, rõ quyết định và lý do khuyến nghị 60-150 từ is a requirements of the answers. Check it this exist first, if not write it down to our document"
- **Đầu ra:**
  - Claude kiểm tra: yêu cầu đã có trong đề bài, `criteria.md`, `AGENTS.md` và danh sách kiểm tra trong `playbook.md`, nhưng chưa có ở Phase 6 của `redraft_plan.md` và trong `answers.md`; Claude ghi thêm vào hai file này và trích nguyên văn yêu cầu vào `AGENTS.md`.
  - Viết lại `answers.md` theo mô hình hiện tại: Câu 1 thêm lý do chọn vấn đề này thay vì rò rỉ và bỏ "loại hợp đồng"; Câu 2 theo kế hoạch 3 ngày và danh sách chưa làm đã duyệt, bỏ "Lark/Slack"; Câu 3 thay "đơn vị cụ thể nhất thắng" bằng phiên bản đang hiệu lực, bộ lọc quyền và phạm vi áp dụng, quan hệ "dùng thay" và "bổ sung" do chủ sở hữu khai báo, cặp chưa khai báo là mâu thuẫn.
  - Ghi quyết định A12 vào `decisions.md`, kèm danh sách phần đã cắt cho vừa số từ.
- **Quyết định của tôi:** không duyệt bản đầu; tôi review và yêu cầu viết lại (xem bên dưới), rồi duyệt bản thứ hai, giữ nguyên câu chữ.
- **Xác minh:**
  - **[AI]** Đếm số từ bằng script Python (tách theo khoảng trắng, chỉ phần trả lời): Câu 1 = 147, Câu 2 = 148, Câu 3 = 145, nằm trong khoảng 60-150.
  - **[AI]** Đối chiếu từng câu với `decisions.md` và `document.md`; kiểm tra không có mã nội bộ hay dấu gạch dài.
  - **[Tôi]** Đọc bản đầu và review: Câu 1 dài vì so sánh với rò rỉ, lý do Câu 2 chưa rõ, Câu 3 dùng thuật ngữ nội bộ.
- **Review của tôi (prompt nguyên văn):** "in q1, the requirements include short and brief answer but you include the reason the the other problem so it may not statisfy that. the reason for q2 is not clear, this part make the answer long  (bản cũ, bản sắp hiệu lực, dự thảo, văn bản mật, cặp mâu thuẫn).in q3 make sure the reader can understand our ideas, do not use our internal terminology for this . my review is applied for all questions so please check again"
- **Đầu ra sau review:** Claude viết lại cả 3 câu: Câu 1 bỏ phần so sánh với rò rỉ; Câu 2 bỏ danh sách bẫy, nói rõ lý do của từng phần và lý do chưa làm, bỏ fine-tune khỏi danh sách vì lý do không khớp; Câu 3 bỏ thuật ngữ nội bộ ("dùng thay", "bổ sung", "chuỗi phiên bản", "metadata"), diễn đạt bằng lời thường.
  Ghi thêm các quy tắc này vào đầu `answers.md` và Phase 6 của `redraft_plan.md`.
- **Xác minh sau review:**
  - **[AI]** Đếm lại bằng script: Câu 1 = 114, Câu 2 = 134, Câu 3 = 130 từ; kiểm tra không còn thuật ngữ nội bộ và dấu gạch dài.
  - **[Duyệt]** Tôi duyệt cả 3 câu của bản thứ hai ngày 08/10 (prompt: "approve the answers").

### 34. Phase 5 - So sánh phương án cho quyết định 2 và sửa cột quyết định 2

- **Thời gian:** 15:28-15:47, ngày 08/10.
- **Công cụ:** Claude Opus 5.5 qua Pi.
- **Prompt (nguyên văn):**
  - "compare the search everthing first and it reverse give examples"
  - "explain the option of LLM choose the topic and give example"
  - "explain the comparision of option A and B in this decision"
  - "is the explanation in the decision table of this case clear, should we improve it"
  - "approve"
- **Đầu ra:** Claude giải thích trong chat, kèm ví dụ trên dữ liệu giả lập (thứ hạng tìm kiếm chỉ là minh họa, chưa đo): tìm trên toàn bộ rồi lọc so với lọc trước rồi tìm; phương án LLM chọn chủ đề; so sánh A và B của quyết định 2. Sau đó Claude chỉ ra 4 chỗ chưa rõ trong cột quyết định 2 và đề xuất câu thay thế; sau khi tôi duyệt, Claude sửa `document.md` và ghi vào `decisions.md` (batch 5).
- **Quyết định của tôi:** giữ phương án B là "LLM chọn chủ đề trước" theo đề xuất; duyệt cách viết lại cột quyết định 2. Các ví dụ so sánh dùng để chuẩn bị pitch, không đưa vào PDF.
- **Xác minh:**
  - **[AI]** Render PDF đúng 5 trang, xem ảnh trang 4 và 5.
  - Chuẩn bị PITCH: tôi tự trình bày lại so sánh A và B của quyết định 2 bằng lời của mình.

### 35. Phase 6 - Prompt review độc lập cho 3 câu trả lời (mô hình khác họ)

- **Thời gian:** 15:51, ngày 08/10.
- **Công cụ:** Claude Opus 5.5 qua Pi.
- **Prompt (nguyên văn):** "now craft me the full prompt so I can send it to another model not from claude so I can check it, remember that I can only send them through their web chat interface (chatgpt, gemini,...) because I have no credit for those models in the coding agent so ensure the prompt include sufficient data so the judge can work properly"
- **Đầu ra:** `docs/mission1/review_prompt_answers.md`: hai tin nhắn để dán vào ChatGPT hoặc Gemini.
  Tin 1 gồm đề bài, quy định chấm điểm và 3 câu trả lời, để giám khảo đọc 3 câu trả lời riêng như khi chấm thật; tin 2 gửi toàn văn tài liệu 5 trang để kiểm tra mâu thuẫn, thiếu sót và hứa quá mức.
  Nội dung được chép nguyên văn từ commit `95346e3` bằng script; prompt không nói ai viết câu trả lời.
- **Quyết định của tôi:** chạy ở mục 36.
- **Xác minh:**
  - **[AI]** Script kiểm tra 3 câu hỏi khớp nguyên văn đề bài và số từ 114 / 134 / 130; dấu gạch dài trong tiêu đề đề bài được đổi thành gạch thường.
  - Prompt được chạy ở mục 36.

### 36. Phase 6 - Kết quả review độc lập 3 câu trả lời (ChatGPT, Gemini)

- **Thời gian:** 19:48-20:13, ngày 08/10.
- **Công cụ:** ChatGPT web (mô hình `gpt-5-6-t-mini`, đọc từ dữ liệu trang chia sẻ) và Gemini web (Gemini 3 Pro, chưa chắc chắn); Claude Opus 5.5 qua Pi tải và tổng hợp kết quả.
- **Prompt (nguyên văn):** hai tin nhắn trong `docs/mission1/review_prompt_answers.md`; sau đó gửi Claude hai đường dẫn chia sẻ: "chatgpt https://chatgpt.com/share/6ac79398-c4d0-83ec-92ad-fb66722c2cbf gemini https://share.gemini.google/82hJ0cK03txm".
- **Đầu ra:** `docs/mission1/redraft/review_answers_output.md`: nguyên văn 4 câu trả lời của hai mô hình.
  Hai mô hình cùng chỉ ra: câu mở đầu Câu 2 ("phần quyết định câu trả lời đúng hay sai") mơ hồ, nghe như hệ thống chấm đáp án; "được xem" ở Câu 1 có thể hiểu là "đang xem trên màn hình".
  ChatGPT thêm: lý do chưa làm ở Câu 2 sai, vì hệ thống nhân sự quyết định đơn vị của người hỏi, nên có ảnh hưởng tới câu trả lời đúng; "mọi ca" và "chắc chắn do AI" nói quá.
  Cả hai giữ nguyên Câu 3 sau khi đọc tài liệu.
- **Quyết định của tôi:** duyệt đề xuất của Claude (prompt: "approve"): sửa Câu 1 ("có quyền xem") và Câu 2 (câu mở đầu, "mọi ca kiểm thử", lý do chưa làm), giữ Câu 3, sửa câu tương ứng ở Phần 5 của tài liệu; ghi quyết định A13.
- **Xác minh:**
  - **[AI]** Claude đối chiếu từng phát hiện với `answers.md` và `document.md`, loại các đề xuất trái với quyết định đã có (dùng "thẻ mâu thuẫn" và "phạm vi tìm kiếm" trong câu trả lời; cho hỏi bản cũ hoặc bản nháp).
  - **[AI]** Đếm số từ bản đề xuất bằng script.
  - **[Duyệt]** Tôi duyệt bản sửa; số từ sau khi sửa: 115 / 146 / 130.

### 37. Phase 7 - Best practice cho nhật ký, trang "thiết kế hiện tại" và hoàn thiện nhật ký

- **Thời gian:** 20:00-21:00, ngày 08/10.
- **Công cụ:** Claude Opus 5.5 qua Pi, có tìm kiếm web.
- **Prompt (nguyên văn):**
  - "I want you to do the research and discuss with me what are the best practices I can do so I can submit the perfect version for the evidence log. Read the document."
  - "should I fix the document system of the project first, it is not in the good shape, the ids are chaos and it's very hard to understand what are decided now"
  - "yes do that"
  - "do the evidence first, what to do now"
  - Ý chính: tìm best practice để hoàn thiện nhật ký nộp bài; hỏi có nên sắp xếp lại hệ thống tài liệu trước vì mã quyết định lộn xộn và khó biết điều gì đang được quyết; đồng ý làm theo đề xuất; làm nhật ký trước và cho biết tôi cần làm gì.
- **Đầu ra:**
  - Trong hội thoại: đối chiếu nhật ký với chính sách AI của cuộc thi và 3 nguồn hướng dẫn (AID Framework của Weaver, 2024; hướng dẫn đánh giá có dùng AI của Charles Sturt University; hướng dẫn khai báo AI cho sinh viên của Saint Louis University); đánh giá nhật ký (quá dài, 30 nhãn [Chưa], nhiều mã nội bộ, phần lớn kiểm chứng do AI làm) và đề xuất cấu trúc 2 lớp.
  - `docs/mission1/redraft/current_design.md`: điều đang được quyết, nhóm theo phần của bài nộp, kèm nguồn gốc và mã cũ để lần vết; các quyết định bị đảo; 6 việc còn mở.
    Việc sắp xếp lại toàn bộ dự án được đưa vào "Deferred ideas" trong `playbook.md`.
  - Nhật ký này: Phần A (tóm tắt 7 mục, trong đó tuyên bố trách nhiệm để tôi tự viết) và các sửa đổi ở Phần B.
  - Khi đối chiếu file lưu phiên của cả Pi (`~/.pi`) và Claude Code (`~/.claude`), Claude phát hiện và sửa:
    - các mục 30-36 ghi công cụ là Claude Code, thực ra là Pi; chỉ mục 29 và một phiên brainstorm lúc 09:15 ngày 07/10 chạy trực tiếp trong Claude Code;
    - thời gian của các mục 25-36 thiếu giờ;
    - 4 phiên phụ chưa ghi (09:15 ngày 07/10; 12:38, 12:47 và 15:34 ngày 08/10), trong đó phiên 12:47 có subagent dùng mô hình OpenAI;
    - các nhãn [Chưa] đã lỗi thời hoặc không còn cần, vì bài nộp không dẫn luật hay nguồn web, hoặc bản nháp đã bị thay;
    - mâu thuẫn giữa sổ quyết định (A7, "Hiep checked every row" của bản lần vết) và mục 14 (tôi chưa đọc từng dòng).
- **Quyết định của tôi:** làm trang "thiết kế hiện tại" trước, chưa sắp xếp lại dự án; làm nhật ký trước các việc còn lại.
- **Xác minh:**
  - **[AI]** Claude mở trực tiếp bài AID Framework (arXiv 2408.01904) và trang của Charles Sturt University trước khi dẫn; hướng dẫn của Saint Louis University đọc từ nội dung tìm kiếm trả về.
  - **[AI]** Công cụ, mô hình và thời gian lấy từ file lưu phiên (trường `model`, `entrypoint`, `timestamp`), không từ trí nhớ của AI.
  - **[AI]** Các dữ kiện ở Phần A6 được kiểm lại trong phiên này: chạy script luật, đếm số từ, so số ngày phép và câu trích với văn bản giả lập.
  - **[AI]** Claude đối chiếu nhãn nguồn gốc trong `current_design.md` và Phần A3 với các mục 3-36, sửa 3 nhãn ghi quá nhiều hoặc quá ít phần của tôi.
  - **[Chưa]** Tôi đọc `current_design.md`, xác nhận từng dòng và 6 việc còn mở.
  - **[Chưa]** Tôi viết tuyên bố trách nhiệm (Phần A1).

## Mẫu cho các mục tiếp theo

Chạy `python tools/ai_sessions.py` để thấy mọi phiên của cả Pi và Claude Code và kiểm tra phiên nào chưa có mục; thêm `--since dd/mm` để chỉ xem từ một ngày.
Chạy `python tools/ai_sessions.py --prompts HH:MM` để lấy nguyên văn prompt của phiên bắt đầu lúc HH:MM.

```
### N. <Việc đã làm>

- **Thời gian:** <giờ theo lịch sử phiên>
- **Công cụ:** <công cụ và mô hình>
- **Prompt (nguyên văn):** "<prompt>"
  Ý chính: <tiếng Việt>
- **Đầu ra:** <file hoặc phần nào trong bài nộp>
- **Quyết định của tôi:** <tôi giữ, sửa hay bỏ gì từ đầu ra, và vì sao>
- **Xác minh:** <[Tôi] / [AI] / [Duyệt] / [Chưa] / [Không dùng], kèm cách kiểm tra>
```

<div style="page-break-before: always"></div>

# Mission 2

Ghi như Phần B của Mission 1, với ba thay đổi rút ra từ Mission 1:

- Công cụ, mô hình và thời gian lấy từ `tools/ai_sessions.py` ngay khi ghi mục, không ghi theo trí nhớ của AI; script đọc cả Pi và Claude Code.
- Mỗi mục ghi "Quyết định của tôi" ngay khi ghi; nhãn [AI] chỉ đổi thành [Tôi] khi tôi tự kiểm.
- Trước khi nộp, viết phần tóm tắt ở đầu phần này theo cấu trúc Phần A: công cụ, nguồn gốc từng phần, những lần tôi bác bỏ AI, lỗi của AI, kiểm chứng.

Mục được đánh số M2.1, M2.2, ... để không trùng với Mission 1.

### M2.1. Sau khi nộp Mission 1: lưu bài nộp và chuẩn bị Mission 2

- **Thời gian:** 21:33-21:50 ngày 08/10, tiếp tục lúc 13:36 ngày 10/10; cùng phiên với mục 37.
- **Công cụ:** Claude Opus 5.5 qua Pi.
- **Prompt (nguyên văn):**
  - "i just submitted. what to do in prior to mision 2" (21:33)
  - "do 1 2 5 6" (21:37)
  - "now 7 8  9" (21:42)
  - "." (13:36 ngày 10/10, để tiếp tục)
  - Ý chính: hỏi cần làm gì trước Mission 2; chọn làm các bước 1, 2, 5, 6 rồi 7, 8, 9 trong danh sách 9 bước Claude đề xuất.
- **Đầu ra:**
  - `docs/mission1/submitted/`: bản sao các file đã nộp, kèm README ghi nguồn của từng file.
  - `tools/render_pdf.py`: sửa khoảng cách của danh sách đánh số (đã dùng khi xuất PDF nộp nhưng chưa commit).
  - `docs/mission1/playbook.md`, mục 9: viết lại phác thảo kỹ thuật cho khớp thiết kế đã nộp; bản cũ (07/10) còn các trường và thứ tự ưu tiên đã bị bỏ.
  - `docs/mission2/mission1_promises.md`: 37 cam kết trích từ tài liệu và 3 câu trả lời đã nộp, mỗi cam kết kèm cách v1 chứng minh; dùng làm tiêu chí nghiệm thu Mission 2.
  - `data/`: 10 văn bản giả lập dạng Markdown kèm metadata, cây tổ chức, 3 persona và 10 dòng bộ test, chép từ `artifacts.md` và `adopted_rules.py`; `tools/check_data.py` kiểm các file khớp nguồn và chạy lại bộ test.
  - Sắp xếp tài liệu: `current_design.md` thành nguồn duy nhất cho thiết kế hiện hành, có mục "Changes since submission"; sổ quyết định được đóng băng; `AGENTS.md` và `README.md` tách file hiện hành với lịch sử Mission 1; sửa 3 dòng lỗi thời trong `decisions.md` và `artifacts.md`.
  - `tools/ai_sessions.py`: đọc thêm phiên Claude Code chạy trực tiếp (bỏ qua bản sao do claude-bridge ghi), lấy được prompt dán vào Claude Code, thêm `--since`.
- **Quyết định của tôi:** chọn 7 trong 9 bước; hai bước còn lại là việc tôi tự làm (tự kiểm các dữ kiện còn [Chưa], đọc `current_design.md` để chuẩn bị PITCH).
  Không bắt đầu viết code cho v1 trước khi có đề Mission 2.
- **Xác minh:**
  - **[AI]** So chữ của PDF đã lưu với bản xuất lại từ file nguồn: tài liệu trùng khớp; nhật ký chỉ khác chỗ xuống dòng.
  - **[AI]** `check_data.py` so từng trường metadata, persona, cây tổ chức, bộ test và nguyên văn từng văn bản với nguồn; bộ test 10/10 đạt trên các file.
    Thử sửa 14 thành 15 ngày và bỏ `overrides` trong một văn bản: script báo cả hai lỗi.
  - **[AI]** Ví dụ YAML trong `playbook.md` được đối chiếu với giá trị `adopted_rules.py` đọc; đã sửa 2 chỗ lệch (`overrides` là một chuỗi, không phải danh sách; dạng giá trị của `access`).
  - **[AI]** `ai_sessions.py` tìm đúng 2 phiên Claude Code chạy trực tiếp mà nhật ký đã ghi (09:15 ngày 07/10, mục 29) và bỏ qua 33 file là bản sao của phiên Pi.
  - **[Chưa]** Tôi xác nhận 3 ô trong `docs/mission1/submitted/README.md` (đúng file đã tải lên portal).
  - **[Chưa]** Tôi đọc `mission1_promises.md` đối chiếu với PDF đã nộp.

### M2.2. Nghiên cứu cách viết nhật ký bằng chứng tốt nhất cho Mission 2

- **Thời gian:** 13:44-14:02 ngày 10/10.
- **Công cụ:**
  - Claude Opus 5.5 qua Pi: đọc quy định cuộc thi và nhật ký Mission 1, tìm kiếm web bằng công cụ `web_search` (nhà cung cấp Exa và OpenAI), mở và đối chiếu nguồn, viết báo cáo.
  - Agnes 2.5 Flash (mức suy luận tối đa), qua 4 subagent chạy song song: 3 lượt xong, lượt "hiring" lỗi do giới hạn của gói miễn phí Agnes.
  - `tools/ai_sessions.py` chỉ thấy Claude Opus 5.5 trong phiên này; Agnes và các nhà cung cấp tìm kiếm được ghi tay.
- **Prompt (nguyên văn):** "I'm going to start mission 2 for this competition. The evidence log of the AI usage is an important part of the competition and the criteria that the competitions use to judge the candidates. It wants you to do research and do a deep dive into what the best practices are that can maximize the score. I want you to research what the max-score evidence log looks like. What are the things the competitors' organizer looks for when they have this evidence log as one part of the test? You can do a web search with Agnes models if you want. Use max reasoning level so you can search what the best practices are that people are doing with AI usage in the decoding task and what the competitions expect."
  Ý chính: nghiên cứu nhật ký bằng chứng đạt điểm tối đa trông như thế nào và ban tổ chức tìm gì trong nhật ký; có thể dùng Agnes để tìm web.
  Ngày 12/10, tôi trả lời 4 việc chờ quyết (nguyên văn, chọn lọc): "Question 1: approve.", "For question 2 I don't think I need it for now.", "we can consider adding the transcripts later when we finish the project. For now I want to keep focus on what the judge sees first.", "Open an issue on GitHub about this.", rồi sửa lại: "no close issue one, the issue is about writing the ai evidence, for the subagent listing, remove that idea"
- **Đầu ra:** `docs/mission2/evidence_log_research.md`: những gì quy định cuộc thi nói, cách nhật ký có thể được dùng khi chấm (suy luận), điểm chung của các nguồn bên ngoài, các khẳng định của subagent bị loại, đánh giá nhật ký Mission 1, thiết kế đề xuất cho nhật ký Mission 2, 4 việc chờ tôi quyết.
- **Quyết định của tôi (12/10):**
  - Chấp nhận giới hạn độ dài: phần tóm tắt tối đa 2 trang, các mục ngắn gọn.
  - Chưa làm bài tập tự xây lại luật lõi không dùng AI; tài liệu cho từng phần có thể làm sau.
  - Chưa nộp kèm lịch sử phiên (transcript); ưu tiên phần giám khảo đọc trước, xem lại khi xong dự án (issue GitHub #2).
  - Mission 2 không yêu cầu nộp nhật ký bằng chứng, nên hoãn phần nộp nhật ký cho Mission 2 (prompt: "mission two does not require the AI evidence submission so we will postpone that part").
  - Bỏ ý tưởng mở rộng `tools/ai_sessions.py` để liệt kê mô hình của subagent và nhà cung cấp tìm kiếm; issue #1 do Claude mở nhầm đề tài nên đã đóng.
- **Xác minh:**
  - **[AI]** Claude mở trực tiếp và trích nguyên văn mọi nguồn trong bảng ở mục 3 của báo cáo, trừ Monash và TEQSA (chỉ có nội dung tìm kiếm trả về, ghi [snippet only]).
  - **[AI]** Khi đối chiếu, Claude loại 4 khẳng định của subagent Agnes: thang điểm 10 điểm của Stanford CS230 (không có trên trang), các mức chấm của TEQSA (không tìm thấy, bản tóm tắt nói gần như ngược lại), cách diễn đạt của Monash, quy định về commit của ETHGlobal (không thấy trong trang đã mở).
  - **[AI]** Số liệu về nhật ký Mission 1 (16.850 từ, 45 nhãn [AI] so với 11 nhãn [Tôi], 15 dấu [Chưa]) đếm bằng `wc` và `grep` trên `docs/mission1/submitted/evidence_log.md`; số trang (28) lấy từ `docs/mission1/submitted/README.md`.
