#!/usr/bin/env python3
"""Validate the attribution layer against the computed screen, then render the HTML.

Usage: render.py <compute.json> <events.json> <urls_seen.txt> <template.html> <out.html>
Schema and every rule enforced here: references/events-schema.md
Any BLOCK aborts the render; the chart is never produced from data that breaks a rule.
"""
import json, math, re, sys

BROKERS = ["goldman", "morgan stanley", "jpmorgan", "jp morgan", "citi", "barclays", "wedbush", "btig",
           "benchmark co", "needham", "piper", "jefferies", "macquarie", "ubs", "deutsche", "hsbc", "canaccord",
           "davidson", "cowen", "oppenheimer", "roth", "wells fargo", "bofa", "b of a", "arete", "riley",
           "bernstein", "evercore", "keybanc", "mizuho", "rbc", "bmo", "loop capital", "raymond james"]
BANNED = ["consensus", "estimate", "street expect", "analysts expected", "news_id", "buy the", "sell the stock",
          "undervalued", "overvalued", "attractive valuation"]
TIERS = {"confirmed", "reported", "none"}
PRIMARY = ("Filings", "Press Releases", "press release feed")  # transcripts are company sources but carry no release time
DENSITY_WARN = 1.5   # events per month above which the render warns (does not block)
NUM = ["Zero", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Eleven", "Twelve"]

errs = []
def block(msg): errs.append(msg)


def t0_for(release, dates):
    """Session a release can first move: before 09:30 ET same day, 09:30-16:00 same day, after 16:00 next session."""
    d, _, hm = release.partition(" ")
    if not hm:
        return None
    if d not in dates:  # weekend or holiday release -> next session
        later = [x for x in dates if x > d]
        return later[0] if later else None
    if hm >= "16:00":
        later = [x for x in dates if x > d]
        return later[0] if later else None
    return d


def comp(rets):
    return math.prod(1 + r for r in rets) - 1


def main():
    cj, ej, uj, tpl, out = sys.argv[1:6]
    C = json.load(open(cj)); E = json.load(open(ej))
    seen = set(l.strip() for l in open(uj) if l.strip())
    days = C["days"]; dates = [d["date"] for d in days]; byd = {d["date"]: d for d in days}
    cand = {c["date"]: c for c in C["candidates"]}
    P = C["params"]; evs = E["events"]

    # 1. every callout sits on a screened day; cap; no duplicates
    used = []
    for k, e in enumerate(evs, 1):
        if e.get("tier") not in TIERS:
            block(f"event {k}: tier {e.get('tier')!r} invalid")
        for d in e["dates"]:
            if d not in cand:
                block(f"event {k}: {d} is not a screened event day")
            if d in used:
                block(f"event {k}: {d} used twice")
            used.append(d)
        if len(e["dates"]) > 1:
            ix = [dates.index(d) for d in e["dates"]]
            if max(ix) - min(ix) > 3:
                block(f"event {k}: merged dates span more than 3 sessions")
    if used != sorted(used):
        block("events are not in date order")
    # completeness replaces the old hard cap: every screened day must be researched and shown
    for d in cand:
        if d not in used:
            block(f"screened day {d} has no event (research it; a 'none' tier is allowed)")
    months = max(1, len(days) / 21)
    if len(evs) / months > DENSITY_WARN:
        print(f"WARN: {len(evs)} events over {months:.0f} months ({len(evs) / months:.1f}/month) - consider raising the screen thresholds")

    # 2. every results reaction that the screen flagged must be a callout
    for r in E["releases"]:
        if r["t0"] in cand and r["t0"] not in used:
            block(f"results reaction {r['t0']} was screened but is not a callout")
        if t0_for(r["release"], dates) != r["t0"]:
            block(f"release {r['release']} maps to {t0_for(r['release'], dates)}, not {r['t0']}")

    # 3. timing + source tier
    for k, e in enumerate(evs, 1):
        src = e.get("sources", [])
        if e["tier"] != "none" and not src:
            block(f"event {k}: no sources")
        for s in src:
            u = s.get("url", "")
            if not re.fullmatch(r"https://app\.samaya\.ai/u/[A-Za-z0-9]+", u):
                block(f"event {k}: malformed url {u}")
            elif u not in seen:
                block(f"event {k}: url {u} was not returned by Samaya this session")
        if e["tier"] == "confirmed":
            if not any(any(p in s["source_name"] for p in PRIMARY) for s in src):
                block(f"event {k}: confirmed without a primary source")
            rel = e.get("release") or ""
            if " " not in rel:
                block(f"event {k}: confirmed needs a timestamped release")
            elif t0_for(rel, dates) != e["dates"][0]:
                block(f"event {k}: release {rel} cannot explain {e['dates'][0]}")

    # 4. visible text: no brokers, no consensus, no internal ids
    for k, e in enumerate(evs, 1):
        txt = " ".join([e["label"], e["summary"], e.get("follow_on") or "", e.get("timing") or ""]).lower()
        for b in BROKERS:
            if re.search(r"\b" + re.escape(b) + r"\b", txt):
                block(f"event {k}: broker name '{b}' in visible text")
        for w in BANNED:
            if w in txt:
                block(f"event {k}: banned phrase '{w}'")
        if len(e["label"]) > 64:
            block(f"event {k}: label over 64 chars")
        if len(e["summary"].split()) > 40:
            block(f"event {k}: summary over 40 words ({len(e['summary'].split())})")

    for c in E.get("context_events", []):
        if c["date"] not in dates: block(f"context event {c['date']} is not a session in the window")
        if c["source"]["url"] not in seen: block(f"context event {c['date']}: url not returned by Samaya")
    if errs:
        print("\n".join("BLOCK: " + x for x in errs)); sys.exit(1)

    # ---- derived layer ----
    ah = set(E.get("after_hours_days", []))
    for e in evs:
        rows = [byd[d] for d in e["dates"]]
        e["ret"] = comp([r["ret"] for r in rows])
        e["bench_ret"] = comp([r["bench_ret"] for r in rows])
        e["abn"] = sum(r["abn"] for r in rows)
        e["mkt"] = sum(r["beta"] * r["bench_ret"] for r in rows)
        e["z"] = max((r["z"] for r in rows), key=abs)
        e["rvol"] = max(r["rvol"] for r in rows)
    ev_dates = set(used)
    S = dict(C["summary"])
    S["event_days_ret"] = comp([d["ret"] for d in days if d["date"] in ev_dates])
    S["other_days_ret"] = comp([d["ret"] for d in days if d["date"] not in ev_dates])
    S["n_event_sessions"] = len(ev_dates)
    market_moves = [{"date": d["date"], "ret": d["ret"], "bench_ret": d["bench_ret"], "beta": d["beta"],
                     "mkt": d["beta"] * d["bench_ret"], "abn": d["abn"], "rvol": d["rvol"]}
                    for d in days if d["date"] in set(C["market_days"])]

    S["mkt_part"] = comp([d["beta"] * d["bench_ret"] for d in days])
    S["spec_part"] = comp([d["abn"] for d in days])
    # headline: the category group with the largest log contribution, stated as arithmetic
    groups = {}
    for e in evs:
        if e["tier"] != "none":
            groups.setdefault(e["category"], []).append(e)
    def contrib(es): return comp([byd[d]["ret"] for e in es for d in e["dates"]])
    cat, es = max(groups.items(), key=lambda kv: abs(math.log(1 + contrib(kv[1]))))
    g = contrib(es); gd = {d for e in es for d in e["dates"]}
    rest = comp([d["ret"] for d in days if d["date"] not in gd]); nrest = len(days) - len(gd)
    noun = {"Earnings and guidance": "results reactions", "Sell-side rating change": "rating-driven days",
            "Regulatory and legal": "regulatory days", "Product and strategy": "product-news days"}.get(cat, "event days")
    co = E["company"].split()[0]
    verb = "took" if g < 0 else "added"
    amt = f"{abs(g) * 100:.0f}%"
    tail = f"the other {nrest} sessions {'lost' if rest < 0 else 'added'} {abs(rest) * 100:.0f}%"
    standfirst = f"{NUM[len(es)] if len(es) < len(NUM) else len(es)} {noun} {verb} {amt} {'off' if g < 0 else 'to'} the share price; {tail}."
    sp, mp = S["spec_part"], S["mkt_part"]
    spv = f"took {abs(sp) * 100:.0f}% off" if sp < 0 else f"added {sp * 100:.0f}% to"
    mpv = f"would have added {mp * 100:.0f}%" if mp >= 0 else f"would have cost {abs(mp) * 100:.0f}%"
    headline = f"Stock-specific moves {spv} {co}'s share price; at its beta, the market alone {mpv}."


    # ---- story layer: model-written prose, mechanically checked ----
    story = E.get("story")
    if not story:
        print("BLOCK: events.json has no story (headline + phases are required)"); sys.exit(1)
    chapters_out = []
    if story:
        st_err = []
        tp = {t["date"] for t in C["turning_points"]}
        pre_release = {dates[dates.index(x["t0"]) - 1] for x in E["releases"] if x["t0"] in dates and dates.index(x["t0"]) > 0}
        hi_d = max(days, key=lambda d_: d_["c"])["date"]; lo_d = min(days, key=lambda d_: d_["c"])["date"]
        allowed = tp | pre_release | {dates[0], dates[-1], hi_d, lo_d}
        ch = story["chapters"]
        if ch[0]["from"] != dates[0] or ch[-1]["to"] != dates[-1]:
            st_err.append("chapters must span the whole window")
        for a_, b_ in zip(ch, ch[1:]):
            if a_["to"] != b_["from"]:
                st_err.append(f"chapters not contiguous at {a_['to']} / {b_['from']}")
        ev_first = {e["dates"][0]: k for k, e in enumerate(evs)}
        def stats(a_, b_, refs):
            i0, i1 = dates.index(a_), dates.index(b_); rows = days[i0 + 1:i1 + 1]
            refd = {d for x in refs for d in evs[ev_first[x]]["dates"]} if refs else set()
            o = {"ret": days[i1]["c"] / days[i0]["c"] - 1,
                 "mkt": comp([r_["beta"] * r_["bench_ret"] for r_ in rows]), "spec": comp([r_["abn"] for r_ in rows]),
                 "flagged": comp([r_["ret"] for r_ in rows if r_["date"] in ev_dates]),
                 "other": comp([r_["ret"] for r_ in rows if r_["date"] not in ev_dates]),
                 "refs": comp([byd[d]["ret"] for d in sorted(refd)]) if refd else 0.0,
                 "from_c": days[i0]["c"], "to_c": days[i1]["c"]}
            return o
        pcts, usd, texts = set(), set(), []
        for v in (S["total_ret"], S["bench_ret"], S["mkt_part"], S["spec_part"], S["event_days_ret"], S["other_days_ret"]): pcts.add(round(abs(v) * 100))
        usd |= {round(S["hi"]), round(S["lo"])}
        for c in ch:
            for x in (c["from"], c["to"]):
                if x not in allowed:
                    st_err.append(f"chapter boundary {x} is not a turning point, the window's high/low or end, or the eve of a results reaction")
            for x in c.get("event_dates", []):
                if x not in ev_first: st_err.append(f"chapter '{c['title']}' cites {x}, which is not an event")
                elif not (c["from"] < x <= c["to"]): st_err.append(f"chapter '{c['title']}' cites {x} outside its dates")
            in_range = [x for x in ev_first if c["from"] < x <= c["to"]]
            if not c.get("event_dates") and not c.get("context_sources") and in_range:
                st_err.append(f"chapter '{c['title']}' has flagged days but cites nothing")
            for s_ in c.get("context_sources", []):
                if s_["url"] not in seen: st_err.append(f"chapter '{c['title']}': url {s_['url']} not returned by Samaya")
            o = stats(c["from"], c["to"], c.get("event_dates", []))
            for k_ in ("ret", "mkt", "spec", "flagged", "other", "refs"): pcts.add(round(abs(o[k_]) * 100))
            usd |= {round(o["from_c"]), round(o["to_c"])}
            texts += [evs[ev_first[x]]["label"] + " " + evs[ev_first[x]]["summary"] + " " + evs[ev_first[x]].get("guidance_check", "") for x in c.get("event_dates", []) if x in ev_first]
            chapters_out.append({**c, **o, "events": [ev_first[x] for x in c.get("event_dates", []) if x in ev_first]})
        if story.get("next"):
            if story["next"]["source"]["url"] not in seen: st_err.append("next-event url not returned by Samaya")
        sourced = " ".join(texts)
        prose = [("headline", story["headline"])] + ([("dek", story["dek"])] if story.get("dek") else []) + [(c["title"], c["text"]) for c in ch]
        for name, txt in prose:
            low = " " + txt.lower() + " "
            for w in [r"\bwill\b", r"\bshould\b", r"\bbuy\b", r"\bupside\b", r"\bcheap\b", r"\bundervalued\b", r"\battractive\b", r"\blikely to\b", r"\bpoised\b", r"\bexpect the\b"]:
                if re.search(w, low): st_err.append(f"story '{name}': speculative or recommendation language '{w[2:-2]}'")
            for b_ in BROKERS:
                if re.search(r"\b" + re.escape(b_) + r"\b", low): st_err.append(f"story '{name}': broker name '{b_}'")
            clean = re.sub(r"\b(19|20)\d\d\b|\bQ[1-4]\b|\bFY\d{4}\b|\b\d{1,2} (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\b", " ", txt)
            for m_ in re.finditer(r"(\$)?(\d[\d,]*(?:\.\d+)?)(?:-(\d+))?(%)?", clean):
                tok = m_.group(0)
                if tok in sourced: continue
                val = float(m_.group(2).replace(",", ""))
                if m_.group(4) and m_.group(3) is None and any(abs(val - p) <= 1 for p in pcts): continue
                if m_.group(1) and any(abs(val - u) <= 1 for u in usd): continue
                if not m_.group(1) and not m_.group(4) and val < 20: continue  # small counts ("two", "one")
                st_err.append(f"story '{name}': figure '{tok}' does not match a computed figure or a cited event")
        if len(story["headline"].split()) > 24: st_err.append("headline over 24 words")
        for c in ch:
            if len(c["title"].split()) > 6: st_err.append(f"tile title '{c['title']}' over 6 words")
            if len(c["text"].split()) > 18: st_err.append(f"tile line for '{c['title']}' over 18 words")
        if len(ch) > 5: st_err.append("more than 5 phases")
        if st_err:
            print("\n".join("BLOCK: " + x for x in st_err)); sys.exit(1)
    lo, hi = S["lo"], S["hi"]
    data = {
        "ticker": C["ticker"].upper(), "company": E["company"], "benchmark": C["benchmark"].upper(), "benchmark_name": E["benchmark_name"],
        "window": C["window"], "as_of": E["as_of"], "base_close": C["base_close"], "params": P,
        "headline": story["headline"] if story else headline, "standfirst": (story.get("dek") or "") if story else standfirst,
        "chapters": chapters_out, "next": (story or {}).get("next"), "context_events": E.get("context_events", []),
        "mechanical_days": C.get("mechanical_days", []), "summary": S, "sources": C["sources"],
        "market_days": C["market_days"], "market_moves": market_moves, "turning_points": C["turning_points"],
        "releases": E["releases"],
        "other_flagged": [c for c in C["candidates"] if c["date"] not in ev_dates],
        "log_scale_note": ("The price axis is logarithmic because the range is wide, so equal distances are equal percentage moves."
                           if hi / lo > 2.2 else "The price axis is linear."),
        "events": [{k: e.get(k) for k in ("dates", "label", "category", "tier", "timing", "summary", "follow_on",
                                          "sources", "ret", "bench_ret", "abn", "mkt", "z", "rvol")} for e in evs],
        "days": [{"date": d["date"], "o": d["o"], "h": d["h"], "l": d["l"], "c": d["c"], "v": d["v"],
                  "bench": d["bench"], "ret": round(d["ret"], 6), "bench_ret": round(d["bench_ret"], 6),
                  "abn": round(d["abn"], 6), "mkt": round(d["beta"] * d["bench_ret"], 6), "beta": round(d["beta"], 3), "sig": round(d["sigma"], 6),
                  "rvol": round(d["rvol"] or 0, 3), "medv": d["avg_vol"], "mech": d.get("mech"),
                  "ah": d["date"] in ah} for d in days],
    }
    html = open(tpl).read()
    if "/*__DATA__*/" not in html:
        sys.exit("BLOCK: template has no data slot")
    html = html.replace("/*__DATA__*/", json.dumps(data, separators=(",", ":")).replace("</", "<\\/"))
    html = html.replace("__TITLE__", f"{C['ticker'].upper()}: what moved the stock")
    if re.search(r"__[A-Z]+__|/\*__", html):
        sys.exit("BLOCK: unfilled placeholder in output")
    # script must parse (catches a broken template before it ships); skipped if node is unavailable
    import shutil, subprocess, tempfile
    if shutil.which("node"):
        js = html[html.index("<script>\n") + 9: html.index("</script>", html.index("<script>\n"))]
        with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as fh: fh.write(js)
        chk = subprocess.run(["node", "--check", fh.name], capture_output=True, text=True)
        if chk.returncode: sys.exit("BLOCK: page script does not parse:\n" + chk.stderr[-400:])
    open(out, "w").write(html)
    print("OK", out, f"{len(html) / 1024:.0f} kB")
    print("headline:", story["headline"])
    print(f"market-explained part {S['mkt_part']:+.1%}; stock-specific part {S['spec_part']:+.1%}; total {S['total_ret']:+.1%}")
    print(f"event days {len(ev_dates)} -> {S['event_days_ret']:+.1%}; other {len(days) - len(ev_dates)} -> {S['other_days_ret']:+.1%}")
    for k, e in enumerate(evs, 1):
        print(f"  {k:>2} {e['dates'][0]} {e['ret']:+6.1%} abn {e['abn']:+6.1%} rvol {e['rvol']:.1f}x  [{e['tier']}] {e['label']}")


if __name__ == "__main__":
    main()
