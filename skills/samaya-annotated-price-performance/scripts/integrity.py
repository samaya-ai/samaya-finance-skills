#!/usr/bin/env python3
"""Check (and only when unambiguous, repair) a stock's daily candles against its benchmark.

Usage: integrity.py <stock_prefix> <bench_prefix> <raw_dir> <out_dir>

Raw slice files: <raw_dir>/<prefix>_*.txt, first line '# url=<u> title=<t>'.
Stock rows 'date | o | h | l | c | vol'; benchmark rows 'date close' (or full candles).
Writes <out_dir>/<prefix>_clean.txt (stock) and <out_dir>/<bench>_clean.txt, plus integrity.json.

Defects handled:
  * duplicate bars   - a bar whose open/high/low/close equal the previous bar's is a copy, dropped
  * date shift       - labels off by whole days (e.g. local-midnight timestamps rendered in UTC)
  * corrupt volume   - a volume below 1% of the series median is set to missing and flagged
A repair is applied only if exactly one shift makes the stock calendar equal the benchmark
calendar AND gives a return correlation >= MIN_CORR that beats every other shift by MARGIN.
Anything else blocks: the chart is never built on data that only might be right.
"""
import datetime as dt, glob, json, re, statistics as st, sys

MIN_CORR, MARGIN, VOL_FLOOR, MAX_GAPS = 0.5, 0.25, 0.01, 2


def parse_vol(s):
    s = s.strip().upper()
    mult = {"K": 1e3, "M": 1e6, "B": 1e9}.get(s[-1], 1)
    return float(s[:-1] if s[-1] in "KMB" else s) * mult


def load(prefix, raw_dir, full):
    rows, src = {}, []
    for f in sorted(glob.glob(f"{raw_dir}/{prefix}_*.txt")):
        lines = open(f).read().strip().splitlines()
        m = re.match(r"# url=(\S+) title=(.*)", lines[0])
        if not m:
            sys.exit(f"BLOCK: {f} has no source header")
        src.append({"url": m.group(1), "title": m.group(2).strip()})
        for ln in lines[1:]:
            p = [x for x in re.split(r"\s*\|\s*|\s+", ln.strip()) if x]
            if full:
                rows[p[0]] = (float(p[1]), float(p[2]), float(p[3]), float(p[4]), parse_vol(p[5]))
            else:
                rows[p[0]] = float(p[4] if len(p) >= 6 else p[1])
    return dict(sorted(rows.items())), src


def weekend(d):
    return dt.date.fromisoformat(d).weekday() >= 5


def corr(a, b):
    ds = sorted(set(a) & set(b))
    pairs = [(a[y] / a[x] - 1, b[y] / b[x] - 1) for x, y in zip(ds, ds[1:])]
    if len(pairs) < 20:
        return 0.0, len(pairs)
    xs, ys = zip(*pairs)
    mx, my = st.fmean(xs), st.fmean(ys)
    num = sum((p - mx) * (q - my) for p, q in pairs)
    den = (sum((p - mx) ** 2 for p in xs) * sum((q - my) ** 2 for q in ys)) ** 0.5
    return (num / den if den else 0.0), len(pairs)


def main():
    sp, bp, raw_dir, out_dir = sys.argv[1:5]
    S, s_src = load(sp, raw_dir, True)
    B, b_src = load(bp, raw_dir, False)
    log = {"stock": sp, "bench": bp, "issues": [], "repair": None}

    # benchmark must itself be clean
    bw = [d for d in B if weekend(d)]
    if bw:
        sys.exit(f"BLOCK: benchmark {bp} has weekend dates {bw[:5]}")

    # 1. duplicate bars
    keys = list(S)
    dups = [keys[i] for i in range(1, len(keys)) if S[keys[i]][:4] == S[keys[i - 1]][:4]]
    if dups:
        log["issues"].append(f"{len(dups)} duplicate bars (identical OHLC to the previous bar) dropped")
    S = {d: v for d, v in S.items() if d not in set(dups)}

    # 2. corrupt volume
    med = st.median(v[4] for v in S.values())
    badv = [d for d, v in S.items() if v[4] < VOL_FLOOR * med]
    if badv:
        log["issues"].append(f"volume implausible on {len(badv)} bar(s) ({', '.join(badv)}); treated as missing")

    # 3. date alignment
    sw = [d for d in S if weekend(d)]
    closes = {d: v[3] for d, v in S.items()}
    lo, hi = max(min(S), min(B)), min(max(S), max(B))
    def shifted(k):
        return {(dt.date.fromisoformat(d) + dt.timedelta(days=k)).isoformat(): v for d, v in S.items()}
    def cal_ok(k):
        sh = shifted(k); a = {d for d in sh if lo < d < hi}; b = {d for d in B if lo < d < hi}
        extra, missing = sorted(a - b), sorted(b - a)
        return (not extra and len(missing) <= MAX_GAPS), extra[:3], missing
    scores = {k: corr({d: v[3] for d, v in shifted(k).items()}, B)[0] for k in (-2, -1, 0, 1, 2)}
    log["correlation_by_shift"] = {str(k): round(v, 3) for k, v in scores.items()}
    best = max(scores, key=scores.get)
    runner = max(v for k, v in scores.items() if k != best)
    ok0 = cal_ok(0)
    gaps = []
    if not sw and ok0[0] and best == 0:
        gaps = ok0[2]
    else:
        okb = cal_ok(best)
        if best != 0 and okb[0] and scores[best] >= MIN_CORR and scores[best] - runner >= MARGIN:
            S = shifted(best)
            log["repair"] = (f"dates shifted {best:+d} day(s): correlation with {bp} {scores[0]:.2f} as labelled, "
                             f"{scores[best]:.2f} after shift; repaired calendar matches {bp}" + (f" except {len(okb[2])} vendor gap(s)" if okb[2] else " exactly"))
            badv = [(dt.date.fromisoformat(d) + dt.timedelta(days=best)).isoformat() for d in badv]
            gaps = okb[2]
        else:
            sys.exit("BLOCK: stock calendar does not match the benchmark and no unambiguous repair exists. "
                     f"weekend labels: {sw[:5]}; correlation by shift: {log['correlation_by_shift']}; "
                     f"as-labelled calendar diff: {ok0[1:]}")
    if gaps:
        log["issues"].append(f"vendor gap: no genuine bar for {', '.join(gaps)}; returns span the gap on both series")
        B = {d: c for d, c in B.items() if d not in set(gaps)}
    log["gaps"] = gaps
    # trim to the benchmark's coverage: a copied bar at a slice edge has no predecessor to reveal it
    edge = [d for d in S if not (min(B) <= d <= max(B))]
    if edge:
        log["issues"].append(f"{len(edge)} bar(s) outside the benchmark's dates dropped at the edges: {', '.join(edge)}")
        S = {d: v for d, v in S.items() if d not in set(edge)}
    if any(weekend(d) for d in S):
        sys.exit("BLOCK: weekend dates remain after repair")

    with open(f"{out_dir}/{sp}_clean.txt", "w") as f:
        f.write("# " + json.dumps({"sources": s_src}) + "\n")
        for d, (o, h, l, c, v) in S.items():
            f.write(f"{d} | {o} | {h} | {l} | {c} | {'' if d in badv else v}\n")
    with open(f"{out_dir}/{bp}_clean.txt", "w") as f:
        f.write("# " + json.dumps({"sources": b_src}) + "\n")
        for d, c in B.items():
            f.write(f"{d} {c}\n")
    log["bad_volume_dates"] = badv
    json.dump(log, open(f"{out_dir}/integrity_{sp}.json", "w"), indent=1)
    print(json.dumps(log, indent=1))


if __name__ == "__main__":
    main()
