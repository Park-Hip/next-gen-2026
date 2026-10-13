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
app/                The rules engine: data loading (data.py) and steps 1-4 and 7 (rules.py)
tests/              The deterministic test suite for the rules
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

The rules engine in `app/` loads `data/`, runs steps 1-4 and 7, and is checked by the test suite.
`data/` is now the source of truth; `artifacts.md` stays as the Mission 1 snapshot.

```bash
pip install -r requirements.txt
python -m pytest
```

See one asker's scope by hand:

```bash
python -m app.rules minh 2026-10-07
```
