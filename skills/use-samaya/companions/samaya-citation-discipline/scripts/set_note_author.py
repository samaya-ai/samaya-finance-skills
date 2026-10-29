"""Set the author of every classic cell Note in an .xlsx to "Samaya", in place.

Why this exists: openpyxl writes Note authors correctly, but the xlsx skill's mandatory
recalc step (scripts/recalc.py, a LibreOffice round-trip) rewrites every Note author to
"Unknown Author". Re-saving with openpyxl afterwards is not a fix, because openpyxl drops
the cached formula values recalc just computed. So patch the XML directly, as the last
step after recalc:

    python set_note_author.py workbook.xlsx

Touches only the <authors> list of each comments part; text, anchors, and the VML shapes
are left alone. Exits non-zero if the workbook has threaded comments (those are never the
citation mechanic here) or no Notes at all.
"""

import re
import shutil
import sys
import tempfile
import zipfile

AUTHOR = "Samaya"
COMMENTS_PART = re.compile(r"^xl/comments(?:/comment\d*|\d*)\.xml$")
AUTHORS = re.compile(r"<authors>.*?</authors>|<authors\s*/>", re.S)


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit("usage: python set_note_author.py workbook.xlsx")
    path = sys.argv[1]

    with zipfile.ZipFile(path) as zin:
        names = zin.namelist()
        if any("threadedComment" in n for n in names):
            sys.exit("threaded comments found: cite with classic Notes only")
        parts = [n for n in names if COMMENTS_PART.match(n)]
        if not parts:
            sys.exit("no cell Notes found in workbook")

        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
        tmp.close()
        changed = 0
        with zipfile.ZipFile(tmp.name, "w", zipfile.ZIP_DEFLATED) as zout:
            for info in zin.infolist():
                data = zin.read(info.filename)
                if info.filename in parts:
                    xml = data.decode("utf-8")
                    # Every note keeps authorId="0"; collapse the list to one author.
                    xml, n = AUTHORS.subn(f"<authors><author>{AUTHOR}</author></authors>", xml, 1)
                    xml = re.sub(r'authorId="\d+"', 'authorId="0"', xml)
                    changed += n
                    data = xml.encode("utf-8")
                zout.writestr(info, data)

    if changed != len(parts):
        sys.exit(f"expected an <authors> list in each of {parts}; patched {changed}")
    shutil.move(tmp.name, path)
    print(f'Set Note author to "{AUTHOR}" in {", ".join(parts)}')


if __name__ == "__main__":
    main()
