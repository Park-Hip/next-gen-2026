# 0008. Step 6 on gemini-3.5-flash-lite at medium thinking

- Status: Accepted
- Date: 2026-10-14
- Origin: Hiep + AI
- Supersedes: The "Model" line of ADR 0003
- Issue: #41
- Research: None

## Context

ADR 0003 pinned step 6 to `gemini-3.8-flash` at `low` thinking.
On 14/10/2026 that model returned 503 "high demand" and 504 DEADLINE_EXCEEDED (run `results/20261014-1048.jsonl` stopped on row 1, and two probe calls).
AI Studio shows its free tier at 5 RPM and 20 RPD, and one evaluation run needs about 150 calls by ADR 0003's own estimate, which is the "Would change if" case in ADR 0003.
The fallback named there, `gemini-3.6-flash`, has the same 5 RPM and 20 RPD.

Probe results on 14/10/2026 (one run each, throwaway script, with the schema fix from #40 applied):

- `gemini-3.5-flash-lite` (15 RPM, 250K TPM, 500 RPD) answered row 1 (14 ngày) and refused the CEO salary rows 9 and 14 at `low`.
- Row 11 ("Tôi còn bao nhiêu ngày phép?", must refuse): at `low` it answered "14 ngày" in 2 of 2 runs; at `medium` and `high` it refused in 2 of 2 runs each, and row 1 still answered.
- `gemini-3.1-flash-lite` (same limits) returned 503 and is shut down on 07/05/2027.
- `gemma-4-31b-it` (30 RPM, 16K TPM, 14.4K RPD) rejects `thinking_level`, returned 500 and 504, and 16K TPM allows only about 5 calls of about 3K tokens a minute.

These are single probe runs, not measurements of a rate.

## Options considered

1. **`gemini-3.5-flash-lite` at `medium`** - 15 RPM and 500 RPD; refused row 11 at `medium` and `high`.
2. **`gemini-3.8-flash` or `gemini-3.6-flash`** - 5 RPM and 20 RPD; cannot carry a run (and 3.8 returned 503 and 504).
3. **`gemini-3.5-flash-lite` at `high`** - same probe behaviour as `medium`, with more thinking per call.
4. **`gemma-4-31b-it`** - rejects `thinking_level` and its token limit allows about 5 calls a minute.
5. **Another provider** - out of scope for this change.

## Decision

Step 6 uses `gemini-3.5-flash-lite` at `thinking_level: medium`, with `requests_per_minute: 12` (80% of 15, as decision 6 did for 3.8 Flash).

## Reasons

[chờ Hiệp] - Hiep approved the recommendation on issue #41 on 14/10/2026 ("approve implement it") but has not yet given his reasons in his own words.
An agent must not supply them; they are to be added by Hiep or from his words before the PR is merged.

## Consequences

- A full run (15 answer calls) is about 3% of the 500 requests a day, so an evaluation run and the public demo both fit.
- The choice of `medium` rests on one probe of row 11 (2 of 2 refusals); the full run's V3 and refusal results are the real test.
- The model is Flash-Lite, which ADR 0003's research rated weak for careful reading; the evaluation must show whether grounding holds.
- ADR 0006's quota line ("about 75% of a day's answer quota on `gemini-3.8-flash`") no longer applies; this ADR gives the current figure.

## Would change if

- The full run shows over-cautious answers above V3's 10%, or answers where a refusal was expected: revisit the thinking level, then the model.
- The model is shut down or its free-tier limits drop below what a run plus the demo needs.

## Evidence

Probe runs of 14/10/2026 described under Context, and the full run reported in the PR for #41.
Evidence log line of 14/10/2026.
