# Model architecture, the Drivers sheet, statement completeness and the publication layer

Moved out of `SKILL.md` to keep it lean; read it before building the first sheet.

## Contents

- MODEL ARCHITECTURE
- THE DRIVERS SHEET
- STATEMENT COMPLETENESS
- THE PUBLICATION LAYER

## MODEL ARCHITECTURE — build sheets in order

**Load one sheet's specification at a time.** The six specifications below are long, and
carrying the DCF spec while building the P&L competes for attention with the P&L. Read the
specification for the sheet you are building, build it, then read the next. Where the
specifications are available as separate reference files, load them per sheet rather than
reading all nine.

Build sheet by sheet, one bounded retrieval block at a time, writing each block before the
next pull (anti-stall discipline; if interrupted, resume from the last written block, never
restart). Label actual years `[FY]A`, forward years `[FY]E` — real fiscal years, never Y0/Y1.

1. **Financial Model** — the core P&L, cash flow, balance sheet (annual). Full line-by-line
   cascade: sales (decomposed into organic / FX / scope for estimate years) → COGS (with
   disclosed component breakdown and any D&A-within-COGS flagged to avoid double-count) →
   gross profit → A&P → R&D (note capitalised portion) → SG&A → **primary metric** (underlying/
   adjusted OP per company definition) → restructuring / acquired-intangible amortisation →
   reported EBIT → net finance costs (decomposed) → associates (equity-accounted profit vs
   dividend received; list stakes at market value) → PBT → tax (reported AND underlying ETR) →
   NCI → net income (reported and adjusted) → EPS (basic / diluted / adjusted diluted, with
   share count and dilution) → constant-currency EPS where FX is material → DPS. Cash flow:
   OCF (with working-capital components and the seasonal H1/H2 dynamic flagged), capex (gross/
   net, vs D&A), interest and tax paid (reconciled to P&L), acquisitions/disposals. Balance
   sheet: goodwill/intangibles (with impairment-test detail), PPE and IFRS 16 ROU assets
   (matched by lease liabilities), associates (book vs market value), net debt (with and
   without lease liabilities), pension deficit (with actuarial assumptions).
2. **Drivers** — the single sheet that drives the Financial Model. **Merges what were previously
   separate Operating Model and Regional Model sheets**, because they were never two things: a
   segmentation is a segmentation, whether it cuts by business line or by geography, and
   splitting them left categories on one sheet and regions on another with no obvious reason.
   One sheet, ordered as below; full specification in its own section.

3. **Scope (M&A)** — cumulative acquisitions/disposals tracker: EV, implied multiple, revenue
   and EBIT contribution, goodwill, margin dilution/accretion; each entry sourced.
4. **DCF** — explicit forecast plus terminal, and **it must complete to a price target.** A DCF
   delivered with blank discount-rate inputs and marked incomplete is not a deliverable: the
   price target is the reason the sheet exists.

   *Discount rate.* Risk-free from the 10-year government bond for the reporting currency; ERP
   from a stated published source, named and dated; beta on a stated basis (commonly 5-year
   monthly) against a named index; pre-tax cost of debt; tax rate from the model. Retrieve these
   — they are publicly available, and a named source with a date beats a blank cell. Where one
   genuinely cannot be retrieved, put a clearly-labelled placeholder with the source to obtain
   it, compute everything else, and flag it per the attention classification — never leave the
   chain broken so nothing downstream calculates.

   *Cash flow build.* Revenue and growth · adjusted EBIT and margin · D&A and % of sales ·
   working capital change and % of sales · capex and % of sales · adjusted tax and effective
   rate · lease principal repayments and % of sales · **FCF** · periods from the PV date ·
   discount factor · discounted FCF.

   *The bridge, in full.* PV of explicit FCF · PV of terminal value · **EV** · associates ·
   minority put/call liabilities · net debt on a stated IFRS 16 basis · **equity value** · share
   count · **price objective** · upside or downside against a dated current price · market cap.

   *Terminal assumptions as their own visible inputs:* terminal growth, terminal EBIT margin,
   terminal D&A as % of sales. All blue, none buried in a formula.

   *Implied multiples on the price objective:* EV/Sales, EV/EBITDA, EV/EBIT, P/E, FCF yield. A
   target implying a multiple the name has never traded on is the sanity check that catches the
   error before a reader does.

   *Tax.* Where profit or revenue by country is disclosed, build the blended statutory rate from
   the country mix and reconcile it to the reported effective rate, explaining the gap. A single
   typed tax rate on a multinational is a guess.

5. **Macro / FX** — a currency table. A group-level "FX impact" line with no pairs behind it
   is not a macro sheet.

   *Deriving the pairs when the company does not disclose them.* Most do not, and that is not a
   reason to skip the sheet — work it out from the revenue-by-region split and the annual report's
   market commentary. Worked example: Americas ~36% of group, of which the US is ~16–17% → EUR/USD
   is material, and the residual ~19% is Mexico, Brazil, Canada → EUR/MXN, EUR/BRL, EUR/CAD.
   Europe ~50% → check whether the UK and Turkey sit inside that number and strip them out if
   disclosed separately → EUR/GBP, EUR/TRY. Asia-Pacific → EUR/JPY, EUR/CNY, EUR/KRW. Ten to
   twenty pairs; state which exposures were excluded and why. Where fewer than ten can be
   established, build what can and name the constraint.

   *History.* Spot and period averages are public. Populate **annual and quarterly** across the
   history span, because the model forecasts quarterly and builds to H1, 9M, H2 and the year — the
   FX series must exist at that grain or Drivers cannot reference it. Include the year-to-date
   average for the current year.

   *Forecast.* Ask the basis — spot held flat (default), forwards, or the analyst's own deck — and
   accept a pasted or uploaded rate table as a first-class input. Where nothing is supplied, hold
   spot flat and label it.

   *Wiring.* Each segment's and region's FX row on Drivers references a pair here by row code,
   never a typed number. Translation effects flow through the revenue bridge; transaction effects
   sit in cost of goods and margin.

6. **Consensus** (Standard/Advanced, if a company template exists) — map every template field
   to a model row with a definition-match check BEFORE populating (net-debt IFRS-16 basis, EPS
   diluted basis, ETR basis, WC basis are the usual false-divergence traps). Estimates link to
   the model (never hardcoded); company consensus mean sourced and dated; flag thresholds
   >3% sales / >5% primary profit / >10% EPS. A definition mismatch is not an analytical
   divergence — resolve it first.

## THE DRIVERS SHEET — detail on top of the core logic

Layout and the four rules are in THE CORE LOGIC above. This is only the detail.

**Forecast mechanics.** Forward revenue per segment is prior period × (1 + LFL), with FX and
scope applied as their own stated terms. The LFL rate, the FX rate and the scope rate are the
blue inputs; revenue is a formula. Forward margin per segment is prior margin ± the bps
assumption, the bps figure being the blue input — forecasting a margin level hides the judgement,
forecasting the change exposes it. Segment operating profit is margin × revenue. Never type a
forecast revenue or a forecast margin level.

**Period layout.** Strictly chronological; a prior year never sits right of the year it precedes.
One periodicity ladder declared at kickoff and applied identically to every segmentation — by
default quarterly for the last reported year, the current year and the next full year, annual
thereafter, with H1, 9M and H2 inside their year. Group each year's sub-annual columns under its
FY column so the sheet collapses to annual. Forecast down the column: one column holds one
period's complete assumption set.

**Retrieval.** The growth decomposition is disclosed as percentages, and it is spread across the
press release, the filing, the results presentation, the annual report and the call transcript —
rarely all in one. Read all five rather than stopping at the release. Where a segment's LFL, FX or
scope is genuinely not given, leave it blank and say so; never derive one segment's rate from the
group's.

**Unit-economics drivers above the segment blocks, where disclosed** — units by brand, online
penetration, store count, price and mix.

**Nothing on the Financial Model duplicates this sheet.** LFL, FX and scope live here only.

## STATEMENT COMPLETENESS — the lines a real model carries

A cash flow of net profit, capex and working capital is not a cash flow statement. Build the full
articulation, and where a line is genuinely nil or undisclosed show it as nil rather than
omitting it — an absent line reads as an oversight.

**Cash flow, at minimum:** net profit · D&A · change in working capital · profit or loss from
associates and JVs · non-cash financial expenses · other adjustments · **operating cash flow** ·
capex and capex as % of revenue · **operating free cash flow** with conversion as % of EBITDA and
of EBIT · M&A · dividends received · other · **cash flow from investments** · dividends paid ·
own shares and buybacks · change in debt · principal lease repayments (IFRS 16) · other ·
**cash flow from financing** · **total cash flow** · FX movement · **total cash flow after FX**.
Then the post-lease measures the market quotes: OpFCF post leases, and its conversion against
EBIT and against adjusted net income.

Lease principal repayments are their own line, never inside "other" — post-IFRS 16 the market's
free cash flow measure depends on them.

**Balance sheet and cash flow are their own sections**, visually separated from the P&L with
their own headers, or their own sheets where the model is large enough. Every line articulating
with the P&L or the balance sheet is a formula, not an input.

## THE PUBLICATION LAYER — where the house has one

House models feeding a downstream platform or consensus contribution carry a mapping sheet
(often `Digital Template`). It is a machine-readable contract: CONTROL / HEAD / HIDDEN / BODY
row grammar; company GUID, template GUID and `template_version`; a descriptive header; one row
per published line carrying its item GUID and the sector template's **standardised** item name
(Sales, EBITDA, EBIT, PBT, Tax Rate, Net Income, Average Number of Shares (FD), EPS (FD)); and
its own ACTUAL/ESTIMATE split and year cascade off one anchor.

Map by row code, never by address. Never invent a GUID. Where a standardised item has no clean
equivalent in this company's accounts, leave it unmapped and say so — a forced mapping publishes
a wrong number into a comparison set. Where the sector template is unknown, ask.
