# Decisions

An ADR (decision record) is a short note about one design decision: the problem, the options, the choice and why.
Each one opens with an "In short" summary in plain words, so it can be read without knowing the code.
Code names, file paths and issue numbers are collected at the end, under "Technical detail".

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
   Start with "In short" (the problem, the decision, what the employee sees, what we give up), in plain words with no code names or IDs.
   Write the rest for a reader who does not know the code, and put function and field names, file paths, test names and issue, PR, gap and promise IDs in "Technical detail" at the end.
   If research fed the decision, link the write-up in `docs/research/`; the ADR and the write-up land in the same PR, which closes the research issue.
3. Add a row to the index below.
4. When a later ADR replaces this one, set this one's status to "Superseded by NNNN"; do not delete or rewrite it.

The ADRs whose "Supersedes" names a Mission 1 ID are the raw material for Mission 2 mandatory question 2 (what changed since the Mission 1 plan, and why).

## Index

| No. | Title | What it decides | Status | Supersedes |
|---|---|---|---|---|
| [0001](0001-langchain-core-with-own-retrieval.md) | Build steps 5-6 on LangChain core, with our own Vietnamese BM25 and fusion | Use the widely used LangChain library for the AI model and the stored embeddings, but write our own Vietnamese keyword search and ranking merge, because LangChain's versions of those sit in packages that are retired or deprecated. | Accepted | None |
| [0002](0002-syllable-bm25-gemini-001-rrf.md) | Hybrid retrieval: syllable BM25 of our own, gemini-embedding-001 and RRF, for now | How the system finds the clauses that fit a question: keyword search on Vietnamese syllables plus a meaning-based search, merged into one ranking, and the five best clauses go to the AI; temporary until real documents arrive. | Accepted | None |
| [0003](0003-gemini-38-flash-enum-citations-quote-check.md) | Step 6 on gemini-3.8-flash at low thinking, citing only retrieved ids, with a quote that step 7 checks | The AI answers only from the clauses it is given, names the clauses it used and copies a word-for-word quote from each, which a fixed rule then checks; it also made the first choice of AI model, later replaced. | Accepted; Model line superseded by 0008, `text` field by 0009, prompt rules by 0011 | None |
| [0004](0004-render-free-singapore-no-bao-sai.md) | Demo on a Render free web service in Singapore; "Báo sai" and the owners' page out of scope for Mission 2 | The demo runs on a free Render web service in Singapore, which can take about a minute to wake up; the "Báo sai" (report an error) button and the owners' page are left out of Mission 2. | Accepted | Mission 1 P1, P2 and the "Báo sai" button in C2 |
| [0005](0005-conflict-card-quotes-per-side-without-meaning.md) | The conflict card quotes one clause per side, chosen without reading meaning | When two documents conflict, the conflict card quotes one clause from each, chosen by a fixed rule that does not read what the documents mean. | Accepted | None |
| [0006](0006-own-harness-one-run-main-wording.md) | Evaluate with our own harness: one run per case, main wording only, unsafe answers judged on the card and on the raw reply | How the product is tested: our own small test program, each question run once in its main wording, and an unsafe answer counted both on the card the employee sees and on the AI's raw reply. | Accepted | Mission 1 V4, the 3 phrasings of A2 and V1, and the "Evaluation" line of ADR 0003 |
| [0007](0007-defer-context-recall.md) | Context recall is deferred until we have real documents | Do not measure whether search finds the right clause (context recall) until real documents exist. | Accepted | The "context recall" row of Mission 1 V1 and RV13 |
| [0008](0008-gemini-35-flash-lite-at-medium.md) | Step 6 on gemini-3.5-flash-lite at medium thinking | The AI model is gemini-3.5-flash-lite at medium thinking, because the earlier model returned errors and its free quota was too small for a test run. | Accepted | The "Model" line of ADR 0003 |
| [0009](0009-answer-card-shows-the-verified-quote.md) | The answer card shows the quote that step 7 verified, not the model's sentence | The answer card showed only the quote that a rule had checked, not the AI's own sentence, because nothing checked that sentence; replaced by ADR 0011. | Superseded by 0011 | The `text` field of ADR 0003 and the answer line wording of Mission 1 C2 |
| [0010](0010-access-never-decides-precedence.md) | Access is the last filter: a document the asker may not read still replaces its series | Who may read a document never decides which rule applies: a restricted document still replaces the rule it overrides, and an employee who cannot read it is refused instead of being shown the old rule. | Accepted | The order of step 2 and step 3 (M3b, M12) for a restricted overriding document; R3 and R4 |
| [0011](0011-answer-card-shows-the-models-sentence-above-the-verified-quote.md) | The answer card shows the model's sentence above the verified quote | The answer card shows one plain sentence written by the AI above the exact quote and its source; the sentence is not checked while the product runs, and Hiep reads it afterwards. | Accepted; point contract and card layout partly superseded by 0018; Reasons pending Hiep; run 20261021-1032 is reference only | ADR 0009 and the prompt rules of ADR 0003 |
| [0012](0012-the-card-tells-the-asker-when-a-version-ends-and-what-replaces-it.md) | The card tells the asker when a version ends and what replaces it | The card tells the asker until when a rule applies to them and what replaces it, so a question about next year no longer gets this year's answer without a warning. | Proposed; Reasons pending Hiep | Mission 1 M8, for published versions |
| [0013](0013-owners-change-a-document-only-by-a-full-new-version.md) | Owners change a document only by publishing a full new version | An owner never changes a single clause alone: any change is a new version of the whole document, so no unchanged clause is lost. | Accepted | None; confirms and extends Mission 1 M1a |
| [0014](0014-the-model-may-add-a-conflict-never-remove-one.md) | The model may add a conflict it reads in the text, never remove one | The AI may flag two clauses from different documents that disagree, and fixed rules check the flag and add a conflict card; the AI can never remove a conflict or change a refusal. | Proposed | The "Deferred" row on an AI conflict check in `docs/scope.md`; "no conflict detection at question time" in SD14 |
| [0015](0015-a-document-that-applies-to-a-unit-must-be-readable-by-it.md) | A document that applies to a unit must be readable by everyone in that unit | A document that applies to a unit must be readable by everyone in that unit, and a role-only document must not share a topic with a policy for everyone; the system does not fix an owner's mistake here. | Accepted | None; records the case ADR 0010 leaves open as an owner rule |
| [0016](0016-simulated-sign-in.md) | A simulated sign-in decides who is asking: pick an account and type one shared demo password | A simulated sign-in decides who is asking: the visitor picks an account and types one shared demo password, and the judge account alone opens the data and test-case pages. | Accepted; Reasons pending Hiep | The persona-picker mechanism of Mission 1 D4 and the B3 line that names it |
| [0017](0017-a-refusal-says-why-and-an-answer-says-what-it-does-not-cover.md) | A refusal says why, and an answer says what it does not cover | A refusal says why (nothing found, answer could not be checked, or system error), and an answer says which part of the question it does not cover; "not allowed" and "not found" still read the same. | Proposed; Reasons pending Hiep | The refusal wording of Mission 1 Phần 2 (C4) for `quote_mismatch`, `outside_retrieved` and `malformed`; R10 is kept |
| [0018](0018-one-answer-per-question-above-the-verified-quotes.md) | One answer per question, above the verified quotes | The AI writes one answer that covers every part of the question, above the exact quotes that the rules checked; the quotes are the only text checked while the product runs, and Hiep reads the answer afterwards. | Accepted; Reasons pending Hiep | ADR 0011's point contract and answer card layout |
