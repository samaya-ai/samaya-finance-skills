# PDF — extraction and annotation

## Extraction

If a `pdf-reading` helper skill is available in this environment
(on claude.ai it is at `/mnt/skills/public/pdf-reading/`), read it for inspection approach —
text extraction for text-heavy PDFs, rasterization for scanned/image-heavy ones; otherwise
extract the text with `pdfplumber` (the same library the annotation helper uses to find
snippets) and rasterize scanned or image-heavy pages to read them as images. A missing helper
skill is never a reason to stop. Walk the extracted text for:

- Hard numbers (figures, percentages, dollar amounts).
- Dates and periods.
- Named claims — officer names/titles, market-position statements.

For `location`, record `{"type": "pdf", "page": <1-indexed page number>, "detail": "<short
verbatim snippet, under ~10 words>"}`. Both fields matter: `page` selects the page,
and `detail` must be an **exact substring from the page** (not paraphrased) — the annotation
helper searches for it with `pdfplumber` to find the note's on-page position. A snippet
that doesn't literally appear on the page falls back to a corner placement on the right page,
which is still correct but less precisely anchored.

## Annotation (if the user opted in)

PDF supports genuine sticky-note comment annotations via `pypdf.annotations.Text`, which
round-trip correctly through save and reopen. Write a helper in your working folder that does
the following, then run it.

1. Open the original twice: with `pdfplumber` (to find word positions) and with
   `pypdf.PdfReader`. Create a `pypdf.PdfWriter` and copy the whole document into it with
   `writer.append(reader)`. If the PDF is encrypted and will not open, stop annotating, deliver
   the audit log alone and say why.
2. For each item in payload order, skip it unless `location.type` is `pdf`. Skip and record the
   `id` when `page` is missing, below 1 or above the page count.
3. **Find the anchor** on that page (`pdfplumber` page `page - 1`):
   - Lower-case `detail`, trim it and split it on whitespace into tokens. If there are no
     tokens, there is no anchor.
   - List the page's words with `extract_words()` (default settings), in the order returned.
     Try these in order and stop at the first that finds a word; its box (`x0`, `x1`, `top`,
     `bottom`) is the anchor:
     1. **Full snippet.** The first run of consecutive words whose lower-cased texts equal the
        tokens one for one. The anchor is the first word of that run.
     2. **First token.** The first word whose lower-cased text contains the first token.
     3. Otherwise there is no anchor (corner fallback below).
   - `pdfplumber` measures from the top-left; PDF annotations measure from the bottom-left.
     With `H` the `pdfplumber` page height, the note rectangle is
     `(x0, H - bottom, x1, H - top)`.
   - **Fallback** when there is no anchor: a 20-point square near the top-left corner,
     `(10, H - 30, 30, H - 10)`. Record the item's `id` as placed at the corner.
4. Build the note with `pypdf.annotations.Text(text=<annotation text>, rect=<rect>)`, using the
   Excel/PDF annotation text in `references/audit-schema.md` ("Annotation text"): verdict line,
   source line, URL line (`Unable to verify`: verdict line only). Leave it closed (the default).
   Set the note's author (its `/T` entry) to `Fact-Checker`.
5. Add it with `writer.add_annotation(page_number=page - 1, annotation=note)`. Several items on
   one page each get their own note; existing annotations in the file stay as they are.
6. Write the output to a new file (e.g. `annotated.pdf`).
7. Print the output path, the number of notes added, the IDs skipped for a bad page number, and
   the IDs placed at the page corner because the snippet was not found. Check the corner list:
   if many items fell back, tighten their `detail` snippets to text that appears verbatim on the
   page and rerun.

**Check before delivering.** Reopen the output with `pypdf` and count `/Text` annotations
(`/Subtype` `/Text`) per page; each page must have its original count plus one per item placed
on it. Read back two or three notes' `/Contents` against the payload.
