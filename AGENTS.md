# AGENTS.md

Appota NextGen AI Talent 2026, Bài test B - "Tri thức nội bộ Appota": an AI assistant that gives each employee the right knowledge for their unit, their access rights, and the version in force today.
Mission 1 (design) was submitted on 08/10/2026; Mission 2 (build v1 in 3 days) is in progress; Mission 3 (adapt to change) follows.

## Read first

- `docs/competition/mission2_brief.md` - what Mission 2 must show and submit.
- `docs/mission1/redraft/current_design.md` plus the ADRs in `docs/decisions/` - the design in force.
- `docs/mission2/mission1_promises.md` - the acceptance checklist.
- `docs/mission2/plan.md` - Hiep's decisions D1-D15 and the roadmap; the issues are under the "Mission 2" milestone on GitHub.

`README.md` shows the repository layout.

## Product rules

- A relevant document is not necessarily allowed, in force, or applicable to the asker; keep access, validity and applicability separate everywhere.
- Deterministic rules decide access, validity, applicability, precedence and the card; the LLM only interprets language.
- All Appota data is simulated: label it "giả lập" and never invent research or measurements.

## Workflow

- Code is implemented through GitHub issues and PRs.
  Every code change starts from an issue made with a form in `.github/ISSUE_TEMPLATE/`, is built on its own branch named `<issue>-<short-title>`, and lands through a PR that fills in `.github/pull_request_template.md` and says `Closes #<issue>`.
  Never commit code directly to `master`.
- Small doc edits and trivial fixes may skip the issue; their PR says "No issue - minor fix".
- Ask Hiep before opening or closing an issue or a PR; Hiep merges.
- A design change is an ADR in `docs/decisions/`, added in the same PR; `current_design.md` stays frozen as the Mission 1 baseline.
- A choice with real alternatives starts from a research issue (label `research`).
  Hiep runs the research with his own agent; its results are filed in `docs/research/` from the template there, and the ADR records Hiep's decision and his reasons in his words.
  Never write an ADR's reasons for Hiep; draft only from what he said, and ask when it is missing.
- A known failure that stays in v1 keeps its issue open with the `limitation` label, so the test suite, README and video report it.
- Before a PR, run `python -m pytest`.
- Do not edit `docs/competition/` or `docs/mission1/`, except "Deferred ideas" in `docs/mission1/playbook.md`.
- At the end of each session that changes the project, add one line under "Ghi chú nhanh Mission 2" at the end of the evidence log, in Vietnamese: date and time, tool and model, task, Hiep's decision, and how the result was checked.
  Take tool, model and time from `tools/ai_sessions.py`; write "[chờ Hiệp]" when the decision is unknown.
  The log is one local file, ignored by git, so a worktree does not contain it.
  Always write to the copy in the main checkout: `$(git rev-parse --path-format=absolute --git-common-dir)/../evidence_log.md`.
  Never create a second copy inside a worktree.

## Competition rules

- `docs/competition/ai_policies.md` is binding and overrides this file.
- Every AI tool and prompt that shaped the result is declared in the evidence log with how it was checked; undeclared use costs 30% of the score.
- Hiep must be able to explain or rebuild any part in the PITCH round: explain your reasoning and flag every factual claim that needs checking, because an unverified hallucination fails the criterion.
- Credit any public source or solution used.
- The repository is public: no API keys, passwords or sensitive data.

## Writing

- Never use the em dash; use a plain "-".
- One sentence per line in Markdown.
- Code comments in English.

## Scope

- Build only what the Mission 2 brief or a promise in `mission1_promises.md` needs, in the simplest way that works end to end; no layers, frameworks or config "for later".
- Ask Hiep before adding a dependency, a new moving part, or more than about half a day of work, and whenever scope is unclear.
- Park an out-of-scope idea as one line under "Deferred ideas" in `docs/mission1/playbook.md`; never promise it in a deliverable.
