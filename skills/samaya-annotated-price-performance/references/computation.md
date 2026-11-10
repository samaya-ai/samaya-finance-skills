# Computation: plan, integrity, screen, phase numbers

This file specifies every number the page rests on. Write your own helper code for it in the
scratch working folder (Python with only the standard library is enough: `statistics`, `math`,
`json`, `datetime`, `re`, `glob`), run it, and read its printed output. It must run on
Python 3.9 (macOS `/usr/bin/python3`): no `X | Y` type hints unless `from __future__ import annotations` is first, no `match` statements. Compute covariance, correlation and beta with the formulas below: `statistics.correlation`, `covariance` and `linear_regression` need Python 3.10+. Do not compute any of
this by hand or in your head, and never hand-edit the data to make a step pass.

Use exactly the parameters below. They are the screen's calibration; changing them changes which
days get a story.

| Name | Value | Meaning |
|---|---|---|
| `SLICE_DAYS` | 120 | Calendar days per candle pull (~85 sessions, under the ~100-row cap) |
| `LOOKBACK_DAYS` | 95 | Calendar days pulled before the window (>= 61 sessions of history) |
| `EST_WIN` | 60 | Trailing sessions for beta and the stock's normal variation |
| `VOL_WIN` | 50 | Trailing sessions for the volume baseline |
| `Z_MIN` | 2.5 | `strong` threshold, and the run threshold |
| `RVOL_MIN` | 1.75 | Heavy volume, as a multiple of the 50-session median |
| `Z_PRICE` | 3.0 | `price` (any-volume) threshold |
| `VOL_ONLY` | 2.0 | Volume-only listing threshold |
| `TOP_N_PER_YEAR` | 10 | Top-move guarantee per 252 sessions (minimum 5) |
| `RUN_LEN` | 10 | Sessions in a run window |
| Integrity `MIN_CORR` | 0.5 | Minimum return correlation for a date-shift repair |
| Integrity `MARGIN` | 0.25 | Required lead over every other shift |
| Integrity `VOL_FLOOR` | 0.01 | Volume below 1% of the series median is implausible |
| Integrity `MAX_GAPS` | 2 | Genuine vendor gaps tolerated |

## Contents
1. Pull plan
2. Parsing the raw slices
3. Integrity check
4. The screen (out.json)
5. Phase numbers

## 1. Pull plan

Inputs: ticker, benchmark, window start `w0`, window end `w1`, optional sector series.

- First pull date = `w0 - 95 days`.
- Slices: starting at the first pull date, take `[a, min(a + 119 days, w1)]`, then start the next
  slice the day after its end; repeat while `a <= w1`.
- For each series in order (stock, benchmark, then sector if used) and each slice `n` (from 1),
  the question is exactly:
  `Daily stock candles (open, high, low, close, volume) for <SYMBOL> from <a> to <b>, as a date-indexed table.`
- Each question is its own `financial_qa` call in a fresh session. Save the reply as
  `raw/<prefix>_<n>.txt` in the format of `data-pulls.md` section 2.

## 2. Parsing the raw slices

- Read every `raw/<prefix>_*.txt` in sorted filename order. The first line must match
  `# url=<non-space url> title=<rest of line>`; a file without it **blocks**. Keep each
  `{url, title}` as that series' source list.
- Split each later line on `|` or whitespace, dropping empty pieces.
- Stock rows: `date, open, high, low, close, volume`. Volume: upper-case it; a trailing `K`, `M`
  or `B` multiplies the number by 1e3, 1e6 or 1e9; otherwise it is a bare number.
- Benchmark and sector rows: if a row has 6 or more pieces the close is piece 5 (the candle
  form), otherwise piece 2 (`date close`).
- Merge slices by date; a later file's row for the same date overwrites an earlier one. Sort by
  date.

## 3. Integrity check

Runs on the parsed stock (full candles) and benchmark (closes) before anything is computed.
Order matters.

1. **Benchmark weekends.** Any benchmark date on a Saturday or Sunday **blocks**.
2. **Copied bars.** Walking the stock series in date order, a bar whose open, high, low and close
   all equal the previous bar's is a copy. Drop it. Log
   `"<n> duplicate bars (identical OHLC to the previous bar) dropped"`.
3. **Implausible volume.** `med` = median of all stock volumes after step 2. A bar with volume
   `< 0.01 * med` keeps its prices but its volume becomes missing. Log
   `"volume implausible on <n> bar(s) (<dates>); treated as missing"`.
4. **Date alignment.** Let `lo` = the later of the two series' first dates and `hi` = the earlier
   of their last dates. For a shift `k` in days, shift every stock date by `k`.
   - *Calendar test for `k`*: take the shifted stock dates and the benchmark dates strictly
     between `lo` and `hi`. `extra` = stock-only dates, `missing` = benchmark-only dates. The
     calendar passes if `extra` is empty and `missing` has at most 2 dates.
   - *Correlation for `k`*: on the dates common to the shifted stock closes and the benchmark,
     pair consecutive common dates and compute each series' simple return between them. With
     fewer than 20 pairs the correlation is 0; otherwise it is the Pearson correlation of the
     pairs.
   - Score shifts `k = -2, -1, 0, +1, +2`. `best` = highest correlation; `runner` = highest
     among the others.
   - If the stock has no weekend dates, shift 0 passes the calendar test and `best == 0`: no
     repair; the gaps are shift 0's `missing` dates.
   - Otherwise repair only if `best != 0`, shift `best` passes the calendar test,
     `corr(best) >= 0.5` and `corr(best) - runner >= 0.25`. Apply the shift to all stock dates
     (and to the missing-volume dates). The gaps are that shift's `missing` dates. Log the repair
     as `"dates shifted <+k> day(s): correlation with <bench> <c0> as labelled, <cb> after shift;
     repaired calendar matches <bench> exactly"` (or `"except <n> vendor gap(s)"`), correlations
     to 2 decimals.
   - Anything else **blocks**, reporting the weekend labels, the correlation for each shift and
     the as-labelled calendar difference.
5. **Vendor gaps.** If there are gaps, log `"vendor gap: no genuine bar for <dates>; returns span
   the gap on both series"` and remove those dates from the benchmark, so returns span the gap on
   both series.
6. **Edges.** Drop stock bars dated before the benchmark's first date or after its last (a
   copied bar at a slice edge has no predecessor to reveal it). Log
   `"<n> bar(s) outside the benchmark's dates dropped at the edges: <dates>"`.
7. Any stock date still on a weekend **blocks**.

Keep the cleaned series (stock rows with missing volume left empty; benchmark closes), the
source lists, and an integrity log with: `stock`, `bench`, `issues` (the logged lines),
`repair` (the repair line or null), `correlation_by_shift` (3 decimals), `gaps`,
`bad_volume_dates`. The `repair` line and every `issues` line must be stated in the page's
method notes. On a block, stop and tell the person what failed.

## 4. The screen (out.json)

Inputs: the cleaned stock and benchmark, window start `ws` and end `we`, and the options in
`data-pulls.md` section 6 (sector factor, constituent removal). Mechanical-volume days are
computed for US listings; for other listings there are none.

### 4a. Preconditions (each failure blocks)

- The stock and benchmark date sets must be identical after integrity; report dates missing
  from each side.
- Warn (do not block) when two consecutive sessions in the same calendar month are more than 4
  days apart: check those for holidays.
- The data must cover the window: first date `<= ws` and last date `>= we`.
- `first_win` = index of the first date `>= ws`. It must be at least 61 (`EST_WIN + 1`)
  lookback sessions.

### 4b. Series

Over all loaded dates (`C` = stock closes, `B` = benchmark closes, `V` = stock volumes):

- `r[i] = C[i]/C[i-1] - 1`, `rb[i] = B[i]/B[i-1] - 1` (none at `i = 0`).
- **Constituent removal** (`exclude = w_a @ d_a`): `d_a` must be a session, else block. Weight
  path `w[i] = w_a * (C[i]/C[d_a]) / (B[i]/B[d_a])`. If `max(w) >= 0.6`, block. Then replace the
  benchmark return with the index excluding the stock:
  `rb[i] = (rb[i] - w[i-1] * r[i]) / (1 - w[i-1])`.
- **Sector factor** (optional; default 0 for every day). One series, or an equal-weight basket
  `a+b+c`: take the dates common to all members, normalise each member to its close on the first
  common date, and average. For each stock date `d`, the sector level is the last sector close
  dated strictly before `d` (`sector_lag=prior`, the default) or on or before `d`
  (`sector_lag=same`). If any date after the first has no level, block.
  `rs[i] = level[i]/level[i-1] - 1`, `rs[0] = 0`.
- Rebuilt benchmark level `Bx[0] = B[0]`, `Bx[i] = Bx[i-1] * (1 + rb[i])` (differs from `B`
  only under constituent removal).

### 4c. Per-day values

For each `i` from `first_win` while `date[i] <= we`, using the 60 sessions **before** `i`
(indices `i-60 .. i-1`; day `i` itself is excluded):

- `beta`: OLS slope, with intercept, of stock returns on benchmark returns:
  `cov(r, rb) / var(rb)` on the window; if `var(rb)` is 0, beta = 1.0.
  With a sector factor, `beta` and `beta2` are the two slopes of a regression with intercept on
  `rb` and `rs` (solve the 2x2 normal equations on demeaned data); if the determinant's absolute
  value is below 1e-18, use the one-factor beta and `beta2 = 0`. Without a sector,
  `beta2 = 0`.
- Residuals on the window: `r - beta*rb - beta2*rs` (no intercept removed).
- `sigma` = 1.4826 x median absolute deviation of those residuals from their median.
- `abn = r[i] - beta*rb[i] - beta2*rs[i]` (the stock-specific move).
- `z = abn / sigma` (0 if sigma is 0).
- `avg_vol` = median of the non-missing volumes in the 50 sessions before `i`.
- `rvol = V[i] / avg_vol`, or null when `V[i]` is missing.
- `sec_part = beta2 * rs[i]`.

Each day record holds: `date, o, h, l, c, v, bench (= Bx[i]), bench_raw (= B[i]), w (weight or
null), ret, bench_ret, beta, abn, sec_ret, beta2, sec_part, sigma, z, avg_vol, rvol, mech,
signal`.

### 4d. Index-mechanics days (US listings)

For every year in the window and each of March, June, September and December: the third Friday
is "Quarterly options and index futures expiry"; in June the last Friday is also "Russell index
reconstitution". If that date is not a session, step back one day at a time (not past the 1st of
the month) to the nearest earlier session. `mech` = that label on those days, else null.

### 4e. Signals

1. `strong`: `|z| >= 2.5` and `(rvol or 0) >= 1.75` and not a mech day.
2. Otherwise `price`: `|z| >= 3.0` (any volume).
3. Top-move guarantee: `top_n = max(5, round(10 * sessions / 252))`, where `sessions` is the
   number of window sessions (the length of `days`), not counting the lookback (Python `round`, halves to
   even). For each of `abn` and `ret` separately, take the `top_n` days with the largest absolute
   value; any of them with no signal yet and `|z| >= 2.0` becomes `rank`.
4. `candidates` = every day with a signal, in date order. These are the flagged days.

### 4f. Runs

For each window of 10 consecutive sessions (ending at index 9 onward): take the sessions in it
that are **not** flagged; skip the window if fewer than 5. `cum` = arithmetic sum of their
`abn`; `sd` = square root of the sum of their `sigma^2`. A hit when `|cum/sd| >= 2.5`, recorded
as `{start, end, abn: cum, z: cum/sd}`.

Merge hits in order: if a hit starts on or before the previous run's end and has the same sign
of `abn`, extend that run's end to the hit's end, and if the hit's `|z|` is larger, take its
`abn` and `z`. Otherwise start a new run.

### 4g. Other lists

- `market_days`: dates with `|ret| >= 2.5 * sigma` and `|z| < 2.5` (large moves the market
  explains).
- `volume_only_days`: `{date, rvol, mech}` where `rvol >= 2.0` and `|z| < 1.5`. Listed, never
  researched or storied.
- `mechanical_days`: `{date, label, rvol}` for mech days with `rvol >= 1.75`.

### 4h. Turning points

Threshold `zz = min(0.25, max(0.10, 1.5 * pstdev(window daily returns) * sqrt(21)))` (population
standard deviation).

Zigzag over the window's closes: start with no trend and the extreme at index 0. For each later
close `c`:
- No trend: if `c >= close[ext] * (1 + zz)`, record `ext` as a `low` pivot, trend up, `ext = i`;
  if `c <= close[ext] * (1 - zz)`, record a `high` pivot, trend down, `ext = i`.
- Up trend: a higher close moves `ext` to `i`; a close `<= close[ext] * (1 - zz)` records `ext`
  as a `high`, trend down, `ext = i`.
- Down trend: a lower close moves `ext` to `i`; a close `>= close[ext] * (1 + zz)` records `ext`
  as a `low`, trend up, `ext = i`.

Each pivot is `{date, kind, close}`. The last unconfirmed extreme is not a pivot.

### 4i. Summary and output

- `base_close` = close of the session before the window (`C[first_win-1]`), `base_date` its date.
- `total_ret = last window close / base_close - 1`.
- `bench_ret = last window Bx / Bx[first_win-1] - 1`; `bench_raw_ret = last loaded B /
  B[first_win-1] - 1`.
- `event_days_ret` and `other_days_ret`: compounded (`prod(1 + ret) - 1`) over flagged days and
  over all other window days.
- `hi`, `lo`: highest and lowest window close.

out.json shape:

```json
{"ticker", "benchmark", "window": [first, last], "base_close", "base_date",
 "params": {"z_min": 2.5, "z_price": 3.0, "top_n", "rvol_min": 1.75, "vol_only": 2.0,
            "run_len": 10, "est_win": 60, "vol_win": 50, "zigzag": zz (3 dp)},
 "sources": {"stock": [...], "bench": [...], "sector": [...]},
 "exclude", "weight_path": {"start", "end", "max"}, "sector", "sector_lag",
 "summary": {"total_ret", "bench_ret", "bench_raw_ret", "n_sessions", "n_events",
             "event_days_ret", "other_days_ret", "hi", "lo"},
 "days": [day records], "candidates": [{date, ret, bench_ret, abn, z, rvol, signal}],
 "runs": [...], "market_days": [...], "volume_only_days": [...],
 "mechanical_days": [...], "turning_points": [...]}
```

With constituent removal, `weight_path` is taken from the implied weight series over every
loaded date (lookback included): `start` is the weight on the window's start date (or on the
first loaded date if the start date isn't a loaded date), `end` is the weight on the last loaded
date, and `max` is the largest weight over all loaded dates. When there is no constituent
removal, `weight_path` is `{"start": null, "end": null, "max": null}` (the keys are always
present).

Print, for review: sessions and dates, total vs benchmark; flagged-day and other-session
compounded returns; per candidate its date, return, market part (`beta*bench_ret`), sector part,
stock-specific move, z, rvol and signal; the runs with their `abn` and z; market-explained days;
volume-only days; mechanical heavy-volume days; the zigzag threshold and turning points.

## 5. Phase numbers

Run this before writing the headline or any phase tile. "Event dates" are every date in
`events.json` `events[].dates`. Compounded means `prod(1 + x) - 1`.

**Window line:** total return, benchmark return, market part (compounded `beta * bench_ret`),
stock-specific part (compounded `abn`); flagged-day compounded `ret` (with the session count) and
all other sessions' compounded `ret`.

**Allowed boundaries** (when you have not chosen boundaries yet): every turning point (date, kind,
close); the window's highest close and lowest close; the session before each `releases[].t0`
(the eve of a results reaction, when `t0` is in the window and not its first session); the
window's first and last sessions.

**Per phase** (for chosen boundaries, sorted, with the window ends added): for each pair `a..b`,
the rows are the sessions after `a` up to and including `b`. Print the closes at `a` and `b` and
`close_b / close_a - 1`; market part (compounded `beta * bench_ret` over the rows); stock-specific
part (compounded `abn`); flagged (compounded `ret` over rows that are event dates, with count);
other (compounded `ret` over the remaining rows).

Note: the validator's phase figures in `checks.md` section 1 use the market part including any
sector part (`beta * bench_ret + sec_part`); without a sector factor the two are the same.
