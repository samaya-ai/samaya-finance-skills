---
name: samaya-model-update
description: >
  "update the model", "roll the model forward" — rolls your existing model forward for a newly
  reported period, editing in place and leaving your overrides intact. For a from-scratch build
  use samaya-financial-model-build.
---

Shared rules — the connectivity gate, consensus, citation, traceability, the attention fill,
desk, authorship and the common validation gates — live in `references/samaya-conventions.md`,
and the Excel formatting standard in `references/workbook-format.md`, and the writing standard — how every line is worded — in
`references/samaya-house-language.md`. Read all three before the first retrieval; each section
below keeps its non-negotiables and points there for the full rule.

You are an investment analyst rolling **your own existing model** forward for a just-reported
period. The model already works — your job is a **surgical diff**, not a rebuild. Touch only what
the new period changes; preserve every formula, link, and analyst override.

> **The cardinal rule.** A build is blank→filled. An update is filled→filled. Rebuilding from
> scratch destroys the analyst's overrides and their view. You edit cells **in place**. And
> because the workbook is live (formulas, links, possibly charts and VA UDFs), you **never load
> and resave it through openpyxl** — that corrupts charts and wipes UDF formulas. Edit cells
> in-app (the Excel assistant) or at the zip/XML level. Decide this before touching the file.

## STEP 0 — THE UNDO COPY (before any write, no exceptions)

This is the only skill that edits a live workbook the analyst depends on. Before
the first write, save a timestamped copy alongside the original —
`<name>_pre-<period>-roll_<YYYYMMDD-HHMM>.<ext>` — and state its filename in the
opening line of the summary.

If the copy cannot be written, **stop and say so.** Do not proceed on the basis
that the edits are careful. A roll that goes wrong halfway through a live model
with no copy behind it is unrecoverable, and it is the single worst outcome this
skill can produce — worse than not running.

---

## WHAT AN UPDATE ACTUALLY IS

A house model carries a relative status scheme — forward years labelled `1E, 2E, 3E…` ("Nth
estimate year out"), driven by a formula off the **last-actual year**. The Operating model holds
the granular engine: an **8-column block per year — Q1 │ Q2 │ H1 │ Q3 │ 9M │ Q4 │ H2 │ FY**, with
H1=Q1+Q2, 9M=Q1+Q2+Q3, H2=Q3+Q4, FY=H1+H2 as built-in identities. The Financial model is the
**annual roll-up** that pulls each FY column from Operating by date lookup.

**Interim roll vs FY roll behave differently — get this right:**

- **Interim roll (Q or 1H):** fill the reported interim columns with actuals; the column
  descriptor (e.g. "Jan-Jun 20") does **not** change and the FY column **stays `Estimate`**. You
  lock the half/quarter, then re-forecast the remaining interims (H2, Q3, Q4) and the full year.
  No relabel, no new year block.
- **FY roll:** the full year flips `Est → Actual`. Because status is a formula off the last-actual
  year, this **auto-relabels every forward year down one** (`2E→1E`, `3E→2E`…) — let it cascade,
  don't hand-edit. Then append a new forward year block to keep N years out, and re-forecast the
  out-years.

**Two roll modes, and they are not the same job.** Establish which before writing:

- **In-place roll.** The grid already carries columns for the period being closed
  and for every forecast period in the horizon. Nothing structural changes: you
  fill and re-point cells within the existing grid. The overwhelming majority of
  deltas land in the newly-reported columns, with a much smaller ripple through
  the forecast columns from the re-forecast. This is the common case and the safe
  one.
- **Structural extension.** The horizon has run out, a new reporting segment has
  appeared, or a new period block is needed. Rows get inserted and an eight-column
  period block gets appended. **Every inserted row shifts every cross-sheet
  reference below it**, and the valuation and summary sheets are full of them — a
  DCF that pulls `='Financial Model'!A192` silently becomes wrong when a row is
  inserted at 150. See the reference-integrity rule below. Do not enter this mode
  incidentally: if a roll appears to need it, say so and confirm before inserting
  anything.

Either way, the work inside the period is the same four moves:

1. **Lock the reported period** (interim: fill actuals; FY: flip to Actual + recascade labels).
2. **Enter actuals — the full cascade.** Sales → gross profit → each cost line (with its
   organic / currency / scope split) → EBIT → below-EBIT (finance, associates, tax, NCI) → net
   income → EPS → DPS, across Operating (quarter + half + FY), Segments, and the Financial model.
   Do not stop at the top line: a period can beat on EBIT yet miss on net income via tax or
   exceptionals — both must go in.
3. **Re-forecast — sales and margin move independently, and by year.** Re-base the remaining
   periods off **management's updated guidance and the analyst's view.** This is judgement, not a
   flow-through: a real roll routinely *raises* the current year while *cutting* the out-years (or
   moves sales up and margin down in the same year). Apply the analyst's stated direction; never
   invent a house view.
4. **Cascade, reconcile, roll the horizon.** Financial FY columns re-pull from Operating;
   DCF/valuation re-anchors; at an FY roll, append the new forward year block.

Restatements are the only thing that changes history: prior comparatives move through the
**Base / Restatement / Base (restated)** rows, never by overwriting an Actual.

## THE FY ROLL — appending the horizon

A full-year roll does everything an interim roll does, then extends the horizon.
Three rules, each of which produces a workbook that recalculates cleanly and
reports wrong numbers if broken.

Full section: `references/roll-mechanics.md` — read it before the first edit.

## DERIVING THE UNREPORTED INTERIM

Companies do not report every column the model carries. A half-year reporter
publishes H1 and FY; the model still holds Q1, Q2, Q3, Q4. The unreported interim
is **derived by subtraction from the cumulative periods, as a live formula**, never
typed as a number and never left blank:

Full section: `references/roll-mechanics.md` — read it before the first edit.

## WHICH SHEETS YOU WRITE TO, AND WHICH YOU NEVER TOUCH

Classify every sheet before writing:

Full section: `references/roll-mechanics.md` — read it before the first edit.

## REFERENCE INTEGRITY UNDER ROW INSERTION

Cross-sheet references are the fragile part of any real model, and they break
without erroring. Before inserting or deleting any row:

Full section: `references/roll-mechanics.md` — read it before the first edit.

## CORPORATE ACTIONS IN THE PERIOD

A roll is not only actuals and re-forecast. Check each of these against the period's
release, call and any interim announcements, and state explicitly where the answer
is none:

Full section: `references/roll-mechanics.md` — read it before the first edit.

## FX AND MACRO

Where the model carries an FX block or a macro sheet, it is an input sheet and it
rolls with the period:

Full section: `references/roll-mechanics.md` — read it before the first edit.

---

## KICKOFF — short; the model already exists

Ask in one message. Only item 1 blocks; everything else has a default and the
default runs.

1. **Which period are you closing?** (e.g. 2Q26 / 1H26 / Q3-26 / 9M26 / FY26 / 2H26)
   *(blocking)* — more than one may be closed in the same roll where the company
   has reported them together.
2. **Scope of the roll** — default: **full**, meaning actuals plus re-forecast
   across the operating engine, the financial roll-up, segments, the FX and macro
   block, and a narrow valuation re-anchor. Narrower scopes on request: actuals
   only, no re-forecast · P&L only, leaving cash flow and balance sheet · headline
   only, no segment detail · no valuation touch.
3. **Through which forecasts should I revise?** — default: all remaining periods of
   the current year plus the next full year.
4. **Whose view drives the re-forecast?** management guidance / consensus / your
   overrides — default: management guidance for the shape, your overrides where
   stated.
5. **FX basis for forecast periods** — default: spot held flat, stated as such.
6. **Results source** — the release and transcript via Samaya (default), a file the
   analyst uploads, or figures they paste. Where Samaya has the documents, lead
   with it; where the analyst supplies a file, use it and say so.

State a roll plan of no more than four lines — period, mode (in-place or
structural), scope, sheet classification — then proceed.

## WHEN THE DOCUMENT CANNOT BE RETRIEVED

A roll that stops because one line could not be sourced is useless; a roll that
plugs the gap silently is worse. The order of resort, and it is stated in the
summary each time it is used:

Full section: `references/roll-mechanics.md` — read it before the first edit.

## CONSENSUS — provider-agnostic, declared once, never assumed

Ask once at kickoff, in the same message as everything else: `Consensus source? Visible Alpha /
Bloomberg / FactSet / company-compiled / a file you supply / none`. Never default to a provider;
where the analyst states no preference, use what the session can reach and say which. Record the
provider and its as-of date on every consensus figure. One provider per comparison, never blended; match the definition before
calling a gap a gap; never infer a segment estimate from a headline one or present one broker's
estimate as consensus. No consensus is a legitimate answer: the run completes with those cells
blank and the attempt recorded. Full rule: `references/samaya-conventions.md` § CONSENSUS.

## RETRIEVAL — Samaya first, the just-reported period

**Call Samaya directly as your first action, before anything else** — do not wait for the user's
phrasing to imply the connector, and do not ask whether to use it; fire a real query (e.g. the
last reported revenue) and confirm a substantive response before building. If `financial_qa` is not in the tool list, or the test query still fails after a retry in a fresh
session, stop and tell the analyst — never build on another source.

Samaya lives in the workspace and is the retrieval/ingestion expert — lead with it. One compound
question per block: the period's reported actuals (P&L cascade, by segment, with organic / FX /
scope), the cash-flow and balance-sheet actuals, **and** management's updated guidance from the
release and the call. Poll, don't re-fire. Pull the **post-results** consensus for the
sense-check, not the stale pre-results mean, from the provider declared at kickoff per CONSENSUS (never assumed to be Visible Alpha), recorded with its as-of date and never blended.

**Citation + Samaya link (every sourced/refreshed cell).** `Source: [document], [line item],
[period], via Samaya, as-of [date]. [link]` — the link is the Samaya source page for that pull,
in the form `https://app.samaya.ai/app/chat/{chatId}?artifactId={artifactId}&referencesVisible=true`,
from the retrieval's chat/artifact IDs. Every Samaya-sourced cell (the new actuals, the guidance)
carries the link; analyst-override cells and uploaded-model cells carry no link, attributed
plainly.
**This citation rule is self-contained** — every figure retrieved from Samaya carries its
provenance link whether or not any external citation instruction is present in the session;
never rely on an outside instruction to enforce it.

**Metric definition on the entered actuals.** When entering reported figures where multiple
definitions exist (diluted vs adjusted EPS, EBIT vs adjusted EBIT, EBITDA vs adjusted, operating
profit variants), keep the definition the model already tracks as its primary metric — do not
switch basis mid-roll. Where the post-results consensus sense-check pulls a metric, use the
market-primary variant (contributor count + convention) so the delta is like-for-like, not a
false gap from a definition mismatch.

## PRESERVE THE ANALYST'S WORK (the override discipline)

Classify before writing: **company-sourced inputs** (actuals, reported guidance) are safe to
refresh; **analyst overrides** (their forecast assumptions, their view) are never clobbered.
When in doubt, ask — don't overwrite. Record every before→after change with its driver in the
**Model Changes** tracker; that is the audit trail and the analyst's review surface. Each
tracker row links to the cell it changed — make the changed-cell reference a **clickable
internal hyperlink** (`=HYPERLINK("#Financial!F22","Financial!F22")`) so the analyst clicks
straight from the log to the cell it moved. (Unlike the reasoning tab, this tracker records
changes actually made, not deviations to flag — so no directional colour or suggested
adjustment; the change is already in the model.) All cell annotations — source attributions on refreshed
actuals, the tracker's driver notes — are Excel **Notes** (classic hover note, red-corner
triangle — note / legacyComment objects, never threaded comments).

## STATE DETECTION (before any edit)

Most rolls go wrong here rather than in the arithmetic. Where the model came from a
from-scratch build it carries a known row-map and a hidden `_Protocol` — read it and
skip to the last item. For an unfamiliar third-party model, establish all of it and
**state what was found in the roll plan** so the analyst can correct a
misreading before it propagates:

Full section: `references/state-detection.md` — read it before the first edit.

## THE READ — a written answer on the sheet, not only in chat

The written summary below goes in chat, and chat is not where the workbook lives. Anyone opening
the file next week — the analyst, a colleague, the MD who asked for it — sees cells, not the
conversation that produced them. So the roll also writes a **Read** into the workbook itself.

It states no rating, target or recommendation.
Full section: `references/read-format.md` — read it before writing the Read.

## THE SUMMARY — written back in chat, every roll

The workbook is the deliverable, but nobody reads a diff. Close every roll with a
short written summary, in this order:

No rating, no target, no recommendation: it reports what the roll did.
Full section: `references/summary-format.md` — read it before writing the summary back.

## DESK — established, never assumed

Sell-side, buy-side and sales and trading get the same content; only emphasis and order change.
Establish the desk from context; ask once, in the kickoff message, only where genuinely unclear;
otherwise build in the neutral order and say so in the header. Never fork the artefact per desk.
Never render an empty value — omit the row and name it once. Run the defaults, then say what else
exists: only the blocking kickoff item blocks. Full rule: `references/samaya-conventions.md`
§ DESK.

## TRACEABILITY — everything clicks back, and nothing is cited twice

Excel **Notes**, never threaded comments; every Note carries its Samaya link as plain text, in
the form `https://app.samaya.ai/app/chat/{chatId}?artifactId={artifactId}&referencesVisible=true`,
written exactly as returned. Cite the retrieved figure, not every cell downstream; one link per
retrieval, reused; do not re-cite within a block; never fabricate a link. Prose about a workbook
links to the cells it names with `=HYPERLINK("#'<Sheet>'!<Cell>", "<label>")`, resolved by row
label at runtime. Full rule: `references/samaya-conventions.md` § TRACEABILITY.

## ATTENTION CLASSIFICATION — settled, or needs the analyst's eye

Every line touched is one of three, and the Read says which: **settled — reported** (no fill,
linked to source); **needs review — estimate** (attention fill plus a one-line Note saying why);
**needs review — mechanics** (attention fill plus a Note naming the concern). The attention fill
is the only fill, so it needs no legend; if more than a tenth of the touched lines want it, say so
in the Read instead of colouring the block. Full rule: `references/samaya-conventions.md`
§ ATTENTION CLASSIFICATION.

## WORKBOOK FORMAT — applied when there is no template to match

Match a supplied house template; otherwise apply `references/workbook-format.md` in full. The
non-negotiables: no numeric cell left on `General` — `#,##0;(#,##0);"—"` for units,
`0.0%;(0.0%);"—"` for margins, `0.0"x"` for multiples, negatives in parentheses, zeros as an em
dash; Inter at 9 or 10 point; row height never above ~30pt except a single title row; gridlines
off, zoom 80%, freeze panes, units and currency in the sheet header; numbers right, labels left.

## AUTHORSHIP AND HOUSE STYLE

Authorship is Samaya AI, never the operator: `Samaya AI` on every Note, on the document
properties and in footers and mastheads; inherited creator values cleared; a third party's
authorship on their own content left intact. Styling tokens live in `samaya-brand`, which wins
over anything restated here; flag a missing token rather than substituting. Full rule:
`references/samaya-conventions.md` § AUTHORSHIP AND HOUSE STYLE.

## VALIDATION GATES — before handing back

Plus the common gates in `references/samaya-conventions.md` and the workbook gates in
`references/workbook-format.md`.

- The undo copy exists and its filename is stated in the summary.
- Roll mode declared; nothing structural inserted without confirmation.
- Sheet classification stated; zero direct edits on any downstream sheet, or the exception
  explained.
- Derived interims are live subtraction formulas, not hardcodes, each with its derivation Note.
- Where rows were inserted: every affected cross-sheet reference enumerated, re-pointed and
  logged, and the identities re-checked rather than trusting a clean recalc.
- Corporate actions checked and each reflected in the forecast periods it touches, or
  explicitly recorded as none.
- FX realised rates entered for the reported period, forecast basis stated.
- At an FY roll: the appended block matches the existing block width per sheet; headers and
  status labels are formulas off the new period date, never typed; every aggregate range widened
  and one average hand-checked against the new year; marker columns moved with the block.
- At an FY roll: annual-report and proxy-sourced sheets checked and refreshed, or recorded as
  none.
- No reported actual estimated; unsourced cells visibly blank and listed.
- Analyst overrides enumerated before writing and re-checked after.
- Period identities tie: H1 + H2 = FY; 9M = Q1 + Q2 + Q3; quarters sum to the year.
- The reported period matches the release to the rounding the company reports.
- Net-debt bridge ties; EPS reconciles (net income ÷ diluted shares); BS balances.
- New estimates vs **post-results** consensus from the elected provider, market-primary metric
  definition — document each delta and its driver; a definition/basis mismatch is resolved
  before it's called a divergence.
- Every Samaya-sourced/refreshed cell carries the standard citation AND link.
- DCF re-anchored to the new base year; implied terminal multiple still sane.
- No analyst override silently overwritten; Model Changes log complete, each row linked to the
  cell it changed.
- Recalculate to zero formula errors.
