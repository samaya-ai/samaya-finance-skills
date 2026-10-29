#!/usr/bin/env python3
"""Steps 2-4 of samaya-correlation-analysis: moves, market-wide days, top groups.

Usage:
    python analyze.py prices.csv --benchmark SPY [--top 10] [--out analysis.json]

prices.csv: one row per trading day, oldest first. First column "date"
(YYYY-MM-DD), then one column per ticker plus the benchmark, holding the
daily close. The first row is the close on the trading day BEFORE the range
starts (it only seeds the first % change). Empty cells are not allowed: the
script stops and lists them, so gaps are never filled with estimates.

Standard library only.
"""
import argparse
import csv
import json
import sys


def load(path):
    with open(path, newline="") as f:
        rows = list(csv.reader(f))
    header = [h.strip() for h in rows[0]]
    if header[0].lower() != "date":
        sys.exit("First column must be 'date'.")
    tickers = header[1:]
    dates, closes, gaps = [], {t: [] for t in tickers}, []
    for r in rows[1:]:
        if not r or not r[0].strip():
            continue
        d = r[0].strip()
        dates.append(d)
        for i, t in enumerate(tickers, start=1):
            v = r[i].strip() if i < len(r) else ""
            if v == "":
                gaps.append(f"{t} {d}")
                closes[t].append(None)
            else:
                closes[t].append(float(v.replace(",", "")))
    if gaps:
        sys.exit("Missing prices (ask the user for a price file):\n  " + "\n  ".join(gaps))
    if len(dates) < 3:
        sys.exit("Need at least 3 rows (seed close + 2 trading days).")
    return dates, tickers, closes


def bits(n):
    return bin(n).count("1")


def mean(x):
    return sum(x) / len(x)


def cov(x, y):
    mx, my = mean(x), mean(y)
    return sum((a - mx) * (b - my) for a, b in zip(x, y)) / (len(x) - 1)


def corr(x, y):
    return cov(x, y) / (cov(x, x) * cov(y, y)) ** 0.5


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("prices")
    ap.add_argument("--benchmark", default="SPY")
    ap.add_argument("--top", type=int, default=10)
    ap.add_argument("--min-days", type=int, default=3)
    ap.add_argument("--out", default="analysis.json")
    a = ap.parse_args()

    dates, cols, closes = load(a.prices)
    if a.benchmark not in cols:
        sys.exit(f"Benchmark {a.benchmark} not found in the CSV columns.")
    tickers = [t for t in cols if t != a.benchmark]
    days = dates[1:]
    n_days = len(days)

    # Step 2: daily % change, average absolute move, outsized moves.
    chg = {}
    for t in cols:
        c = closes[t]
        chg[t] = [(c[i] / c[i - 1] - 1) * 100 for i in range(1, len(c))]
    avg = {t: sum(abs(x) for x in chg[t]) / n_days for t in cols}

    b = chg[a.benchmark]
    beta = {t: cov(chg[t], b) / cov(b, b) for t in tickers}
    corr_bench = {t: corr(chg[t], b) for t in tickers}

    up, dn = {}, {}  # bitmask over days
    for t in tickers:
        u = d = 0
        for i, x in enumerate(chg[t]):
            if abs(x) > avg[t]:
                if x > 0:
                    u |= 1 << i
                elif x < 0:
                    d |= 1 << i
        up[t], dn[t] = u, d

    # Step 3: market-wide days.
    mw = 0
    for i, x in enumerate(chg[a.benchmark]):
        n_up = sum(1 for t in tickers if up[t] >> i & 1)
        n_dn = sum(1 for t in tickers if dn[t] >> i & 1)
        if abs(x) > avg[a.benchmark] or max(n_up, n_dn) >= 0.75 * len(tickers):
            mw |= 1 << i

    # Step 4: candidate groups. Supersets can never have more co-move days
    # than a subset, so only extend groups that still meet the minimum.
    max_size = len(tickers) if len(tickers) <= 12 else 5
    cands = []

    def extend(group, gu, gd, gany, start):
        for j in range(start, len(tickers)):
            t = tickers[j]
            nu, nd, nany = gu & up[t], gd & dn[t], gany | up[t] | dn[t]
            co = bits(nu) + bits(nd)
            if co < a.min_days:
                continue
            g = group + [t]
            if len(g) >= 2:
                cands.append((co / bits(nany), co, g, nu, nd, bits(nany)))
            if len(g) < max_size:
                extend(g, nu, nd, nany, j + 1)

    for i, t in enumerate(tickers):
        extend([t], up[t], dn[t], up[t] | dn[t], i + 1)
    cands.sort(key=lambda c: (-c[0], -c[1], -len(c[2]), c[2]))

    # Distill.
    sel = []
    for c in cands:
        s = set(c[2])
        if any(s <= set(x[2]) for x in sel):
            continue  # subset of (or same as) a selected group
        inside = [x for x in sel if set(x[2]) < s]
        if inside:
            if all(c[0] >= 0.8 * x[0] for x in inside):
                sel = [x for x in sel if x not in inside] + [c]
            continue
        if len(sel) < a.top:
            sel.append(c)  # no overlap, or only partial overlap
    sel.sort(key=lambda c: (-c[0], -c[1], -len(c[2]), c[2]))
    sel = sel[: a.top]

    groups = []
    for score, co, g, gu, gd, nany in sel:
        ds = []
        for i in range(n_days):
            if gu >> i & 1 or gd >> i & 1:
                upday = bool(gu >> i & 1)
                bm = chg[a.benchmark][i]
                ds.append({
                    "date": days[i],
                    "direction": "up" if upday else "down",
                    "market_wide": bool(mw >> i & 1),
                    "bench_move": round(bm, 2),
                    "bench_opposite": (bm > 0) != upday and bm != 0,
                    "driver": None,
                    "sources": [],
                })
        pairs = [(x, y) for i, x in enumerate(g) for y in g[i + 1:]]
        groups.append({
            "tickers": g,
            "score": round(score, 4),
            "co_move_days": co,
            "up": bits(gu),
            "down": bits(gd),
            "any_move_days": nany,
            "market_wide_days": sum(1 for d in ds if d["market_wide"]),
            "market_wide_bench_opposite": sum(1 for d in ds if d["market_wide"] and d["bench_opposite"]),
            "return_corr": round(mean([corr(chg[x], chg[y]) for x, y in pairs]), 2),
            "beta": {t: round(beta[t], 2) for t in g},
            "dates": ds,
        })

    out = {
        "range_label": "",
        "start": days[0],
        "end": days[-1],
        "trading_days": n_days,
        "benchmark": a.benchmark,
        "benchmark_avg": round(avg[a.benchmark], 4),
        "avg_moves": {t: round(avg[t], 4) for t in tickers},
        "beta": {t: round(beta[t], 2) for t in tickers},
        "corr_benchmark": {t: round(corr_bench[t], 2) for t in tickers},
        "min_days": a.min_days,
        "max_group_size": max_size,
        "market_wide_days": [days[i] for i in range(n_days) if mw >> i & 1],
        "groups": groups,
    }
    with open(a.out, "w") as f:
        json.dump(out, f, indent=2)
    print(f"{len(groups)} groups, {n_days} trading days, "
          f"{len(out['market_wide_days'])} market-wide days -> {a.out}")
    if len(groups) < a.top:
        print(f"Note: only {len(groups)} groups had at least {a.min_days} co-move days.")


if __name__ == "__main__":
    main()
