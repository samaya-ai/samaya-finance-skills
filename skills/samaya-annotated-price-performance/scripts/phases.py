#!/usr/bin/env python3
"""Print the numbers to write the story from, before writing it.

Usage: phases.py <compute.json> <events.json> [boundary_date ...]

Without boundaries, lists the allowed ones (turning points, window high/low and ends, eves of
results reactions). With boundaries, prints each phase's return, its market and stock-specific
parts, and how much came on flagged days versus all other sessions.
"""
import json, math, sys

def comp(xs): return math.prod(1 + x for x in xs) - 1

C = json.load(open(sys.argv[1])); E = json.load(open(sys.argv[2])); bounds = sys.argv[3:]
days = C["days"]; dates = [d["date"] for d in days]; idx = {d: i for i, d in enumerate(dates)}
ev = {d for e in E.get("events", []) for d in e["dates"]}
pre = {dates[idx[r["t0"]] - 1] for r in E.get("releases", []) if r["t0"] in idx and idx[r["t0"]] > 0}
hi = max(days, key=lambda d: d["c"]); lo = min(days, key=lambda d: d["c"])
S = C["summary"]
print(f"Window {dates[0]}..{dates[-1]}: total {S['total_ret']:+.1%}, benchmark {S['bench_ret']:+.1%}, "
      f"market part {comp([d['beta'] * d['bench_ret'] for d in days]):+.1%}, stock-specific {comp([d['abn'] for d in days]):+.1%}")
print(f"Flagged days {comp([d['ret'] for d in days if d['date'] in ev]):+.1%} ({len(ev)} sessions); "
      f"all other sessions {comp([d['ret'] for d in days if d['date'] not in ev]):+.1%}")
if not bounds:
    print("\nAllowed boundaries:")
    for t in C["turning_points"]: print(f"  {t['date']}  turning point ({t['kind']}) {t['close']}")
    print(f"  {hi['date']}  window high {hi['c']}\n  {lo['date']}  window low {lo['c']}")
    for d in sorted(pre): print(f"  {d}  eve of a results reaction")
    print(f"  {dates[0]} / {dates[-1]}  window ends")
    sys.exit(0)
pts = [dates[0]] + sorted(bounds) + [dates[-1]]
for a, b in zip(pts, pts[1:]):
    rows = days[idx[a] + 1: idx[b] + 1]
    fl = [r for r in rows if r["date"] in ev]
    print(f"{a}..{b}  {days[idx[a]]['c']:.2f}->{days[idx[b]]['c']:.2f}  {days[idx[b]]['c'] / days[idx[a]]['c'] - 1:+.1%}  "
          f"market {comp([r['beta'] * r['bench_ret'] for r in rows]):+.1%}  stock-specific {comp([r['abn'] for r in rows]):+.1%}  "
          f"flagged {comp([r['ret'] for r in fl]):+.1%} ({len(fl)})  other {comp([r['ret'] for r in rows if r['date'] not in ev]):+.1%}")
