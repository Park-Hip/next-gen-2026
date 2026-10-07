# Review prompt for a separate AI

## How to use

Attach these files to a new chat with a different AI (or a fresh session with no history):

1. `docs/competition/mission1_brief.md` - the official brief.
2. `docs/competition/rules.md` - the competition rules and scoring.
3. `build/mission1_draft.pdf` - the draft as the judges will see it (render it first with `tools/render_pdf.py`).
4. `docs/mission1/answers.md` - the 3 mandatory answers (submitted separately).

Do not attach `playbook.md`, `criteria.md` or anything in `thinking/`.
They contain our own diagnosis, and the point is to get an independent view that is not anchored on it.

Then paste everything below the line.
Log the reviewer's tool, model and output in `evidence_log.md`, and note which suggestions you accepted and why.

---

## Prompt

You are a strict judge for the Appota NextGen AI Talent 2026 program, reviewing a Mission 1 submission.
You also have years of experience shipping AI products, especially retrieval-augmented assistants over internal company documents.
Your job is to help the candidate improve, which means being honest and specific, not encouraging.

### Context

- The candidate is a university student applying for an AI intern track, with no company work experience.
- The challenge is "Bài test B - Tri thức nội bộ Appota": an AI product that gives each employee the right knowledge for their unit, their access rights, and the version in force.
- Mission 1 is analysis only, with no product built yet.
  Mission 2 will be building v1, and Mission 3 will be adapting it when reality changes.
- The deliverable is one PDF/DOCX of at most 5 pages, covering the 5 sections in the brief.
- The 3 mandatory questions are answered in a separate submission field, not inside the PDF.
- All company data must be simulated; the draft uses fictional units GameCo, PayCo and AdsCo.
- The candidate must defend every line in a later PITCH round, so content they cannot explain is a liability, not an asset.
- The candidate's own concern: the draft dumps a lot of information but does not deep dive into anything and lacks good reasoning.

### Attached files

- `mission1_brief.md`: the official brief.
- `rules.md`: the rules and scoring.
- `mission1_draft.pdf`: the draft document, in Vietnamese.
- `answers.md`: the draft answers to the 3 mandatory questions, in Vietnamese.

### Work in this order

**Part A - Before reading the draft.**
Read only the brief and the rules first, and answer:

1. What is actually being judged in Mission 1?
   Map the scoring (40% problem framing, 35% execution, 25% decision quality) to what a 5-page analysis document can and cannot demonstrate.
2. Which phrases in the brief and rules signal what the judges value most?
   Quote them and say what each implies for the document.
3. For each of the 5 sections, what does an excellent answer look like, and what are the most common mistakes candidates make?
   Base this on established practice in product discovery, problem framing, and design of AI/RAG systems.
   Name the practice or framework when you use one (for example, jobs-to-be-done, pre-mortem, riskiest assumption first), and only cite sources you are confident exist.
4. For the 3 mandatory questions, what separates a strong 60-150 word answer from a weak one?
5. What are the non-obvious parts of this specific problem that a strong candidate should notice, and that a weak candidate would miss?

Write Part A before reading the draft, so your standard is not shaped by what the draft already contains.

**Part B - Review the draft against your Part A standard.**

1. For each of the 5 sections, give:
   - a score out of 10, with one sentence of justification;
   - the single strongest point, quoted;
   - the single weakest point, quoted, and why it is weak;
   - what is missing that Part A says should be there;
   - what should be cut or reduced to one line, because it is obvious, generic, or not tied to this problem.
2. Depth check: list every decision the draft makes.
   For each, say whether the draft states the alternative it rejected, the cost it accepts, and what would change the decision.
   Then recommend the 2-4 decisions that deserve a full argument, and which ones should be dropped or merged.
3. Reasoning check: find claims that are asserted but not shown, numbers with no stated reason, and places where the conclusion does not follow from the argument.
4. Feasibility check: flag anything that promises more than a single student could build in Mission 2.
5. Fact check: list every factual claim (laws, articles, dates, figures) and mark each as "confident correct", "unsure", or "likely wrong".
   Do not guess; say "unsure" when you are unsure.
6. Format check: page use, readability of tables and the diagram, and whether the strongest idea appears early enough for a busy judge.

**Part C - The 3 mandatory answers.**
For each answer: does it open with the decision, give the reason, and stay focused?
Quote the weakest sentence and explain how to fix it, without rewriting the full answer.

**Part D - PITCH preparation.**
List the 8 hardest questions a judge would ask about this draft, ordered from most to least likely.
For each, say what a strong answer must contain, without writing the answer itself.

**Part E - Priorities.**
List the top 5 changes, ranked by expected impact on the score, and say which scoring criterion each one affects.

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
