# AGENTS.md

## Project

Appota NextGen AI Talent 2026, Bài test B - "Tri thức nội bộ Appota".
Goal: an AI assistant that gives each employee the right knowledge for their unit, their access rights, and the version in force today.
Current stage: Mission 1 (analysis document only, no product yet).
Missions 2 (build v1) and 3 (adapt to change) are expected to follow.

## Files

- `docs/competition/mission1_brief.md` - official brief. Source of truth. Do not edit.
- `docs/competition/rules.md` - competition rules. Do not edit.
- `docs/competition/ai_policies.md` - AI usage policy. Do not edit. Binding, overrides anything here.
- `docs/mission1/playbook.md` - working notes and strategy for Mission 1-3.
- `docs/mission1/document.md` - the 5-page submission draft. Render it with `python tools/render_pdf.py docs/mission1/document.md build/mission1_draft.pdf`.
- `docs/mission1/answers.md` - the 3 mandatory answers, submitted in a separate field.
- `docs/mission1/criteria.md` - what Mission 1 is judged on, and the rewrite principles.
- `docs/mission1/review_prompt.md` - prompt for an independent AI review.
- `docs/mission1/review_output.md` - output of running that prompt (same model as the drafter, so not independent).
- `docs/mission1/thinking/` - thinking-phase workbook and the candidate's decisions (Round 1-3).
- `docs/mission1/submitted/` - the exact files submitted, kept as a record.
- `evidence_log.md` - AI usage log for all missions. Add an entry whenever AI shapes the result.
- `build/` - generated output, not committed.

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
2. The 3 mandatory "Forced Decision" answers, submitted separately from the PDF, each about 60-150 words, opening with the decision.
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
