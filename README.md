# NextGen AI Talent 2026 - Bài test B: Tri thức nội bộ Appota

An AI assistant that gives each employee the right knowledge for their unit, their access rights, and the version in force today.
All company data in this repository is simulated ("giả lập"); no real Appota data is used.

## Status

| Mission | Goal | Status |
|---|---|---|
| 1 | Understand the problem (5-page analysis) | Submitted 08/10/2026 (`docs/mission1/submitted/`) |
| 2 | Build v1 | In progress: plan and decisions in `docs/mission2/plan.md`, issues under the "Mission 2" milestone |
| 3 | Adapt to change | Not started |

## Layout

```
.github/            Issue forms and the PR template
docs/competition/   Official brief, rules and AI policy (do not edit)
docs/decisions/     One ADR per decision from Mission 2 on, with Hiep's reasons
docs/research/      One write-up per research question; feeds an ADR
docs/mission1/      Mission 1 document, answers, criteria, playbook, thinking phase, redraft plan
  submitted/        The exact files submitted (do not edit)
  redraft/          Mission 1 design baseline and decision register (both frozen), simulated data and traces, reviews
    checks/         Scripts that run the core model on the simulated data
docs/mission2/      Mission 2 plan, and what Mission 1 promised; the test report (`test_report.md`) is generated
src/appota_kb/      The installed package; `main.py` is the uvicorn factory
  models/           Data types only, no I/O: documents, org, scope, answer, card, search hit
  integrations/     The only code that reads `data/` (`data_files.py`) or calls Gemini (`gemini.py`)
  services/         Steps 1-7: `scope.py` (1-4), `retrieval/` (5), `answering/` (6), `citations.py` (7), `card_text.py`, and `ask.py`, one question end to end; `guide.py` builds the judges' pages
  api/              The pages: `page.py` and `templates/` (the question form, `/data`, `/cases`), HTTP only
  core/             `config.py` (reads `config.yaml`) and `paths.py`
  evaluation/       The harness: `run.py` asks each test case once, `score.py` checks offline, `report.py` and `review.py` write the report and Hiep's review files, `committed.py` reads the committed run back for the "Test cases" page
tests/              The deterministic test suite, one folder per package folder
results/            Committed runs: one `<run_id>.jsonl` per run plus Hiep's review files
config.yaml         Tunable values (top k, thresholds, limits); read only through src/appota_kb/core/config.py
render.yaml         Deploy config for the Render free web service (ADR 0004)
.python-version     Pins Python 3.12 for Render
data/               Simulated documents, org tree, personas and test cases as files
evidence_log.md     AI usage log for all missions (local only, ignored by git; lives in the main checkout, not in worktrees)
scripts/            Hand checks (`show_scope.py`, `search.py`, `answer.py`) and the document and evidence log tools
build/              Generated output (not committed)
```

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

## Run the tests

The pipeline in `src/appota_kb/` loads `data/` and runs steps 1-7: scope, retrieval, one grounded Gemini call, and the card.
`data/` is now the source of truth; `artifacts.md` stays as the Mission 1 snapshot.

```bash
uv sync
uv run python -m pytest
```

See one asker's scope by hand:

```bash
uv run python scripts/show_scope.py minh 2026-10-07
```

## Check retrieval by hand

Step 5 searches only the asker's scope: syllable BM25 and `gemini-embedding-001`, fused with reciprocal rank fusion (ADRs 0001 and 0002).
It needs a Gemini API key in the environment and the network; the tests do not (they use a fake embedder).
All documents are simulated ("giả lập").

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
All documents are simulated ("giả lập").

```bash
export GEMINI_API_KEY=...        # PowerShell: $env:GEMINI_API_KEY = "..."
uv run python scripts/answer.py minh 2026-10-07 "Phép năm của tôi là bao nhiêu ngày?"
```

It prints the retrieved ids, the raw model output, each point with its quote, and the card kind with its refusal reason.
Every answer also logs one JSON line (persona, as-of date, question, model, retrieved ids, points, raw output and latency) on the `appota_kb.services.answering.answerer` logger.

## Run the page locally

The page runs the whole pipeline: steps 1-4 build the asker's scope, step 5 retrieves, step 6 asks Gemini, and step 7 picks the card.
It needs a Gemini API key in the environment, and the index is built eagerly, so a missing key or a failed embedding stops the start.
Every unit, person, document and number on the page is simulated ("giả lập").

```bash
export GEMINI_API_KEY=...        # PowerShell: $env:GEMINI_API_KEY = "..."
uv run uvicorn appota_kb.main:create_app --factory --reload
```

Then open http://127.0.0.1:8000, pick Minh, Lan or Hà and an as-of date, and ask a question.
Two more pages are made for the judges and call no model: "Simulated data" (`/data`) lists the units, the askers and every document with its status for today, and "Test cases" (`/cases`) lists every test case with why it is tested, its expectation and the result of the committed run, with a "Thử ngay" link that asks the same case again on the main page.
"Test cases" shows the run that `docs/mission2/test_report.md` names, so the page and the report cannot disagree.
The public demo URL and the first-load warning are added once the Render service is live.

## Run the evaluation

The harness asks every row of `data/test_cases.yaml` once, in its main wording, through the same `services/ask.py` as the page (ADR 0006).
It writes one JSON record per row, then a separate offline step scores the saved replies and writes `docs/mission2/test_report.md` in the brief's format "Kỳ vọng → Kết quả thực tế → Đạt/Chưa đạt → Điều học được".
It needs a Gemini API key in the environment or in a `.env` file at the repository root (ignored by git, read by `appota_kb.evaluation.run` only); the tests do not (they use fake replies).

```bash
export GEMINI_API_KEY=...        # PowerShell: $env:GEMINI_API_KEY = "..."
uv run python -m appota_kb.evaluation.run                 # every row, once
uv run python -m appota_kb.evaluation.run --rows 1,7,8    # a quota-limited practice subset
uv run python -m appota_kb.evaluation.report results/<run_id>.jsonl
```

One full run is 15 answer calls and 15 query embeddings, about 3% of the 500 requests a day the free tier of `gemini-3.5-flash-lite` allows, shared with the demo.
A run stopped by the daily quota is resumed with `--resume results/<run_id>.jsonl` (under another project's key); a resume re-asks only rows without a reply and refuses when the commit, the model settings or the test file changed.
The test report is [`docs/mission2/test_report.md`](docs/mission2/test_report.md); it is generated, never edited by hand.
