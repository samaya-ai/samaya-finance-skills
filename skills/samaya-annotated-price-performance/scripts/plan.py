#!/usr/bin/env python3
"""Print the candle pulls to make, as ready-to-send Samaya questions.

Usage: plan.py <ticker> <benchmark> <window_start> <window_end> [sector=<etf>]

A single candle pull keeps only the most recent ~100 sessions and silently drops the rest, so
pulls are sliced into windows of at most SLICE_DAYS calendar days. The first slice starts
LOOKBACK_DAYS before the window: beta, normal daily variation and the volume baseline need about
three months of history before the first charted day.
"""
import datetime as dt
import sys

SLICE_DAYS = 120      # ~85 sessions, safely under the ~100-row cap
LOOKBACK_DAYS = 95    # >= 61 sessions of history before the window


def slices(start, end):
    out, a = [], start
    while a <= end:
        b = min(a + dt.timedelta(days=SLICE_DAYS - 1), end)
        out.append((a, b))
        a = b + dt.timedelta(days=1)
    return out


def main():
    if len(sys.argv) < 5:
        sys.exit(__doc__)
    tk, bk, ws, we = sys.argv[1:5]
    opts = dict(a.split("=", 1) for a in sys.argv[5:])
    w0, w1 = dt.date.fromisoformat(ws), dt.date.fromisoformat(we)
    first = w0 - dt.timedelta(days=LOOKBACK_DAYS)
    series = [(tk, "stock"), (bk, "benchmark")] + ([(opts["sector"], "sector")] if opts.get("sector") else [])
    print(f"Window {w0} to {w1}; pulls start {first} for lookback. One financial_qa call per line,\n"
          f"each in a fresh session. Save each reply verbatim to raw/<prefix>_<n>.txt (see references/data-pulls.md).\n")
    for sym, role in series:
        for n, (a, b) in enumerate(slices(first, w1), 1):
            print(f"[{role} {sym} slice {n}] Daily stock candles (open, high, low, close, volume) for {sym} "
                  f"from {a} to {b}, as a date-indexed table.")
        print()


if __name__ == "__main__":
    main()
