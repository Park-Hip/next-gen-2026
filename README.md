# NextGen AI Talent 2026 - Bài test B: Tri thức nội bộ Appota

An AI assistant that gives each employee the right knowledge for their unit, their access rights, and the version in force today.
All company data in this repository is simulated ("giả lập"); no real Appota data is used.

## Status

| Mission | Goal | Status |
|---|---|---|
| 1 | Understand the problem (5-page analysis) | Drafting |
| 2 | Build v1 | Not started |
| 3 | Adapt to change | Not started |

## Layout

```
docs/competition/   Official brief, rules and AI policy (do not edit)
docs/mission1/      Mission 1 document, answers, criteria, playbook, thinking phase
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
