# 0005. How should v1 evaluate the AI steps: our own harness or a library?

- Status: Draft
- Issue: #8
- Feeds: ADR 0006
- Method: Pi on 14/10/2026 from 08:53 (`tools/ai_sessions.py`), orchestrator and only model Claude Opus 5.5 (`claude-bridge/claude-opus-5-5`), no subagents.
  Search: the `web_search` tool (providers reported: OpenAI and Exa); every source in the table below was then opened with `fetch_content` or read from PyPI and npm metadata, and its quote copied from the opened page.
  `docs.ragas.io` answered HTTP 429, so the RAGAS faithfulness page was read from the same Markdown file in the RAGAS GitHub repository (S1).
  Repository files read: issues #8, #13 (plan comment) and #14, `docs/competition/mission2_brief.md`, `docs/mission2/mission1_promises.md`, `docs/mission2/plan.md`, ADRs 0003 and 0007, `docs/mission1/submitted/document.md` Phần 5, `docs/mission1/redraft/artifacts.md` (test matrix and metrics), `data/test_cases.yaml`, `config.yaml`, `pyproject.toml`.
  No Gemini call was made and no library was installed: nothing below is measured on our data.
  Hiep's prompt, verbatim:

```text
https://github.com/Park-Hip/next-gen-2026/issues/8 Research and deep dive into this. I want you to give me options and tell me when there are important decisions.

There's some news for you about the promises that we promised in Mission 1. Due to our constraints (the rate limit of the Gemini model), I want to ignore some rules, some promises, like every case needs to be run three times. That's not very valid now. About the phrase, this different paraphrased version of a test case, I want to delay it right now too. I want to test the main version of the tests first and we will defer the ideas of testing other paraphrasing versions of them for now.
```

## Why it matters for v1

The evaluation is the evidence for the brief's "biết sản phẩm đang tốt và chưa tốt ở đâu" and for its test format "Kỳ vọng → Kết quả thực tế → Đạt/Chưa đạt → Điều học được".
It fills #14: `eval/run.py`, committed results and `docs/mission2/test_report.md`.

Constraints any option must respect:

- Mission 1 promised the gates in V3: rules correct in every case, 0 leaks, 0 unsafe answers, faithfulness read by hand for every answer, at most 10% over-cautious cases.
- V1 and the Deferred ideas rejected an LLM judge: "a judge adds a second model to trust".
- Context recall is not measured (ADR 0007).
- Hiep's decisions of 14/10/2026 in the prompt above: each case runs once, not 3 times (V4), and only the main wording of each row is asked (A2's 3 phrasings deferred).
- The free tier of `gemini-3.8-flash` that Hiep read in AI Studio on 14/10: 5 requests per minute, 20 requests per day (#13 plan, decision 6); quotas are per project, not per key, and the daily quota resets at midnight Pacific time (S10), which is 14:00 in Vietnam on 15/10/2026.
- One run is now 15 rows, so 15 answer calls plus 15 query embeddings, which is 75% of one day's answer quota; the public demo shares the same quota.
- AGENTS.md: no new dependency or moving part without Hiep's approval; tunable values only in `config.yaml`.

## Options found

### Harness

| Option | What it is | Strengths | Costs and risks | Fit for v1 | Sources |
|---|---|---|---|---|---|
| A. Our own harness | `eval/run.py` calls the same `Answerer` and step 7 the page uses (#13), saves each raw reply, and a scoring module applies the checks of `data/test_cases.yaml` | No new dependency; every check is a few lines that Hiep can explain in PITCH; the checks are specific to our product (card kind, scope, citations), which is what practitioners recommend over generic metrics; scoring is testable offline in pytest | We write the report generator and the review sheet ourselves (about 100-200 lines, an estimate) | Good | S7, S8 |
| B. RAGAS 0.4.3 | Python library of RAG metrics | Well known; has non-LLM string metrics | Its faithfulness metric uses an LLM to split the answer into claims and check each one; installs `langchain-community`, `langchain_openai`, `openai`, `datasets` and more; its string metrics are one line each in our own code | Poor | S1, S11 |
| C. DeepEval 4.2.8 | pytest-style LLM evaluation framework | Custom deterministic metrics are allowed through `BaseMetric` | Faithfulness is LLM-as-a-judge by default; sends PostHog telemetry unless opted out; installs pytest plugins (`pytest-repeat`, `pytest-rerunfailures`, `pytest-xdist`) into our test environment | Poor | S2, S3, S4, S11 |
| D. promptfoo 0.124.1 | YAML test runner with deterministic assertions, Python assertions and `repeat` | Assertions such as `contains`, `regex` and `python` fit our checks | A Node.js tool (engine `>=22.22.0`) beside a Python project, a new moving part; it calls a "provider", so our pipeline would need a Python provider wrapper | Poor | S5, S11 |
| E. Inspect AI 0.3.279 | UK AISI evaluation framework with scorers, epochs and a log viewer | Text scorers (`includes`, `match`, `pattern`), epoch reducers such as `pass_at`, `stderr` built in | Built around its own model calls and `TaskState`; our pipeline would be wrapped as a custom solver; about 40 direct dependencies (`boto3`, `s3fs`, `textual`, ...) | Poor | S6, S11 |
| F. Langfuse experiments (SDK 4.17.0) | Hosted traces and experiment runs; local data and our own evaluator functions allowed | Run comparison in a web UI; evaluators can be plain Python | A cloud account and a new moving part; the data leaves the machine (acceptable for simulated data, but still a new service); the checks are still ours | Poor for v1 | S9, S11 |

No library removes the work that matters here: the checks are product rules (which card, which documents may be cited), and each library either wraps the same few lines or adds an LLM judge.

### Faithfulness and citations

| Option | What it is | Strengths | Costs and risks | Fit for v1 | Sources |
|---|---|---|---|---|---|
| G. Read every answer by hand | A generated review sheet shows, per row, the question, the expected answer, the card, each point's text, its quote and the full text of the chunk it cites; Hiep marks pass or fail with a note | What Mission 1 promised (V3); about 6 answer cards per run, so it takes minutes | One reader; judgement not repeatable by code | Good, promised | S8 |
| H. Deterministic checks from the test file | Card kind; answer rows cite every `must_cite` and nothing outside `must_cite` + `may_cite`; conflict rows cite one of `conflict_pair`; no `forbidden_for_llm` citation; `must_not_contain` absent; retrieved ids inside the scope | Free, exact, re-runnable; already defined by the fields of `data/test_cases.yaml` | Says nothing about whether the text is right | Good | S7 |
| I. Key facts per answer row | A new field `key_facts` (for example `14 ngày` for row 1) that must appear in the answer text after NFC and whitespace folding | Catches the most dangerous misstatement, a wrong number, without a reader; Mission 1's metric table already counted "a wrong key fact" as unsafe | A new field in the test data, which Hiep reviews; a substring passes even if the sentence around it is wrong, so G is still needed | Good | S7 |
| J. LLM judge (RAGAS or DeepEval faithfulness with Gemini) | A second model splits and checks claims | Automatic | Rejected by V1; at least 2 extra calls per answer on a quota of 20 a day; Vietnamese judging quality unknown | Poor | S1, S2 |
| K. NLI or hallucination classifier | A local model checks support, as ALCE does with an NLI model or RAGAS with HHEM-2.1-Open | No API quota | A second model to trust, the same objection as J; brings in a model runtime (ALCE's NLI model has 11B parameters); Vietnamese support of these models not checked | Poor | S1, S12 |

The quote check of step 7 (ADR 0003) is already a deterministic faithfulness check on every point: a quote not found in the cited chunk refuses the answer.
What it cannot catch, a true quote under a wrong sentence, is what G is for.

### Where an unsafe answer is counted

| Option | What it is | Strengths | Costs and risks | Fit for v1 | Sources |
|---|---|---|---|---|---|
| L. On the card the employee sees | Unsafe means an answer card where a refusal or conflict was expected, a wrong key fact, or a `forbidden_for_llm` citation; Mission 1's metric table defines it this way | Measures what reaches the employee | Hides the model's own mistakes when step 7 catches them | Good as the gate | S7 |
| M. On the raw model reply | Unsafe means the model returned points on a refusal row, or cited a forbidden document, even if step 7 then refused | Tests V6, the riskiest assumption, which is about the model ("LLM nói không tìm thấy") | Counts errors no employee saw | Good as a report line | S7 |
| N. Both | The card is the gate (L); the raw reply is reported beside it (M) | Honest on both questions; a row where step 7 caught the model is a strong example for the video and for question 3 | Two numbers to explain | Good | - |

### One run per case: reporting run-to-run variance honestly

| Option | What it is | Strengths | Costs and risks | Fit for v1 | Sources |
|---|---|---|---|---|---|
| O. One run, variance stated as not measured | The report says each case ran once, that Gemini answers vary between identical calls (ADR 0003), and that a pass is one sample | Matches Hiep's decision and the quota | A passing row may fail on the next call | Good | S13, S14 |
| P. O plus declared spot repeats | Before the run, name the rows to repeat if quota is left (for example refusal rows 6, 8 and 11, where V6 can be disproved); report every repeat, and a row fails if any run fails | Some evidence of variance where it matters most | Uses the demo's quota; few samples | Optional | S13, S14 |
| Q. Re-run a failed row until it passes | - | - | Hides exactly the noise that matters; Mission 1 V4's spirit is "một lần sai tính là trượt" | Reject | S14 |
| R. Report counts and an upper bound | "0 of n" with the exact one-sided 95% upper bound 1 - 0.05^(1/n), the formula Mission 1's `run_matrix` used: 18.1% for n = 15, 28.3% for n = 9 | Turns V5 ("passing a small set is not proof") into one number | The rule of three (3/n) is only a good approximation above n = 30, so use the exact formula; standard errors from the CLT need many questions | Good | S13, S15 |

### Running under the quota

| Option | What it is | Strengths | Costs and risks | Fit for v1 | Sources |
|---|---|---|---|---|---|
| S. Run and score as two steps | `eval/run.py` writes one JSON line per row (persona, date, question, model id, commit, retrieved ids, raw reply, card, reason, latency); scoring reads the file offline | A fix to a check or to the report costs no quota; a run stopped by a 429 resumes and skips rows already answered; scoring is unit-tested in CI with fake replies | Two commands instead of one | Good | S10 |
| T. API errors are errors | A 429, timeout or `AnswerUnavailable` (#13 decision 4) is recorded as `error`, never as a refusal or a pass, and the run is incomplete until every row has a reply | A quota failure cannot look like a correct refusal | None found | Good | - |
| U. Gemini Batch API | Asynchronous jobs at 50% of the paid price | Made for evaluations | The rate-limits page lists batch limits only for paid tiers 1-3; free-tier availability for `gemini-3.8-flash` was not confirmed | Poor | S16, S10 |

## Claims that did not hold up

1. **"Ragas documents non-LLM metrics as deterministic" (search summary, citing docs.ragas.io).**
   The page returned HTTP 429 and was not read; the claim is unverified and is not used above.
2. **"The rule of three gives a 95% bound for any n."**
   The source says it is a good approximation only "when n is greater than 30" (S15); the exact formula is used instead.
3. **A support-forum thread says AI Studio did not reset the daily quota at midnight Pacific.**
   One user report, not checked; S10 states the reset time.

## AI recommendation (not a decision)

Claude's pick: option A (own harness) with S and T, faithfulness by G plus H and I, unsafe answers counted by N, and variance reported by O and R, with P only if Hiep wants to spend quota on it.
One line: the checks we need are our product rules, which no library knows, and every library's added value is the LLM judge Mission 1 rejected and the quota cannot pay for.

## Sources

| ID | Title and URL | Accessed | Quote that supports the claim |
|---|---|---|---|
| S1 | RAGAS, Faithfulness (repository docs), https://raw.githubusercontent.com/vibrantlabsai/ragas/main/docs/concepts/metrics/available_metrics/faithfulness.md | 2026-10-14 | "Identify all the claims in the response." / "Check each claim to see if it can be inferred from the retrieved context." / "Vectara's HHEM-2.1-Open is a classifier model (T5) that is trained to detect hallucinations" |
| S2 | DeepEval, Faithfulness, https://deepeval.com/docs/metrics-faithfulness | 2026-10-14 | "The faithfulness metric uses LLM-as-a-judge to measure the quality of your RAG pipeline's generator" / "deepeval set-eval-mode llm # LLM-as-a-judge (default)" |
| S3 | DeepEval, 'Do it yourself' Metrics, https://deepeval.com/docs/metrics-custom | 2026-10-14 | "a non-LLM eval is simply a metric that is not scored using an LLM" |
| S4 | DeepEval, Data Privacy, https://deepeval.com/docs/data-privacy | 2026-10-14 | "By default, `deepeval` uses **PostHog** to track only very basic telemetry data." |
| S5 | promptfoo, Test Case Configuration, https://www.promptfoo.dev/docs/configuration/test-cases/ | 2026-10-14 | "Set `options.repeat` to a positive integer to run one test case multiple times" / "add `--no-cache` when every run must call the provider" |
| S6 | Inspect, Scorers, https://inspect.aisi.org.uk/scorers.html, and Solvers, https://inspect.aisi.org.uk/solvers.html | 2026-10-14 | "Inspect includes both text matching scorers as well as model graded scorers." / "A solver is a Python function that takes a TaskState and `generate` function" |
| S7 | Hamel Husain, AI Evals: Everything You Need to Know, https://hamel.dev/blog/posts/evals-faq/index.html | 2026-10-14 | "Should I use \"ready-to-use\" evaluation metrics? No. Generic evaluations waste time and create false confidence when you use them as quality measures." / "Start with cheap code-based checks where possible: regex patterns, structural validation, or execution tests." |
| S8 | Same page as S7 | 2026-10-14 | "Binary evaluations force clearer thinking and more consistent labeling." / "Build a custom annotation tool. This is the single most impactful investment you can make for your AI evaluation workflow." |
| S9 | Langfuse, Experiments via SDK, https://langfuse.com/docs/evaluation/experiments/experiments-via-sdk | 2026-10-14 | "Local data means the inputs originate in your process; experiment data is still sent to your configured Langfuse instance." |
| S10 | Gemini API, Rate limits, https://ai.google.dev/gemini-api/docs/rate-limits | 2026-10-14 | "Rate limits are applied per project, not per API key. Requests per day (**RPD**) quotas reset at midnight Pacific time." / "Batch API requests are subject to their own rate limits, separate from the non-batch API calls." |
| S11 | PyPI JSON metadata for `ragas`, `deepeval`, `inspect-ai`, `langfuse`, and npm metadata for `promptfoo`, https://pypi.org/pypi/<name>/json and https://registry.npmjs.org/promptfoo/latest | 2026-10-14 | Versions 0.4.3, 4.2.8, 0.3.279, 4.17.0 and 0.124.1; `ragas` requires `langchain-community`, `langchain_openai`, `openai`, `datasets`; `deepeval` requires `pytest-repeat`, `pytest-rerunfailures`, `pytest-xdist`, `posthog`; `promptfoo` engines `{"node": ">=22.22.0"}` |
| S12 | Gao et al., Enabling Large Language Models to Generate Text with Citations (ALCE), EMNLP 2023, https://arxiv.org/abs/2305.14627 | 2026-10-14 | "We use the NLI model TRUE (Honovich et al., 2022) again to automatically examine whether the cited passages entail the model generation." (TRUE is "a T5-11B ... model fine-tuned on a collection of natural language inference (NLI) datasets") |
| S13 | Miller, Adding Error Bars to Evals: A Statistical Approach to Language Model Evaluations (Anthropic), https://arxiv.org/html/2411.00640v1 | 2026-10-14 | "Reducing variance by resampling answers and by analyzing next-token probabilities" / "advised against adjusting the sampling temperature for the sake of variance reduction" |
| S14 | Yao et al., τ-bench, https://arxiv.org/abs/2406.12045 | 2026-10-14 | "We also propose a new metric (pass^k) to evaluate the reliability of agent behavior over multiple trials." / "quite inconsistent (pass^8 <25% in retail)" |
| S15 | Rule of three (statistics), Wikipedia, https://en.wikipedia.org/wiki/Rule_of_three_(statistics) | 2026-10-14 | "the interval from 0 to 3/n is a 95% confidence interval for the rate of occurrences in the population. When n is greater than 30, this is a good approximation of results from more sensitive tests." |
| S16 | Gemini API, Batch API, https://ai.google.dev/gemini-api/docs/batch-api | 2026-10-14 | "Use Batch API for large-scale, non-urgent tasks such as data pre-processing or running evaluations where an immediate response is not required." |
