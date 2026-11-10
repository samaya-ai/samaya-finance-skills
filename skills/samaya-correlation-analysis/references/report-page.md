# Report page spec: report.json → report.html

Write one helper in your working folder that takes the path to `report.json` (the `analysis.json` from `references/analysis.md` plus the fields you added in step 4 of SKILL.md) and the path to `analysis.json`, runs the checks below, and writes `report.html`. Standard library only. Build the page from the data every time; never hand-edit the output. The helper must run on Python 3.9 (macOS `/usr/bin/python3`): no `X | Y` type hints unless `from __future__ import annotations` is first, no `match` statements.

Two forms:

- **Fragment** (for the Artifact tool, which adds the page skeleton): the `<title>`, then the `<style>` block, then the page content. No doctype and no `html`, `head` or `body` tags.
- **Standalone**: `<!doctype html>`, `<html lang="en">`, a `head` with `<meta charset="utf-8">`, `<meta name="viewport" content="width=device-width,initial-scale=1">`, the title and the style, then a `body` holding the page content.

The `<title>` is `title` from report.json, or "Correlation Analysis" if empty. No scripts, no external files, fonts or images: the page is self-contained.

HTML-escape every piece of text that comes from report.json (tickers, titles, facts, URLs in attributes, sentences). Every external link opens in a new tab: `target="_blank" rel="noopener"`.

In the templates below, {braces} mark a value filled from report.json; everything else is fixed wording.

## Checks (run before building)

Collect every problem, then, if there are any, print "report.json problems:" followed by one per line, write nothing, and stop. The problems to look for:

1. For each group (name it "A + B + C" in messages):
   - the number of `dates` differs from `co_move_days`;
   - `up + down` differs from `co_move_days`;
   - a date whose `driver` is not one of `oil`, `fed`, `earnings`, `inflation`, `consumer`, `sector`, `none` (including a null driver);
   - a date with a driver other than `none` and no source id;
   - a source id on a date that is not a key of `evidence_sources`.
2. `drivers_summary` has more than 3 bullets, or a bullet's `text` has more than 50 words (split on whitespace).
3. A source id used on any date whose `evidence_sources` entry has no `fact` ("add a one-line 'fact' with the size of the move or the event").
4. `takeaway`, `range_label` or `proof_note` is missing or empty.
5. A value from `analysis.json` differs in `report.json` ("{field}: changed from analysis.json", with the field path, for example `groups[2].score`). Compare exactly, with `==`, never by rounding:
   - top level: every key of `analysis.json` except `range_label`, that is `start`, `end`, `trading_days`, `benchmark`, `benchmark_avg`, `avg_moves`, `beta`, `corr_benchmark`, `min_days`, `max_group_size`, `market_wide_days`;
   - `groups`: the same number of groups in the same order; in each group every key except `dates`, that is `tickers`, `score`, `co_move_days`, `up`, `down`, `any_move_days`, `market_wide_days`, `market_wide_bench_opposite`, `return_corr`, `beta`;
   - `dates`: the same number in the same order; in each date every key except `driver` and `sources`, that is `date`, `direction`, `market_wide`, `bench_move`, `bench_opposite`.

   Only `driver` and `sources` on dates, `range_label`, and the new fields from step 4 of SKILL.md may differ or be added. Any changed number blocks the build like every other problem: fix `report.json` by copying the value back from `analysis.json`, never the other way round.

## Fixed driver list

Same order and colors in every run. "Short" is the label used in the groups table.

| Key | Label | Short | Color |
|---|---|---|---|
| `oil` | Oil or commodity prices | Oil | `#D9711C` (orange) |
| `fed` | Fed / interest rates | Fed | `#2563EB` (blue) |
| `earnings` | Earnings, dividends, buybacks | Earnings | `#14918A` (teal) |
| `inflation` | Inflation and macro data | Macro data | `#8B3FC4` (purple) |
| `consumer` | Consumer demand data | Consumer | `#D6457A` (pink) |
| `sector` | Sector news or regulation | Sector | `#7A8B2E` (olive) |
| `none` | No clear news found | Unclear | `#CFCBC4` (light grey) |

## Derived values

- **Unit word**: "pair" if every group has exactly 2 tickers (also when there are no groups), else "group".
- **Short date** (MM-DD): the date with the year dropped, for example "2026-08-05" → "08-05". Used in every date list on the page.
- **Day mix** of a group: for each driver in the fixed order, the number of its dates with that driver; leave out drivers with 0.
- **Common driver** of a group, with n = `co_move_days`: take the driver other than `none` with the most days (on a tie, the first in the fixed order). If its count × 2 > n, the common driver is "{Label} ({count} of {n} days)", for example "Oil or commodity prices (12 of 19 days)". Otherwise, or if every date is `none`, it is "No common driver found".
- **Benchmark caveat** of a group, with mw = its `market_wide_days` and opp = its `market_wide_bench_opposite`:
  - If mw × 2 > n and opp × 2 ≥ mw: "Not a market effect: benchmark moved the other way on {opp} of {mw} market-wide days."
  - If mw × 2 > n and opp × 2 < mw: "Mainly broad-market moves ({mw} of {n} days market-wide)."
  - Otherwise no caveat.
- **Unexplained dates**: every date tagged `none` in any group, each date once, oldest first.

## Page content, in order

Everything sits in one centered wrapper.

1. **Heading.** `h1` with `title` (or "Correlation analysis"). Under it a muted meta line: "{range_label} · {start} to {end} · {trading_days} trading days · benchmark {benchmark}".
2. **Takeaway.** `h2` "Takeaway", then the `takeaway` text in a paragraph.
3. **Driver chart card.** A card containing:
   - `h3`: "How often each {unit} moved together, and why ({range_label})".
   - A muted sub-line: "Bar length = score: of the days when any stock in the {unit} had a big move, the share of days when all of them moved the same way. Colors split the bar by the news behind those shared days; the number in each color is the count of days."
   - The chart (below), inside a box that scrolls sideways. If there are no groups, instead a muted line: "No group had enough shared big-move days."
   - The legend: one item per driver used on at least one date, in the fixed order: a 12 px square swatch in the driver's color with 2 px rounded corners, then the label. If `driver_themes` has text for that key, show "{Label} ({theme})".
   - If `driver_how_to_read` is set: a paragraph "**How to read it:** {driver_how_to_read}".
4. **What drove the co-moves.** Only if `drivers_summary` has bullets: `h2` "What drove the co-moves", then a bullet list. Each bullet is "**{name}.** {text}"; a bullet given as a plain string is shown as is.
5. **Groups.** `h2` "Groups", then a muted note: "Score = shared big-move days ÷ days when any member had a big move. ↑/↓ = direction of the shared move. * = market-wide day; "opposite {benchmark}" = market-wide days when {benchmark} moved the other way. Each source id (S1, S2…) links to the source; hover over it to see the date and the fact it proves." Then the groups table (below).
6. **Dates with no supporting source.** A muted line: "**Dates with no supporting source** ({count}): {short dates, comma-separated}", or "none" after the colon if there are none.
7. **Average moves.** `h2` "Average moves", a muted line "Mean absolute daily % change, {start} to {end}.", then the average moves table (below).
8. **Market-wide days.** A muted line: "**Market-wide days** ({count}): {short dates from the top-level list, comma-separated}", or "none".
9. **Methodology.** `h2` "Methodology", then a bullet list (below).

## The driver chart

An inline SVG, `viewBox="0 0 1000 H"`, `role="img"`, `aria-label="Driver chart"`, drawn at 100% width with auto height and a minimum width of 640 px (so on a phone it scrolls inside its box).

- Layout: label column 150, right margin 150, so the plot area runs from x = 150 to x = 850 (width 700). Top padding 10, row height 46, bar height 30. H = 10 + 46 × (number of groups) + 36.
- Grid: vertical lines at 0, 25, 50, 75 and 100% of the plot width, from y = 6 to y = H − 30, 1 px in the grid color. Axis labels "0%" … "100%" centered under each line at y = H − 10, 15 px, muted.
- One row per group, in the report's group order (already sorted by score). Row i (from 0) has its bar top at y = 10 + 46i + 8 and its center 15 below that.
- Row label: the tickers joined with " + ", right-aligned at x = 136, vertically centered, 17 px.
- Bar: starts at x = 150. For each driver in the fixed order with c > 0 days in the group, draw a rectangle of width 700 × score × c / co_move_days in the driver's color, each one right after the last, so the whole bar is 700 × score long. Give each rectangle a hover tooltip (an SVG `title` element): "{Label}: 1 day" or "{Label}: {c} days".
- If a segment is at least 22 units wide, write c centered in it, 15 px, weight 600, white; on the grey `none` segment use dark text `#3A3A3A` instead.
- After the bar's end, 10 units to the right and vertically centered: the score as a whole percent in bold (score × 100, rounded) followed by " · {co_move_days} days" in muted text, 16 px. Example: "**61%** · 19 days".
- All SVG text uses the page font and the text color, so it follows light and dark mode.

## The groups table

Columns: `#` · Group · Score · Return corr · Beta vs {benchmark} · Co-move days · Market-wide days · Common driver · Dates and proof. One row per group, numbered from 1.

- **Group**: tickers joined with " + ", bold, no wrapping.
- **Score**: whole percent; under it, small and muted, "{co_move_days}/{any_move_days}". The cell does not wrap (`white-space: nowrap`).
- **Return corr**: `return_corr` as stored.
- **Beta**: one line per member, "{ticker} {beta to 2 decimals}", small, no wrapping.
- **Co-move days**: "{co_move_days} ({up}↑ / {down}↓)", no wrapping (`white-space: nowrap`).
- **Market-wide days**: the group's `market_wide_days`; under it, small and muted, "{market_wide_bench_opposite} opposite {benchmark}".
- **Common driver** (at least 190 px wide): the common driver text; under it, small and muted, the day mix as "{Short} {count}" items joined with " · " (for example "Oil 12 · Sector 2 · Unclear 5"); under that, small, the benchmark caveat if there is one.
- **Dates and proof** (small, at least 320 px wide, line height 1.7): every date of the group, oldest first, joined with " · ". Each item is the short date, then ↑ or ↓, then * if market-wide (kept together, no wrapping), then:
  - for `none`: muted "no source";
  - otherwise: the driver's Short label and its source ids, comma-separated. Each id links to the source's `url`, with a hover tooltip (`title` attribute) of the source's title, date and fact joined with " · " (skip empty parts). A source with no url shows the id as plain text with the same tooltip.
- Example item: "08-03↓* Oil S4, S7".

There is no separate source list: the id links are the citations.

## The average moves table

A narrower table (at most 640 px) with columns Ticker · Avg daily move · Beta vs {benchmark} · Correlation with {benchmark}.

- One row per ticker from `avg_moves`, sorted by average move, high to low. Ticker bold; average as "1.23%" (2 decimals); beta and correlation to 2 decimals.
- Last row, set off by a heavier top border: "{benchmark} (benchmark)" bold, `benchmark_avg` as a bold "0.61%", then "1.00" and "1.00".

## Methodology bullets

Keep the wording exactly; fill the {braces}.

1. "Prices: daily closes from Samaya Market Data for {start} to {end} ({trading_days} trading days); the first % change uses the close of the trading day before the range." If `prices_sources` is not empty, add: " Price data (Samaya Market Data, as of {date of the first prices_sources entry, or "undated"}): {tickers, comma-separated}." with each ticker linked to its `url` (plain text if it has none).
2. "Big move: a day when a stock's absolute daily % change was above its own average absolute daily change over the range."
3. "Market-wide day: {benchmark}'s absolute move was above its own average, or at least 75% of the stocks had big moves in the same direction. These days stay in all counts and are marked *."
4. "Score: days when every stock in the group had a big move in the same direction, divided by days when at least one of them had a big move. Groups of {size} were tested; groups with fewer than {min_days} shared days were dropped. A larger group replaces the pairs inside it only if its score is at least 80% of each of theirs. The top 10 are shown." {size} is "any size" when `max_group_size` ≥ the number of tickers in `avg_moves`, else "up to {max_group_size} stocks".
5. "Return corr: Pearson correlation of daily % returns over the whole range (average across pairs for larger groups). Beta: covariance of the stock's daily return with {benchmark}'s, divided by the variance of {benchmark}'s."
6. "Drivers: each shared day was checked against Samaya sources. A day gets a driver only if a dated source shows news on that day (or the prior evening) or a meaningful same-day move in the driving market variable that fits the stocks' move. What counts as meaningful is a judgment call; each source's fact shows the size of the move. Otherwise the day is marked 'no clear news'."
7. "Judgment used in this run: {proof_note}"

## Styling

Define colors as variables on `:root`, with a dark set applied under `@media (prefers-color-scheme: dark)` guarded by `:root:not([data-theme="light"])`, and again under `:root[data-theme="dark"]`.

| Variable | Light | Dark | Used for |
|---|---|---|---|
| `--bg` | `#F7F6F3` | `#16181B` | page background |
| `--card` | `#FFFFFF` | `#1E2125` | chart card |
| `--line` | `#E4E1DA` | `#33373D` | borders, table rules |
| `--text` | `#1F2328` | `#E8E6E3` | body and SVG text |
| `--mute` | `#6B6F76` | `#9AA0A6` | meta lines, small notes, axis labels |
| `--grid` | `#E9E6E0` | `#2C3036` | chart grid lines |
| `--accent` | `#0F8A80` | `#3FB8AD` | `h2` headings and links |

Driver colors are the same in both modes.

- `box-sizing: border-box` on everything. Body: no margin, `--bg` background, `--text` color, 15 px system sans-serif stack (-apple-system, BlinkMacSystemFont, "Segoe UI", Inter, Helvetica, Arial, sans-serif), line height 1.55.
- Wrapper: max width 1080 px, centered, padding 28 px top, 16 px sides, 48 px bottom.
- `h1` 22 px, margin 0 0 4 px. `h2` 20 px in the accent color, margin 28 px 0 8 px. Card `h3` 17 px, margin 0 0 4 px.
- Card: `--card` background, 1 px `--line` border, 12 px radius, padding 22 px 24 px, margin 14 px 0.
- Chart sub-line 13.5 px muted, 12 px below. "How to read it" 14 px, 12 px above. Legend: wrapping row, gaps 6 px by 18 px, 13.5 px, 10 px above.
- Meta lines 14 px muted. Bullet lists indent 20 px; Drivers bullets at most 900 px wide with 8 px below each; Methodology bullets 4 px below each, in the text color.
- Tables: full width, collapsed borders, 13.5 px. Cells padded 8 px 10 px, left-aligned, top-aligned, 1 px `--line` bottom border. Headers muted, weight 600. Small text 12.5 px. Each table sits in a box with sideways scrolling.
- The page itself must never scroll sideways at phone width: only the chart box and the table boxes scroll.

## Final look-over

Open the built page and confirm: the sections are in the order above; the chart has one bar per group with the right percentages; every non-`none` date shows at least one linked source id; the two date lists and the methodology are present; and both light and dark modes read cleanly.
