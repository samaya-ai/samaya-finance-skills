"""Make PPTX citation markers render consistently. Run once on the finished deck:

    python pptx_superscripts.py deck.pptx

Write markers as Unicode superscripts (¹ ² ³ ⁴ …) so every call site in the generator stays
a plain string. Then this script fixes the two problems that approach leaves:

1. Glyphs: ¹ ² ³ come from Latin-1 and ⁰ ⁴–⁹ from the Superscripts block, so in most fonts
   ⁴–⁹ sit lower and smaller than ¹–³. Each run holding marker characters is split so the
   markers become ordinary digits in a run with baseline="30000" (a true superscript),
   cloning the run's formatting and any hyperlink. Every marker then looks the same.
2. Paragraphs: pptxgenjs writes an <a:pPr> for every run of a rich-text paragraph, so a
   bullet followed by a differently formatted run loses its bullet and the paragraph is
   schema-invalid. Only the first <a:pPr> of each paragraph is kept.

Generating true superscript runs in pptxgenjs instead is worse: in a table cell each run of
an array becomes its own paragraph, so the marker drops onto a new line.
"""

import re
import shutil
import sys
import tempfile
import zipfile

SUP = {"¹": "1", "²": "2", "³": "3", "⁰": "0", "⁴": "4", "⁵": "5",
       "⁶": "6", "⁷": "7", "⁸": "8", "⁹": "9"}
SUP_RE = re.compile("([%s]+)" % "".join(SUP))
RUN_RE = re.compile(r"<a:r>(<a:rPr\b[^>]*?(?:/>|>.*?</a:rPr>))<a:t>([^<]*)</a:t></a:r>", re.S)
PARA_RE = re.compile(r"<a:p>.*?</a:p>", re.S)
PPR_RE = re.compile(r"<a:pPr\b[^>]*?(?:/>|>.*?</a:pPr>)", re.S)
SLIDE_RE = re.compile(r"^ppt/(slides|slideLayouts|notesSlides)/[^/]+\.xml$")


def superscript_rpr(rpr: str) -> str:
    head = re.match(r"<a:rPr\b[^>]*?(/?>)", rpr, re.S)
    tag = head.group(0)
    tag = re.sub(r'\sbaseline="-?\d+"', "", tag)
    tag = tag[: -len(head.group(1))].rstrip() + ' baseline="30000"' + head.group(1)
    return tag + rpr[len(head.group(0)):]


def split_run(m: re.Match) -> str:
    rpr, text = m.group(1), m.group(2)
    if not SUP_RE.search(text):
        return m.group(0)
    out = []
    for part in SUP_RE.split(text):
        if not part:
            continue
        if SUP_RE.fullmatch(part):
            digits = "".join(SUP[c] for c in part)
            out.append(f"<a:r>{superscript_rpr(rpr)}<a:t>{digits}</a:t></a:r>")
        else:
            space = ' xml:space="preserve"' if part != part.strip() else ""
            out.append(f"<a:r>{rpr}<a:t{space}>{part}</a:t></a:r>")
    return "".join(out)


def keep_first_ppr(m: re.Match) -> str:
    para, seen = m.group(0), []

    def drop(p: re.Match) -> str:
        seen.append(1)
        return p.group(0) if len(seen) == 1 else ""

    para = PPR_RE.sub(drop, para)
    return para


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit("usage: python pptx_superscripts.py deck.pptx")
    path = sys.argv[1]
    markers = paras_fixed = 0
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pptx")
    tmp.close()
    with zipfile.ZipFile(path) as zin, zipfile.ZipFile(tmp.name, "w", zipfile.ZIP_DEFLATED) as zout:
        for info in zin.infolist():
            data = zin.read(info.filename)
            if SLIDE_RE.match(info.filename):
                xml = data.decode("utf-8")
                markers += sum(len(SUP_RE.findall(t)) for _, t in RUN_RE.findall(xml))
                xml = RUN_RE.sub(split_run, xml)
                before = sum(len(PPR_RE.findall(p)) > 1 for p in PARA_RE.findall(xml))
                xml = PARA_RE.sub(keep_first_ppr, xml)
                paras_fixed += before
                left = [c for c in SUP if c in "".join(re.findall(r"<a:t[^>]*>([^<]*)</a:t>", xml))]
                if left:
                    sys.exit(f"{info.filename}: markers left unconverted {left}")
                data = xml.encode("utf-8")
            zout.writestr(info, data)
    shutil.move(tmp.name, path)
    print(f"Converted {markers} marker group(s) to superscript runs; "
          f"removed stray <a:pPr> from {paras_fixed} paragraph(s)")


if __name__ == "__main__":
    main()
