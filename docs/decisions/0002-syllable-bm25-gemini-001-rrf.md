# 0002. Hybrid retrieval: syllable BM25 of our own, gemini-embedding-001 and RRF, for now

- Status: Accepted
- Date: 2026-10-13
- Origin: AI, accepted
- Supersedes: None (keeps `gemini-embedding-001` from plan decision D2)
- Issue: #5
- Research: `docs/research/0002-hybrid-retrieval-for-vietnamese.md`

## In short

- **The problem:** When Minh asks about his annual leave, the system must find the right clauses among those he may use.
  Vietnamese is written in space-separated syllables, so there is no single obvious way to split text into words, and no real Appota documents exist yet to test on.
- **The decision:** Search two ways and merge the results.
  A keyword search of our own that matches syllables, and a search by meaning with Google's `gemini-embedding-001`, merged by reciprocal rank fusion (RRF); the 5 best clauses go to the AI.
  This is a temporary choice, made on simulated data.
- **What the employee sees:** Nothing directly, but a question typed without Vietnamese accents will mostly match nothing by keyword.
- **What we give up:** The choices rest on 25 simulated clauses and a stand-in model, not on Gemini or real documents, so they must be re-measured when real documents arrive.

## Context

ADR 0001 left four choices for step 5, the hybrid search inside the asker's scope: how to split text for the keyword search, which BM25 code to use (BM25 is a standard keyword-ranking formula), which embedding model to use (a model that turns text into numbers so that similar meanings are found), and how to fuse the two rankings.
Vietnamese writes words as space-separated syllables, so a keyword index can use syllables or a word segmenter.
The research measured the options on our simulated data ("giả lập"): 25 clauses, scopes of 2 to 11 clauses, and 21 question wordings, 12 of them written by Claude for the measurement.
No Gemini API key was available, so the embedding and fusion measurements used a small local stand-in model, not Gemini.
Real Appota documents will be longer, more numerous and worded differently, so these results may not hold for them.

## Options considered

1. **Word splitting** - syllables (chosen); word segmentation with underthesea; pyvi; VnCoreNLP.
2. **BM25 code** - our own code with Lucene's IDF (chosen); bm25s; rank_bm25.
3. **Embedding model** - `gemini-embedding-001` (chosen); `gemini-embedding-2`; a small local model; a Vietnamese bi-encoder.
4. **Fusion** - reciprocal rank fusion with k = 60 (chosen); weighted score combination; no retrieval, the whole scope to the AI.

## Decision

Version 1 uses these four choices, as a temporary decision for our synthetic data:

- **Word splitting:** the text is normalised (NFC, so that accented letters have one form) and lowercased, then split into syllables with their accents kept.
  Each clause is indexed with its document title in front of its text, for both the keyword and the meaning-based search.
  Accents are not folded away.
- **Keyword search:** our own BM25 code with Lucene's IDF `log(1 + (N - df + 0.5) / (df + 0.5))`, k1 = 1.2, b = 0.75, with the statistics computed over the asker's scope only.
- **Meaning-based search:** `gemini-embedding-001` through LangChain's Gemini embeddings, at its default 3,072 dimensions, with LangChain's default task types (`RETRIEVAL_DOCUMENT`, `RETRIEVAL_QUERY`).
- **Fusion:** reciprocal rank fusion with k = 60 over the full keyword and meaning-based rankings of the scope; the top 5 clauses go to the AI, with no score threshold and no reranker.

## Reasons

Hiep took the research's recommendation as it stands, and set it as temporary: it was chosen on synthetic data and will be revisited when we see real documents (Hiep, 13/10/2026).

The comparison behind the recommendation is Claude's, in the research write-up under "AI recommendation", not Hiep's reasoning.

## Consequences

Drafted by Claude from the research; approved by Hiep on 13/10/2026, including `numpy` as a dependency.

- No new dependency for the word splitting or the keyword search: both are standard-library Python.
- The build needs `numpy` (a numbers library): the in-memory store of ADR 0001 raises an error at search time without it, and neither LangChain core nor its Gemini connector installs it.
- Scope-only statistics mean that keyword scores for the same clause differ between askers.
  Nothing relies on comparing them, since there is no score threshold.
- Refusal ("không tìm thấy") stays with the AI and the step 7 check, because no keyword score separated unanswerable questions from answerable ones.
- Questions typed without accents will mostly match nothing by keyword; this is outside the v1 promises.
- `gemini-embedding-001` shuts down on 14/05/2028.
  Moving to `gemini-embedding-2` means re-embedding all clauses, and first checking how it handles the `task_type` that LangChain sends.
- Not yet measured: Gemini's meaning-based ranking on our wordings, and so whether RRF with equal weights helps or hurts the keyword ranking.

## Would change if

Drafted by Claude from Hiep's "revisit with real documents"; approved by Hiep on 13/10/2026.

- Real documents arrive: rerun the research measurements on them before keeping any of the four choices.
- The Gemini measurement shows a meaning-based ranking as weak as the stand-in's: weight the keyword search above it in RRF, or reconsider the fusion.
- Test cases or real questions show word-segmentation errors costing less than syllable-by-syllable matching, for example on longer documents.
- `gemini-embedding-2` is shown to work correctly through LangChain's Gemini connector.
- Scopes grow well beyond the top 5, so that the cut-off starts dropping the right clause.

## Evidence

The research write-up above, with measurements M1 to M4 and their scripts.
Evidence log line of 13/10/2026 (Claude Opus 5.5 with Agnes 2.5 Flash subagents).

## Technical detail

- Tokenizer: NFC, lowercase, syllables with diacritics kept; the chunk text is prefixed with its document title for BM25 and for embeddings.
  Code: `src/appota_kb/services/retrieval/bm25.py`.
- BM25: Lucene IDF `log(1 + (N - df + 0.5) / (df + 0.5))`, `bm25_k1: 1.2`, `bm25_b: 0.75`; N, df and average length come from the asker's scope only.
- Embeddings: `GoogleGenerativeAIEmbeddings` with `gemini-embedding-001` (`embedding_model` in `config.yaml`), 3,072 dimensions.
- Fusion: `rrf_k: 60`, `top_k: 5`, over the full BM25 and dense rankings.
- Rejected options by name: underthesea, pyvi, VnCoreNLP, bm25s, rank_bm25, `gemini-embedding-2`, a small local model, a Vietnamese bi-encoder, weighted score combination.
- Dependencies: `numpy` is required by `InMemoryVectorStore` at search time; the modules are built in #12.
- Plan decision D2 chose `gemini-embedding-001` as the working default; the original wording of the accents consequence cited Mission 1 item RV7 (the review item behind the hybrid retriever).
