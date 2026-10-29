# The FY roll, interim derivation, sheet boundaries, reference integrity, corporate actions, FX and unretrievable documents

Moved out of `SKILL.md` to keep it lean; read it before the first edit.

## Contents

- THE FY ROLL
- DERIVING THE UNREPORTED INTERIM
- WHICH SHEETS
- REFERENCE INTEGRITY
- CORPORATE ACTIONS
- FX AND MACRO
- WHEN THE DOCUMENT CANNOT BE RETRIEVED

## THE FY ROLL — appending the horizon

A full-year roll does everything an interim roll does, then extends the horizon.
Three rules, each of which produces a workbook that recalculates cleanly and
reports wrong numbers if broken.

**1. A period block, not a column.** The horizon extends by a whole year's block,
and the block width differs by sheet — eight columns on the operating engine
(Q1 │ Q2 │ H1 │ Q3 │ 9M │ Q4 │ H2 │ FY), three on the annual roll-up (FY │ H1 │ H2),
and whatever the macro sheet carries. Establish each sheet's block width from the
existing years before adding anything, and append the same shape.

**2. Extend by the date, not by the header.** In a well-built model the period
headers are formulas off the year's date cell — `="Q1 "&TEXT(<FY date>,"yy")`,
`="Jan-Sep "&TEXT(<FY date>,"yy")` — and the status label is a formula off the same
date. Set the new block's date cell and every header and label builds itself.
Typing a header, or typing "Actual" or "Estimate" into a status cell, replaces a
formula with a literal that will be wrong at the next roll. Let the cascade run.

**3. Widen every aggregate range, or the new year silently disappears.** Models
carry summary columns to the right of the horizon — averages, CAGRs, through-cycle
statistics — built as range formulas across every period column, often anchored on
a named range: `=AVERAGEIFS($E10:$HG10,<year-end name>,">…")`. Appending a block
beyond the range's right edge leaves those formulas reading the old span, so the
new year is excluded from every average in the model. Nothing errors. Nothing looks
wrong.

After appending, enumerate every formula whose range ends at the previous last
column, widen each one, and check one average against a hand calculation including
the new year. Also expect the Actual/Estimate marker columns to sit outside the
horizon and to shift right with the block — move them, don't leave them stranded
mid-grid.

**4. FY-only refreshes.** Some sheets are sourced from the annual report and the
proxy, and they move once a year and only at the FY roll — the ownership register
and free float, the remuneration structure including the metric weightings in the
bonus and the long-term plan, board and supervisory composition, and any
accounting-policy or auditor note the model tracks. These are easy to skip because
no interim touches them, and they can grow substantially in a single roll. Check
them explicitly at every FY roll and record them as checked, or as none.

## DERIVING THE UNREPORTED INTERIM

Companies do not report every column the model carries. A half-year reporter
publishes H1 and FY; the model still holds Q1, Q2, Q3, Q4. The unreported interim
is **derived by subtraction from the cumulative periods, as a live formula**, never
typed as a number and never left blank:

- `Q2 = H1 − Q1` · `Q3 = 9M − H1` · `Q4 = FY − 9M` · `H2 = FY − H1`

Write the subtraction as a formula referencing the two period columns, so the
derived column stays true when either input is revised. A derived interim entered
as a hardcode breaks silently at the next restatement, and it is the commonest
cause of a quarterly row that no longer foots to its year.

Where the company reports the interim directly, enter it as an actual and let the
identity row check it rather than deriving it. Where neither route is available —
no cumulative figure and no direct disclosure — leave the cell blank and name it in
the summary. Never plug it.

Every derived interim carries a Note saying which two periods it was derived from.

## WHICH SHEETS YOU WRITE TO, AND WHICH YOU NEVER TOUCH

Classify every sheet before writing:

- **Input sheets** — the operating engine, the financial roll-up, the macro and FX
  block, the segment detail. These take the actuals and the re-forecast.
- **Downstream sheets** — summary pages, ratio and margin sheets, organic-growth
  and EBIT-bridge sheets, chart feeds. These are pure formula and they flow from
  the input sheets. **Write nothing here.** In a correctly built model a clean roll
  leaves them with zero direct edits; a delta on a downstream sheet means either a
  formula was overwritten or the sheet is not as pure as assumed. Either way, stop
  and establish which before continuing.
- **Valuation sheets** — the DCF and any multiple-based bridge. Touched narrowly
  and deliberately: the base year, the terminal value, the share count and
  minorities, the price and its as-of date, the consensus anchor, and the
  "updated on" stamp. Not re-forecast wholesale.

State the classification in the roll plan. Where a sheet cannot be classified with
confidence, treat it as downstream and leave it alone.

## REFERENCE INTEGRITY UNDER ROW INSERTION

Cross-sheet references are the fragile part of any real model, and they break
without erroring. Before inserting or deleting any row:

1. **Prefer not to.** Ask whether the new line can go in an existing spare row
   inside the relevant block. Most house models carry them.
2. **Anchor on names, not addresses.** Where the model uses named ranges or a
   machine row-code column, add the new line's code and reference it by name. A
   reference resolved by name survives insertion; `A192` does not.
3. **Where insertion is unavoidable**, enumerate every reference into the affected
   sheet below the insertion point before you insert, re-point each one after, and
   list them in the change log. A single row inserted into a statement sheet
   routinely shifts dozens of references on the valuation and summary sheets.
4. **Then check the identities**, not just the recalc. Reference drift produces a
   workbook with zero formula errors and wrong numbers.

## CORPORATE ACTIONS IN THE PERIOD

A roll is not only actuals and re-forecast. Check each of these against the period's
release, call and any interim announcements, and state explicitly where the answer
is none:

- **Acquisitions and disposals** — consideration, close date, and the scope
  contribution split out from organic in the growth bridge. A disposal removes
  forward revenue and profit that the pre-existing forecast still carries.
- **Joint ventures and associates** — equity income line, and whether the stake
  was consolidated, deconsolidated or re-based. Deconsolidation moves revenue out
  of the top line entirely and is the change most often missed.
- **Buybacks** — amount executed in the period against the amount authorised, and
  the effect on the diluted share count used for EPS. Authorised is not executed.
- **Dividends** — declared per share, payment timing, and the cash-flow and
  net-debt effect.
- **Refinancing and new issuance** — the finance-cost line and the debt maturity
  profile.
- **Share count** — actual weighted average for the period, and the basis for the
  forecast periods.

Each one that occurred is entered, logged in the change tracker with its driver, and
reflected in the forecast periods it touches — not just the reported one.

## FX AND MACRO

Where the model carries an FX block or a macro sheet, it is an input sheet and it
rolls with the period:

- **Realised rates** for the reported period, replacing the estimate.
- **Forecast rates** for the remaining periods on the analyst's stated basis —
  spot held flat, forwards, or their own deck. Ask which; do not pick one.
- **Translation against transaction.** A translation effect flows through the
  revenue bridge's FX line; a transaction effect sits in cost of goods and margin.
  Do not conflate them.
- **Macro drivers** — the rates, inflation and volume assumptions the operating
  model reads — updated where the period moved them, and left alone where it did
  not.

FX is a common source of a roll that ties at the top line and misses at EBIT.

## WHEN THE DOCUMENT CANNOT BE RETRIEVED

A roll that stops because one line could not be sourced is useless; a roll that
plugs the gap silently is worse. The order of resort, and it is stated in the
summary each time it is used:

1. **Retry** on the ladder: same session, then a fresh session.
2. **A different source class for the same figure** — the release, then the
   presentation, then the transcript, then the filing. Name which one carried it.
3. **Ask the analyst** for the figure or the document, naming exactly what is
   missing and which cells wait on it.
4. **Leave the cell blank**, carry the blank through the identity checks so it is
   visible rather than absorbed, and list it in the summary under what could not be
   sourced.

Never estimate a reported actual. An actual that was inferred rather than read is
indistinguishable from a real one once it is in the cell, and everything downstream
inherits it.
