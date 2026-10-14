# 0003. Step 6 on gemini-3.8-flash at low thinking, citing only retrieved ids, with a quote that step 7 checks

- Status: Accepted; its "Evaluation" line is superseded by ADR 0006 and its "Model" line by ADR 0008
- Date: 2026-10-13
- Origin: AI, accepted
- Supersedes: None (fixes the working default of plan decision D2; replaces the draft output contract `{found, points}` in issue #6)
- Issue: #6
- Research: `docs/research/0003-llm-grounded-answers-citations-refusal.md`

## Context

Step 6 is one LLM call that must answer only from the retrieved chunks, cite the chunk ids behind each point, or say "không tìm thấy".
This is the riskiest assumption named in Mission 1 (V2, V6): one unsafe answer disproves it.
ADR 0001 fixed the integration (`ChatGoogleGenerativeAI.with_structured_output`), and ADR 0002 sends the top 5 chunks to the model.
Plan decision D2 left the model as a working default: the newest Flash the Gemini free tier allows.
The research found that `gemini-3.8-flash` and `gemini-3.6-flash` are both stable, that Gemini no longer honours `temperature`, `top_p` and `top_k`, that its JSON output is valid JSON but its values are not checked for meaning, and that refusal is where models fail most in published benchmarks.
No live Gemini call was made: the research was written from documents, the installed library source and one offline check, not from our data.

## Options considered

1. **Model** - `gemini-3.8-flash` (chosen); `gemini-3.6-flash`; `gemini-3.5-flash-lite`; a `-latest` alias; another provider's free tier.
2. **Output contract** - draft `{found, points:[{text, chunks}]}` with free-text ids; per-request enum of retrieved ids (chosen); empty `points` for "không tìm thấy" instead of `found` (chosen); a verbatim `quote` per point (chosen); Gemini's own File Search citations.
3. **Prompt** - Google's layout (chosen); Google's strict-grounding clause (chosen); Anthropic's quote and "I don't know" techniques (chosen as principles); a second verification call; rules in Vietnamese or in English.
4. **Variance and limits** - default sampling (chosen); forcing determinism with `temperature=0` or `seed`; repeated runs per case (chosen); built-in retries (chosen); caching answers between evaluation runs.

The strongest alternative: keep the draft contract with `found` and add only the enum, as the smallest change to the Mission 1 design.

## Decision

- **Model:** `gemini-3.8-flash`, pinned by its exact id, with `thinking_level="low"`.
  Fallback: `gemini-3.6-flash` at `low`, if the free-tier limits shown in AI Studio are too tight for the evaluation and the demo.
- **Output contract:** `{points: [{text, quote, chunks}]}`.
  - `chunks` is a non-empty list whose items are an enum of the ids retrieved for this question, built per request.
  - `quote` is a word-for-word passage from one of the cited chunks that supports `text`.
  - An empty `points` list means "không tìm thấy".
- **Step 7 adds one rule:** the answer is refused, as for a citation outside the retrieved chunks, when a point's `quote` is not a substring of any chunk it cites, compared after Unicode NFC and whitespace folding.
- **Prompt:** the rules, the output format and Google's "strictly grounded assistant" clause go in the system instruction, written in English, with explicit permission to return no points and the answer required in Vietnamese.
  The user turn gives the chunks first, each with its id, and the question last after "Based on the information above".
- **Sampling and retries:** never set `temperature`, `top_p`, `top_k` or `seed`; use non-streaming calls with langchain's default 6 retries.
- **Evaluation:** each case runs 3 times and one wrong run fails it (V4); answers are never cached between evaluation runs.

## Reasons

Hiep took the research's recommendation as it stands (Hiep, 13/10/2026).

The comparison behind the recommendation is Claude's, in the research write-up under "AI recommendation", not Hiep's reasoning.

## Consequences

Drafted by Claude from the research; approved by Hiep on 13/10/2026.

- #13 builds the Pydantic answer model per request, with `chunks` as a `Literal` of the retrieved ids; the offline check C1 showed langchain sends it as a JSON-schema enum with `#` and "Điều" intact.
- #13 tests, with a fake LLM: a quote not found in the cited chunk gives a refusal; empty `points` gives the "không tìm thấy" refusal; an id outside the retrieved chunks still gives a refusal (R7), even though the enum should prevent it.
- The quote check catches a misstated passage (V6) without an extra call, but not a true quote that does not answer the question; only the manual reading in V3 catches that.
- Answers vary between identical calls, and nothing in the API can stop it; the 3 runs per case in #14 are the only measure of that noise.
- The model thinks on every call (`minimal` returns an error on 3.8 Flash); `low` keeps that short, but demo latency is not measured yet.
- Free-tier limits are unknown until Hiep reads them in AI Studio; free-tier prompts may be used by Google, which is acceptable because all data is simulated ("giả lập").
- `langchain-google-genai` 4.4.1 does not list 3.8 Flash among its fixed-sampling models; this is harmless because we never set a temperature.
- The in-memory answer cache in #13 is for the public demo only, as #13 already says.
- Not yet measured: how often 3.8 Flash refuses an answerable question (V3 allows at most 10%) or answers an unanswerable one; the first full run in #14 is the real test of this decision.

## Would change if

Drafted by Claude from the research; approved by Hiep on 13/10/2026.

- AI Studio shows free-tier limits for 3.8 Flash that cannot carry about 150 calls per evaluation run plus the demo: switch to `gemini-3.6-flash`.
- The evaluation finds over-cautious answers above V3's 10%, or answers where a refusal was expected: revisit the strict-grounding clause and the thinking level first.
- The quote check refuses correct answers often because the model paraphrases instead of quoting: revisit the quote rule or its prompt wording.
- Gemini rejects the enum schema, or `gemini-3.8-flash` is deprecated.

## Evidence

The research write-up above, with the offline check C1 and its script.
Evidence log line of 13/10/2026 (Claude Opus 5.5 with Agnes 2.5 Flash subagents).
