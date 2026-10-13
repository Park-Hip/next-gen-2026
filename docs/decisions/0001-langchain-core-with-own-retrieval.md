# 0001. Build steps 5-6 on LangChain core, with our own Vietnamese BM25 and fusion

- Status: Accepted
- Date: 2026-10-13
- Origin: AI, accepted
- Supersedes: None (adds two dependencies to the working default of plan decision D10)
- Issue: #4
- Research: `docs/research/0001-rag-framework-or-own-modules.md`

## Context

Steps 1-4 and 7 are deterministic rules and stay our own code.
Steps 5-6 (hybrid retrieval inside the asker's scope, then the LLM answer with cited chunk ids) needed a choice: a RAG framework or our own small modules.
Hiep asked for a framework that is widely used in real production projects, has a large user base, and is a common choice for similar projects.
The research found that LangChain meets that bar by a wide margin, but its BM25 and fusion retrievers sit in `langchain-community` (sunset on 22/05/2026) and `langchain-classic` (deprecated functionality).
It also found that LlamaIndex's BM25 ignores a custom tokenizer and mangles Vietnamese, and that Haystack fits technically but has a much smaller user base.

## Options considered

1. **A. Own modules** - `google-genai` plus our own BM25, fusion, scope filter and citation check; no framework.
2. **B. Full LangChain hybrid stack** - adds `BM25Retriever` from `langchain-community` and `EnsembleRetriever` from `langchain-classic`.
3. **C. LangChain core plus our own retrieval** - `langchain-core` and `langchain-google-genai` for the Gemini model, embeddings and in-memory vector store; our own Vietnamese BM25 and fusion.
4. **D. LlamaIndex** - its BM25, fusion retriever, Gemini integrations and citation engine.
5. **E. Haystack 3.x** - its in-memory document store, BM25 and embedding retrievers, joiner and Gemini integrations.

## Decision

Option C: v1 uses `langchain-core` 1.x and `langchain-google-genai` for the Gemini chat model, structured output, embeddings and `InMemoryVectorStore`, and our own code for the Vietnamese BM25, reciprocal rank fusion, the scope filter and the step 7 citation check.

## Reasons

The main reason is LangChain's popularity, with a large user base (Hiep, 13/10/2026).

## Consequences

Drafted by Claude from the research; approved by Hiep on 13/10/2026.

- New dependencies: `langchain-core` and `langchain-google-genai`, pinned; `google-genai` stays as their dependency.
  `langchain`, `langchain-community` and `langchain-classic` are not installed.
- #12: our BM25 and fusion modules sit next to `InMemoryVectorStore`, which receives the scope as a `filter` so only in-scope chunks are scored.
  The tokenizer follows ADR 0002 (#5).
- #13: the model returns the answer and its cited chunk ids through `with_structured_output`; step 7 checks those ids against the retrieved ones, as before.
- Run logging can use LangSmith tracing (free plan: 5k base traces a month), or our own log file.
- Cost: one more layer to explain in PITCH than option A; measured on Windows, the install grows from 34 MB to 46 MB and memory after import from about 50 MB to about 76 MB.

## Would change if

Drafted by Claude; approved by Hiep on 13/10/2026.

- R3 (#6) picks a model with no maintained LangChain integration.
- LangChain moves `ChatGoogleGenerativeAI`, `GoogleGenerativeAIEmbeddings` or `InMemoryVectorStore` out of the maintained packages.
- The deployed app on Render runs short of its 512 MB.

## Evidence

The research write-up above, with measurements M1 and M2.
Evidence log line of 13/10/2026 (Claude Opus 5.5 with Agnes 2.5 Flash subagents).
