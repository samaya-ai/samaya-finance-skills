# PowerPoint (.pptx) — extraction and annotation

## Extraction

If a `pptx` helper skill is available in this environment
(on claude.ai it is at `/mnt/skills/public/pptx/`), read it for how to inspect a deck's
content; otherwise open the deck with `python-pptx` and walk it directly. A missing helper
skill is never a reason to stop. Walk every slide's text frames, tables, and chart data
labels for:

- Hard numbers in body text, tables, and chart labels/data.
- Dates and periods.
- Named claims — officer names/titles, market-position statements.

For `location`, record `{"type": "pptx", "slide": <1-indexed slide number>, "detail": "..."}`.
`slide` is required — the annotation helper uses it directly to find the notes slide. `detail`
should say roughly where on the slide (e.g., "Financial Highlights table, row 2").

## Annotation (if the user opted in) — speaker notes, not visible content

**PPTX has no native comment API reachable from any tool in this environment.** Tested
directly: pptxgenjs, python-pptx, and the Office.js PowerPoint add-in API all lack a
comment-writing capability. Don't attempt to work around this by adding visible superscript
markers or footer legends to someone else's existing deck — that mechanic is for content *we
generate*, not for annotating a deck we didn't create, and it would visibly alter the person's
slide.

Instead, write each flagged slide's citations into that slide's **speaker notes** —
non-destructive to visible content, and still gives the person a findable, per-slide citation
trail. Multiple flagged items on the same slide are appended as one block under a
`--- Fact-Check Notes ---` header, not overwritten one after another.

Write a helper in your working folder that does the following, then run it.

1. Open the original with `pptx.Presentation(path)`.
2. For each item in payload order, skip it unless `location.type` is `pptx`. Skip and record
   the `id` when `slide` is missing, below 1 or above the number of slides. Group the rest by
   slide number, keeping payload order within each slide.
3. For each slide with items, get `slide.notes_slide` (python-pptx creates the notes slide if
   the slide has none) and its `notes_text_frame`.
4. Leave the existing notes exactly as they are and append, as new paragraphs at the end:
   - when the notes are empty, keep their single empty paragraph as the first line and write
     the header into a new paragraph after it; when notes already exist, add no blank
     paragraph — the header goes directly after the last existing paragraph,
   - a paragraph reading `--- Fact-Check Notes ---`,
   - one paragraph per item, using the PowerPoint speaker-notes line in
     `references/audit-schema.md` ("Annotation text").

   Append paragraphs (`add_paragraph()`) rather than reassigning `text_frame.text`, which would
   flatten the formatting of the author's own notes. Apply one block per slide per run — if you
   rerun on an already annotated output, start again from the original file.
5. Do not touch any shape on the slide itself.
6. Save to a new file (e.g. `annotated.pptx`).
7. Print the output path, the number of note lines written, the number of slides they went to,
   and the IDs skipped for an invalid or missing slide number.

**Check before delivering.** Reopen the output with `python-pptx`; for each flagged slide,
confirm its notes still begin with the original notes text, contain exactly one
`--- Fact-Check Notes ---` line, and have one line per item for that slide. Confirm the slide
count and every slide's visible text are unchanged from the original.
