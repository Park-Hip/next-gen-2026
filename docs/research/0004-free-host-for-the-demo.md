# 0004. Which free host should serve the public demo?

- Status: Draft (decided in ADR 0004)
- Issue: #7
- Feeds: ADR 0004
- Method: Pi on 13/10/2026, 17:27-17:55.
  Hiep chose the web stack himself before the research (FastAPI with Jinja2 templates), so only the free host was researched; Streamlit and Gradio were not compared.
  Orchestrator: Claude Opus 5.5 (`claude-bridge/claude-opus-5-5`), which wrote the lane prompts and checked the sources.
  Web research: three `researcher` subagents on Agnes 2.5 Flash with max reasoning (`agnes/agnes-2.5-flash:max`), run one after another at 17:33-17:45; all three finished on the first attempt.
  Search providers: the `web_search` tool's configured provider.
  While the lanes ran and after, Claude opened every source in the table below itself (page fetch), with no other model involved.
  Nothing was deployed and no account was created, so every statement about a host comes from its documents, not from a test.
  Hiep's prompt to Claude, the shared context and the three lane prompts follow verbatim.

```text
Hiep to Claude:
https://github.com/Park-Hip/next-gen-2026/issues/7 I choose  FastAPI with Jinja template, research the free host only. use agnes max reasoning for web search if needed and use them as subagent

Shared context, sent at the top of each lane:
You are researching one technical decision for a small Python web prototype. Today is 2026-10-13. Your own knowledge may be out of date: free tiers, limits and pricing change often, so trust only pages you open today.

Project: v1 of an internal-policy assistant for a Vietnamese company, built inside a 3-day competition (deadline 15/10/2026). All data is simulated, about 11 Markdown files. The repository is public on GitHub.
Stack (decided, do not research alternatives to it): Python 3.12, FastAPI + Jinja2 templates served by uvicorn; dependencies fastapi, uvicorn, jinja2, pyyaml, langchain-core, langchain-google-genai (wraps google-genai). No local ML model: embeddings and answers come from the Gemini API over HTTPS (generativelanguage.googleapis.com), about 2-5 calls per question. Expected RAM well under 512 MB.
The app needs: one public HTTPS URL for judges, who may open it days or weeks after submission (judging runs after 15/10/2026; keep the link alive for at least about a month); a secret GEMINI_API_KEY set as a server-side environment variable, never in the repository or the browser; outbound HTTPS to Google's API; small writes when a user presses "Báo sai" (report wrong answer) and when a conflict is recorded (a few JSON lines per day, which an owners' page lists). Traffic is tiny: a few judges, a few dozen requests.
Working default: Render free web service, auto-deploy from the GitHub master branch. Known from 12/10 (re-check): Render free is 0.1 CPU and 512 MB, sleeps after 15 minutes idle, takes about a minute to wake, ephemeral disk; Hugging Face Docker and Gradio Spaces on free CPU reportedly need a PRO subscription.
The question: which FREE host should serve the demo. Free means no payment; say clearly if a credit card is required to sign up even when not charged.

Rules for your work:
- Use web_search, then OPEN each page you cite with fetch_content. Prefer official docs and pricing pages of each host, official changelogs and status/blog posts, official GitHub repos. Community posts only for real-world experience, labelled as such.
- Every claim needs: the claim, the URL, an exact quote copied from the opened page, and the date the page states (if any).
- If you only saw a search snippet, mark the claim [snippet only]. If you could not find something, say so; never guess numbers or limits.
- Do not write any files. Return your report as your final message.
- Keep the work bounded: at most about 12 searches and 15 page fetches, then write the report.
- Output format: (1) a short summary of findings, (2) a Markdown table: Claim | URL | Exact quote | Page date, (3) a list "Could not verify".

Your lane:

Lane "Render": the working default, checked in depth.
1. Render free web service today (render.com/docs/free, render.com/pricing): CPU, RAM, free instance hours per month and what happens when they run out, spin-down after idle and wake time, bandwidth and build-minute limits, regions (is Singapore available on free?), whether a credit card is required, and any 2026 changes to the free tier.
2. Persistent storage on free: is the disk ephemeral, are persistent disks available on free, and when exactly local files are lost (redeploy, restart, spin-down). Render free Postgres and Key Value: limits and expiry (for example free Postgres deleted after 30 days?).
3. Deploying FastAPI on Render: the official FastAPI quickstart, start command, Python version selection, render.yaml Blueprint, auto-deploy from a GitHub branch, health checks on free, and environment variables / secret files (are they kept out of the repository and logs?).
4. Keeping the service awake: does Render's policy forbid or discourage external pinging (cron-job.org, UptimeRobot) to prevent spin-down, and would pinging exhaust the 750 free hours? Any official statement.
5. Render's terms or docs on free services being suspended or deleted when unused for a long time.

Lane "alternatives": other free hosts that can run a FastAPI server with a secret env var and outbound HTTPS.
For each host give: free limits (CPU, RAM, hours or requests), sleep / cold start, whether a credit card is required, persistent disk or not, GitHub auto-deploy, secret env vars, region near Vietnam, and anything that makes it unusable (for example outbound internet allow-lists, no ASGI support, trial credits that expire before judging ends).
Hosts to check, current state in 2026: Hugging Face Spaces (Docker SDK and Gradio SDK on free CPU basic: is PRO really required now? read huggingface.co/docs/hub/spaces-overview, spaces-sdks-docker, pricing; secrets in Spaces; sleep after 48 h; persistent storage), Koyeb (free instance), Fly.io (is there still a free allowance for new accounts?), Railway (free plan or trial credit), Google Cloud Run (free tier, billing account required?), Vercel (Python runtime / FastAPI support, function limits, read-only filesystem), PythonAnywhere free (ASGI/FastAPI support, outbound internet allow-list: is generativelanguage.googleapis.com allowed?), Northflank free, Zeabur, Leapcell, Azure App Service F1, Google App Engine standard free quota, Oracle Cloud Always Free VM, Cloudflare Workers Python (can FastAPI run?), Deno Deploy is not Python so skip.
Drop any host quickly if it clearly needs payment; list it with the reason.

Lane "state and uptime": two cross-cutting needs of the demo on a free host.
1. Small persistent writes ("Báo sai" reports and conflict records, a few JSON lines a day) when the host disk is ephemeral. Compare free options usable from Python with no paid plan: (a) accept loss on restart and keep a seed file in the repo; (b) a free hosted database: Neon Postgres free (limits, scale to zero, does it expire?), Supabase free (pauses after inactivity? how long?), Turso / libSQL free, MongoDB Atlas M0, Upstash Redis free, Render free Postgres expiry; (c) committing to a GitHub repository or a Gist via the GitHub API with a fine-grained token (rate limits, security of putting a token on the server); (d) Google Sheets API. For each: free limits, inactivity pause or deletion rules, Python client, and the extra secret it needs.
2. Cold starts and uptime for a demo opened by judges days later: published guidance from Render, Koyeb or Hugging Face on idle sleep and wake time, whether free hosts allow keep-alive pings in their terms (quote them), free uptime-ping services (UptimeRobot free interval, cron-job.org) and their limits, and GitHub Actions scheduled workflows as a pinger (minimum interval, are scheduled workflows disabled after 60 days of repository inactivity?).
3. Keeping an API key secret in a public repository deployed to a free host: official guidance from GitHub (secret scanning, push protection) and Google (restricting a Gemini API key, key leak auto-revocation if any), quote it.
```

## Why it matters for v1

The answer decides where #11 deploys the walking skeleton and what #15 can promise about "Báo sai" and conflict records.
It also sets what the README must warn judges about.

Constraints any option must respect:

- Stack fixed by Hiep: Python, FastAPI with Jinja2 templates, run by uvicorn; Gemini answers and embeddings come over HTTPS, so no local model is loaded.
- Free means no payment; a credit card asked at signup counts against an option even if nothing is charged.
- The brief prefers an online link, and judges may open it days or weeks after 15/10/2026.
- `GEMINI_API_KEY` stays on the server as an environment variable, never in the public repository or the browser.
- The server must be in a country where the Gemini API is available.
- "Báo sai" and conflict records need small writes; Mission 1 V4 allowed them to "stay in a file" (`docs/mission2/plan.md`, cut order).
- The plan's definition of done already accepts a first load of about a minute, if the README says so.

## Options found

### Host

| Option | What it is | Strengths | Costs and risks | Fit for v1 | Sources |
|---|---|---|---|---|---|
| A. Render free web service (working default, D3) | A normal uvicorn process on 0.1 CPU and 512 MB, auto-deployed from a GitHub branch | Runs the app exactly as it runs locally; "No payment is required"; Singapore region; environment variables and secret files on the free plan; `render.yaml` Blueprint with `sync: false` for the key; health checks, custom domain and TLS included | Spins down after 15 minutes without traffic and takes "about one minute" to wake; local files are lost on spin-down, restart or redeploy, and Render "might restart a Free web service at any time"; 750 free hours per workspace per month; 5 GB bandwidth and 500 build minutes per month on Hobby; default Python is now 3.14.3, so 3.12 must be pinned; how long our imports take on 0.1 CPU is unmeasured | Good | S1, S2, S3, S4, S5, S6, S7 |
| B. Vercel Hobby (Python runtime) | FastAPI deployed with zero configuration as one Vercel Function on Fluid compute | Free; no 15-minute sleep and one-minute wake as on Render; up to 2 GB and 1 vCPU per function; the Hobby plan can set its single function region, for example Singapore (`sin1`) | Hobby is "restricted to non-commercial personal use only", and Vercel defines commercial use broadly ("financial gain of anyone involved in any part of the production"); whether a competition entry counts is for Hiep to judge or ask Vercel; the deployed filesystem is read-only except `/tmp` (lane report and Vercel community, not an official page opened by Claude), so even short-lived records need extra care; a serverless function behaves differently from the local uvicorn process; cold-start time for our imports is unmeasured; "No credit card is required" comes only from Render's comparison article, not from Vercel | Possible; strongest alternative | S8, S9, S10, S11, S12, S6 |
| C. Cloudflare Workers, Python | FastAPI on Cloudflare's Python Workers (Pyodide) through Cloudflare's own ASGI adapter | Free 100,000 requests a day; no sleep; network waits do not count as CPU time | Free plan allows 10 ms of CPU per request and 128 MB per isolate; only pure-Python and PyEmscripten packages are supported, and nobody checked whether `langchain-google-genai`, `google-genai` and their dependencies run there; a different runtime and deploy tool (`pywrangler`) from local development | Poor: too much unknown for 3 days | S13, S14, S15 |
| D. Koyeb free instance | One free 0.1 vCPU, 512 MB instance | Scale to zero after 1 hour instead of 15 minutes | Signup requires a credit card with a $29 pre-authorization hold, and the pro-rated Pro plan is charged on signup; free instances only in Frankfurt or Washington, D.C. | Out (card and charge) | S16, S17 |
| E. Hugging Face Spaces | Docker or Gradio Space on free CPU Basic | 2 vCPU and 16 GB on CPU Basic | "Gradio and Docker Spaces run on compute and require a paid plan to create: PRO for personal accounts"; only Static Spaces, and Gradio on ZeroGPU, stay free | Out (paid plan) | S18 |
| F. Fly.io | Machines from a Dockerfile | - | "Is there a free tier? No."; the trial lasts up to 2 hours of Machine runtime or 7 days | Out | S19 |
| G. Railway | Git deploy with runtime detection | No card for the trial | The Free plan includes $1 of usage a month and the trial $5 for 30 days; at Railway's rates ($10 per GB of memory and $20 per vCPU a month) that does not keep a server up all month | Out | S20 |
| H. Northflank Developer Sandbox | 2 free always-on services | No sleep | "All users must add a payment method to start creating resources on Northflank, regardless of plan selection"; free compute is only described as "Limited" | Out (card) | S21 |
| I. Google Cloud Run, App Engine, Azure, Oracle Cloud | Cloud free tiers | Generous Cloud Run free tier, Singapore region | Google Cloud signup asks for "a credit card or other payment method"; the lane reports the same for Azure and Oracle (not checked by Claude) | Out (card) | S22 |
| J. PythonAnywhere free | One free web app | No card | 100 CPU-seconds, a web app with "1 month expiry", ASGI hosting still in beta, and outbound internet only to an allowlist through a proxy (`.googleapis.com` is on the list) | Out | S23, S24 |
| K. Zeabur free | Git deploy with auto-sleep | "No credit card required"; Asian regions | Services "automatically sleep after a period of inactivity"; the free plan's compute limits are only in an image Claude could not read | Weak: limits unknown | S25 |

Region note: Singapore and Vietnam are on the Gemini API's list of available regions, and Hong Kong is not (S26).
So on any host the server should run in Singapore or the US, never in Hong Kong.

### Keeping the demo awake (applies to option A)

| Option | What it is | Strengths | Costs and risks | Fit for v1 | Sources |
|---|---|---|---|---|---|
| L. Let it sleep and warn | README says the first load can take about a minute; Render shows a loading page meanwhile | Nothing to build; no grey area in Render's terms; already in the plan's definition of done | Each judge's first visit after 15 idle minutes waits about a minute, and the first visit after a spin-down starts with no new records | Good | S1, S6 |
| M. External pinger every few minutes | cron-job.org (free, down to every minute) or UptimeRobot (free, every 5 minutes, "Good for hobby and non-profit projects") calls a health URL | No wake wait for judges | Keeps the service up all month: 744 of the 750 free hours in a 31-day month, so a second free service in the same workspace would push it over and suspend both; Render's policy forbids load "for the purpose of evading payment", and no Render page allows or forbids pinging; still restarts "at any time" | Possible only for the judging window, Hiep's call | S1, S27, S28, S29 |
| N. GitHub Actions scheduled pinger | A cron workflow in the repository | No extra account | In a public repository, scheduled workflows are disabled after 60 days without repository activity; same hour use as M | Weaker than M | S30 |

### Where "Báo sai" and conflict records live (follows from the host)

| Option | What it is | Strengths | Costs and risks | Fit for v1 | Sources |
|---|---|---|---|---|---|
| O. A JSON Lines file on the server disk, seeded from the repository | Records append to a file; a few demo records ship in the repo, labelled "giả lập" | Matches Mission 1 V4; no new dependency or secret; a judge who presses "Báo sai" sees the record on the owners' page in the same visit | On Render free the file is lost on every spin-down, restart or redeploy, so records never last longer than the visit; the README and the owners' page must say so | Good for v1, with the limitation stated | S1 |
| P. Neon Postgres free | A hosted Postgres that scales to zero | "The Free plan is permanent (not a trial); no credit card required"; 1 GB storage; "None of these limits delete your data" | A new dependency (a Postgres driver), a second secret and a new moving part, which `AGENTS.md` says need Hiep's approval; wake time after scale to zero not found on an official page | Good if records must survive | S31, S32 |
| Q. Render free Postgres | Render's own free database | Same dashboard | Expires 30 days after creation and is deleted 14 days later, inside the judging window | Poor | S1 |
| R. Supabase free | Hosted Postgres | Free | Pauses a project after 7 days of low activity, and a human must click "Resume project" | Poor for an unattended demo | S33 |
| S. Commit records to GitHub through the API | The server writes to the repository with a fine-grained token | Records survive and are visible | A write token on the server of a public demo, and anyone on the page can push commits into the public repository; lane report only | Poor | - |

### Keeping the key secret (all options)

- Render and Hugging Face keep secrets as server-side environment variables (S5, S18; Vercel's was not checked); Render's docs warn "Don't commit the values of secret credentials to your `render.yaml` file!" and offer `sync: false` placeholders (S5).
- Since 28/05/2026, every new key made in AI Studio is an auth key, "restricted to the Generative Language API (Gemini API) by default" with "fast-acting leaked key enforcement"; unrestricted standard keys are rejected (S34).
- Google's own rule matches the design: "Never check API keys into source control" and "run a backend proxy server to make the actual API calls" (S34).
- On public repositories GitHub's secret scanning "runs automatically for free", and push protection for users "is enabled by default" (S35).
- Whether secret scanning recognises a Gemini auth key was not checked.

## Render vs Vercel

Added on 13/10/2026 at Hiep's request, after his decision, from pages Claude opened that day.
Nothing was deployed on either host, so no row is a measurement.

| Point | Render free web service | Vercel Hobby | Sources |
|---|---|---|---|
| How the app runs | One long-running uvicorn process, started with the same command as locally | One Vercel Function on Fluid compute; Vercel asks for `vercel dev` locally "instead of running Uvicorn directly" | S5, S8, S38 |
| Setup | `render.yaml` with build and start commands, or the same values in the dashboard | Zero configuration if the FastAPI `app` sits at a recognised entry file; static files go in `public/` instead of `app.mount` | S5, S38 |
| First load after idle | Spins down after 15 minutes; waking takes "about one minute" behind a loading page | No sleep of that kind; Fluid compute "reduces the effects of cold starts" with pre-warming on production, but Vercel gives no number | S1, S39 |
| Region | Singapore | One function region on Hobby, which can be set to Singapore (`sin1`) | S3, S11 |
| CPU and memory | 0.1 CPU, 512 MB | Up to 2 GB and 1 vCPU per function; 4 active CPU-hours and 360 GB-hours of memory a month, and waiting on an API call does not count as active CPU | S1, S9, S12 |
| Monthly allowance and what happens past it | 750 instance hours, 5 GB bandwidth, 500 build minutes; past the hours, free services are suspended until next month | 1,000,000 invocations, 100 GB fast data transfer and the CPU and memory above; past a limit, "you will have to wait until 30 days have passed" | S1, S6, S9 |
| Local files (conflict records) | Writable; lost on spin-down, restart or redeploy | Read-only except `/tmp`, which is per instance and short-lived (lane report and Vercel community, not an official page opened by Claude) | S1 |
| The Gemini key | Environment variable; `sync: false` keeps it out of `render.yaml` | "Secret" variables are write-only after saving, and a value of 32 characters or more is replaced by `[REDACTED]` in build logs | S5, S36 |
| Deploy from GitHub | Auto-deploys the linked branch | Production deploys from `main`, or `master` if there is no `main`; every other push gets a preview URL, which Standard Protection keeps private by default | S2, S37, S40 |
| Terms for our use | Hobby is "For individuals building personal projects and prototypes" | Hobby is "non-commercial, personal use only", with commercial use defined broadly | S6, S9, S10 |
| Card at signup | "No payment is required" (Render's own guide) | Not stated on a Vercel page opened by Claude; only Render's comparison article says no card | S2, S6 |

In short: Render runs the app the way it runs on a laptop and keeps a file for a visit, at the cost of a one-minute first load.
Vercel removes that wait and gives far more memory, at the cost of a different runtime model, no usable local file for records, and a non-commercial clause Hiep would have to judge.

## Claims that did not hold up

1. **"Pinging every 5 minutes would consume ... ~54 minutes/month" of Render's 750 free hours (Render lane).**
   A service pinged every 5 minutes never reaches 15 idle minutes, so it runs all month: 744 hours in October, almost the whole allowance (S1).
2. **"Render free: Region: not near Vietnam (US/EU only)" (alternatives lane).**
   Render's regions page lists Singapore, with no free-plan restriction (S3).
3. **"Vercel region defaults to `iad1` ... can't be changed on Hobby" (alternatives lane).**
   Hobby is limited to a "Single region", but the default region can be changed in settings or `vercel.json` (S11).
4. **"Cloudflare Workers ... the strongest candidate", "FastAPI officially supported via Python Workers (GA since Sep 2026)" (alternatives lane).**
   FastAPI support is real (S13), but no opened page says "GA since Sep 2026", and the lane never checked whether our LangChain and Gemini packages run on Pyodide, which the packages page leaves open (S15).
5. **"Northflank: No credit card mentioned as required" (alternatives lane).**
   Northflank's billing docs say every user must add a payment method, whatever the plan (S21).
6. **"PythonAnywhere free blocks `generativelanguage.googleapis.com`" (alternatives lane).**
   `.googleapis.com` is on the allowlist (S24); PythonAnywhere is out for its CPU, expiry and ASGI limits, not for this.
7. **"On free hardware, a Space sleeps after 48 hours" (state lane).**
   The Hugging Face page only says "after a period of time if unused" (S18).
8. **"Neon ... wakes in ~1-5 seconds on the next connection" (state lane).**
   No opened Neon page gives a wake time.
9. **"Render free tier requires no credit card ... interpretation, medium confidence" (state lane).**
   Not false, but stronger than the lane said: Render's first-deploy guide states "No payment is required" (S2).

Not checked by Claude, so not used above: Azure F1's 60 CPU minutes a day, App Engine's 28 instance-hours a day, Oracle's $1 hold, Leapcell's quotas, Turso, MongoDB Atlas, Upstash and Google Sheets limits, Koyeb's 1-5 second cold start, and a DEV Community post saying Koyeb's free Starter plan closed to new signups after Mistral AI acquired Koyeb.

## AI recommendation (not a decision)

Claude's picks, each with its one-line reason (Claude's):

- **Host:** option A, Render free web service in Singapore, auto-deploying `master` through a `render.yaml` with `plan: free`, Python pinned to 3.12, `GEMINI_API_KEY` as `sync: false`, and a health check path.
  Reason: it is the only checked option that runs the same uvicorn process as local development, needs no card, and sits in a Gemini-supported region close to Vietnam; its costs (one-minute wake, lost files) are already accepted in the plan.
- **Awake:** option L, warn in the README, and open the link once before any live judging session.
  Reason: a pinger buys a faster first load at the cost of the whole free-hour allowance and a grey area in Render's terms.
- **Records:** option O, a JSON Lines file seeded with labelled demo records, with the loss on restart stated on the owners' page, in the README and as a `limitation` issue.
  Reason: it keeps Mission 1 V4's "records stay in a file" with no new moving part; P (Neon) is the upgrade if Hiep wants records to survive, and needs his approval as a new dependency.

The strongest alternative: option B, Vercel Hobby in `sin1`, if Hiep weighs a fast first load above running the same process as locally and is satisfied the competition entry is non-commercial personal use.

Open risks the documents cannot settle:

- How long the app takes to start on 0.1 CPU after a spin-down; #11 should measure the first load from a clean browser.
- Whether Render keeps the service and its hours as documented through the whole judging window; nothing published says Render deletes idle free services, but its terms allow suspension "for any reason" (lane report, S1 for restarts).

Questions for Hiep before the ADR: which option in each table, and in your own words why it beats the strongest alternative.

## Sources

All accessed 2026-10-13 by Claude.

| ID | Title and URL | Accessed | Quote that supports the claim |
|---|---|---|---|
| S1 | Render, Deploy for Free, https://render.com/docs/free | 2026-10-13 | "Render spins down a Free web service that goes 15 minutes without receiving any inbound traffic."; "This process takes about one minute. Render displays a loading page to connecting browsers while a service is spinning up."; "any changes to your web service's filesystem ... are lost every time the service redeploys, restarts, or spins down."; "Render grants 750 Free instance hours to each workspace per calendar month"; "If you consume all of your Free instance hours during a given month, Render suspends all of your Free web services until the start of the next month."; "Render might restart a Free web service at any time."; "Free Render Postgres databases expire 30 days after creation."; "After the grace period, Render deletes the database"; glossary: "`free`: 0.1 CPU / 512 MB RAM" |
| S2 | Render, Your First Render Deploy, https://render.com/docs/your-first-deploy | 2026-10-13 | "This tutorial uses free Render resources. No payment is required." |
| S3 | Render, Regions, https://render.com/docs/regions | 2026-10-13 | "Oregon, USA - Ohio, USA - Virginia, USA - Frankfurt, Germany - Singapore" |
| S4 | Render, Setting Your Python Version, https://render.com/docs/python-version | 2026-10-13 | "Current default Python version `3.14.3`"; "Add a file named `.python-version` to the root of your repo." |
| S5 | Render, Environment Variables and Secrets, https://render.com/docs/configure-environment-variables; Deploy a FastAPI App, https://render.com/docs/deploy-fastapi | 2026-10-13 | "They also protect you from committing secret credentials (such as API keys or database connection strings) to your application source."; "Don't commit the values of secret credentials to your `render.yaml` file!"; "`sync: false # For security, provide STRIPE_API_KEY in the Render Dashboard`"; FastAPI page: "Start Command `uvicorn main:app --host 0.0.0.0 --port $PORT`" |
| S6 | Render, Pricing, https://render.com/pricing; Platforms with a real free tier for developers in 2026, https://render.com/articles/platforms-with-a-real-free-tier-for-developers-in-2026 (2026-04-23) | 2026-10-13 | Pricing: "Hobby $0/month + compute For individuals building personal projects and prototypes."; Hobby: "5 GB included per month (then $0.15 per GB)"; "500 mins per month"; "Environment variables & secret files ✓"; "Health checks ✓"; article on Render: "No credit card is required."; on Vercel: "The free tier includes 100 GB of bandwidth per month. No credit card is required." |
| S7 | Render, Acceptable Use Policy, https://render.com/acceptable-use | 2026-10-13 | "Impose an unreasonable or disproportionately large load on our infrastructure ... especially for the purpose of evading payment or financial obligations." |
| S8 | Vercel, Deploy a FastAPI app on Vercel, https://vercel.com/docs/frameworks/backend/fastapi | 2026-10-13 | "When you deploy a FastAPI app to Vercel, it becomes a single Vercel Function. Vercel uses Fluid compute by default" |
| S9 | Vercel, Hobby Plan, https://vercel.com/docs/plans/hobby (last updated 2026-09-14) | 2026-10-13 | "The Hobby plan is free and aimed at developers with personal projects, and small-scale applications."; "the Hobby plan restricts users to non-commercial, personal use only."; "Function Invocations First 1,000,000"; "Fast Data Transfer First 100 GB"; "if you exceed your usage limits on the Hobby plan, you will have to wait until 30 days have passed"; "Active CPU 4 CPU-hrs"; "Provisioned Memory 360 GB-hrs" |
| S10 | Vercel, Fair Use Guidelines, https://vercel.com/docs/limits/fair-use-guidelines | 2026-10-13 | "Commercial usage is defined as any Deployment that is used for the purpose of financial gain of anyone involved in any part of the production of the project, including a paid employee or consultant writing the code." |
| S11 | Vercel, Configuring regions for Vercel Functions, https://vercel.com/docs/functions/configuring-functions/region (last updated 2026-08-11); Global network and regions, https://vercel.com/docs/regions | 2026-10-13 | "By default, Vercel Functions execute in Washington, D.C., USA (`iad1`) for all new projects ... You can set a new default region through your project's settings"; "Hobby Single region"; regions page: "sin1 ap-southeast-1 Singapore" |
| S12 | Vercel, Functions Limits, https://vercel.com/docs/functions/limitations; Python runtime, https://vercel.com/docs/functions/runtimes/python (last updated 2026-08-12) | 2026-10-13 | "Hobby 2 GB / 1 vCPU"; "Hobby: 300s default and maximum"; Python runtime: "3.12 (default)"; "The standard Python bundle size limit is 500 MB uncompressed."; limits page: "Waiting for I/O (e.g. calling AI models, database queries) does not count towards active CPU time." |
| S13 | Cloudflare, FastAPI in Python Workers, https://developers.cloudflare.com/workers/languages/python/packages/fastapi/ (last updated 2026-08-28) | 2026-10-13 | "FastAPI is supported in Python Workers."; "The Python Workers provide an ASGI server that you can use directly in your Python Worker" |
| S14 | Cloudflare, Workers Limits, https://developers.cloudflare.com/workers/platform/limits/ (last updated 2026-10-12) | 2026-10-13 | "Requests 100,000/day"; "CPU time 10 ms"; "Memory 128 MB"; "Waiting on network requests ... does not count toward CPU time." |
| S15 | Cloudflare, Python Workers Packages, https://developers.cloudflare.com/workers/languages/python/packages/ (last updated 2026-09-18) | 2026-10-13 | "Python Workers support pure and PyEmscripten Python packages on PyPI."; "WebAssembly support for Python packages is still in early stages, and some packages may not yet be available as PyEmscripten wheels on PyPI." |
| S16 | Koyeb, Pricing FAQ, https://www.koyeb.com/docs/faqs/pricing | 2026-10-13 | "We require a credit card to prevent fraud and abuse. We verify the card you enter by placing a $29 pre-authorization hold"; "Right after we place the $29 pre-authorization hold to verify your card, we also charge you the pro-rated amount for the plan you select."; "One `free` web Service in the Frankfurt or Washington, D.C. regions with 512MB of RAM, 0.1 vCPU" |
| S17 | Koyeb, Instances, https://www.koyeb.com/docs/reference/instances | 2026-10-13 | "They scale down to zero when they don't receive any traffic for 1 hour."; "They can't be used with Volumes to add persistent storage" |
| S18 | Hugging Face, Spaces Overview, https://huggingface.co/docs/hub/spaces-overview | 2026-10-13 | "Static Spaces are free for everyone. Gradio and Docker Spaces run on compute and require a paid plan to create: PRO for personal accounts, Team or Enterprise for organizations. Free personal accounts in good standing can still host up to 2 Gradio Spaces running on ZeroGPU."; "On free hardware, your Space will "go to sleep" and stop executing after a period of time if unused."; "Secrets to store access tokens, API keys, or any sensitive values or credentials. They are private" |
| S19 | Fly.io, Resource Pricing, https://fly.io/docs/about/pricing/ | 2026-10-13 | "Is there a free tier? No. New organizations don't have a free tier or a monthly free usage allowance. New accounts do get a free trial, which lasts for up to 2 hours of Machine runtime or 7 days, whichever comes first." |
| S20 | Railway, Pricing, https://railway.com/pricing | 2026-10-13 | "Free Trial $0 $5 one-time credit (30 days)"; "Free $0 $1/month 1 vCPU / 0.5 GB"; "Memory $0.00000386 per GB/s $10 per GB"; "CPU $0.00000772 per vCPU/s $20 per vCPU" |
| S21 | Northflank, Pricing on Northflank, https://northflank.com/docs/v1/application/billing/pricing-on-northflank; Pricing, https://northflank.com/pricing | 2026-10-13 | "all users must add a payment method to start creating resources on Northflank, regardless of plan selection."; pricing table: "Compute ... Limited" |
| S22 | Google Cloud, Free features and trial offer, https://docs.cloud.google.com/free/docs/free-cloud-features; Cloud Run pricing, https://cloud.google.com/run/pricing | 2026-10-13 | "During the sign up, you must provide a credit card or other payment method that is valid for the period of the Free Trial."; "Cloud Run ... 2 million requests per month. 360,000 GB-seconds of memory, 180,000 vCPU-seconds of compute time." |
| S23 | PythonAnywhere, Free Accounts Features, https://help.pythonanywhere.com/pages/FreeAccountsFeatures/; Deploying ASGI sites (beta), https://help.pythonanywhere.com/pages/ASGICommandLine/ | 2026-10-13 | "100 CPU seconds"; "1 web app with 1 web worker and 1 month expiry"; ASGI page title "Deploying ASGI sites on PythonAnywhere (beta)" |
| S24 | PythonAnywhere, 403 Forbidden error, https://help.pythonanywhere.com/pages/403ForbiddenError/; Allowlisted sites, https://www.pythonanywhere.com/whitelist/ | 2026-10-13 | "Free accounts' internet access goes via a proxy "allowlist"; they can only access sites that are on that list."; allowlist entry ".googleapis.com" |
| S25 | Zeabur, Free Plan, https://zeabur.com/docs/en-US/pricing/free-plan | 2026-10-13 | "No credit card required"; "Services on the Free Plan automatically sleep after a period of inactivity. They wake up on the next incoming request, which may cause a few seconds of cold-start latency." |
| S26 | Google, Available regions for Google AI Studio and Gemini API, https://ai.google.dev/gemini-api/docs/available-regions | 2026-10-13 | List includes "Singapore", "United States" and "Vietnam"; "Hong Kong" is not on the page |
| S27 | cron-job.org, FAQ, https://cron-job.org/en/faq/ | 2026-10-13 | "Our service is entirely free of charge."; "Every cronjob can be executed up to 60 times an hour, i.e. every minute." |
| S28 | UptimeRobot, Plans and Pricing, https://uptimerobot.com/pricing/ | 2026-10-13 | "Free $0/month Good for hobby and non-profit projects. No credit card required!"; "50 monitors - 5 min. monitoring interval" |
| S29 | Render free docs, S1, and Acceptable Use Policy, S7 | 2026-10-13 | No sentence on either page allows or forbids keep-alive pings |
| S30 | GitHub Docs, Disabling and enabling a workflow, https://docs.github.com/en/actions/how-tos/manage-workflow-runs/disable-and-enable-workflows | 2026-10-13 | "In a public repository, scheduled workflows are automatically disabled when no repository activity has occurred in 60 days." |
| S31 | Neon, Pricing, https://neon.com/pricing | 2026-10-13 | "The Free plan is permanent (not a trial); no credit card required." |
| S32 | Neon, Free plan limits and quotas, https://neon.com/faqs/free-plan-limits-and-quotas | 2026-10-13 | "Computes scale to zero after 5 minutes of inactivity"; "1 GB of Postgres storage per project"; "None of these limits delete your data." |
| S33 | Supabase, Project Pausing, https://supabase.com/docs/guides/platform/free-project-pausing | 2026-10-13 | "Supabase pauses Free Plan projects that show low activity over a 7-day period"; "Click Resume project and confirm" |
| S34 | Google, Using Gemini API keys, https://ai.google.dev/gemini-api/docs/api-key | 2026-10-13 | "Authorization keys are restricted to the Generative Language API (Gemini API) by default and provide fast-acting leaked key enforcement"; "Starting May 28, 2026, all new API keys created in Google AI Studio are automatically created as auth keys."; "The Gemini API rejects requests from unrestricted standard keys."; "Never check API keys into source control systems like Git."; "To secure client-side apps, run a backend proxy server to make the actual API calls." |
| S35 | GitHub Docs, Secret scanning, https://docs.github.com/en/code-security/concepts/secret-security/secret-scanning; Push protection, https://docs.github.com/en/code-security/concepts/secret-security/push-protection | 2026-10-13 | "Public repositories: Secret scanning runs automatically for free."; push protection for users "Is enabled by default" and "Stops you from pushing secrets to public repositories on GitHub" |
| S36 | Vercel, Config and Secret environment variables, https://vercel.com/docs/environment-variables/sensitive-environment-variables (last updated 2026-08-28) | 2026-10-13 | "Secret values are write-only after saving. Use them for passwords, API keys, and tokens."; "if a Secret environment variable value is 32 characters or longer and appears in build logs, Vercel replaces the value with `[REDACTED]`." |
| S37 | Vercel, Deploying Git Repositories with Vercel, https://vercel.com/docs/git (last updated 2026-09-18) | 2026-10-13 | "Preview deployments for every push."; "The `main` branch. - If not present, the `master` branch" |
| S38 | Vercel, How to ship a FastAPI app on Vercel, https://vercel.com/kb/guide/ship-a-fastapi-app-on-vercel | 2026-10-13 | "Run `vercel dev` for local development instead of running Uvicorn directly."; "FastAPI's own `app.mount("/public", ...)` is not needed on Vercel, so rely on the `public` directory instead." |
| S39 | Vercel, Fluid compute, https://vercel.com/docs/fluid-compute | 2026-10-13 | "Automatic cold start optimizations: Reduces the effects of cold starts through automatic bytecode optimization, and function pre-warming on production deployments." |
| S40 | Vercel, Deployment Protection, https://vercel.com/docs/deployment-protection | 2026-10-13 | "Standard Protection is the recommended option for most projects. It protects all domains except production domains."; "Standard Protection is available on all plans" |
