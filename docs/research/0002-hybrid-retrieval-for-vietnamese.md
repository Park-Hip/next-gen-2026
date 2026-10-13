# 0002. How should v1 do hybrid search (keyword plus embedding) over Vietnamese policy text?

- Status: Draft
- Issue: #5
- Feeds: ADR 0002
- Method: Pi on 13/10/2026, 11:39-14:15.
  Orchestrator: Claude Opus 5.5 (`claude-bridge/claude-opus-5-5`), which wrote the lane prompts, ran the measurements and checked the sources.
  Web research: four `researcher` subagents on Agnes 2.5 Flash with max reasoning (`agnes/agnes-2.5-flash:max`), run in two pairs.
  The first two lanes ("tokenize", "embed") failed after about 3 minutes with "Request timed out" during a network outage on this machine; they were relaunched with the same prompts and all four lanes finished.
  Search providers: the `web_search` tool's configured provider; the failed runs' logs name Exa and OpenAI.
  Claude then opened every source in the table below itself (page fetch, curl of official pages and PDFs, PyPI JSON API, GitHub raw files, or installed package source), with no other model involved.
  No Gemini API key was available in the session, so Gemini embeddings were not measured on our data (see "Not measured").
  Hiep's prompts to Claude and the four lane prompts follow verbatim.

```text
Hiep to Claude:
research this issue research R2, when needed use Agnes max reasoning level for web search.
(later, after the outage: "continue", then "resume")

Shared context, sent at the top of each lane:
You are researching one technical decision for a small Python RAG prototype. Today is 2026-10-13.

Project: v1 of an internal-policy assistant, built in about one day inside a 3-day competition. Python, FastAPI + Jinja2, hosted on Render's free web service (512 MB RAM). LangChain core 1.x with langchain-google-genai is already chosen for the Gemini chat model, embeddings and InMemoryVectorStore; BM25 and fusion are our own code.
Data: about 10 simulated Vietnamese HR policy documents in Markdown, chunked by article ('Dieu'), so roughly 30-40 chunks in total; deterministic rules first restrict each asker to about 10 chunks (their allowed scope), and retrieval only ever scores chunks inside that scope.
Questions are short Vietnamese questions in three phrasings: as written in the document, a paraphrase, and spoken style ('van noi'), for example 'Phep nam cua toi la bao nhieu ngay?', 'Nam nay toi duoc nghi may ngay?', 'Em duoc off may ngay phep mot nam?' (with Vietnamese diacritics in the real data).
Decision: how to do hybrid retrieval (keyword BM25 plus embeddings, then fusion) for Vietnamese at this tiny scale. Working default: our own BM25 over Vietnamese syllables with diacritics kept, gemini-embedding-001, reciprocal rank fusion.

Rules for your work:
- Use web_search, then OPEN each page you cite with fetch_content. Prefer official docs, official repos, PyPI, Hugging Face model cards, papers (arXiv, ACL Anthology) and first-party engineering blogs.
- Every claim needs: the claim, the URL, an exact quote copied from the opened page, and the date the page states (if any).
- If you only saw a search snippet, mark the claim [snippet only]. If you could not find something, say so; never guess numbers.
- Do not write any files. Return your report as your final message.
- Output format: (1) a short summary of findings, (2) a Markdown table: Claim | URL | Exact quote | Page date, (3) a list 'Could not verify'.

Your lane:

The four lanes:
Lane "tokenize":
Keyword tokenization of Vietnamese for BM25.
1. Syllable tokens (split on whitespace and punctuation, lowercase, diacritics kept) versus word segmentation (Vietnamese words are often two or more syllables, e.g. 'nghi phep', 'lam them gio'). Find published retrieval results (papers, shared tasks such as Zalo AI 2021 legal text retrieval, ALQAC, Vietnamese MS MARCO / mMARCO, VN-MTEB, Vietnamese legal retrieval papers) that compare BM25 on syllables versus segmented words, or syllable bigrams; give the numbers and the dataset.
2. Word segmentation libraries: underthesea, pyvi, VnCoreNLP (py_vncorenlp, Java), and any newer ones. For each: latest version and release date on PyPI, license, required dependencies (read the dependency list on PyPI or in the repo), whether it needs Java or downloads a model, any published accuracy and speed, and any reported install size or memory.
3. Unicode issues: NFC versus NFD composed and decomposed Vietnamese characters, and old versus new tone-mark placement (for example 'hoa' with the tone on o or on a, 'thuy'), and how retrieval systems normalize them. Cite official docs or well-known libraries that handle it.
4. Spoken style and informal Vietnamese: words without diacritics, teencode, English loanwords such as 'off', abbreviations like 'ko', 'dc'. What do Vietnamese search or RAG systems do about it (diacritic restoration, synonym lists, relying on embeddings)?
5. Vietnamese stopword lists (source, size) and whether removing stopwords helps BM25 on short queries.

Lane "embed":
Embedding models for Vietnamese retrieval, for a host with 512 MB RAM.
1. Google's gemini-embedding-001 (and any newer Gemini embedding model released by October 2026): model ids, status (GA or preview, deprecation dates), dimensions and output_dimensionality (Matryoshka), task_type values such as RETRIEVAL_QUERY and RETRIEVAL_DOCUMENT, max input tokens, free-tier rate limits (requests per minute, per day) from ai.google.dev, price, whether free-tier data is used to improve Google's products, and its MMTEB / MTEB Multilingual score.
2. Vietnamese retrieval benchmarks: VN-MTEB (or ViMTEB), MTEB/MMTEB Vietnamese tasks, Zalo legal retrieval, and the scores of gemini-embedding-001, OpenAI text-embedding-3-small/large, intfloat/multilingual-e5 (small, base, large), BAAI/bge-m3, Alibaba gte-multilingual, Qwen3-Embedding (0.6B), and Vietnamese bi-encoders (bkai-foundation-models/vietnamese-bi-encoder, AITeamVN/Vietnamese_Embedding, dangvantuan/vietnamese-embedding, hiieu/halong_embedding, or others). Note which Vietnamese models expect word-segmented input (pyvi) and their licenses.
3. Running a local model on 512 MB RAM: parameter counts, model file sizes, and any published RAM usage for multilingual-e5-small, bge-m3, and ONNX runtimes (fastembed, sentence-transformers with onnx backend); whether torch alone exceeds 512 MB.
4. Paraphrase and informal-language robustness: any evidence that multilingual embeddings match colloquial or diacritic-less Vietnamese queries to formal text.
5. Precomputing document embeddings at build time and storing them, so only the query is embedded at request time: any guidance or caveats (model version pinning, same task_type).

Lane "bm25":
BM25 implementations and their behaviour on a tiny corpus (about 10 chunks per asker).
1. rank_bm25 (dorianbrown/rank_bm25) and bm25s (xhluca/bm25s): latest version and release date on PyPI, last commit date, license, required dependencies, variants offered (Okapi, BM25L, BM25+, ATIRE, Lucene), default k1 and b and epsilon, and how each computes IDF.
2. Known problems with tiny corpora: negative or zeroed IDF for terms that appear in more than half the documents (the Robertson-Sparck Jones IDF), rank_bm25's epsilon floor, Lucene's log(1 + ...) IDF that is always positive. Find the GitHub issues, the source lines, and articles that explain it.
3. Writing BM25 in plain Python: how many lines, references to the exact formula (Robertson and Zaragoza 2009 'The Probabilistic Relevance Framework: BM25 and Beyond', Lucene BM25Similarity docs), and recommended k1 and b for short documents.
4. Whether corpus statistics (IDF, average document length) should be computed over the whole collection or only over the filtered subset, and how Elasticsearch, OpenSearch, Lucene, Haystack or Weaviate handle filtered BM25 (statistics over the whole index or the filtered set).
5. How LangChain's own BM25Retriever (langchain-community, rank_bm25 underneath) and any maintained replacement in langchain-core or a partner package do it in 2026, given that langchain-community was sunset on 22 May 2026.

Lane "fusion":
Fusing BM25 and embedding results, and whether hybrid helps for Vietnamese at this scale.
1. Reciprocal rank fusion: the original paper (Cormack, Clarke and Buettcher, SIGIR 2009), the constant k=60 and why, and how Elasticsearch, OpenSearch, Weaviate, Qdrant, Azure AI Search, LangChain EnsembleRetriever and Haystack implement it (default k, weights, rank_window_size).
2. Score-based fusion: convex combination with min-max or z-score normalization, Weaviate relativeScoreFusion and alpha, Bruch, Gai and Ingber 2023 'An Analysis of Fusion Functions for Hybrid Retrieval' (ACM TOIS) and its findings on RRF versus convex combination, especially with few or no tuning queries.
3. Evidence that hybrid (BM25 plus dense) beats either alone for Vietnamese: papers or shared-task reports (Zalo AI 2021 legal retrieval, ALQAC, Vietnamese legal or medical RAG papers, VN-MTEB) with the numbers.
4. Tiny candidate sets: with only about 10 chunks in scope, guidance on top-k, on fusing full rankings versus top-k lists, on a minimum score or relevance cutoff so off-topic questions retrieve nothing, and on sending the whole scope to the LLM instead of retrieving (long-context versus RAG comparisons).
5. Optional reranking with a cross-encoder or an LLM (for example a Vietnamese reranker, bge-reranker-v2-m3, or Gemini as reranker), and its cost on a 512 MB host; whether it is worth it for 10 candidates.
```

## Why it matters for v1

The answer sets how #12 builds step 5: the tokenizer, the BM25 code, the embedding model and the fusion that pick the chunks the LLM sees.
It serves promises A1 (hybrid search only over the asker's scope) and A2 (also finds questions phrased differently, including "văn nói"), and must not weaken R8 (out-of-scope documents never enter retrieval).

Constraints any option must respect:

- ADR 0001: `langchain-core` and `langchain-google-genai` for the embeddings and `InMemoryVectorStore`; our own Vietnamese BM25 and fusion.
- The scope is small: 2 to 11 chunks per test case on our data (measured below), 25 chunks in all.
- Render free web service: 512 MB RAM.
- Hiep must be able to explain every part in PITCH.

The question splits into four choices: the keyword tokenizer, the BM25 implementation, the embedding model, and the fusion.

## Options found

### Tokenizer for BM25

| Option | What it is | Strengths | Costs and risks | Fit for v1 | Sources |
|---|---|---|---|---|---|
| T1. Syllables (working default) | NFC, lowercase, `re.findall(r"\w+", text)`; diacritics kept | No dependency; best BM25 ranking on our data (M3); nothing to mis-segment | Multi-syllable words are matched syllable by syllable | Good | M2, M3 |
| T2. Syllables plus syllable bigrams | T1 plus every adjacent pair joined | Rewards phrase matches; one line more | Ranked worse than T1 on our data (18/21 against 20/21 at rank 1) | Weak | M3 |
| T3. Word segmentation with underthesea 9.5.0 | `word_tokenize`, words joined by "_" | Maintained (17/05/2026), Apache-2.0, no Java (S2); the only published Vietnamese IR comparison found favours dictionary segmentation (S1) | Ranked worse than T1 on our data (16/21); segmentation errors on our text such as "gameco_tạo" and "hr_gameco" (M2); 25 packages and about 100 MB memory (M1) | Weak | S1, S2, M1-M3 |
| T4. Word segmentation with pyvi 0.1.1 | `ViTokenizer.tokenize` | MIT, no Java (S3) | Last release 30/06/2021 (S3); pulls scikit-learn and scipy, 212 MB, about 120 MB memory, 5.8 s import, a `SyntaxWarning` on Python 3.12 (M1); ranked like T3 (16/21) | Weak | S3, M1, M3 |
| T5. VnCoreNLP | Java toolkit with Python wrappers | Accurate segmenter (lane report) | Needs Java 1.8+, a 27 MB jar plus 115 MB of models, `-Xmx2g` in its examples, GPL-3.0 (S4) | Poor | S4 |

Two additions apply to any option:

- **Document title in front of each chunk** ("Quy chế nghỉ phép Tập đoàn. Điều 2. ..."): with T1 it put the target chunk first in all 21 wordings, against 20 without it (M3c).
  The one fix was row 3's informal wording "Em muốn off vài hôm thì đăng ký kiểu gì?", whose answer is the procedure document, which has no "Điều" lines.
- **Diacritic-folded copies of each syllable** ("nghỉ" also indexed as "nghi", "đ" as "d"): for questions typed without diacritics, T1 alone matched nothing in 8 of 9 wordings, while T1 plus folded copies put the target first in all 9 (M3).
  The Mission 1 design replaced the "không dấu" test phrasing with "văn nói" on Hiep's call (`current_design.md`, line 118), so this is outside the v1 promises.

### BM25 implementation

| Option | What it is | Strengths | Costs and risks | Fit for v1 | Sources |
|---|---|---|---|---|---|
| B1. Own code (working default) | About 20 lines: Lucene IDF `log(1 + (N - df + 0.5) / (df + 0.5))`, k1 = 1.2, b = 0.75, statistics over the asker's scope | IDF is never zero or negative (S5); 21/21 at rank 1 with titles (M3c); every line explainable | Our code to test | Good | S5, M3 |
| B2. rank_bm25 0.2.2 `BM25Okapi` | The library under LangChain's sunset `BM25Retriever` | Widely used | Last release 16/02/2022 (S7); its IDF goes negative when a term is in more than half the documents and is then floored to `epsilon * average_idf` (S6), which is itself negative when most terms are common: 13 of our 31 wordings had a scope with negative IDFs after the floor, and it ranked the target first in 16/21 (M3d) | Poor | S6, S7, M3d |
| B3. bm25s 0.3.13 | Maintained library (07/10/2026, MIT) with a `lucene` method (S8) | Same formula as B1 without writing it; fast on large corpora | One more dependency for 2-11 chunks, where speed does not matter; not measured on our data | Fair | S8 |

Statistics over the scope or over all 25 chunks gave the same rankings on our data (20/21 at rank 1 either way, M3b).
Lucene and Haystack keep statistics over the whole index and only use filters to choose which documents are scored (S5, S9).
Computing them over the scope means out-of-scope documents influence nothing, not even IDF, which is the most literal reading of R8.

### Embedding model

| Option | What it is | Strengths | Costs and risks | Fit for v1 | Sources |
|---|---|---|---|---|---|
| E1. `gemini-embedding-001` (working default) | Gemini API, text only, through `GoogleGenerativeAIEmbeddings` | Stable; `task_type` supported, and LangChain already sends `RETRIEVAL_DOCUMENT` for documents and `RETRIEVAL_QUERY` for queries (S10, S15); no local memory | Shutdown date 14/05/2028, replacement `gemini-embedding-2` (S11); 2,048 input tokens; no longer on the pricing page (S13); no published Vietnamese score (S17) | Good | S10, S11, S13, S15, S17 |
| E2. `gemini-embedding-2` | Gemini's current model, GA on 22/04/2026 (S12) | Recommended replacement, no shutdown date (S11); 8,192 input tokens; normalises truncated vectors itself (S10) | Does not support `task_type`; tasks go in a text prefix such as "task: search result \| query: ..." (S10), while `langchain-google-genai` 4.4.1 sends `task_type` by default and has no special case for this model (S15), so the combination is untested; free-tier content is "Used to improve our products" (S13); no published Vietnamese score | Fair until tested | S10-S13, S15 |
| E3. Small local model | For example `paraphrase-multilingual-MiniLM-L12-v2` (0.22 GB) through fastembed and ONNX | No API key or quota | 626 MB memory after loading on Windows, above Render's 512 MB (M4); it ranked the target first in only 9/21 wordings (M4) | Poor | S24, M4 |
| E4. Vietnamese bi-encoders | `bkai-foundation-models/vietnamese-bi-encoder`, `AITeamVN/Vietnamese_Embedding` and others | Strong on Vietnamese legal retrieval (S23) | bkai needs word segmentation first; AITeamVN is about 2.3 GB on disk (S23); either way a local model on a 512 MB host, as E3 | Poor | S23 |

The Gemini models' published score is MTEB (Multilingual) overall, for example 67.99 at 768 dimensions for `gemini-embedding-001` (S10).
The Vietnamese benchmarks found (VN-MTEB, S18, and a public VN-MTEB run of 19 models, S17) cover open models only, so no option above has a checked Vietnamese score.
The two Gemini models' vectors cannot be compared with each other, so switching later means re-embedding the 25 chunks (S10), which takes one batch call.

### Fusion and cut-off

| Option | What it is | Strengths | Costs and risks | Fit for v1 | Sources |
|---|---|---|---|---|---|
| F1. Reciprocal rank fusion, k = 60 (working default) | Score = sum of 1 / (60 + rank) over the BM25 and the dense ranking of the whole scope | No tuning; k = 60 "near-optimal, but ... not critical" in the original paper (S19); default in Elasticsearch (S21) and LangChain (`c: int = 60`, R1 S10) | With a weak dense ranker it pulled BM25's correct first place down: 13/21 at rank 1, but every target chunk stayed in the top 3 (M4); on a Vietnamese legal subset RRF also scored between BM25 and dense at rank 1 (S23) | Good | S19, S21, S23, M4 |
| F2. Weighted score combination | Normalise both scores to 0-1 and mix with a weight alpha, as Weaviate's default "Relative Score Fusion" (S22) | Beats RRF in Bruch et al. once alpha is tuned, and needs few tuning queries (S20) | Our only labelled questions are the test cases; tuning alpha on them would fit the test set | Fair | S20, S22 |
| F3. No retrieval: the whole scope goes to the LLM | Scopes hold at most 11 chunks | Simplest; nothing can be missed | Breaks promise A1; step 7 would check citations against the whole scope; more distractors for rows 6, 10, 13 (`forbidden_for_llm`) | Poor | Promises A1, R7 |

Cut-off and reranking, for any F option:

- **Top k:** scopes have 2-11 chunks (M3); in M4 every target chunk, including both chunks of each conflict pair, was in the RRF top 3.
- **No score threshold:** BM25 top scores of refusal rows (0.23 to 4.36) overlap those of answer rows (0.00 to 13.05), so no BM25 threshold separates "nothing relevant" from "relevant" (M3b); refusal stays with the LLM's "không tìm thấy" and step 7.
- **No reranker:** `bge-reranker-v2-m3` has 568M parameters and about 2.3 GB on disk (S23), far above 512 MB, for at most 11 candidates.

### Measured by Claude on 13/10/2026

These are measurements on this machine, not published figures.
Windows 11 and Python 3.12, while Render runs Linux, so memory figures are indicative only.
The data is `data/` on this branch (25 chunks: one per "Điều" line, one per line of the procedure document); each test case's scope comes from `adopted_rules.rulebook`.

**M1, install and memory cost.**
Each option in its own fresh virtual environment with `uv`; package counts include `psutil`, used for the measurement.

| Option | Packages | site-packages | Memory after import and first calls | Versions |
|---|---|---|---|---|
| T1 syllables | 0 extra | - | - | standard library |
| T3 underthesea | 25 | 52 MB | about 100 MB, 0.6 s import | underthesea 9.5.0, underthesea-core 3.3.2 |
| T4 pyvi | 14 | 212 MB | about 120 MB, 5.8 s import | pyvi 0.1.1, scikit-learn 1.9.1, scipy 1.18.1 |
| E3 fastembed + MiniLM-L12 | 31 | 131 MB, plus 241 MB model cache | 626 MB after loading the model | fastembed 0.9.0, onnxruntime 1.31.0 |

**M2, segmentation on our text.**
underthesea and pyvi gave the same tokens on 31 of the 35 distinct texts (chunk lines, some repeated across versions, and test-case questions).
Where they differ, each makes errors: underthesea joined "GameCo tạo" into `gameco_tạo` and "HR GameCo" into `hr_gameco`; pyvi split "giả lập" into two syllables.
Neither joined "nghỉ bù", "làm thêm" or "phép năm".

**M3, BM25 rankings inside each asker's scope.**
21 wordings: the 9 test-case wordings of the answer and conflict rows 1-5, 7 and 12, plus 12 extra paraphrase and "văn nói" wordings written by Claude for this measurement only (they are not test cases).
Row 15 is left out: its target clause is outside the scope, which is the known limitation.
"Rank 1" means the target clause (either clause of a conflict pair) came first.

| Tokenizer, Lucene IDF, chunk text only | Rank 1 | Top 3 |
|---|---|---|
| T1 syllables | 20/21 | 20/21 |
| T2 syllables + bigrams | 18/21 | 20/21 |
| T3 underthesea | 16/21 | 20/21 |
| T4 pyvi | 16/21 | 20/21 |
| T1 + folded copies | 20/21 | 20/21 |

With the Robertson-Sparck Jones IDF (which goes negative) instead of Lucene's, T1 dropped to 12/21 at rank 1.
M3b: statistics over the scope or over all 25 chunks, 20/21 either way.
M3c: T1 with the document title in front of each chunk, 21/21 at rank 1 and in the top 3.
M3d: rank_bm25 0.2.2 `BM25Okapi` with defaults on the same titled chunks, 16/21 at rank 1, against 21/21 for B1.

**M4, dense and fused rankings with a local stand-in model.**
`paraphrase-multilingual-MiniLM-L12-v2` through fastembed, cosine similarity, on the titled chunks; this is not Gemini and says nothing about Gemini's quality.

| Ranking | Rank 1 | Top 3 |
|---|---|---|
| BM25 (B1, T1, titles) | 21/21 | 21/21 |
| Dense (stand-in) | 9/21 | 16/21 |
| RRF, k = 60 | 13/21 | 21/21 |

### Not measured

- Gemini embeddings on our data: no API key in this session.
  The M4 script runs with `GoogleGenerativeAIEmbeddings` in place of fastembed (see the end), which would show whether Gemini's dense ranking helps or hurts the RRF result on our 21 wordings.
- Whether `gemini-embedding-2` accepts or rejects the `task_type` that `langchain-google-genai` sends.
- The Gemini free-tier rate limits for embeddings: the rate-limits page says they are per project and shown in AI Studio, without numbers (S14).

### A finding for ADR 0001

`InMemoryVectorStore` needs `numpy`, which neither `langchain-core` 1.6.10 nor `langchain-google-genai` 4.4.1 installs.
Without it, a search raises "cosine_similarity requires numpy to be installed" (S16).
With `numpy` installed, `filter=lambda d: d.metadata["doc"] == "A"` returned only the document in scope, so the scope filter works as ADR 0001 expects.
So #12 needs `numpy` as a pinned dependency, whichever option is chosen.

## Claims that did not hold up

1. **"Ho (EVIA 2007): syllables plus bigrams 0.3636"** (tokenize lane, which also named the author "D.T.P. Ho").
   The paper is by Ho Bao Quoc; 0.3636 is single syllables, bigrams are 0.3778, syllables plus dictionary segmentation 0.4989, dictionary segmentation alone 0.5625 (S1).
   It used the SMART vector model on a news collection, not BM25, so it does not transfer directly to our short clauses.
2. **"Gemini Embedding is about 47.23 on VN-MTEB retrieval"** (embed lane, marked as its inference).
   In the cited table 47.23 belongs to `google/embeddinggemma-300m`, an open model; no Gemini API model is in the table (S17).
   The tokenize lane gave the same 47.23 as a BM25 baseline on HotpotQA-VN, which was not checked and is not used.
3. **"`gemini-embedding-001` has no published deprecation date"** (embed lane).
   The deprecations page gives a shutdown date of 14/05/2028 (S11).
4. **"`gemini-embedding-001` costs $0.15 per 1M tokens, per the pricing page"** (embed lane).
   The current pricing page lists only `gemini-embedding-2` (free tier free of charge, paid $0.20 per 1M text tokens) (S13); $0.15 comes from the 2025 launch blog post.
5. **"Both Gemini models take 8K input tokens"** (embed lane).
   `gemini-embedding-001` takes 2,048; `gemini-embedding-2` takes 8,192 (S10).
6. **"multilingual-e5-small fits 512 MB with ONNX, at about 300-600 MB"** (embed lane, citing a third-party CLI page).
   Not checked for that model, but a smaller model of the same kind used 626 MB after loading here (M4).
7. **"ViLeXa: dense-only beat hybrid, Recall@10 0.950 against 0.937, MRR 0.842 against 0.650"** (fusion lane).
   The ViLeXa README reports one system (95.0% Recall@10, MRR 0.842) and no hybrid-against-dense comparison (S25).
8. **"Haystack's `InMemoryBM25Retriever` depends on rank_bm25 internally"** (BM25 lane).
   Haystack's document store implements the same BM25 variants in its own code and only links to rank_bm25 in a docstring (S9).

Not checked by Claude, so not used above: the lanes' numbers for OpenAI embeddings (a blog's 200-query Vietnamese test), the Hugging Face model card details of the Vietnamese bi-encoders, the Zalo AI 2021 F2 scores, the stopword lists, and the date `langchain-community`'s repository was archived.

## AI recommendation (not a decision)

Claude's pick, as one bundle for #12:

- Tokenizer: T1, syllables with diacritics kept, with each chunk's document title in front of its text for both BM25 and embeddings.
- BM25: B1, our own code with Lucene IDF, k1 = 1.2, b = 0.75, statistics over the asker's scope.
- Embeddings: E1, `gemini-embedding-001` at its default 3,072 dimensions, with LangChain's default task types.
- Fusion: F1, RRF with k = 60 over the full BM25 and dense rankings of the scope, the top 5 chunks sent to the LLM, no score threshold and no reranker.

One-line reason (Claude's): on our own data, plain syllables beat every segmenter and our 20-line BM25 beat the common library, while the Gemini choice keeps the one model LangChain already drives correctly, and RRF needs no tuning on a test set we must not tune on.
The strongest alternative is E2, `gemini-embedding-2`, if Hiep weighs Google's recommended model above an untested LangChain combination; a 10-minute test with a key would settle it.
Before the ADR, Claude suggests running M4 with Gemini (script below): if Gemini's dense ranking is as weak as the stand-in's, weighting BM25 above dense in RRF becomes a real alternative.

Questions for Hiep before the ADR: which option for each of the four choices, and in your own words why it beats the strongest alternative.

Hiep's answer (13/10/2026): take this recommendation, as a temporary decision for the synthetic data, to be revisited with real documents; recorded in ADR 0002.

## Sources

All accessed 2026-10-13 by Claude.
"Installed source" means the file in the package version named, installed from PyPI on that day.

| ID | Title and URL | Accessed | Quote that supports the claim |
|---|---|---|---|
| S1 | Ho Bao Quoc, Vietnamese Text Retrieval: Test Collection and First Experimentations, EVIA 2007, https://research.nii.ac.jp/ntcir/workshop/OnlineProceedings6/EVIA/17.pdf | 2026-10-13 | "The average precision 11-pt for this case is 0.3636" (single syllables); "the average precision is augmented to 0.3778" (bigrams); "The average precision for 11-ptr is 0.4989." (mixed); "The average precision for 11-pt is improved to 0.5625" (dictionary segmentation) |
| S2 | underthesea on PyPI, https://pypi.org/pypi/underthesea/json | 2026-10-13 | version 9.5.0, uploaded 2026-05-17, license "Apache-2.0", requires "Click>=6.0, tqdm, requests, joblib, PyYAML, underthesea_core>=3.3.0, huggingface-hub" |
| S3 | pyvi on PyPI, https://pypi.org/pypi/pyvi/json | 2026-10-13 | version 0.1.1, uploaded 2021-06-30, license "MIT", requires "scikit-learn, sklearn-crfsuite" |
| S4 | VnCoreNLP README and LICENSE, https://github.com/vncorenlp/VnCoreNLP | 2026-10-13 | "`Java 1.8+` (Prerequisite)"; "File `VnCoreNLP-1.2.jar` (27MB) and folder `models` (115MB)"; "java -Xmx2g -jar VnCoreNLP-1.2.jar"; "GNU General Public License as published by the Free Software Foundation, either version 3" |
| S5 | Lucene 9.9.0 BM25Similarity, https://lucene.apache.org/core/9_9_0/core/org/apache/lucene/search/similarities/BM25Similarity.html | 2026-10-13 | "`k1 = 1.2` * `b = 0.75`"; idf "Implemented as `log(1 + (docCount - docFreq + 0.5)/(docFreq + 0.5))`"; scorer: "Compute any collection-level weight (e.g. IDF, average document length, etc)" |
| S6 | rank_bm25 source, https://raw.githubusercontent.com/dorianbrown/rank_bm25/master/rank_bm25.py | 2026-10-13 | `def __init__(self, corpus, tokenizer=None, k1=1.5, b=0.75, epsilon=0.25)`; "idf can be negative if word is contained in more than half of documents"; `eps = self.epsilon * self.average_idf` |
| S7 | rank-bm25 on PyPI, https://pypi.org/pypi/rank-bm25/json | 2026-10-13 | version 0.2.2, uploaded 2022-02-16, requires "numpy" |
| S8 | bm25s on PyPI and GitHub, https://pypi.org/pypi/bm25s/json, https://github.com/xhluca/bm25s | 2026-10-13 | version 0.3.13, uploaded 2026-10-07; `def _score_idf_lucene(df, N):`; LICENSE "MIT License" |
| S9 | Haystack in-memory document store, https://raw.githubusercontent.com/deepset-ai/haystack/main/haystack/document_stores/in_memory/document_store.py | 2026-10-13 | in `bm25_retrieval`: `all_documents = self.filter_documents(filters=filters)`; in `_score_bm25okapi`: `for tok, n in self._freq_vocab_for_idf.items():` and `idf[tok] = math.log((len(self._bm25_attr) - n + 0.5) / (n + 0.5))` (store-wide counts); "You can learn more about these parameters by visiting https://github.com/dorianbrown/rank_bm25." |
| S10 | Gemini API, Embeddings, https://ai.google.dev/gemini-api/docs/embeddings | 2026-10-13 | "Use `RETRIEVAL_QUERY` for queries; `RETRIEVAL_DOCUMENT` for documents to be retrieved."; "MRL Dimension MTEB Score (Gemini Embedding 001) 2048 68.16 1536 68.17 768 67.99"; for 001 "**Input token limit** 2,048", for 2 "8,192"; "If you are using `gemini-embedding-001`, you must manually normalize non-3072 dimensions"; "The embedding spaces between `gemini-embedding-001` and `gemini-embedding-2` are **incompatible**."; "With `gemini-embedding-2`, the `task_type` parameter is not supported."; "`task: search result \| query: {content}`" |
| S11 | Gemini API, Deprecations, https://ai.google.dev/gemini-api/docs/deprecations | 2026-10-13 | "gemini-embedding-2 April 22, 2026 No shutdown date announced gemini-embedding-001 July 14, 2025 May 14, 2028 gemini-embedding-2"; "embedding-2-preview March 10, 2026 August 10, 2026" |
| S12 | Gemini API, Release notes, https://ai.google.dev/gemini-api/docs/changelog | 2026-10-13 | "April 22, 2026 Released gemini-embedding-2 as generally available (GA)."; "July 14, 2025 Released gemini-embedding-001 , the stable version of our text embedding model." |
| S13 | Gemini API, Pricing, https://ai.google.dev/gemini-api/docs/pricing | 2026-10-13 | "Gemini Embedding 2 gemini-embedding-2 ... Text input price Free of charge $0.20 ... Used to improve our products Yes No"; no entry for `gemini-embedding-001` |
| S14 | Gemini API, Rate limits, https://ai.google.dev/gemini-api/docs/rate-limits | 2026-10-13 | "Rate limits are applied per project, not per API key."; "Rate limits depend on a variety of factors (such as your usage tier) and can be viewed in Google AI Studio." |
| S15 | `GoogleGenerativeAIEmbeddings`, installed source of langchain-google-genai 4.4.1, `langchain_google_genai/embeddings.py` | 2026-10-13 | `effective_task_type = task_type or self.task_type or "RETRIEVAL_DOCUMENT"` (documents); `effective_task_type = task_type or self.task_type or "RETRIEVAL_QUERY"` (queries); `EmbedContentConfig(task_type=effective_task_type, ...)`; docstring example `model="gemini-embedding-2-preview"` |
| S16 | `InMemoryVectorStore`, installed source of langchain-core 1.6.10, `langchain_core/vectorstores/utils.py` | 2026-10-13 | "cosine_similarity requires numpy to be installed. Please install numpy with `pip install numpy`." (raised at search time; `langchain-core` requires: httpx, jsonpatch, langchain-protocol, langsmith, packaging, pydantic, pyyaml, tenacity, typing-extensions, uuid-utils) |
| S17 | Vietnamese Embedding & Reranking Benchmark, https://github.com/dangvansam/vietnamese-embedding-benchmark | 2026-10-13 | "Kết quả (NDCG@10 trung bình, 24 task Retrieval) ... 4 \| google/embeddinggemma-300m \| 47.23 ... 5 \| Qwen/Qwen3-Embedding-0.6B \| 45.87 \| 6 \| BAAI/bge-m3 \| 45.53" (no Gemini API model in the table) |
| S18 | VN-MTEB, arXiv:2507.21500, https://arxiv.org/abs/2507.21500 | 2026-10-13 | "Our comprehensive benchmark consists of 41 datasets from six tasks specifically designed for Vietnamese text embeddings."; "benchmark 18 text embedding models" |
| S19 | Cormack, Clarke and Buettcher, Reciprocal Rank Fusion outperforms Condorcet and individual Rank Learning Methods, SIGIR 2009, https://cormack.uwaterloo.ca/cormacksigir09-rrf.pdf | 2026-10-13 | "where k = 60 was fixed during a pilot investigation and not altered during subsequent validation"; "indicated that k = 60 was near-optimal, but that the choice was not critical" |
| S20 | Bruch, Gai and Ingber, An Analysis of Fusion Functions for Hybrid Retrieval, arXiv:2210.11934 (ACM TOIS, doi 10.1145/3596512), https://arxiv.org/abs/2210.11934 | 2026-10-13 | "we find RRF to be sensitive to its parameters; ... that CC outperforms RRF in in-domain and out-of-domain settings; and finally, that CC is sample efficient, requiring only a small set of training examples to tune its only parameter to a target domain." |
| S21 | Elasticsearch, Reciprocal rank fusion, https://www.elastic.co/docs/reference/elasticsearch/rest-apis/reciprocal-rank-fusion | 2026-10-13 | "rank_constant ... This value must be greater than or equal to `1`. Defaults to `60`." |
| S22 | Weaviate, Hybrid search, https://weaviate.io/developers/weaviate/search/hybrid | 2026-10-13 | "`Relative Score Fusion` is the default fusion method starting in `v1.24`."; "An `alpha` of `1` is a pure vector search. An `alpha` of `0` is a pure keyword search." |
| S23 | nom-vn benchmark, https://github.com/nrl-ai/nom-vn/blob/main/docs/benchmark.md | 2026-10-13 | Zalo Legal 5k subset, `dangvantuan/vietnamese-embedding`: "BM25 only \| 0.762", "Dense only \| 0.412", "Hybrid (RRF) \| 0.650" (recall@1); `AITeamVN/Vietnamese_Embedding` "(1024-d, ~2.3 GB, BGE-M3 base)": BM25 0.762, Dense 0.825, Hybrid (RRF) 0.800; "`BAAI/bge-reranker-v2-m3` ... ~2.3 GB \| 568 M"; "bkai cần preprocessing word-segmenter" |
| S24 | fastembed on PyPI and its model list, https://pypi.org/pypi/fastembed/json | 2026-10-13 | version 0.9.0, uploaded 2026-10-07; `TextEmbedding.list_supported_models()`: "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 384 0.22 apache-2.0" |
| S25 | ViLeXa README, https://github.com/trtkiet/ViLeXa | 2026-10-13 | "achieved **77.3% Hit Rate@1** and **95.0% Recall@10** on the Zalo AI Legal Retrieval benchmark (150 queries), with **NDCG@10 of 0.867** and **MRR of 0.842**" (no hybrid-against-dense comparison) |

R1 sources reused: LangChain `EnsembleRetriever` `c: int = 60` and Haystack RRF k = 61 (`docs/research/0001-rag-framework-or-own-modules.md`, S10 and S16).

## How the measurements were taken

<details>
<summary>M1-M4 scripts (run in throwaway virtual environments outside the repository)</summary>

M1: `uv venv -p 3.12`, then `uv pip install underthesea psutil`, `pyvi psutil` or `fastembed psutil pyyaml`; size with `du -sm <venv>/Lib/site-packages`; memory with `psutil.Process().memory_info().rss` after importing and segmenting five sentences, or after loading the embedding model.

M2: each segmenter was run on all chunk texts and wordings, its output split with `re.findall(r"\w+", seg(text).lower())`, and the two outputs compared text by text.

M3 and M4, the core (chunks, scopes and wordings are loaded from `data/` and `adopted_rules.rulebook`):

```python
import math, re, unicodedata
from collections import Counter

def syllables(text):
    return re.findall(r"\w+", unicodedata.normalize("NFC", text).lower())

def bm25(query, texts, tok=syllables, k1=1.2, b=0.75):
    """Scores every text; statistics over the given texts only (the asker's scope)."""
    docs = [tok(t) for t in texts]
    n = len(docs); avgdl = sum(map(len, docs)) / n
    df = Counter(w for d in docs for w in set(d))
    scores = []
    for d in docs:
        tf = Counter(d); s = 0.0
        for w in tok(query):
            if w in tf:
                idf = math.log(1 + (n - df[w] + 0.5) / (df[w] + 0.5))
                s += idf * tf[w] * (k1 + 1) / (tf[w] + k1 * (1 - b + b * len(d) / avgdl))
        scores.append(s)
    return scores

def rrf(rankings, k=60):
    s = {}
    for r in rankings:
        for pos, i in enumerate(r):
            s[i] = s.get(i, 0) + 1 / (k + pos + 1)
    return sorted(s, key=lambda i: -s[i])

def fold(tokens):  # diacritic-folded copies
    return ["".join(c for c in unicodedata.normalize("NFD", t) if unicodedata.category(c) != "Mn").replace("đ", "d") for t in tokens]

# Titled chunk text: f"{title}. {chunk}"; the target clauses per row:
TARGET = {1: ["LEAVE-GAMECO-v2#Điều 2"], 2: ["LEAVE-GAMECO-v3#Điều 2"], 3: ["LEAVE-PROC-GAMECO-v1#p1", "LEAVE-PROC-GAMECO-v1#p2"],
          4: ["OT-GAMECO-v1#Điều 3"], 5: ["LEAVE-GROUP-v1#Điều 1"], 7: ["LEAVE-GROUP-v1#Điều 1", "LEAVE-PAYCO-v1#Điều 1"],
          12: ["LEAVE-GROUP-v1#Điều 2", "LEAVE-PAYCO-v1#Điều 2"]}
```

The extra wordings written by Claude for M3 and M4 (not test cases):

```text
2:  Sang năm 2027 tôi có bao nhiêu ngày nghỉ phép? | Năm sau em được off mấy ngày?
3:  Muốn xin nghỉ thì làm đơn ở đâu, ai ký? | Em muốn off vài hôm thì đăng ký kiểu gì?
4:  Làm OT xong được nghỉ bù thì có bị trừ phép không? | Nghỉ bù có tính vào ngày phép năm không?
5, 7:  Năm nay tôi được nghỉ mấy ngày? | Em được off mấy ngày phép một năm?
12: Muốn nghỉ thì phải xin trước bao lâu? | Nghỉ phép phải báo sếp trước mấy hôm?
```

M3d: `BM25Okapi([syllables(t) for t in texts]).get_scores(syllables(query))` with rank_bm25 0.2.2 defaults.
M4: `TextEmbedding("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")`, vectors normalised, dense ranking by dot product, then `rrf([bm25_order, dense_order])`.
To run M4 with Gemini instead, replace the model with `GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")`, embed the titled chunks with `embed_documents` and each wording with `embed_query`, and keep the rest.

</details>
