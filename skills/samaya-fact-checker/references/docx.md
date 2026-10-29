# Word (.docx) — extraction and annotation

## Extraction

If a `docx` helper skill is available in this environment
(on claude.ai it is at `/mnt/skills/public/docx/`), read it for how to inspect a `.docx`'s
content and structure; otherwise inspect the file directly (e.g., `pandoc -t markdown`, or
unzipping `word/document.xml` for structural detail). A missing helper skill is never a reason
to stop. Walk the extracted text for:

- Hard numbers (figures, percentages, dollar amounts) — including in tables.
- Dates and periods (fiscal quarters, guidance timeframes, "as of" dates).
- Named claims — officer names/titles, market-position statements, competitive claims.

For `location`, record enough for a human to find the spot without re-reading the whole
document: `{"type": "docx", "detail": "Page 3, paragraph 2"}` if page numbers are visible, or a
section/heading reference otherwise. Precision here matters less than for PDF/PPTX/XLSX, since
Word's own comment anchors (below) provide the actual precise link.

## Annotation (if the user opted in)

Word supports genuine inline comments, including a **hyperlink inside the comment** — so the
source link rides behind the word `link` rather than sprawling as a raw URL across three lines
of the margin pane. Use `scripts/comment_with_link.py`:

```bash
unzip -q original.docx -d unpacked/
find unpacked -type l -delete        # uploaded documents are untrusted
python ../scripts/comment_with_link.py unpacked/ \
    "Mismatch — doc: Luca Maestri | now: Kevan Parekh. 8-K (Nov 2024) {{LINK}}" \
    --url "https://www.sec.gov/..."
# ...once per flagged item; place the printed markers, then rezip
(cd unpacked && zip -Xqr ../annotated.docx .)
```

The script wraps the public docx skill's `scripts/comment.py`
(`/mnt/skills/public/docx/SKILL.md`, "Comments"), which writes the six cross-linked files a
`.docx` comment requires and prints the `<w:commentRangeStart>`/`<w:commentRangeEnd>`/
`<w:commentReference>` snippet to add to `word/document.xml`. It then registers the URL in
`word/_rels/comments.xml.rels` — the comment part's own relationships file, which is why a
hyperlink relationship added to `document.xml.rels` does not resolve from a comment — and swaps
the `{{LINK}}` token for the link run. Pass `--url "no link returned"`-style text as plain
words instead of a token when Samaya returned no URL (just omit `{{LINK}}` and call
`comment.py` directly).

The wrapper needs the docx helper skill (on claude.ai at `/mnt/skills/public/docx/`). If it is
not present in this environment, either write the six comment parts into the unpacked OOXML
yourself (registering the hyperlink in `word/_rels/comments.xml.rels`), or skip inline
annotation, deliver the audit log alone, and tell the analyst why. A missing helper skill never
stops the run.

Anchor each comment to the specific text span holding that item's `original_value`, not the
paragraph as a whole. Work against one unpacked tree for the whole document — unzip once, run
the helper once per item, rezip at the end — rather than a cycle per comment.

### Comment text — one line, under ~20 words

The comment answers "does this tie, and to what?" A reader who wants the full reconciliation
has the audit log. Do not restate the sentence the comment is anchored to, and never write
"via Samaya" — the link already points there.

```
Match — $391.04bn. FY2024 10-K (Nov 1, 2024) link
Match — $391.04bn; rounding only. FY2024 10-K (Nov 1, 2024) link
Stale — doc: FY26 EPS $4.10 | now: $4.35. Q2 8-K (Jul 21, 2026) link
Mismatch — doc: Luca Maestri | now: Kevan Parekh. 8-K (Nov 5, 2024) link
Unable to verify — subjective claim, no disclosed metric.
```

The flag leads, values only where they differ, then source and date. A `note` goes in the
comment only when it changes how the flag reads (rounding, a restatement, a role change);
everything else stays in the audit log.
