# Mission 3 gap analysis

Step 1 of the [Mission 3 checklist](checklist.md): for each requirement of the [Mission 3 brief](../competition/mission3_brief.md), what Mission 2 does today, the evidence that it works, and the gaps that remain.
Claude draft, 21/10/2026, for Hiep to check.
All data is simulated ("giả lập").

This page lists gaps only.
Which ones Mission 3 closes is step 2 of the checklist, and every priority there is Hiep's.

"M2" is the code of tag `mission2` (`b6ca78d`).
The baseline is the Mission 2 run [`results/20261014-2239.jsonl`](../../results/20261014-2239.jsonl); its rows are in the [test report](../mission2/test_report.md), and "row N" below is row N of [`data/test_cases.yaml`](../../data/test_cases.yaml) in that run.
The run was made at commit `c3120ff`; between it and `b6ca78d` only the page banner and the report code changed (checklist step 0).

## How to read it

Every gap names its evidence, of one or more of these kinds:

- **Failed row:** a row of the baseline run fails because of it.
- **Passed row:** a row passes, but its output shows the gap; no gate checks it.
- **Limitation:** an open issue labelled `limitation` reproduces it.
- **Probe:** one of the probes P1-P9 in the [appendix](#appendix-the-probes) shows it; there is no row or issue for it yet.
- **Test:** a deterministic test in `tests/` asserts the behaviour.
- **On purpose:** Mission 2 chose it, in [`scope.md`](../scope.md) or an ADR; the evidence shows its effect.

The probes call the product's own code with the test suite's fake models, so they make no Gemini call and give the same result every time.
Where a probe needs a model reply, the reply is scripted, so the probe shows what the rules and the card do with that reply, not what Gemini would answer.

## The gap table

| Requirement | What M2 does today | Evidence that it works | Open gaps |
|---|---|---|---|
| Change Request | Not assigned yet: the brief says "Chưa có Change Request được chỉ định cho bạn" | - | Open: when it arrives, it is copied into `docs/competition/` and gets its own section here, with the same columns |
| [1. Phân biệt phiên bản và thời điểm có hiệu lực của tài liệu](#1-versions-and-effective-dates) | Rules keep the version in force on the as-of date, without reading the question; the answer card gives the document's title and start date | Rows 1 and 2 pass | G1.1-G1.5 |
| [2. Kiểm soát quyền truy cập theo bối cảnh người dùng](#2-access-by-the-askers-context) | Rules build the asker's scope from their unit and roles before any search, checking access last; nothing outside the scope reaches search or the model | Rows 5, 6, 10 and 13 pass; 0 leaks in the 14 gated rows and none in the 4 limitation rows; the leak test over every asker, boundary date and test question | G2.1-G2.3 |
| [3. Xử lý thông tin mâu thuẫn giữa nhiều nguồn/cấp tổ chức](#3-conflicting-sources-and-levels) | Precedence comes only from relations an owner declared; two policies on one topic with no declared relation form a conflict pair, and an answer citing either one gives the conflict card, which quotes both sides and does not choose | Rows 1, 3, 7 and 12 pass | G3.1-G3.7 |
| [4. Từ chối hoặc thể hiện rõ khi chưa đủ căn cứ](#4-refusing-when-the-basis-is-not-enough) | The model may return nothing; rules refuse the whole answer on any citation or quote they cannot verify, and the refusal card names the asker's HR contact | Rows 6, 8, 9, 10, 11, 13 and 14 refuse; 0 unsafe and 0 over-cautious in the 14 gated rows | G4.1-G4.5 |
| [5. Cho người dùng kiểm chứng tài liệu được sử dụng](#5-letting-the-user-check-the-documents-used) | The answer card shows the verified quote word for word, and names the document, the Điều and the start date | 7 of 7 answers read by Hiep against their quotes, all faithful | G5.1-G5.3 |

The 6 open limitation issues all appear below: [#24](https://github.com/Park-Hip/next-gen-2026/issues/24) (G3.1), [#50](https://github.com/Park-Hip/next-gen-2026/issues/50) (G1.3, G2.3, G3.3), [#51](https://github.com/Park-Hip/next-gen-2026/issues/51) (G4.2), [#52](https://github.com/Park-Hip/next-gen-2026/issues/52) (G3.2), [#53](https://github.com/Park-Hip/next-gen-2026/issues/53) (G1.1, G4.1) and [#74](https://github.com/Park-Hip/next-gen-2026/issues/74) (G3.3).
`scope.md` and the README list the first 5; #74 was opened on 20/10/2026, after Mission 2 was submitted.

## 1. Versions and effective dates

> Phân biệt phiên bản và thời điểm có hiệu lực của tài liệu.

**What M2 does today**

- Step 1 keeps, for each policy, the published version with the latest start date not after the as-of date (`in_force` in `services/scope.py`).
  Drafts and future versions never count, and a version past its end date ends its policy.
  The rules never read the question.
- Loading the data fails on two published versions of one policy with the same start date, on a document that replaces its own policy, and on a cycle of replacements (`integrations/data_files.py`).
- The answer card's source line gives the document's title, the Điều and the start date, for example "Quy chế nghỉ phép GameCo (bản 2), Điều 2, hiệu lực từ 01/01/2026".
  The page shows the as-of date ("Ngày áp dụng") above the card.

**Evidence that it works:** rows 1 and 2 pass.
The same asker and the same question get 14 days on 07/10/2026 and 15 days on 01/01/2027, and neither cites the draft version 4.

| ID | Gap | Evidence | Kind |
|---|---|---|---|
| G1.1 | A question about another period is answered with the version in force on the as-of date: the rules pick the version by that date, and the model is given no date at all | Row 18: Minh on 15/12/2026, "Từ năm sau tôi được nghỉ phép năm bao nhiêu ngày?", gets an answer card "14 ngày", where version 3 gives 15 days from 01/01/2027; the only unsafe answer of the run ([#53](https://github.com/Park-Hip/next-gen-2026/issues/53)); "Questions about past or future dates" is under Deferred in [`scope.md`](../scope.md) | Failed row; limitation; on purpose |
| G1.2 | Nothing tells the asker that the version they get is about to be replaced: the card says when it started, not when it stops | P4: with a reply citing version 2 Điều 2, the card for Minh on 15/12/2026 says 14 days, "hiệu lực từ 01/01/2026", and mentions neither "bản 3" nor "01/01/2027"; row 18's real card mentions neither; "Showing a future version as 'sắp thay đổi'" is under Deferred in [`scope.md`](../scope.md) | Probe; failed row; on purpose |
| G1.3 | A separate amendment that changes some clauses of a version cannot be declared: as "bổ sung" the old and the new value both stay in the scope with no conflict, as a new version it drops the clauses it does not amend, and as "dùng thay" it is G3.1 | [#50](https://github.com/Park-Hip/next-gen-2026/issues/50) example 2, on edited data: an amendment giving 16 days leaves both "14 ngày" and "16 ngày" in Minh's scope; rules only, the model was not run | Limitation |
| G1.4 | The as-of date comes from the request, so any visitor can read a published version before it is in force; production would use today's date only | P1: the date is a URL parameter; row 2 uses this on purpose to show the 2027 version; "As-of date" is under Simplified in [`scope.md`](../scope.md), and [#76](https://github.com/Park-Hip/next-gen-2026/issues/76) (decision 4, awaiting Hiep) recommends keeping it as a labelled demo control | Probe; on purpose |
| G1.5 | The card names the version only when the owner wrote it into the title: a document has no version field, so a policy with one version, or an owner who leaves the number out, gives a source line with no version | Row 5: "Nguồn: Quy chế nghỉ phép Tập đoàn, Điều 1, hiệu lực từ 01/01/2024. Hỏi thêm: HR Tập đoàn."; rows 1 and 2 show "(bản 2)" and "(bản 3)" only because the GameCo titles contain them; the metadata fields are in `integrations/data_files.py` | Passed row |

## 2. Access by the asker's context

> Kiểm soát quyền truy cập theo bối cảnh người dùng.

**What M2 does today**

- The asker's context is a unit and roles from a simulated profile (`data/personas.yaml`), picked on the page.
  There is no field to type a unit, and a role claimed in the question changes nothing.
- Access and applicability are separate rules: `access` says who may read a document (`all_staff`, `roles:...` or `unit:...`), and `applies_to` says which units must follow it.
- Access is checked last, so whether the asker may read a document never decides which policy replaces which (ADR 0010).
  It can still hide one side of a conflict pair (G3.6).
- Search runs only on the chunks of the asker's scope and raises `ScopeLeakError` on any other chunk; the model sees only what search returned.
- "Not allowed" and "not found" give the same refusal text, so a refusal does not reveal that a restricted document exists.

**Evidence that it works:** rows 5, 6, 10 and 13 pass.
The test report counts 0 leaks in the 14 gated rows, and none of the 4 limitation rows fails on a leak.
`tests/services/retrieval/test_search.py` asks every test question as each of the 3 askers on every boundary date, and again on seven trap mutations of the data on 07/10/2026, and no chunk outside the scope is returned.

| ID | Gap | Evidence | Kind |
|---|---|---|---|
| G2.1 | Who is asking comes from the request: the page reads `persona` from the URL, so anyone can ask as anyone and get that person's rules | P1: `GET /?persona=lan&...` with no cookie and no credential answers as Lan, "Bạn đang hỏi với tư cách: nhân sự Tập đoàn, Nhân sự Tập đoàn."; "Identity" is under Simplified in [`scope.md`](../scope.md); proposal [#76](https://github.com/Park-Hip/next-gen-2026/issues/76) | Probe; on purpose |
| G2.2 | The judges' page `/data` shows every visitor the title and the full text of a document only one role may read | P2: `/data` contains "Khung bậc lương GameCo" and "Bậc 3 có mức lương từ 18 đến 25 triệu đồng mỗi tháng", readable only by `hr_gameco`; `/cases` contains neither; the page is labelled "Góc nhìn ban tổ chức", and the file is public in the repository anyway, so this is the product's boundary, not a secret; [#76](https://github.com/Park-Hip/next-gen-2026/issues/76) decision 3 | Probe |
| G2.3 | A wrong `access` value is applied as written, so "0 leaks" holds only while the metadata is right | P7: with `access: all_staff` on `SAL-BAND-GAMECO`, Minh's scope gets both salary chunks; [#50](https://github.com/Park-Hip/next-gen-2026/issues/50): "a wrong `access` leaks every time, deterministically" | Probe; limitation |

## 3. Conflicting sources and levels

> Xử lý thông tin mâu thuẫn giữa nhiều nguồn/cấp tổ chức.

**What M2 does today**

- One policy wins over another only where its owner declared it: `overrides` ("dùng thay") drops the whole replaced policy for the units the document applies to.
  There is no default such as "the lower unit wins".
- `complements` ("bổ sung") lets two documents on one topic be used together.
- Two documents in the asker's scope with the same topic and no declared relation form a conflict pair.
  An answer citing either one gives the conflict card, which does not choose and sends the asker to HR.
  For each side it quotes the clauses the model cited, or, for a side with none, one clause chosen without reading meaning (ADR 0005).
  An answer citing neither, as in row 8, is not affected by the pair.

**Evidence that it works:** rows 1 (the Group policy replaced for Minh), 3 ("bổ sung", no conflict), 7 and 12 (conflict cards) pass.
In row 12 the model cited only the PayCo clause, and the card still quoted Điều 2 of both sides.

| ID | Gap | Evidence | Kind |
|---|---|---|---|
| G3.1 | A company that replaces one clause of a Group policy cannot say so: "dùng thay" drops the whole Group policy, and the asker loses the Group clauses the company kept | Row 15, on edited data, is refused instead of answered with the Group's notice of 3 working days; its rules part is a strict xfail in `tests/services/test_scope.py`; [#24](https://github.com/Park-Hip/next-gen-2026/issues/24) | Failed row; limitation |
| G3.2 | Conflicts are per document, not per question: when both sides say the same thing on the point asked, the asker still gets the conflict card | Row 17: Hà asks "Đơn nghỉ phép gửi cho ai duyệt?" and gets the conflict card, although both policies say "quản lý trực tiếp"; strict xfail in `tests/services/test_scope.py`; [#52](https://github.com/Park-Hip/next-gen-2026/issues/52) | Failed row; limitation |
| G3.3 | A disagreement that the metadata hides gives no conflict card: with a wrong or different topic, or a wrong "bổ sung", the pair is never formed, so a reply citing one side gives an answer card | [#74](https://github.com/Park-Hip/next-gen-2026/issues/74): with `LEAVE-PAYCO-v1` tagged `nghi_phep_nam`, Hà's scope has no conflict pair, and a reply citing the PayCo clause gives an answer card "13 ngày" (rules only); [#50](https://github.com/Park-Hip/next-gen-2026/issues/50) example 1; no test row yet | Limitation |
| G3.4 | No simulated document is issued below company level, so no row shows a department rule that adds to or replaces a company rule | P5: every document applies to the Group (level 1) or a company (level 2), while Minh and Hà sit at level 3; the rules themselves handle a lower level: `test_applies` in `tests/services/test_scope.py` applies a Studio document to a Studio asker, and in P9 a Kế toán policy enters Hà's scope and forms a pair with each of the other two | Probe; test |
| G3.5 | The owners never learn of a conflict: the card sends the employee to HR, and nothing is recorded for the two owners to settle it | Rows 7 and 12 end with "Vui lòng hỏi HR PayCo." and record nothing; ADR 0004 chose a records file, and the file was cut when [#15](https://github.com/Park-Hip/next-gen-2026/issues/15) was closed as not planned on 14/10/2026 (promise C3 in [`mission1_promises.md`](../mission2/mission1_promises.md)) | Passed row; on purpose |
| G3.6 | Access can hide a conflict: when one side of an undeclared pair is a document the asker may not read, the pair disappears and a reply citing the other side gives an answer card | P8: with `LEAVE-PAYCO-v1` readable only by `hr_payco`, Hà's scope keeps only the Group policy, and a reply citing its Điều 1 gives an answer card (12 days) instead of the conflict card, although the PayCo policy (13 days) applies to Hà; ADR 0010, Consequences: "a restricted document inside an undeclared conflict pair still makes the pair disappear"; `test_hiding_one_document_removes_only_that_document` asserts that the pair goes; no restricted document in the data is in a pair, so no row shows it | Probe; test; on purpose |
| G3.7 | A conflict among three or more documents is not worded for: the headline always says "hai quy định", and a document in two pairs is quoted twice | P9: with a third leave policy for Kế toán added in memory (15 days), Hà's scope has three pairs, and a reply citing PayCo Điều 1 gives a card headed "Có hai quy định cùng áp dụng cho bạn" that quotes the Group, PayCo, Kế toán and PayCo again; ADR 0005, "Would change if": "A case appears with three or more documents in one conflict" | Probe |

## 4. Refusing when the basis is not enough

> Từ chối hoặc thể hiện rõ khi chưa đủ căn cứ.

**What M2 does today**

- The model may return no points, and its instruction says that this is a correct answer.
- Step 7 refuses the whole answer on malformed output, no points, a point without a citation, a citation outside what search returned, or a quote that is not in the chunk it cites (`services/citations.py`).
- The refusal card names the asker's HR contact.
  If Gemini still fails after its retries, the page shows an error, never a card.

**Evidence that it works:** rows 6, 8, 9, 10, 11, 13 and 14 refuse as expected, and the 14 gated rows have 0 unsafe answers and 0 over-cautious cards.
`tests/services/test_citations.py` refuses invented ids and quotes that are not in their chunk.

| ID | Gap | Evidence | Kind |
|---|---|---|---|
| G4.1 | An answer where the system should have refused: the quote check proves that the clause exists, not that it answers the question asked | Row 18, the same failure as G1.1 ([#53](https://github.com/Park-Hip/next-gen-2026/issues/53)) | Failed row; limitation |
| G4.2 | A question that needs a clause applied to a case can be refused, although the clause that answers it was retrieved first | [#51](https://github.com/Park-Hip/next-gen-2026/issues/51): refused in a probe on 14/10/2026, answered as row 16 in the final run; each was asked once, so how often it happens is not known | Limitation |
| G4.3 | There is nothing between an answer and a refusal, and the refusal never says why: every reason gives "Hệ thống không tìm thấy quy định phù hợp", even when a clause was found but its quote failed the check | P6: no points, malformed output, a quote that is not in its chunk and a citation outside the retrieved chunks all give the same three lines; one text is on purpose for "not allowed" and "not found" (promise R10), but the other reasons are inside the asker's scope | Probe |
| G4.4 | An answer can rest on a condition the system cannot check: the clause says who it covers, and the asker's profile does not say whether that includes them | Row 5: Lan gets "Nhân sự chính thức của Tập đoàn được nghỉ phép năm 12 ngày mỗi năm."; the profile has only a unit and roles, so whether the asker is "chính thức" is left to them to read; ADR 0009, Consequences: "the rules still do not decide it"; employment type is under Deferred in [`scope.md`](../scope.md) | Passed row; on purpose |
| G4.5 | A faithful answer can leave out part of what was asked, and nothing tells the asker that it is incomplete | Row 3: "Tôi xin nghỉ phép ở đâu, ai duyệt?" is answered with two lines of the procedure, not the third, "Kết quả phê duyệt được gửi về email công ty của nhân sự.", which search returned; the row passes on its key facts, and its lesson in the test report says "không check tự động nào bắt được việc thiếu ý" | Passed row |

## 5. Letting the user check the documents used

> Cho người dùng kiểm chứng tài liệu được sử dụng.

**What M2 does today**

- The answer card shows the clauses the model quoted, word for word, after step 7 checked each quote against the chunk it cites (ADR 0003); it shows the quote, never a sentence the model wrote (ADR 0009).
- Under the quotes, one source line per cited document gives its title, the Điều, the start date and the HR contact.
- The conflict card quotes each side, as described in section 3 (ADR 0005).
- Every card starts with the identity the question was asked under ("Bạn đang hỏi với tư cách: ..."), and the page shows the question and the as-of date above it.

**Evidence that it works:** the 7 answer cards of the run (rows 1-5, 16 and 18) each name their source, and Hiep read all 7 against their quotes and marked them faithful.

| ID | Gap | Evidence | Kind |
|---|---|---|---|
| G5.1 | The employee cannot open the cited Điều or the document, so they see only the quoted sentences, not the rest of the clause or the lines around it | P3: the source line is plain text, and the card has no link; in row 3 the line the answer left out (G4.5) is in the cited document, but the employee cannot reach it from the card; proposal [#77](https://github.com/Park-Hip/next-gen-2026/issues/77) | Probe; passed row |
| G5.2 | For a document without "Điều" numbering, the source line names no part of it | Row 3: "Nguồn: Hướng dẫn đăng ký nghỉ phép trên hệ thống HR GameCo, hiệu lực từ 01/01/2026. Hỏi thêm: HR GameCo." | Passed row |
| G5.3 | The conflict card names each side by its unit, not by its document or version | Row 7: "Tập đoàn, Điều 1 (từ 01/01/2024): ..." and "PayCo, Điều 1 (từ 01/01/2025): ..."; row 12 the same with Điều 2; no title such as "Quy chế nghỉ phép PayCo" | Passed row |

## Changes already proposed

Three open proposals already touch these requirements; this page does not decide whether they are Mission 3 changes.

| Proposal | Serves | Gaps it targets | State on 21/10/2026 |
|---|---|---|---|
| [#75](https://github.com/Park-Hip/next-gen-2026/issues/75) Answer card: the model's sentence above its verified quote | [Spec](../mvp_spec.md) E1: an answer in plain Vietnamese that answers the question directly | None of the gaps above; it adds a sentence the model writes, not checked at run time, to the card of requirement 5, and its prompt asks the model to quote both sides of a disagreement nobody declared (G3.3) | Plan approved by Hiep on 20/10/2026; in progress, not merged |
| [#76](https://github.com/Park-Hip/next-gen-2026/issues/76) Sign in as a simulated account | Requirement 2 | G2.1; G2.2 through its decision 3; it keeps G1.4 if decision 4 is a) | Plan posted; decisions awaited |
| [#77](https://github.com/Park-Hip/next-gen-2026/issues/77) Answer card: open the cited Điều | Requirement 5 | G5.1 | No plan yet |

## Appendix: the probes

Run on 21/10/2026 at commit `259bfbb`, whose `src/`, `data/`, `config.yaml` and `tests/` are identical to tag `mission2` (`b6ca78d`).
Each probe calls the product's own functions or pages, with the fake embedder and the scripted fake model of `tests/fakes.py`, so no Gemini call is made and network access is blocked.
Edited data is either a temporary copy of `data/` (P7) or a changed copy of the loaded documents in memory (P8, P9); the files in the repository are never changed.

| Probe | What it does | Result |
|---|---|---|
| P1 | `GET /?persona=lan&as_of=2026-10-07&q=Phép năm của tôi là bao nhiêu ngày?`, with no cookie, and a fake reply citing `LEAVE-GROUP-v1#1` | 200, no cookie set; the card says "Bạn đang hỏi với tư cách: nhân sự Tập đoàn, Nhân sự Tập đoàn." and quotes the Group policy |
| P2 | `GET /data` and `GET /cases`, searched for the salary document's title and its Điều 2 | `/data` has both "Khung bậc lương GameCo" and "18 đến 25 triệu đồng"; `/cases` has neither |
| P3 | Minh, 07/10/2026, the leave question, with a fake reply citing `LEAVE-GAMECO-v2#2` | Source line "Nguồn: Quy chế nghỉ phép GameCo (bản 2), Điều 2, hiệu lực từ 01/01/2026. Hỏi thêm: HR GameCo."; 0 links in the card |
| P4 | As P3, on 15/12/2026 | The same card, 14 days; it mentions neither "01/01/2027" nor "bản 3", while `in_force` on 01/01/2027 gives `LEAVE-GAMECO-v3` |
| P5 | Each document's `applies_to`, and its depth in the org tree | The Group (level 1) for `LEAVE-GROUP-v1`; GameCo or PayCo (level 2) for the other 9; the askers sit at Studio (3), Nhân sự Tập đoàn (2) and Kế toán (3) |
| P6 | Step 7 and the card text for Minh on 07/10/2026, with four replies: no points, malformed, the quote "Nhân sự GameCo được nghỉ phép năm 30 ngày." citing `LEAVE-GAMECO-v2#2`, which does not contain it, and a citation of `OT-GAMECO-v1#1`, which was not retrieved | Reasons `no_points`, `malformed`, `quote_mismatch` and `outside_retrieved`; 1 distinct card text for all four |
| P7 | Minh's scope on 07/10/2026, on a temporary copy of `data/` where `SAL-BAND-GAMECO` has `access: all_staff` | Original: no salary chunk; edited: `SAL-BAND-GAMECO#1` and `SAL-BAND-GAMECO#2` |
| P8 | Hà's scope on 07/10/2026 with `LEAVE-PAYCO-v1` set to `access: roles:hr_payco`, and step 7 on a reply citing `LEAVE-GROUP-v1#1` | Original: both policies, one pair, conflict card; edited: `LEAVE-GROUP-v1` only, no pair, answer card |
| P9 | Hà's scope on 07/10/2026 with an added `LEAVE-KETOAN-v1` (a copy of the PayCo policy for Kế toán, 15 days, no relations), and the card for a reply citing `LEAVE-PAYCO-v1#1` | Three documents and three pairs; a conflict card headed "Có hai quy định cùng áp dụng cho bạn nhưng chưa được khai báo quan hệ với nhau." that quotes Tập đoàn Điều 1, PayCo Điều 1, Kế toán Điều 1 and PayCo Điều 1 again |

To run them again, save the script below outside the repository as `probe.py`, then from the repository root run `uv run python -I -X utf8 <path>/probe.py .`.

<details>
<summary>The probe script</summary>

```python
"""Mission 3 step 1 gap probes, deterministic: fake embedder, scripted fake LLM, no network.

Run from the repository root: uv run python -I -X utf8 <this file> <repo root>
Prints one block per probe; every probe calls the product's own functions or pages.
"""
import html
import json
import re
import shutil
import socket
import sys
import tempfile
from datetime import date
from pathlib import Path

REPO = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(REPO / "tests"))


def _blocked(*args, **kwargs):
    raise RuntimeError("network is disabled during probes")


_connect = socket.socket.connect


def _guarded(sock, address):
    if isinstance(address, tuple) and address[0] in {"127.0.0.1", "::1", "localhost"}:
        return _connect(sock, address)
    raise RuntimeError("network is disabled during probes")


socket.socket.connect = _guarded
socket.create_connection = _blocked

from fastapi.testclient import TestClient  # noqa: E402

from builders import RETRIEVAL, chunk_text  # noqa: E402
from fakes import FakeGemini, SyllableEmbeddings, reply_citing  # noqa: E402

from appota_kb.api.page import build_app  # noqa: E402
from appota_kb.core.config import load_config  # noqa: E402
from appota_kb.integrations.data_files import load_documents, load_org, load_personas  # noqa: E402
from appota_kb.models.answer import Point  # noqa: E402
from appota_kb.services.answering.answerer import Answerer  # noqa: E402
from appota_kb.services.card_text import render  # noqa: E402
from appota_kb.services.citations import card_for_answer  # noqa: E402
from appota_kb.services.retrieval.index import build_index  # noqa: E402
from appota_kb.services.scope import in_force, scope  # noqa: E402

LEAVE_Q = "Phép năm của tôi là bao nhiêu ngày?"
documents = load_documents()
org = load_org()
personas = load_personas(org)


def client(reply: str) -> TestClient:
    index = build_index(documents, SyllableEmbeddings())
    answerer = Answerer(index, FakeGemini(reply=reply), RETRIEVAL)
    return TestClient(build_app(load_config(), answerer))


def card_html(page: str) -> str:
    match = re.search(r"<article.*?</article>", page, re.S)
    return match.group(0) if match else ""


def card_text(page: str) -> str:
    return " ".join(re.sub(r"<[^>]+>", " ", card_html(page)).split())


def head(name: str) -> None:
    print(f"\n=== {name}")


# P1: who is asking comes from the request.
head("P1 identity from the URL")
quote = chunk_text(documents, "LEAVE-GROUP-v1#1")
c = client(reply_citing("LEAVE-GROUP-v1#1", quote_from={"LEAVE-GROUP-v1#1": quote}))
r = c.get("/", params={"persona": "lan", "as_of": "2026-10-07", "q": LEAVE_Q})
page = html.unescape(r.text)
print("request: GET /?persona=lan&as_of=2026-10-07&q=... with no cookie and no credential")
print("status:", r.status_code, "| set-cookie:", r.headers.get("set-cookie"))
print("card:", card_text(page))

# P2: the judges' pages show restricted text to every visitor.
head("P2 /data and /cases to an anonymous visitor")
for path in ("/data", "/cases"):
    page = html.unescape(c.get(path).text)
    print(
        path,
        "| title 'Khung bậc lương GameCo':", "Khung bậc lương GameCo" in page,
        "| salary clause '18 đến 25 triệu đồng':", "18 đến 25 triệu đồng" in page,
    )

# P3: the answer card's source is plain text.
head("P3 answer card source line, Minh 07/10/2026")
quote = chunk_text(documents, "LEAVE-GAMECO-v2#2")
c = client(reply_citing("LEAVE-GAMECO-v2#2", quote_from={"LEAVE-GAMECO-v2#2": quote}))
page = html.unescape(c.get("/", params={"persona": "minh", "as_of": "2026-10-07", "q": LEAVE_Q}).text)
print("card:", card_text(page))
print("links (<a ...>) inside the card:", len(re.findall(r"<a\s", card_html(page))))

# P4: nothing tells the asker that the version they get ends soon.
head("P4 answer on 15/12/2026, 17 days before version 3")
page = html.unescape(c.get("/", params={"persona": "minh", "as_of": "2026-12-15", "q": LEAVE_Q}).text)
text = card_text(page)
print("card:", text)
print("mentions '01/01/2027':", "01/01/2027" in text, "| mentions 'bản 3':", "bản 3" in text)
print("in force on 2027-01-01 for LEAVE-GAMECO:",
      [d.id for d in in_force(documents, date(2027, 1, 1)) if d.series == "LEAVE-GAMECO"])

# P5: the levels the simulated documents are issued at.
head("P5 levels of applies_to")
depth = {u: len(org.path(u)) for u in {p.unit for p in personas.values()} | {d.applies_to for d in documents}}
for d in sorted(documents, key=lambda d: d.id):
    print(f"{d.id:24} applies_to={d.applies_to:10} level={depth[d.applies_to]} status={d.status}")
print("units with an asker:", {p.id: (p.unit, depth[p.unit]) for p in personas.values()})

# P6: one refusal text for every reason step 7 refuses.
head("P6 refusal text by reason, Minh 07/10/2026")
s = scope(personas["minh"], date(2026, 10, 7), documents)
retrieved = ("LEAVE-GAMECO-v2#2", "LEAVE-GAMECO-v2#3")
by_id = {ch.id: ch for ch in s.chunks}
cases = {
    "no_points": (),
    "malformed": None,
    "quote_mismatch": (Point(chunks=("LEAVE-GAMECO-v2#2",), quote="Nhân sự GameCo được nghỉ phép năm 30 ngày."),),
    "outside_retrieved": (Point(chunks=("OT-GAMECO-v1#1",), quote=chunk_text(documents, "OT-GAMECO-v1#1")),),
}
texts = set()
for name, points in cases.items():
    card = card_for_answer(s, retrieved, points)
    lines = render(card, s, points, tuple(by_id[cid] for cid in retrieved))
    texts.add(lines)
    print(f"{name:17} -> kind={card.kind} reason={card.reason} lines={json.dumps(lines, ensure_ascii=False)}")
print("distinct refusal texts:", len(texts))

# P7: a wrong `access` value is applied as written.
head("P7 SAL-BAND-GAMECO with access: all_staff, on a temporary copy of data/")
with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp) / "data"
    shutil.copytree(REPO / "data", root)
    path = root / "documents" / "SAL-BAND-GAMECO.md"
    path.write_text(path.read_text(encoding="utf-8").replace("access: roles:hr_gameco", "access: all_staff"), encoding="utf-8")
    edited = load_documents(root)
    for label, docs in (("original", documents), ("edited", edited)):
        sc = scope(personas["minh"], date(2026, 10, 7), docs)
        sal = [ch.id for ch in sc.chunks if ch.document_id == "SAL-BAND-GAMECO"]
        print(f"{label:8} Minh's scope has SAL-BAND-GAMECO chunks: {sal}")

# P8: access decides the answer when it hides one side of a conflict pair.
head("P8 LEAVE-PAYCO-v1 with access: roles:hr_payco, Hà 07/10/2026, in memory")
from dataclasses import replace  # noqa: E402

hidden = [replace(d, access="roles:hr_payco") if d.id == "LEAVE-PAYCO-v1" else d for d in documents]
ha = personas["ha"]
for label, docs in (("original", documents), ("edited", hidden)):
    sc = scope(ha, date(2026, 10, 7), docs)
    ids = tuple(ch.id for ch in sc.chunks)
    points = (Point(chunks=("LEAVE-GROUP-v1#1",), quote=chunk_text(documents, "LEAVE-GROUP-v1#1")),)
    card = card_for_answer(sc, ids, points)
    print(f"{label:8} scope={[d.id for d in sc.documents]} pairs={[(a.id, b.id) for a, b in sc.conflicts]} "
          f"card for a reply citing LEAVE-GROUP-v1#1: {card.kind}")

# P9: three documents on one topic with no declared relation, one of them below company level.
head("P9 a third leave policy for Kế toán, Hà 07/10/2026, in memory")
payco = next(d for d in documents if d.id == "LEAVE-PAYCO-v1")
dept = replace(payco, id="LEAVE-KETOAN-v1", series="LEAVE-KETOAN", title="Quy chế nghỉ phép Kế toán",
               applies_to="Kế toán", body="Điều 1. Nhân sự Kế toán được nghỉ phép năm 15 ngày mỗi năm.")
docs = documents + [dept]
sc = scope(ha, date(2026, 10, 7), docs)
ids = tuple(ch.id for ch in sc.chunks)
points = (Point(chunks=("LEAVE-PAYCO-v1#1",), quote=chunk_text(documents, "LEAVE-PAYCO-v1#1")),)
card = card_for_answer(sc, ids, points)
by_id = {ch.id: ch for ch in sc.chunks}
lines = render(card, sc, points, tuple(by_id[cid] for cid in ids))
print("scope:", [d.id for d in sc.documents])
print("pairs:", [(a.id, b.id) for a, b in sc.conflicts])
print("card:", card.kind)
for line in lines:
    print("  ", line)
```

</details>
