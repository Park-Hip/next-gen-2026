# AGENTS.md

## Project

Appota NextGen AI Talent 2026, Bài test B - "Tri thức nội bộ Appota".
Goal: an AI assistant that gives each employee the right knowledge for their unit, their access rights, and the version in force today.
Current stage: Mission 1 submitted on 08/10/2026; preparing Mission 2 (build v1) before its brief arrives.
Mission 3 (adapt to change) is expected to follow.

## Files

Read `docs/mission1/redraft/current_design.md` first.

Competition (do not edit):

- `docs/competition/mission1_brief.md` - official brief. Source of truth.
- `docs/competition/rules.md` - competition rules.
- `docs/competition/ai_policies.md` - AI usage policy. Binding, overrides anything here.

Current:

- `docs/mission1/redraft/current_design.md` - the single source for the design in force, grouped by submission section, with origin and old IDs as a trace; every design change is made here and listed under "Changes since submission".
- `docs/mission2/mission1_promises.md` - every commitment in the submitted Mission 1 text, as the Mission 2 acceptance checklist.
- `data/` - the simulated documents, org tree, personas and test cases as files (see `data/README.md`). Check them with `python -I -X utf8 tools/check_data.py`.
- `docs/mission1/redraft/artifacts.md` - simulated data model, personas, documents, Minh's worked trace, test matrix, metrics and the 3-day plan.
- `docs/mission1/redraft/checks/adopted_rules.py` - the adopted core model run on the simulated data, plus the publish-time check and the deterministic part of the test matrix. Run with `python -I -X utf8 docs/mission1/redraft/checks/adopted_rules.py`.
- `docs/mission1/playbook.md` - strategy notes; section 9 prepares Missions 2-3; "Deferred ideas" lists what is out of scope.
- `evidence_log.md` - AI usage log for all missions; Mission 1 is Phần A-B, Mission 2 has its own section. Add an entry whenever AI shapes the result.
- `tools/render_pdf.py` (Markdown to PDF), `tools/ai_sessions.py` (lists Pi and Claude Code sessions for the evidence log), `tools/check_data.py`.
- `build/` - generated output, not committed.

Mission 1 record (do not edit):

- `docs/mission1/submitted/` - the exact files submitted on 08/10, with a README on where each came from.
- `docs/mission1/document.md` and `docs/mission1/answers.md` - sources of the submitted document and answers; render with `python tools/render_pdf.py docs/mission1/document.md build/mission1_draft.pdf` (5 pages).
- `docs/mission1/redraft/decisions.md` - decision register, frozen on 08/10; the audit trail behind the submitted text and the evidence log.

Mission 1 history (cited by the evidence log and the register; read only to trace a past decision):

- `docs/mission1/redraft_plan.md` - the redraft plan, Phases 0-7.
- `docs/mission1/criteria.md` - what Mission 1 was judged on, and the rewrite principles.
- `docs/mission1/thinking/` - thinking-phase workbook and the candidate's decisions (Round 1-3).
- `docs/mission1/redraft/open_issues.md` - gaps found while building the artifacts.
- `docs/mission1/redraft/production_review.md` - review of the core model against real practice (findings P1-P9).
- `docs/mission1/redraft/phase2_prompt.md`, `phase3_decisions.md`, `review_notes.md` - Phase 2 prompt, the A-vs-B arguments for Section 4, Hiep's review notes.
- `docs/mission1/review_prompt_reader.md`, `docs/mission1/redraft/review_reader_output.md` - new-reader review prompt and its Claude output (same model family, not independent).
- `docs/mission1/review_prompt_answers.md`, `docs/mission1/redraft/review_answers_output.md` - independent ChatGPT/Gemini review of the answers and its verbatim output (A13).
- `docs/mission1/review_prompt.md`, `docs/mission1/review_output.md` - pre-redraft review of the first draft.
- `docs/mission1/redraft/checks/current_rules.py`, `proposed_rules.py` - rule scripts from the production review.

## Competition rules that affect agents

- Mission 1 scoring (from the brief): 40% Khung vấn đề - "bạn có hiểu đúng vấn đề không?", 35% Thực thi - "giải pháp có chạy thật không?", 25% Chất lượng quyết định - "lý do chọn A thay vì B có thuyết phục không?".
- Every AI tool and prompt that shaped the final result must be declared in the evidence log, with how the output was verified. Undeclared AI use costs 30% of the score.
- The candidate must be able to explain or rebuild any part during the PITCH round. Explain your reasoning; never hand over output the candidate cannot defend.
- Unverified hallucinations fail the criterion. Flag every factual claim that needs checking.
- No plagiarism. Credit any public solution or source that is used.
- Code comments in English.

## Mission 1 deliverable

Three parts are submitted (brief, "Nộp gì cho mission 1"), and no code is required:

1. One PDF/DOCX or a Notion link, at most 5 pages, written in Vietnamese (English technical terms are fine).
   It covers 5 sections: problem and users, solution and flow, AI/data/people, decisions and risks, validation and MVP.
2. The 3 mandatory "Forced Decision" answers, submitted separately from the PDF.
   The brief requires "Trả lời ngắn gọn, rõ quyết định và lý do. Khuyến nghị 60–150 từ.": each answer opens with the decision, gives the reason, and is 60-150 words counted by whitespace.
3. The evidence log (`evidence_log.md`): AI tools, prompts, and decisions.
   It is a judged deliverable, so keep it accurate, readable and in Vietnamese.

## Core thesis

A relevant document is not necessarily allowed, in force, or applicable to the person asking.
Keep access, validity and applicability separate in every design and every piece of writing.

## Working rules

- All Appota data is simulated. Label it "giả lập" and never invent research or measurements.
- Deterministic rules decide access, validity and precedence. The LLM only interprets language.
- Promise only what can be built in Mission 2.
- Do not use the em dash. Use a plain "-".
- Put each sentence on its own line in Markdown.

## Scope discipline (MVP first)

AI suggestions that sound impressive but do not fit the MVP are a real risk to shipping time.
Treat every suggestion as out of scope until it proves it serves the current mission.

- Before proposing or accepting a feature, architecture or tool, ask: does it directly serve the Mission 1 deliverable or the Mission 2 MVP?
  If not, do not add it.
- Prefer the simplest design that works end to end.
  Do not add abstractions, layers, services, frameworks or config systems "for later".
- Do not build for scale, extensibility or edge cases that the brief does not require.
  Note them as future work in one line instead.
- When a suggestion is impressive but out of scope, do not implement it.
  Name it, say in one sentence why it is deferred, and park it under "Deferred ideas" in `docs/mission1/playbook.md`.
- Flag complexity honestly.
  If a suggestion adds a new dependency, a new moving part, or more than about half a day of work, say so and ask before proceeding.
- Never let a deferred idea leak into the document as a promise.
  Only promise what can be built in Mission 2.
- When unsure whether something is in scope, ask the candidate.
  Do not decide silently.
