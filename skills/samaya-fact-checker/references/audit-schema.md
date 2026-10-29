# Audit item schema

Every extracted quantitative fact, date/period, or named claim becomes one audit item.
Assemble these into a single JSON payload as you go (don't hold them all in memory until the
end) — this same payload drives every downstream script.

```json
{
  "source_file": "Q2_Investor_Deck.pptx",
  "items": [
    {
      "id": "1",
      "description": "FY2024 total revenue",
      "original_value": "$391.0 billion",
      "location": {
        "type": "pptx",
        "slide": 4,
        "detail": "Financial Highlights table, row 2"
      },
      "samaya_value": "$391.04 billion",
      "source_doc": "AAPL FY2024 10-K",
      "source_url": "https://www.sec.gov/...",
      "as_of_date": "2024-11-01",
      "flag": "Match",
      "note": "Rounding only — within materiality threshold."
    },
    {
      "id": "2",
      "description": "Current CFO named",
      "original_value": "Luca Maestri",
      "location": {"type": "docx", "detail": "Page 2, paragraph 3"},
      "samaya_value": "Kevan Parekh",
      "source_doc": "AAPL 8-K (Nov 2024 CFO transition)",
      "source_url": "https://www.sec.gov/...",
      "as_of_date": "2025-01-01",
      "flag": "Mismatch",
      "note": "Named individual left the role; deck was not updated."
    },
    {
      "id": "3",
      "description": "\"Market leader in premium smartphones\" claim",
      "original_value": "Market leader in premium smartphones",
      "location": {"type": "xlsx", "sheet": "Overview", "cell": "B12"},
      "samaya_value": null,
      "source_doc": null,
      "source_url": null,
      "as_of_date": null,
      "flag": "Unable to verify",
      "note": "Subjective/qualitative claim; no disclosed metric to check against."
    }
  ]
}
```

## Field notes

- **`location.type`** is one of `docx`, `pptx`, `xlsx`, `pdf` — matches the source file format,
  and determines which annotation script (if any) can act on this item.
  - `docx`: free-text location description (page/paragraph/section) — used in the audit log
    only; the actual comment anchor for `comment.py` is a text string to search for.
  - `pptx`: `slide` (1-indexed integer) is required; `detail` is free text.
  - `xlsx`: `sheet` and `cell` (e.g. `"B12"`) are both required.
  - `pdf`: `page` (1-indexed integer) is required; `detail` should include a short verbatim
    snippet (under 10 words) so `annotate_pdf.py` can locate it on the page.
- **`flag`** is exactly one of `Match`, `Stale`, `Mismatch`, `Unable to verify`. Nothing else.
  - `Match` — value ties to the Samaya-sourced figure. Fold immaterial rounding differences
    into `Match` with a note; don't create a separate rounding category.
  - `Stale` — value was accurate as of an earlier period but has since been superseded/restated
    (e.g., a since-departed officer, a since-revised guidance figure).
  - `Mismatch` — value does not tie to the Samaya-sourced figure and isn't explained by staleness.
  - `Unable to verify` — no Samaya route exists for this claim (subjective claims, undisclosed
    figures, or every route returned nothing). Never force a flag here into Match or Mismatch.
- **`samaya_value` / `source_doc` / `source_url` / `as_of_date`** are `null` together only when
  `flag` is `Unable to verify`. Every other flag requires all four populated — no partial
  citations.
- **Never invent a `source_url`.** Use the exact URL Samaya's `references` returned. If Samaya
  returned no URL for an otherwise-confirmed source, write `"no link returned"` as the value
  rather than leaving it null or fabricating one.
