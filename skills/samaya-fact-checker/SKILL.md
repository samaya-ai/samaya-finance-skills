---
name: samaya-fact-checker
description: >-
  "fact-check this deck", "audit this 10-K summary", "can you verify the numbers in this doc",
  "double-check this workbook against the filings", "does this presentation still hold up" —
  verifies every figure, date and named claim in an existing Word, PDF, PowerPoint or Excel file
  against Samaya and writes an Excel audit log. Verification only; it does not write new
  content.
---

# Fact-Checker

Extract every checkable quantitative fact, date/period, and named claim from an uploaded
document, verify each against Samaya-sourced data, and produce an audit log Excel workbook.
Optionally annotate the original file in place with citation comments.

This is a **verification** skill: it never edits the substance of the source document (numbers,
claims, structure) and never adds new content beyond citations. It only checks and annotates.

## HOUSE LANGUAGE — shared, and it governs every line of output

Read `references/samaya-house-language.md` before writing any output: no sayings, no "X, not Y",
no metaphors, the ordinary word rather than the academic one, answers scored against the question
asked without grading the answerer, signs not words, and the materiality pass before handing back.
The worked examples in that file are the operative version of these rules.

## Preflight (confirm before extracting)

1. **Identify the file and format.** If more than one file is attached, confirm which one to
   check. Route to the matching reference file for extraction/annotation mechanics:
   `references/docx.md`, `references/pptx.md`, `references/xlsx.md`, `references/pdf.md`.
2. **Confirm Samaya is connected.** Every verification routes through the Samaya MCP. If the
   connector is not available, say so and stop — do not verify from web search or memory alone.
3. **Ask once, upfront, whether to also annotate the original file** with inline citations, in
   addition to the audit log (which is always produced). Word, Excel, and PDF support genuine
   inline comments; PowerPoint gets citations written into each flagged slide's speaker notes
   instead (no native PPTX comment API is reachable from any tool in this environment — see
   `references/pptx.md`). Make this an upfront yes/no, not a per-item prompt.

## Build order

1. **Extract.** Read the document per its format (see the matching reference file) and pull out
   every quantitative fact, date/period, and named/qualitative claim, each with a `description`,
   `original_value`, and precise `location` (page/paragraph for Word, slide # for PowerPoint,
   sheet+cell for Excel, page # + a short verbatim snippet for PDF). Assemble this list in a
   working JSON payload as you go — this is the same payload every downstream script consumes
   (see `references/audit-schema.md` for the exact shape).
2. **Cluster and verify via Samaya.** Group items by (company, source document) — related facts
   from the same filing go in **one** Samaya query as a compound question; unrelated clusters
   (different companies, different documents, unrelated topics) go as separate calls. Do not
   combine unrelated clusters into one query, and do not fire one query per literal fact when
   several facts trace to the same document. See "Sourcing" below for routing by data type.
3. **Flag each item** — exactly one of `Match`, `Stale`, `Mismatch`, `Unable to verify` (see
   `references/audit-schema.md` for what each means; fold immaterial rounding differences into
   `Match` rather than treating them as their own category).
4. **Build the audit log:**
   ```bash
   python scripts/build_audit_log.py data.json audit_log.xlsx
   ```
5. **If the user opted into inline annotation**, run the script matching the source format:
   ```bash
   # Excel source
   python scripts/annotate_xlsx.py original.xlsx data.json annotated.xlsx
   # PDF source
   python scripts/annotate_pdf.py original.pdf data.json annotated.pdf
   # PowerPoint source (writes to speaker notes, not visible slide content)
   python scripts/annotate_pptx_notes.py original.pptx data.json annotated.pptx
   # Word source — unzip once, then run this per item, then rezip (see references/docx.md):
   python scripts/comment_with_link.py unpacked/ "<one-line comment> {{LINK}}" --url "<source URL>"
   #   Needs the `docx` helper skill; without it, write the OOXML comment parts directly or
   #   deliver the audit log alone and say why. A missing helper skill never stops the run.
   ```
   Each annotation script silently skips items whose `location.type` doesn't match that format,
   so it's safe to run against the full payload.

   Annotations are short by design — one verdict line (flag, then values only where they
   differ), then the source document and date. They don't restate the anchored text and never
   say "via Samaya." In Word the URL hides behind the word `link`; in Excel and PDF, whose
   comments are plain text, it goes on its own line. The full reconciliation lives in the audit
   log, not in the margin. See `references/docx.md` for the exact shapes.
6. **Deliver** the audit log (always) plus the annotated file (if opted in). Summarize counts by
   flag in chat (e.g., "14 Match, 2 Stale, 3 Mismatch, 1 Unable to verify").

## Sourcing — route by data type, not by habit

| Claim type | Route |
|---|---|
| Reported actuals, segment/financial figures, guidance language, management facts | Company filings & transcripts via Samaya (10-K/10-Q/8-K/20-F/6-K/proxy/annual report/earnings call) |
| Forward estimates / street consensus | The consensus provider the document names, or what Samaya can reach for the name, with its as-of date — never a single broker's estimate presented as consensus |
| Price or any single point-in-time market figure | Market data via Samaya, stated as-of a date |
| Named officers/executives | Latest proxy statement, 10-K, or 8-K via Samaya |
| Ownership | Latest 13F/13D filings via Samaya |
| Market-position / competitive claims ("market leader", "largest provider") | Check against the most recent disclosed market-share or ranking data via Samaya if it exists; otherwise flag `Unable to verify` — do not treat an un-sourceable qualitative claim as a `Mismatch` |
| Recent events / news | Most recent filings and press releases via Samaya, not a newswire aggregator |

Never invent a route not on this list, and never cite a newswire summary of a number when a
filing is the source. If every Samaya route returns nothing for a claim, flag `Unable to
verify` — don't force a verdict.

## Querying Samaya

Send the query as a **single `financial_qa` call per (company, source document) cluster** —
Samaya handles multi-fact, compound questions about one company/document well on its own, so
don't split a cluster into one call per fact. Only split into separate calls when clusters are
genuinely independent (different companies, different unrelated documents) — run those as
separate calls with a fresh `session_id` each, not combined into one mega-query that would blur
which returned figure supports which original claim.

Use the exact document title and URL Samaya's `references` return for the audit log's Source
Document / Source URL columns — never assemble a URL from a pattern or invent one. If Samaya
returns no URL for an otherwise-confirmed source, write `"no link returned"`, not a guess.

## Guardrails (non-negotiable)

1. Use only disclosed or Samaya-retrieved information to verify claims — no memory-based
   figures, dates, or officeholders standing in for a real check.
2. Never render a verdict as an investment recommendation or valuation opinion — a flag reports
   whether a stated fact ties to a disclosed source, nothing more.
3. Never fabricate a source document, date, or URL. `Unable to verify` is always the correct
   flag when no real source was found — never a guessed `Match`.
4. Never alter the substance of the original document — no correcting the number in place, no
   rewriting claims. Verification and citation only; the person decides what to fix.
5. Don't force a flag: an immaterial rounding difference is `Match` with a note, not a fabricated
   fifth category; a genuinely unverifiable qualitative claim is `Unable to verify`, not a
   `Mismatch` by default.

## Before delivery

- Every item in the audit log has exactly one of the four valid flags.
- Every `Match`/`Stale`/`Mismatch` item has a populated Source Document, Source URL, and
  As-Of Date; `Unable to verify` items clearly state why (no route / undisclosed / subjective).
- No source URL was invented — every one traces to an actual Samaya `references` return.
- If inline annotation was requested, every flagged location that exists in the original file
  received an annotation, and the annotated file opens cleanly (spot-check by reopening it).
- Every annotation is one verdict line plus a source line — no restated body text, no raw URL
  in a Word comment where a hyperlinked `link` was possible.
- No investment-recommendation or valuation language anywhere in the audit log or annotations.
