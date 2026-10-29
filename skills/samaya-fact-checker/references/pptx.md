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
`slide` is required — the annotation script uses it directly to find the notes slide. `detail`
should say roughly where on the slide (e.g., "Financial Highlights table, row 2").

## Annotation (if the user opted in) — speaker notes, not visible content

**PPTX has no native comment API reachable from any tool in this environment.** Tested
directly: pptxgenjs, python-pptx, and the Office.js PowerPoint add-in API all lack a
comment-writing capability. Don't attempt to work around this by adding visible superscript
markers or footer legends to someone else's existing deck — that mechanic is for content *we
generate*, not for annotating a deck we didn't create, and it would visibly alter the person's
slide.

Instead, `scripts/annotate_pptx_notes.py` writes each flagged slide's citations into that
slide's **speaker notes** — non-destructive to visible content, and still gives the person a
findable, per-slide citation trail. Multiple flagged items on the same slide are appended as one
block under a `--- Fact-Check Notes ---` header, not overwritten one after another.

Run:
```bash
python scripts/annotate_pptx_notes.py original.pptx data.json annotated.pptx
```
It only processes items with `location.type == "pptx"` — safe to run against the full payload
alongside other formats' annotation scripts.
