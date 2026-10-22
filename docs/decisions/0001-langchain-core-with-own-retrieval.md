# 0001. Build steps 5-6 on LangChain core, with our own Vietnamese BM25 and fusion

- Status: Accepted
- Date: 2026-10-13
- Origin: AI, accepted
- Supersedes: None (adds two dependencies to the working default of plan decision D10)
- Issue: #4
- Research: `docs/research/0001-rag-framework-or-own-modules.md`

## In short

- **The problem:** After the fixed rules have decided which documents an employee may use, the system still has to search those documents and have the AI answer from them.
  Hiep wanted a toolkit that real production projects widely use, and the most popular one, LangChain, keeps its keyword-search and merge parts in packages that are being retired.
  Another toolkit, LlamaIndex, mangles Vietnamese in its keyword search.
- **The decision:** Use LangChain's small core package and its Gemini connector for the AI model, the meaning-based search and the in-memory store of clauses.
  Write our own Vietnamese keyword search and our own way of merging the two rankings.
- **What the employee sees:** Nothing changes on screen; this is a choice of building blocks.
- **What we give up:** One more layer to explain in the PITCH round than with fully own code.
  On Windows, the install grows from 34 MB to 46 MB and memory after start-up from about 50 MB to about 76 MB.

## Context

The product answers a question in seven steps.
Steps 1-4 and 7 are fixed rules and stay our own code: steps 1-4 build the asker's scope (the documents the asker may read, that apply to their unit, and that are in force), and step 7 checks the AI's answer and picks the card.
Steps 5-6 are different.
Step 5 searches inside the scope with a mix of keyword search and meaning-based search ("hybrid retrieval").
Step 6 has the AI model answer and name the clauses behind each point.
These two steps needed a choice: a ready-made toolkit for retrieval-augmented generation (RAG, answering from retrieved documents), or our own small modules.
Hiep asked for a toolkit that is widely used in real production projects, has a large user base, and is a common choice for similar projects.
The research found that LangChain meets that bar by a wide margin.
But its keyword-search (BM25) and merge retrievers sit in `langchain-community` (sunset on 22/05/2026) and `langchain-classic` (deprecated functionality).
It also found that LlamaIndex's BM25 ignores a custom word splitter and mangles Vietnamese, and that Haystack fits technically but has a much smaller user base.

## Options considered

1. **A. Own modules** - Google's Gemini library plus our own keyword search, merge, scope filter and citation check; no toolkit.
2. **B. Full LangChain hybrid stack** - LangChain's own keyword retriever and its retriever that merges two rankings, from the two retiring packages.
3. **C. LangChain core plus our own retrieval** - LangChain's core and Gemini connector for the AI model, the embeddings (the meaning-based search) and the in-memory store; our own Vietnamese keyword search and merge.
4. **D. LlamaIndex** - its keyword search, merge retriever, Gemini connectors and citation engine.
5. **E. Haystack 3.x** - its in-memory store, keyword and embedding retrievers, merge step and Gemini connectors.

## Decision

Option C.
Version 1 uses LangChain core 1.x and its Gemini connector for the chat model, the structured output (the model must reply in a fixed shape), the embeddings and the in-memory store.
Our own code does the Vietnamese BM25, the reciprocal rank fusion (RRF, a way to merge two ranked lists into one), the scope filter and the step 7 citation check.

## Reasons

The main reason is LangChain's popularity, with a large user base (Hiep, 13/10/2026).

## Consequences

Drafted by Claude from the research; approved by Hiep on 13/10/2026.

- Two new dependencies, pinned: LangChain core and the Gemini connector; Google's own library stays as their dependency.
  The full `langchain` package and the two retiring ones are not installed.
- Our keyword search and merge sit next to the in-memory store, which receives the scope as a filter so that only in-scope clauses are scored.
  The word splitter follows ADR 0002.
- The model returns its answer and the ids of the clauses it cites through the structured-output call; step 7 checks those ids against the retrieved ones, as before.
- Run logging can use LangSmith tracing (a hosted tracing service; free plan: 5k base traces a month), or our own log file.
- Cost: one more layer to explain in the PITCH round than option A; measured on Windows, the install grows from 34 MB to 46 MB and memory after import from about 50 MB to about 76 MB.

## Would change if

Drafted by Claude; approved by Hiep on 13/10/2026.

- The model choice (ADR 0003) lands on a model with no maintained LangChain integration.
- LangChain moves the Gemini chat model, the Gemini embeddings or the in-memory store out of the maintained packages.
- The deployed app on Render (a free web host) runs short of its 512 MB.

## Evidence

The research write-up above, with measurements M1 and M2.
Evidence log line of 13/10/2026 (Claude Opus 5.5 with Agnes 2.5 Flash subagents).

## Technical detail

- Packages: `langchain-core` 1.x and `langchain-google-genai` give `ChatGoogleGenerativeAI`, `with_structured_output`, `GoogleGenerativeAIEmbeddings` and `InMemoryVectorStore`; `google-genai` stays as their dependency.
  `langchain`, `langchain-community` and `langchain-classic` are not installed.
- Rejected options by name: B used `BM25Retriever` from `langchain-community` and `EnsembleRetriever` from `langchain-classic`; A used `google-genai` directly.
- #12: our BM25 and fusion modules sit next to `InMemoryVectorStore`, which receives the scope as a `filter`; the tokenizer follows ADR 0002 (#5).
- #13: the answer and its cited chunk ids come through `with_structured_output`.
- Steps 1-4 and 7: step 1 keeps the current version of each document series, step 2 filters access and applicability, step 3 applies "dùng thay", step 4 marks conflict pairs, step 7 picks the card.
- Plan decision D10 is the working default this ADR amends; the original "Would change if" wording said "R3 (#6)", the issue behind ADR 0003.
