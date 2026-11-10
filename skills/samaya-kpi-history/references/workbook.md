# The workbook — samaya-kpi-history

Read before building the Excel. This skill bundles no code: you write a short `openpyxl` helper
yourself, in your scratch working folder, from the spec below. Every value, colour, width and
format here is fixed so every run looks the same. Do not add styling, sheets or columns the spec
does not name, and do not drop any it does.

## HOW TO BUILD IT

1. **Write the grid as JSON** in the scratch folder (shape below). The JSON is the single input;
   the helper reads it and writes nothing it did not get from it.
2. **Write the helper** in the scratch folder, never the outputs folder, and run it with the JSON
   and the output path. If `openpyxl` is missing, `pip install openpyxl`. The helper must run on
   Python 3.9 (macOS `/usr/bin/python3`): no `X | Y` type hints unless
   `from __future__ import annotations` is the first statement, and no `match` statements.
3. **Reopen the saved file** with `openpyxl.load_workbook` and run every check under CHECKS. On any
   failure, fix the helper and rebuild; do not patch the saved workbook by hand.
4. Only then send the workbook (SKILL.md, Step 2). The JSON and the helper stay in the scratch
   folder and are never sent.

## THE JSON SPEC

```json
{
  "title": "XPO North American LTL — YoY % per day",
  "metrics": [{"name": "Tonnage/day YoY %", "format": "pct"}],
  "rows": [
    {"company": "XPO", "period": "Jan 2023", "status": "Final", "note": "",
     "values": {"Tonnage/day YoY %": {"value": 2.8, "title": "Q1 2023 earnings call",
       "date": "2023-05-04", "url": "https://app.samaya.ai/u/...", "excerpt": "..."}}}
  ],
  "notes": ["Disclosure map and breaks, one line each"],
  "scorecard": {"Periods found": "44/48"}
}
```

- **`metrics`** — in column order. `name` carries the unit and basis ("Tonnage/day YoY %").
  `format` is `pct` or `number`; omitted means `number`. `"format": null`, or any other value,
  means apply no number format at all.
- **`rows`** — one per grid period, in grid order (per company × period for a peer panel). Every
  row has `period` and `status`; `company` and `note` default to empty. `status` is one of the
  vocabulary in `references/retrieval-and-gaps.md`.
- **`values`** — keyed by metric name. A metric with no figure is simply absent from `values`.
  Each entry has `value` (a number, or `null`), `title` (document name), `date` (ISO),
  `url` (the provenance link exactly as retrieved) and optional `excerpt` (the one sentence or
  table row containing the figure).
- **Percent values are stored as the number shown**: a 2.8% YoY change is `2.8`, not `0.028`. The
  `pct` format appends the `%` sign without multiplying.
- **`notes`** — the Notes & breaks content, one string per line, in the order to show.
- **`scorecard`** — label → value, in the order to show; the same figures as the chat scorecard.
- An empty or missing `notes` or `scorecard` still creates its sheet with its widths and styling;
  the sheet simply has no content, so A1 is blank. No placeholder text.

**Peer panel or single company.** The run is a peer panel when the rows carry more than one
distinct `company` value; otherwise it is single-company. That one test decides the lead columns,
the Pivot sheet and the Chart sheet.

## SHEETS, IN THIS ORDER

1. `Series` (always first; rename the default sheet)
2. `Chart` (single-company runs with more than two rows) **or** `Pivot` (peer panels)
3. `Notes & breaks`
4. `Scorecard`

A single-company run with two rows or fewer has no Chart sheet. No other sheets.

## SERIES SHEET

### Columns (row 1 is the header)

| Block | Header text | Cell contents |
| --- | --- | --- |
| Lead | `Company`, `Period` (peer panel) or `Period` alone (single company) | the row's company and period label |
| Values | one column per metric, header = the metric name | the metric's `value`; blank when absent or `null` |
| Status | `Status` | the row's status |
| Sources | one per metric, header = `Source: <metric name>` | the metric's document `title`; blank when absent |
| Note | `Note` | the row's note |

So a single company with two metrics runs: `Period | M1 | M2 | Status | Source: M1 | Source: M2 |
Note`. The first value column is B for a single company and C for a peer panel.

### Header row

Every cell in row 1: bold white font (`FFFFFF`) on a solid dark-navy fill (`1F3864`). No other
row is styled this way, and no other header styling (borders, alignment, height) is set.

### Data rows

One row per spec row, in spec order, starting at row 2. For each metric in each row:

- **Number format** on the value cell, set whether or not the cell holds a value:
  - `pct` → `0.0"%";(0.0"%")` — one decimal, literal `%`, negatives in parentheses.
  - `number` → `#,##0.00`.
  - `null` or any other value → leave the cell's format untouched.
- The openpyxl `Comment` used here is Excel's legacy Note, which is what `samaya-conventions.md`
  means by "Notes, never comments"; never write a threaded comment.
- **Cell comment and hyperlink** only when the metric's entry exists, its `value` is not `null`
  and it has a `url`:
  - A comment on the **value cell**, author `samaya-kpi-history`, width 340, height 110, whose
    text is these lines joined with newlines:
    1. `<title> (<date>), via Samaya.`
    2. the excerpt wrapped in straight double quotes — this line only when an excerpt exists
    3. the URL
  - On the matching **Source cell**: hyperlink to the URL, font colour `0563C1`, single
    underline. The cell's displayed text stays the document title.
  - A Source cell with a title but no qualifying value (no URL, or `null` value) keeps the title
    as plain text, with no link and no link font.

### Gap rows

When a row's status is `Not disclosed`, `Not retrieved` or `Not yet reported`, every cell in that
row from column A to the last column gets a solid light-peach fill (`FCE4D6`). No other status
is shaded — `Derived`, `Comparative`, `Proxy` and `Preliminary` rows look like `Final` rows and
are told apart by their Status cell and Note.

### Breaks, revisions and derived values

There is no separate colour or marker for these; they are carried in text, the same in every run:

- **Definition break** — the redefined metric is a second metric column with its own name (e.g.
  "Revenue per load, old basis" and "Revenue per load, new basis"), each blank on the other's
  periods. The Note of the first period on the new basis names the break and its date, and the
  Notes & breaks sheet explains it.
- **Revision or restatement** — the row carries the value on the series' basis; its Note records
  the other value, its document and date ("Flash +3.1% (8-K, 2024-02-06); revised to +2.8% in Q4
  call").
- **Derived, comparative, proxy** — the status says which; the Note gives the working or the
  source document.
- **Gap rows** — the Note gives the reason (`company reports Q3 only as a quarterly total`).

### Widths and freeze panes

- Column width by header: `Source…` columns 44, `Note` 60, every other column 16 (Company,
  Period, value columns, Status).
- Freeze panes at row 2 of the first value column (`B2` single company, `C2` peer panel), so the
  header row and lead columns stay in view.
- No wrap, autofilter, borders or conditional formatting.

## CHART SHEET — single company, more than two rows

- A sheet named `Chart` holding one **line chart**, anchored at `A1`.
- Chart title = the spec's `title` (empty if none); height 8, width 22 (openpyxl chart units, cm).
- Data: every value column of the Series sheet, rows 1 through the last row, with series names
  taken from the header row (one line per metric).
- Categories: column A (Period) of the Series sheet, rows 2 through the last row.
- No axis titles, styles or colours beyond openpyxl's defaults. Gap rows plot as breaks because
  their cells are blank; do not fill them.

## PIVOT SHEET — peer panels only

- A sheet named `Pivot`. Header row: `Period`, then one column per company × metric, labelled
  `<company> — <metric>` (an em dash with a space each side). Companies in alphabetical order;
  within each company, metrics in spec order.
- Header row styled as on Series: bold white on `1F3864`.
- One row per distinct period, in the order periods first appear in the spec rows. Each cell
  holds that company's value for that period and metric, or blank.
- Values only: no number formats, comments, links, gap shading, widths or freeze panes.

## NOTES & BREAKS SHEET

- A sheet named `Notes & breaks`, no header row. Each `notes` line goes in column A, one per row
  from row 1, in order.
- Column A width 130, and every cell in column A set to wrap text.
- Content: the disclosure map per company (label, definition, where disclosed, cadence, start
  date, fiscal calendar), every break with its date, cadence changes inside the window, proxies
  used and why, and anything deliberately excluded.

## SCORECARD SHEET

- A sheet named `Scorecard`, no header row. One row per scorecard entry: label in column A, value
  in column B, in spec order.
- Column A width 26 and every column-A cell bold; column B width 90.
- Same figures as the chat scorecard, including elapsed time.

## CHECKS — on the reopened file, before sending

Reopen the saved `.xlsx` and confirm each of these. Any failure means fix and rebuild.

1. **Sheets.** Names and order exactly as above: `Series`, then `Chart` or `Pivot` (or neither,
   for a single company with two rows or fewer), then `Notes & breaks`, `Scorecard`.
2. **Grid.** Series has exactly one data row per spec row (`max_row` = rows + 1), and the period
   list matches the grid — no period missing, none added.
3. **Headers.** Row 1 matches the column layout above, in order, with bold white on `1F3864`.
4. **Status.** Every data row has a status from the vocabulary, and every gap-status row
   (`Not disclosed`, `Not retrieved`, `Not yet reported`) has a Note giving the reason. Blank
   cells in a definition-break column on the other basis's periods are expected and need no Note.
5. **Provenance.** Every non-blank value cell has a comment carrying the title, date and URL, and
   its Source cell links to that same URL with the link font. The URL is byte-identical to the
   one retrieval returned — none built, shortened or edited.
6. **Gap shading.** Exactly the rows with a gap status are filled `FCE4D6`, across every column.
7. **Formats.** Every value cell carries its metric's number format (none for a `null` format); percent values are on the
   2.8-means-2.8% scale.
8. **Layout.** Freeze panes at `B2` or `C2`; widths 16 / 44 / 60 on Series, 130 on Notes, 26 / 90
   on Scorecard.
9. **Chart or Pivot.** Single company with more than two rows: one line chart with one series
   per metric. Peer panel: Pivot column count = 1 + companies × metrics, and its values match
   Series.
10. **Scorecard** matches the scorecard you will post in chat.
