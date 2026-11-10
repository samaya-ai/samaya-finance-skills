# Analysis spec: prices.csv → analysis.json

Write one helper in your working folder that does everything below and writes `analysis.json`. Standard library only. It must run on Python 3.9 (macOS `/usr/bin/python3`): no `X | Y` type hints unless `from __future__ import annotations` is first, no `match` statements. Settings are fixed for this skill: top groups = 10, minimum co-move days = 3, benchmark = the one chosen in Input (default SPY).

## 1. Read prices.csv

- Row 1 is the header. Strip spaces from every header cell. The first header cell must be `date` (any case); otherwise stop with "First column must be 'date'."
- The other header cells are the columns, in file order. One of them must be the benchmark; otherwise stop with "Benchmark X not found in the CSV columns."
- **Tickers** = every column except the benchmark, in file order. This order matters: it decides the order of tickers inside a group and breaks ties between groups.
- Skip any row that is empty or whose first cell is blank. For every other row, strip each cell, remove thousands commas ("1,234.5" → 1234.5) and read it as a number.
- A missing or blank cell is a gap. Collect every gap as "TICKER DATE" and, if there are any, stop and print them all under "Missing prices (ask the user for a price file):". Never fill, interpolate or drop a row to get past a gap.
- At least 3 data rows are needed (the seed close plus 2 trading days); otherwise stop.
- The first data row is the seed close. **Trading days** = every date after it; `n_days` = their count.

## 2. Daily moves

For every column, including the benchmark, and each trading day i (1 … n_days):

- **% change** = (close[i] / close[i−1] − 1) × 100.
- **Average move** `avg[t]` = mean of |% change| over all trading days of the range.

Keep full precision for all later math. Round only when writing the output.

## 3. Beta and correlation vs the benchmark

With x = the stock's daily % changes and b = the benchmark's, over all trading days:

- Sample covariance: cov(x, y) = Σ (x − mean x)(y − mean y) / (n_days − 1).
- **Beta** = cov(x, b) / cov(b, b).
- **Correlation** (Pearson) = cov(x, y) / √(cov(x, x) × cov(y, y)).

If any ticker or the benchmark has zero variance (a flat series), stop and report it; don't divide by zero.

## 4. Big moves

For each ticker (not the benchmark) and day, the day is a **big move** if |% change| > `avg[t]` (strictly greater).

- **Up** big move: % change > 0. **Down** big move: % change < 0.
- Keep, per ticker, the set of up days and the set of down days. A day can't be in both.

## 5. Market-wide days

A trading day is **market-wide** if either:

- |benchmark % change| > `avg[benchmark]` (strictly greater), or
- the number of tickers with an up big move that day, or the number with a down big move, is at least 0.75 × the number of tickers (max(n_up, n_down) ≥ 0.75 × count; no rounding).

Market-wide days stay in every count. They are only flagged.

## 6. Candidate groups

- **Largest size tested** `max_group_size` = the number of tickers if there are 12 or fewer, else 5.
- Test every combination of 2 to `max_group_size` tickers. Write each group's tickers in file order.
- For a group:
  - **Shared up days** = days where every member had an up big move. **Shared down days** = days where every member had a down big move.
  - **co_move_days** = shared up days + shared down days.
  - **any_move_days** = days where at least one member had a big move, in either direction.
  - **score** = co_move_days / any_move_days.
- Drop every group with co_move_days < 3. Adding a member can never add shared days, so you may stop extending any group that already has fewer than 3 (this keeps long lists fast). The result must equal testing every combination.
- **Sort** candidates by, in order: score high to low; co_move_days high to low; size large to small; then the ticker list compared item by item as text, A before Z (Python's list ordering).

## 7. Pick the top 10 (distill)

Go through the sorted candidates once, keeping a selected list that starts empty. For each candidate C:

1. If C's tickers are a subset of (or the same as) any selected group's tickers, skip C.
2. Otherwise, find the selected groups whose tickers are a **strict** subset of C's ("inside" groups).
   - If there is at least one: replace them with C only if C's score ≥ 0.8 × the score of **every** inside group (remove all the inside groups, add C). If not, skip C. Either way, go to the next candidate. A replacement is allowed even when 10 are already selected.
   - If there are none (no overlap, or only partial overlap with selected groups): add C only if fewer than 10 are selected.
3. After the pass, sort the selected list with the same key as step 6 and keep the first 10.

Partially overlapping groups (for example XOM + CVX and CVX + COP) can both be kept.

## 8. Per-group output

For each selected group, in final order:

- `dates`: every shared up or shared down day, oldest first. Each entry:
  - `date`: YYYY-MM-DD.
  - `direction`: `"up"` or `"down"`.
  - `market_wide`: true or false, from step 5.
  - `bench_move`: the benchmark's % change that day, rounded to 2 decimals.
  - `bench_opposite`: true when the benchmark moved against the group: (benchmark change > 0) differs from (direction is up), **and** the benchmark change is not exactly 0. Use the unrounded change.
  - `driver`: `null`. `sources`: `[]`. You fill these in step 3 of SKILL.md.
- `market_wide_days`: count of its dates with `market_wide` true.
- `market_wide_bench_opposite`: count of its dates with both `market_wide` and `bench_opposite` true.
- `return_corr`: Pearson correlation of daily % changes over the whole range for each pair of members; the group value is the plain mean across all pairs (one pair for a group of 2), rounded to 2 decimals.
- `beta`: each member's beta vs the benchmark, rounded to 2 decimals, in group order.

## 9. analysis.json shape

Field order as shown. Round only here: `score` to 4 decimals, averages to 4, betas and correlations to 2.

```json
{
  "range_label": "",
  "start": "2026-07-01",
  "end": "2026-09-30",
  "trading_days": 64,
  "benchmark": "SPY",
  "benchmark_avg": 0.6123,
  "avg_moves": {"XOM": 1.2345, "CVX": 1.1023},
  "beta": {"XOM": -0.41, "CVX": -0.38},
  "corr_benchmark": {"XOM": -0.22, "CVX": -0.2},
  "min_days": 3,
  "max_group_size": 5,
  "market_wide_days": ["2026-07-03", "2026-08-05"],
  "groups": [
    {
      "tickers": ["XOM", "CVX"],
      "score": 0.6129,
      "co_move_days": 19,
      "up": 9,
      "down": 10,
      "any_move_days": 31,
      "market_wide_days": 4,
      "market_wide_bench_opposite": 3,
      "return_corr": 0.86,
      "beta": {"XOM": -0.41, "CVX": -0.38},
      "dates": [
        {"date": "2026-07-03", "direction": "down", "market_wide": true,
         "bench_move": 0.84, "bench_opposite": true, "driver": null, "sources": []}
      ]
    }
  ]
}
```

- `range_label` is left empty here; you fill it in report.json.
- `start` / `end`: first and last trading day (not the seed date). `trading_days` = n_days.
- `avg_moves`, `beta`, `corr_benchmark`: tickers only, in file order; the benchmark is not in them. `benchmark_avg` is the benchmark's average move.
- `max_group_size`: the value used in step 6. `market_wide_days` (top level): every market-wide date in the range, oldest first.
- `up` / `down`: shared up days and shared down days.

After writing, print one line: "N groups, D trading days, M market-wide days". If fewer than 10 groups survived, also print "Note: only N groups had at least 3 co-move days." If no group survived, `groups` is an empty list; still build the page (it says so).

## 10. Self-checks before step 3

Run these on your own output and fix the helper if any fails:

- No gap in the prices; every ticker and the benchmark have n_days changes.
- Every group: `up + down = co_move_days`, `len(dates) = co_move_days`, `any_move_days ≥ co_move_days ≥ 3`, `score` = co_move_days / any_move_days (to 4 decimals), and 2 ≤ size ≤ `max_group_size`.
- Groups sorted by the step 6 key; at most 10; no group's tickers are a subset of another selected group's.
- Every date in a group is a big move in the same direction for every member (spot-check one date per group against the % changes).
- Each group's `market_wide_days` and `market_wide_bench_opposite` match its date flags.
- Spot-check one beta and one correlation by hand: a beta and the matching correlation with the benchmark have the same sign.
