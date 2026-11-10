# Workbook format — shared by every Samaya Excel skill

How a Samaya workbook looks when no house template is supplied: number formats, type, row
height, sheet setup, alignment and the house palette. `references/samaya-conventions.md` carries
the rules that apply to every deliverable (sourcing, Notes, attention fill, authorship); this file
is the Excel-specific layer on top of it.

## Contents

- WORKBOOK FORMAT — explicit, and applied when there is no template to match
- HOUSE STYLE — subordinate to samaya-brand
- WORKBOOK VALIDATION GATES

## WORKBOOK FORMAT — explicit, and applied when there is no template to match

Where a house template is supplied, match it and do not restyle. **Where there is no template —
which is the common case — apply the standard below.** Falling through to the application's
defaults is not a neutral choice: it produces a 12-point default font, unformatted numbers and
blown-out row heights, and the reader reads that as an unfinished file whatever the numbers say.

**Number formats. No numeric cell is ever left on `General`.** A raw `3551` sitting next to a
formatted `3,551` in the same table is the single most visible defect a workbook can have.

| Content | Format |
| --- | --- |
| Whole currency and units | `#,##0;(#,##0);"—"` |
| Per-share, ratios, one-decimal figures | `#,##0.0;(#,##0.0);"—"` |
| Two-decimal figures (EPS, DPS) | `#,##0.00;(#,##0.00);"—"` |
| Percentages and margins | `0.0%;(0.0%);"—"` |
| Basis-point changes | `+0"bps";-0"bps";"—"` |
| Multiples | `0.0"x"` |
| Dates | `dd mmm yy` |

Negatives in parentheses, never with a minus sign. Zeros as an em dash, never as `0` or blank.
One decimal convention per row, and the same convention for a line and its own growth rate
wherever both appear.

**Type.** Inter throughout at 9 or 10 point for body rows, per the `samaya-brand` styleguide,
which is authoritative. Not the application default face, and not 12 point — 12 point is what
makes a dense financial table look padded and forces the reader to scroll for information that
should fit one screen.

**Row height stays at the default.** Never set a manual height above about 30 points except for
a single title row. Heights of 70 to 90 points, which is what wrapped text produces when it is
allowed to expand, are the main reason a sheet reads as spaced-out and unfinished. Where a long
note or description must appear, put it in a designated notes column with a capped height and let
it clip, or move it to a Note on the cell — never let it inflate the row for every column
beside it.

**Column width to content.** Label columns wide enough for the longest label and no wider;
period columns uniform. A 50-point-wide prose column inside a financial table breaks the grid
for every row it crosses.

**Sheet setup on every sheet written:** gridlines off · zoom 80% · freeze panes at the label
column and the header rows · print area set to the used range · one decimal convention per
sheet stated in the header along with units and currency.

**Alignment.** Numbers right, labels left, period headers right-aligned over their columns and
never centred. Indent sub-lines one level under their parent rather than prefixing them with
dashes.

## HOUSE STYLE — subordinate to samaya-brand

The tokens live in `samaya-brand` and it wins over anything restated here. The spine every
workbook shares: Inter; ink `#181A1E`; muted `#777E85`; Samaya blue `#0019FF` on analyst inputs;
black title bars; gridlines off; charts in Samaya blue, grey and black; negatives in parentheses;
zeros as an em dash; `Samaya AI` on the document properties and every Note. Each skill names its
own fills and banners on top of this and never adds a second attention colour.

Never roundtrip a live or charted host workbook through openpyxl: it drops charts, data
validation and conditional formatting. Write into the open workbook through the host, or into a
copy the analyst has approved.

## WORKBOOK VALIDATION GATES — added to the common gates

- No numeric cell left on General; every number carries its house format, negatives in
  parentheses, zeros as an em dash.
- Inter at 9 or 10 point, not the application default face or size.
- No manual row height above ~30pt except a single title row; long prose in a capped notes
  column or a cell Note, never inflating the row.
- Gridlines off, zoom 80%, freeze panes set, units and currency in the sheet header.
- Every write resolved by row label found at runtime, not by a remembered row number.
