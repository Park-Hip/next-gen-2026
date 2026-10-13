# 0001. Should v1 build retrieval and generation with a RAG framework or with our own modules?

- Status: Draft
- Issue: #4
- Feeds: ADR 0001
- Method: Pi on 13/10/2026, 09:56-10:20.
  Orchestrator: Claude Opus 5.5 (`claude-bridge/claude-opus-5-5`), which wrote the lane prompts, ran the measurements and checked the sources.
  Web research: four `researcher` subagents on Agnes 2.5 Flash with max reasoning (`agnes/agnes-2.5-flash:max`), run in two pairs to stay under the Agnes free-tier rate limit; all four finished.
  Search providers: the `web_search` tool's configured provider; one lane reported Exa and DuckDuckGo (Brave had no key).
  Claude then opened every source in the table below itself (page fetch, PyPI and GitHub APIs, OSV API, or the installed package source), with no other model involved.
  Hiep's prompt to Claude and the four lane prompts follow verbatim.

```text
Hiep to Claude:
https://github.com/Park-Hip/next-gen-2026/issues/4 I want you to do research about this. You may use web search using some subagent and only use Agnes with max reasoning level for the web search. Do not use other models. I want you to consider reading the research R2 so we can have a good itegration with our  framework. Another thing is that I want a framework that is popularly used by many real production projects, has a big user base, and is a popular technical choice for similar projects.

Shared context, sent at the top of each lane:
You are researching one technical decision for a small Python RAG prototype. Today is 2026-10-13.

Project: v1 of an internal-policy assistant, built in about one day inside a 3-day competition. Python, FastAPI + Jinja2, hosted on Render's free web service (512 MB RAM).
Data: about 10 simulated Vietnamese HR policy documents in Markdown with YAML front matter, chunked by article ('Dieu'), so roughly 30-60 chunks in total and about 10 chunks per asker.
Pipeline: steps 1-4 are deterministic rules that build the asker's allowed scope (a set of chunk ids) from metadata BEFORE any retrieval. Step 5 is hybrid retrieval restricted to that scope: BM25 over Vietnamese syllables with diacritics kept, plus gemini-embedding-001 embeddings, fused with reciprocal rank fusion (RRF). Step 6 is a Gemini Flash call via the google-genai SDK that must answer only from the retrieved chunks, cite chunk ids, or say 'not found'. Step 7 is deterministic: the answer is refused if any cited chunk id is not among the retrieved chunks, and conflict cards are chosen from the citations.
Decision: build steps 5-6 and the glue (loading and chunking, retrieval, the LLM call, run logging) with a RAG framework (LangChain, LlamaIndex, Haystack, or another) or with our own small Python modules. The owner prefers a framework only if it is widely used in real production projects, has a large user base, and is a common choice for similar projects.

Rules for your work:
- Use web_search, then OPEN each page you cite with fetch_content. Prefer official docs, official repos, PyPI, package registries and first-party engineering blogs.
- Every claim needs: the claim, the URL, an exact quote copied from the opened page, and the date the page states (if any).
- If you only saw a search snippet, mark the claim [snippet only]. If you could not find something, say so; never guess numbers.
- Do not write any files. Return your report as your final message.
- Output format: (1) a short summary of findings, (2) a Markdown table: Claim | URL | Exact quote | Page date, (3) a list 'Could not verify'.

Your lane:

Lane "adoption":
Popularity and production use of Python LLM/RAG frameworks in 2026: LangChain (and LangGraph), LlamaIndex, Haystack, and any other contender you find (for example DSPy, Pydantic AI, txtai, Semantic Kernel, Google ADK).
Gather: GitHub stars and contributors (with date), PyPI download counts (pypistats.org or pepy.tech, with date), named companies using each in production with links to case studies, developer survey results (Stack Overflow Developer Survey 2025, JetBrains, State of AI reports, LangChain's own reports), and which framework is most often used in RAG tutorials and courses.
Also gather counter-evidence: well-known posts from teams that removed a framework from production and why, and guidance from model vendors (for example Anthropic's 'Building effective agents', OpenAI, Google) on frameworks versus direct API calls.

Lane "retrieval":
How well each of LangChain, LlamaIndex and Haystack 2.x supports exactly our step 5, from their official docs and source code:
1. BM25 retriever with a custom tokenizer or preprocess function (we need Vietnamese syllable tokens with diacritics kept): class names, parameter names, which library is underneath (rank_bm25, bm25s, own code).
2. Gemini embeddings with gemini-embedding-001: the integration package names, whether they use the new google-genai SDK or the deprecated google-generativeai SDK, and support for task_type / output dimensionality.
3. An in-memory vector store suitable for about 50 chunks.
4. Reciprocal rank fusion of BM25 and dense results: LangChain EnsembleRetriever, LlamaIndex QueryFusionRetriever (mode reciprocal_rerank), Haystack DocumentJoiner (join_mode reciprocal_rank_fusion); the default k constant and weights.
5. Pre-filtering: can retrieval be restricted to an allowed set of chunk ids or metadata values BEFORE scoring (not filtering after top-k)? Show the exact API (metadata filters, filters dict, etc.) for BM25 and for the vector store in each framework.
Include short code snippets from the docs. Note any gap where we would have to write our own code anyway.

Lane "generation":
How each of LangChain, LlamaIndex and Haystack 2.x handles our step 6 and the run log, from official docs and source code:
1. Calling Gemini Flash: integration package names (langchain-google-genai, llama-index-llms-google-genai, google-genai-haystack), and whether they wrap the google-genai SDK.
2. Structured output with a list of cited chunk ids (JSON schema / Pydantic): with_structured_output, LlamaIndex structured_predict / output_cls, Haystack equivalents; reliability with Gemini.
3. Built-in citation features: LlamaIndex CitationQueryEngine, Haystack AnswerBuilder with references, LangChain citation guides. Do they cite ids we control, or re-chunk the text into their own 'sources'?
4. Transparency: can a developer see and fully control the exact prompt sent to the model? Are there hidden default prompts in high-level chains or query engines (for example LlamaIndex default text_qa_template, LangChain create_retrieval_chain)?
5. Run logging and tracing: LangSmith, Langfuse, Arize Phoenix, OpenTelemetry; which work with each framework and which work without any framework (plain google-genai calls), including free tiers.
6. The no-framework path: the google-genai SDK's own support for structured output (response_schema), and how much code a minimal retrieve-then-generate loop needs.

Lane "weight":
Cost and risk of each framework (LangChain, LlamaIndex, Haystack 2.x) for a tiny app on a 512 MB RAM host:
1. Install footprint: the minimal core packages (langchain-core, langchain, langchain-community, llama-index-core, haystack-ai), their required dependencies (read the dependency lists on PyPI or in pyproject.toml), wheel sizes, and any measured import time or RAM numbers people have published.
2. Stability: release cadence, major versions and breaking changes since 2024 (LangChain 1.0 in late 2025 and what moved to langchain-classic, LlamaIndex 0.10 to 0.14 package split, Haystack 1.x to 2.x), deprecation policies and how long APIs stay stable.
3. Security: published CVEs or advisories in 2024-2026 for these packages (for example LangChain serialization issues, LlamaIndex CVEs), with GHSA or NVD links.
4. Who maintains them: company behind each (LangChain Inc, LlamaIndex Inc, deepset), funding and license.
5. Any published comparisons of these frameworks for small RAG apps (benchmarks of overhead, lines of code, learning curve), with their method stated.
```

## Why it matters for v1

The answer sets the code layout and dependencies of #12 (retrieval) and #13 (generation), and what Hiep must explain or rebuild in PITCH.
Steps 1-4 and 7 stay our own code either way; the question covers loading and chunking, hybrid retrieval, the LLM call and run logging.

Constraints any option must respect:

- The scope comes first: retrieval may only score the chunks the rules allowed for this asker (promise R8 in `docs/mission2/mission1_promises.md`).
- Step 7 checks citations against the chunk ids that were actually retrieved (R7), so the model must cite ids we control, not ids a framework invents.
- The card comes from rules, never from LLM text (A4), so a framework's answer object is only an input to step 7.
- Render free web service: 512 MB RAM.
- About one day to build, and Hiep must be able to explain every part.

Fit with R2 (#5).
R2 has no write-up yet; its working default is our own BM25 over Vietnamese syllables with diacritics kept, `gemini-embedding-001`, and reciprocal rank fusion (RRF) over the asker's scope chunks (about 10).
So this write-up checks each framework against exactly that stack: a custom Vietnamese tokenizer for BM25, Gemini embeddings, RRF, and a scope filter applied before scoring.
If R2 changes the stack (for example to word segmentation with underthesea or pyvi), the tokenizer row below matters even more, because the tokenizer must be pluggable.

## Options found

| Option | What it is | Strengths | Costs and risks | Fit for v1 | Sources |
|---|---|---|---|---|---|
| A. Own modules | `google-genai` for embeddings and the Gemini call; our own BM25, RRF, scope filter and citation check in plain Python | Smallest install (M1); every line visible for PITCH; matches R2's default exactly; `google-genai` supports JSON-schema output (`response_schema`) | Not a framework, so it does not meet Hiep's popularity preference; we write about 30-60 more lines (BM25, RRF, cosine); tracing must be added by hand (LangSmith `@traceable` or Langfuse work without a framework) | Good | S20, S21, S22, S26, S27, S28, M1 |
| B. LangChain, full hybrid stack | `langchain-google-genai` for model and embeddings, `InMemoryVectorStore`, `BM25Retriever` from `langchain-community`, `EnsembleRetriever` (weighted RRF, c=60) from `langchain-classic` | By far the largest user base (S1, S2, S3, S4); custom tokenizer via `preprocess_func` worked on Vietnamese (M2); vector store applies the filter before scoring (S9) | The two hybrid pieces sit outside LangChain's maintained core: `langchain-community` was sunset on 22/05/2026 and warns on import (S6, M2), `langchain-classic` holds "deprecated functionality" (S7); 66 packages, 121 MB, about 100 MB RAM at import (M1) | Weak: builds on a sunset package | S1-S10, M1, M2 |
| C. LangChain core plus own retrieval | `langchain-core` 1.x and `langchain-google-genai` for the Gemini chat model, structured output, embeddings and `InMemoryVectorStore` (scope filter before scoring); our own Vietnamese BM25 and RRF | Uses LangChain only where it is LTS and semver-covered (S5); keeps R2's own tokenizer and RRF; a model or embedding change from R3 or R2 is one class swap; LangSmith tracing fits natively | One more layer to explain than A; 43 packages, 46 MB, about 76 MB RAM at import (M1); the retrieval half is still our code, so the framework covers less than half of steps 5-6 | Good | S1-S5, S9, M1 |
| D. LlamaIndex | `BM25Retriever` (bm25s), `VectorStoreIndex`, `QueryFusionRetriever` (RRF, k=60 fixed), `GoogleGenAIEmbedding`, `GoogleGenAI` LLM | Second-largest user base (S1, S2); RAG-focused; metadata filters on the vector store and on BM25 | BM25 silently ignores a custom tokenizer (deprecated, only warns) and its English stemmer turned "ngày" into "ngài" and dropped "ở" (S11, M2); `CitationQueryEngine` re-splits chunks into "Source N" and drops our ids (S13); default QA prompt is hidden unless overridden (S14); largest install: 78 packages, 160 MB, about 127 MB RAM (M1) | Weak for Vietnamese BM25 and for our citation ids | S1, S2, S11-S14, M1, M2 |
| E. Haystack 3.x | `InMemoryDocumentStore` with BM25 and embedding retrievers, `DocumentJoiner` (RRF, k=61), `google-genai-haystack` generator and embedders | Best technical fit: default tokenizer kept Vietnamese syllables including "ở", and `filters` restricted BM25 to the scope before scoring (S15, M2); structured output via `response_format` (S17); explicit prompts | Much smaller user base than LangChain: 26.7k stars and 0.57M downloads a month against 147.7k and 170M (S1, S2); 3.0 shipped on 20/07/2026 (S30); 61 packages, 114 MB, about 96 MB RAM (M1) | Good technically; weak on Hiep's popularity criterion | S1, S2, S15-S19, S30, M1, M2 |

### Measured by Claude on 13/10/2026

These are measurements on this machine, not published figures.
They are indicative only: Windows 11 and Python 3.12, while Render runs Linux.

**M1, install and import cost.**
Each option was installed into its own fresh virtual environment with `uv` (latest versions on 13/10/2026); package counts include `psutil`, used for the measurement.
Memory is the resident set size after importing the classes the option would use, median of 3 runs.

| Option | Packages installed | site-packages | Memory after import | Versions |
|---|---|---|---|---|
| A. Own (`google-genai`) | 26 | 34 MB | about 50 MB | google-genai 2.30.0 |
| C. LangChain core + `langchain-google-genai` | 43 | 46 MB | about 76 MB | langchain-core 1.6.10, langchain-google-genai 4.4.1 |
| B. LangChain full hybrid | 66 | 121 MB | about 100 MB | langchain 1.4.5, langchain-community 0.4.2, langchain-classic 1.0.8 |
| E. Haystack | 61 | 114 MB | about 96 MB | haystack-ai 3.3.0, google-genai-haystack 6.0.1 |
| D. LlamaIndex | 78 | 160 MB | about 127 MB | llama-index-core 0.14.25, retrievers-bm25 0.8.0 |

All options leave most of the 512 MB free, so memory does not decide this question.
FastAPI and the app itself come on top of every row equally.

**M2, Vietnamese BM25 on our simulated data.**
Each framework's BM25 retriever was built from the "Điều" lines of the 10 files in `data/documents/` (branch `3-simulated-data`), using the sentence "Nhân sự ở GameCo được nghỉ phép năm 13 ngày" and the query "ở GameCo được nghỉ phép năm mấy ngày".

| Framework | Tokens produced for the sentence | Note |
|---|---|---|
| Own, `re.findall(r"\w+", text.lower())` | nhân, sự, ở, gameco, được, nghỉ, phép, năm, 13, ngày | Passed to LangChain as `preprocess_func`; LangChain printed "`langchain-community` is being sunset and is no longer actively maintained" on import |
| LlamaIndex defaults | nhân, sự, gameco, được, nghỉ, phép, năm, 13, ngài | "ở" dropped by the default `token_pattern`; "ngày" stemmed to "ngài"; passing our tokenizer only logged "The tokenizer parameter is deprecated" and the retriever kept no tokenizer |
| Haystack defaults | nhân, sự, ở, gameco, được, nghỉ, phép, năm, 13, ngày | With `filters={"field": "id", "operator": "in", "value": scope}` it returned only the 2 PayCo chunks |

The top 3 results were the same leave clauses in all three frameworks on this small query, so the tokenizer problems did not change this ranking; they would matter on questions where a dropped or merged syllable is the distinguishing word.
LlamaIndex can be configured around both problems (`skip_stemming=True` and a wider `token_pattern`), but not with our own tokenizer function.

The scripts are under "How the measurements were taken" at the end.

### Popularity, as Hiep asked

| Framework | GitHub stars (13/10/2026) | PyPI downloads, last month | Other evidence |
|---|---|---|---|
| LangChain | 147,715 (`langchain`); LangGraph 43,157 | 170.5M `langchain`, 144.8M `langchain-core` | Stack Overflow 2025: LangChain is the second most used agent orchestration tool, at 33% (S3); company reports 90M monthly downloads for `langchain` and `langgraph` and "35 percent of the Fortune 500" (S4, self-reported) |
| LlamaIndex | 52,468 | 6.6M `llama-index-core`, 2.9M `llama-index` | Vendor case studies (lane report, not opened by Claude) |
| DSPy | 38,602 | 5.3M | Not a RAG pipeline library in the same sense |
| Haystack | 26,728 | 0.57M `haystack-ai` | Vendor case studies such as Lufthansa Industry Solutions (lane report, not opened by Claude) |
| Pydantic AI | 20,583 | 5.4M | Agent framework, no retrieval components |
| `google-genai` (no framework) | - | 137.6M | Google's official SDK; also a dependency of every Gemini integration above |

Download counts include CI runs and installs pulled in as dependencies, so they measure reach, not the number of production projects.
No independent count of production projects per framework was found.

Counter-evidence on frameworks in production (S21, S22, S23): Anthropic advises starting with LLM APIs directly; Vody (SIGIR eCom 2025) removed LangChain because it "became a source of additional bugs"; Vettio (one team's blog post, metrics self-reported) replaced LangChain with the raw SDK in April 2026.
All three are about agents or large-scale inference rather than small RAG, and all three name LangChain because it is the most used.

Security (S24, S25): each framework had at least one advisory in 2024-2026 (LangChain unsafe deserialization CVE-2026-44843; LlamaIndex CVE-2025-6209 and CVE-2025-1793; Haystack Jinja2 RCE CVE-2024-41950).
The versions installed on 13/10/2026 (langchain-core 1.6.10, llama-index-core 0.14.25, haystack-ai 3.3.0, google-genai 2.30.0) had no open advisories in OSV.

## Claims that did not hold up

1. **"LlamaIndex `BM25Retriever` has no filters parameter, so BM25 pre-filtering is not available"** (retrieval lane).
   The installed source (llama-index-retrievers-bm25 0.8.0) has `filters: Optional[MetadataFilters] = None` in `__init__` and `from_defaults` and builds a weight mask from it (S11).
2. **"LlamaIndex `BM25Retriever.from_defaults(..., tokenizer=fn)` accepts a custom tokenizer"** (retrieval lane, quoting the docs page).
   The parameter is accepted but not used: the source logs "The tokenizer parameter is deprecated" and does not pass it on, and M2 confirmed the retriever keeps no tokenizer (S11).
3. **"Haystack has no first-party structured-output component"** (generation lane).
   `GoogleGenAIChatGenerator` documents `generation_kwargs={"response_format": City}` (S17).
4. **"No Haystack CVEs were found in 2024-2026"** (weight lane).
   OSV lists GHSA-hx9v-6r9f-w677 / CVE-2024-41950, "Insecure Jinja2 templates rendered in Haystack Components can lead to RCE", published 31/07/2024 (S24).
5. **"LangChain adds +200-400 MB to Docker images; LlamaIndex and Haystack are baseline", "~10-14 ms vs ~6 ms overhead", "~2.4k vs ~1.6k tokens per request"** (weight lane, from algorithmine.com, S29).
   The article cites only other blogs and states no method.
   M1 contradicts the size claim for our use: LlamaIndex was the largest install (160 MB) and LangChain core the smallest framework (46 MB).
   The weight lane's summary ("LlamaIndex or Haystack 2.x are the stronger framework choices over LangChain") rests on these figures, so it is not carried into this write-up.
6. **"Stack Overflow 2025: LlamaIndex 13.3%, Haystack 4.4%, survey published December 2025"** (adoption lane).
   The page text only says "Ollama (51%) and LangChain (33%) are the most-used frameworks" (S3); the other figures may come from the chart but could not be checked, and the publication date is not on the page.
7. **"Haystack embedders do not show `task_type` or output dimensionality"** (retrieval lane, a gap rather than a false claim).
   `GoogleGenAITextEmbedder` takes a `config` dict passed to `types.EmbedContentConfig`, which carries both (S18).

Not checked by Claude, so not used above: the lanes' customer lists for LlamaIndex and Haystack, LlamaIndex's and deepset's funding figures, and contributor counts.

The lanes also missed one fact that changes option B: `langchain-community`, home of LangChain's `BM25Retriever`, was sunset on 22/05/2026 (S6).

## AI recommendation (not a decision)

Claude's pick: option C, LangChain core 1.x for the Gemini model, embeddings and the in-memory vector store, with our own Vietnamese BM25, RRF, scope filter and citation check.
One-line reason (Claude's): it is the only option that meets Hiep's "popular, production-proven framework" preference using only parts the vendor covers with LTS, while keeping R2's tokenizer and the step 7 citation ids under our control.
The strongest alternative is A (no framework), if Hiep weighs the smallest code to explain in PITCH above the popularity preference; E is the best technical fit but fails the popularity preference.

Questions for Hiep before the ADR: which option, and in your own words why it beats the strongest alternative.

## Sources

All accessed 2026-10-13 by Claude.
"Installed source" means the file in the package version named, installed from PyPI on that day.

| ID | Title and URL | Accessed | Quote that supports the claim |
|---|---|---|---|
| S1 | GitHub REST API, `repos/<owner>/<repo>` for langchain-ai/langchain, run-llama/llama_index, deepset-ai/haystack, stanfordnlp/dspy, pydantic/pydantic-ai, langchain-ai/langgraph; https://api.github.com/repos/langchain-ai/langchain | 2026-10-13 | `stargazers_count`: 147715, 52468, 26728, 38602, 20583, 43157 |
| S2 | pypistats API, https://pypistats.org/api/packages/langchain/recent (and the same for each package named) | 2026-10-13 | `last_month`: langchain 170457766, langchain-core 144826657, llama-index-core 6574473, llama-index 2937852, haystack-ai 566454, dspy 5312050, pydantic-ai 5383780, google-genai 137607856 |
| S3 | 2025 Stack Overflow Developer Survey, AI, https://survey.stackoverflow.co/2025/ai/ | 2026-10-13 | "Among developers building agents, Ollama (51%) and LangChain (33%) are the most-used frameworks." |
| S4 | LangChain raises $125M, https://www.langchain.com/blog/series-b | 2026-10-13 | "Today, `langchain` and `langgraph` have a combined 90M monthly downloads, and 35 percent of the Fortune 500 use our services." |
| S5 | LangChain release policy, https://docs.langchain.com/oss/python/release-policy | 2026-10-13 | "Breaking changes to the public API will only occur in major version releases (e.g., `2.0.0`)"; "**LangChain 1.0** is designated as an LTS release" |
| S6 | Sunsetting `langchain-community`, https://github.com/langchain-ai/langchain-community/issues/674 (opened 2026-05-22) | 2026-10-13 | "we are making the decision to sunset the `langchain-community` package ... This sunset will take effect immediately." |
| S7 | langchain-classic on PyPI, https://pypi.org/project/langchain-classic/ | 2026-10-13 | "Legacy chains, `langchain-community` re-exports, indexing API, deprecated functionality, and more." |
| S8 | `BM25Retriever`, installed source of langchain-community 0.4.2, `langchain_community/retrievers/bm25.py` | 2026-10-13 | `preprocess_func: Callable[[str], List[str]] = default_preprocessing_func`; `from rank_bm25 import BM25Okapi` |
| S9 | `InMemoryVectorStore`, installed source of langchain-core 1.6.10, `langchain_core/vectorstores/in_memory.py` | 2026-10-13 | `if filter is not None: docs = [doc for doc in docs if filter(...)]` before `similarity = cosine_similarity(...)` |
| S10 | `EnsembleRetriever`, installed source of langchain-classic 1.0.8, `langchain_classic/retrievers/ensemble.py` | 2026-10-13 | `c: int = 60` |
| S11 | `BM25Retriever`, installed source of llama-index-retrievers-bm25 0.8.0, `llama_index/retrievers/bm25/base.py` | 2026-10-13 | `filters: Optional[MetadataFilters] = None`; "The tokenizer parameter is deprecated and will be removed in a future release. Use a stemmer from PyStemmer instead."; `self.stemmer = stemmer or Stemmer.Stemmer("english")` |
| S12 | `QueryFusionRetriever`, installed source of llama-index-core 0.14.25, `llama_index/core/retrievers/fusion_retriever.py` | 2026-10-13 | "k = 60.0  # k is a parameter used to control the impact of outlier rankings." (backticks around k removed) |
| S13 | `CitationQueryEngine`, installed source of llama-index-core 0.14.25, `llama_index/core/query_engine/citation_query_engine.py` | 2026-10-13 | `source_data.pop("id_", None)`; `text = f"Source {len(new_nodes) + 1}:\n{text_chunk}\n"` |
| S14 | Default prompts, installed source of llama-index-core 0.14.25, `llama_index/core/prompts/default_prompts.py` | 2026-10-13 | `"Given the context information and not prior knowledge, " "answer the query.\n"` |
| S15 | `InMemoryDocumentStore`, installed source of haystack-ai 3.3.0, `haystack/document_stores/in_memory/document_store.py` | 2026-10-13 | `bm25_tokenization_regex: str = _DEFAULT_BM25_TOKENIZATION_REGEX`; in `bm25_retrieval`: `all_documents = self.filter_documents(filters=filters)` before scoring |
| S16 | RRF, installed source of haystack-ai 3.3.0, `haystack/utils/misc.py` | 2026-10-13 | "The constant k is set to 61 (60 was suggested by the original paper, plus 1 as python lists are 0-based ...)" |
| S17 | `GoogleGenAIChatGenerator`, installed source of google-genai-haystack 6.0.1, `.../generators/google_genai/chat/chat_generator.py` | 2026-10-13 | `generation_kwargs={"response_format": City}` |
| S18 | `GoogleGenAITextEmbedder`, installed source of google-genai-haystack 6.0.1, `.../embedders/google_genai/text_embedder.py` | 2026-10-13 | "A dictionary of keyword arguments to configure embedding content configuration."; `kwargs["config"] = types.EmbedContentConfig(**self._config)` |
| S19 | `AnswerBuilder`, installed source of haystack-ai 3.3.0, `haystack/components/builders/answer_builder.py` | 2026-10-13 | `builder = AnswerBuilder(reference_pattern="\\[(\\d+)\\]", ...)` (references are positions in the document list, not our ids) |
| S20 | `GenerateContentConfig`, installed source of google-genai 2.30.0, `google/genai/types.py` | 2026-10-13 | `response_mime_type: Optional[str] = Field(`; `response_schema: Optional[SchemaUnion] = Field(` |
| S21 | Building effective agents, Anthropic, https://www.anthropic.com/engineering/building-effective-agents | 2026-10-13 | "We suggest that developers start by using LLM APIs directly: many patterns can be implemented in a few lines of code. If you do use a framework, ensure you understand the underlying code." |
| S22 | Kim et al., Lessons from the bleeding edge: large-scale production inference of LLMs, SIGIR eCom 2025, https://sigir-ecom.github.io/eCom25Papers/paper_31.pdf | 2026-10-13 | "LLM-ecosystem frameworks such as Langchain, became a source of additional bugs. ... we removed the use of Langchain as found that standardizing to Open AI API was sufficient for our needs" |
| S23 | Why we replaced LangChain with the raw Anthropic SDK in production, https://dev.to/tufailkhan457/why-we-replaced-langchain-with-the-raw-anthropic-sdk-in-production-3611 | 2026-10-13 | "In April 2026, we ripped it out."; "Lines of integration code: 812 → 187" |
| S24 | OSV advisories, https://api.osv.dev/v1/vulns/PYSEC-2026-2564, .../GHSA-hx9v-6r9f-w677, .../PYSEC-2026-1558, .../CVE-2025-1793 | 2026-10-13 | "LangChain vulnerable to unsafe deserialization of attacker-controlled objects through overly broad `load()` allowlists" (fixed in langchain-core 1.3.3); "Insecure Jinja2 templates rendered in Haystack Components can lead to RCE" (2024-07-31); "LlamaIndex vulnerable to Path Traversal attack through its encode_image function"; "SQL Injection in run-llama/llama_index" |
| S25 | OSV query by version, https://api.osv.dev/v1/query | 2026-10-13 | 0 advisories for langchain-core 1.6.10, llama-index-core 0.14.25, haystack-ai 3.3.0 and google-genai 2.30.0 |
| S26 | LangSmith plans and pricing, https://www.langchain.com/pricing | 2026-10-13 | "Developer ... $0 / seat per month ... Up to 5k base traces / mo" |
| S27 | Langfuse pricing, https://langfuse.com/pricing | 2026-10-13 | "Hobby (Free) ... 50k units / month included ... 30 days data access" |
| S28 | LangSmith SDK README, https://github.com/langchain-ai/langsmith-sdk/blob/main/python/README.md | 2026-10-13 | "The easiest way to log traces using the SDK is via the `@traceable` decorator." |
| S29 | LangChain, LlamaIndex, and Haystack in 2026, https://algorithmine.com/learn/langchain-llamaindex-haystack-comparison-2026 | 2026-10-13 | "Docker image size delta +200–400 MB baseline baseline"; sources: "Gigagpu.com benchmark data, AIMultiple ..., Dev.to ..., ranksquire.com ..." (no method stated) |
| S30 | PyPI JSON API, https://pypi.org/pypi/haystack-ai/json and https://pypi.org/pypi/langchain/json | 2026-10-13 | haystack-ai 3.0.0 uploaded 2026-07-20; langchain 1.0.0 uploaded 2025-10-17 |

## How the measurements were taken

<details>
<summary>M1 and M2 scripts (run in throwaway virtual environments outside the repository)</summary>

M1: one environment per option, each with `uv venv -p 3.12` and `uv pip install`:

```text
A  google-genai psutil
C  langchain-core langchain-google-genai psutil
B  langchain langchain-google-genai langchain-community rank-bm25 psutil
D  llama-index-core llama-index-embeddings-google-genai llama-index-llms-google-genai llama-index-retrievers-bm25 psutil
E  haystack-ai google-genai-haystack psutil
```

Size: `du -sm <venv>/Lib/site-packages`; count: `uv pip list`.
Memory: this script runs an import file and prints the resident set size; each import file imports the classes the option uses (for example, for E: `Pipeline`, `InMemoryDocumentStore`, `InMemoryBM25Retriever`, `InMemoryEmbeddingRetriever`, `DocumentJoiner`, `GoogleGenAITextEmbedder`, `GoogleGenAIChatGenerator`).

```python
import runpy, sys, time, psutil
p = psutil.Process()
t = time.perf_counter()
runpy.run_path(sys.argv[1])
dt = time.perf_counter() - t
print(f"import_s={dt:.2f} rss_MB={p.memory_info().rss/2**20:.0f} modules={len(sys.modules)}")
```

M2: shared loader, then one short script per framework.

```python
# common.py
import glob, re, sys
DOCS = sys.argv[1]
def load_chunks():
    chunks = []
    for path in sorted(glob.glob(DOCS + "/*.md")):
        body = open(path, encoding="utf-8").read().split("---", 2)[2]
        doc = path.replace("\\", "/").rsplit("/", 1)[1][:-3]
        for line in body.strip().splitlines():
            m = re.match(r"(Điều \d+)\.", line)
            if m:
                chunks.append((f"{doc}#{m.group(1)}", line))
    return chunks
def own_tokens(text):
    return re.findall(r"\w+", text.lower())
SAMPLE = "Nhân sự ở GameCo được nghỉ phép năm 13 ngày"
QUERY = "ở GameCo được nghỉ phép năm mấy ngày"
```

```python
# LangChain
r = BM25Retriever.from_documents([Document(page_content=t, metadata={"id": i}) for i, t in chunks], preprocess_func=own_tokens, k=3)
print(r.preprocess_func(SAMPLE), [d.metadata["id"] for d in r.invoke(QUERY)])

# LlamaIndex: build with our tokenizer, then show what the defaults produce
r = BM25Retriever.from_defaults(nodes=[TextNode(text=t, id_=i) for i, t in chunks], tokenizer=own_tokens, similarity_top_k=3)
print(hasattr(r, "tokenizer"))
ids = bm25s.tokenize([SAMPLE], stopwords="en", stemmer=Stemmer.Stemmer("english"), token_pattern=r"(?u)\b\w\w+\b", show_progress=False)

# Haystack
store = InMemoryDocumentStore()
store.write_documents([Document(id=i, content=t) for i, t in chunks])
r = InMemoryBM25Retriever(store, top_k=3)
scope = [i for i, _ in chunks if i.startswith("LEAVE-PAYCO")]
r.run(query=QUERY, filters={"field": "id", "operator": "in", "value": scope})
```

</details>
