# Development

Hand checks for developers, moved from the README so it can stay the judges' front page.
How to install, run the page, run the tests and run the evaluation is in the [README](../README.md#running-locally).
All company data in this repository is simulated ("giả lập").

## Build the Mission 1 PDF

Requires Python 3, Microsoft Edge, and an internet connection (the diagram library loads from a CDN).

```bash
pip install markdown pypdf
python scripts/render_pdf.py docs/mission1/document.md build/mission1_draft.pdf
```

The script prints the page count; the limit is 5 pages.

## Check the core model

Runs the adopted rules on the simulated documents and personas, then the publish-time check.
No dependencies beyond Python 3.

```bash
python -I -X utf8 docs/mission1/redraft/checks/adopted_rules.py
```

## See one asker's scope

The pipeline in `src/appota_kb/` loads `data/` and runs steps 1-7: scope, retrieval, one grounded Gemini call, and the card.
`data/` is now the source of truth; `artifacts.md` stays as the Mission 1 snapshot.
Steps 1-4 need no key:

```bash
uv run python scripts/show_scope.py minh 2026-10-07
uv run python scripts/show_scope.py minh 2026-10-07 --why   # why each document is kept or dropped
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

Step 6 asks `gemini-3.5-flash-lite` (ADR 0008) for points citing retrieved chunk ids, and step 7 picks the card from those citations, never from the model's own words (ADRs 0003 and 0009).
It needs a Gemini API key in the environment and the network; the tests do not (they use a fake model).

```bash
export GEMINI_API_KEY=...        # PowerShell: $env:GEMINI_API_KEY = "..."
uv run python scripts/answer.py minh 2026-10-07 "Phép năm của tôi là bao nhiêu ngày?"
```

It prints the retrieved ids, the raw model output, each point with its quote, and the card kind with its refusal reason.
Every answer also logs one JSON line (persona, as-of date, question, model, retrieved ids, points, raw output and latency) on the `appota_kb.services.answering.answerer` logger.

## Evaluation details

A practice run on a few rows, and resuming a run stopped by the daily quota:

```bash
uv run python -m appota_kb.evaluation.run --rows 1,7,8    # a quota-limited practice subset
uv run python -m appota_kb.evaluation.run --resume results/<run_id>.jsonl
```

A resume re-asks only rows without a reply, and refuses when the commit, the model settings or the test file changed; a key from another Google Cloud project has its own quota.
Each run also writes Hiep's review files next to it: `results/<run_id>.review.md` to read, and `results/<run_id>.review.yaml` where he marks faithfulness and writes the lesson of each row; the report reads them.
The "Test cases" page shows the run that `docs/mission2/test_report.md` names, so a practice run saved in `results/` never replaces the official one.
