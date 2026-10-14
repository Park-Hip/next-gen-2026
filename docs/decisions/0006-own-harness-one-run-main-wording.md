# 0006. Evaluate with our own harness: one run per case, main wording only, unsafe answers judged on the card and on the raw reply

- Status: Accepted
- Date: 2026-10-14
- Origin: Hiep + AI
- Supersedes: Mission 1 V4 (each case run 3 times) and the 3 phrasings of A2 and V1 (`docs/mission2/mission1_promises.md`); the "Evaluation" line of ADR 0003
- Issue: #8
- Research: `docs/research/0005-how-to-evaluate-a-small-rag.md`

## Context

#14 must show where the product is good and where it is not, in the brief's format "Kỳ vọng → Kết quả thực tế → Đạt/Chưa đạt → Điều học được".
Mission 1 promised the gates of V3 (rules correct in every case, 0 leaks, 0 unsafe answers, faithfulness read by hand, at most 10% over-cautious), 3 phrasings per row (A2) and 3 runs per case (V4), and rejected an LLM judge (V1).
The free tier of `gemini-3.8-flash` that Hiep read in AI Studio allows 5 requests per minute and 20 per day, shared by the evaluation and the public demo; 15 rows in 3 phrasings and 3 runs would need about 135 answer calls.
The research found that the RAG libraries judge faithfulness with a second LLM, and that their deterministic checks are one line each in our own code.

## Options considered

1. **Harness** - our own (chosen); RAGAS; DeepEval; promptfoo; Inspect AI; Langfuse experiments.
2. **Faithfulness and citations** - hand reading of every answer (chosen); deterministic checks from the test file (chosen); key facts per answer row (chosen); an LLM judge; an NLI or hallucination classifier.
3. **Where an unsafe answer is counted** - on the card the employee sees; on the raw model reply; both, with the card as the gate (chosen).
4. **Repeats** - one run per case (chosen); one run plus declared spot repeats; re-running a failed row until it passes.
5. **Running under the quota** - run and score as two steps (chosen); API errors recorded as errors (chosen); the Gemini Batch API.

The strongest alternative: DeepEval with only custom `BaseMetric` checks, for its test runner and report.

## Decision

- **Harness:** `eval/run.py` calls the same `Answerer` and step 7 as the page, with no cache, and writes one JSON line per row to `results/`: persona, as-of date, question, model id, commit, retrieved ids, raw reply, card, refusal reason, latency.
  A separate scoring step reads that file offline, applies the checks and generates `docs/mission2/test_report.md`; it is unit-tested in CI with fake replies.
  No evaluation library is added.
- **Wording:** each row is asked only in its main wording, the first entry of `questions` in `data/test_cases.yaml`; the other wordings stay in the file and in the offline tests, which cost no quota.
- **Runs:** each case runs once; there are no spot repeats; a failed run is never re-run to get a pass.
  The report says that each case ran once and that run-to-run variance is not measured.
- **Checks:**
  - Deterministic, from the test file: the card kind; answer rows cite every `must_cite` and nothing outside `must_cite` + `may_cite`; conflict rows cite one of `conflict_pair`; no `forbidden_for_llm` citation; no `must_not_contain` text; retrieved ids inside the scope.
  - A new field `key_facts` on answer rows, each of which must appear in the answer text after NFC and whitespace folding; Hiep reviews the values.
  - Hiep reads every answer by hand against the chunks it cites, from a generated review sheet that shows each quote beside the full chunk text.
- **Unsafe answers:** the gate is the card the employee sees (an answer card where a refusal or conflict was expected, a wrong key fact, or a `forbidden_for_llm` citation).
  The raw model reply is reported beside it: a refusal row where the model returned points, or a forbidden citation, counts against V6 even when step 7 refused it.
- **Limitation rows** (`kind: limitation`, today row 15) are reported as the failing case the brief asks for, outside the gates.
- **Numbers:** counts as "k of n", with the exact one-sided 95% upper bound 1 - 0.05^(1/n) when k is 0, the formula Mission 1's `run_matrix` used.
- **Errors:** a rate-limit error, a timeout or `AnswerUnavailable` is recorded as `error`, never as a refusal or a pass; a run is complete only when every row has a reply, and a resumed run skips rows already answered.
- **Model:** the evaluation runs on the model and settings the demo ships with in `config.yaml`.
  If that stays `gemini-3.8-flash`, a practice run is made on 14/10 and the final run after the daily quota resets at 14:00 Vietnam time on 15/10, which leaves 5 requests for the demo and the video.

## Reasons

Hiep, 14/10/2026, on runs and wordings: "Due to our constraints (the rate limit of the Gemini model), I want to ignore some rules, some promises, like every case needs to be run three times. That's not very valid now."
And: "I want to test the main version of the tests first and we will defer the ideas of testing other paraphrasing versions of them for now."
On the rest, Hiep took the research's recommendations: "Approve all the decisions except for the O, which is optional." (14/10/2026).
Claude read "the O, which is optional" as the optional spot repeats (option P in the research), so no spot repeats are made; to be confirmed by Hiep in the PR.
The comparison of the harness options is Claude's, in the research write-up under "AI recommendation", not Hiep's reasoning.

## Consequences

Drafted by Claude from the research and Hiep's decisions; to be approved by Hiep in the PR.

- One run is 15 answer calls and 15 query embeddings, about 75% of a day's answer quota on `gemini-3.8-flash`.
- A pass is one sample: a row that passed may fail on the next identical call, and the report says so; this is a change since Mission 1 for mandatory question 2.
- Paraphrased questions are not tested with the real model, so A2 ("it also finds questions phrased differently") is not shown in Mission 2; both ideas are parked under "Deferred ideas" in `docs/mission1/playbook.md`.
- With n = 14 gated rows, 10% over-cautious allows at most 1 such row.
- 0 unsafe answers in 14 rows only bounds the true rate below about 19.3% at 95% confidence; the report states it next to the gates (V5).
- #14 adds `key_facts` to the answer rows of `data/test_cases.yaml`, the run and scoring scripts, the review sheet and the report generator; no dependency is added.
- A fix to a check or to the report re-scores saved replies without any API call.

## Would change if

- A model or gateway with enough quota for repeated runs is adopted: restore 3 runs per case (V4) and the 3 phrasings (A2).
- Hand reading finds an unfaithful answer that every deterministic check passed, often enough that reading alone is not trusted.

## Evidence

The research write-up above.
Evidence log line of 14/10/2026 08:53 (Claude Opus 5.5, Pi).
