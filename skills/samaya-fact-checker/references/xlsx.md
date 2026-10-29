# Excel (.xlsx) — extraction and annotation

## Extraction

If an `xlsx` helper skill is available in this environment
(on claude.ai it is at `/mnt/skills/public/xlsx/`), read it for inspection approach; otherwise
load the workbook read-only with `openpyxl` and walk it directly. A missing helper skill is
never a reason to stop. Either way, walk every sheet's cells for:

- Hardcoded hard numbers (not formulas that derive from other cells already in the workbook —
  those aren't independently checkable facts, they're computed from something else in-file).
- Dates and periods in cell values.
- Named claims in text cells (officer names, market-position statements).

For `location`, record `{"type": "xlsx", "sheet": "<exact sheet name>", "cell": "<e.g. B12>"}`.
Both fields are required — the annotation script looks up the sheet by exact name and writes
the comment to that specific cell.

## Annotation (if the user opted in)

Excel supports genuine cell comments via openpyxl, same discipline as the Word/PDF comment
mechanic. Run:
```bash
python scripts/annotate_xlsx.py original.xlsx data.json annotated.xlsx
```
This attaches an `openpyxl.comments.Comment` to each flagged cell (author: "Fact-Checker"),
two-line format:
```
[Match] Original: $391.0 billion | Samaya: $391.04 billion
Source: AAPL FY2024 10-K (2024-11-01), via Samaya. https://www.sec.gov/...
```
It only processes items with `location.type == "xlsx"` and skips (reporting) any item whose
sheet name or cell reference doesn't resolve — check the printed skip list before declaring the
annotation pass complete.
