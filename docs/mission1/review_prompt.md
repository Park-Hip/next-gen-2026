# Review prompt for a separate AI

## Purpose

This review comes before the redraft, not after it.
The current draft was written before the Mission 1 scoring criteria were published, and it will be rewritten.
The review should set an independent standard, decide what in the draft is worth keeping, and give a blueprint for the redraft.
It should not polish wording that is about to be replaced.

## How to use

Attach these files to a new chat with a different AI (or a fresh session with no history):

1. `docs/competition/mission1_brief.md` - the official brief, including the Mission 1 scoring and submission requirements.
2. `docs/competition/rules.md` - the competition rules.
3. `build/mission1_draft.pdf` - the current draft as the judges would see it (render it first with `tools/render_pdf.py`).
4. `docs/mission1/answers.md` - the 3 mandatory answers (submitted separately).
5. `evidence_log.md` - the evidence log (also submitted).

Do not attach `playbook.md`, `criteria.md` or anything in `thinking/`.
They contain our own diagnosis, and the point is to get an independent view that is not anchored on it.

Then paste everything below the line.
Log the reviewer's tool, model and output in `evidence_log.md`, and note which suggestions you accepted and why.

---

## Prompt

You are a strict judge for the Appota NextGen AI Talent 2026 program.
You also have years of experience shipping AI products, especially retrieval-augmented assistants over internal company documents.
Your job is to help the candidate improve, which means being honest and specific, not encouraging.

### Context

- The candidate is a university student applying for an AI intern track, with no company work experience.
- The challenge is "Bài test B - Tri thức nội bộ Appota": an AI product that gives each employee the right knowledge for their unit, their access rights, and the version in force.
- Mission 1 is analysis only, with no product built yet.
  Mission 2 will be building v1, and Mission 3 will be adapting it when reality changes.
- Three parts are submitted, and no code is required:
  a PDF/DOCX or Notion link of at most 5 pages covering the 5 sections;
  the 3 mandatory "Forced Decision" answers, in a separate field;
  and an evidence log of AI tools, prompts, and decisions.
- Mission 1 scoring:
  40% Khung vấn đề ("bạn có hiểu đúng vấn đề không?"),
  35% Thực thi ("giải pháp có chạy thật không?"),
  25% Chất lượng quyết định ("lý do chọn A thay vì B có thuyết phục không?").
- All company data must be simulated; the draft uses fictional units GameCo, PayCo and AdsCo.
- The candidate must defend every line in a later PITCH round, so content they cannot explain is a liability, not an asset.

### Where the candidate is

- The current draft was written before the scoring criteria above were published.
- The candidate will rewrite the PDF after this review, in their own words, and wants your review to guide that rewrite.
- The candidate's own diagnosis: the draft dumps a lot of information but does not deep dive into anything and lacks good reasoning.
  Test this diagnosis; do not just accept it.
- Do not spend effort on wording, typos or small layout issues in the PDF; that text will be replaced.

### Attached files

- `mission1_brief.md`: the official brief.
- `rules.md`: the rules.
- `mission1_draft.pdf`: the current draft, in Vietnamese.
- `answers.md`: the draft answers to the 3 mandatory questions, in Vietnamese.
- `evidence_log.md`: the evidence log, in Vietnamese.

### Work in this order

**Part A - The standard, written before reading the draft.**
Read only the brief and the rules first, and answer:

1. For each of the three scoring criteria, what would a top-scoring submission show, and what can a no-code submission realistically demonstrate?
   Be concrete about "giải pháp có chạy thật không?": what evidence, inside a 5-page analysis, convinces a judge that the solution would actually work?
2. Which phrases in the brief and rules signal what the judges value most?
   Quote them and say what each implies.
3. For each of the 5 sections, what does an excellent answer look like, and what are the most common mistakes?
   Base this on established practice in product discovery, problem framing, and design of AI/RAG systems.
   Name the practice or framework when you use one (for example, jobs-to-be-done, pre-mortem, riskiest assumption first), and only cite sources you are confident exist.
4. What makes an "A instead of B" argument convincing to a judge, and what makes one look like a fake choice?
5. What are the non-obvious parts of this specific problem that a strong candidate should notice, and that a weak candidate would miss?

Write Part A before reading the draft, so your standard is not shaped by what the draft already contains.

**Part B - Verdict on the current draft.**

1. For each of the 5 sections, give:
   - a score out of 10 against your Part A standard, with one sentence of justification;
   - **Keep:** the ideas worth carrying into the redraft, quoted;
   - **Deepen:** the ideas that are right but only asserted, and what argument or evidence they need;
   - **Cut:** what is obvious, generic, or not tied to this problem;
   - **Missing:** what Part A says should be there and is not.
2. Decision check: list every decision the draft makes, and for each say whether it is a real choice or a fake one.
   For the real ones, say whether the draft names B, explains why A wins, states what A costs, and says what would make B win.
3. Reasoning check: list claims that are asserted but not shown, numbers with no stated reason, and conclusions that do not follow from the argument.
4. Feasibility check: flag anything that promises more than a single student could build in Mission 2.
5. Fact check: list every factual claim (laws, articles, dates, figures) and mark each as "confident correct", "unsure", or "likely wrong".
   Do not guess; say "unsure" when you are unsure.

**Part C - Blueprint for the redraft.**
Give a structure the candidate can write from, without writing the text yourself:

1. For each of the 5 sections: the one central claim it should argue, its page budget out of 5, and the supporting evidence it needs.
2. The 2-4 decisions that deserve a full "A instead of B" argument, and why those ones.
   For each, name A and B and the kind of reasoning that would make it convincing, but leave the reasoning to the candidate.
3. The concrete artifacts that would earn "Thực thi" without code (for example, a worked trace of one question, a sample of simulated data, test cases), and where each should go.
4. What should open page 1, so a judge who reads only the first half page understands the candidate's diagnosis.
5. Which scoring criterion each section mainly serves, so the 40/35/25 weighting is reflected in how the pages are spent.

**Part D - The 3 mandatory answers.**
For each answer: does it open with the decision, give the reason, and stay focused?
Is it consistent with the blueprint in Part C, or will it need to change after the redraft?
Quote the weakest sentence and explain how to fix it, without rewriting the answer.

**Part E - The evidence log.**
Does it make clear which decisions are the candidate's own and which came from AI, and how each AI output was verified?
List what a judge would find missing or unconvincing.

**Part F - PITCH preparation.**
List the 8 hardest questions a judge would ask about this submission, ordered from most to least likely.
For each, say what a strong answer must contain, without writing the answer itself.

**Part G - Priorities.**
List the top 5 changes for the redraft, ranked by expected impact on the score, and say which scoring criterion each one affects.

### Rules for your review

- Be blunt.
  Do not praise unless it helps the candidate understand what to keep.
- Quote the exact Vietnamese text you are commenting on, so the candidate can find it.
- Separate three kinds of feedback, and label each item:
  **[Brief]** for a requirement stated in the brief or rules,
  **[Practice]** for established good practice,
  **[Opinion]** for your own judgment.
- Do not rewrite the document or the answers.
  Point out problems and directions; the candidate must write the fixes in their own words.
- Do not invent facts about Appota, its subsidiaries, or its internal policies.
- If something in the files is ambiguous, say what you assumed.
- Answer in English, keeping Vietnamese quotes as they are.
