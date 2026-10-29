#!/usr/bin/env python3
"""Build the samaya-correlation-analysis report page from report.json.

Usage:
    python build_report.py report.json --out report.html [--fragment]

report.json = the analysis.json written by analyze.py, plus the fields the
agent fills in (see SKILL.md, "Fill in report.json"). The script draws the
driver chart and all tables, builds each group's proof, common driver and
benchmark caveat, the source list and the methodology, and checks that the
numbers and source ids agree.
--fragment leaves out <!doctype>/<html>/<head>/<body> for publishing tools
that add the page skeleton themselves (the Artifact tool does).

Standard library only.
"""
import argparse
import html
import json
import sys
from datetime import date

DRIVERS = [  # fixed order and colors, same in every run
    ("oil", "Oil or commodity prices", "#D9711C"),
    ("fed", "Fed / interest rates", "#2563EB"),
    ("earnings", "Earnings, dividends, buybacks", "#14918A"),
    ("inflation", "Inflation and macro data", "#8B3FC4"),
    ("consumer", "Consumer demand data", "#D6457A"),
    ("sector", "Sector news or regulation", "#7A8B2E"),
    ("none", "No clear news found", "#CFCBC4"),
]
KEYS = [d[0] for d in DRIVERS]
LABEL = {k: l for k, l, _ in DRIVERS}
COLOR = {k: c for k, _, c in DRIVERS}
SHORT = {"oil": "Oil", "fed": "Fed", "earnings": "Earnings", "inflation": "Macro data",
         "consumer": "Consumer", "sector": "Sector", "none": "Unclear"}


def e(s):
    return html.escape(str(s if s is not None else ""))


def short_date(d):
    try:
        x = date.fromisoformat(d)
        return f"{x.strftime('%b')} {x.day}"
    except ValueError:
        return d


def check(r):
    errs = []
    for g in r["groups"]:
        name = " + ".join(g["tickers"])
        if len(g["dates"]) != g["co_move_days"]:
            errs.append(f"{name}: {len(g['dates'])} dates but co_move_days={g['co_move_days']}")
        for d in g["dates"]:
            if d.get("driver") not in KEYS:
                errs.append(f"{name} {d['date']}: driver must be one of {KEYS}, got {d.get('driver')!r}")
            elif d["driver"] != "none" and not d.get("sources"):
                errs.append(f"{name} {d['date']}: driver '{d['driver']}' needs at least one source id")
            for x in d.get("sources", []):
                if x not in r.get("evidence_sources", {}):
                    errs.append(f"{name} {d['date']}: source id {x!r} not in evidence_sources")
        if g["up"] + g["down"] != g["co_move_days"]:
            errs.append(f"{name}: up + down != co_move_days")
    ds = r.get("drivers_summary", [])
    if len(ds) > 3:
        errs.append("drivers_summary: at most 3 bullets")
    for x in ds:
        t = x.get("text", "") if isinstance(x, dict) else x
        if len(t.split()) > 50:
            errs.append(f"drivers_summary: keep each bullet under 50 words ({len(t.split())}): {t[:40]}...")
    used = {x for g in r["groups"] for d in g["dates"] for x in d.get("sources", [])}
    for x in sorted(used):
        if x in r.get("evidence_sources", {}) and not r["evidence_sources"][x].get("fact"):
            errs.append(f"source {x}: add a one-line 'fact' with the size of the move or the event")
    for k in ("takeaway", "range_label", "proof_note"):
        if not r.get(k):
            errs.append(f"missing '{k}'")
    if errs:
        sys.exit("report.json problems:\n  " + "\n  ".join(errs))


def driver_chart(groups):
    W, LW, RW, RH, BH, TOP = 1000, 150, 150, 46, 30, 10
    CW = W - LW - RW
    H = TOP + RH * len(groups) + 36
    o = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Driver chart">']
    for p in (0, 25, 50, 75, 100):
        x = LW + CW * p / 100
        o.append(f'<line x1="{x}" y1="{TOP - 4}" x2="{x}" y2="{H - 30}" class="grid"/>')
        o.append(f'<text x="{x}" y="{H - 10}" class="axis" text-anchor="middle">{p}%</text>')
    for i, g in enumerate(groups):
        y = TOP + i * RH + (RH - BH) / 2
        cy = y + BH / 2
        o.append(f'<text x="{LW - 14}" y="{cy}" class="row" text-anchor="end" dominant-baseline="central">'
                 f'{e(" + ".join(g["tickers"]))}</text>')
        n = g["co_move_days"]
        x = LW
        for k in KEYS:
            c = sum(1 for d in g["dates"] if d["driver"] == k)
            if not c:
                continue
            w = CW * g["score"] * c / n
            o.append(f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{BH}" fill="{COLOR[k]}">'
                     f'<title>{e(LABEL[k])}: {c} day{"s" if c > 1 else ""}</title></rect>')
            if w >= 22:
                cls = "seg dark" if k == "none" else "seg"
                o.append(f'<text x="{x + w / 2:.1f}" y="{cy}" class="{cls}" text-anchor="middle" '
                         f'dominant-baseline="central">{c}</text>')
            x += w
        o.append(f'<text x="{x + 10:.1f}" y="{cy}" dominant-baseline="central" class="val">'
                 f'<tspan class="b">{round(g["score"] * 100)}%</tspan>'
                 f'<tspan class="mute"> · {n} days</tspan></text>')
    o.append("</svg>")
    return "".join(o)


def legend(groups, themes):
    used = {d["driver"] for g in groups for d in g["dates"]}
    out = []
    for k, label, color in DRIVERS:
        if k in used:
            t = f"{label} ({themes[k]})" if themes.get(k) else label
            out.append(f'<span class="lg"><i style="background:{color}"></i>{e(t)}</span>')
    return '<div class="legend">' + "".join(out) + "</div>"


def link(item):
    t = e(item.get("text") or item.get("title"))
    d = item.get("date") or "undated"
    url = item.get("url")
    a = f'<a href="{e(url)}" target="_blank" rel="noopener">{t}</a>' if url else t
    return f"{a} <span class=\"mute\">({e(d)})</span>"


def md(d):
    return d[5:] if len(d) == 10 else d


def mix_of(g):
    return [(k, c) for k in KEYS if (c := sum(1 for d in g["dates"] if d["driver"] == k))]


def common_driver(g):
    n = g["co_move_days"]
    named = [(k, c) for k, c in mix_of(g) if k != "none"]
    top = max(named, key=lambda kc: kc[1]) if named else None
    if top and top[1] * 2 > n:
        main = f"{LABEL[top[0]]} ({top[1]} of {n} days)"
    else:
        main = "No common driver found"
    mw, opp = g["market_wide_days"], g.get("market_wide_bench_opposite", 0)
    note = ""
    if mw * 2 > n:
        if opp * 2 >= mw:
            note = f"Not a market effect: benchmark moved the other way on {opp} of {mw} market-wide days."
        else:
            note = f"Mainly broad-market moves ({mw} of {n} days market-wide)."
    return main, note


def src_link(x, srcs):
    s_ = srcs.get(x, {})
    tip = " · ".join(v for v in [s_.get("title"), s_.get("date"), s_.get("fact")] if v)
    if s_.get("url"):
        return f'<a href="{e(s_["url"])}" target="_blank" rel="noopener" title="{e(tip)}">{e(x)}</a>'
    return f'<span title="{e(tip)}">{e(x)}</span>'


def dates_proof(g, srcs):
    out = []
    for d in g["dates"]:
        arrow = "↑" if d["direction"] == "up" else "↓"
        star = "*" if d["market_wide"] else ""
        if d["driver"] == "none":
            proof = '<span class="mute">no source</span>'
        else:
            ids = ", ".join(src_link(x, srcs) for x in d.get("sources", []))
            proof = f"{e(SHORT[d['driver']])} {ids}"
        out.append(f'<span class="nw">{md(d["date"])}{arrow}{star}</span> {proof}')
    return " · ".join(out)


def groups_table(groups, bench, srcs):
    rows = []
    for i, g in enumerate(groups, 1):
        main, note = common_driver(g)
        mix = " · ".join(f"{SHORT[k]} {c}" for k, c in mix_of(g))
        beta = "<br>".join(f"{e(t)} {v:.2f}" for t, v in g.get("beta", {}).items())
        rows.append(
            f'<tr><td>{i}</td><td class="nw b">{e(" + ".join(g["tickers"]))}</td>'
            f'<td class="nw">{round(g["score"] * 100)}%<div class="small mute">{g["co_move_days"]}/{g.get("any_move_days", "")}</div></td>'
            f'<td>{g.get("return_corr", "")}</td>'
            f'<td class="small nw">{beta}</td>'
            f'<td class="nw">{g["co_move_days"]} ({g["up"]}↑ / {g["down"]}↓)</td>'
            f'<td>{g["market_wide_days"]}<div class="small mute">{g.get("market_wide_bench_opposite", 0)} opposite {e(bench)}</div></td>'
            f'<td class="cd">{e(main)}<div class="small mute">{e(mix)}</div>'
            + (f'<div class="small">{e(note)}</div>' if note else "") + '</td>'
            f'<td class="small dates">{dates_proof(g, srcs)}</td></tr>')
    return ('<div class="tw"><table><thead><tr><th>#</th><th>Group</th><th>Score</th><th>Return corr</th>'
            f'<th>Beta vs {e(bench)}</th><th>Co-move days</th><th>Market-wide days</th><th>Common driver</th>'
            '<th>Dates and proof</th></tr></thead><tbody>' + "".join(rows) + "</tbody></table></div>")


def avg_table(r):
    bench = r["benchmark"]
    items = sorted(r["avg_moves"].items(), key=lambda kv: -kv[1])
    rows = [f'<tr><td class="b">{e(t)}</td><td>{v:.2f}%</td><td>{r.get("beta", {}).get(t, ""):.2f}</td>'
            f'<td>{r.get("corr_benchmark", {}).get(t, ""):.2f}</td></tr>' for t, v in items]
    rows.append(f'<tr class="bench"><td class="b">{e(bench)} (benchmark)</td><td class="b">{r["benchmark_avg"]:.2f}%</td>'
                '<td>1.00</td><td>1.00</td></tr>')
    return ('<div class="tw"><table class="narrow"><thead><tr><th>Ticker</th><th>Avg daily move</th>'
            f'<th>Beta vs {e(bench)}</th><th>Correlation with {e(bench)}</th></tr></thead><tbody>'
            + "".join(rows) + "</tbody></table></div>")


def used_source_ids(groups):
    ids = []
    for g in groups:
        for d in g["dates"]:
            for x in d.get("sources", []):
                if x not in ids:
                    ids.append(x)
    return sorted(ids, key=lambda x: (x.rstrip("0123456789"), int("0" + "".join(c for c in x if c.isdigit()))))


def methodology(r):
    b = r["benchmark"]
    big = r.get("max_group_size", 5)
    size = "any size" if big >= len(r["avg_moves"]) else f"up to {big} stocks"
    return [
        f'Prices: daily closes from Samaya Market Data for {r["start"]} to {r["end"]} ({r["trading_days"]} trading days); '
        "the first % change uses the close of the trading day before the range.",
        "Big move: a day when a stock's absolute daily % change was above its own average absolute daily change over the range.",
        f"Market-wide day: {b}'s absolute move was above its own average, or at least 75% of the stocks had big moves "
        "in the same direction. These days stay in all counts and are marked *.",
        f"Score: days when every stock in the group had a big move in the same direction, divided by days when at least "
        f"one of them had a big move. Groups of {size} were tested; groups with fewer than {r.get('min_days', 3)} shared "
        "days were dropped. A larger group replaces the pairs inside it only if its score is at least 80% of each of theirs. "
        "The top 10 are shown.",
        f"Return corr: Pearson correlation of daily % returns over the whole range (average across pairs for larger groups). "
        f"Beta: covariance of the stock's daily return with {b}'s, divided by the variance of {b}'s.",
        "Drivers: each shared day was checked against Samaya sources. A day gets a driver only if a dated source shows news "
        "on that day (or the prior evening) or a meaningful same-day move in the driving market variable that fits the "
        "stocks' move. What counts as meaningful is a judgment call; each source's fact shows the size of the move. "
        "Otherwise the day is marked 'no clear news'.",
    ] + ([f'Judgment used in this run: {r["proof_note"]}'] if r.get("proof_note") else [])


CSS = """
:root{--bg:#F7F6F3;--card:#FFFFFF;--line:#E4E1DA;--text:#1F2328;--mute:#6B6F76;--grid:#E9E6E0;--bench:#1F2937;--accent:#0F8A80}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#16181B;--card:#1E2125;--line:#33373D;--text:#E8E6E3;--mute:#9AA0A6;--grid:#2C3036;--bench:#E5E7EB;--accent:#3FB8AD}}
:root[data-theme="dark"]{--bg:#16181B;--card:#1E2125;--line:#33373D;--text:#E8E6E3;--mute:#9AA0A6;--grid:#2C3036;--bench:#E5E7EB;--accent:#3FB8AD}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--text);font:15px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Helvetica,Arial,sans-serif}
.wrap{max-width:1080px;margin:0 auto;padding:28px 16px 48px}
h1{font-size:22px;margin:0 0 4px}
h2{color:var(--accent);font-size:20px;margin:28px 0 8px}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:22px 24px;margin:14px 0}
.card h3{margin:0 0 4px;font-size:17px}
.sub{color:var(--mute);font-size:13.5px;margin:0 0 12px}
.how{font-size:14px;margin:12px 0 0}
svg{width:100%;height:auto;display:block}
.chart{overflow-x:auto}.chart svg{min-width:640px}
svg text{fill:var(--text);font-family:inherit}
svg .grid{stroke:var(--grid);stroke-width:1}
svg .axis{font-size:15px;fill:var(--mute)}
svg .row{font-size:17px}
svg .val{font-size:16px}
svg .b{font-weight:700}
svg .mute{fill:var(--mute)}
svg .seg{font-size:15px;font-weight:600;fill:#fff}
svg .seg.dark{fill:#3A3A3A}
svg .bench{stroke:var(--bench);stroke-width:2;stroke-dasharray:6 5}
svg .benchlab{font-size:14px;font-weight:700}
.legend{display:flex;flex-wrap:wrap;gap:6px 18px;font-size:13.5px;margin-top:10px}
.lg i{display:inline-block;width:12px;height:12px;border-radius:2px;margin-right:6px;vertical-align:-1px}
.meta{color:var(--mute);font-size:14px}
.tw{overflow-x:auto}
table{border-collapse:collapse;width:100%;font-size:13.5px}
th,td{border-bottom:1px solid var(--line);padding:8px 10px;text-align:left;vertical-align:top}
th{color:var(--mute);font-weight:600}
.small{font-size:12.5px}.mute{color:var(--mute)}.b{font-weight:700}.nw{white-space:nowrap}
a{color:var(--accent)}
ul{padding-left:20px}
.drv li{margin:0 0 8px;max-width:900px}
table.narrow{max-width:640px}
tr.bench td{border-top:2px solid var(--line)}
td.dates{min-width:320px;line-height:1.7}
td.cd{min-width:190px}
.src li{margin-bottom:4px}
.method li{margin-bottom:4px;color:var(--text)}
"""


def build(r, fragment):
    groups = r["groups"]
    all_pairs = all(len(g["tickers"]) == 2 for g in groups)
    unit = "pair" if all_pairs else "group"
    bench = r["benchmark"]
    rng = r["range_label"]
    mw = ", ".join(md(d) for d in r["market_wide_days"]) or "none"

    drivers_html = []
    for x in r.get("drivers_summary", []):
        if isinstance(x, dict):
            drivers_html.append(f'<li><b>{e(x.get("name"))}.</b> {e(x.get("text"))}</li>')
        else:
            drivers_html.append(f'<li>{e(x)}</li>')
    drivers_block = ('<h2>What drove the co-moves</h2><ul class="drv">' + "".join(drivers_html) + '</ul>') if drivers_html else ""

    unexplained = sorted({d["date"] for g in groups for d in g["dates"] if d["driver"] == "none"})
    srcs = r.get("evidence_sources", {})
    price_items = []
    ps = r.get("prices_sources", [])
    if ps:
        tick = ", ".join(f'<a href="{e(p["url"])}" target="_blank" rel="noopener">{e(p.get("ticker", ""))}</a>'
                         if p.get("url") else e(p.get("ticker", "")) for p in ps)
        price_items.append(f' Price data (Samaya Market Data, as of {e(ps[0].get("date") or "undated")}): {tick}.')

    body = [
        '<div class="wrap">',
        f'<h1>{e(r.get("title") or "Correlation analysis")}</h1>',
        f'<p class="meta">{e(rng)} · {e(r["start"])} to {e(r["end"])} · {r["trading_days"]} trading days · '
        f'benchmark {e(bench)}</p>',
        '<h2>Takeaway</h2>', f'<p>{e(r["takeaway"])}</p>',
        '<div class="card">',
        f'<h3>How often each {unit} moved together, and why ({e(rng)})</h3>',
        f'<p class="sub">Bar length = score: of the days when any stock in the {unit} had a big move, the share of '
        'days when all of them moved the same way. Colors split the bar by the news behind those shared days; the '
        'number in each color is the count of days.</p>',
        '<div class="chart">' + driver_chart(groups) + '</div>' if groups else '<p class="mute">No group had enough shared big-move days.</p>',
        legend(groups, r.get("driver_themes", {})),
        f'<p class="how"><b>How to read it:</b> {e(r.get("driver_how_to_read", ""))}</p>' if r.get("driver_how_to_read") else "",
        '</div>',
        drivers_block,
        '<h2>Groups</h2>',
        f'<p class="meta">Score = shared big-move days ÷ days when any member had a big move. ↑/↓ = direction of the '
        f'shared move. * = market-wide day; "opposite {e(bench)}" = market-wide days when {e(bench)} moved the other way. '
        'Each source id (S1, S2…) links to the source; hover over it to see the date and the fact it proves.</p>',
        groups_table(groups, bench, srcs),
        f'<p class="meta"><b>Dates with no supporting source</b> ({len(unexplained)}): '
        f'{e(", ".join(md(x) for x in unexplained)) or "none"}</p>',
        f'<h2>Average moves</h2><p class="meta">Mean absolute daily % change, {e(r["start"])} to {e(r["end"])}.</p>',
        avg_table(r),
        f'<p class="meta"><b>Market-wide days</b> ({len(r["market_wide_days"])}): {e(mw)}</p>',
    ]
    meth = [e(x) for x in methodology(r)]
    if price_items:
        meth[0] += price_items[0]
    body += ['<h2>Methodology</h2><ul class="method">'] + [f"<li>{x}</li>" for x in meth] + ['</ul></div>']

    head = f'<title>{e(r.get("title") or "Correlation Analysis")}</title><style>{CSS}</style>'
    if fragment:
        return head + "".join(body)
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            + head + '</head><body>' + "".join(body) + '</body></html>')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("report")
    ap.add_argument("--out", default="report.html")
    ap.add_argument("--fragment", action="store_true")
    a = ap.parse_args()
    with open(a.report) as f:
        r = json.load(f)
    check(r)
    with open(a.out, "w") as f:
        f.write(build(r, a.fragment))
    print(f"Wrote {a.out}")


if __name__ == "__main__":
    main()
