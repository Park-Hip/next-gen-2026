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
- `docs/mission1/thinking/` - thinking-phase workbook and the candidate's decisions (Round 1-3).
- `docs/mission1/submitted/` - the exact files submitted, kept as a record.
- `evidence_log.md` - AI usage log for all missions. Add an entry whenever AI shapes the result.
- `build/` - generated output, not committed.

## Competition rules that affect agents

- Scoring: 40% problem framing, 35% execution (does it run?), 25% decision quality.
- Every AI tool and prompt that shaped the final result must be declared in the evidence log, with how the output was verified. Undeclared AI use costs 30% of the score.
- The candidate must be able to explain or rebuild any part during the PITCH round. Explain your reasoning; never hand over output the candidate cannot defend.
- Unverified hallucinations fail the criterion. Flag every factual claim that needs checking.
- No plagiarism. Credit any public solution or source that is used.
- Code comments in English.

## Mission 1 deliverable

- One PDF/DOCX, at most 5 pages, written in Vietnamese (English technical terms are fine).
- Covers 5 sections: problem and users, solution and flow, AI/data/people, decisions and risks, validation and MVP.
- Answers 3 mandatory questions, each 60-150 words, opening with the decision.

## Core thesis

A relevant document is not necessarily allowed, in force, or applicable to the person asking.
Keep access, validity and applicability separate in every design and every piece of writing.

## Working rules

- All Appota data is simulated. Label it "giả lập" and never invent research or measurements.
- Deterministic rules decide access, validity and precedence. The LLM only interprets language.
- Promise only what can be built in Mission 2.
- Do not use the em dash. Use a plain "-".
- Put each sentence on its own line in Markdown.
