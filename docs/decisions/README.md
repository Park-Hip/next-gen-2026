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
| [0003](0003-gemini-38-flash-enum-citations-quote-check.md) | Step 6 on gemini-3.8-flash at low thinking, citing only retrieved ids, with a quote that step 7 checks | Accepted; Model line superseded by 0008, `text` field by 0009, prompt rules by 0011 | None |
| [0004](0004-render-free-singapore-no-bao-sai.md) | Demo on a Render free web service in Singapore; "Báo sai" and the owners' page out of scope for Mission 2 | Accepted | Mission 1 P1, P2 and the "Báo sai" button in C2 |
| [0005](0005-conflict-card-quotes-per-side-without-meaning.md) | The conflict card quotes one clause per side, chosen without reading meaning | Accepted | None |
| [0006](0006-own-harness-one-run-main-wording.md) | Evaluate with our own harness: one run per case, main wording only, unsafe answers judged on the card and on the raw reply | Accepted | Mission 1 V4, the 3 phrasings of A2 and V1, and the "Evaluation" line of ADR 0003 |
| [0007](0007-defer-context-recall.md) | Context recall is deferred until we have real documents | Accepted | The "context recall" row of Mission 1 V1 and RV13 |
| [0008](0008-gemini-35-flash-lite-at-medium.md) | Step 6 on gemini-3.5-flash-lite at medium thinking | Accepted | The "Model" line of ADR 0003 |
| [0009](0009-answer-card-shows-the-verified-quote.md) | The answer card shows the quote that step 7 verified, not the model's sentence | Superseded by 0011 | The `text` field of ADR 0003 and the answer line wording of Mission 1 C2 |
| [0010](0010-access-never-decides-precedence.md) | Access is the last filter: a document the asker may not read still replaces its series | Accepted | The order of step 2 and step 3 (M3b, M12) for a restricted overriding document; R3 and R4 |
| [0011](0011-answer-card-shows-the-models-sentence-above-the-verified-quote.md) | The answer card shows the model's sentence above the verified quote | Accepted; Reasons pending Hiep; run 20261021-1032 is reference only | ADR 0009 and the prompt rules of ADR 0003 |
| [0013](0013-owners-change-a-document-only-by-a-full-new-version.md) | Owners change a document only by publishing a full new version | Accepted | None; confirms and extends Mission 1 M1a |
| [0014](0014-the-model-may-add-a-conflict-never-remove-one.md) | The model may add a conflict it reads in the text, never remove one | Proposed | The "Deferred" row on an AI conflict check in `docs/scope.md`; "no conflict detection at question time" in SD14 |
| [0015](0015-a-document-that-applies-to-a-unit-must-be-readable-by-it.md) | A document that applies to a unit must be readable by everyone in that unit | Accepted | None; records the case ADR 0010 leaves open as an owner rule |
| [0016](0016-simulated-sign-in.md) | A simulated sign-in decides who is asking: pick an account and type one shared demo password | Accepted; Reasons pending Hiep | The persona-picker mechanism of Mission 1 D4 and the B3 line that names it |
