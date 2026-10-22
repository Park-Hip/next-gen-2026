# 0003. Step 6 on gemini-3.8-flash at low thinking, citing only retrieved ids, with a quote that step 7 checks

- Status: Accepted; its "Evaluation" line is superseded by ADR 0006, its "Model" line by ADR 0008, its `text` field by ADR 0009, and its prompt rules by ADR 0011
- Date: 2026-10-13
- Origin: AI, accepted
- Supersedes: None (fixes the working default of plan decision D2; replaces the draft output contract `{found, points}` in issue #6)
- Issue: #6
- Research: `docs/research/0003-llm-grounded-answers-citations-refusal.md`

## In short

- **The problem:** The AI must answer only from the clauses it is given, say which clauses support each point, or say "không tìm thấy".
  One unsafe answer disproves the whole design, and refusing is where AI models fail most in published benchmarks.
  Citing a clause by its id is not enough: the AI could cite the right clause and still misstate it.
- **The decision:** The AI may cite only the clauses retrieved for this question, and for each point it must also copy, word for word, the passage that supports it.
  Fixed rules then refuse the whole answer if a copied passage is not in a clause the point cites.
  An empty list of points means "không tìm thấy".
  The model is `gemini-3.8-flash` with a low "thinking" setting.
- **What the employee sees:** Either an answer backed by a quote that was checked against its source, or a refusal; never a citation to a clause the system did not retrieve.
- **What we give up:** The check catches a misstated passage, but not a true quote that does not answer the question; only manual reading catches that.
  Answers vary between identical calls, and nothing in the API can stop it.
  How often the model wrongly refuses was not yet measured.

## Context

Step 6 is one AI call.
It must answer only from the retrieved clauses, cite the ids of the clauses behind each point, or say "không tìm thấy".
This is the riskiest assumption named in Mission 1: one unsafe answer disproves it.
ADR 0001 fixed how the AI is called, and ADR 0002 sends the top 5 clauses to the model.
Plan decision D2 left the model as a working default: the newest Flash model the Gemini free tier allows.
The research found that `gemini-3.8-flash` and `gemini-3.6-flash` are both stable, and that Gemini no longer honours `temperature`, `top_p` and `top_k` (the settings that control randomness).
It also found that Gemini's JSON output is valid JSON but its values are not checked for meaning, and that refusal is where models fail most in published benchmarks.
No live Gemini call was made: the research was written from documents, the installed library source and one offline check, not from our data.

## Options considered

1. **Model** - `gemini-3.8-flash` (chosen); `gemini-3.6-flash`; `gemini-3.5-flash-lite`; a `-latest` alias; another provider's free tier.
2. **Output contract** (the shape of the AI's reply):
   - the draft: `found` plus a list of points, each with free text and free-text clause ids;
   - a per-request list of allowed ids, the retrieved ones (chosen);
   - an empty list of points for "không tìm thấy", instead of `found` (chosen);
   - a word-for-word `quote` per point (chosen);
   - Gemini's own File Search citations.
3. **Prompt** - Google's layout (chosen); Google's strict-grounding clause (chosen); Anthropic's "quote first" and "say I don't know" techniques (chosen as principles); a second verification call; rules in Vietnamese or in English.
4. **Variance and limits** - default sampling (chosen); forcing determinism with `temperature=0` or `seed`; repeated runs per case (chosen); built-in retries (chosen); caching answers between evaluation runs.

The strongest alternative: keep the draft contract with `found` and add only the list of allowed ids, as the smallest change to the Mission 1 design.

## Decision

- **Model:** `gemini-3.8-flash`, pinned by its exact id, with `thinking_level="low"`.
  Fallback: `gemini-3.6-flash` at `low`, if the free-tier limits shown in AI Studio are too tight for the evaluation and the demo.
  (AI Studio is Google's console where the free-tier limits are shown.)
  (Superseded by ADR 0008.)
- **Output contract:** each point has `text`, `quote` and `chunks`.
  - `chunks` is a non-empty list whose items may only be the ids of the clauses retrieved for this question, a list built per request.
  - `quote` is a word-for-word passage from one of the cited clauses that supports `text`.
  - An empty list of points means "không tìm thấy".
- **Step 7 (the fixed rules that check the answer and pick the card) adds one rule:** the answer is refused, as for a citation outside the retrieved clauses, when a point's `quote` is not a substring of any clause it cites, compared after Unicode NFC and whitespace folding (so that equivalent accented forms and extra spaces do not matter).
- **Prompt:** the rules, the output format and Google's "strictly grounded assistant" clause go in the system instruction, written in English, with explicit permission to return no points and the answer required in Vietnamese.
  The user turn gives the clauses first, each with its id, and the question last after "Based on the information above".
  (Superseded by ADR 0011.)
- **Sampling and retries:** never set `temperature`, `top_p`, `top_k` or `seed`; use non-streaming calls with LangChain's default of 6 retries.
- **Evaluation:** each case runs 3 times and one wrong run fails it; answers are never cached between evaluation runs.
  (Superseded by ADR 0006.)

## Reasons

Hiep took the research's recommendation as it stands (Hiep, 13/10/2026).

The comparison behind the recommendation is Claude's, in the research write-up under "AI recommendation", not Hiep's reasoning.

## Consequences

Drafted by Claude from the research; approved by Hiep on 13/10/2026.

- The answer model is built per request, with the ids as a fixed list of allowed values.
  An offline check showed that LangChain sends it to Gemini as an enum with the `#` and "Điều" characters intact.
- Tests with a fake AI must show three refusals: a quote not found in the cited clause; an empty list of points ("không tìm thấy"); and an id outside the retrieved clauses even though the list of allowed ids should prevent it.
- The quote check catches a misstated passage without an extra call, but not a true quote that does not answer the question; only the manual reading catches that.
- Answers vary between identical calls, and nothing in the API can stop it; the 3 runs per case are the only measure of that noise.
- The model thinks on every call (`minimal` returns an error on 3.8 Flash); `low` keeps that short, but demo latency is not measured yet.
- Free-tier limits are unknown until Hiep reads them in AI Studio.
  Free-tier prompts may be used by Google, which is acceptable because all data is simulated ("giả lập").
- `langchain-google-genai` 4.4.1 does not list 3.8 Flash among its fixed-sampling models; this is harmless because we never set a temperature.
- The in-memory answer cache is for the public demo only.
- Not yet measured: how often 3.8 Flash refuses an answerable question (the Mission 1 target allows at most 10%) or answers an unanswerable one; the first full run is the real test of this decision.

## Would change if

Drafted by Claude from the research; approved by Hiep on 13/10/2026.

- AI Studio shows free-tier limits for 3.8 Flash that cannot carry about 150 calls per evaluation run plus the demo: switch to `gemini-3.6-flash`.
- The evaluation finds over-cautious answers above the 10% target, or answers where a refusal was expected: revisit the strict-grounding clause and the thinking level first.
- The quote check refuses correct answers often because the model paraphrases instead of quoting: revisit the quote rule or its prompt wording.
- Gemini rejects the enum schema, or `gemini-3.8-flash` is deprecated.

## Evidence

The research write-up above, with the offline check C1 and its script.
Evidence log line of 13/10/2026 (Claude Opus 5.5 with Agnes 2.5 Flash subagents).

## Technical detail

- Integration: `ChatGoogleGenerativeAI.with_structured_output` (ADR 0001).
- Output contract: `{points: [{text, quote, chunks}]}`; the draft in issue #6 was `{found, points:[{text, chunks}]}`.
  `chunks` is a `Literal` of the retrieved ids, built per request as a Pydantic model (#13) and sent as a JSON-schema enum.
- Step 7 rule: `quote` must be a substring of a cited chunk after NFC and whitespace folding (`fold` in `src/appota_kb/services/citations.py`); the refusal reasons are `quote_mismatch` and `outside_retrieved`.
- #13 tests with a fake LLM: quote not in the cited chunk gives a refusal; empty `points` gives the "không tìm thấy" refusal; an id outside the retrieved chunks gives a refusal (R7, the Mission 1 promise that a citation of a clause that was not retrieved refuses the whole answer).
- Config: `llm.model`, `llm.thinking_level`, `llm.max_retries: 6` (this ADR names it in `config.yaml`); the current model and thinking level are those of ADR 0008.
- The quote check answers V6; the manual reading is V3; the noise measure is the 3 runs per case in #14 (replaced by ADR 0006); V4 is the Mission 1 promise of 3 runs per case.
- The in-memory answer cache is #13 and is for the demo only.
- Plan decision D2 is the working default; the offline check is C1.
