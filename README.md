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
docs/mission2/      Mission 2 plan, and what Mission 1 promised
app/                The rules engine (data.py, rules.py), hybrid retrieval (retrieval.py), the grounded answer (answer.py) and the page: config.py, cards.py, web.py, templates/
tests/              The deterministic test suite for the rules, retrieval, the answerer, the cards and the page
config.yaml         Tunable values (top k, thresholds, limits); read only through app/config.py
render.yaml         Deploy config for the Render free web service (ADR 0004)
.python-version     Pins Python 3.12 for Render
data/               Simulated documents, org tree, personas and test cases as files
evidence_log.md     AI usage log for all missions (local only, ignored by git; lives in the main checkout, not in worktrees)
tools/              Helper scripts
build/              Generated output (not committed)
```

## Build the Mission 1 PDF

Requires Python 3, Microsoft Edge, and an internet connection (the diagram library loads from a CDN).

```bash
pip install markdown pypdf
python tools/render_pdf.py docs/mission1/document.md build/mission1_draft.pdf
```

The script prints the page count; the limit is 5 pages.

## Check the core model

Runs the adopted rules on the simulated documents and personas, then the publish-time check.
No dependencies beyond Python 3.

```bash
python -I -X utf8 docs/mission1/redraft/checks/adopted_rules.py
```

## Run the tests

The pipeline in `app/` loads `data/` and runs steps 1-7: scope, retrieval, one grounded Gemini call, and the card.
`data/` is now the source of truth; `artifacts.md` stays as the Mission 1 snapshot.

```bash
uv sync
uv run python -m pytest
```

See one asker's scope by hand:

```bash
uv run python -m app.rules minh 2026-10-07
```

## Check retrieval by hand

Step 5 searches only the asker's scope: syllable BM25 and `gemini-embedding-001`, fused with reciprocal rank fusion (ADRs 0001 and 0002).
It needs a Gemini API key in the environment and the network; the tests do not (they use a fake embedder).
All documents are simulated ("giả lập").

```bash
export GEMINI_API_KEY=...        # PowerShell: $env:GEMINI_API_KEY = "..."
uv run python -m app.retrieval minh 2026-10-07 "Phép năm của tôi là bao nhiêu ngày?"
uv run python -m app.retrieval          # the top 5 for every row and wording of data/test_cases.yaml
```

Each line shows the chunk id, its RRF score, and its BM25 and dense scores with their ranks.
Every search also logs one JSON line (persona, as-of date, question, scope size, and the same numbers per chunk) on the `app.retrieval` logger.

## Check the grounded answer by hand

Step 6 asks `gemini-3.8-flash` for points citing retrieved chunk ids, and step 7 picks the card from those citations, never from the model's own words (ADR 0003).
It needs a Gemini API key in the environment and the network; the tests do not (they use a fake model).
All documents are simulated ("giả lập").

```bash
export GEMINI_API_KEY=...        # PowerShell: $env:GEMINI_API_KEY = "..."
uv run python -m app.answer minh 2026-10-07 "Phép năm của tôi là bao nhiêu ngày?"
```

It prints the retrieved ids, the raw model output, each point with its quote, and the card kind with its refusal reason.
Every answer also logs one JSON line (persona, as-of date, question, model, retrieved ids, points, raw output and latency) on the `app.answer` logger.

## Run the page locally

The page runs the whole pipeline: steps 1-4 build the asker's scope, step 5 retrieves, step 6 asks Gemini, and step 7 picks the card.
It needs a Gemini API key in the environment, and the index is built eagerly, so a missing key or a failed embedding stops the start.
Every unit, person, document and number on the page is simulated ("giả lập").

```bash
export GEMINI_API_KEY=...        # PowerShell: $env:GEMINI_API_KEY = "..."
uv run uvicorn app.web:main --factory --reload
```

Then open http://127.0.0.1:8000, pick Minh, Lan or Hà and an as-of date, and ask a question.
The public demo URL and the first-load warning are added once the Render service is live.
