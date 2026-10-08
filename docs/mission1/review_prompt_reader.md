# Review prompt: a new reader reads the 5-page document

## Purpose

An AI reviewer reads the Phase 5 document as someone who has never seen this project.
It reports what is hard to understand, what a reader would dispute, where the document contradicts itself, how to make it easier to read, and whether it meets the competition brief.
It does not rewrite the document: Hiep revises it in his own words.

`review_prompt.md` is the earlier pre-redraft review and is kept as history.

## How to use

1. Render the current draft: `python tools/render_pdf.py docs/mission1/document.md build/mission1_draft.pdf`.
2. Open a new chat with no history, preferably on a different model family from the one that drafted the document (GPT or Gemini), so the review is independent.
3. Attach only these files:
   - `build/mission1_draft.pdf` - the document as the judges will see it.
   - `docs/competition/mission1_brief.md` - the official brief.
   - `docs/competition/rules.md` - the competition rules.
4. Do not attach `decisions.md`, `artifacts.md`, `playbook.md`, `criteria.md` or the evidence log.
   A new reader has none of them, and they would fill the gaps the review is meant to find.
5. Paste everything below the line.
   Add any optional modules from the end of this file that you want, before "Rules for your review".
6. Save the output to `docs/mission1/redraft/review_reader_output.md`, and log the tool, model and prompt in `evidence_log.md`.

---

## Prompt

You are reading a competition submission for the first time.
You have never seen this project, its notes, or any earlier draft.
You are a Vietnamese professional who reads product documents for a living: you understand software and AI in general, but you are not an expert in the candidate's design.
Read like a busy judge, and report honestly where you got lost, where you disagreed, and where you had to guess.

### What you are reading

- `mission1_draft.pdf`: a document of at most 5 pages, written in Vietnamese, submitted to Mission 1 of the Appota NextGen AI Talent 2026 program.
- `mission1_brief.md` and `rules.md`: the official brief and rules for that mission.

Do not open the brief or the rules until Part 4.
Parts 1-3 must reflect what the document alone communicates.

### Part 1 - Cold read

Read the document once, from start to finish, at normal speed.

1. **First half page.** After reading only the title and the opening box, write in 2-3 sentences what you think the document proposes and why.
2. **Teach-back.** For each of the 5 sections, explain its main point in your own words, in at most 3 sentences, as if telling a colleague.
   Where you cannot, say so: that is a finding, not a failure on your part.
3. **Where attention dropped.** Name the places where you started skimming, re-read a passage, or lost track of who or what was being discussed.

### Part 2 - Hard to understand

List every passage that is hard to understand.
For each item give:

- the exact Vietnamese quote and its section;
- the type of problem: undefined or unexplained term, term used inconsistently, sentence too long or too dense, unnatural Vietnamese (for example a phrase that reads like a translation from English), missing context (who, what, or why), example that does not clearly support the point, or a table or diagram that is hard to read;
- what you understood, and what you think the author meant, if different;
- severity: **High** (a judge would misunderstand a key idea), **Medium** (slows the reader down), **Low** (minor friction).

**Needs more explanation.**
Separately, list the places that read smoothly but leave a careful reader asking "why?" or "how?".
Look for:

- a claim or decision stated without its reason;
- a mechanism or rule named but not shown working (what goes in, what comes out, for whom);
- a jump in reasoning, where a step between two sentences is missing;
- a number, threshold or example given without saying where it comes from or what it shows;
- an important idea mentioned only once and never connected to the rest.

For each item, quote it, write the question a judge would ask, and say how much more is needed: one sentence, one example, or a full paragraph.
Also name any passage that explains more than a reader needs, so space can be moved to where it is short.

Then list the terms a reader must learn to follow the document (for example "phạm vi tìm kiếm", "dùng thay", "naive RAG").
For each, say whether it is defined, where, and whether the definition is clear enough.

### Part 3 - Controversial points and conflicts

**Controversial points.**
List the claims and decisions that a reasonable expert or judge could dispute.
For each: quote it, give the strongest counterargument in 1-3 sentences, and say whether the document already answers that counterargument (quote where) or leaves it open.
Include claims that are stated as obvious but are really a choice.

**Conflicts.**
List every place where the document contradicts itself or could be read as contradicting itself:

- between sections (for example, something promised in one section and contradicted or missing in another);
- between the text and a table, diagram or example card;
- between numbers (counts, dates, days, thresholds);
- a term that means different things in different places.

For each conflict, quote both sides and say which one you think is wrong, or that you cannot tell.

### Part 4 - Match against the brief and rules

Now read `mission1_brief.md` and `rules.md`.

1. Make a table of every requirement and every question the brief asks of the document, including:
   the format (PDF/DOCX/Notion, at most 5 pages, simulated data rather than real Appota data);
   each of the 5 sections and every question listed under it;
   the core question of the challenge;
   and the three scoring criteria with their weights.
   For each row, give: where the document answers it (section and a short quote), and a verdict: **Met**, **Partly met**, or **Missing**, with one sentence of reason.
2. Name anything in the document that the brief did not ask for and that takes space without serving a requirement.
3. For each scoring criterion, say which parts of the document earn it and what is weakest.

### Part 5 - How to make it easier to read and understand

Give concrete changes, ordered by how much they would help a first-time reader.
They can be about order, structure, splitting or merging paragraphs, what to turn into a table or diagram (or back into prose), what to define earlier, what to cut, and how to phrase things more naturally in Vietnamese.
For each change, say what it fixes from Parts 1-3.
You may show at most one example phrasing per change, labelled "ví dụ", to make the direction clear; do not rewrite whole paragraphs.
Respect the 5-page limit: if a change adds text, say what could be removed to make room.

### Part 6 - Summary

1. The 5 most important problems, ranked, each with its part number; include the most important gaps from "Needs more explanation".
2. What works well and should be kept, quoted, so the revision does not lose it.
3. In one sentence: after reading, what would a judge remember about this document?

### Rules for your review

- Be direct and specific.
  Praise only when it tells the author what to keep.
- Quote the exact Vietnamese text you comment on, so the author can find it.
- Label every finding: **[Brief]** if it comes from a requirement in the brief or rules, **[Reader]** if it comes from your experience reading the document, **[Opinion]** if it is your own judgment about what would be better.
- Do not invent facts about Appota, its companies or its policies, and do not assume the document's data is real: it is stated to be simulated.
- If something is ambiguous, say what you assumed.
- Answer in English, keeping Vietnamese quotes as they are.

---

## Optional modules

Paste any of these before "Rules for your review" if you want the extra checks.

### Optional A - Claims that need evidence

List every factual claim, number and statistic in the document (for example dates, counts, thresholds, confidence figures).
For each, say whether the document shows where it comes from, whether it looks correct, and mark it "confident correct", "unsure" or "likely wrong".
Do not guess: say "unsure" when you are unsure.
Flag any sentence that presents a prediction or an assumption as if it had been measured.

### Optional B - Are the decisions real choices?

For each decision the document argues, say whether the rejected option is a real alternative that a competent team might choose, or a weak option set up to lose.
Say whether the document states what the chosen option costs and what evidence would make the author switch.

### Optional C - Can it be built?

The next mission is to build a first version, alone, in a few days.
Flag anything the document promises or implies that would not fit that, and anything left too vague to start building from.

### Optional D - Questions a judge would ask

The author must defend every line aloud in a later pitch round.
List the 8 hardest questions a judge would ask after reading this document, most likely first.
For each, say what a strong answer must contain, without writing the answer.

### Optional E - Layout and visuals

Look at the PDF as a page, not only as text.
Report pages that look too dense or too empty, tables or diagrams whose text is too small or badly broken across pages, and anything that looks unfinished (for example a placeholder).
