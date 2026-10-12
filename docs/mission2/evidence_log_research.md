# Evidence log for Mission 2: research and recommendations

Written 10/10/2026 for the Mission 2 evidence log.
Hiep decided the open points on 12/10/2026 (section 7); section 6 is the plan in force.

How this was produced:
Claude Opus 5.5 via Pi read the competition files and the submitted Mission 1 log.
Four Agnes 2.5 Flash subagents (max reasoning) searched the web on four angles; three finished, and the "hiring" lane failed on the Agnes free-tier rate limit.
Claude covered that angle itself with the `web_search` tool (Exa and OpenAI providers) and direct page fetches.
Every source quoted below was opened by Claude unless it is marked [snippet only].
Section 4 lists the subagent claims that did not survive this check.

## 1. What the competition itself says

These are primary sources, in `docs/competition/`.

- `ai_policies.md`, required: "Ghi lại mọi công cụ AI + prompt đã định hình kết quả cuối cùng trong Nhật ký Bằng chứng. Tóm tắt cách bạn đã xác minh đầu ra của AI."
- `ai_policies.md`, prohibited: "Nộp đầu ra của AI mà bạn không hiểu. Trong vòng PITCH (Bảo vệ), chúng tôi sẽ yêu cầu bạn xây lại hoặc giải thích bất kỳ phần nào."
- `ai_policies.md`, penalties: "Không khai báo việc dùng AI = -30% điểm. Ảo giác AI rõ ràng mà không xác minh = trượt tiêu chí đó."
- `ai_policies.md`, purpose: "Chúng tôi kiểm tra bạn trở thành ai khi có AI - và liệu bạn có làm chủ được kết quả hay không."
- `ai_policies.md`, the organizer's own "good" example: three one-line entries, each with tool, task, prompt gist, a concrete check, and in one case a human fix ("Đã test trên 20 tài liệu mẫu, tự sửa 2 trường hợp biên").
- `mission1_brief.md`, what to submit: "Nhật ký Bằng chứng (công cụ AI, prompt, quyết định)".
  So the organizer names four fields across the two files: tool, prompt, decision, verification.
- `rules.md`: "Làm chủ > Hoàn hảo" and "Không có tiêu chí ẩn."

Public search found nothing about how the organizer grades the log.
`portal.agentlize.dev` is not indexed, and "Nhật ký bằng chứng" with Appota returns no public results (competition lane, negative result).
The only public material is the program's job postings, which stress real problems and working prototypes.

## 2. How the log is likely used in judging (inference)

This section is my reading of the rules above, not a published rubric.

1. **Compliance gate.** Any undeclared AI use costs 30% of the score.
   Over-declaring costs nothing, so the safe side is clear.
2. **Hallucination gate.** An obvious unverified AI hallucination fails the criterion it touches.
   The log is where a judge looks to see whether a fact was checked.
3. **Evidence for the three scored criteria.** "Không có tiêu chí ẩn" means the log has no score of its own.
   Its value is how it supports Thực thi (does it really run?), Chất lượng quyết định (A over B), and Khung vấn đề.
   A longer log earns nothing by itself.
4. **Question map for PITCH.** A judge who wants to test ownership will pick the parts the log says AI wrote and ask the candidate to explain or rebuild them.
   The log tells the judge where to probe, so every part it attributes to AI must be one the candidate can defend.

## 3. What outside practice converges on

All sources below were opened and quoted, except those marked [snippet only].

| Source | What it says | Lesson for the log |
|---|---|---|
| Hello Interview, interviewer interviews on AI-enabled coding rounds (Meta, Shopify, Canva and others) | Four things graded: approach, "Control over the AI", "Verification habits", communication. "We don't want the AI making decisions. We want to see you making decisions and using the AI to execute them." At Canva the interviewer asks "what does this code do?" after each generation. | Show that you set the approach and AI executed it; show checks after each step, not one check at the end. |
| Linux kernel, "Kernel Guidelines for Tool-Generated Content" | Disclose "What tools were used?", "If code was largely generated from a single or short set of prompts, include those prompts. For longer sessions, include a summary of the prompts and the nature of resulting assistance.", "Which portions of the content were affected", "How is the submission tested". "You are expected to understand and to be able to defend everything you submit." | Ready-made rule for agentic sessions: verbatim prompts when few, a prompt summary when many. Name affected files and the test. |
| Linux kernel, "AI Coding Assistants" | Only a human signs off and takes "full responsibility". Step 8: "Indicate what could not be done. If the fix could not be built or tested ... say so explicitly". | A "what I could not verify" section is expected good practice, not a weakness. |
| Ghostty `AI_POLICY.md` | "state the tool you used ... along with the extent that the work was AI-assisted". "If you can't explain what your changes do ... without the aid of AI tools, do not contribute". "AI is very good at being overly verbose and including noise ... Humans must do their research and trim this down." | State the extent per part. Trim the log; verbosity reads as unreviewed AI output. |
| Apache RAI, commit messages for AI-assisted code (unofficial draft) | "Explain what AI did and what you did." "The commit message is your representation." Example: "The function signature and connection logic were drafted by the AI; error handling and integration were written manually." "Don't over-annotate." | Split each part into AI-drafted and human-written, in one sentence. |
| ETHGlobal ETHOnline 2026 rules | "specifying which parts of the code, specific files, or assets were generated or assisted by AI". For spec-driven work: "include all spec files, prompts, and planning artifacts ... Judges need to see the full picture of how you directed the AI, not just the generated output." | Map AI use to files. Specs, `AGENTS.md` and plans are evidence of direction. |
| MLH hackathon rules template | "be clear on what you made and what was generated ... we want to see what you created/changed/built on". Not crediting AI means disqualification. | Same split, same penalty logic as this competition. |
| Stanford CS230 AI policy for project reports | AI Disclosure section "Must identify the AI tools used" and "describe the specific tasks for which each tool was used". Deductions for "Hallucinated or fabricated citations", "Unverified or incorrect code", "AI-generated content that has not been appropriately checked". | The deductions mirror this competition's hallucination rule. |
| Charles Sturt University, AI-integrated assessments | Three "transparency artefacts": a one-paragraph AI-use statement, a "Verification log (table): claim → source → check → result → citation", and a prompt appendix. Marks for how well students "verify facts, distinguish AI vs human work". | Closest published model to this log: summary statement, claim table, prompt appendix. |
| Microsoft Research, Lee et al., CHI 2025 (319 knowledge workers) | "higher confidence in GenAI is associated with less critical thinking". GenAI "shifts the nature of critical thinking toward information verification, response integration, and task stewardship." | Verification and integration are the skills to make visible. |
| Anthropic AI Fluency framework (Dakan, Feller, Anthropic; CC BY-NC-SA 4.0) | Delegation "deciding whether, when and how to engage with AI"; Description; Discernment "Accurately assessing the usefulness of AI outputs"; Diligence "Taking responsibility for what we do with AI and how we do it." | Useful as a checklist: does the log show each of the four? |
| Anthropic candidate AI guidance | "Use AI to refine your ideas, not replace them." "Be transparent." | Same stance as this competition. |
| Simon Willison, Claude Code transcripts (25/12/2025) | Transcripts "capture extremely important context ... what I asked for, what Claude suggested, decisions I made". | Exported session transcripts are a credible appendix. |
| Monash University, AI acknowledgement [snippet only] | Asks what output was "altered, adopted, integrated or built upon" and recommends keeping prompts, outputs and drafts. | Kept / changed / rejected per entry. |
| TEQSA, criteria and standards for gen AI use [snippet only] | The content of an AI acknowledgement should not affect marks, unless responsible AI use is itself a learning outcome; then descriptors can assess model choice, prompts and use of outputs. | This competition makes AI use an outcome ("bạn trở thành ai khi có AI"), so the log's content probably does count. |

The common core across all of them:

1. Name tool and model.
2. Say what AI did and what the human did, part by part.
3. Show how the output was checked.
4. Take responsibility.
5. Say what was not checked.

What sets the better examples apart: verification tied to specific claims, concrete human corrections, mapping to files or sections, and concision.

## 4. Subagent claims that did not hold up

- "Stanford CS230 10-point rubric, 2 points each for declaration, process evidence, ownership, verification, responsible use": not on the page; the page has the disclosure rule and the list of deductions only.
- "TEQSA Excellent / Competent / Limited descriptors requiring verbatim prompts": not found; the page could not be opened, and a search summary of it says roughly the opposite (section 3).
- "Monash: retained / changed / rejected": Monash's wording is "altered, adopted, integrated or built upon" [snippet only].
- "ETHGlobal penalizes large single commits or missing histories": not seen in the opened rules text; not used.
- The "hiring" lane returned nothing (Agnes rate limit); its angle is covered by the Hello Interview, Microsoft and Anthropic sources above.

## 5. The submitted Mission 1 log measured against this

Strengths worth keeping:

- Verbatim prompts with a Vietnamese gist, and a "Quyết định của tôi" field on every entry.
- A list of rejections of AI (A4) and of AI errors caught (A5), with entry numbers.
- Honest corrections of its own past overclaims (entries 20 and 37).
- Tools, models and times taken from session files, not from AI memory.

Gaps:

- Length: 28 pages and 16,850 words, against the organizer's three one-line examples.
  The summary signals are there but buried.
- The A1 responsibility statement shipped as a template, "[Hiệp tự viết, 4-6 câu, rồi xoá khung gợi ý này.]"; a judge reading for ownership sees an unfinished AI scaffold at the top.
- Verification is mostly by AI: 45 entry labels `[AI]` against 11 `[Tôi]`, and 15 `[Chưa]` marks.
  A judge can read this as AI checking AI.
- Internal codes (F1, M18, RV10) need a legend before the log is readable.

## 6. Recommended design for the Mission 2 log

Mission 2 builds code, so verification can be executable.
That is the biggest chance to improve on Mission 1.

### 6.1 Summary layer (at most 2 pages, the part judges read)

1. **Tuyên bố trách nhiệm**, written by Hiep without an AI draft, in his own words.
2. **Công cụ**: tool, model, what for, entries.
   Separate the AI used to build the submission from the LLM inside the product, so neither is mistaken for undeclared use.
3. **Nguồn gốc theo thành phần**, one row per part of v1 (data, rule engine, retriever, prompt, answer cards, UI, tests):
   who designed it, what AI drafted, what Hiep wrote or changed, how it was checked, and the command to reproduce the check.
   This follows the organizer's Cursor example and the kernel's "which portions" question.
4. **Kiểm chứng khẳng định**: every number or claim in the Mission 2 submission, with how it was checked, the result, who checked it, and the command.
   This is the CSU verification table, and the direct defence against the hallucination rule.
5. **Bác bỏ và lỗi của AI**: the concrete cases, each with the commit that fixed it.
   This is the strongest evidence of "control over the AI".
6. **Chưa làm được, chưa kiểm**: following the kernel's step 8.

### 6.2 Entry layer

- Use the organizer's format, about 5 lines per entry: tool and model, task, prompt, output with files and commit, decision (kept, changed or rejected), and check.
- Prompts follow the kernel rule: verbatim when a few prompts shaped the result; for long agent sessions, a summary of the prompts.
  Exported transcripts are not part of the submission for now (section 7, decision 3).
- Link entries to commit hashes.
  This gives provenance without `Assisted-by` trailers, which fits Hiep's rule against agent co-author lines in commits.

### 6.3 Practices specific to code

- **The human owns the test oracle.** The expected outcomes in `data/` tests are fixed and checked by Hiep before AI writes the code.
  If AI writes both the code and the expected values, the tests verify nothing independent.
  Log any change to an expected value, with the reason.
- **Hiep runs the final checks himself** (tests, the persona demo, any eval) and records the output with date and time; only these become `[Tôi]`.
- **Numbers only from runs**, each with its command and date; no estimated metrics.
- **Scrub secrets** (API keys, tokens) from any log excerpt.

### 6.4 Process during Mission 2

- Write the entry at the end of each session from `tools/ai_sessions.py`, and fill "Quyết định của tôi" immediately.
- Keep the AI-error list as errors happen; it cannot be rebuilt reliably afterwards.
- Before submitting: no template text left, no `[Chưa]` on any claim that appears in the submission, every session accounted for, and Hiep has read the summary layer end to end.

## 7. Decisions (Hiep, 12/10/2026)

1. Length budget: accepted, at most 2 pages of summary plus compact entries.
2. Rebuild drill for the core rules: not now; documentation for each part can come later.
   Parked under "Deferred ideas" in `docs/mission1/playbook.md`.
3. Exported transcripts in the submission: not now; focus on what the judge sees first, and reconsider when the project is finished.
   Parked under "Deferred ideas" in `docs/mission1/playbook.md`.
4. `tools/ai_sessions.py` does not list subagent models or web-search providers: tracked as GitHub issue #1.
   Until it is done, check subagent models and search providers by hand at the end of each session.

## Sources

- Competition: `docs/competition/ai_policies.md`, `rules.md`, `mission1_brief.md`.
- Hello Interview, "Introduction to AI-Enabled Coding Interviews": https://www.hellointerview.com/learn/ai-coding/overview/introduction
- Linux kernel, "Kernel Guidelines for Tool-Generated Content": https://cdn.kernel.org/doc/html/latest/process/generated-content.html
- Linux kernel, "AI Coding Assistants": https://docs.kernel.org/process/coding-assistants.html
- Ghostty AI policy: https://github.com/ghostty-org/ghostty/blob/main/AI_POLICY.md
- Apache RAI, "Commit messages for AI-assisted code" (unofficial draft): https://rai.apache.org/commit-messages.html
- ETHGlobal ETHOnline 2026 rules: https://ethglobal.com/events/ethonline2026/info/details
- MLH hackathon rules template: https://github.com/MLH/mlh-hackathon-organizer-guide/blob/master/general-information/judging-and-submissions/rules-for-your-hackathon.md
- Stanford CS230 AI policy: https://web.stanford.edu/class/cs230/
- Charles Sturt University, AI-integrated assessments: https://libguides.csu.edu.au/information-and-digital-literacies-glo/ai-assessments
- Lee et al., CHI 2025: https://www.microsoft.com/en-us/research/publication/the-impact-of-generative-ai-on-critical-thinking-self-reported-reductions-in-cognitive-effort-and-confidence-effects-from-a-survey-of-knowledge-workers/
- Anthropic AI Fluency framework: https://www-cdn.anthropic.com/b383cf6baddbfc72fdf8b0ed533a518e2872d531.pdf
- Anthropic candidate AI guidance: https://www.anthropic.com/candidate-ai-guidance
- Simon Willison, Claude Code transcripts: https://simonwillison.net/2025/Dec/25/claude-code-transcripts/
- Monash [snippet only]: https://www.monash.edu/student-academic-success/ai-hub/acknowledging-the-use-of-ai
- TEQSA [snippet only]: https://www.teqsa.gov.au/guides-resources/protecting-academic-integrity/academic-integrity-toolkit/risks-academic-integrity-ai/principles-criteria-and-standards-assessment-gen-ai-use
- Subagent reports (full text, including sources not used here): Pi subagent artifacts of run `2f3caa51`, files `competition.md`, `frameworks.md`, `engineering.md`.
