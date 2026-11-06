#!/usr/bin/env python3
"""Independent coverage audit of a finished page. Does not trust the research; checks the data.

Usage: coverage_check.py <compute.json> <events.json> [n=10]

For the window's largest raw and stock-specific moves (as many as the screen's scaled top-move guarantee), reports how each is handled:
flagged (with tier), explained by the market, inside a researched run, or NOT COVERED. Also lists
days the old volume gate would have dropped, phases whose move came mostly from unflagged
sessions, and the tier mix. A page passes when no top move is NOT COVERED.
"""
import json, math, sys
C = json.load(open(sys.argv[1])); E = json.load(open(sys.argv[2]))
# same scaled count as the screen's top-move guarantee (about 10 per year), unless overridden
n = int(sys.argv[3].split("=")[1]) if len(sys.argv) > 3 else int(C["params"].get("top_n", 10))
days = C["days"]; ix = {d["date"]: i for i, d in enumerate(days)}
tier = {d: e["tier"] for e in E["events"] for d in e["dates"]}
runs = [(r["start"], r["end"]) for r in E.get("runs", [])]
mkt = set(C.get("market_days", []))
def status(d):
    if d["date"] in tier: return "flagged/" + tier[d["date"]]
    if any(a <= d["date"] <= b for a, b in runs): return "in run"
    if d["date"] in mkt or abs(d["z"]) < 2.0: return "market/normal"
    return "NOT COVERED"
fail = 0
for key, lab in (("ret", "largest raw moves"), ("abn", "largest stock-specific moves")):
    print(f"Top {n} {lab}:")
    for d in sorted(days, key=lambda x: -abs(x[key]))[:n]:
        s = status(d); fail += s == "NOT COVERED"
        print(f"  {d['date']}  ret {d['ret']:+6.1%}  stock {d['abn']:+6.1%}  z {d['z']:+4.1f}  vol {(d['rvol'] or 0):.1f}x  -> {s}")
old = [d for d in days if d["date"] in tier and not (abs(d["z"]) >= 4 or (abs(d["z"]) >= 2.5 and (d["rvol"] or 0) >= 1.75 and not d.get("mech")))]
print(f"Callouts the old volume gate would have dropped: {len(old)} of {len(tier)}  " + ", ".join(d['date'] for d in old))
near = [d for d in days if 2.0 <= abs(d["z"]) < 2.5 and d["date"] not in tier and not any(a <= d["date"] <= b for a, b in runs)]
print(f"Near misses (z 2.0-2.5, unflagged): " + (", ".join(f"{d['date']} {d['ret']:+.1%}" for d in near) or "none"))
for c in E["story"]["chapters"]:
    rows = [d for d in days if c["from"] < d["date"] <= c["to"]]
    tot = math.prod(1 + d["ret"] for d in rows) - 1
    oth = math.prod(1 + d["abn"] for d in rows if d["date"] not in tier) - 1  # stock-specific, unflagged
    drift = abs(oth) > 0.08 and not any(c["from"] <= a and b <= c["to"] for a, b in runs) and not c.get("context_sources")
    print(f"Phase {c['title']!r}: {tot:+.1%}, stock-specific on unflagged sessions {oth:+.1%}" + ("  <- DRIFT NEEDS PHASE RESEARCH" if drift else ""))
    fail += drift
mix = {}
for e in E["events"]: mix[e["tier"]] = mix.get(e["tier"], 0) + 1
src = {}
for e in E["events"]:
    for s in e["sources"]: src[s["source_name"]] = src.get(s["source_name"], 0) + 1
print("Tiers:", mix, "| sources:", src)
print("RESULT:", "PASS" if not fail else f"{fail} issue(s)")
