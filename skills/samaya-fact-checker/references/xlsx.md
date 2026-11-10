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
Both fields are required — the annotation helper looks up the sheet by exact name and writes
the comment to that specific cell.

## Annotation (if the user opted in)

Excel supports genuine cell comments via `openpyxl`, same discipline as the Word/PDF comment
mechanic. Write a helper in your working folder that does the following, then run it.

1. Load the original with `openpyxl.load_workbook(path)` — not read-only, not `data_only`, so
   formulas survive. For a macro workbook (`.xlsm`) pass `keep_vba=True` and keep the `.xlsm`
   extension on the output.
2. For each item in payload order, skip it unless `location.type` is `xlsx`.
3. Skip and record the item's `id` when `sheet` or `cell` is missing, when no sheet has exactly
   that name (case and spaces count), or when `cell` is not a valid single-cell reference.
4. Otherwise attach `openpyxl.comments.Comment(text, "Fact-Checker")` to that cell. The author
   is always `Fact-Checker`; leave the comment box at openpyxl's default size. The text is the
   Excel/PDF annotation text in `references/audit-schema.md` ("Annotation text"): the verdict
   line, then the source line and the URL line (Excel comments are plain text, so the URL
   cannot hide behind a `link`). `Unable to verify` items get the verdict line only.
5. If the cell already carries a comment (the author's own, or an earlier item on the same
   cell), keep that text and add the new text below it after a blank line, rather than
   replacing it.
6. Save to a new file (e.g. `annotated.xlsx`); never overwrite the original.
7. Print the output path, the number of comments written, and the skipped IDs with the reason
   (`missing/invalid sheet or cell`). Check that list before declaring the annotation pass
   complete.

**Check before delivering.** Reopen the output with `openpyxl` and confirm that every
non-skipped item's cell has a comment whose text contains its verdict line, with author
`Fact-Checker`. `openpyxl` does not carry over everything it cannot read (images, charts,
some form controls and pivot caches): if the original had any of these, compare the two
workbooks, and if anything is lost tell the user and offer the audit log on its own instead.
