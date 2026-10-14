# Research

One write-up per question, from Mission 2 on.
A write-up gathers options and sources so Hiep can decide; it is AI work unless it says otherwise, and it is never the decision.
The decision and Hiep's reasons go into an ADR in `docs/decisions/`.

## How

1. Open an issue with the "Research" form (label `research`): the question, the ADR it feeds, the options already known, done when.
2. Hiep runs the research with his own agent (decision D15, 12/10/2026).
3. The results are filed as `NNNN-short-title.md` from `template.md`, with the tool, model and verbatim prompt under "Method".
4. Hiep opens the sources behind the option he picks, then states his decision and reasons.
5. The write-up and the ADR land in one PR that says `Closes #<issue>`; Hiep ticks "Hiệp's check" and merges.
6. Add a row to the index below.

A claim that could not be checked against its source goes under "Claims that did not hold up" or is marked unverified; it never reaches an ADR as fact.

## Index

| No. | Question | Issue | Feeds | Status |
|---|---|---|---|---|
| [0001](0001-rag-framework-or-own-modules.md) | Build the RAG with a framework or with our own modules? | #4 | ADR 0001 | Decided: option C (ADR 0001) |
| [0002](0002-hybrid-retrieval-for-vietnamese.md) | How should v1 do hybrid search over Vietnamese policy text? | #5 | ADR 0002 | Decided, temporary for synthetic data (ADR 0002) |
| [0003](0003-llm-grounded-answers-citations-refusal.md) | Which LLM, and how to make it answer only from the chunks, cite and refuse | #6 | ADR 0003 | Decided: AI recommendation as it stands (ADR 0003) |
| [0004](0004-free-host-for-the-demo.md) | Which free host should serve the public demo? (stack chosen by Hiep: FastAPI + Jinja2) | #7 | ADR 0004 | Decided: Render free in Singapore, no pinger, "Báo sai" and the owners' page out of scope (ADR 0004) |
| [0005](0005-how-to-evaluate-a-small-rag.md) | How should v1 evaluate the AI steps: our own harness or a library? | #8 | ADR 0006 | Decided: AI recommendation without spot repeats; one run per case and main wording only by Hiep (ADR 0006) |

Earlier research, kept where it was written: `docs/mission2/evidence_log_research.md` (how to write the evidence log, 10/10/2026).
