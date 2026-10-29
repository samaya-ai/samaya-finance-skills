---
name: samaya-kpi-history
description: >-
  "KPI history", "pull four years of [metric] for [company]", "track a reported KPI" — builds
  the full, primary-sourced history of a company-reported operating KPI (monthly, quarterly or
  annual; one company or a peer set) through Samaya, every period in the window present, a source
  on every figure, and gaps, definition breaks and revisions marked. Always delivered as a
  downloadable Excel file.
---

You are building the history of a number a company reports, and the reason this is worth a skill
is that the easy version fails quietly. Ask a model for "four years of XPO tonnage" and it returns
a dozen rows from press-release aggregators, assumes a reporting cadence the company never used,
skips the periods it could not find, and presents the result as complete. The analyst then
re-checks every figure by hand. This skill does the opposite: it establishes how the company
discloses the metric, builds every period the window requires, fills each one from the filing or
call it came from, and shows the analyst exactly what is missing and why.

> **The cardinal rule.** **Every period in the window has a row, and every row has a source or a
> stated reason it has none.** A series that is shorter than the window without saying so is a
> build failure. A figure with no document and date behind it does not go in the table.

> **The delivery rule.** **The product is a downloadable Excel file in the chat.** Every run ends
> with the `.xlsx` workbook sent to the analyst as a file attachment they can click and download.
> A chat summary without the attached Excel is a failed run. A file path printed in chat, or a
> file saved only on disk, is **not** delivery. Do not finish your reply until the Excel has been
> sent.

---

## STEP 0 — SAMAYA CONNECTIVITY GATE (hard requirement, before anything else)

**Do not begin until Samaya MCP is verified live.**

1. **Check the tool list** for `Samaya:financial_qa` and `Samaya:financial_qa_result`. If absent:
   **STOP.** Tell the analyst the Samaya connector is not active in this session and ask them to
   enable it (connectors icon in the Claude sidebar, or Settings > Connectors in claude.ai), then
   wait. Do not proceed, do not substitute another source, do not build "what you can".
2. **Call Samaya directly as your first action** — the disclosure-map query for the first company
   in scope — and confirm a substantive response. A tool that is listed but errors, times out or
   returns empty counts as NOT live.
3. **Retry ladder on any mid-run failure:** retry same session_id → fresh session → record the
   period as unretrieved and continue. **Never silently fall back to web search.**
4. **Non-Samaya sources require explicit analyst approval, per source**, with the true retrieval
   path stated.
5. **Samaya mechanics.** `financial_qa` returns citations, not an answer: write every figure from
   the snippets. Poll `financial_qa_result` by job_id until done; never re-send the same question
   to get a result. Parallel calls each take a fresh, empty session_id.

## EMPTY INVOCATION — say what this does, then ask

If the skill is invoked with no company, metric or thesis, do not guess. Reply with two lines on
what it does and three example prompts, one per entry route, then ask for theirs:

> I build the full history of a KPI a company reports — for one company or a peer set — with a
> source on every figure, as a downloadable Excel file, plus a short read of the trend. You can
> give me an exact metric, a rough one, or a thesis you want tested.
>
> - **Exact:** "Barclays UK NIM, quarterly, Q1 2021 to Q2 2026"
> - **Rough:** "Chipotle traffic over the last two years"
> - **Thesis:** "I think Dutch Bros' food launch is driving a durable traffic lift — what data
>   would show it?"
>
> Which company and what would you like to see?

## KICKOFF — route the request, state the defaults, then build

Only the **company** blocks. Everything else has a default and the default runs.

1. **Company or companies** *(blocking)* — one name, a list, or a peer set the analyst names.
2. **Metric** — exact, rough, or absent with a thesis given. Routed below.
3. **Window:** **the last 12 months, ending at the latest period the company has reported
   (default)**, or any period the analyst names.
4. **Frequency:** **the finest cadence the company discloses for that metric (default)** —
   established by the disclosure map, never assumed. Twelve months of a monthly metric is twelve
   rows; of a quarterly metric, four; of a half-yearly metric, two.
5. **Sources:** **company disclosures only (default)** — filings, releases, results
   presentations, earnings-call and conference transcripts. Broker research only on request,
   labelled as such and never mixed into a reported-actuals column.
6. **Output:** **the attached Excel plus a chat summary — always** (the delivery rule). A table in
   chat, if asked for, is added on top and never replaces the workbook.

State the plan in one line and build:
`No period given — pulling the last 12 months. XPO discloses this monthly (8-K releases and
earnings calls), so 12 monthly rows. You'll get a downloadable Excel at the end.`

### Routing — three entry routes into one pipeline

| Input | Route |
| --- | --- |
| **Exact** metric, company, period | Disclosure map → grid → retrieve → gap pass → Excel delivered. No questions. |
| **Rough** metric ("traffic", "churn") | Disclosure map resolves it. One clear reported match: state the reading in one line and run. Several genuine candidates: show a 2–4 item menu with cadence and history depth, default pre-selected, and wait. None: say so and offer the closest disclosed proxy, labelled as a proxy. |
| **Thesis** only | Thesis mode (below): propose KPIs → disclosure check → **analyst confirms** → pipeline → per-KPI evidence read → Excel delivered. |

## THE DISCLOSURE MAP — always first, per company

Before any figure is retrieved, establish for each company and metric:

- **The exact reported label** and the company's definition of it (e.g. "tonnage per day, North
  American LTL, year-over-year %", not "tonnage").
- **Where it is disclosed**: monthly operating-data 8-K, quarterly release, results presentation,
  call transcript only, 10-Q/10-K, annual report.
- **The cadence**, including figures that exist only on a call — monthly figures inside a quarter
  that the release reports only as a quarterly total.
- **When disclosure starts** and whether it has stopped.
- **Fiscal calendar**: year-end, quarter labels, 52/53-week years.
- **Known breaks**: redefinitions, re-segmentations, restatements, accounting changes, M&A that
  changes the scope.

Where the analyst's premise does not match the disclosure, correct it in the plan line before
building — "XPO does not publish daily tonnage; it reports tonnage per day, monthly, as a YoY %."
Correcting the premise is part of the product, not a caveat.

**Combine the map with the most recent block.** One call asks for the label, definition,
location, cadence and start date **and** the values for the most recent block of periods (the
first chunk in `references/retrieval-and-gaps.md`). For the 12-month default this one call often completes the retrieval. Any
values it returns go straight into the grid and are not fetched again.

**Disclosure that starts or changes inside the window.** Periods before the finer cadence began
stay in the grid at that cadence with status `Not disclosed`, and the coarser figure that does
exist (the quarter) goes in the row's Note — never spread across the months.

**Start-date guard — never trim on a guess.** Periods before the start date are skipped without a
query **only** when the map returns an explicit company statement of when the disclosure began
(XPO, Q1 2023 call: "we're going to be providing monthly tonnage data starting this quarter").
Otherwise the earliest document found is not proof of a start: send one **boundary probe** for the
block just before it, and trim only what that probe confirms is not disclosed. Figures are often
given retrospectively — XPO's first monthly 8-K was for May 2023, but January–April 2023 were
disclosed on the calls.

## THE GRID — every period exists before any value does

Build the full row set for the window at the disclosed cadence **before retrieval**. Every
expected period is a row from the start, so a period that cannot be found surfaces as a gap
rather than disappearing. Where the cadence changed inside the window (quarterly, then monthly),
the grid follows the disclosure and the Notes tab records the change.

## RETRIEVAL, GAP PASS AND RECONCILIATION

**Read `references/retrieval-and-gaps.md` before the first retrieval call** and follow it in
full: chunking by cadence, document anchoring, parallel calls and polling, the slow-chunk and
large-job rules, the two-step gap pass, and the reconciliation rules with the status vocabulary
every row carries (`Final`, `Preliminary`, `Derived`, `Comparative`, `Proxy`, `Not disclosed`,
`Not retrieved`, `Not yet reported`).

## MULTIPLE COMPANIES — the peer panel

- **One disclosure map per company.** The same concept carries different labels and definitions
  across companies ("NIM", "customer spread", "NII / average assets"); each company's definition
  is shown beside its values.
- **Calendar alignment.** Report each company's fiscal periods and map them to calendar quarters
  so a May year-end lines up against December peers.
- **Comparability flags, not silent normalisation.** Cells that are not like-for-like — a
  different definition, currency or cadence — are marked.
- **Plan check.** Above roughly 8 companies or 5 years, show the call plan and estimated time and
  confirm before running.

## THESIS MODE — from a claim to the KPIs that test it

Used when the analyst has a view but not the metric.

1. **Translate the thesis into 2–4 testable, reported KPIs**, with one line each on why it bears
   on the claim. **Include at least one KPI that could disprove it**, and mark which way each
   would cut. A list of only supporting metrics is a build failure.
2. **Disclosure check before proposing.** Show, per KPI, whether the company reports it, at what
   cadence and since when. A metric that would be ideal but is not disclosed is shown as
   unavailable, not dropped silently.
3. **Look for a natural comparison.** Where the company discloses a group the change did not reach
   — shops that cannot run the new program, regions not yet rolled out, franchise vs company
   units — propose it alongside the KPIs. A difference between the two groups tests a thesis
   far better than a single trend line.
4. **Wait for confirmation.** This is the one route that blocks after kickoff, because the
   choice of metrics is the analyst's call. If the analyst says "go", run the first two.
5. **Build the confirmed KPIs** through the standard pipeline, ending with the attached Excel.
6. **Per-KPI evidence read**, in place of plain trend bullets: for each KPI, whether the series is
   `consistent with`, `inconsistent with`, or `not informative on` the thesis, with the numbers and
   periods that make it so. **No overall verdict.** Weighing the evidence into a call, or arguing
   both sides, is a separate request the analyst can make through `use-samaya`.

## HARD RULES

1. **Disclosure before retrieval.** No figure is fetched until the metric's label, definition,
   cadence and start date are established.
2. **The grid is the window.** Every expected period has a row; the table is never silently
   shorter than the window.
3. **Primary sources by default.** Aggregator sites, news rewrites and broker tables are not
   sources for reported actuals unless the analyst approves them, and then they are labelled.
4. **No silent estimates.** Derived, comparative and proxy values carry their status and their
   working. Interpolation is never used.
5. **Breaks are visible.** A redefinition, restatement or cadence change is marked in the series
   and explained on the Notes tab.
6. **Describe, do not characterise.** Trend bullets state direction, magnitude, inflections and
   breaks with the numbers. No "strong", "impressive" or "worrying".
7. **Only the company's own words count.** A figure an analyst states in a call question is not a
   disclosure, even when management does not correct it.
8. **Name what is missing, individually.** Every `Not disclosed` and `Not retrieved` period is
   listed in the chat summary, not counted.
9. **No Excel, no deliverable.** The delivery rule above, without exception.

## OUTPUT

### Step 1 — Build the Excel workbook

One workbook per run, named `<Company or Peer set> <Metric> <Window>.xlsx`. Build it with the
bundled `scripts/build_workbook.py`: write the grid as the JSON spec documented at the top of that script and
run it (`python scripts/build_workbook.py spec.json out.xlsx`; it needs `openpyxl`, which most
sandboxes have — otherwise `pip install openpyxl`). Save the output in the session's outputs
folder (e.g. `/mnt/user-data/outputs/`) when one exists. Do not write workbook code by hand; the
script fixes the layout, statuses, notes and gap shading so every run looks the same. The workbook
holds:

1. **Series** — one row per period (per company × period for a peer panel): the period label, one
   column per metric, status, a Source column per metric hyperlinked to the provenance link, and a
   Note. Put the unit and basis in the metric name ("Tonnage/day YoY %"). Each value cell carries
   a cell note with the document, date, the sentence or table row containing the figure, and the
   provenance link. Gap rows are shaded.
2. **Pivot** — peer panels only: periods down, company × metric across.
3. **Chart** — single-company runs: one line chart of the metrics.
4. **Notes & breaks** — the disclosure map per company: definition, cadence, start date, breaks,
   proxies used and why, and anything deliberately excluded.
5. **Scorecard** — the same figures as the chat scorecard.

Provenance links are used exactly as the retrieval returns them (currently short links of the
form `https://app.samaya.ai/u/…`). Never reconstruct, normalise or invent one. The citation rules in
`references/samaya-conventions.md` apply on top of these.

### Step 2 — Deliver the Excel as a downloadable file (mandatory)

A file created by a script is **not** visible to the analyst until you send it. Right after the
workbook is built and checked:

1. **Send the `.xlsx` into the chat as a file attachment** using the file-delivery tool (in Cowork:
   `SendUserFile` with the workbook path, `display: "attach"`). The analyst must see a download
   card for the Excel.
2. **If a folder from the analyst's computer is connected**, also save the workbook there and say
   the folder and file name in plain words.
3. **If sending fails**, say so plainly in the reply and retry once; never end the run silently
   without the file.
4. **Never** say "the workbook is attached" unless the send step succeeded.

Send the Excel **before** writing the final chat summary, so the summary can point to it.

### Step 3 — Chat summary, in this order

1. **Plan line** as stated at kickoff, including any premise correction.
2. **Scorecard**:
   `Periods: 44/48 found · Not disclosed: 4 (Sep–Dec 2022, before monthly reporting began) ·
   Sources: 39 call transcripts, 5 filings, 0 web · Derived: 0 · Breaks: 0 · Time: 5 min 25 s`
3. **Trend read** — 3–5 bullets (thesis mode: the per-KPI evidence read), each with the figures
   and periods behind it and a link to the source.
4. **Gaps and breaks** — each missing period named with its reason; each break with its date.
5. **The Excel** — one line pointing to the attached, downloadable workbook ("The Excel is attached
   above — click to download") and what its tabs hold.

Do not repeat the series table in chat; the workbook carries it.

## BOUNDARIES AGAINST NEIGHBOURING SKILLS

- **One current figure** ("what was Q2 backlog?") — plain Samaya Q&A, not this skill.
- **Guidance changes and management language** — `samaya-guidance-credibility`, or
  `samaya-guidance-sweep` and `samaya-management-narrative-drift` through `use-samaya`.
- **Rolling a model forward** — `samaya-model-update`.
- **Checking figures already in a document** — `samaya-fact-checker`.
- **A verdict on a thesis or the argued cases** — plain Samaya Q&A through `use-samaya`.
- **Consensus and forecasts** — out of scope; this skill builds reported history only.

## VALIDATION GATES — before handing back

- Samaya verified live before the first build step; no silent web fallback anywhere.
- Disclosure map completed for every company before retrieval; any premise correction stated.
- No period trimmed as `Not disclosed` without an explicit company statement or a boundary probe
  confirming it.
- Window ends at the latest reported period unless the analyst named one; unreported periods
  carry `Not yet reported`.
- Grid row count equals the window at the disclosed cadence, per company.
- Every value has a document, date, excerpt and working provenance link; no fabricated link.
- Every empty cell went through the two-step gap pass and carries a status and reason.
- Derived, comparative and proxy values labelled with their working.
- Breaks marked in the series and explained on the Notes tab.
- Peer panel: definitions shown per company, calendars aligned, non-comparable cells flagged.
- Thesis mode: at least one disconfirming KPI proposed; a natural comparison group proposed where
  one is disclosed; analyst confirmation recorded; no overall verdict given.
- Workbook built with `scripts/build_workbook.py`, not hand-written code.
- **The `.xlsx` was sent to the analyst as a downloadable attachment in the chat, and the send
  step returned success.** A path in text does not pass this gate.
- Scorecard present in chat and workbook, with elapsed time.
- One workbook delivered; no partial files except a labelled large-job preview.

## SCOPE — what this does and does not do

- **Builds reported history; it does not forecast.** Guidance, consensus and estimates are other
  skills' work.
- **Completeness is bounded by disclosure.** Smaller names, private companies, metrics given only
  on calls and periods before transcript coverage are systematically harder; the scorecard and
  gap list say so rather than hiding it.
- **Tests evidence for a thesis; does not decide it.**
- **Most useful** when the analyst would otherwise pull the same metric period by period and
  stitch the answers together by hand.
