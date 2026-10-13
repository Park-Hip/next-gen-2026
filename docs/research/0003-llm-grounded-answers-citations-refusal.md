# 0003. Which LLM, and how do we make it answer only from the chunks, cite them, and refuse?

- Status: Draft
- Issue: #6
- Feeds: ADR 0003
- Method: Pi on 13/10/2026, 11:41-15:15.
  Orchestrator: Claude Opus 5.5 (`claude-bridge/claude-opus-5-5`), which wrote the lane prompts, read the installed library source, ran one offline check (C1) and checked the sources.
  Web research: four `researcher` subagents on Agnes 2.5 Flash with max reasoning (`agnes/agnes-2.5-flash:max`).
  A first run with the lanes in pairs failed on all four lanes (Agnes free-tier 429, a timeout and two connection errors); the rerun at 13:06-13:36 ran the lanes one after another, and all four finished on the first attempt.
  Search providers: the `web_search` tool's configured provider.
  Claude then opened every source in the table below itself (page fetch or the installed package source), with no other model involved.
  No live Gemini call was made: Hiep chose on 13/10/2026 to write the research without measuring, so every statement about model behaviour below comes from documents, not from our data.
  Hiep's prompt to Claude, the shared context and the four lane prompts follow verbatim.

```text
Hiep to Claude:
https://github.com/Park-Hip/next-gen-2026/issues/6 research this, use Agnes max reasoning for web search with subagent when needed. then discuss with me

Shared context, sent at the top of each lane:
You are researching one technical decision for a small Python RAG prototype. Today is 2026-10-13. Your own knowledge may be out of date: model names and limits change monthly, so trust only pages you open today.

Project: v1 of an internal-policy assistant for a Vietnamese company, built in about one day inside a 3-day competition. Python, FastAPI + Jinja2, hosted on Render's free web service. All data is simulated.
Data: about 11 simulated Vietnamese HR policy documents in Markdown, chunked by article ("Điều"), about 30-60 chunks in total; each question sees about 5-10 retrieved chunks, each with an id we control such as "LEAVE-PAYCO-v1#Điều 1".
Pipeline: steps 1-4 are deterministic rules that build the asker's allowed scope before retrieval. Step 5 is hybrid retrieval inside that scope. Step 6 is ONE LLM call that must answer only from the retrieved chunks, cite the chunk ids behind each point, or say "không tìm thấy" (not found) when no chunk answers. Step 7 is deterministic: the answer is refused if it has no citation or cites a chunk id that was not retrieved.
Already decided (ADR 0001): the LLM call goes through langchain-core 1.x and langchain-google-genai (ChatGoogleGenerativeAI, with_structured_output), which wraps Google's google-genai SDK. Working default model: Gemini Flash on the free tier of the Gemini API (AI Studio key), the newest Flash the free tier allows; the team believes "gemini-3.8-flash" and "gemini-3.6-flash" are listed as stable on ai.google.dev, but this needs checking. Draft output contract: JSON {found: bool, points: [{text: str, chunks: [chunk_id]}]}.
Evaluation: about 15 test cases, each asked in up to 3 phrasings, each run 3 times (one wrong run counts as a failure), so roughly 100-150 LLM calls per full run, several full runs per day; plus a public demo.
Questions and answers are in Vietnamese.

Rules for your work:
- Use web_search, then OPEN each page you cite with fetch_content. Prefer official docs (ai.google.dev, cloud.google.com, docs.langchain.com, reference.langchain.com), official GitHub repos and source code, PyPI, vendor engineering blogs, and peer-reviewed papers (arXiv, ACL Anthology).
- Every claim needs: the claim, the URL, an exact quote copied from the opened page, and the date the page states (if any).
- If you only saw a search snippet, mark the claim [snippet only]. If you could not find something, say so; never guess numbers, model names or limits.
- Do not write any files. Return your report as your final message.
- Keep the work bounded: at most about 12 searches and 15 page fetches, then write the report.
- Output format: (1) a short summary of findings, (2) a Markdown table: Claim | URL | Exact quote | Page date, (3) a list "Could not verify".

Your lane:

Lane "structured output": making step 6 return valid JSON with chunk ids we control.
1. Gemini API structured output today: response_mime_type, response_schema vs response_json_schema, which JSON Schema keywords are supported (enum, minItems, maxItems, required, propertyOrdering, anyOf), whether output is guaranteed to match the schema (constrained decoding) or best effort, size limits on the schema, and known limitations (ai.google.dev/gemini-api/docs/structured-output and the google-genai SDK docs).
2. Can the schema restrict citation values to the retrieved chunk ids, for example an enum built per request from the 5-10 retrieved ids? Is that supported, and are there limits on enum values or characters such as '#' or Vietnamese letters? Any reports of it working or failing.
3. langchain-google-genai: ChatGoogleGenerativeAI.with_structured_output, its method options (json_schema vs function_calling / tool calling), the default method in the current version, include_raw, how Pydantic models are converted, and known issues (GitHub issues in langchain-ai/langchain-google) with enums, nested lists, Optional fields, or Gemini 3 models. Read the reference docs and the source of the current version.
4. Gemini's own citation features (citation_metadata, grounding_metadata, File Search tool, grounding with your own data): do any cite our own chunk ids, or only Google Search / Google-managed stores? Would any replace our schema approach?
5. Published patterns for answer-with-citations output schemas (for example per-sentence citations, quote + id, "found" flag before or after the answer) and evidence on whether field order matters (reasoning or quotes before the answer).

Lane "grounding prompts": making the model answer only from the chunks, cite each point, and say "không tìm thấy" when no chunk answers.
1. Official prompt guidance from model vendors on grounded answers, citations and refusal: Google's Gemini prompting strategies and Gemini 3 prompting guide (ai.google.dev), Anthropic's "Reduce hallucinations" and long-context tips (extract quotes first, allow "I don't know"), OpenAI's guidance. Quote the exact recommended patterns, and where instructions should sit (system instruction vs user turn, context before or after the question).
2. Research on negative rejection / abstention in RAG: how often LLMs answer when the context lacks the answer, and what helps. For example RGB (Chen et al. 2023, negative rejection), FaithEval, "RAG with unanswerable questions" benchmarks, Trust-Score / Trust-Align, ALCE (citation quality), and any 2025-2026 results for Gemini models. Give the measured numbers and setups.
3. Techniques that reduce citing a valid but non-answering chunk, or misstating a chunk: quote-then-answer, requiring a verbatim supporting quote per point that code can check as a substring of the cited chunk, per-claim citations, self-check / second-pass verification, chain-of-verification. Evidence of effect size, and cost (extra calls).
4. Over-refusal: evidence that strict grounding prompts make models refuse answerable questions, and how papers measure and balance it.
5. Vietnamese-specific: any study of grounded QA, refusal or citation quality in Vietnamese (for example ViRAG, Vietnamese legal QA such as ALQAC or Zalo legal retrieval, VLSP), and whether prompts should be written in Vietnamese or English for Vietnamese answers.

Lane "variance and limits": run-to-run stability and rate limits for step 6.
1. Temperature on current Gemini models (Gemini 3.x Flash): what Google recommends (check whether the docs say to keep temperature at its default of 1.0 for Gemini 3 and what happens if lowered), default values of temperature, top_p, top_k, and whether a seed parameter exists and is honoured. Quote the docs.
2. Determinism: evidence that LLM APIs are non-deterministic even at temperature 0 (for example Thinking Machines "Defeating Nondeterminism in LLM Inference", Google docs statements, papers measuring run-to-run variance), and how evaluations handle it (repeated runs, pass^k, majority vote). Give numbers where published.
3. Thinking level / thinking budget effect on answer stability and on refusal or faithfulness, if any evidence exists.
4. Rate limits in practice: how the Gemini API signals limit errors (429 RESOURCE_EXHAUSTED, retry info), recommended retry and backoff, whether google-genai or langchain-google-genai retries automatically (max_retries, timeouts) and its defaults; whether daily quotas reset at midnight Pacific; how to stay within free limits for about 150 calls per evaluation run (batching, caching responses by prompt hash, context caching).
5. Latency: published or measured latency of Gemini Flash models for short prompts (about 2-4k input tokens, about 300 output tokens), with and without thinking, so a demo answer stays under a few seconds.

Lane "models": which model and provider for step 6.
1. The Gemini API models available today (October 2026): exact model ids of every Flash and Flash-Lite model, which are stable vs preview vs deprecated, and announced shutdown dates (ai.google.dev/gemini-api/docs/models, the changelog, and the deprecations page). Check whether gemini-3.8-flash and gemini-3.6-flash exist and are stable.
2. Free tier: which of these models have a free tier, and the free-tier rate limits (RPM, TPM, RPD) per model (ai.google.dev/gemini-api/docs/rate-limits and the pricing page). Note if the docs say limits are only shown in AI Studio. Note whether free-tier prompts may be used by Google to improve products (terms / pricing page).
3. Thinking: do these Flash models think by default, how to set thinking level or budget, and how thinking affects latency, tokens and free-tier quota.
4. Vietnamese quality: any published benchmark covering Vietnamese for Gemini Flash and its alternatives (for example VMLU, ViLLM-Eval, VLSP shared tasks, MMMLU/Global-MMLU Vietnamese split, Vietnamese RAG or reading-comprehension benchmarks), with scores and dates.
5. Alternatives with a free tier usable from Python that also support JSON-schema output: for example Groq, Cerebras, OpenRouter free models, Mistral (La Plateforme free tier), GitHub Models, Cloudflare Workers AI, Cohere, and open Vietnamese models (Vistral, SeaLLM, Qwen). For each: free limits, structured-output support, and whether langchain has a maintained integration package.
```

## Why it matters for v1

The answer fixes step 6 for #13: the model id, the thinking level, the output schema, the prompt, and how calls are retried.
It also decides what step 7 can check, and how the evaluation in #8 must treat run-to-run noise.

Constraints any option must respect:

- ADR 0001: the call goes through `langchain-core` 1.x and `langchain-google-genai` (`ChatGoogleGenerativeAI.with_structured_output`).
- Working default (D2, D14): Gemini Flash on the free tier.
- The model may only cite ids we control; step 7 refuses an answer with no citation or with a citation outside the retrieved chunks (promise R7 in `docs/mission2/mission1_promises.md`).
- The card comes from rules, never from LLM text (A4), so the model's answer is only an input to step 7.
- Refusal and over-caution are measured: V3 allows at most 10% over-cautious answers, V4 counts a case as failed if one of 3 runs is wrong, and V6 names "misstates a passage" as a known risk.
- About 100-150 calls per evaluation run, several runs a day, plus a public demo, all on free-tier limits we cannot see in public docs (S4).
- Questions and answers are in Vietnamese; all data is simulated, so free-tier data use by Google is acceptable (S3).

## Options found

### Model

| Option | What it is | Strengths | Costs and risks | Fit for v1 | Sources |
|---|---|---|---|---|---|
| A. `gemini-3.8-flash` | Newest stable Flash, released 02/09/2026 | Stable, no shutdown date announced; free on the free tier; the model Google's own examples now use | Thinking is always on: `low`, `medium` (default) or `high`, and `minimal` returns an error; free-tier limits unknown until checked in AI Studio; our langchain version does not list it among fixed-sampling models (harmless, see C1) | Good | S1, S2, S3, S5, S6 |
| B. `gemini-3.6-flash` | Previous-generation stable Flash, released 21/07/2026 | Stable, no shutdown date announced; free; allows `minimal` thinking, the lowest-latency setting | One generation older; Google calls it "previous-generation" | Good as a fallback | S1, S2, S3, S5 |
| C. `gemini-3.5-flash-lite` | Stable Flash-Lite, released 21/07/2026 | Cheapest and fastest; `minimal` thinking by default | Positioned for "high-throughput execution", not careful reading; no evidence on grounded answers | Weak: speed is not our bottleneck | S1, S2, S5 |
| D. A `-latest` alias | `gemini-flash-latest` | Always the newest | "hot-swapped with every new release", so results can change between test runs without a code change | Poor: breaks V4 reproducibility | S1 |
| E. Another provider's free tier (Groq, OpenRouter free models, Cohere) | A non-Gemini model through another langchain package | A second opinion if Gemini fails | Changes ADR 0001's integration; Groq's published limits are for the paid Developer plan (S20); no Vietnamese grounding evidence for any of them | Poor for v1 | S20 |

No published benchmark measures grounded answering, citation or refusal in Vietnamese for any of these models (all four lanes looked; none found).
The only evidence for our case will be our own test rows.

### Output contract

| Option | What it is | Strengths | Costs and risks | Fit for v1 | Sources |
|---|---|---|---|---|---|
| F. Draft contract with free-text ids | `{found, points:[{text, chunks:[str]}]}` | As drafted | The model can type an id we never retrieved; step 7 then refuses the whole answer | Works, with more refusals | S7 |
| G. Per-request `enum` of retrieved ids | Same contract, but `chunks` items are an `enum` of the ids retrieved for this question, built as a Pydantic `Literal` per request | Constrained decoding keeps ids inside the retrieved set; `#` and "Điều" pass through unchanged (C1); step 7's id check stays as a second guard | Values are still not checked for meaning: a valid id can point at a chunk that does not support the point; very large schemas "may be rejected", but ours has 5-10 ids | Good | S7, S8, C1 |
| H. Drop `found`, use an empty `points` list for "không tìm thấy" | `{points:[...]}` | One fewer field; the contradictory "found=true with no points" cannot happen; refusal stays a structured signal, not free text | Small change to the draft contract and to step 7 | Good | S7, S12 |
| I. Add a verbatim `quote` per point | `{text, quote, chunks}`; step 7 checks that `quote` is a substring of the cited chunk text | Deterministic, no extra call; directly targets V6 "misstates a passage"; matches vendor advice to ground in word-for-word quotes | A true quote that does not answer the question still passes; Vietnamese text needs Unicode normalisation (NFC) and whitespace folding before the substring test; a new step 7 rule | Good | S11, S10 |
| J. Gemini's own citations (File Search, grounding metadata) | Upload documents to a Google-managed File Search store and read its citation annotations | Built in | Citations name Google's file and source, not our chunk ids, so step 7 and the scope rules (R8) cannot use them | Poor | S9 |

Field order: since Gemini 2.5, the output keeps the key order of the schema (S8).
So a field placed first is generated first; whether that improves answers was not tested by any source found.

### Prompt

| Option | What it is | Strengths | Costs and risks | Fit for v1 | Sources |
|---|---|---|---|---|---|
| K. Google's layout | Rules and output format in the system instruction; chunks first, question last after "Based on the information above..." | Google's own guidance for Gemini 3 | None found | Good | S10 |
| L. Google's "strictly grounded assistant" clause | A ready system-instruction paragraph: rely only on the context, and "state that the information is not available" when the answer is not written there | Vendor template, written for grounding | Strict refusal wording raised refusals on answerable questions in older models (S14, S15); our V3 limit makes this a risk to measure | Good, measured against V3 | S10, S14, S15 |
| M. Anthropic's three techniques | Allow "I don't know"; extract word-for-word quotes first; drop any claim without a supporting quote | Directly supports option I | Written for Claude, not Gemini | Good as principles | S11 |
| N. Second verification call (chain-of-verification) | A second LLM pass that checks each point | Catches misstatements | 2-4 calls per question against unknown free-tier limits; the effect sizes found were not on our task (lane report, not checked by Claude) | Poor for v1 | - |
| O. Prompt language | Rules in English or in Vietnamese; answers in Vietnamese either way | - | No study compares the two for Vietnamese grounded answers (grounding lane found none) | Either; low stakes | - |

### Run-to-run variance, retries and limits

| Option | What it is | Strengths | Costs and risks | Fit for v1 | Sources |
|---|---|---|---|---|---|
| P. Leave sampling at the defaults | Never set `temperature`, `top_p`, `top_k` | Google deprecated them from 3.6 Flash on and says the API ignores them; Gemini 3 is tuned for 1.0; langchain leaves temperature unset for Gemini 3 (C1) | Answers vary between identical calls | Good, the only real choice | S5, S6, C1 |
| Q. Try to force determinism | `temperature=0`, `seed` | - | Ignored by 3.6 Flash and later, and "returns an error in future model generations"; even temperature 0 does not give identical outputs (S16, S17) | Poor | S5, S16, S17 |
| R. Measure variance with repeated runs | Each case 3 times, one wrong run fails the case (V4) | Matches the evidence that single runs hide flips | 3x the calls | Good, already promised | S16, S17 |
| S. Built-in retries | `max_retries` (default 6 in `langchain-google-genai` 4.4.1), passed to the SDK as `attempts=6` on normal calls | No code needed | Does not apply to streaming calls (open issue #1652, S19); a 429 on a daily limit cannot be fixed by retrying | Good, non-streaming | C1, S19 |
| T. Cache answers by prompt hash between evaluation runs | Reuse an earlier answer for the same prompt | Saves calls | Hides exactly the run-to-run variance V4 must catch | Poor for evaluation; acceptable only for the demo | - |

### Checked by Claude on 13/10/2026

**C1, what `with_structured_output` sends (offline, no API call).**
In a throwaway environment with `langchain-google-genai` 4.4.1 and `google-genai` 2.30.0, Claude built a Pydantic model with `chunks: list[Literal[<3 chunk ids>]]` and `min_length=1`, called `with_structured_output` on `ChatGoogleGenerativeAI(model="gemini-3.8-flash", thinking_level="low")`, and printed the request config langchain builds, without sending it.

- `response_mime_type` was `application/json` and the schema went in `response_json_schema`, so the default method is Gemini's native JSON schema.
- `chunks` became `{"type": "array", "items": {"type": "string", "enum": ["LEAVE-PAYCO-v1#Điều 1", ...]}, "minItems": 1}`; the ids kept `#` and the Vietnamese letters.
- `temperature` was `None` (not sent), because langchain clears its 0.7 default for Gemini 3 and later unless the caller sets it (S18).
- `thinking_level` was passed as `LOW`, and retries as `attempts=6`.

This shows what is sent, not how Gemini answers; whether the model respects the enum on our data was not tested.

## Claims that did not hold up

1. **"langchain-google-genai silently does no retries" (variance lane, citing issue #1652).**
   The issue's title is "`max_retries` has no effect on streaming requests"; for normal calls the installed 4.4.1 passes `attempts=6` to the SDK (C1, S19).
2. **"Groq free tier: 30 RPM and 1K RPD on GPT-OSS-120B" (models lane).**
   The page says these are "the base limits for the Developer plan", which is paid (S20).
3. **"Rate limits are approximately 20 req/day for 3.x Flash models" (structured lane).**
   No source on the page; Google publishes no free-tier numbers and points to AI Studio (S4).
4. **"langchain overrides temperature to 1.0 for Gemini 3" (variance lane, implied).**
   The installed source sets it to `None`, so it is not sent at all (S18).
5. **Artificial Analysis latency: about 3 s to first token for 3.8 Flash at `low` thinking, 21 s at `high`, 17 s for 3.6 Flash (variance lane).**
   The page text has no numbers; they sit in charts, and the 3.6 figure was a search snippet only (S21).
   Not used.
6. **"Cache responses by prompt hash" as a way to save calls during evaluation (variance lane).**
   Not false, but it would hide the run-to-run variance that V4 measures, so it is excluded for evaluation.
7. **"Constrained decoding is guaranteed for syntax/structure, not for semantic correctness" (structured lane), given as a quote.**
   That wording is not on the cited page; the conclusion holds through the Gemini docs' own words: "While output is syntactically correct JSON, always validate values in your application" (S7).
8. **"Putting `found` before `points` helps the model commit to an answer direction" (structured lane).**
   The lane marked this as its own inference; no source tests it.
9. **"Free tier offers rate-limited access to 3.8, 3.7, 3.6, 3.5 Flash" (structured lane).**
   3.7 Flash and 3.5 Flash were deprecated on 08/10/2026 and now route to 3.8 and 3.6 (S2).

Not checked by Claude, so not used above: V-Bench scores (Gemini 3.6 Flash 76.9, Claude Opus 5 81.2), Cohere's 1,000 calls a month, OpenRouter's free model list, ALCE's "around 50%" unsupported generations, chain-of-verification's FactScore gain, and the ViRE retrieval results (those belong to R2, #5).

## AI recommendation (not a decision)

Claude's picks, each with its one-line reason (Claude's):

- **Model:** option A, `gemini-3.8-flash` with `thinking_level="low"`, pinned by its exact id; B (`gemini-3.6-flash`) as the fallback if the free-tier limits in AI Studio are too tight.
  Reason: it is the newest stable Flash and free, and `low` is Google's advice for fact retrieval while keeping the demo responsive.
- **Output contract:** G plus H plus I, that is `{points:[{text, quote, chunks}]}` with `chunks` as a per-request enum, an empty list meaning "không tìm thấy", and step 7 checking ids and quote substrings.
  Reason: each piece removes one failure mode with deterministic code instead of trusting the model, at no extra call.
- **Prompt:** K plus L plus M: Google's layout, its strict-grounding clause, and an explicit "say không tìm thấy" permission, with rules in English and answers required in Vietnamese.
  Reason: these are the vendor's own patterns; the language choice has no evidence either way and is cheap to swap.
- **Variance and limits:** P, R and S: no sampling parameters, 3 runs per case as V4 already promises, the default 6 retries on non-streaming calls, no answer caching during evaluation.
  Reason: the docs leave no other option for sampling, and V4 already handles the noise.

The strongest alternative: keep the draft contract (F with `found`) and add only the enum, if Hiep weighs the smallest change to the Mission 1 design above catching misstated passages.

Open risk the documents cannot settle: refusal.
In RGB the best model refused only 45% of unanswerable questions (S12), and refusal instructions raised refusals on answerable ones (S14, S15); both are older models.
Only our refusal rows (V3, V6) can show where Gemini 3.8 Flash falls, so the first full evaluation run in #8 is the real test of this choice.

Questions for Hiep before the ADR: which option in each table, and in your own words why it beats the strongest alternative.

## Sources

All accessed 2026-10-13 by Claude.
"Installed source" means the file in the package version named, installed from PyPI on that day.

| ID | Title and URL | Accessed | Quote that supports the claim |
|---|---|---|---|
| S1 | Gemini API, Models, https://ai.google.dev/gemini-api/docs/models | 2026-10-13 | "Our most intelligent Flash model ... New Stable" (gemini-3.8-flash); "Our previous-generation Flash model ... Stable" (gemini-3.6-flash); "Stable models usually don't change. Most production apps should use a specific stable model."; "This alias will get hot-swapped with every new release of a specific model variation." |
| S2 | Gemini deprecations, https://ai.google.dev/gemini-api/docs/deprecations, and Release notes, https://ai.google.dev/gemini-api/docs/changelog | 2026-10-13 | "`gemini-3.8-flash` September 2, 2026 No shutdown date announced"; "`gemini-3.6-flash` July 21, 2026 No shutdown date announced"; "`gemini-3.1-flash-lite` May 7, 2026 May 7, 2027"; release notes, October 8, 2026: "gemini-3.7-flash is deprecated and has been replaced by gemini-3.8-flash"; "gemini-3.5-flash is deprecated and has been replaced by gemini-3.6-flash" |
| S3 | Gemini Developer API pricing, https://ai.google.dev/gemini-api/docs/pricing | 2026-10-13 | Free tier: "Free input & output tokens", "Content used to improve our products"; gemini-3.8-flash: "Input price Free of charge $0.75 through December 31, 2026"; "Output price (including thinking tokens) Free of charge $3.75 through December 31, 2026" |
| S4 | Rate limits, https://ai.google.dev/gemini-api/docs/rate-limits | 2026-10-13 | "Rate limits are applied per project, not per API key. Requests per day (RPD) quotas reset at midnight Pacific time."; "Rate limits depend on a variety of factors (such as your usage tier) and can be viewed in Google AI Studio." |
| S5 | Gemini thinking, https://ai.google.dev/gemini-api/docs/thinking; Gemini 3.8 Flash model page, https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash (last updated 2026-09-02) | 2026-10-13 | Table: "gemini-3.8-flash On (medium) low, medium, high"; "gemini-3.6-flash On (medium) minimal, low, medium, high"; "Simple tasks: Use minimal or low thinking for fact retrieval or classification"; model page: "Note: minimal is not supported and returns an error." |
| S6 | What's new in Gemini 3.6, https://ai.google.dev/gemini-api/docs/whats-new-gemini-3.6 (last updated 2026-10-09); Gemini 3 developer guide, https://ai.google.dev/gemini-api/docs/gemini-3 | 2026-10-13 | "Starting with Gemini 3.6 Flash and Gemini 3.5 Flash-Lite, the following API changes apply to these models and all future Gemini model releases. Sampling parameter deprecation: temperature, top_p, and top_k are deprecated. The API ignores these parameters and returns an error in future model generations."; Gemini 3 guide: "For all Gemini 3 models, we strongly recommend keeping the temperature parameter at its default value of 1.0." and "Changing the temperature (setting it below 1.0) may lead to unexpected behavior, such as looping or degraded performance" |
| S7 | Structured outputs, https://ai.google.dev/gemini-api/docs/structured-output | 2026-10-13 | "For string values: enum: Lists a specific set of possible strings for classification tasks."; "Validation: While output is syntactically correct JSON, always validate values in your application."; "Schema complexity: Very large or deeply nested schemas may be rejected." |
| S8 | Improving Structured Outputs in the Gemini API, Google blog, 05/11/2025, https://blog.google/innovation-and-ai/technology/developers-tools/gemini-api-structured-outputs | 2026-10-13 | "the API now preserves the same order as the ordering of keys in the schema. This is supported for all Gemini 2.5 models and beyond" |
| S9 | File Search, https://ai.google.dev/gemini-api/docs/file-search | 2026-10-13 | "the model's response may include citations that specify which parts of your uploaded documents were used"; the example prints `annotation.file_name` and `annotation.source` for `file_citation` annotations |
| S10 | Prompt design strategies, https://ai.google.dev/gemini-api/docs/prompting-strategies (last updated 2026-09-17) | 2026-10-13 | "supply all the context first. Place your specific instructions or questions at the very end of the prompt."; "use a clear transition phrase ... such as "Based on the information above...""; "You are a strictly grounded assistant limited to the information provided in the User Context." ... "If the exact answer is not explicitly written in the context, you must state that the information is not available." |
| S11 | Reduce hallucinations, Anthropic, https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations | 2026-10-13 | "Explicitly give Claude permission to admit uncertainty."; "ask Claude to extract word-for-word quotes first before performing its task"; "If it can't find a quote, it must retract the claim." |
| S12 | Chen et al., Benchmarking Large Language Models in Retrieval-Augmented Generation (RGB), AAAI 2024, https://arxiv.org/html/2309.01431v2 | 2026-10-13 | "The highest rejection rates for LLMs in English and Chinese were only 45% and 43.33%, respectively."; "they often generate unpredictable responses, which make it hard to use them as state triggers (such as for recognizing rejection)"; Table 3: ChatGPT English Rej 24.67, Rej* 45.00 |
| S13 | Ming et al., FaithEval, https://arxiv.org/html/2410.03727 | 2026-10-13 | "Abstaining is challenging, even when explicitly instructed."; "Across all chat models, the performance gap ranges from 13.6% to 68.4%." |
| S14 | FaithEval, same paper, Section 5 and Table 1 | 2026-10-13 | "Having the additional task instruction degrades the performance on normal contexts consistently."; "Claude 3.5 experiencing a 5% decrease in average accuracy" |
| S15 | Song et al., Measuring and Enhancing Trustworthiness of LLMs in RAG through Grounded Attributions and Learning to Refuse (Trust-Score), https://arxiv.org/html/2409.11242v4 | 2026-10-13 | "Under the default prompt, models rarely refuse (AR% close to 100), while adding a refusal prompt in ICL drastically reduces AR%, often to near zero, indicating indiscriminate refusal." |
| S16 | Thinking Machines, Defeating Nondeterminism in LLM Inference, https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/ | 2026-10-13 | "We use Qwen/Qwen3-235B-A22B-Instruct-2507 and sample 1000 completions at temperature 0 ... Surprisingly, we generate 80 unique completions" |
| S17 | Tamba, Necessary but Not Sufficient: Temperature Control and Reproducibility in LLM-as-Judge Safety Evaluations, arXiv 2606.26185, 24/06/2026, https://arxiv.org/abs/2606.26185 | 2026-10-13 | "pinning temperature=0 reduces but does not eliminate flips"; "harnesses that report single-run verdicts without variance or grader-disagreement metrics can present noise as a safety property" |
| S18 | `ChatGoogleGenerativeAI`, installed source of langchain-google-genai 4.4.1, `langchain_google_genai/_common.py` and `chat_models.py` | 2026-10-13 | `temperature: float \| None = 0.7`; `max_retries: int = Field(default=6, alias="retries")`; `if "temperature" not in self.model_fields_set and _is_gemini_3_or_later(self.model): self.temperature = None`; `method: Literal["function_calling", "json_mode", "json_schema"] \| None = "json_schema"`; `_FIXED_SAMPLING_AND_NO_PREFILL_MODELS = frozenset({"gemini-3.5-flash-lite", "gemini-3.6-flash"})` |
| S19 | langchain-ai/langchain-google issue #1652, https://github.com/langchain-ai/langchain-google/issues/1652 (opened 2026-03-19, open) | 2026-10-13 | "ChatGoogleGenerativeAI - `max_retries` has no effect on streaming requests (`_astream` / `generate_content_stream`)" |
| S20 | Groq rate limits, https://console.groq.com/docs/rate-limits | 2026-10-13 | "Note that the limits shown below are the base limits for the Developer plan"; "openai/gpt-oss-120b 30 1K 8K 200K" |
| S21 | Artificial Analysis, Gemini 3.8 Flash (low), https://artificialanalysis.ai/models/gemini-3-8-flash-low | 2026-10-13 | The page text shows chart titles and "No publicly available API", no latency figures |

## How the check was run

<details>
<summary>C1 script (run in a throwaway virtual environment outside the repository, no API key, no network call)</summary>

Environment: `uv venv -p 3.12` and `uv pip install langchain-core langchain-google-genai` (langchain-core 1.6.10, langchain-google-genai 4.4.1, google-genai 2.30.0).

```python
# Offline check: what response_json_schema does with_structured_output send for a per-request citation enum?
import json
from typing import Literal
from pydantic import BaseModel, Field, create_model
from langchain_google_genai import ChatGoogleGenerativeAI

ids = ["LEAVE-PAYCO-v1#Điều 1", "LEAVE-PAYCO-v1#Điều 2", "LEAVE-GROUP-v1#Điều 1"]
ChunkId = Literal[tuple(ids)]
Point = create_model("Point", text=(str, Field(description="One point of the answer")), chunks=(list[ChunkId], Field(min_length=1)))
Answer = create_model("Answer", found=(bool, ...), points=(list[Point], ...))

llm = ChatGoogleGenerativeAI(model="gemini-3.8-flash", google_api_key="dummy-offline")
print("temperature:", llm.temperature, "max_retries:", llm.max_retries, "thinking_level:", llm.thinking_level)
chain = ChatGoogleGenerativeAI(model="gemini-3.8-flash", google_api_key="dummy-offline", thinking_level="low").with_structured_output(Answer)
bound = chain.first
print(json.dumps({k: v for k, v in bound.kwargs.items() if k != "ls_structured_output_format"}, ensure_ascii=False, indent=1))
# Build the real request config without sending it
from langchain_core.messages import HumanMessage
req = bound.bound._prepare_request([HumanMessage("x")], **{k: v for k, v in bound.kwargs.items() if k != "ls_structured_output_format"})
cfg = req["config"]
print("response_mime_type:", cfg.response_mime_type, "temperature:", cfg.temperature, "thinking:", cfg.thinking_config, "retries:", cfg.http_options.retry_options if cfg.http_options else None)
```

Last line of output:

```text
response_mime_type: application/json temperature: None thinking: include_thoughts=None thinking_budget=None thinking_level=<ThinkingLevel.LOW: 'LOW'> retries: attempts=6 initial_delay=None max_delay=None exp_base=None jitter=None http_status_codes=None
```

</details>
