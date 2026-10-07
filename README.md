# NextGen AI Talent 2026 - Bài test B: Tri thức nội bộ Appota

An AI assistant that gives each employee the right knowledge for their unit, their access rights, and the version in force today.
All company data in this repository is simulated ("giả lập"); no real Appota data is used.

## Status

| Mission | Goal | Status |
|---|---|---|
| 1 | Understand the problem (5-page analysis) | Redraft, Phase 2 of 7 (see `docs/mission1/redraft_plan.md`) |
| 2 | Build v1 | Not started |
| 3 | Adapt to change | Not started |

## Layout

```
docs/competition/   Official brief, rules and AI policy (do not edit)
docs/mission1/      Mission 1 document, answers, criteria, playbook, thinking phase, redraft plan
  redraft/          Decision register, simulated data and traces, open issues, production review
    checks/         Scripts that run the core model on the simulated data
evidence_log.md     AI usage log for all missions
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
