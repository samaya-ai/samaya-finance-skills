#!/usr/bin/env python3
"""
Add citation comments to specific cells in the ORIGINAL Excel file being fact-checked.

Usage:
    python annotate_xlsx.py <original.xlsx> <data.json> <output.xlsx>

Only items with location.type == "xlsx" are processed; everything else is skipped. Each
comment is one short verdict line, then the source document, date and URL on a second line
(Excel cell comments are plain text, so the URL cannot hide behind a "link"). Comment author
is set to "Fact-Checker".

Only run this after the user has explicitly opted in to inline annotation.
"""
import json
import sys
from openpyxl import load_workbook
from openpyxl.comments import Comment

AUTHOR = "Fact-Checker"


def short_note(item):
    """Note text trimmed for a margin pane: no trailing period, lower-cased opener."""
    note = (item.get("note") or "").strip().rstrip(".")
    if not note:
        return ""
    return note[0].lower() + note[1:]


def verdict_line(item):
    """One short line: flag, then values only where they differ."""
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
    return line


def source_line(item):
    doc = item.get("source_doc") or "Not disclosed"
    date = item.get("as_of_date") or ""
    url = item.get("source_url") or "no link returned"
    return f"{doc}{f' ({date})' if date else ''}\n{url}"


def comment_text(item):
    if item.get("flag") == "Unable to verify":
        return verdict_line(item)
    return f"{verdict_line(item)}\n{source_line(item)}"


def annotate(src_path, data, out_path):
    wb = load_workbook(src_path)
    applied, skipped_missing = 0, []

    for item in data.get("items", []):
        loc = item.get("location") or {}
        if loc.get("type") != "xlsx":
            continue
        sheet_name = loc.get("sheet")
        cell_ref = loc.get("cell")
        if not sheet_name or not cell_ref:
            skipped_missing.append(item.get("id"))
            continue
        if sheet_name not in wb.sheetnames:
            skipped_missing.append(item.get("id"))
            continue
        ws = wb[sheet_name]
        ws[cell_ref].comment = Comment(comment_text(item), AUTHOR)
        applied += 1

    wb.save(out_path)
    print(f"Wrote {out_path}: {applied} comment(s) applied.")
    if skipped_missing:
        print(f"Skipped (missing/invalid sheet or cell): {skipped_missing}")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(__doc__)
        sys.exit(1)
    with open(sys.argv[2]) as f:
        data = json.load(f)
    annotate(sys.argv[1], data, sys.argv[3])
