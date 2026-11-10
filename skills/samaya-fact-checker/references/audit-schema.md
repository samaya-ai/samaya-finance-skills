# Audit item schema

Every extracted quantitative fact, date/period, or named claim becomes one audit item.
Assemble these into a single JSON payload (`data.json` in your working folder) as you go (don't
hold them all in memory until the end) — this same payload drives every helper you write: the
audit log (`references/audit-log.md`) and the annotation pass for the source format.

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
      "location": {"type": "docx", "paragraph": 9, "detail": "Page 2, paragraph 3"},
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
  and determines which annotation helper (if any) acts on this item.
  - `docx`: `paragraph` (0-based index of the body paragraph holding the value, counting every
    `w:p` in `w:body` of `word/document.xml` in document order) — record it at extraction; the
    comment anchors on the first occurrence of `original_value` inside that paragraph, or on the
    first occurrence in the document when it is absent (see `references/docx.md`). `detail` is
    a free-text page/paragraph/section description, used in the audit log only.
  - `pptx`: `slide` (1-indexed integer) is required; `detail` is free text.
  - `xlsx`: `sheet` and `cell` (e.g. `"B12"`) are both required.
  - `pdf`: `page` (1-indexed integer) is required; `detail` should include a short verbatim
    snippet (under 10 words) so the PDF helper can locate it on the page.
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

## Annotation text

The Excel comment, the PDF sticky note, the PowerPoint notes line and the Word comment are
built from the item's fields by fixed rules, so every annotation reads the same way. The Word
comment uses the Excel/PDF verdict and source lines below, with a `link` hyperlink in place of
the URL line (see `references/docx.md`). In the rules below, a field
that is missing or `null` counts as an empty string, and the dash is an em dash with a space on
each side (` — `).

**Short note.** Take `note`, trim surrounding whitespace, strip every trailing period, and
lower-case its first character. If `note` is empty the short note is empty.

### Excel comment and PDF sticky note (identical text)

1. **Verdict line.**
   - `Unable to verify`: `Unable to verify — <short note>`; when the short note is empty, use
     `no Samaya route for this claim` in its place. This line is the whole annotation — no
     source lines follow.
   - `Match`: `Match — <samaya_value>`, or `<original_value>` when `samaya_value` is empty.
   - `Stale` / `Mismatch`: `<flag> — doc: <original_value> | now: <samaya_value>`.
   - For `Match`, `Stale` and `Mismatch`, when the short note is not empty append
     `; <short note>` to the verdict line.
2. **Source line** (second line): `<source_doc>`, or `Not disclosed` when empty, followed by
   ` (<as_of_date>)` only when `as_of_date` is set.
3. **URL line** (third line): `<source_url>`, or `no link returned` when empty.

Lines are joined with a single newline. Examples:

```
Match — $391.04 billion; rounding only — within materiality threshold
AAPL FY2024 10-K (2024-11-01)
https://www.sec.gov/...
```

```
Unable to verify — subjective/qualitative claim; no disclosed metric to check against
```

### PowerPoint speaker-notes line (one line per item)

The notes pane lists several items together, so each line also names the item's `description`
and keeps the source on the same line:

- `Unable to verify`: `Unable to verify — <description>: <short note>`, with
  `no Samaya route for this claim` when the short note is empty. Nothing follows.
- `Match`: `Match — <description>: <samaya_value or original_value>`.
- `Stale` / `Mismatch`: `<flag> — <description>: doc <original_value> | now <samaya_value>`
  (no colons after `doc` and `now` here).
- For those three, append `; <short note>` when it is not empty, then `. `, then the source
  document (or `Not disclosed`), then ` (<as_of_date>)` when set, then a space and the URL (or
  `no link returned`).

Example:

```
Mismatch — Current CFO named: doc Luca Maestri | now Kevan Parekh; named individual left the role; deck was not updated. AAPL 8-K (Nov 2024 CFO transition) (2025-01-01) https://www.sec.gov/...
```
