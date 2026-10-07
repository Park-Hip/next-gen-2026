# Mission 1 - What is judged and how to do it well

Sources: `docs/competition/mission1_brief.md` and `docs/competition/rules.md`, reread on 07/10/2026.

## Submission facts

Three parts are submitted (brief, "Nộp gì cho mission 1"), and no code is required:

1. A PDF/DOCX or a Notion link, at most 5 pages, covering the 5 sections only.
2. The 3 mandatory "Forced Decision" answers, in a separate submission section, not in the PDF.
3. The evidence log: AI tools, prompts, and decisions.

Notes:

- The evidence log is a deliverable that judges read, not just a compliance file.
  It must show the candidate's own decisions, not only what the AI produced.
- The 3 answers are "khuyến nghị 60-150 từ" (recommended, not a hard limit), and must be "ngắn gọn, rõ quyết định và lý do".
- Tables, diagrams and illustrations are allowed.
- Deadline: 2 days from opening, no extensions, the system locks automatically.
- Submission channel: follow HR/Appota instructions.

## What the judges say they value (direct quotes)

| Quote | Source | What it means for us |
|---|---|---|
| "Không kỳ vọng một tài liệu hoàn hảo. Hãy ưu tiên chất lượng tư duy, khả năng lựa chọn và lý do đằng sau những quyết định của bạn." | Brief | Fewer points, each with full reasoning. Coverage is not rewarded. |
| "Trước khi xây sản phẩm, hãy chứng minh rằng bạn hiểu đúng vấn đề cần giải quyết." | Brief | Mission 1 is mainly about the problem, not the architecture. |
| "Hiểu đúng vấn đề, biết ưu tiên và thiết kế hướng giải quyết." | Brief | Three skills: understand, prioritise, design. |
| "Làm chủ > Hoàn hảo ... Vòng PITCH sẽ lộ ra." | Rules | Every line must be something the candidate can defend aloud. |
| "40% Khung vấn đề (Problem Framing) - bạn có hiểu đúng vấn đề không?, 35% Thực thi (giải pháp có chạy thật không?), 25% Chất lượng quyết định (lý do chọn A thay vì B có thuyết phục không?)." | Brief, Mission 1 scoring | See the mapping below. |
| "Không có tiêu chí ẩn." | Rules | Optimise for these three criteria and nothing else. |

## How the scoring maps to Mission 1

| Criterion | Weight | Judge's question | Where it shows | What "good" looks like |
|---|---|---|---|---|
| Khung vấn đề | 40% | "Bạn có hiểu đúng vấn đề không?" | Section 1, answer 1, and the "why" in every other section | A non-obvious diagnosis, shown with a concrete failure, not asserted |
| Thực thi | 35% | "Giải pháp có chạy thật không?" | Sections 2 and 5, answer 2 | No code is required, so this means credibility: a flow concrete enough to trace by hand, data and rules specific enough to build, a 3-day plan that a student can really finish, and tests that would prove it works |
| Chất lượng quyết định | 25% | "Lý do chọn A thay vì B có thuyết phục không?" | Sections 3-4, answers 2-3, and the evidence log | Every key decision names both A and B, why A wins, what A costs, and what would make B win |

How to earn "Thực thi" without code:

- Trace one real question through the flow, showing which simulated document drops out at each step and why.
- Show a small sample of the simulated data (one document's metadata, one persona) so the design is clearly buildable.
- Make the 3-day plan specific enough to start on day 1 without further design.
- Promise nothing that cannot be built in Mission 2.

## What a "deep" point looks like

Every important claim should carry this chain:

1. **Claim:** what we decided.
2. **Why:** the reasoning, tied to the problem diagnosis.
3. **Alternative:** the strongest option we rejected, and why it loses.
4. **Cost:** what we give up, stated honestly.
5. **Flip condition:** what evidence would make us change our mind.
6. **Test:** how Mission 2 would check it.

A point that cannot fill this chain is either obvious or not ours, and should be cut or reduced to one line.

## Diagnosis of the first draft

- It covered about 9 decisions and 6 risks in tables with one-line reasons, so none of them were argued.
- Several "decisions" are not real choices for this problem (RAG vs fine-tune, web vs chat tool), so they dilute the important ones.
- Section 1 asserts that naive RAG fails but never shows it failing on a concrete question.
- The metrics (95%, 25%, < 15 s) have no stated reason.
- The risks list mitigations but not how each failure would actually happen.
- Much of the content came from the playbook's checklist rather than from the candidate's own reasoning, which is a PITCH risk.

## Principles for the rewrite

- One running example (Minh asking about leave) carries the whole document.
- Each section has one central claim, argued fully, plus only short supporting lines.
- Pick about 3 decisions to argue in depth; mention the rest in one line or drop them.
- Show failure before solution: what goes wrong without the design, step by step.
- Every number gets a reason, or is removed.
- Use the space freed by moving the 3 answers out of the PDF for depth, not for more items.
