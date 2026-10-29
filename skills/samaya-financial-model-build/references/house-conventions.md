# Opening elicitation, house-model conventions, metric definition and interim derivation

Moved out of `SKILL.md` to keep it lean; read it at kickoff.

## Contents

- OPENING ELICITATION
- HOUSE-MODEL CONVENTIONS
- METRIC DEFINITION
- INTERIM DERIVATION

## OPENING ELICITATION — three questions block, the rest are inferred

**Only three items block the build.** Nine blocking questions before any work is the single
biggest reason a build never starts, and seven of them are answerable from the filings the skill
is about to read anyway.

**Ask these three, together, in one message:**

- **Company** — name or ticker. Resolve the exchange, reporting currency and fiscal year-end
  from Samaya rather than asking.
- **Most recent completed FY** — anchors the Actual columns; everything to its right is E.
- **Complexity tier** — Basic / **Standard (default)** / Advanced, as defined below.

**Infer the rest and confirm inline as each sheet is built**, stating the inference in one line
at the top of the sheet it governs so the analyst can correct it before it propagates:

- Forward years — default 4, stated on the Financial Model sheet.
- Historical years — default 10, stated on the Financial Model sheet. Where archived filings
  are needed beyond what Samaya reaches, say which years are thin rather than asking up front.
- Interim reporting — read what the company actually reports (half-yearly or quarterly) from
  the filings and follow it. Do not ask an analyst what a company's reporting calendar is.
- Material listed stakes — read the associates and subsidiaries note and list what is there,
  with ownership percentages, then confirm the list on the sheet.
- Company-collected consensus template — check whether one exists before asking. Where one does,
  say so and ask only whether to use it.
- Primary documents — find them. Ask only where retrieval fails, naming the document missing.

**One exception.** Where the analyst has supplied a house template or an existing workbook to
build into, ask before the first write whether to build into it or into a new file, and if into
it, save a timestamped copy first. That is the only question that must not be inferred, because
inferring it wrongly destroys someone's work.

## HOUSE-MODEL CONVENTIONS OBSERVED IN THE FIELD

These are not preferences. Each is taken from institutional house models in production, and a
build that ignores them produces a workbook that looks right and cannot be maintained or
published.

**A machine row-code column, and it is load-bearing.** House models carry a dedicated column
(commonly immediately left of the labels) holding either a relative row position computed off a
single anchor — of the form `=ROW(<this row>)-ROW($A$<anchor>)+1` — or a short semantic code for
any line referenced from outside the sheet, on the pattern `BS_<line>` for a balance-sheet item
or `RES_<line>` for a restated series. Build it
on every statement sheet from the start. It is the reason cross-sheet references and any
publication mapping survive an inserted row, and adding a missing code later is fiddly
maintenance work that should never have been needed. Where a line will be referenced from
another sheet, from a DCF, or from a publication layer, it gets a semantic code, not a number.

**A status row, per column, in text.** One row under the period headers reading `Actual` or
`Estimate` for every column. The Actual/Estimate boundary is then a fact on the sheet rather
than a formatting convention someone has to infer from font colour.

**Period headers are dates, not labels.** The header row holds real period-end dates
(`2022-06-30`), formatted for display, with the year cascade built as formulas off a single
anchor cell (`=F22-1`). Extending the horizon means changing one date; typing a header is a
defect, because it breaks at the next roll.

**A summary block at the top, pulling from the detail below.** The first rows of the statement
sheet carry the headline series — EPS, growth, the primary metric — as simple references down to
the detail rows (`=F84`), so the reader sees the shape of the model before scrolling. Never
duplicate the calculation up there; reference it.

**Depth of history is a house decision and it can be very long.** Production models routinely
carry forty years of actuals. Where the analyst wants deep history, build it and flag which
years came from archived filings or third-party history rather than from documents Samaya
reached directly. Do not silently truncate to ten because that is the default.

**Add-in cache sheets are load-bearing and invisible.** Workbooks fed by a data add-in carry a
cache sheet — `__FDSCACHE__` and equivalents. **Never delete, rename, reorder or rebuild one**,
and never roundtrip a workbook containing one through a library that drops it: the add-in
formulas stop resolving and the model silently loses its feed. Its presence is also the signal
that in-app or zip/XML editing is the only safe route.

## METRIC DEFINITION — pull the one the market tracks (all line items, not just profit)
Where a line item has multiple reported definitions — EPS (diluted / reported / adjusted /
adjusted-diluted), EBIT vs adjusted EBIT, EBITDA vs adjusted EBITDA, operating profit
variants, and equivalents across the P&L, cash flow, and balance sheet — pull the definition
the market and covering analysts treat as **primary for that issuer**. Decide using two
factors together:
1. **Contributor count** — the variant with the broadest consensus coverage (most estimates
   on VA) is usually the more-tracked one.
2. **The issuer's own reporting convention** — how the company and the street primarily
   present the metric.
For most names this is unambiguous (one or two variants; contributor count or reporting
convention settles it). Where two variants are genuinely close on both coverage and
prominence, **flag and ask** rather than guessing. State which definition was pulled, and its
contributor count where relevant.

**Primary profit metric (mandatory before building any margin row):** identify the operating
profit metric the market uses to price the stock — the one with the highest consensus
coverage on VA (check estimate counts for EBITDA / EBITA / EBIT / operating profit /
underlying operating profit / adjusted operating income). Add a Note at the top of the operating
section: "Primary profit metric: [METRIC]. [N] consensus estimates on VA vs [N] for
[alternative]. All margin commentary, consensus comparisons, and valuation multiples use
this." Sector conventions as a guide, always verified: European staples/luxury → underlying/
core operating profit; acquisitive industrials → EBITA; leveraged/capital-intensive/telecom →
EBITDA; European software → adjusted EBIT (strips SBC); US GAAP → check whether consensus
tracks GAAP or non-GAAP EPS as primary.

## INTERIM DERIVATION — when only half-year consensus exists
If pulling quarterly consensus but the feed only carries half-year (1H/2H) estimates, do not
leave the quarter blank: pull the half-year and derive the quarter from the reported stub, or
ask. **2Q = 1H consensus − 1Q actual** (when 1Q is reported); **4Q = 2H consensus − 3Q
actual**. State the derivation in the cell Note. If the derivation inputs are not both
available, leave blank and flag — never approximate.
