# Mechanical integrity, Note standards, provenance links and the worked example

Moved out of `SKILL.md` to keep it lean; read it before writing the first formula.

## Contents

- MECHANICAL INTEGRITY
- NOTE STANDARDS
- SAMAYA PROVENANCE LINKS
- A WORKED EXAMPLE

## MECHANICAL INTEGRITY — the failures that make a model quietly wrong

Checked as the relevant sheet is built, not at the end.

**Circularity.** Interest on average net debt is the classic one: interest drives net income,
which drives cash flow, which drives net debt, which drives interest. Do not enable iterative
calculation to make it resolve — it hides the loop and produces a workbook whose answer depends
on calculation order. Break it explicitly, with the choice stated in a Note on the interest row:
compute interest on **opening** net debt (simplest, and defensible), or run a stated circuit
breaker the analyst can switch off. The same applies to any revolver sizing, cash sweep or
covenant-triggered pricing.

**The three statements must tie, and be tested.** Every year, not just the first:
- Assets = liabilities + equity.
- The cash flow statement's closing cash equals the balance sheet cash line.
- The net debt bridge reconciles opening to closing through cash flow, leases, FX and M&A.
- Retained earnings move by net income less dividends less buybacks, with any other movement
  named.
- Interest and tax paid in the cash flow reconcile to the P&L charge through the accrual
  movement.
A model that balances only because a plug line absorbs the difference does not balance. Where a
plug exists, name it, size it, and flag it — never label it "other".

**Cross-footing.** Segment revenue sums to group revenue; segment profit sums to group profit
before unallocated, with the unallocated line explicit; quarters sum to the half, halves to the
year; the organic / FX / scope bridge sums to reported growth within a stated tolerance.

**Sign convention, declared once and held.** Costs, capex and outflows negative or positive —
pick one, state it in a Note on the first cost row, and hold it in every sheet including the DCF.
Mixed conventions are the commonest source of a bridge that does not foot and of a DCF that
silently double-counts capex.

**Hardcodes are inputs, and inputs are visible.** Every hardcoded number is either a reported
actual (carrying its source Note and link) or an analyst assumption (in the input colour, per
`samaya-brand`). A hardcode sitting in a row of formulas with neither is a defect: flag it per
the attention classification below.

**No consensus inside an actuals series, ever**, and no estimate in an actual column. The
Actual/Estimate boundary is a single column on every sheet and it is the same column on all of
them.

**Rounding and units, stated per sheet.** Millions or thousands, and the reporting currency,
in the sheet header. A model mixing units across sheets fails cross-footing for reasons nobody
can find.

**Never roundtrip a live workbook through openpyxl** — it destroys charts, external links and
add-in formulas. Build a new file with a library that preserves what you need, or edit in-app or
at the zip/XML level. Where the analyst supplied a template with charts or UDFs, the in-app or
zip/XML route is the only one available.

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

## SAMAYA PROVENANCE LINKS (every Samaya-sourced cell)
Every cell sourced via Samaya carries a hyperlink back to its Samaya source page, so the
workbook's sourcing is traceable into the app and onward to the underlying document. Emit the
link using the chat/artifact IDs from the actual retrieval, in the standard form:
`https://app.samaya.ai/app/chat/{chatId}?artifactId={artifactId}&referencesVisible=true`.
Standard citation format for every sourced cell **Note** (the classic hover Note with the
red-corner triangle — an Excel Note, never a threaded comment):
`Source: [Visible Alpha (S&P Global) consensus mean | document name], [line item], [period],
via Samaya, as-of [date]. [link]`
Cells NOT sourced via Samaya — an uploaded third-party model, the analyst's own inputs — carry
no such link; label their true origin instead.
**This citation rule is self-contained** — every figure retrieved from Samaya carries its
provenance link whether or not any external citation instruction is present in the session;
never rely on an outside instruction to enforce it.

## A WORKED EXAMPLE — the estimate rationale Note

The Notes are the product wherever a number is a judgement, so one worked pair, because the
difference between these is the difference between a model someone can defend and one they
cannot.

**WRONG** — restates the number and sources nothing:

> Sales growth 4.5% in FY27E.

**WRONG** — sources the guidance but not the deviation:

> Company guided mid-single-digit organic growth.

**RIGHT** — states the estimate, the anchor, the deviation and its driver, with the source:

> FY27E organic +4.5%, against management's "mid single digit" guide given on the FY26 call
> (link). Set below the middle of that range because the H2 FY26 exit rate was +3.1% (link) and
> the pricing contribution rolls off as the FY25 increases annualise; volume is assumed flat
> rather than the +1% implied by the guide. Consensus +5.1% as of 12 Mar (link).

The test: could a research director read the Note alone and know what the estimate rests on, and
what would change it? Where the answer is no, the Note is not finished. Where an estimate rests
on nothing but judgement, the Note says exactly that — analyst judgement, no external anchor —
which is honest and is how a reviewer finds the lines to challenge.
