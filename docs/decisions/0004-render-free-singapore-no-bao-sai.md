# 0004. Demo on a Render free web service in Singapore; "Báo sai" and the owners' page out of scope for Mission 2

- Status: Accepted
- Date: 2026-10-13
- Origin: Hiep + AI
- Supersedes: Mission 1 promises P1 and P2, and the "Báo sai" button in C2 (`docs/mission2/mission1_promises.md`); confirms the working default of plan decision D3
- Issue: #7
- Research: `docs/research/0004-free-host-for-the-demo.md`

## Context

The brief prefers an online demo link, and judges may open it days or weeks after 15/10/2026.
Hiep chose the web stack before the research: FastAPI with Jinja2 templates, run by uvicorn.
Plan decision D3 left the host as a working default: a Render free web service auto-deploying `master`.
The research found that most free hosts now ask for a card, charge on signup or need a paid plan, that only Render runs the same uvicorn process as local development on a free plan, and that a Render free service loses its local files on every spin-down, restart or redeploy.
That loss is what made the "Báo sai" records the hardest part to host for free.
Nothing was deployed during the research, so start-up time on Render's 0.1 CPU is not measured.

## Options considered

1. **Host** - Render free web service (chosen); Vercel Hobby; Cloudflare Workers Python; Koyeb, Hugging Face Spaces, Fly.io, Railway, Northflank, Google Cloud, PythonAnywhere and Zeabur, all ruled out by a card, a charge, a paid plan or limits.
2. **Keeping the demo awake** - let it sleep and warn in the README (chosen); an external pinger; a GitHub Actions scheduled pinger.
3. **"Báo sai"** - build it with records in a file, in Neon Postgres, in Render Postgres, in Supabase or committed to GitHub; leave it out of Mission 2 (chosen).
4. **Conflict records ("Đã ghi nhận" on the conflict card)** - a JSON Lines file on the server disk (chosen); a hosted database.
5. **Owners' page** - list the conflict records for owners; leave it out of Mission 2 and revisit later (chosen).

The strongest alternative host: Vercel Hobby with its function region in Singapore (`sin1`), which has no one-minute wake.

## Decision

- **Host:** a Render free web service in the Singapore region, auto-deploying `master` from a `render.yaml` Blueprint with `plan: free`.
  - Python pinned to 3.12 with a `.python-version` file, because Render's default is now 3.14.3.
  - `GEMINI_API_KEY` declared with `sync: false` and set only in the Render Dashboard.
  - A health check path on the app.
- **Awake:** no pinger.
  The README warns that the first load can take about a minute, and Hiep opens the link once before any live judging session.
- **"Báo sai":** out of scope for Mission 2; no button and no "Báo sai" records.
  It is parked under "Deferred ideas" in `docs/mission1/playbook.md`.
- **Owners' page:** out of scope for Mission 2, to be revisited later; also parked under "Deferred ideas".
- **Conflict records:** the conflict card appends a record to a JSON Lines file on the server disk, seeded from the repository with demo records labelled "giả lập".
  The loss of records on spin-down, restart or redeploy is stated in the README and kept as an open `limitation` issue.

## Reasons

Hiep, 13/10/2026: "mark the Báo Sai feature as out-of-scope for now, it add little value to mission 2."

On the owners' page, Hiep, 13/10/2026: "drop the page too, we will revisit later".

For the host, keeping the demo awake and the conflict records, Hiep approved the research's recommendation as it stands (13/10/2026).
The comparison behind that recommendation is Claude's, in the research write-up under "AI recommendation" and "Render vs Vercel", not Hiep's reasoning.

## Consequences

Drafted by Claude from the research and Hiep's answers; approved by Hiep on 13/10/2026.

- #11 adds `render.yaml`, `.python-version` and a health route, deploys the page, and measures the first load after a spin-down from a clean browser.
- The answer card has no "Báo sai" button and there is no owners' page, so Mission 1 promises P1, P2 and that part of C2 are reported as not done, with this ADR as the reason; mandatory question 2 can cite it as a change since Mission 1.
- #15 shrinks to writing conflict records to the file; its "Báo sai" and owners' page parts go.
- Every judge's first visit after 15 idle minutes waits about a minute behind Render's loading page.
- Conflict records last only until the next spin-down, so a judge sees a record in the same visit, never days later.
- No new dependency, secret or account beyond Render and the Gemini key.
- The 750 free hours a month cover one service that sleeps when idle; a second free service in the same workspace would share them.

## Would change if

Drafted by Claude from the research; approved by Hiep on 13/10/2026.

- The first load after a spin-down in #11 takes much longer than a minute, or the app does not fit in 512 MB: revisit Vercel Hobby in `sin1`.
- Render suspends or deletes the free service during judging, or changes its free plan.
- The brief or a judge asks for "Báo sai", the owners' page, or records that survive a restart: build them then, with Neon Postgres as the first candidate.

## Evidence

The research write-up above, with every source opened by Claude on 13/10/2026.
Evidence log lines of 13/10/2026 (Claude Opus 5.5 with Agnes 2.5 Flash subagents).
