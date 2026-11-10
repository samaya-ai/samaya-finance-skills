# Audit log workbook — `audit_log.xlsx`

The audit log is always delivered. Write a helper in your working folder that reads `data.json`
(shape in `references/audit-schema.md`) and writes this workbook with `openpyxl`. It must run
on Python 3.9 (macOS `/usr/bin/python3`): no `X | Y` type hints unless
`from __future__ import annotations` is first, no `match` statements. This
workbook is the deliverable itself, separate from any annotated copy of the original file.

## Before writing anything

1. Check every item's `flag` is exactly one of `Match`, `Stale`, `Mismatch`, `Unable to
   verify`. If any is not, stop without writing the file and report the item `id` and its bad
   flag. Fix the payload and rerun; never coerce a flag.
2. Count items per flag; the counts feed the `Summary` sheet and the chat summary.

## Styles

| Name | Setting |
|---|---|
| Title | Arial, bold, size 14 |
| Body | Arial, regular |
| Bold body | Arial, bold |
| Header | Arial, bold, white (`FFFFFF`) text on a solid `1F3864` (dark navy) fill |

Flag fills (solid):

| Flag | Fill |
|---|---|
| `Match` | `C6E0B4` (green) |
| `Stale` | `FFE699` (yellow) |
| `Mismatch` | `F8CBAD` (orange-red) |
| `Unable to verify` | `D9D9D9` (grey) |

## Sheet 1: `Audit Log` (the workbook's first, active sheet)

**Title block.**

| Cell | Value | Style |
|---|---|---|
| A1 | `Fact-Check Audit Log` | Title |
| A2 | `Source file: <source_file>` (`Not specified` when missing) | Body |
| A3 | `Items checked: <number of items>` | Body |

Row 4 is empty.

**Header row (row 5).** Ten columns in this order, each header cell in the Header style,
vertically centred, text wrapped. Set each column's width as listed.

| Col | Header | Width |
|---|---|---|
| A | `ID` | 6 |
| B | `Item Description` | 30 |
| C | `Original Stated Value` | 22 |
| D | `Location` | 24 |
| E | `Samaya-Sourced Value` | 22 |
| F | `Source Document` | 26 |
| G | `Source URL` | 40 |
| H | `As-Of Date` | 12 |
| I | `Flag` | 16 |
| J | `Note` | 36 |

**Data rows (row 6 onward).** One row per item, in payload order. Every cell in Body style,
aligned to the top, text wrapped. Cell values:

| Col | Value |
|---|---|
| A | `id` as given |
| B | `description` |
| C | `original_value` |
| D | Location text (rules below) |
| E | `samaya_value`, or `—` (em dash) when empty or null |
| F | `source_doc`, or `—` |
| G | `source_url` as plain text, or `—` |
| H | `as_of_date` as text, or `—` |
| I | `flag`, in Bold body with that flag's fill |
| J | `note`, or empty |

Write each value with the JSON type it has in the payload, unconverted: a JSON number (for
example `"id": 3` or `"samaya_value": 391.04`) is written as a number, a JSON string as text.
Never parse a string into a number or an Excel date (`"$391.0 billion"`, `"2024-11-01"` and
`"3"` stay text), and do not turn the Source URL into a hyperlink. The `—` fallback in E–H
applies to any falsy value (`null`, `""`, and also a numeric `0`); a missing or `null` `id`,
`description`, `original_value` or `note` leaves the cell empty.

**Location text.**

- No `location`: `Not specified`.
- `pptx`: `Slide <slide>`.
- `xlsx`: `<sheet>!<cell>`.
- `pdf`: `Page <page>`.
- `docx`: the `detail` text, or `Word document` when it has none.
- Any other type: the type string, or `Unknown` when there is none.
- Use `?` for a missing slide, sheet, cell or page.
- For every type except `docx`, when `detail` is set append ` — <detail>`
  (e.g. `Slide 4 — Financial Highlights table, row 2`, `Overview!B12`).

**Freeze panes** at A6, so the title block and header row stay in view.

## Sheet 2: `Summary`

| Cell | Value | Style |
|---|---|---|
| A1 | `Fact-Check Summary` | Title |
| A2 | `Source file: <source_file>` (`Not specified` when missing) | workbook default font |
| A3 | `Total items checked: <number of items>` | workbook default font |
| A5 | `Flag` | Header |
| B5 | `Count` | Header |
| A6–A9 | `Match`, `Stale`, `Mismatch`, `Unable to verify`, in that order | Body, each with its flag's fill |
| B6–B9 | The count for that flag, as a number (0 when none) | Body |

Column widths: A = 20, B = 10. No freeze panes on this sheet.

## After writing

1. Print one line: the output path, the item count, and the count per flag.
2. Reopen the file and check: sheet names are `Audit Log` then `Summary`; row 5 holds the ten
   headers in order; there are as many data rows as items; B6:B9 on `Summary` add up to the
   item count; every `Match`/`Stale`/`Mismatch` row has Source Document, Source URL and As-Of
   Date filled.
