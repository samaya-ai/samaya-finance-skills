#!/usr/bin/env python3
"""Merge sliced Samaya candle pulls and compute the event-day layer.

Usage: compute.py <ticker> <bench> <window_start> <window_end> <data_dir> <out.json> [opts]
  opts: clean=1                     read <data_dir>/<ticker>_clean.txt and <bench>_clean.txt (integrity.py output)
        sector=<prefix> sector_raw=<dir> sector_lag=prior|same   optional sector factor (prior = foreign
                                    session that closed before this market opened, e.g. US semis for Seoul)
        exclude=<weight>@<date>     constituent removal when the stock is a large benchmark weight
        calendar=us|none            mechanical-volume calendar (quarterly expiry, Russell reconstitution)

Slice files: <data_dir>/<ticker>_*.txt and <bench>_*.txt. First line of each is
'# url=<samaya url> title=<reference title>'. Stock rows: 'date | o | h | l | c | vol';
benchmark rows may be 'date close' or the full candle form.
"""
import glob, json, math, re, statistics, sys

Z_MIN = 2.5        # abnormal-return z-score threshold
RVOL_MIN = 1.75    # relative-volume gate for mid-size moves (vs trailing 50-session median)
Z_ALWAYS = 4.0     # abnormal moves this large qualify regardless of volume
CAP = 10_000       # no cap: the thresholds decide; every candidate is researched and shown
EST_WIN = 60       # trailing window for beta and residual sigma
VOL_WIN = 50       # trailing window for average volume
ZIGZAG = 0.20      # turning-point reversal threshold


def parse_vol(s):
    s = s.strip().upper()
    mult = {"K": 1e3, "M": 1e6, "B": 1e9}.get(s[-1], 1)
    return float(s[:-1] if s[-1] in "KMB" else s) * mult


def load_clean(path, full):
    lines = open(path).read().strip().splitlines()
    meta = json.loads(lines[0][2:]); rows = {}
    for ln in lines[1:]:
        p = [x.strip() for x in ln.split("|")] if full else ln.split()
        if full:
            rows[p[0]] = {"o": float(p[1]), "h": float(p[2]), "l": float(p[3]), "c": float(p[4]), "v": float(p[5]) if p[5] else None}
        else:
            rows[p[0]] = {"c": float(p[1])}
    return rows, meta["sources"]


def load(prefix, data_dir, full):
    rows, sources = {}, []
    for f in sorted(glob.glob(f"{data_dir}/{prefix.lower()}_*.txt")):
        lines = open(f).read().strip().splitlines()
        m = re.match(r"# url=(\S+) title=(.*)", lines[0])
        if not m:
            sys.exit(f"BLOCK: {f} has no source header")
        sources.append({"url": m.group(1), "title": m.group(2).strip()})
        for ln in lines[1:]:
            parts = [p.strip() for p in re.split(r"\s*\|\s*|\s+", ln.strip()) if p.strip()]
            d = parts[0]
            if full:
                o, h, l, c = map(float, parts[1:5])
                rows[d] = {"o": o, "h": h, "l": l, "c": c, "v": parse_vol(parts[5])}
            else:
                rows[d] = {"c": float(parts[4] if len(parts) >= 6 else parts[1])}
    return rows, sources


def ols2(y, x1, x2):
    """Slopes of y on (x1, x2) with an intercept, via the 2x2 normal equations on demeaned data."""
    m = lambda v: statistics.fmean(v)
    y_, a_, b_ = [v - m(y) for v in y], [v - m(x1) for v in x1], [v - m(x2) for v in x2]
    saa = sum(v * v for v in a_); sbb = sum(v * v for v in b_); sab = sum(p * q for p, q in zip(a_, b_))
    say = sum(p * q for p, q in zip(a_, y_)); sby = sum(p * q for p, q in zip(b_, y_))
    det = saa * sbb - sab * sab
    if abs(det) < 1e-18:
        return ols_beta(y, x1), 0.0
    return (say * sbb - sby * sab) / det, (sby * saa - say * sab) / det


def ols_beta(y, x):
    mx, my = statistics.fmean(x), statistics.fmean(y)
    vx = sum((a - mx) ** 2 for a in x)
    return sum((a - mx) * (b - my) for a, b in zip(x, y)) / vx if vx else 1.0


def us_mechanical_days(dates):
    """Days with index-driven volume: quarterly expiry (3rd Friday of Mar/Jun/Sep/Dec, or the prior
    session if that Friday is a holiday) and the Russell reconstitution (last Friday of June, same rule)."""
    import datetime as dt
    have, out = set(dates), {}
    years = {int(d[:4]) for d in dates}
    for y in years:
        for m in (3, 6, 9, 12):
            f = [dt.date(y, m, k) for k in range(1, 32) if k <= 28 or (dt.date(y, m, 1) + dt.timedelta(days=k - 1)).month == m]
            fridays = [x for x in f if x.weekday() == 4]
            cands = [("Quarterly options and index futures expiry", fridays[2])]
            if m == 6: cands.append(("Russell index reconstitution", fridays[-1]))
            for label, x in cands:
                while x.isoformat() not in have and x > dt.date(y, m, 1): x -= dt.timedelta(days=1)
                if x.isoformat() in have: out[x.isoformat()] = label
    return out


def mad_sigma(xs):
    med = statistics.median(xs)
    return 1.4826 * statistics.median([abs(v - med) for v in xs])


def zigzag(dates, closes, thr):
    """Swing highs/lows: a pivot is confirmed once price reverses >= thr from it."""
    pts, trend, ext = [], 0, 0
    for i in range(1, len(closes)):
        c = closes[i]
        if trend == 0:
            if c >= closes[ext] * (1 + thr):
                pts.append({"date": dates[ext], "kind": "low", "close": closes[ext]}); trend, ext = 1, i
            elif c <= closes[ext] * (1 - thr):
                pts.append({"date": dates[ext], "kind": "high", "close": closes[ext]}); trend, ext = -1, i
        elif trend > 0:
            if c > closes[ext]:
                ext = i
            elif c <= closes[ext] * (1 - thr):
                pts.append({"date": dates[ext], "kind": "high", "close": closes[ext]}); trend, ext = -1, i
        else:
            if c < closes[ext]:
                ext = i
            elif c >= closes[ext] * (1 + thr):
                pts.append({"date": dates[ext], "kind": "low", "close": closes[ext]}); trend, ext = 1, i
    return pts


def main():
    tk, bk, ws, we, data_dir, out = sys.argv[1:7]
    opts = dict(a.split("=", 1) for a in sys.argv[7:])  # sector=<prefix> sector_raw=<dir> sector_lag=prior|same clean=1
    if opts.get("clean"):
        s, s_src = load_clean(f"{data_dir}/{tk}_clean.txt", True)
        b, b_src = load_clean(f"{data_dir}/{bk}_clean.txt", False)
    else:
        s, s_src = load(tk, data_dir, True)
        b, b_src = load(bk, data_dir, False)
    sec, sec_src = (load(opts["sector"], opts.get("sector_raw", data_dir), False) if opts.get("sector") else ({}, []))

    # Continuity: the two calendars must match exactly; a missing session blocks.
    ds, db = set(s), set(b)
    if ds != db:
        sys.exit(f"BLOCK: calendar mismatch. Missing from {tk}: {sorted(db-ds)[:10]}; "
                 f"missing from {bk}: {sorted(ds-db)[:10]}")
    dates = sorted(ds)
    gaps = [(a, c) for a, c in zip(dates, dates[1:])
            if (int(c.replace("-", "")) - int(a.replace("-", ""))) > 4 and a[5:7] == c[5:7]]
    if gaps:
        print("WARN: gaps >4 calendar days inside a month (check holidays):", gaps)
    if dates[0] > ws or dates[-1] < we:
        sys.exit(f"BLOCK: data {dates[0]}..{dates[-1]} does not cover window {ws}..{we}")
    first_win = next(i for i, d in enumerate(dates) if d >= ws)
    if first_win < EST_WIN + 1:
        sys.exit(f"BLOCK: only {first_win} lookback sessions; need {EST_WIN + 1}")

    C = [s[d]["c"] for d in dates]
    B = [b[d]["c"] for d in dates]
    V = [s[d]["v"] for d in dates]
    r = [None] + [C[i] / C[i - 1] - 1 for i in range(1, len(C))]
    rb = [None] + [B[i] / B[i - 1] - 1 for i in range(1, len(B))]
    # constituent removal: when the stock is a large index weight, its own move contaminates the
    # benchmark. exclude=<weight>@<date> anchors the weight; it then drifts with relative price
    # (w_t = w_a * (P_t/P_a) / (I_t/I_a)), and the market return becomes the index ex the stock:
    # r_ex = (r_index - w_{t-1} * r_stock) / (1 - w_{t-1}).
    wpath = None
    if opts.get("exclude"):
        w_a, d_a = opts["exclude"].split("@"); w_a = float(w_a)
        if d_a not in s: sys.exit(f"BLOCK: weight anchor date {d_a} not in the series")
        Pa, Ia = s[d_a]["c"], b[d_a]["c"]
        wpath = [w_a * (C[i] / Pa) / (B[i] / Ia) for i in range(len(dates))]
        if max(wpath) >= 0.6: sys.exit("BLOCK: implied index weight above 60%; constituent removal unreliable")
        rb = [None] + [(rb[i] - wpath[i - 1] * r[i]) / (1 - wpath[i - 1]) for i in range(1, len(dates))]
    # sector factor. "prior": a local session on date t sees foreign sessions dated before t
    # (a US close lands before the next Asian open), so its sector move is the foreign index's
    # change between the last foreign close before t-1's session and the last before t's.
    rs = [0.0] * len(dates)
    if sec:
        sd = sorted(sec)
        def level(d):
            prior = [x for x in sd if (x < d if opts.get("sector_lag", "prior") == "prior" else x <= d)]
            return sec[prior[-1]]["c"] if prior else None
        lv = [level(d) for d in dates]
        if None in lv[1:]:
            sys.exit("BLOCK: sector series does not cover the window")
        rs = [0.0] + [lv[i] / lv[i - 1] - 1 for i in range(1, len(dates))]

    Bx = [B[0]]
    for i in range(1, len(dates)): Bx.append(Bx[-1] * (1 + rb[i]))
    days = []
    for i in range(first_win, len(dates)):
        if dates[i] > we:
            break
        y, x, xs = r[i - EST_WIN:i], rb[i - EST_WIN:i], rs[i - EST_WIN:i]
        if sec:
            beta, beta2 = ols2(y, x, xs)
        else:
            beta, beta2 = ols_beta(y, x), 0.0
        resid = [a - beta * c - beta2 * e for a, c, e in zip(y, x, xs)]
        sig = mad_sigma(resid)
        abn = r[i] - beta * rb[i] - beta2 * rs[i]
        vols = [v for v in V[i - VOL_WIN:i] if v]
        avgv = statistics.median(vols)
        days.append({
            "date": dates[i], **s[dates[i]], "bench": Bx[i], "bench_raw": B[i], "w": wpath[i] if wpath else None,
            "ret": r[i], "bench_ret": rb[i], "beta": beta, "abn": abn,
            "sec_ret": rs[i], "beta2": beta2, "sec_part": beta2 * rs[i],
            "sigma": sig, "z": abn / sig if sig else 0.0,
            "avg_vol": avgv, "rvol": (V[i] / avgv) if V[i] else None,
        })

    mech = us_mechanical_days([d["date"] for d in days]) if opts.get("calendar", "us") == "us" else {}
    for d in days: d["mech"] = mech.get(d["date"])
    # on mechanical days volume is index-driven, so only the price-only path can flag them
    cands = [d for d in days if abs(d["z"]) >= Z_ALWAYS or (abs(d["z"]) >= Z_MIN and (d["rvol"] or 0) >= RVOL_MIN and not d["mech"])]
    cands.sort(key=lambda d: -abs(d["abn"]))
    events = sorted(cands[:CAP], key=lambda d: d["date"])
    over_cap = [d["date"] for d in cands[CAP:]]
    # Days that moved a lot but the market explains it: shown as context only.
    mkt = [d["date"] for d in days if abs(d["ret"]) >= 2.5 * d["sigma"] and abs(d["z"]) < Z_MIN]
    # Heavy-volume days with no abnormal move: candidates for mechanical causes.
    vol_only = [d["date"] for d in days if (d["rvol"] or 0) >= 2.5 and abs(d["z"]) < Z_MIN]
    mech_vol = [{"date": d["date"], "label": d["mech"], "rvol": d["rvol"]} for d in days if d["mech"] and (d["rvol"] or 0) >= 1.75]

    win_c = [d["c"] for d in days]
    # turning-point threshold scales with the stock's own volatility: 1.5x monthly vol, clamped 10-25%
    zz = min(0.25, max(0.10, 1.5 * statistics.pstdev([d["ret"] for d in days]) * 21 ** 0.5))
    base = C[first_win - 1]
    total = days[-1]["c"] / base - 1
    ev_set = {e["date"] for e in events}
    ev_comp = math.prod(1 + d["ret"] for d in days if d["date"] in ev_set) - 1
    other_comp = math.prod(1 + d["ret"] for d in days if d["date"] not in ev_set) - 1
    bench_total = days[-1]["bench"] / Bx[first_win - 1] - 1
    bench_raw_total = B[-1] / B[first_win - 1] - 1

    res = {
        "ticker": tk, "benchmark": bk, "window": [days[0]["date"], days[-1]["date"]],
        "base_close": base, "base_date": dates[first_win - 1],
        "params": {"z_min": Z_MIN, "z_always": Z_ALWAYS, "rvol_min": RVOL_MIN, "cap": CAP, "est_win": EST_WIN,
                   "vol_win": VOL_WIN, "zigzag": round(zz, 3)},
        "sources": {"stock": s_src, "bench": b_src, "sector": sec_src},
        "exclude": opts.get("exclude"), "weight_path": {"start": wpath[dates.index(ws) if ws in dates else 0] if wpath else None,
                                                        "end": wpath[-1] if wpath else None, "max": max(wpath) if wpath else None},
        "sector": opts.get("sector"), "sector_lag": opts.get("sector_lag", "prior") if sec else None,
        "summary": {"total_ret": total, "bench_ret": bench_total, "bench_raw_ret": bench_raw_total, "n_sessions": len(days),
                    "n_events": len(events), "event_days_ret": ev_comp, "other_days_ret": other_comp,
                    "hi": max(win_c), "lo": min(win_c)},
        "days": days,
        "event_days": [{k: e[k] for k in ("date", "ret", "bench_ret", "abn", "z", "rvol", "v", "c")} for e in events],
        "candidates": [{k: c[k] for k in ("date", "ret", "bench_ret", "abn", "z", "rvol")} for c in sorted(cands, key=lambda d: d["date"])],
        "over_cap": over_cap, "market_days": mkt, "volume_only_days": vol_only,
        "mechanical_days": mech_vol,
        "turning_points": zigzag([d["date"] for d in days], win_c, zz),
    }
    json.dump(res, open(out, "w"), indent=1)
    print(f"{tk}: {len(days)} sessions {days[0]['date']}..{days[-1]['date']}  "
          f"total {total:+.1%}  vs {bk} {bench_total:+.1%}")
    print(f"event days {len(events)} -> {ev_comp:+.1%}; other sessions {other_comp:+.1%}")
    for e in events:
        print(f"  {e['date']}  ret {e['ret']:+.1%}  mkt part {e['beta']*e['bench_ret']:+.1%}  sector part {e['sec_part']:+.1%}  abn {e['abn']:+.1%}  "
              f"z {e['z']:+.1f}  rvol {(e['rvol'] or 0):.1f}x")
    print("over cap:", over_cap)
    print("market-explained days:", mkt)
    print("volume-only days:", vol_only)
    print("mechanical heavy-volume days:", [(m["date"], m["label"][:20], round(m["rvol"], 1)) for m in mech_vol]); print("zigzag", round(zz, 3))
    print("turning points:", [(t["date"], t["kind"], t["close"]) for t in res["turning_points"]])


if __name__ == "__main__":
    main()
