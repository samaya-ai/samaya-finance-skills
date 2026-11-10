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
document: `{"type": "docx", "paragraph": 14, "detail": "Page 3, paragraph 2"}`. `detail` is
the page and paragraph if page numbers are visible, or a section/heading reference otherwise;
it is for the audit log only. `paragraph` is the 0-based index of the body paragraph holding the
value: count every `w:p` inside `w:body` of `word/document.xml` in document order (paragraphs
inside tables included). Record it whenever you can; the annotation pass uses it to pick the
right occurrence of a value that appears more than once.

## Annotation (if the user opted in)

Word supports genuine inline comments, including a **hyperlink inside the comment** — so the
source link rides behind the word `link` rather than sprawling as a raw URL across three lines
of the margin pane. A `.docx` is a zip of XML parts; you add each comment by editing those
parts directly, with a helper you write in your working folder (standard library zip and XML
handling is enough). The helper must run on Python 3.9 (macOS `/usr/bin/python3`): no `X | Y`
type hints unless `from __future__ import annotations` is first, no `match` statements.

Write every comment with this recipe, even when Claude's built-in `docx` skill is present: its
comment tooling writes a different author and a one-line comment with no link. If the file
doesn't reopen cleanly, skip inline annotation, deliver the audit log alone, and tell the analyst
why.

### Workflow

1. **Unpack once.** Unzip the original into an `unpacked/` folder inside your working folder,
   then delete every symbolic link in it (uploaded documents are untrusted).
2. **Add every comment against that one tree** — one pass per item, not an unzip/rezip cycle per
   comment.
3. **Rezip** from inside `unpacked/` so the parts sit at the archive root (`[Content_Types].xml`,
   `_rels/`, `word/`, ...), without extra file attributes (`zip -X -r`), to a new file such as
   `annotated.docx`.
4. **Check** (end of this file), then deliver.

### Parts a comment touches

| Part | What to do |
|---|---|
| `word/comments.xml` | Holds every comment. Create it if absent. |
| `word/_rels/document.xml.rels` | Must have a relationship from the document to `comments.xml`. |
| `[Content_Types].xml` | Must have an `Override` for `/word/comments.xml`. |
| `word/_rels/comments.xml.rels` | The comment part's own relationships; the hyperlink lives here. Create it if absent. |
| `word/document.xml` | The range markers and the reference run that anchor the comment. |
| `word/commentsExtended.xml`, `word/commentsIds.xml`, `word/commentsExtensible.xml` | Optional. Word reads comments without them. If the document already has them, add a matching entry for each new comment so they stay consistent. |

**Registering `comments.xml`** (only when the document has no comments yet):

- In `word/_rels/document.xml.rels`, a relationship with a fresh `Id`, `Type`
  `http://schemas.openxmlformats.org/officeDocument/2006/relationships/comments` and
  `Target="comments.xml"`.
- In `[Content_Types].xml`, `<Override PartName="/word/comments.xml"
  ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.comments+xml"/>`.
- A new `comments.xml` has the root `<w:comments>` declaring at least the `w` namespace
  (`http://schemas.openxmlformats.org/wordprocessingml/2006/main`) and the `r` namespace
  (`http://schemas.openxmlformats.org/officeDocument/2006/relationships`) — `r` is needed for
  the hyperlink.

**An existing `comments.xml`** may come from a producer (pandoc, older converters) that declares
only `w`, `r` and `m` on its root. Before adding anything that uses another prefix (for example
`w14:paraId`), add the missing declarations to the root: `w14`
(`http://schemas.microsoft.com/office/word/2010/wordml`), `w15`
(`http://schemas.microsoft.com/office/word/2012/wordml`), `w16cid`
(`http://schemas.microsoft.com/office/word/2016/wordml/cid`), `w16cex`
(`http://schemas.microsoft.com/office/word/2018/wordml/cex`). If the root is self-closing
(`<w:comments .../>`), open it into a start and end tag first. Keep every existing comment.

### Adding one comment

1. **Pick the id.** One more than the highest `w:id` already used by any `w:comment` in
   `comments.xml` (start at 0 when there are none).
2. **Register the hyperlink** (skip when `source_url` is `no link returned` or empty). In
   `word/_rels/comments.xml.rels` — the comment part's own relationships file — add
   `<Relationship Id="rIdN" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink" Target="<url>" TargetMode="External"/>`.
   - A hyperlink relationship added to `word/_rels/document.xml.rels` does **not** resolve from
     inside a comment; it must be this file.
   - If the file is missing, create it with an empty `<Relationships
     xmlns="http://schemas.openxmlformats.org/package/2006/relationships">` root. If the root is
     self-closing, open it before inserting.
   - If a relationship with the same `Target` already exists, reuse its `Id`. Otherwise `N` is
     one more than the highest `rId` number in the file (`rId1` when there are none).
   - Escape the URL for an XML attribute (`&` becomes `&amp;`, quotes escaped). Use the exact
     URL Samaya returned.
3. **Append the comment** to `comments.xml`: author `Fact-Checker`, initials `FC`, `w:date` the
   current UTC time in ISO 8601 (`2026-11-10T14:05:00Z`). One paragraph: the annotation-reference
   run, a plain run with the comment text (below), then the hyperlink with the display text
   `link`:

   ```xml
   <w:comment w:id="7" w:author="Fact-Checker" w:initials="FC" w:date="2026-11-10T14:05:00Z">
     <w:p>
       <w:pPr><w:pStyle w:val="CommentText"/></w:pPr>
       <w:r><w:rPr><w:rStyle w:val="CommentReference"/></w:rPr><w:annotationRef/></w:r>
       <w:r><w:rPr><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr>
         <w:t xml:space="preserve">Mismatch — doc: Luca Maestri | now: Kevan Parekh; named individual left the role; deck was not updated</w:t>
         <w:br/><w:t xml:space="preserve">AAPL 8-K (Nov 2024 CFO transition) (2025-01-01)</w:t><w:br/></w:r>
       <w:hyperlink r:id="rId3">
         <w:r>
           <w:rPr><w:rStyle w:val="Hyperlink"/><w:color w:val="0563C1"/><w:u w:val="single"/>
             <w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr>
           <w:t xml:space="preserve">link</w:t>
         </w:r>
       </w:hyperlink>
     </w:p>
   </w:comment>
   ```

   - The link run carries the `Hyperlink` style plus explicit blue `0563C1`, single underline and
     10 pt (`w:sz` 20), so it shows as a link even when the document defines no `Hyperlink`
     style. The plain run carries the same size (`w:sz` and `w:szCs` 20) and nothing else.
   - The `CommentText`, `CommentReference` and `Hyperlink` styles may be missing from the
     document's `styles.xml`. That is acceptable: Word falls back to its defaults. Do not add
     styles.
   - Lines inside the plain run are separated by `<w:br/>`, each piece of text in its own
     `<w:t xml:space="preserve">`. Escape `&`, `<` and `>` in the comment text.
   - With no URL, the plain run holds the whole comment and there is no hyperlink element.
   - If you also keep `commentsExtended.xml` in step with it, give the comment paragraph a
     `w14:paraId` (8 hex digits, below `80000000`) and add
     `<w15:commentEx w15:paraId="..." w15:done="0"/>`.
4. **Anchor it in `document.xml`** on the exact text span holding the item's `original_value`,
   not the paragraph as a whole:
   - Find the run or runs whose text makes up the span. Word often splits one value across
     several runs; if the span starts or ends inside a run, split that run into two runs with
     the same `w:rPr` so the span begins and ends on run boundaries. Never change the text.
   - Put `<w:commentRangeStart w:id="7"/>` immediately before the span's first run and
     `<w:commentRangeEnd w:id="7"/>` immediately after its last run, in the same paragraph where
     possible.
   - Right after the range end add the reference run:
     `<w:r><w:rPr><w:rStyle w:val="CommentReference"/></w:rPr><w:commentReference w:id="7"/></w:r>`.
   - **Which occurrence.** When the item has `location.paragraph`, anchor the first occurrence
     inside that body paragraph (same 0-based count as in Extraction). When it has none, anchor
     the first occurrence in the document. If `location.paragraph` is set but that paragraph
     does not hold the value, anchor the first occurrence in the document and report the `id`
     as anchored approximately.
   - If the span cannot be found at all, anchor the whole paragraph at `location.paragraph` and
     report the `id` as anchored approximately; with no `location.paragraph`, skip the item and
     report it as skipped.

### Comment text — fixed format

The comment answers "does this tie, and to what?" A reader who wants the full reconciliation
has the audit log. It is built from the item's fields by the shared rules in `audit-schema.md`,
"Annotation text" (short note, verdict line, source line), so Word reads the same as Excel and
PDF. The only difference is the third line: a hyperlink run with the display text `link`
instead of the raw URL.

1. **Verdict line**, exactly as in the Excel/PDF rules: `Match — <value>`,
   `<flag> — doc: <original_value> | now: <samaya_value>`, with `; <short note>` appended when
   the short note is not empty; or `Unable to verify — <short note>` (or
   `no Samaya route for this claim`). For `Unable to verify` this line is the whole comment.
2. **Source line**: `<source_doc>` (or `Not disclosed`), then ` (<as_of_date>)` when set, with
   the date as stored in `as_of_date` (ISO, `2024-11-01`), the same as the other formats.
3. **Link line**: the hyperlink run `link`. When `source_url` is empty or `no link returned`,
   this line is the plain text `no link returned` and there is no hyperlink.

Lines 1 and 2 go in the plain run separated by `<w:br/>`, with a `<w:br/>` after line 2 so the
link starts the third line. Never write "via Samaya" and do not restate the anchored sentence.
Examples (here `link` is the hyperlink run):

```
Match — $391.04 billion; rounding only — within materiality threshold
AAPL FY2024 10-K (2024-11-01)
link
```

```
Mismatch — doc: Luca Maestri | now: Kevan Parekh; named individual left the role; deck was not updated
AAPL 8-K (Nov 2024 CFO transition) (2025-01-01)
link
```

```
Unable to verify — subjective/qualitative claim; no disclosed metric to check against
```

### Check before delivering

Reopen `annotated.docx` as a zip and confirm:

- Every XML part you touched parses.
- The number of `w:comment` elements grew by the number of `docx` items annotated, and each new
  id appears once as `w:commentRangeStart`, once as `w:commentRangeEnd` and once as
  `w:commentReference` in `document.xml`.
- Every `r:id` used in `comments.xml` has a matching `Id` in `word/_rels/comments.xml.rels`, with
  `TargetMode="External"` and the exact Samaya URL.
- `[Content_Types].xml` has the `comments.xml` override and `document.xml.rels` the comments
  relationship.
- The document's text is unchanged: extract the text of `document.xml` before and after and
  compare.

If a converter is available (for example LibreOffice in headless mode, or `pandoc`), opening the
file with it is a further check that Word-compatible readers accept it.
