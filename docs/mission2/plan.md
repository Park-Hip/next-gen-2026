# Mission 2 plan

Claude (Opus 5.5) draft of 12/10/2026, reviewed by Hiep in a Lavish session the same evening; his answers are in "Decisions".
Mission 2 opened on 12/10/2026 at about 20:00; the deadline is 3 days later, about 15/10 20:00 (exact time to confirm on the portal).
Target: submit by 15/10 17:00.
All Appota data is simulated ("giả lập").

## The bet

Build the 7-step pipeline thin but real and get it online on day 1.
Then spend most of the time measuring the one risky part, the LLM working inside the asker's scope, and report honestly where it fails.

What we prove (Mission 2 question 1): rules build the asker's scope before any AI runs.
If the scope is right, a wrong version, another unit's rule or a restricted document cannot reach an answer, because the LLM never sees them.
What remains is the LLM citing a valid in-scope document that does not answer the question, or misstating it: the riskiest assumption of Mission 1 (V6).

## Decisions (Hiep, 12/10/2026)

| ID | Question | Hiep's answer |
|---|---|---|
| D1 | How `data/` gets its issue and PR | Move commit `e3ec479` off `master`; land it through #3 with Hiep's check |
| D2 | LLM and embeddings | Gemini free tier, newest Flash allowed, `gemini-embedding-001`; working default until #6 |
| D3 | Hosting | Render free web service, auto-deploy from `main`; working default until #7 |
| D4 | A Studio-level document (third org level) | Yes, with an ADR (#10) |
| D5 | New test rows | N1-N6 (#10) |
| D6 | Who writes the "văn nói" phrasings and the lessons | Hiep; Claude checks the format |
| D7 | CI | GitHub Actions runs pytest on every PR |
| D8 | Demo extras and README language | No trace panel or compare view; README in English |
| D9 | "Hiệp's check" in the PR template | Yes |
| D10 | Dependencies (fastapi, uvicorn, jinja2, pyyaml, google-genai, pytest) | Approved as a working default; research may change it, with Hiep's approval |
| D11 | Open the issues | All at once, under the "Mission 2" milestone |
| D12 | Where research and decisions live | Write-ups in `docs/research/`, ADRs in `docs/decisions/` linking them; one PR per research issue |
| D13 | Research topics | R1-R5 (#4-#8), run on 13/10 |
| D14 | D2, D3 and D10 while research runs | Working defaults; research can overturn them before #11 and #13 start |
| D15 | Who runs the research | Hiep, with his own research agent; Claude provides the template and files the results |

## Roadmap

Each issue has its own branch `<issue>-<short-title>` and a PR that says `Closes #<issue>`.
Promise IDs refer to `docs/mission2/mission1_promises.md`.

| Day | Issue | Work | Depends on |
|---|---|---|---|
| 12/10 | No issue | Workflow bootstrap PR: forms, templates, research layer, this plan | - |
| 12/10 | #3 | Simulated data as files, reviewed by Hiep, with phrasings for rows 2-10 | Bootstrap PR |
| 13/10 | #4-#8 | Research R1-R5; each closes with a write-up and an ADR | - |
| 13/10 | #9 | Rules engine (steps 1-4 and 7), deterministic tests, CI | #3 |
| 13/10 | #10 | Studio-level document and rows N1-N6 (ADR 0005) | #9 |
| 13/10 | #11 | Walking skeleton: the page with the three cards, deployed | #9, ADR 0004 (#7) |
| 14/10 | #12 | Hybrid retrieval inside the asker's scope | #9, ADRs 0001-0002 (#4, #5) |
| 14/10 | #13 | LLM answer with citations and the step 7 cards | #12, ADR 0003 (#6) |
| 14/10 | #14 | Evaluation harness and the test report | #13, ADR 0006 (#8) |
| 15/10 | #15 | "Báo sai", conflict records and the owners' page | #13 |
| 15/10 | #16 | Submission README with the 3 mandatory questions | All |
| 15/10 | No issue | Final run on the deployed commit, video, make the repository public, submit | #16 |

Rules (#9) merge before retrieval (#12), as promised in Mission 1 (B1).
Cut order if a day slips: first #15 (records stay in a file, as Mission 1 V4 planned); never #9 or #14.

## Definition of done

- The demo URL works from a clean browser; the README warns that the first load can take about a minute.
- The README answers the 3 questions and links the test report: at least 5 cases, with at least one good, one hard and one failing.
- Every major choice has a research write-up and an ADR with Hiep's reasons.
- Every PR is merged with "Hiệp's check" ticked, and CI is green on `main`.
- Every known failure has an open issue labelled `limitation`, and the README and video mention it.
- The video is at most 5 minutes; the repository is public, and its history has no key patterns (`AIza`, `sk-`, `.env`).

## Not doing in v1

As promised in Mission 1 (Câu 2, V4): real login or HR system, chat-tool integration, DOCX or PDF reading, multi-turn memory, an LLM judge, an owner upload screen, notifications.
The naive-RAG baseline stays deferred (RV10); the trace panel and compare view are dropped (D8).
