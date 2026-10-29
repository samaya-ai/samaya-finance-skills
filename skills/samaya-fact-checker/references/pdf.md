# PDF — extraction and annotation

## Extraction

If a `pdf-reading` helper skill is available in this environment
(on claude.ai it is at `/mnt/skills/public/pdf-reading/`), read it for inspection approach —
text extraction for text-heavy PDFs, rasterization for scanned/image-heavy ones; otherwise
extract the text with `pdfplumber` (already used by `scripts/annotate_pdf.py`) and rasterize
scanned or image-heavy pages to read them as images. A missing helper skill is never a reason
to stop. Walk the extracted text for:

- Hard numbers (figures, percentages, dollar amounts).
- Dates and periods.
- Named claims — officer names/titles, market-position statements.

For `location`, record `{"type": "pdf", "page": <1-indexed page number>, "detail": "<short
verbatim snippet, under ~10 words>"}`. Both fields matter: `page` selects the page,
and `detail` must be an **exact substring from the page** (not paraphrased) — the annotation
script searches for it via `pdfplumber` to find the annotation's on-page position. A snippet
that doesn't literally appear on the page falls back to a corner placement on the right page,
which is still correct but less precisely anchored.

## Annotation (if the user opted in)

PDF supports genuine sticky-note comment annotations via `pypdf.annotations.Text` — confirmed
working directly (round-trips correctly through save/reopen) while building this skill. Run:
```bash
python scripts/annotate_pdf.py original.pdf data.json annotated.pdf
```
This uses `pdfplumber` to locate each item's `detail` snippet on its page and anchors a sticky
note there via `pypdf`, two-line format:
```
[Match] Original: $391.0 billion | Samaya: $391.04 billion
Source: AAPL FY2024 10-K (2024-11-01), via Samaya. https://www.sec.gov/...
```
It only processes items with `location.type == "pdf"` and reports which items fell back to
corner placement (snippet not found verbatim on the page) — check that list and consider
tightening the `detail` snippet and re-running if too many fell back.
