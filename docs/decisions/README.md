# Decisions

One file per decision, from Mission 2 on.
Each file records the context, the options, the choice, the reasons and who decided.
Mission 1 decisions stay in `docs/mission1/redraft/decisions.md` (frozen); an ADR that changes one names its old ID under "Supersedes".

## When to write one

Write an ADR when at least one of these holds:

- A real alternative was considered and rejected.
- It changes or reverses an earlier decision, including a Mission 1 ID such as M1a.
- A judge could ask "why A over B" about it in the PITCH round.

Anything smaller is a line in the PR, not an ADR.

## How

1. Copy `template.md` to `NNNN-short-title.md`, using the next free number.
2. Fill it in; one sentence per line.
   If research fed the decision, link the write-up in `docs/research/`; the ADR and the write-up land in the same PR, which closes the research issue.
3. Add a row to the index below.
4. When a later ADR replaces this one, set this one's status to "Superseded by NNNN"; do not delete or rewrite it.

The ADRs whose "Supersedes" names a Mission 1 ID are the raw material for Mission 2 mandatory question 2 (what changed since the Mission 1 plan, and why).

## Index

| No. | Title | Status | Supersedes |
|---|---|---|---|
| [0001](0001-langchain-core-with-own-retrieval.md) | Build steps 5-6 on LangChain core, with our own Vietnamese BM25 and fusion | Accepted | None |
| [0002](0002-syllable-bm25-gemini-001-rrf.md) | Hybrid retrieval: syllable BM25 of our own, gemini-embedding-001 and RRF, for now | Accepted | None |
| [0003](0003-gemini-38-flash-enum-citations-quote-check.md) | Step 6 on gemini-3.8-flash at low thinking, citing only retrieved ids, with a quote that step 7 checks | Accepted | None |
| [0004](0004-render-free-singapore-no-bao-sai.md) | Demo on a Render free web service in Singapore; "Báo sai" and the owners' page out of scope for Mission 2 | Accepted | Mission 1 P1, P2 and the "Báo sai" button in C2 |
| [0005](0005-conflict-card-quotes-per-side-without-meaning.md) | The conflict card quotes one clause per side, chosen without reading meaning | Proposed | None |
