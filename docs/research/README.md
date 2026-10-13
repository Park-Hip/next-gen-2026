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
| - | Build the RAG with a framework or with our own modules? | #4 | ADR 0001 | Open |
| - | Hybrid retrieval for Vietnamese | #5 | ADR 0002 | Open |
| - | Which LLM, and how to make it answer only from the chunks, cite and refuse | #6 | ADR 0003 | Open |
| - | Web UI and free hosting for the public demo | #7 | ADR 0004 | Open |
| - | How to evaluate a small RAG | #8 | ADR 0006 | Open |

Earlier research, kept where it was written: `docs/mission2/evidence_log_research.md` (how to write the evidence log, 10/10/2026).
