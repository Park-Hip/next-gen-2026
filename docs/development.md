# Development

Hand checks and tools for working on the repository.
How to install, start the page, run the tests and run the evaluation is in the [README](../README.md#running-locally).
All documents are simulated ("giả lập").

## See one asker's scope by hand

Steps 1-4 only: rules, no key and no network.

```bash
uv run python scripts/show_scope.py minh 2026-10-07
```

## Check retrieval by hand

Step 5 searches only the asker's scope: syllable BM25 and `gemini-embedding-001`, fused with reciprocal rank fusion (ADRs 0001 and 0002).
It needs a Gemini API key in the environment and the network; the tests do not (they use a fake embedder).

```bash
export GEMINI_API_KEY=...        # PowerShell: $env:GEMINI_API_KEY = "..."
uv run python scripts/search.py minh 2026-10-07 "Phép năm của tôi là bao nhiêu ngày?"
uv run python scripts/search.py          # the top 5 for every row and wording of data/test_cases.yaml
```

Each line shows the chunk id, its RRF score, and its BM25 and dense scores with their ranks.
Every search also logs one JSON line (persona, as-of date, question, scope size, and the same numbers per chunk) on the `appota_kb.services.retrieval.search` logger.

## Check the grounded answer by hand

Step 6 asks `gemini-3.5-flash-lite` (ADR 0008) for points citing retrieved chunk ids, and step 7 picks the card from those citations, never from the model's own words (ADR 0003).
It needs a Gemini API key in the environment and the network; the tests do not (they use a fake model).

```bash
export GEMINI_API_KEY=...        # PowerShell: $env:GEMINI_API_KEY = "..."
uv run python scripts/answer.py minh 2026-10-07 "Phép năm của tôi là bao nhiêu ngày?"
```

It prints the retrieved ids, the raw model output, each point with its quote, and the card kind with its refusal reason.
Every answer also logs one JSON line (persona, as-of date, question, model, retrieved ids, points, raw output and latency) on the `appota_kb.services.answering.answerer` logger.

## Resume an evaluation run

A run stopped by the daily quota is resumed with `--resume results/<run_id>.jsonl` (under another project's key).
A resume re-asks only rows without a reply and refuses when the commit, the model settings or the test file changed.

```bash
uv run python -m appota_kb.evaluation.run --rows 1,7,8                       # a quota-limited practice subset
uv run python -m appota_kb.evaluation.run --resume results/<run_id>.jsonl
```

## Check the core model of Mission 1

Runs the adopted rules on the simulated documents and personas, then the publish-time check.
No dependencies beyond Python 3.

```bash
python -I -X utf8 docs/mission1/redraft/checks/adopted_rules.py
```

`tests/test_parity.py` checks the rules in `src/appota_kb/` against this script.

## Build the Mission 1 PDF

Requires Python 3, Microsoft Edge, and an internet connection (the diagram library loads from a CDN).

```bash
pip install markdown pypdf
python scripts/render_pdf.py docs/mission1/document.md build/mission1_draft.pdf
```

The script prints the page count; the limit is 5 pages.
