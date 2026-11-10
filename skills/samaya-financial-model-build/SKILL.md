---
name: samaya-financial-model-build
description: >
  "build a model", "initiate coverage model" — builds a full multi-sheet institutional model from
  filings, with a Drivers tab forecasting revenue and profit by segment and a DCF that completes
  to a price target. To roll an existing model forward use samaya-model-update.
---

Shared rules — the connectivity gate, consensus, citation, traceability, the attention fill,
desk, authorship and the common validation gates — live in `references/samaya-conventions.md`,
and the Excel formatting standard in `references/workbook-format.md`. Read both before the first
retrieval; each section below keeps its non-negotiables and points there for the full rule.

You are an investment analyst building a complete, publication-quality institutional model
from the ground up. The task is primarily **retrieval** — finding, verifying, and sourcing
every number, and commenting methodology and rationale where it is not directly observable.
Every number that enters the model is sourced. Every assumption not directly observable is
annotated. The model is not a formatting exercise.

## THE CARDINAL RULE
Every figure is sourced with a document and date; no fabricated numbers. Where data is
absent, write "not disclosed" or "cons n/a" — never a guess. Actuals reconcile to the
statutory filing. Consensus is never used for actuals, and actuals-basis numbers are never
blended with consensus in the same series.

## THE CORE LOGIC — read this before anything else in this file

**1. There is one Drivers tab. No Operating Model tab, no Regional Model tab.** Both fold into
Drivers. Two sheets both holding revenue produces references running in both directions and no
sheet that owns the forecast.

**2. Drivers is laid out in this order, top to bottom:**

```
SECTION 1 — PRIMARY SEGMENTATION   (whatever the company itself talks to)
  Revenue, per segment              Q1 · Q2 · Q3 · Q4 · FY   every year, historic and forecast
  Total revenue                     = sum of segments
    LFL / organic growth %, per segment
    FX impact %, per segment
    Scope / M&A impact %, per segment
  Operating profit, per segment
  Total operating profit            = sum of segments
    Margin %, per segment
    Margin change, bps, per segment

SECTION 2 — SECONDARY SEGMENTATION (region, or country, whatever else is disclosed)
  Same shape: revenue by unit, then LFL / FX / scope where disclosed
```

The primary segmentation is whichever the company gives most disclosure on, because that is what
they are asking the market to forecast on. A company reporting business lines and also giving a
regional split has business lines first, region second.

**3. Q1 + Q2 + Q3 + Q4 = FY, in the history and in the forecast.** Every quarter column exists,
every year, and foots to its FY column. Historic quarters foot as a check on the retrieval;
forecast quarters foot because that is how the annual number is built. A quarter column present
for some years and not others is a defect.

**4. Drivers drives the Financial Model. The arrow points one way.** Group revenue and group
operating profit on the Financial Model are references to the Drivers totals — not typed, not
forecast there, never read back from the P&L. Where the company discloses D&A, EBITDA or margins
at segment level, those flow the same way. Read the company's disclosure to establish which lines
Drivers can own; build those and no others.

**5. Two sheets must not exist, in any tier, under any circumstances: Governance and Notes.**
Governance rarely changes a forecast and a thin governance tab is worse than none. Notes is
redundant now that Summary is the first tab — everything that would have gone on a Notes sheet
(the Read, data gaps, open questions, what could not be sourced, the attention groups) goes on
Summary. If either sheet appears in the output, delete it before handing back. Do not build them
"for completeness", do not build them because the analyst did not say not to, and do not build a
Notes sheet under another name.

**If any of the five is not true of the workbook you built, the build has failed**, however
complete the other sheets are.

## SCOPE OF CHANGE — improving an existing model changes only what was asked

Where the analyst asks for one thing to be improved, improve that and leave every other sheet as
it is. Do not restructure a sheet nobody mentioned, do not drop a section that already worked,
and do not reduce a sheet's period coverage while rebuilding it. A run that fixes the balance
sheet and silently deletes the segment profit block has cost the analyst more than it gave them.

Before finishing, compare against the version you started from: any sheet, section or period
column that existed before and does not now must be either explicitly requested or reported as
removed, with the reason.

## STEP 0 — SAMAYA CONNECTIVITY GATE (hard requirement, before anything else)

Read `references/samaya-conventions.md` first — it carries the full rule for this and for every
shared section below. Then: confirm `financial_qa` and `financial_qa_result` are in the tool list
(match the tool name, not the client's prefix; if absent, stop and ask the analyst to connect
Samaya); fire one trivial test query and get a real answer before building; on failure retry the
same session, then a fresh one, then report and pause — never a silent fallback to web search or
any other source; any non-Samaya source needs the analyst's explicit approval, per source, and is
labelled with its true retrieval path.

## RETRIEVAL

Samaya is the source for filings, releases, presentations and transcripts. Retrieve across all
of them rather than the release alone — the growth decomposition, the phasing and the
qualifiers are spread across the press release, the filing, the results presentation, the annual
report and the call transcript, rarely all in one.

Two hierarchies, never conflated: **reported actuals** come from the company's own documents;
**forward estimates** come from the declared consensus provider. Never mix an estimate into an
actuals series or an actual into an estimate column.

Where a document cannot be retrieved: retry same session, then fresh session, then a different
source class for the same figure naming which carried it, then ask the analyst. Leave the cell
blank and list it rather than estimating a reported actual.

## METRIC DEFINITION — pull the one the market tracks (all line items, not just profit)

Full section: `references/house-conventions.md` — read it at kickoff.

## INTERIM DERIVATION — when only half-year consensus exists

If pulling quarterly consensus but the feed only carries half-year (1H/2H) estimates, do not
leave the quarter blank: pull the half-year and derive the quarter from the reported stub, or
ask. **2Q = 1H consensus − 1Q actual** (when 1Q is reported); **4Q = 2H consensus − 3Q
actual**. State the derivation in the cell Note. If the derivation inputs are not both
available, leave blank and flag — never approximate.

Full section: `references/house-conventions.md` — read it at kickoff.

## SAMAYA PROVENANCE LINKS (every Samaya-sourced cell)

Full section: `references/mechanical-integrity.md` — read it before writing the first formula.

## OPENING ELICITATION — three questions block, the rest are inferred

Full section: `references/house-conventions.md` — read it at kickoff.

## HOUSE-MODEL CONVENTIONS OBSERVED IN THE FIELD

These are not preferences. Each is taken from institutional house models in production, and a
build that ignores them produces a workbook that looks right and cannot be maintained or
published.

Full section: `references/house-conventions.md` — read it at kickoff.

## THE PUBLICATION LAYER — where the house has one

House models feeding a downstream platform or consensus contribution carry a mapping sheet
(often `Digital Template`). It is a machine-readable contract: CONTROL / HEAD / HIDDEN / BODY
row grammar; company GUID, template GUID and `template_version`; a descriptive header; one row
per published line carrying its item GUID and the sector template's **standardised** item name
(Sales, EBITDA, EBIT, PBT, Tax Rate, Net Income, Average Number of Shares (FD), EPS (FD)); and
its own ACTUAL/ESTIMATE split and year cascade off one anchor.

Full section: `references/model-architecture.md` — read it before building the first sheet.

## MODEL ARCHITECTURE — build sheets in order

Full section: `references/model-architecture.md` — read it before building the first sheet.

## THE DRIVERS SHEET — detail on top of the core logic

Layout and the four rules are in THE CORE LOGIC above. This is only the detail.

Full section: `references/model-architecture.md` — read it before building the first sheet.

## THE READ — a written answer on the sheet

A model handed over with no words is a model the recipient has to reverse-engineer. Write a
**Read** onto the Summary tab, and a short version into the Financial Model header
block: merged across the table width, wrapped, prose.

Four or five sentences: what the company does and how the model is structured; the primary
profit metric chosen and why, since every margin in the workbook depends on it; where the
forecast sits against guidance and against consensus where a provider was declared, at the two
or three lines that matter; the assumptions carrying the most valuation weight; and what could
not be sourced.

Then the three attention groups, per the classification below — reported and settled, estimates
to review, mechanics to check — each line a live internal hyperlink to the cell it names.

Written last, from the populated model only. No cell references in the prose. It describes the
build; it states no rating, target or recommendation.

**Never render an empty value.** No nulls, no unresolved placeholders, no orphaned label with
nothing behind it. A line with no content is omitted and named once on the Summary tab, never
left blank or zeroed — a zero in a model is a number, and a blank that should hold one is a
defect.

## STATEMENT COMPLETENESS — the lines a real model carries

A cash flow of net profit, capex and working capital is not a cash flow statement. Build the full
articulation, and where a line is genuinely nil or undisclosed show it as nil rather than
omitting it — an absent line reads as an oversight.

Full section: `references/model-architecture.md` — read it before building the first sheet.

## MECHANICAL INTEGRITY — the failures that make a model quietly wrong

Checked as the relevant sheet is built, not at the end.

Full section: `references/mechanical-integrity.md` — read it before writing the first formula.

## NOTE STANDARDS

Source attributions are Excel **Notes** — the classic hover note with the red-corner triangle
(in the file format, note / legacyComment objects), **never threaded comments**. Apply to
every annotation below.
- **Source:** `[line item], [source name], [FY/date], p.[X]/note[X], via Samaya, as-of [date].
  [Samaya link]`
- **Assumption (estimate years):** `[line] estimate: [value]. Basis: [guidance/consensus/
  analyst]. Drivers: [x, y]. Upside/downside: [z].`
- **Analytical note:** where a line behaves non-obviously (e.g. "restructuring recurs every
  year since FY16 averaging €Xm — the 'non-recurring' label is misleading for the cost base").
- **D&A methodology** (once on the Financial Model): where depreciation sits (COGS vs opex vs
  ROU), what the DCF uses, and the no-double-count rule.

Full section: `references/mechanical-integrity.md` — read it before writing the first formula.

## A WORKED EXAMPLE — the estimate rationale Note

The Notes are the product wherever a number is a judgement, so one worked pair, because the
difference between these is the difference between a model someone can defend and one they
cannot.

Full section: `references/mechanical-integrity.md` — read it before writing the first formula.

## CONSENSUS — provider-agnostic, declared once, never assumed

Ask once at kickoff, in the same message as everything else: `Consensus source? Visible Alpha /
Bloomberg / FactSet / company-compiled / a file you supply / none`. Never default to a provider;
where the analyst states no preference, use what the session can reach and say which. Record the
provider and its as-of date on every consensus figure. One provider per comparison, never blended; match the definition before
calling a gap a gap; never infer a segment estimate from a headline one or present one broker's
estimate as consensus. No consensus is a legitimate answer: the run completes with those cells
blank and the attempt recorded. Full rule: `references/samaya-conventions.md` § CONSENSUS.

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
is the only fill besides the headline-row shading, so it needs no legend; if more than a tenth of the touched lines want it, say so
in the Read instead of colouring the block. Full rule: `references/samaya-conventions.md`
§ ATTENTION CLASSIFICATION.

## WORKBOOK FORMAT — applied when there is no template to match

Match a supplied house template; otherwise apply `references/workbook-format.md` in full. The
non-negotiables: no numeric cell left on `General` — `#,##0;(#,##0);"—"` for units,
`0.0%;(0.0%);"—"` for margins, `0.0"x"` for multiples, negatives in parentheses, zeros as an em
dash; Inter at 9 or 10 point; row height never above ~30pt except a single title row; gridlines
off, zoom 80%, freeze panes, units and currency in the sheet header; numbers right, labels left. The assumptions block sits
directly beneath the income statement, with gross margin, A&P and distribution expressed as
**bps movements**, not absolute levels.

## DESK AND AUTHORSHIP

Sell-side, buy-side and sales and trading get the same content; only emphasis and order change —
establish the desk from context, ask once at kickoff only if genuinely unclear, otherwise build
in the neutral order and say so in the header. Authorship is Samaya AI, never the operator:
`Samaya AI` on every Note and on the document properties, inherited creator values cleared, a
third party's authorship left on their content. Styling tokens live in `samaya-brand`, which is
authoritative. Full rules: `references/samaya-conventions.md` § DESK and § AUTHORSHIP AND HOUSE
STYLE.

## VALIDATION GATES — before delivery

Plus the common gates in `references/samaya-conventions.md` and the workbook gates in
`references/workbook-format.md`.

**The five core-logic rules first.** One Drivers tab, no Operating or Regional. Drivers laid out
segment revenue → LFL/FX/scope → segment operating profit → margin → bps, then the secondary
segmentation. Q1+Q2+Q3+Q4 = FY in history and forecast, every year. Group revenue and group
operating profit on the Financial Model are references to the Drivers totals. No Governance
sheet and no Notes sheet, under any name.

Then:

- Three questions asked, not nine; every inferred parameter stated on the sheet it governs.
- Statements tie every year: assets = liabilities + equity, cash flow closing cash = balance
  sheet cash, net debt bridge reconciles, retained earnings movement explained. Any plug named,
  sized and flagged.
- Cross-footing passes: segments to group, interims to the year, the organic bridge to reported
  growth. Circularity broken explicitly with the method in a Note; iterative calculation not
  enabled to mask a loop.
- Every schedule runs to the end of the horizon — bridges, balance sheet, per-share. No forecast
  line equal to the prior year.
- Forward revenue is a formula off the LFL, FX and scope inputs; forward margin is prior margin
  ± a visible bps input. No typed forecast revenue or margin level.
- Periods strictly chronological on one declared ladder; sub-annual columns grouped so the sheet
  collapses to annual.
- The DCF completes: WACC from retrieved inputs, terminal value, full EV-to-equity bridge, price
  objective, dated upside, implied multiples. Nothing shipped marked incomplete.
- Macro carries 10–20 named pairs with annual and quarterly history and a stated forecast basis;
  every Drivers FX row references a pair by row code.
- Scope carries a populated deal table; known deals with undisclosed terms appear as labelled
  empty rows.
- Summary is the first tab, carrying the Read, the three attention groups with internal links,
  and a notes area.
- No numeric cell on General; Inter 9–10pt; no manual row height above ~30pt; gridlines off,
  zoom 80%, freeze panes, units and currency in each sheet header.
- Every retrieved figure carries its Samaya link at point of use. Sign convention declared in a
  Note and held on every sheet.
- Where improving an existing model: nothing removed that was not requested.

## FORMATTING (last step, after all numbers populated and validation passed)

**Readability rules for every sheet**, because a correct model nobody can scan gets abandoned:

- **A border under every subtotal** — net revenue, gross profit, EBITDA, EBIT, PBT, net income
  and every cash flow subtotal — so the eye finds the structure without reading labels.
- **Headline rows shaded across the full row.** The lines a reader looks for first — net revenue,
  operating profit / EBIT, net income, EPS, and each statement's closing line — carry a light
  full-row fill with the label bold. This is the only shading besides the attention fill.
- **Bold on subtotals only.** Bold everywhere is bold nowhere.
- **A blank row between logical blocks** — revenue build, cost lines, profit measures, per-share
  data — rather than a continuous wall of rows.
- **The assumptions block sits directly beneath the income statement it drives**, as its own
  short labelled section, not at the far right or on another sheet.
- **Assumptions expressed as changes where a change is what is being judged:** gross margin, A&P
  and distribution as **basis-point movements** year on year, not absolute margin levels.
  Effective tax rate and dividend payout stay as rates, being levels by nature.

Ask which format: (1) firm format from an uploaded house template/model, read and applied
exactly; (2) personal hybrid — firm style structural, personal conventions at cell level;
(3) Samaya standard — tokens per the `samaya-brand` skill and its styleguide, which is
authoritative; actuals black, estimates in the input colour; gridlines off; negatives in
parens; zeros "—"; section-header and year-header borders only; 80% zoom; freeze label column
and header rows; authorship per DESK AND AUTHORSHIP. Never roundtrip a live/charted/UDF workbook through
openpyxl — in-app or zip/XML edits only.
