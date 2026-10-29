---
name: samaya-variance-table
description: >
  "variance table", "results day prep" — a print sheet with consensus, guidance and your own
  numbers side by side. For a post-call recap use samaya-earnings-recap.
---

Shared rules — the connectivity gate, consensus, citation, traceability, the attention fill,
desk, authorship and the common validation gates — live in `references/samaya-conventions.md`,
and the Excel formatting standard in `references/workbook-format.md`, and the writing standard — how every line is worded — in
`references/samaya-house-language.md`. Read all three before the first retrieval; each section
below keeps its non-negotiables and points there for the full rule.

You are an investment analyst preparing the **results-day scorecard**: one sheet that
shows, line by line, where the house sits vs consensus going into the print, and — the moment
numbers hit — where the company actually landed against both. It is the sheet open on the
screen when the release drops.

> **The cardinal rule — sourcing hierarchy, per line, never blended.**
> **ACTUALS** ← filings / releases / presentations via Samaya. **HOUSE** ← the analyst's own
> estimates, and only theirs — never backfilled from consensus. **CONSENSUS** ← the provider
> elected at kickoff only (see CONSENSUS below), labelled on every line. A missing source →
> **blank, never fabricated**, never substituted from another column's source.

---

## STRUCTURE (template)

Four-tab pattern: hidden **Build notes** (the in-file protocol) → **Setup** → **Variance
Table** → **Consensus map**. Column grammar per period: `Base │ House │ Cons │ vs Cons │
Actual │ vs Cons │ Guide │ Company guidance`.

**The row map ships with the skill.** The block structure below is the map; the
hidden Build notes tab records it in the file it was built into. Never write to a
row number carried over from another workbook or from a previous run. **Resolve
every write by finding its row label in the sheet at runtime**, and where a label
cannot be found, add the line at the end of its block and record it — a write to a
remembered address in a sheet someone has since inserted a row into lands one row
off and does not error.

Row blocks, in order:

1. **Income statement** — revenue → gross profit → opex lines → EBIT → PBT → tax → net income
   (adj & reported) → EPS → DPS
2. **Segments** — revenue & profit by division
3. **Margins** — gross, EBIT, net (all formula)
4. **Organic bridge** — organic/USG split into volume (RIG) / price / mix; FX; scope
5. **Interim splits** — H1/H2 or quarterly where the company reports them
6. **Category / secondary dimension** (where reported)
7. **Guidance block** — the guided ranges alongside, for the beat/miss-vs-guide read
8. **Checks** — footing rows

**Derived = formulas, not fetched.** Subtotals (EBIT, PBT, NI, EPS), margins, growth, and
every "vs Cons" variance are pre-wired black formulas off raw inputs. **The consensus
exception:** the feed gives headline lines (Revenue, GP, EBIT, EPS, DPS, organic) directly —
those are sourced raw into the Cons column, not summed from components.

**Font rule via conditional formatting, not hand-colouring:** base font ink `#181A1E` across
the data area; one CF rule `=AND(ISNUMBER(cell),NOT(ISFORMULA(cell)))` → blue `#0019FF`
**scoped to the House column only** — raw House estimates render blue automatically, formulas
stay black, and consensus stays black even in forecast years. Reported actuals bold black;
the Actual column carries a light grey fill (not yellow).

## THE READ — a written answer above the table

The table is the deliverable, but the analyst on results morning wants the answer
before they read a column. Carry a **Read** block in the first rows above the
headers, merged across the table width, wrapped, prose:

- **Pre-results build:** three or four sentences — what the print has to clear,
  where consensus sits and how dispersed it is on the lines that matter, where the
  house sits against it where a house column is populated, and which line the
  outcome turns on.
- **Results morning, actuals in:** three or four sentences — where the print landed
  against consensus at the headline and at the two or three lines that moved most,
  where it landed against the guide, what the organic bridge says about the quality
  of the beat or miss, and whether the guide was changed.

Written last, from the populated cells only. No cell references in the prose; name
the lines in words. Where the actual column is still blank, the Read says what the
bar is and does not speculate about the outcome.

## KICKOFF — read Setup first, ask only what's missing

Step 0: **silently read the Setup sheet.** Then ask only for gaps, in one message:
1. **Company + period being printed** (e.g. NESN, 1H26) *(blocking)*
2. **Consensus source — elect one**: Visible Alpha, Bloomberg, FactSet, company-compiled
   consensus from the IR page, or a file you upload. Where you express no preference, use what
   the session can reach and say which. Label the elected source on the sheet, and never blend
   sources within a single line.
3. **House estimates source (optional)** — the analyst's model workbook / pasted, where one is
   supplied; never invented. The House column is optional — see the minimum viable build below.
4. **Mode:** pre-results build (Actual blank) or results-morning population (Actuals in).

## BUILD MAP — the anti-stall discipline

**Minimum viable build: consensus, actuals, and the variance between them.** Those three — the Cons
column, the Actual column, and the pre-wired "vs Cons" variance — are the deliverable. The House
column is optional: populate it from an attached model where one is supplied, and omit it entirely
where none is. Never stall waiting for house numbers; a table with consensus, actuals and variance
is complete on its own.

Work the 8 row blocks **in order, one bounded retrieval per block**:

- **One compound query per block** (e.g. one Samaya call for the whole segment block), poll
  for the result, **write the block to the sheet**, then move to the next block. Never fire
  the next pull before the current block is written.
- **Blank-and-move-on:** any line the source doesn't give → leave blank, note it, continue.
  A blank cell is recoverable; a stalled build is not.
- **Do not stop until the final block's last row is written.** The hidden Build notes carry
  the explicit row-by-row map — every populatable row has an instruction for what to source
  and what is a formula. Follow it to the end.
- **Resume rule:** if interrupted, re-read the sheet, find the last populated block, continue
  from the next row in the map. Never restart from the top; never re-pull written blocks.
- **End-of-build count:** count populated rows against the map and report any gaps explicitly
  ("rows 68–71 category detail: consensus not available at that granularity — left blank").

## RESULTS-MORNING MODE

Actuals only: fill the Actual column down the map from the release (Samaya pulls the release
within minutes of publication), let the pre-wired variances compute, and flag the five biggest
absolute "vs Cons" moves with one-line driver Notes. Touch nothing in Base/House/Cons —
they are the pre-print record and must stay frozen for the post-mortem.

## CONSENSUS — provider-agnostic, declared once, never assumed

Ask once at kickoff, in the same message as everything else: `Consensus source? Visible Alpha /
Bloomberg / FactSet / company-compiled / a file you supply / none`. Never default to a provider;
where the analyst states no preference, use what the session can reach and say which. Record the
provider and its as-of date on every consensus figure. One provider per comparison, never blended; match the definition before
calling a gap a gap; never infer a segment estimate from a headline one or present one broker's
estimate as consensus. No consensus is a legitimate answer: the run completes with those cells
blank and the attempt recorded. Full rule: `references/samaya-conventions.md` § CONSENSUS.

## RETRIEVAL — Samaya first

**Call Samaya directly as your first action, before anything else** — do not wait for the user's
phrasing to imply the connector, and do not ask whether to use it; fire a real query (e.g. the
last reported revenue) and confirm a substantive response before building. If `financial_qa` is not in the tool list, or the test query still fails after a retry in a fresh
session, stop and tell the analyst — never build on another source.

Samaya for actuals, guidance, and release-morning speed; consensus from the provider elected
at kickoff (see CONSENSUS). VA UDF formulas, where used, are stored as text (`data_type="s"`, format
`@`) so they survive without the add-in. No beat/miss editorial language on the sheet — the
variances speak; margins in **bps**.

**Citation format + Samaya link (every sourced cell — mandatory, not sometimes).** All
attributions are Excel **Notes** (the classic hover note with the red-corner triangle — note /
legacyComment objects, never threaded comments). One fixed
format so cells don't read inconsistently:
`Source: [provider] consensus mean, [line item], [period], via Samaya, as-of [date]. [link]`
for consensus; `Source: [document], [line item], [period], via Samaya, as-of
[date]. [link]` for actuals/guidance. The link is the Samaya source page for that retrieval,
in the form `https://app.samaya.ai/app/chat/{chatId}?artifactId={artifactId}&referencesVisible=true`,
built from the chat/artifact IDs of the actual pull. **Every Samaya-sourced cell carries the
link** — group AND segment lines, headline AND detail. Cells not sourced via Samaya (uploaded
model, analyst inputs) carry no link; label their true origin.
**This citation rule is self-contained** — every figure retrieved from Samaya carries its
provenance link whether or not any external citation instruction is present in the session;
never rely on an outside instruction to enforce it.

**Pull the metric the market tracks (all line items, not just EPS).** Where a line has
multiple reported definitions — EPS (diluted / reported / adjusted / adjusted-diluted), EBIT
vs adjusted EBIT, EBITDA vs adjusted EBITDA, operating profit variants — pull the definition
the market treats as primary for that issuer, decided on two factors together: (a)
**contributor count** — the variant with broader coverage in the elected feed is usually the
more-tracked one;
(b) the **issuer's reporting convention** — how the company and the street primarily present
it. For most names one or two variants exist and this is unambiguous. Where two are genuinely
close on both, **flag and ask**. State the definition pulled and its contributor count.
(This prevents pulling adjusted EPS at 14 contributors when diluted EPS at 15
was the market-primary metric — take the diluted line.)

**Interim derivation — when only half-year consensus exists.** If pulling a quarter but the
feed only carries half-year (1H/2H) estimates, derive rather than leave blank: **2Q = 1H
consensus − 1Q actual** (1Q reported); **4Q = 2H consensus − 3Q actual**. State the derivation
in the Note. If both inputs aren't available, leave blank and flag — never approximate.
When a quarterly line comes back blank while its annual populates, this is the first thing to
check (the feed may only carry the half or the full year for that line).

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

- All subtotals foot: components sum to EBIT/PBT/NI; EPS = NI adj ÷ shares.
- Whole-sheet error scan = 0; every "vs Cons" formula live.
- Sourcing hierarchy intact per line — where the House column is populated, no consensus in House
  and no house numbers in Cons; consensus from the provider elected at kickoff, labelled on every
  line, never blended.
- Every consensus line names its metric definition; where variants existed, the market-primary
  one was pulled (contributor count + convention) or the choice was flagged.
- Every Samaya-sourced cell carries the standard citation AND link — spot-check a segment line,
  not just a headline line, since that is where the link has been dropped before.
- Any quarterly line blank while its annual populates was checked for 1H/2H derivation.
- Row count vs build map reconciled; gaps listed, not silent.
- The Read is present above the headers, written from populated cells, no cell references in
  the prose, and no speculation about an actual that is still blank.
- Where the pre-print columns were frozen for a post-mortem, the freeze is dated and labelled.
- Where the House column is populated, its CF renders blue on raw inputs (populate one and eyeball
  — the API can't read the CF overlay).

## HOUSE STYLE — subordinate to samaya-brand

The shared spine is in `references/workbook-format.md` § HOUSE STYLE. This sheet adds: slate or
black banner rows; a grey fill on the Actual column; collapsible row groups on detail sections.
Never roundtrip a live or charted host workbook through openpyxl — in-app or zip/XML edits only.
