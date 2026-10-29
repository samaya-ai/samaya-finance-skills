"""Add a Word comment whose source reference is a real hyperlink on short display text.

Wraps the public docx skill's scripts/comment.py, then rewrites the comment so a
`{{LINK}}` token in the text becomes a clickable external hyperlink (default display
text: "link"). Needed because a Word comment part carries its own relationships file
(word/_rels/comments.xml.rels) — a hyperlink relationship added to document.xml.rels
will not resolve from inside comments.xml.

Usage:
    python comment_with_link.py unpacked/ "CEO, Q2 2026 earnings call {{LINK}}" \
        --url https://app.samaya.ai/u/bFMeCdaHlp2

    python comment_with_link.py unpacked/ "Q2 revenue {{LINK}}" \
        --url https://... --text "Q2 10-Q"

Prints the comment id and the document.xml marker snippet from comment.py.
Run once per citation against the same unpacked/ tree, then rezip.
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape, quoteattr

DOCX_SCRIPTS = Path("/mnt/skills/public/docx/scripts")
REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
HYPERLINK_REL = (
    "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink"
)
TOKEN = "{{LINK}}"

EMPTY_RELS = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    f'<Relationships xmlns="{REL_NS}"></Relationships>'
)


def add_hyperlink_rel(rels_path: Path, url: str) -> str:
    """Add (or reuse) an external hyperlink relationship; return its rId."""
    rels_path.parent.mkdir(parents=True, exist_ok=True)
    xml = rels_path.read_text(encoding="utf-8") if rels_path.exists() else EMPTY_RELS

    existing = re.search(
        r'<Relationship[^>]*Target="%s"[^>]*Id="(rId\d+)"' % re.escape(url), xml
    ) or re.search(
        r'<Relationship[^>]*Id="(rId\d+)"[^>]*Target="%s"' % re.escape(url), xml
    )
    if existing:
        return existing.group(1)

    used = [int(n) for n in re.findall(r'Id="rId(\d+)"', xml)]
    rid = f"rId{max(used) + 1 if used else 1}"
    rel = (
        f'<Relationship Id="{rid}" Type="{HYPERLINK_REL}" '
        f"Target={quoteattr(url)} TargetMode=\"External\"/>"
    )
    if "</Relationships>" not in xml:
        # An empty part is often serialized self-closing: <Relationships .../>
        root = re.search(r"<Relationships\b[^>]*/>", xml)
        if not root:
            sys.exit(f"{rels_path} has no <Relationships> root")
        xml = xml.replace(root.group(0), root.group(0)[:-2] + "></Relationships>", 1)
    xml = xml.replace("</Relationships>", rel + "</Relationships>", 1)
    rels_path.write_text(xml, encoding="utf-8")
    if rid not in rels_path.read_text(encoding="utf-8"):
        sys.exit(f"failed to write hyperlink relationship to {rels_path}")
    return rid


def link_token(comments_path: Path, comment_id: int, rid: str, text: str) -> None:
    """Replace the {{LINK}} token inside one comment with a hyperlink run."""
    xml = comments_path.read_text(encoding="utf-8")

    match = re.search(
        r'(<w:comment\b[^>]*w:id="%d".*?</w:comment>)' % comment_id, xml, re.S
    )
    if not match:
        sys.exit(f"comment id={comment_id} not found in {comments_path}")
    block = match.group(1)
    if TOKEN not in block:
        sys.exit(f"no {TOKEN} token in comment id={comment_id}")

    run = re.search(r"<w:r>(?:(?!</w:r>).)*?%s.*?</w:r>" % re.escape(TOKEN), block, re.S)
    if not run:
        sys.exit("could not locate the run holding the token")
    run_xml = run.group(0)

    rpr = re.search(r"<w:rPr>.*?</w:rPr>", run_xml, re.S)
    rpr_xml = rpr.group(0) if rpr else ""
    body = re.search(r"<w:t[^>]*>(.*?)</w:t>", run_xml, re.S)
    before, _, after = body.group(1).partition(TOKEN)

    link_rpr = (
        "<w:rPr><w:rStyle w:val=\"Hyperlink\"/><w:color w:val=\"0563C1\"/>"
        "<w:u w:val=\"single\"/><w:sz w:val=\"20\"/><w:szCs w:val=\"20\"/></w:rPr>"
    )

    def plain(content: str) -> str:
        if not content:
            return ""
        return (
            f'<w:r>{rpr_xml}<w:t xml:space="preserve">{content}</w:t></w:r>'
        )

    replacement = (
        plain(before)
        + f'<w:hyperlink r:id="{rid}">'
        + f'<w:r>{link_rpr}<w:t xml:space="preserve">{xml_escape(text)}</w:t></w:r>'
        + "</w:hyperlink>"
        + plain(after)
    )
    comments_path.write_text(
        xml.replace(block, block.replace(run_xml, replacement), 1), encoding="utf-8"
    )


EXTRA_NS = {
    "w14": "http://schemas.microsoft.com/office/word/2010/wordml",
    "w15": "http://schemas.microsoft.com/office/word/2012/wordml",
    "w16cid": "http://schemas.microsoft.com/office/word/2016/wordml/cid",
    "w16cex": "http://schemas.microsoft.com/office/word/2018/wordml/cex",
}


def ensure_namespaces(comments_path: Path) -> None:
    """Declare w14/w15/w16* on an existing comments.xml root.

    Some producers (pandoc, older converters) ship a comments.xml that declares only
    w/r/m. comment.py writes w14:paraId into it and its next run then fails to reparse
    the file ("unbound prefix"). Declaring the prefixes up front avoids that.
    """
    if not comments_path.exists():
        return
    xml = comments_path.read_text(encoding="utf-8")
    match = re.search(r"<w:comments\b[^>]*>", xml)
    if not match:
        return
    root = match.group(0)
    missing = "".join(
        f' xmlns:{p}="{u}"' for p, u in EXTRA_NS.items() if f"xmlns:{p}=" not in root
    )
    if missing:
        patched = root[:-1].rstrip("/") + missing + (">" if not root.endswith("/>") else "/>")
        comments_path.write_text(xml.replace(root, patched, 1), encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("unpacked", help="unpacked .docx directory")
    ap.add_argument("comment", help=f"comment text containing a {TOKEN} token")
    ap.add_argument("--url", required=True, help="exact URL returned by the source")
    ap.add_argument("--text", default="link", help='hyperlink display text (default "link")')
    ap.add_argument("--parent", type=int, default=None, help="reply to this comment id")
    args = ap.parse_args()

    root = Path(args.unpacked)
    if not root.is_dir():
        sys.exit("unpacked must be a directory (unzip the .docx first)")
    if TOKEN not in args.comment:
        sys.exit(f"comment text must contain the {TOKEN} token")

    ensure_namespaces(root / "word" / "comments.xml")

    cmd = [sys.executable, "comment.py", str(root.resolve()), args.comment]
    if args.parent is not None:
        cmd += ["--parent", str(args.parent)]
    proc = subprocess.run(cmd, cwd=DOCX_SCRIPTS, capture_output=True, text=True)
    if proc.returncode != 0:
        sys.exit(proc.stderr or proc.stdout)
    out = proc.stdout
    cid = int(re.search(r"Added comment id=(\d+)", out).group(1))

    rid = add_hyperlink_rel(root / "word" / "_rels" / "comments.xml.rels", args.url)
    link_token(root / "word" / "comments.xml", cid, rid, args.text)
    print(out.rstrip())
    print(f'Linked "{args.text}" -> {args.url} ({rid}) in comment id={cid}')


if __name__ == "__main__":
    main()
