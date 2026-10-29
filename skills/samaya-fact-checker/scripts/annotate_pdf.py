#!/usr/bin/env python3
"""
Add sticky-note comment annotations to the ORIGINAL PDF being fact-checked.

Usage:
    python annotate_pdf.py <original.pdf> <data.json> <output.pdf>

Only items with location.type == "pdf" are processed. For each, location.detail should hold a
short verbatim snippet (under ~10 words) from the page so this script can find its bounding box
via pdfplumber and anchor the note there. If the snippet isn't found on the page, the note is
placed in the top-left corner of the page instead (still correctly attributed to that page,
just not precisely anchored) and this is reported at the end.

Only run this after the user has explicitly opted in to inline annotation.
"""
import json
import sys
import pdfplumber
from pypdf import PdfReader, PdfWriter
import pypdf.annotations as annotations

AUTHOR = "Fact-Checker"
FALLBACK_RECT_SIZE = 20


def short_note(item):
    """Note text trimmed for a margin pane: no trailing period, lower-cased opener."""
    note = (item.get("note") or "").strip().rstrip(".")
    if not note:
        return ""
    return note[0].lower() + note[1:]


def note_text(item):
    """One short verdict line, then source document, date and URL."""
    flag = item.get("flag", "")
    original = item.get("original_value", "")
    sourced = item.get("samaya_value", "")
    note = short_note(item)

    if flag == "Unable to verify":
        return f"{flag} — {note or 'no Samaya route for this claim'}"

    if flag == "Match":
        line = f"{flag} — {sourced or original}"
    else:
        line = f"{flag} — doc: {original} | now: {sourced}"
    if note:
        line += f"; {note}"

    doc = item.get("source_doc") or "Not disclosed"
    date = item.get("as_of_date") or ""
    url = item.get("source_url") or "no link returned"
    return f"{line}\n{doc}{f' ({date})' if date else ''}\n{url}"


def find_rect(plumber_page, snippet):
    """Search for a short snippet on the page; return (x0, y0, x1, y1) in PDF coords or None."""
    if not snippet:
        return None
    words = plumber_page.extract_words()
    page_height = plumber_page.height
    snippet_lower = snippet.lower().strip()
    # Try to find a run of consecutive words whose joined text contains the snippet.
    joined = " ".join(w["text"] for w in words).lower()
    if snippet_lower not in joined:
        # fall back to matching on the first token of the snippet only
        first_tok = snippet_lower.split()[0] if snippet_lower.split() else None
        candidates = [w for w in words if first_tok and first_tok in w["text"].lower()]
        if not candidates:
            return None
        w = candidates[0]
        x0, x1, top, bottom = w["x0"], w["x1"], w["top"], w["bottom"]
    else:
        # crude approach: find the first word of the snippet and use its box
        first_tok = snippet_lower.split()[0]
        candidates = [w for w in words if first_tok in w["text"].lower()]
        if not candidates:
            return None
        w = candidates[0]
        x0, x1, top, bottom = w["x0"], w["x1"], w["top"], w["bottom"]
    # pdfplumber's origin is top-left; pypdf/PDF coords are bottom-left. Convert.
    y0 = page_height - bottom
    y1 = page_height - top
    return (x0, y0, x1, y1)


def annotate(src_path, data, out_path):
    reader_plumber = pdfplumber.open(src_path)
    reader = PdfReader(src_path)
    writer = PdfWriter()
    writer.append(reader)

    applied, fallback_used = 0, []

    for item in data.get("items", []):
        loc = item.get("location") or {}
        if loc.get("type") != "pdf":
            continue
        page_num = loc.get("page")
        if not page_num or page_num < 1 or page_num > len(reader.pages):
            continue
        page_idx = page_num - 1
        plumber_page = reader_plumber.pages[page_idx]
        snippet = loc.get("detail", "")
        rect = find_rect(plumber_page, snippet)
        if rect is None:
            rect = (10, plumber_page.height - 30, 10 + FALLBACK_RECT_SIZE,
                    plumber_page.height - 10)
            fallback_used.append(item.get("id"))

        note = annotations.Text(text=note_text(item), rect=rect)
        writer.add_annotation(page_number=page_idx, annotation=note)
        applied += 1

    reader_plumber.close()
    with open(out_path, "wb") as f:
        writer.write(f)

    print(f"Wrote {out_path}: {applied} annotation(s) applied.")
    if fallback_used:
        print(f"Placed at page corner (snippet not located precisely) for items: {fallback_used}")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(__doc__)
        sys.exit(1)
    with open(sys.argv[2]) as f:
        data = json.load(f)
    annotate(sys.argv[1], data, sys.argv[3])
