# Artifacts - Mission 1 redraft

All data is simulated ("giả lập").

## Data model (Claude draft; fields follow decisions M0-M18)

Purpose: make the core model decisions concrete.
A field marked with a decision ID was set by that decision.

### Employee profile

Source: HR records (MVP: persona switcher).

| Field | Example (Minh) | Used for |
|---|---|---|
| `units` | GameCo → Studio | Applicability; access to unit-only documents (two units: M5) |
| `roles` | `employee` (Lan: `hr_group`) | Access to restricted documents |

Employment type and start date are out of the MVP (M0); they can be added later as applicability fields.

### Document metadata

| Check | Fields | Example (GameCo v2) |
|---|---|---|
| Identity | `id`, `title`, `doc_type`, `owner` | POL-LEAVE-GAMECO-v2, quy chế, HR GameCo |
| Version series (M9) | `series`: one document across its versions | `LEAVE-GAMECO` |
| Topic | `topic`, one value from a fixed list (M4) | `nghi_phep` |
| Allowed (who may read) | `access` | Group-wide / unit only / listed roles |
| Applicable (who it covers) | `applies_to.unit` | GameCo |
| In force (when) (M9, M10) | `status`, `effective_from`; `effective_to` only when the document really ends | published, from 01/01/2026, no end date |
| Relations (M11, M14) | `overrides`: a broader series used instead of this one; `complements`: a list of series this one adds to without contradicting them (M17) | overrides `LEAVE-GROUP` |

`replaces` is no longer typed by hand (M9): within a series, the version with the later `effective_from` supersedes the earlier one.

### Minh's trace

Moved to the section "Minh's trace" at the end of this file, rebuilt on the Step 3 document set.

## Personas (giả lập)

Approved by Hiep in Step 2.
As-of date for every artifact: 07/10/2026.

| `id` | `name` | `unit_path` | `roles` |
|---|---|---|---|
| `minh` | Minh | Tập đoàn / GameCo / Studio | `[employee]` |
| `lan` | Lan | Tập đoàn / Nhân sự Tập đoàn | `[employee, hr_group]` |
| `ha` | Hà | Tập đoàn / PayCo / Kế toán | `[employee]` |

## Simulated documents (giả lập)

Approved by Hiep in Step 3, then changed by decisions M9-M18 (series, `overrides` between series, `complements`, trap T11).
All content is simulated.
Topics: `nghi_phep`, `lam_them_gio`, `cong_tac_phi`, `luong`.
Order of the checks (M12, M18).
Steps 1-4 do not read the question; they build the asker's rulebook.

1. Current version of each series on the as-of date, the same for every asker (M9).
2. Filters on those current versions: access and applies to the asker.
3. `overrides` between series, counted only among documents that passed step 2 (M11).
4. Conflict pairs, per topic: two documents left on the same topic with no declared relation (`complements`) (M14).
5. The retriever returns chunks, only from the documents left after step 3.
6. The LLM answers from the chunks, citing each statement to its document, or says nothing relevant was found.
7. Rules decide the outcome from the cited documents: a cited document in a conflict pair shows the conflict with both documents; no valid citation is the refusal (M7); otherwise the answer.

The data is checked by `checks/adopted_rules.py`, which also runs the publish-time check (M15).

### Metadata

| `id` | `title` | `owner` | `series` | `topic` | `access` | `applies_to` | `status` | `effective_from` | `effective_to` | `overrides` | `complements` | Trap |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `LEAVE-GROUP-v1` | Quy chế nghỉ phép Tập đoàn | HR Tập đoàn | `LEAVE-GROUP` | `nghi_phep` | `all_staff` | Tập đoàn | published | 01/01/2024 | | | | T5, T7 |
| `LEAVE-GAMECO-v1` | Quy chế nghỉ phép GameCo (bản 1) | HR GameCo | `LEAVE-GAMECO` | `nghi_phep` | `all_staff` | GameCo | published | 01/01/2024 | | | | T1 |
| `LEAVE-GAMECO-v2` | Quy chế nghỉ phép GameCo (bản 2) | HR GameCo | `LEAVE-GAMECO` | `nghi_phep` | `all_staff` | GameCo | published | 01/01/2026 | | `LEAVE-GROUP` | | T5, T6, T11 |
| `LEAVE-GAMECO-v3` | Quy chế nghỉ phép GameCo (bản 3) | HR GameCo | `LEAVE-GAMECO` | `nghi_phep` | `all_staff` | GameCo | published | 01/01/2027 | | `LEAVE-GROUP` | | T2 |
| `LEAVE-GAMECO-v4-DRAFT` | Dự thảo quy chế nghỉ phép GameCo (bản 4) | HR GameCo | `LEAVE-GAMECO` | `nghi_phep` | `all_staff` | GameCo | draft | (empty) | | `LEAVE-GROUP` | | T3 |
| `LEAVE-PROC-GAMECO-v1` | Hướng dẫn đăng ký nghỉ phép trên hệ thống HR GameCo | HR GameCo | `LEAVE-PROC-GAMECO` | `nghi_phep` | `all_staff` | GameCo | published | 01/01/2026 | | | `[LEAVE-GAMECO]` | T11 |
| `LEAVE-PAYCO-v1` | Quy chế nghỉ phép PayCo | HR PayCo | `LEAVE-PAYCO` | `nghi_phep` | `all_staff` | PayCo | published | 01/01/2025 | | | | T6, T7 |
| `SAL-BAND-GAMECO` | Khung bậc lương GameCo | HR GameCo | `SAL-BAND-GAMECO` | `luong` | `roles:[hr_gameco]` | GameCo | published | 01/01/2026 | | | | T4 |
| `OT-GAMECO-v1` | Quy định làm thêm giờ GameCo | HR GameCo | `OT-GAMECO` | `lam_them_gio` | `all_staff` | GameCo | published | 01/01/2026 | | | | T8 |
| `TRAVEL-GAMECO-v1` | Quy định công tác phí GameCo | HR GameCo | `TRAVEL-GAMECO` | `cong_tac_phi` | `all_staff` | GameCo | published | 01/01/2026 | | | | T9 |

No document has an `effective_to`: none of them is temporary or repealed.
`LEAVE-PROC-GAMECO-v1` is written as plain steps, not "Điều", on purpose: relations work on unstructured documents too.
`LEAVE-GAMECO-v2` stays in force until v3 takes effect, so a delayed v3 cannot leave GameCo without a policy (M10).

### Bodies

**`LEAVE-GROUP-v1`**

Điều 1. Nhân sự chính thức của Tập đoàn được nghỉ phép năm 12 ngày mỗi năm.
Điều 2. Đơn nghỉ phép được gửi cho quản lý trực tiếp trước ít nhất 3 ngày làm việc.

**`LEAVE-GAMECO-v1`**

Điều 1. Nhân sự GameCo được nghỉ phép năm 13 ngày mỗi năm.
Điều 2. Đơn nghỉ phép được gửi cho trưởng nhóm trước ít nhất 3 ngày làm việc.

**`LEAVE-GAMECO-v2`**

Điều 1. Quy chế này thay thế quy chế nghỉ phép của Tập đoàn đối với nhân sự GameCo.
Điều 2. Nhân sự GameCo được nghỉ phép năm 14 ngày mỗi năm.
Điều 3. Đơn nghỉ phép được gửi cho trưởng nhóm trước ít nhất 3 ngày làm việc.

**`LEAVE-GAMECO-v3`**

Điều 1. Quy chế này thay thế quy chế nghỉ phép của Tập đoàn đối với nhân sự GameCo.
Điều 2. Nhân sự GameCo được nghỉ phép năm 15 ngày mỗi năm.
Điều 3. Đơn nghỉ phép được gửi cho trưởng nhóm trước ít nhất 3 ngày làm việc.

**`LEAVE-GAMECO-v4-DRAFT`**

Điều 1. Quy chế này thay thế quy chế nghỉ phép của Tập đoàn đối với nhân sự GameCo.
Điều 2. Nhân sự GameCo được nghỉ phép năm 16 ngày mỗi năm.
Điều 3. Văn bản đang trong giai đoạn lấy ý kiến, chưa ban hành.

**`LEAVE-PROC-GAMECO-v1`**

Để xin nghỉ phép, nhân sự GameCo tạo đơn trên hệ thống HR nội bộ (giả lập), chọn loại nghỉ và ngày nghỉ.
Hệ thống tự gửi đơn cho trưởng nhóm phê duyệt.
Kết quả phê duyệt được gửi về email công ty của nhân sự.

**`LEAVE-PAYCO-v1`**

Điều 1. Nhân sự PayCo được nghỉ phép năm 13 ngày mỗi năm.
Điều 2. Đơn nghỉ phép được gửi cho quản lý trực tiếp trước ít nhất 5 ngày làm việc.

**`SAL-BAND-GAMECO`**

Điều 1. Khung bậc lương GameCo gồm 5 bậc, từ bậc 1 đến bậc 5.
Điều 2. Bậc 3 có mức lương từ 18 đến 25 triệu đồng mỗi tháng (số liệu giả lập).

**`OT-GAMECO-v1`**

Điều 1. Làm thêm giờ phải được trưởng nhóm phê duyệt trước khi thực hiện.
Điều 2. Giờ làm thêm được nghỉ bù trong vòng 30 ngày kể từ ngày làm thêm.

**`TRAVEL-GAMECO-v1`**

Điều 1. Nhân sự GameCo đi công tác trong nước được hỗ trợ ăn uống 300.000 đồng mỗi ngày.
Điều 2. Vé đi lại và khách sạn được thanh toán theo hóa đơn, tối đa theo hạn mức do trưởng phòng duyệt.

## Minh's trace (Hiep) (giả lập)

Persona: Minh, `Tập đoàn / GameCo / Studio`, roles `[employee]`.
As-of date: 07/10/2026.
Question: "Phép năm của tôi là bao nhiêu ngày?"
Claude wrote the first draft at Hiep's request, instead of Hiep tracing it from the empty template in the phase 2 prompt.
Hiep checked every row and approved it.
Rebuilt after decisions M9-M12 (series, no pre-typed end dates, `overrides` between series) and M14 (`complements`, trap T11), then after M18 (rulebook first, then retrieval; no topic picked from the question).

### Step A - Current version of each series (M9)

This step is the same for every asker.
Per series, the current version is the published version with the latest `effective_from` that is not after 07/10/2026.

| Series | Versions | Current version | Why the other versions are out |
|---|---|---|---|
| `LEAVE-GROUP` | v1 | `LEAVE-GROUP-v1` | - |
| `LEAVE-GAMECO` | v1, v2, v3, v4-DRAFT | `LEAVE-GAMECO-v2` | v1: superseded by v2, whose `effective_from` 01/01/2026 is later (T1). v3: `effective_from` 01/01/2027 is after the as-of date (T2). v4: `status: draft` (T3) |
| `LEAVE-PROC-GAMECO` | v1 | `LEAVE-PROC-GAMECO-v1` | - |
| `LEAVE-PAYCO` | v1 | `LEAVE-PAYCO-v1` | - |
| `SAL-BAND-GAMECO` | one | `SAL-BAND-GAMECO` | - |
| `OT-GAMECO` | v1 | `OT-GAMECO-v1` | - |
| `TRAVEL-GAMECO` | v1 | `TRAVEL-GAMECO-v1` | - |

### Step B - Filters for Minh (rule 2)

Only the current versions from Step A are checked.

| Doc | Passes access? | Applies to Minh? | Result |
|---|---|---|---|
| `LEAVE-GROUP-v1` | Yes (`all_staff`) | Yes (Tập đoàn covers everyone below) | Kept |
| `LEAVE-GAMECO-v2` | Yes (`all_staff`) | Yes (GameCo) | Kept |
| `LEAVE-PROC-GAMECO-v1` | Yes (`all_staff`) | Yes (GameCo) | Kept |
| `LEAVE-PAYCO-v1` | Yes (`all_staff`) | No (PayCo is not on Minh's path) | Removed by `applies_to` (T6) |
| `SAL-BAND-GAMECO` | No (needs role `hr_gameco`, Minh has `[employee]`) | Yes (GameCo) | Removed by `access` (T4) |
| `OT-GAMECO-v1` | Yes (`all_staff`) | Yes (GameCo) | Kept |
| `TRAVEL-GAMECO-v1` | Yes (`all_staff`) | Yes (GameCo) | Kept |

### Step C - `overrides` between series (rule 3, M11)

| Doc | Relation used | Result |
|---|---|---|
| `LEAVE-GROUP-v1` | `LEAVE-GAMECO-v2` declares `overrides: LEAVE-GROUP`, and v2 was kept in Step B | Removed for Minh (T5) |
| `LEAVE-GAMECO-v2` | Declares the relation | Kept |
| `LEAVE-PROC-GAMECO-v1` | No `overrides` (its `complements` is used in Step E) | Kept |
| `OT-GAMECO-v1`, `TRAVEL-GAMECO-v1` | None | Kept |

### Step D - Conflict pairs per topic (rule 4, M14, M18)

This step does not read the question.
It checks every topic among the 4 documents left after Step C.

| Topic | Documents left | Result |
|---|---|---|
| `nghi_phep` | `LEAVE-GAMECO-v2`, `LEAVE-PROC-GAMECO-v1` | No conflict: the procedure declares `complements: [LEAVE-GAMECO]` (T11) |
| `lam_them_gio` | `OT-GAMECO-v1` | One document, no pair (T8: a different topic is never a conflict) |
| `cong_tac_phi` | `TRAVEL-GAMECO-v1` | One document, no pair |

Minh's rulebook on 07/10/2026: these 4 documents, no conflict pair.
If the procedure had not declared the relation, the `nghi_phep` pair would be a conflict pair.

### Step E - Retrieval and answer (rules 5 and 6, M18)

The retriever searches only the chunks of the 4 documents in Minh's rulebook.
For "Phép năm của tôi là bao nhiêu ngày?", the chunk expected at the top is Điều 2 of `LEAVE-GAMECO-v2` ("14 ngày mỗi năm") (expected, not measured).
The LLM writes the answer only from the returned chunks, and cites each statement to its own document.
`LEAVE-GROUP-v1` (12 days) and the other GameCo versions cannot be returned, because they are not in the rulebook.

### Result (rule 7)

The answer cites `LEAVE-GAMECO-v2`, which is in the rulebook and in no conflict pair, so the system shows the answer.
Answer: 14 days of annual leave, citing `LEAVE-GAMECO-v2` (Quy chế nghỉ phép GameCo, bản 2), in force from 01/01/2026, owner HR GameCo.
The procedure does not state a number of days, so it is only cited if the answer adds how to apply (for example "đăng ký trên hệ thống HR").
If the LLM cited a document outside the rulebook, that citation would be dropped; with no valid citation left, Minh would get the refusal.

### Things to note

1. Without `overrides` on `LEAVE-GAMECO-v2`, Group v1 and GameCo v2 would both be left as a conflict pair, and Minh would get the conflict (rule 7).
   Hà's case (T7) is exactly that shape.
2. GameCo v1 is removed in Step A by its own series, not by a relation that another document must carry.
   So it stays out on 01/01/2027, when v3 replaces v2.
   Under the old rule (`replaces` counted only among filtered documents), v1 came back on that date and conflicted with v3 (`production_review.md`, P1).
3. On 01/01/2027, v3 becomes the current version automatically.
   If v3 is delayed, v2 stays in force, because it has no `effective_to` (M10).
4. If Group publishes a new leave policy, `LEAVE-GAMECO-v2` still overrides it, because `overrides` names the series, not a version (M11).
5. The procedure's `complements` names the series `LEAVE-GAMECO`, so it keeps working when v3 takes effect on 01/01/2027.
6. If GameCo repealed its policy, the procedure would be left next to `LEAVE-GROUP-v1` with no declared relation, which is a conflict.
   That is correct: the procedure was confirmed against GameCo's policy, not the Group's.
   The publish-time check (M15) lists this pair as soon as the repeal is entered, before it takes effect.

## Naive vs correct, Minh's question (Claude draft) (giả lập, minh họa, chưa đo)

Question: "Phép năm của tôi là bao nhiêu ngày?"
Persona: Minh, `Tập đoàn / GameCo / Studio`. As-of date: 07/10/2026.
No similarity score was measured.
The left column describes the failure qualitatively.
What a real retriever returns first is expected, not measured.

| | Naive: search, then answer | Core model (M9-M18) |
|---|---|---|
| What goes into search | All 10 documents, ranked by similarity to the question | Minh's rulebook: 4 documents (`LEAVE-GAMECO-v2`, `LEAVE-PROC-GAMECO-v1`, `OT-GAMECO-v1`, `TRAVEL-GAMECO-v1`) |
| Leave documents that compete | `LEAVE-GROUP-v1` (12), `LEAVE-GAMECO-v1` (13), `LEAVE-GAMECO-v2` (14), `LEAVE-GAMECO-v3` (15), `LEAVE-GAMECO-v4-DRAFT` (16), `LEAVE-PAYCO-v1` (13) | `LEAVE-GAMECO-v2` only (the procedure states no number of days) |
| Why they compete | Seven documents use almost the same words about annual leave, so similarity cannot tell them apart; it sees no `status`, date, unit or relation | The other leave documents were removed by exact metadata before search |
| Likely answer | One of 12, 13, 15 or 16 days, or a blend such as "12 đến 16 ngày tùy quy chế", said with confidence | "14 ngày", citing `LEAVE-GAMECO-v2`, from 01/01/2026, owner HR GameCo |
| If the top result is wrong | Nothing notices; the LLM writes a fluent answer from it | A citation outside the rulebook is dropped; with no valid citation Minh gets the refusal |

How each trap breaks the naive chatbot:

| Trap | What goes wrong without the filter | What stops it in the core model |
|---|---|---|
| T1 | `LEAVE-GAMECO-v1` (13 days) is still published and matches the question | Step A: v2 has the later `effective_from` in the same series |
| T2 | `LEAVE-GAMECO-v3` (15 days) is the newest file, so it looks like the answer | Step A: `effective_from` 01/01/2027 is after 07/10/2026 |
| T3 | The draft (16 days) reads like a policy | Step A: `status: draft` |
| T5 | `LEAVE-GROUP-v1` (12 days) is a broader policy that says the same kind of thing | Step C: GameCo v2 `overrides` the Group series |
| T6 | `LEAVE-PAYCO-v1` (13 days) is readable by Minh but covers another company | Step B: `applies_to` |

T4 (the salary band) is not triggered by this question, because it does not match leave wording.
It is exposed by a salary question, in the outcome table below.

## Outcome table and cards (Claude draft, Hiep edits the wording) (giả lập)

Three outcomes, one card each.
Every card starts with "Bạn đang hỏi với tư cách", so the asker sees which rulebook was used.
As-of date: 07/10/2026.

| Outcome | Persona and question | Trap | Rule | Cited |
|---|---|---|---|---|
| Answer | Minh: "Phép năm của tôi là bao nhiêu ngày?" | T1, T2, T3, T5, T6, T11 | 7 | `LEAVE-GAMECO-v2` |
| Conflict | Hà: "Phép năm của tôi là bao nhiêu ngày?" | T7 | 4, 7 | `LEAVE-GROUP-v1` and `LEAVE-PAYCO-v1` |
| Refusal | Minh: "Khung bậc lương của GameCo thế nào?" | T4 | 6 | none |

The refusal card is the same text for "not allowed" (T4) and "not found" (T9).
It only changes the unit in the first line.

### Card 1 - Answer (Minh)

> **Bạn đang hỏi với tư cách:** nhân sự GameCo, Studio
>
> **Phép năm của bạn là 14 ngày mỗi năm.**
>
> Nguồn: `LEAVE-GAMECO-v2` - Quy chế nghỉ phép GameCo (bản 2), có hiệu lực từ 01/01/2026.
> Cần hỏi thêm: HR GameCo.
>
> [Báo sai]

### Card 2 - Conflict (Hà)

> **Bạn đang hỏi với tư cách:** nhân sự PayCo, Kế toán
>
> **Có hai quy định về phép năm cùng áp dụng cho bạn và chúng khác nhau. Hệ thống không tự chọn một quy định.**
>
> - `LEAVE-GROUP-v1` - Quy chế nghỉ phép Tập đoàn, từ 01/01/2024: 12 ngày mỗi năm.
> - `LEAVE-PAYCO-v1` - Quy chế nghỉ phép PayCo, từ 01/01/2025: 13 ngày mỗi năm.
>
> Vui lòng hỏi HR PayCo để biết quy định nào áp dụng. Chủ sở hữu hai văn bản (HR Tập đoàn, HR PayCo) đã được báo để xác nhận mối quan hệ giữa hai văn bản.

### Card 3 - Refusal (Minh)

> **Bạn đang hỏi với tư cách:** nhân sự GameCo, Studio
>
> **Hệ thống không tìm thấy quy định phù hợp để trả lời câu hỏi này cho bạn.**
>
> Vui lòng liên hệ HR GameCo.

Notes for Hiep when editing the wording:

1. The refusal says "không tìm thấy quy định phù hợp" and never "bạn không có quyền", so it does not reveal that a restricted document exists (M7).
2. The conflict card names two owners, because the two documents have different owners.
   The system routes the asker to HR of their own unit (M7), and notifies both owners.
   "Đã được báo" is a promise for Mission 2: the MVP must either send that notice or the sentence must go.
3. The answer card cites only `LEAVE-GAMECO-v2`.
   The procedure is cited only when the answer adds how to apply.
4. "[Báo sai]" is the report button (B1).
   It sends the question, the answer, the cited documents and the persona to the owner of each cited document.
