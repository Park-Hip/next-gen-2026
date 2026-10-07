# Mission 1 - What is judged and how to do it well

Sources: `docs/competition/mission1_brief.md` and `docs/competition/rules.md`, reread on 07/10/2026.

## Submission facts

- The 5-page PDF/DOCX covers the 5 sections only.
- The 3 mandatory questions go in a separate submission section, not in the PDF.
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
| "40% Khung vấn đề, 35% Thực thi, 25% Chất lượng quyết định (lựa chọn bắt buộc). Không có tiêu chí ẩn." | Rules | See the mapping below. |

## How the scoring maps to Mission 1

| Criterion | Weight | Where it shows in the PDF | What "good" looks like |
|---|---|---|---|
| Khung vấn đề | 40% | Section 1, and the "why" in every other section | A non-obvious diagnosis, shown with a concrete failure, not asserted |
| Thực thi | 35% | Mostly Missions 2-3; in Mission 1, Section 5 | A plan that is realistic in 3 days and clearly testable |
| Chất lượng quyết định | 25% | Sections 3-4, and the MVP cuts in Section 5 | Real choices between real options, with costs accepted and a condition that would change the decision |

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
