# The page: what to build

Write the page yourself as one self-contained HTML file: inline CSS, one inline vanilla
JavaScript script, an inline SVG chart drawn by that script, and the page data (`checks.md`
section 2) embedded as JSON in `<script id="data" type="application/json">`. No libraries, no
other external requests, except fonts from Google Fonts: Inter (optical size 14..32, weights
400..700) and JetBrains Mono (400, 500), with `preconnect` hints for `fonts.googleapis.com` and
`fonts.gstatic.com`. Every number shown comes from the embedded data; nothing is typed into the
markup by hand.

`<title>`: `<TICKER>: what moved the stock`. `lang="en"`, `charset utf-8`, viewport
`width=device-width, initial-scale=1, viewport-fit=cover`.

## Contents
1. Tokens and type
2. Layout, top to bottom
3. Phase tiles
4. Controls bar
5. The chart
6. Markers
7. Hover and click
8. Detail panel
9. Tables and collapsed sections
10. Formatting and accessibility

## 1. Tokens and type

Define colours as CSS custom properties on `:root`; redefine them for dark mode under
`@media (prefers-color-scheme: dark)` with `:root:not([data-theme="light"])`, and again under
`:root[data-theme="dark"]`. Set `color-scheme` to match. The chart reads the tokens at draw time,
and redraws when the colour scheme changes.

| Token | Light | Dark | Use |
|---|---|---|---|
| `--surface` | #ffffff | #15171a | Page background, hollow marker fill |
| `--surface-2` | #f6f7f8 | #1d2024 | Tiles, chips, hovered rows |
| `--ink` | #181A1E | #eef0f2 | Text, cluster badges |
| `--ink-soft` | #3E4349 | #c4c9ce | Secondary text, results ticks |
| `--ink-muted` | #6b7279 | #8e959c | Labels, axes, market part bars |
| `--rule` | #D7DDD9 | #33383d | Borders, zero line |
| `--rule-soft` | #ecefed | #24282c | Grid lines, row rules |
| `--brand` | #0019FF | #6b7dff | Focus outlines |
| `--brand-ink` | #0012B2 | #9aa6ff | Links |
| `--price` | #3366FF | #6f93ff | Price line, hover dot |
| `--bench` | #8b9197 | #7d848b | Benchmark line, market diamonds |
| `--up` | #299448 | #4cc06c | Up moves |
| `--down` | #E01F1A | #ff5a52 | Down moves |
| `--none` | #9aa1a7 | #6f767c | "No catalyst found" |
| `--up-soft` / `--down-soft` | rgba(41,148,72,.16) / rgba(224,31,26,.14) | rgba(76,192,108,.18) / rgba(255,90,82,.16) | Run hatching |
| `--band` | rgba(51,102,255,.07) | rgba(111,147,255,.10) | Phase highlight, multi-day bands, normal range |
| `--vol` | #c5cbd0 | #3a4046 | Ordinary volume bars |
| `--vol-ev` | #6b7279 | #9aa1a7 | After-hours bar outline |
| `--tip-bg` / `--tip-ink` | #181A1E / #ffffff | #eef0f2 / #15171a | Tooltip |

Type: body Inter 15px/1.5, antialiased. Every number (key figures, table numerals, tooltip,
panel figures, axis labels, tile figures) in JetBrains Mono with tabular figures. Content column
max 1240px, centred, padding 28px 24px 56px; respect safe-area insets. Positive figures in
`--up`, negative in `--down`.

## 2. Layout, top to bottom

1. **Header.** A line in muted 14px text: ticker (bold, ink, 15px), company name, and the window
   as "16 Oct 2025 to 15 Oct 2026". Then the headline as `h1`: `clamp(22px, 3.1vw, 32px)`, weight
   about 640, tight letter-spacing, max 46ch, balanced wrapping. Then a key-figures line: ticker
   total return, benchmark return, "Stock-specific" (`spec_part`) and "Market-explained"
   (`mkt_part`), each a label then a signed whole-number percent, coloured by sign. If the data
   carries a `standfirst`, show it under the headline in 16px soft ink.
2. **Phase tiles** (section 3).
3. **Controls bar** (section 4).
4. **Main grid:** chart column (`minmax(0, 1fr)`) and a 330px detail panel, 24px gap. Below
   960px the panel stacks under the chart.
5. Under the chart, a 12.5px muted caption: "Daily candles for <TICKER> and <BENCH>, Market Data
   via Samaya, as of <d Mon yyyy>. Grey is the market part of each day's move (beta x <BENCH>);
   colour is the stock-specific part. Letters mark the phases above."
6. **"Event days"** heading and table, then the "other" notes line (section 9).
7. Three collapsed sections: "Large moves the market explained (<n>)", "How this chart is
   built", "Sources (<n>)".

## 3. Phase tiles

A grid of 4 equal columns (2 below 900px; below 620px a horizontal scroll-snap strip with each
tile 78% wide). Each tile is a button on `--surface-2` with 10px radius, containing:

- a mono label: phase letter (A, B, C...) then "d Mon to d Mon";
- the title (15px, weight ~640);
- the phase return, signed whole percent, 24px mono, coloured;
- "stock-specific <signed whole percent>" in 12px muted mono;
- the phase text, 13px soft ink;
- on the last tile only, when `next` exists: "Next: <label without ', after the close'>, d Mon".

Clicking a tile toggles a highlight band (`--band`) over that phase in the price pane and sets
`aria-pressed`; clicking it again clears it. Hide the tile row if there are no phases.

## 4. Controls bar

- **View switch** (segmented control, pressed state ink background with surface text): Price
  (default), Daily split, Cumulative split.
- **Legend** (muted 12.5px, pushed right): filled dot "Confirmed"; outlined dot "Reported";
  dotted dot "X context"; dashed hollow dot "No catalyst"; small outlined dot "Smaller move"
  (tooltip: smaller flagged moves are dots on the price line; click one for the same detail);
  hatched swatch "Run: multi-day move" (tooltip: a stretch of about two weeks where the stock
  moved well beyond the market without any single standout day; click a band for details).
- **Display** dropdown (a `details` element with a popover panel) with four checkboxes:
  1. benchmark (on): labelled "<benchmark_name> (rebased)" in Price view, "Normal-range band"
     in Daily split, "Market-explained line" in Cumulative split;
  2. "Market-driven days" (on);
  3. "No catalyst found (<count>)" (on) — hides or shows `none`-tier events everywhere on the
     chart;
  4. "Turning points" (off).

Any change redraws; if the selected event becomes hidden, clear the panel.

## 5. The chart

One SVG, width = the chart box width (minimum 340), height computed. "Narrow" means width under
620.

**Geometry.** Left padding 52 (narrow 40), right 16 (10). From the top: a marker rail of
`12 + rows * (2 * rMax + 4)` px (section 6), the price pane 340px (250), a 14px gap, the volume
pane 124px (88), a 22px month axis. Day `i` of `N` is centred at
`x0 + (x1 - x0) * (i + 0.5) / N`; bars are 72% of a slot (at least 1px).

**Views and scales.**

- *Price:* main series = daily close (`--price`, 1.9px). Second series = the benchmark rebased
  to the base close (`bench / bench[0] * base_close`), dashed `--bench` 1.25px, labelled with the
  benchmark ticker at its right end; shown when the benchmark option is on and included in the
  scale. Use a log scale when `hi / lo > 2.2`, else linear. Ticks: on a log scale pick from
  10, 20, 25, 30, 40, 50, 60, 75, 100, 125, 150, 200, 250, 300, 400, 500, 750, 1000 within the
  range; on a linear scale a "nice" step (1, 2, 2.5, 5 or 10 times a power of ten, about five
  steps). Labels: whole numbers at 100 and above, one decimal below 10.
- *Cumulative split:* main series = cumulative stock-specific (`prod(1 + abn) - 1`, labelled
  "Stock-specific" in `--price`); second = cumulative market-explained (`prod(1 + mkt) - 1`,
  dashed, labelled "Market-explained (beta x <BENCH>)"). Scale `ln(1 + v)`; percent ticks from
  -90% to +200% at round values; the 0% line is heavier.
- *Daily split:* one stacked bar per day. Grey (`--ink-muted`) from 0 to the market part `mkt`,
  full opacity on market days, 0.7 otherwise. Coloured (`--up`/`--down` by sign of `abn`) for the
  stock-specific part: stacked on top of the grey when both share a sign, otherwise from 0;
  opacity 1 on event days, 0.4 otherwise. A shaded `--band` area between `±z_min * sig` (the
  normal range) when the benchmark option is on. Percent axis with a heavier 0% line. Markers sit
  on the bar's tip: `mkt + abn` when signs agree, else whichever part is larger in magnitude.

Pad every scale by 6% of its range. Grid lines `--rule-soft`; drop tick labels closer than 24px.

**Layers, in drawing order.**

1. Grid and y labels; volume baseline; the volume pane's top label = largest non-mechanical
   volume in millions to one decimal (e.g. "132.5M"; a trailing ".0" is dropped, so "132M"),
   right-aligned 6px left of the plot at the top of the volume pane; month ticks under the volume pane with "Mon" labels ("Jan yyyy" for
   January) where they fit, and only odd months on narrow screens.
2. Phase highlight band, if a tile is selected.
3. **Runs:** a hatched band across the price pane from start to end (45-degree hatch over
   `--up-soft` or `--down-soft`, dashed outline in `--up`/`--down`, 0.75 opacity; 2px outline when
   selected), with a small haloed label "Run: <signed %> vs market" bottom-left. Clickable and
   keyboard-focusable; opens the run panel.
4. **Phase boundaries:** dashed vertical lines at each phase start after the first, and the phase
   letter in mono near the top of the pane.
5. **Multi-day events:** a `--band` rectangle spanning the event's sessions over price and volume.
6. **Volume bars:** event days (of visible events) coloured `--up`/`--down` by that day's return;
   others `--vol`. Days in `after_hours_days` drawn as dashed outlines in `--vol-ev` with no fill.
   Scale volume to the largest non-mechanical day x 1.05; taller bars are clipped and get a small
   caret notch at the top. A dashed muted line traces the 50-session median volume; label the pane
   "Volume, with 50-day median" at top right.
7. The daily-split bars (Daily split only).
8. The benchmark / market-explained line, then the main line.
9. **Results ticks:** a small filled `--ink-soft` triangle on the volume baseline at each
   release `t0`.
10. **Context events:** the same triangle, open (surface fill, `--ink-soft` outline).
11. **Market-driven days** (when the option is on): a grey `--bench` diamond on the main series
    with a surface outline (offset 9px off the bar tip in Daily split).
12. **Turning points** (when on, Price view only): "▲ <close>" above highs, "▼ <close>" below
    lows, muted mono 11px.
13. Smaller-move circles, cluster badges, and event markers (section 6).
14. Hover crosshair, hover dot, and a transparent hit area over price and volume (section 7).

Haloed labels: text with a 4px `--surface` stroke painted under the fill.

## 6. Markers

Colour of an event: `--none` for tier `none`, otherwise `--up` or `--down` by the event's
return. Each marker shows its event number (order in `events`, from 1).

**Prominent events** get a numbered circle in the rail above the price pane, joined to the price
line at the event's last date by a thin line (55% opacity). Radius scales with the stock-specific
move: `rMin + (rMax - rMin) * sqrt(|abn| / max |abn|)` with `rMin` 8 and `rMax` 13.5 (narrow 7 and
11), times 0.82 for `price`-signal events. Style by tier:

- `confirmed`: filled with the colour, white number, no stroke;
- `reported`: surface fill, 2px coloured ring, coloured number;
- `social`: dotted ring (1 on, 2.5 off, round caps);
- `none`: dashed 1.5px ring in `--none`.

A selected marker gets an extra ring 4px outside it.

**Rows.** Place prominent markers left to right by the midpoint of their dates; each takes the
lowest row where it clears the previous marker in that row by 3px. Row 0 sits directly above the
price pane and further rows stack upward. With `rowH = 2 * rMax + 4`, `nRows` = the number of
rows used (at least 1) and `rail = 12 + nRows * rowH` (the price pane's top y), a marker in row
`r` is centred at `cy = rail - 6 - rMax - r * rowH`. The row budget is 3 rows on
desktop, 2 when narrow. While the rows exceed the budget, find chains of free, non-anchor markers
each within `2 * rMax + 3` px of the previous (an anchor breaks a chain); collapse the longest
chain of 3 or more that is not expanded and does not contain the selected event into a **cluster
badge** (filled `--ink` circle of `rMax` at the chain's mean position, showing the count in
`--surface`), then lay out again. Clicking a badge expands that cluster for the rest of the
session. Anchors (the three largest moves and every results reaction) never cluster.

**Smaller moves** (`prominent: false`) are numbered circles sitting on the main series at the
event's last date: radius 7.5 (9 when selected), 1.6px coloured ring, filled for `confirmed`,
dashed for `none`, number 8.5px. They open the same panel.

All markers are focusable buttons (`tabindex=0`, `role=button`, an `aria-label` with event number,
label and return) and respond to click, Enter and Space.

## 7. Hover and click

Hovering the plot shows a vertical crosshair at the nearest session, a dot on the main series
(not in Daily split), and a tooltip (dark `--tip-bg`, 11.5px mono, 6px radius, flips left near
the right edge) with:

- the date (sans, bold), plus "• market-driven move" on market days;
- `O h  H h  L l  C c` to 2 decimals;
- "<TICKER> <ret> = market <mkt> (β <beta> × <BENCH> <bench_ret>) + stock-specific <abn>";
- "Volume <x.x>M (<rvol>× median)";
- when relevant: "Includes after-hours trading on a results release"; "Index-driven volume:
  <label>"; "Event: <context label>"; "Inside a run (click for what drove it)"; in Cumulative
  split, "Cumulative stock-specific <x>, market-explained <y>".

Clicking the plot opens the nearest visible event whose dates are within one session of the
pointer; otherwise the run under the pointer, if any. The pointer shows a hand inside runs.

## 8. Detail panel

Sticky on desktop with a 3px left border (top border when stacked) coloured `--up`, `--down` or
`--none` for the selection, neutral `--rule` when empty.

**Empty state:** a hint: select a marker to see what moved the stock that day; numbered markers
are the moves that tell the story (bigger marker, bigger stock-specific move); small numbered
circles on the line are smaller flagged moves; a dark badge groups close-together events; grey
diamonds are days the market explains; hatched bands are runs, multi-day moves with no single
standout day.

**Event:** top line "<n> of <total>, <date or 'd Mon to d Mon yyyy'>" with previous/next step
buttons (wrapping, skipping hidden events); the label as a 19px title; a meta line: the tier text
("Company-confirmed", "Reported in news", "Context from X posts that day, not a confirmed cause",
"No catalyst found"), plus " (single source)" when set, the category in lower case, ", on normal
volume" for `price` signals, ", one of the window's largest stock-specific moves" for `rank`, and
the timing note in lower case; three figures: ticker return, `factor_label` (market part) and
"Stock-specific", signed to 1 decimal; the summary; a footer "Volume <rvol>× normal" plus the
follow-on text; a collapsed "Sources (<n>, <k> company)" list with company sources (Filings,
Press Releases, press-release feed, Transcripts) first, each a link (new tab, `rel=noopener`) on
its title with source name and date below. Selecting an event highlights its table row.

**Run:** "Run, d Mon to d Mon yyyy (<n> sessions)"; the run label; "<tier text>, multi-day move
with no single standout day"; the three figures (price change, market part, stock-specific); the
summary; a footer: a run is flagged when the stock-specific moves over <run_len> sessions add up
to an unusually large total, even though no single day stood out; collapsed sources.

## 9. Tables and collapsed sections

**Event days table** (min width 760px, scrolls horizontally inside its box): a coloured
numbered circle; date ("d Mon" or "d Mon–d Mon", then the two-digit year); move; stock-specific
move (both signed, coloured); what happened (label); "On chart" ("Marker" or "Dot"); attribution
("Confirmed", "Reported", "X context", "None found"). Rows are focusable; click or Enter selects the
event (turning "No catalyst found" back on if needed) and scrolls the chart into view.

**Other notes line** under the table, when present:
- "Other company events (marked with open triangles; none moved the stock beyond the screen):"
  then "d Mon label (source)" for each context event;
- "Multi-day runs (shaded; no single day stood out):" then "d Mon to d Mon <abn>: <summary>
  (source)";
- "Heavy volume from index mechanics, not news:" then "d Mon (<label in lower case, Russell
  capitalised>)".

**Large moves the market explained (<n>):** an intro: these days moved <TICKER> at least
<z_min>× a normal day in raw terms, but most of the move is what beta × <BENCH> predicts, so they
get no story; they are the grey diamonds on the chart. (If none: "No large market-driven days in
this window.") Then a table: date, ticker move, benchmark move, beta (2 dp), market part,
stock-specific, volume (x.x×).

**How this chart is built:** short paragraphs, with the parameters filled from the data:
- *Which days get a marker:* each day's move is split into a market part (the stock's
  <est_win>-day beta × <BENCH>'s move) and a stock-specific part; a day is marked when its
  stock-specific part is at least <z_min>× the stock's normal daily variation on volume at least
  <rvol_min>× its 50-day median, or at least <z_price>× on any volume; the window's <top_n>
  largest stock-specific moves are always marked; a hatched run marks <run_len> sessions whose
  stock-specific moves add up to an unusual total with no single standout day; every marked day
  is researched and none are dropped to fit a limit.
- *Daily split:* grey is the market part, colour the stock-specific part; the shaded band is
  <z_min>× the typical stock-specific move; event days are solid.
- *Cumulative split:* the two parts compounded separately; together they compound to roughly the
  total return.
- *Attribution:* a cause must be public before the close of the session it moved; a release after
  16:00 moves the next session; what each tier means; "No catalyst found" days are shown, not
  hidden; same-day rating changes are a reaction, not the cause.
- *Beat or miss* is against the company's own prior guidance; consensus is not used.
- *Volume:* coloured bars are event days; dashed outlined bars are results-release days whose
  volume includes after-hours trading; the reaction day carries the volume test.
- *Scale:* the `log_scale_note`.
- *Data notes:* from the page data's `integrity` object (`checks.md` section 2): every
  `repairs` and `issues` line verbatim (the vendor-gap and dropped-bar lines are in `issues`);
  the sector factor when `integrity.sector` is set; any constituent removal when
  `integrity.exclude` is set, with the sourced weight from `integrity.weight_path`; and any limit
  of the split (for example a market dominated by one peer).

**Sources (<n>):** a numbered list: the stock and benchmark price sources first, then every
distinct event source URL, each a link on its title followed by its source name.

## 10. Formatting and accessibility

- Percent: sign first, using a true minus (U+2212) for negatives; 1 decimal by default, whole
  numbers in headline figures and tiles (1 decimal if the whole-number value would round to 0).
- Dates: "d Mon yyyy" in full, "d Mon" when short.
- Volume: millions to 1 decimal ("63.1M").
- Escape all text taken from the data before inserting it as HTML.
- Visible focus outlines (`--brand`) on every interactive element; the panel is `aria-live`.
- Redraw on resize (debounced ~80ms). The SVG uses `touch-action: pan-y` so a phone can still
  scroll the page. No horizontal page scroll at phone width; wide tables scroll inside their box.
