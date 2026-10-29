# Price data: pulls, files, benchmark, integrity

Read this before the first candle pull. Every rule here came from a live failure.

## Contents
1. Slicing and the 100-row cap
2. Raw slice files (exact format)
3. The URL ledger
4. Choosing the benchmark
5. Integrity check: what it catches and what it repairs
6. Optional factors: sector and constituent removal
7. Known data behaviours

## 1. Slicing and the 100-row cap

A candle pull keeps only the most recent ~100 sessions. A 12-month request silently returns
May-to-October while the reference title still claims the full range. So:

- Run `scripts/plan.py <ticker> <benchmark> <start> <end>`. It prints one question per slice,
  each of at most 120 calendar days, starting ~95 days before the window. The lookback feeds
  the 60-session beta, the normal-variation estimate and the 50-session volume baseline.
- Send each question as its own `financial_qa` call in a fresh session; poll
  `financial_qa_result` until done. Never re-issue a question that is still running.
- Pull the benchmark (and sector series, if used) over the same slices.

## 2. Raw slice files (exact format)

Save each reply verbatim (no reformatting of numbers) to `raw/<prefix>_<n>.txt`. The prefix is
the lower-case name you will pass to the scripts (`aapl`, `spy`, `hynix`, `kodex`).

```
# url=https://app.samaya.ai/u/<id> title=<reference title exactly as returned>
2026-07-01 | 293.44 | 296.59 | 289.19 | 294.38 | 50.16M
2026-07-02 | 294.12 | 309.42 | 293.68 | 308.63 | 75.40M
```

- Stock rows: `date | open | high | low | close | volume`; drop the trailing currency column.
  Volume keeps its suffix (`K`, `M`, `B`) or a bare number. Copy a bad value as returned
  (e.g. `151`); the integrity check flags it, never edit it by hand.
- Benchmark and sector rows may be `date close` only, or the full candle form.
- Overlapping dates between slices are fine; the scripts merge by date.
- The first line must carry the reference's `url` and `title`. A file without it blocks.

## 3. The URL ledger

Append every `https://app.samaya.ai/u/...` URL returned in the session, one per line, to
`urls_seen.txt`. `render.py` rejects any source URL that is not in this file, so a URL that is
mistyped, edited or remembered from elsewhere cannot reach the page. Never construct or edit a
Samaya URL.

## 4. Choosing the benchmark

Benchmark against the broad index of the stock's own exchange, in its own currency, on its own
calendar. A foreign index breaks the method: non-overlapping hours make same-day beta near
zero (every move looks stock-specific), holidays differ, and currency moves leak into the
"market part".

| Listing | Default benchmark (index, else its largest local ETF) |
|---|---|
| US | S&P 500: SPY |
| Japan | TOPIX |
| Korea | KOSPI 200: KODEX 200 (069500.KS) |
| Germany | DAX (HDAX for mid-caps) |
| UK | FTSE All-Share |
| France / Eurozone | CAC 40 / Euro Stoxx |
| Hong Kong | Hang Seng |
| Canada | S&P/TSX Composite |

- If the index itself comes back only as web scrapes (the KOSPI did), use the largest local ETF
  tracking it, and sanity-check one large index day against reported index moves.
- ADRs and dual listings: chart the primary local listing.
- The person can override (e.g. QQQ for a Nasdaq name). The page always names the benchmark.

## 5. Integrity check: what it catches and what it repairs

`scripts/integrity.py <stock> <bench> raw clean` runs before anything is computed. It writes
`clean/<prefix>_clean.txt` for both series and `clean/integrity_<stock>.json`.

| Defect | Handling |
|---|---|
| Copied bar (open/high/low/close identical to the previous bar) | Dropped |
| Implausible volume (< 1% of the series median) | Set to missing; that day cannot pass the volume test |
| Dates shifted by whole days (local-midnight timestamps rendered in UTC put Korean sessions on Sundays) | Repaired only if exactly one shift makes the calendar match the benchmark and its return correlation is >= 0.5 and beats every other shift by >= 0.25 |
| Up to 2 genuine vendor gaps (a session missing from the stock only) | Logged; returns span the gap on both series |
| Anything else, or an ambiguous repair | Blocks |

A repair or gap must be stated in the page's method notes (the integrity JSON gives the exact
wording). Never hand-edit a slice to make the check pass.

## 6. Optional factors: sector and constituent removal

Off by default. Use them when the person asks, or when the stock's situation calls for it:

- **Sector factor** (`sector=<prefix> sector_raw=<dir> sector_lag=prior|same`). For an Asian
  stock driven by US-listed peers, `prior` matches each local session with the foreign move
  over the sessions that closed before it opened. In the one test (SK hynix vs SOXX) it added
  little, because the local market already prices the overnight move.
- **Constituent removal** (`exclude=<weight>@<date>`). When the stock is a large weight in its
  benchmark (rule of thumb: above ~10%), its own move contaminates the "market part". The
  weight is anchored on a sourced date and drifts with relative price; the market factor
  becomes the index excluding the stock. Source the weight through Samaya and state it.
- Known limit: when a second giant peer remains in the index (Samsung for SK hynix), the
  market factor still carries that industry's cycle. For such names, say on the page that the
  split is relative to a market dominated by that peer, or use the peer as the sector factor.

## 7. Known data behaviours

- Volume strings carry suffixes (`63.12M`); the scripts parse them.
- Results-release days include after-hours trading in daily volume. List those dates in
  `after_hours_days`; the page outlines their bars and the reaction day carries the volume test.
- Index-mechanics volume (quarterly expiry, Russell reconstitution) is computed by
  `compute.py` for US listings; those days cannot pass the volume gate (only the price-only
  path), and the page lists them as "index mechanics, not news".
- Turning points scale with the stock's own volatility (1.5x monthly, clamped 10 to 25%).
