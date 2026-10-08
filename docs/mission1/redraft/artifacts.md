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
Điều 3. Ngày nghỉ bù không trừ vào số ngày phép năm.

Điều 3 was added in Phase 4 (V6, Claude proposal, accepted by Hiep 08/10) so that test row 4 has an answer in the data.

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
If the LLM cited a document outside the rulebook, the whole answer would be refused, even if another citation were valid (RV5).

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
| If the top result is wrong | Nothing notices; the LLM writes a fluent answer from it | A citation outside the rulebook refuses the whole answer (RV5) |

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
> **Có hai quy định cùng áp dụng cho bạn nhưng chưa được khai báo quan hệ với nhau. Hệ thống không tự chọn.** (RV8: the system only knows the relation is undeclared, not that the texts differ)
>
> - `LEAVE-GROUP-v1` - Quy chế nghỉ phép Tập đoàn, Điều 1, từ 01/01/2024: "Nhân sự chính thức của Tập đoàn được nghỉ phép năm 12 ngày mỗi năm."
> - `LEAVE-PAYCO-v1` - Quy chế nghỉ phép PayCo, Điều 1, từ 01/01/2025: "Nhân sự PayCo được nghỉ phép năm 13 ngày mỗi năm."
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
   Decided in V4 (accepted by Hiep 08/10): the conflict card writes one record per owner to the owners' list, and the sentence becomes "đã được ghi nhận để chủ sở hữu hai văn bản (HR Tập đoàn, HR PayCo) xác nhận".
3. The answer card cites only `LEAVE-GAMECO-v2`.
   The procedure is cited only when the answer adds how to apply.
4. "[Báo sai]" is the report button (B1).
   It sends the question, the answer, the cited documents and the persona to the owner of each cited document.
   How the report reaches the owner in the MVP is decided in V4 (accepted by Hiep 08/10): a record in one owners' list, a page filtered by owner, with no email or chat notice.
5. Decided in V7 (accepted by Hiep 08/10): the refusal card gets one more line, the same for every refusal, "Hệ thống chỉ trả lời các quy định áp dụng cho bạn.", so a question about another unit's rule (M3a) gets its explanation without anything detecting the unit.
6. Decided in RV4 (accepted by Hiep 08/10): the conflict card quotes the cited chunk of each document word for word, so the LLM writes nothing on it.
   A document of the pair with no cited chunk is shown by title and effective date only.

## Phase 4 - Test matrix, metrics and 3-day plan (Claude draft, accepted by Hiep 08/10) (giả lập)

Decisions V1, V2, V4, V5, V6 and V7 in `decisions.md`.
Nothing here was measured: the LLM columns are what Mission 2 must check.
The deterministic part of every row is run by `checks/adopted_rules.py` (`run_matrix`), and all 10 rows pass.

### Test matrix (excerpt, 10 rows)

"Cấm (luật)" are documents outside the asker's rulebook: rules guarantee they cannot be cited.
"Cấm (LLM)" are documents inside the rulebook that do not answer the question: only the LLM can avoid citing them (V2).

| # | Persona | Question | As-of | Expected behaviour | Must cite | Must not cite: luật | Must not cite: LLM | Trap |
|---|---|---|---|---|---|---|---|---|
| 1 | Minh | Phép năm của tôi là bao nhiêu ngày? | 07/10/2026 | Answer: 14 ngày | `LEAVE-GAMECO-v2` | `LEAVE-GROUP-v1`, `LEAVE-GAMECO-v1`, `-v3`, `-v4-DRAFT`, `LEAVE-PAYCO-v1` | - | T1, T2, T3, T5, T6 |
| 2 | Minh | Phép năm của tôi là bao nhiêu ngày? | 01/01/2027 | Answer: 15 ngày | `LEAVE-GAMECO-v3` | `LEAVE-GAMECO-v2`, `-v1`, `-v4-DRAFT`, `LEAVE-GROUP-v1`, `LEAVE-PAYCO-v1` | - | T2 (version switch, M6, M9) |
| 3 | Minh | Tôi xin nghỉ phép ở đâu, ai duyệt? | 07/10/2026 | Answer: tạo đơn trên hệ thống HR, trưởng nhóm duyệt; no conflict | `LEAVE-PROC-GAMECO-v1` (`LEAVE-GAMECO-v2` allowed) | `LEAVE-GROUP-v1`, `LEAVE-GAMECO-v1` | - | T11 |
| 4 | Minh | Ngày nghỉ bù sau làm thêm giờ có trừ vào phép năm không? | 07/10/2026 | Answer: không trừ; no conflict across topics | `OT-GAMECO-v1` (`LEAVE-GAMECO-v2` allowed) | `LEAVE-GROUP-v1`, `LEAVE-GAMECO-v1` | - | T8 (needs V6) |
| 5 | Lan | Phép năm của tôi là bao nhiêu ngày? | 07/10/2026 | Answer: 12 ngày | `LEAVE-GROUP-v1` | `LEAVE-GAMECO-v2`, `LEAVE-PAYCO-v1` | - | T6 (readable, not applicable) |
| 6 | Lan | Nhân sự GameCo được nghỉ phép năm bao nhiêu ngày? | 07/10/2026 | Refusal (another unit's rule, M3a, V7) | - | `LEAVE-GAMECO-v2` | `LEAVE-GROUP-v1` | M3a |
| 7 | Hà | Phép năm của tôi là bao nhiêu ngày? | 07/10/2026 | Conflict card with both documents, no number chosen | `LEAVE-GROUP-v1` or `LEAVE-PAYCO-v1` (the card shows both) | `LEAVE-GAMECO-v2`, `LEAVE-PROC-GAMECO-v1` | - | T7 |
| 8 | Hà | Làm thêm giờ có cần ai duyệt trước không? | 07/10/2026 | Refusal; not a leave conflict card | - | `OT-GAMECO-v1` | `LEAVE-GROUP-v1`, `LEAVE-PAYCO-v1` | T6, T8 |
| 9 | Hà | Đi công tác được hỗ trợ ăn uống bao nhiêu một ngày? | 07/10/2026 | Refusal | - | `TRAVEL-GAMECO-v1` | `LEAVE-GROUP-v1`, `LEAVE-PAYCO-v1` | T9 |
| 10 | Minh | Khung bậc lương của GameCo thế nào? | 07/10/2026 | Refusal, same text as row 9 apart from the unit; the reply contains no salary figure and no document title | - | `SAL-BAND-GAMECO` | `LEAVE-GAMECO-v2`, `LEAVE-PROC-GAMECO-v1`, `OT-GAMECO-v1`, `TRAVEL-GAMECO-v1` | T4, M7 |

What the script shows about the last column, if the LLM cites the "Cấm (LLM)" documents:

- Row 6: Lan gets an answer card "12 ngày" for a question about GameCo.
- Rows 8 and 9: Hà gets a false leave conflict card for a question about overtime or travel.
- Row 10: Minh gets an answer card built from his leave, overtime and travel documents.

Rules cannot stop these, because every one of those documents is valid for the asker.
They are the remaining path to a confident wrong answer, which is why V2 is about them.

Mutation check (run once by hand in this session, not kept in the script): removing `overrides` from `LEAVE-GAMECO-v2`, or publishing the draft v4 with an `effective_from` in the past, makes 3 of the 10 rows fail.
So the matrix catches a broken rule or a broken document, not only the happy path.

In Mission 2 every row is asked in 3 phrasings: as written, without the key word (for example "Năm nay tôi được nghỉ mấy ngày?"), and in colloquial speech (for example "Em được off mấy ngày phép một năm?"; RV7 replaced the earlier "without diacritics" phrasing).
That gives 30 cases; each case is run 3 times because LLM output varies, and a case fails if any run fails.

### Metrics (V1)

| Stage | Metric | Threshold on the 30 cases | Reason |
|---|---|---|---|
| Rules (steps 1-4, 7) | Rulebook correct: must-cite documents in it, "Cấm (luật)" documents not in it; outcome correct given the citations | 100%, release gate | Same input, same output: one failure is a bug, not noise, and it is a confident wrong answer or a leak |
| Rules | Leak: no chunk outside the asker's access reaches the retriever's output or the LLM's input | 0, release gate | Checked on chunk ids against `access`, no LLM judge; one leak is the failure HR stops the product for (Round 2) |
| Rules | Refusal text identical for "not allowed" and "not found" (rows 9 and 10) | 100%, release gate | A different text reveals that a restricted document exists (M7) |
| LLM (steps 5-6) | Unsafe error: an answer card where the expected outcome is a refusal or a conflict, a wrong key fact, or a "Cấm (LLM)" citation | 0, release gate for L | This is the problem in F1; with employees asking directly (L) nobody stands between this error and the employee |
| LLM | Faithfulness: every statement in an answer is in the chunk it cites | 100%, read by hand, release gate for L | The answer rows give about 45 answers to read, so a person can check all of them; an LLM judge would add a second model to trust |
| LLM | Over-cautious error: a refusal or a conflict card where an answer was expected, or a false conflict card on a refusal row | At most 10% of cases (3 of 30 at the planned size; RV11) | Safe-side error: the employee asks HR, which is today's situation; more than 1 in 10 means employees go back to HR and the assistant stops being used |
| Retriever | Must-cite chunk among the chunks given to the LLM | Diagnostic, no threshold | It explains over-cautious errors; correctness is judged on the outcome, not on ranking |

Honest limit: 0 failures in 30 cases only shows, with 95% confidence, that the true failure rate is below about 9.5% (computed in `run_matrix`).
Passing the gates is the precondition for letting employees ask directly, not proof that the answers are always right; after opening, the live signal is confirmed "Báo sai" reports (the pilot was removed by RV9).
Latency gets no target in v1: it is logged, and no decision depends on it.

### 3-day plan (V4)

| Day | Build | Done when |
|---|---|---|
| 1 | The 10 documents as Markdown files with the metadata above, chunked by Điều (by paragraph for the procedure); 3 personas; steps 1-4 and 7 ported from `adopted_rules.py`; the 30 cases as a data file; the deterministic checks and the leak check | Every rules-stage gate passes, with no LLM in the loop yet |
| 2 | Step 5: a hybrid retriever (keyword plus embedding, RV7) over the chunks of the asker's rulebook only; step 6: the LLM answers from those chunks and cites each statement, or says nothing relevant was found; the 30 cases run 3 times | Unsafe errors, faithfulness and over-cautious errors measured, prompt fixed until the gates pass or the failure is written down |
| 3 | One web page: persona switcher, as-of date as a test input (M6), the three cards, "Báo sai" and conflict records in one owners' list page; final run of the matrix (the naive baseline, V5, was removed by RV10) | The demo shows rows 1, 7 and 10 end to end, and the results table is written from the final run |

Cut order if a day slips: the owners' list page first (records kept in a file), never the test matrix or the gates.

### Not doing in the 3 days (V4)

Each cut holds the documents, metadata and identity fixed, so a failure on the matrix can only come from the LLM and retriever, which is what V2 tests.

| Not doing | Why it does not affect testing V2 |
|---|---|
| Real SSO or HRIS | The persona switcher gives the same two fields (`units`, `roles`); V2 is about reading documents, not where identity comes from |
| Document upload, owner screen, AI-suggested metadata | Metadata is written by hand, so a wrong answer cannot be blamed on wrong metadata |
| Publish-time check screen | Stays a script (M15); the query-time check is the same resolver (M16) |
| Email or chat notices to owners | Reports land in the owners' list; the delivery channel does not change whether an answer is right |
| Integration with the company chat tool | The web page asks the same pipeline |
| Multi-turn memory | Each case is one question; memory kept across a persona switch could leak one persona's documents into another's answer |
| Personal data such as remaining leave balance | Needs the HR system and a privacy review; V2 is about policy text |
| PDF, DOCX or OCR ingestion | Documents are Markdown; parsing does not change which documents are valid |
| Search tuning beyond plain hybrid search (reranking, weight tuning) | The rulebook holds at most 4 documents per persona; retrieval is diagnostic |
| Showing future versions (M8), other units' rules (M3a), two units per person (M5), employment type (M0) | Decided out earlier; none of them is needed by a row of the matrix |
| LLM judge for faithfulness | About 45 answers can be read by hand |

