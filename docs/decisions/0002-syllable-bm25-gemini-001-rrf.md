# 0002. Hybrid retrieval: syllable BM25 of our own, gemini-embedding-001 and RRF, for now

- Status: Accepted
- Date: 2026-10-13
- Origin: AI, accepted
- Supersedes: None (keeps `gemini-embedding-001` from plan decision D2)
- Issue: #5
- Research: `docs/research/0002-hybrid-retrieval-for-vietnamese.md`

## Context

ADR 0001 left four choices for step 5, the hybrid search inside the asker's scope: the keyword tokenizer, the BM25 code, the embedding model and the fusion.
Vietnamese writes words as space-separated syllables, so a keyword index can use syllables or a word segmenter.
The research measured the options on our simulated data ("giả lập"): 25 chunks, scopes of 2 to 11 chunks, and 21 question wordings, 12 of them written by Claude for the measurement.
No Gemini API key was available, so the embedding and fusion measurements used a small local stand-in model, not Gemini.
Real Appota documents will be longer, more numerous and worded differently, so these results may not hold for them.

## Options considered

1. **Tokenizer** - syllables (chosen); word segmentation with underthesea; pyvi; VnCoreNLP.
2. **BM25** - our own code with Lucene's IDF (chosen); bm25s; rank_bm25.
3. **Embedding model** - `gemini-embedding-001` (chosen); `gemini-embedding-2`; a small local model; a Vietnamese bi-encoder.
4. **Fusion** - reciprocal rank fusion with k = 60 (chosen); weighted score combination; no retrieval, the whole scope to the LLM.

## Decision

v1 uses, as a temporary decision for our synthetic data:

- **Tokenizer:** NFC, lowercase, syllables with diacritics kept; each chunk is indexed with its document title in front of its text, for both BM25 and embeddings.
  No diacritic folding.
- **BM25:** our own code with Lucene's IDF `log(1 + (N - df + 0.5) / (df + 0.5))`, k1 = 1.2, b = 0.75, with the statistics computed over the asker's scope only.
- **Embeddings:** `gemini-embedding-001` through `GoogleGenerativeAIEmbeddings`, at its default 3,072 dimensions, with LangChain's default task types (`RETRIEVAL_DOCUMENT`, `RETRIEVAL_QUERY`).
- **Fusion:** reciprocal rank fusion with k = 60 over the full BM25 and dense rankings of the scope; the top 5 chunks go to the LLM, with no score threshold and no reranker.

## Reasons

Hiep took the research's recommendation as it stands, and set it as temporary: it was chosen on synthetic data and will be revisited when we see real documents (Hiep, 13/10/2026).

The comparison behind the recommendation is Claude's, in the research write-up under "AI recommendation", not Hiep's reasoning.

## Consequences

Drafted by Claude from the research; approved by Hiep on 13/10/2026, including `numpy` as a dependency.

- No new dependency for the tokenizer or BM25: both are standard-library Python in #12.
- #12 needs `numpy`: `InMemoryVectorStore` (ADR 0001) raises an error at search time without it, and neither `langchain-core` nor `langchain-google-genai` installs it.
- Scope-only statistics mean BM25 scores for the same chunk differ between askers; nothing relies on comparing them, since there is no score threshold.
- Refusal ("không tìm thấy") stays with the LLM and the step 7 check, because no BM25 score separated unanswerable questions from answerable ones.
- Questions typed without diacritics will mostly match nothing by keyword; this is outside the v1 promises (RV7).
- `gemini-embedding-001` shuts down on 14/05/2028; moving to `gemini-embedding-2` means re-embedding all chunks, and first checking how it handles the `task_type` that LangChain sends.
- Not yet measured: Gemini's dense ranking on our wordings, and so whether RRF with equal weights helps or hurts the BM25 ranking.

## Would change if

Drafted by Claude from Hiep's "revisit with real documents"; approved by Hiep on 13/10/2026.

- Real documents arrive: rerun the research measurements on them before keeping any of the four choices.
- The Gemini measurement shows a dense ranking as weak as the stand-in's: weight BM25 above dense in RRF, or reconsider the fusion.
- Test cases or real questions show segmentation errors costing less than syllable-by-syllable matching, for example on longer documents.
- `gemini-embedding-2` is shown to work correctly through `langchain-google-genai`.
- Scopes grow well beyond the top 5, so that the cut-off starts dropping the right clause.

## Evidence

The research write-up above, with measurements M1 to M4 and their scripts.
Evidence log line of 13/10/2026 (Claude Opus 5.5 with Agnes 2.5 Flash subagents).
