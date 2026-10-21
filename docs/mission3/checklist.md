# Mission 3 checklist

The acceptance checklist for Mission 3, taken from [`docs/competition/mission3_brief.md`](../competition/mission3_brief.md).
Claude draft, 20/10/2026, updated 21/10/2026, for Hiep to check against the brief.
Every box is either ticked with its evidence, or left open with the reason.

Deadline: **11:48, 23/10/2026**; the system locks and there is no extension, so plan to submit by the evening of 22/10.
The brief grades "hiểu yêu cầu mới → lựa chọn → cải tiến → kiểm chứng → giải thích quyết định", not the number of features.
Scoring (`rules.md`): 40% problem framing, 35% execution, 25% decision quality.

## 0. Before any change

- [x] Tag the commit submitted for Mission 2 (`mission2`), so "before" is one fixed commit that judges can open.
  - Annotated tag `mission2` created locally on `b6ca78d` (merge of PR #71, 15/10 16:25), the last commit on `main` before the Mission 2 deadline (about 20:00 on 15/10, [`plan.md`](../mission2/plan.md)); the next commit on `main` is the Mission 3 brief on 20/10.
  - Hiep asked for the push on 21/10 and the tag is on `origin` (`git ls-remote --tags origin mission2` shows it).
- [x] Keep the Mission 2 run `results/20261014-2239.jsonl` as the baseline; never regenerate it.
  - The file is committed once (`9e3b384`) and unchanged since: SHA-256 `597e1480124ec35bfac7e35ad6f72bb3d75ba95aef2093efc446eb82ae018a26` on disk, at `b6ca78d` and at `836d770`.
  - It holds 18 rows, all run at commit `c3120ff` with a clean tree and `gemini-3.5-flash-lite`.
  - From `c3120ff` to `b6ca78d` only the page banner text and the report code changed, not data, config, prompts or rules, so the baseline is the submitted product's answers.
  - The harness already protects it: a new run refuses an existing file (`evaluation/run.py`), and `--resume` refuses when the commit differs from the first record, so Mission 3 code cannot append to it.
- [ ] Check the portal for the Change Request; repeat every morning until it arrives.
  - Hiep only; the portal cannot be reached from the repository. As of 20/10 the brief says "Chưa có Change Request được chỉ định cho bạn".
- [x] Decide whether the Mission 2 demo stays online next to the Mission 3 one, for side-by-side comparison.
  - Decided by Hiep on 20/10: the Mission 2 demo stays online.
  - Today `render.yaml` deploys `main` with `autoDeploy: true`, so the first Mission 3 merge replaces the Mission 2 demo behind the link judges already have.
  - The brief asks for a new link ("Link phiên bản Mission 3").
  - Render free tier ([docs](https://render.com/docs/free), read 20/10): 750 free instance hours per workspace per month, shared by all free services; a spun-down service uses none; it spins down after 15 minutes without traffic; if the hours run out, every free service is suspended until the next month.
  - Two services awake around the clock from 20/10 to 31/10 use at most 2 × 12 × 24 = 576 hours, under 750 if October's earlier use leaves room (Hiep checks the Billing page).
  - Render can pin a service to one commit: "Deploy a specific commit" in the dashboard, which also turns auto-deploy off ([docs](https://render.com/docs/deploys#deploying-a-specific-commit)).
  - How: the current service stays the Mission 2 demo, pinned to `mission2` (`b6ca78d`) with auto-deploy off, and a second free service from `main` serves Mission 3 at its own URL; the video and the before/after then show the same question live on both.
- [ ] Pin the Mission 2 service before the first Mission 3 code change is merged: Render Dashboard, the service's Deploys page, "Manual Deploy > Deploy a specific commit", `b6ca78d`.
  - The deploy steps in the #11 plan create the service from the Blueprint (`render.yaml`); if so, a Blueprint sync applies `autoDeploy: true` from `render.yaml` again, so `render.yaml` must also be changed to match: auto-deploy off for the Mission 2 service, and a second service for Mission 3.
  - Both services would share one `GEMINI_API_KEY` quota unless the second gets its own key.
  - Open and urgent, as of 21/10: Mission 3 code has already merged (#90, #92, #93, #94) and `render.yaml` still has one service on `main` with `autoDeploy: true`.
    Unless Hiep pinned the service by hand in the dashboard, the Mission 2 link now serves Mission 3 code.
    The repository cannot show the dashboard; Hiep checks it.

## 1. Understand the new requirement

- [ ] The Change Request, once assigned, is copied word for word into `docs/competition/`, as the briefs were.
  - Open: not assigned as of 21/10/2026 (step 0).
- [ ] A gap table maps the Change Request and each of the 5 general requirements to what M2 does today, the evidence for it, and the open gap: [`gaps.md`](gaps.md).
  - Open for the Change Request only: its row says it is not assigned yet, and it gets its own section in `gaps.md` when it arrives.
  - [x] Phân biệt phiên bản và thời điểm có hiệu lực của tài liệu: G1.1-G1.5.
  - [x] Kiểm soát quyền truy cập theo bối cảnh người dùng: G2.1-G2.3.
  - [x] Xử lý thông tin mâu thuẫn giữa nhiều nguồn/cấp tổ chức: G3.1-G3.7.
  - [x] Từ chối hoặc thể hiện rõ khi chưa đủ căn cứ: G4.1-G4.5; G4.1 is G1.1 seen from this requirement.
  - [x] Cho người dùng kiểm chứng tài liệu được sử dụng: G5.1-G5.3.
- [ ] Each gap names its evidence from M2: a test row, a limitation issue (#24, #50, #51, #52, #53, #74) or a probe; no gap is claimed without one.
  - Done for the 5 general requirements: every gap in `gaps.md` names a row of the baseline run, a limitation issue, a test or one of the probes P1-P9, and all 6 limitation issues appear.
  - The probes use the test suite's fake models, so they make no Gemini call; the script and the result of each probe are in the appendix of `gaps.md`.
  - Open until the Change Request's gaps are added the same way.

## 2. Choose

- Merged so far (21/10), for reference when the lists below are written:
  - With an issue and a plan: #75 (ADR 0011, supersedes 0009), #76 (simulated sign-in, ADR 0016), #83 (validity window and next change, ADR 0012), #87 (conflicts, ADR 0014 and 0015; the G3.6 fix was dropped).
  - Docs only: ADR 0013 and the section write-ups (#85, #86, #88, #91, #95, #97).
  - Still proposals: #96 (why a refusal happens), #77 (open the cited Điều), #39 (docs for judges), #16 (submission README).
- [ ] Every candidate change has a priority and one line of reason in Hiep's words.
- [ ] A written "chủ động chưa làm" list: each item not built, with why (it feeds Question 1).
- [ ] Each of the 5 general requirements is either improved, or explicitly kept as it is, with the reason.
- [ ] The Change Request is improved; it is never skipped.
- [ ] Every design change has an ADR in `docs/decisions/` in the same PR; a reversal of an earlier ADR (for example #75 against ADR 0009) says what is given up.
  - Open: ADRs 0011 to 0016 exist; check each against its PR before ticking, and ADR 0013 landed in a docs PR (#85), not with code.
- [ ] A choice with real alternatives went through a `research` issue first.
- [ ] Nothing is rebuilt from scratch: every change lands on the Mission 2 code, in the same repository.

## 3. Improve

- [ ] Each change: issue from a form → plan comment approved by Hiep → branch `<issue>-<short-title>` → PR with the template and `Closes #<issue>`.
- [ ] Rules still decide access, validity, applicability, precedence and the card; the LLM only interprets language.
- [ ] New tunable values are `config.yaml` keys read through `core/config.py`, added by the PR that first reads them.
- [ ] `python -m pytest` passes before every PR; no new flaky or skipped test is left unexplained.
- [ ] The Mission 3 version is deployed, and every demo link in the README works after a cold start.

## 4. Verify

### 4.1 Regression

- [ ] All 18 Mission 2 rows are run again on the Mission 3 code, through the same harness as the demo.
  - Open: the only Mission 3 run so far is `results/20261021-1032.jsonl` (20 rows, all `ok`, commit `d31d304`).
    It predates #90, #92, #93 and #94, so it is an early run, not the final one; its review sheet is still "[chờ Hiệp]" for faithful and lesson.
- [ ] Every gate that passed in M2 still passes: rules correct, 0 leaks, 0 unsafe answers, over-cautious within target, faithfulness on every answer.
- [ ] A row that changed result is explained, whether it got better or worse.

### 4.2 New tests (brief minimum: 3)

- [ ] At least 1 test for the Change Request.
- [ ] At least 1 edge case or hard case for the improvement.
- [ ] At least 1 regression test for an old function that the change could break.
- [ ] Each new test is a row in `data/test_cases.yaml` with its reason, and, where possible, a deterministic test in `pytest`.
- [ ] Each row is reported as "Kỳ vọng → Kết quả thực tế → Đạt/Chưa đạt → Điều học được".

### 4.3 Evidence that M3 is better

- [ ] A before/after table per row: M2 result → M3 result, from the two committed runs, generated, never edited by hand.
- [ ] A row that went from fail to pass is run more than once, so a lucky run (as row 16 in M2) is not counted as a fix; the number of runs is stated.
- [ ] Every new answer, and every sentence the model writes on a card, is read by Hiep against its quote.
- [ ] Every number in the docs comes from a committed run; nothing is estimated or invented.
- [ ] A known failure that stays keeps its issue open with the `limitation` label.

## 5. Explain

### 5.1 Before → After (mandatory), for each change

- [ ] **M2 - Trước cải tiến:** what M2 did, with a test row or screenshot.
- [ ] **Vấn đề/Yêu cầu mới:** the Change Request or the general requirement, and the gap.
- [ ] **Quyết định thay đổi gì / không thay đổi gì:** with the ADR.
- [ ] **M3 - Sau cải tiến:** what M3 does now, with the same row or screenshot.
- [ ] **Bằng chứng cho thấy tốt hơn:** the before/after row results and gates.
- [ ] **Giới hạn còn lại:** what still fails, with its issue.

### 5.2 The 3 mandatory questions

- [ ] Câu 1: what was prioritised and what was deliberately not done, and why.
- [ ] Câu 2: the change that made the biggest difference, and the evidence that M3 is better.
- [ ] Câu 3: the biggest remaining risk if real users had it tomorrow, and how it would be handled first.

### 5.3 README and docs

- [ ] The README leads with Mission 3: links to the new demo, the video, the before/after and the updated test report.
- [ ] The Mission 2 answers stay readable (moved, not deleted).
- [ ] `docs/scope.md` and the limitation list match the final run.
- [ ] Every public source or solution used is credited.

### 5.4 Video (5 minutes or less)

- [ ] Structure: "Yêu cầu mới → Quyết định → Before/After → Kết quả → Giới hạn"; no full demo of the product again.
- [ ] Shows the same question on M2 and on M3 for the main change.
- [ ] Public link, checked without signing in.

## 6. Competition rules

- [ ] Every AI tool and prompt that shaped the result is in the evidence log, with how it was checked; `docs/evidence_log.md` is refreshed from the local log before submission.
- [ ] Hiep can explain or rebuild every change in the PITCH round; every factual claim in the docs has been checked.
- [ ] No API keys, passwords or real data in the repository or its history; all data labelled "giả lập".

## 7. Submission

- [ ] GitHub repository: the same repository as Mission 2, history kept, every PR merged into `main`, CI green.
- [ ] Mission 3 demo link.
- [ ] Video link.
- [ ] Updated test suite: Change Request + edge case + regression, and the report of the run.
- [ ] The 3 mandatory answers.
- [ ] Submitted on the portal before 11:48, 23/10/2026, and the submission page checked afterwards.
