# Checks: the validator, the page data, the coverage audit

Write the validator as your own helper code in the scratch working folder and run it on
`out.json`, `events.json` and `urls_seen.txt` before writing any HTML. It must run on
Python 3.9 (macOS `/usr/bin/python3`): no `X | Y` type hints unless `from __future__ import annotations` is first, no `match` statements. It prints one
`BLOCK: <reason>` line per failure. **If any line prints, do not write the page.** Fix the data
or the wording and rerun; never weaken a check. When it passes, the same helper builds the page
data (section 2). After the page is written, run the coverage audit (section 3) and the page
checks (section 4).

## Contents
1. Validator gates
2. Page data (what the page embeds)
3. Coverage audit
4. Page checks before delivery

## 1. Validator gates

Notation: `dates` = the window's sessions from out.json `days`; `cand` = out.json `candidates`
by date; `used` = every date in `events[].dates`, in file order; "compounded" = `prod(1 + x) - 1`;
`expl(d) = beta * bench_ret + sec_part`.

### 1a. Word lists

- **Brokers** (word-boundary match, case-insensitive; skip any entry contained in the company
  name): goldman, morgan stanley, jpmorgan, jp morgan, citi, barclays, wedbush, btig,
  benchmark co, needham, piper, jefferies, macquarie, ubs, deutsche, hsbc, canaccord, davidson,
  cowen, oppenheimer, roth, wells fargo, bofa, b of a, arete, riley, bernstein, evercore,
  keybanc, mizuho, rbc, bmo, loop capital, raymond james.
- **Banned phrases** (substring, lower-cased): consensus, estimate, street expect, analysts
  expected, news_id, buy the, sell the stock, undervalued, overvalued, attractive valuation.
- **Web kinds**: `original_report`, `primary_document`, `wire_relay`.
- **Web blocklist** (substring of publisher + title, lower-cased): stockstory, quiver,
  marketbeat, finbold, invezz, 24/7 wall st, 247wallst, chartexchange, altindex, tipranks,
  simply wall st, tapbit.
- **Explainer headline patterns** (regex on the lower-cased title):
  `\bwhy\b.*\b(stocks?|shares)\b`; `what'?s going on with`; `\bstock is (up|down|trading)\b`;
  `\b(stocks?|shares?)( price)? (surges?|soars?|jumps?|pops?|plunges?|tumbles?|sinks?|slides?|slide|rally|rallies)\b.*\b(on|as|after)\b`.
- **Hedges** (substring of evidence, lower-cased): appears to, appear to, may have, might have,
  likely due, likely driven, seems to, seem to, could be, possibly, probably.
- **Story language** (word-boundary regex on lower-cased prose): will, should, buy, upside,
  cheap, undervalued, attractive, likely to, poised, expect the.
- **Primary source names** (substring of `source_name`): `Filings`, `Press Releases`,
  `press release feed`.

### 1b. Release timing

`t0_for(release)`: split `"YYYY-MM-DD HH:MM"`. No time part: no session (so it never matches). Date
not a session (weekend or holiday): the next session after it. Time `>= "16:00"`: the next
session. Otherwise: the same date.

### 1c. Events

1. Tier must be one of `confirmed`, `reported`, `social`, `none`.
2. Every date must be in `cand`; no date used twice; merged dates may span at most 3 sessions
   (index difference); `used` must be in ascending order.
3. **Completeness:** every candidate date must appear in some event (a `none` tier is allowed).
4. Density warning only: events per month (`sessions / 21`, at least 1) above 1.5 prints a
   warning suggesting higher screen thresholds.
5. **Releases:** a `t0` that is a candidate but not in `used` blocks; `t0_for(release) != t0`
   blocks.
6. **Sources:** a non-`none` event with no sources blocks. Every source URL must fully match
   `https://app\.samaya\.ai/u/[A-Za-z0-9]+` and be in `urls_seen.txt`.
7. **Reddit:** "reddit" in title or source_name (lower-cased), or a title starting `r/`, blocks.
8. **Web sources** (`source_name == "Web"`): missing publisher, a kind outside the three, or
   empty evidence blocks (and skip that source's other tests). Else block when the publisher
   (lower-cased) is not in the title plus `byline`; when publisher or title hits the blocklist;
   when the evidence contains a hedge; when the evidence is over 30 words.
9. **Support:** a source supports the tier when it is not `Social Media`, its title matches no
   explainer pattern, and its title does not contain `(searched)` (the marker for a searched
   window cited by a `none` event).
   - `confirmed`/`reported` with sources but no support blocks.
   - `reported` whose support is all Web: needs a `primary_document` or two distinct publishers
     among non-`wire_relay` sources, unless `single_source: true` with exactly one such
     publisher.
   - `single_source` on any tier other than `reported` blocks.
   - `confirmed`/`reported` whose sources are all `Social Media` blocks.
10. **Social tier:** needs a `Social Media` source dated from the previous session to `dates[0]`
    inclusive.
11. **Confirmed tier:** needs a primary source; `release` must contain a time; `t0_for(release)`
    must equal `dates[0]`.
12. **Visible text** (label, summary, follow_on, timing; lower-cased): no broker, no banned
    phrase; label at most 64 characters; summary at most 40 words (split on whitespace).

### 1d. Runs and context events

- Every out.json run `(start, end)` needs an `events.json` `runs` entry with the same start and
  end.
- Run tiers valid; run source URLs in the ledger.
- Each `context_events[].date` must be a session; its source URL must be in the ledger.

### 1e. Story

`story` is required. Allowed boundaries: turning-point dates, the session before each release
`t0` (when `t0` is a session and not the first), the first and last session, and the highest and
lowest close dates.

1. The first phase's `from` is the first session, the last phase's `to` the last session; each
   `to` equals the next `from`.
2. Every `from`/`to` is an allowed boundary.
3. **Drift:** for each phase, compounded `abn` over the sessions after `from` up to `to` that are
   not event dates. If `|drift| > 0.08` and the phase has no `context_sources` and contains no run
   (`from <= run.start` and `run.end <= to`), block.
4. Each `event_dates` entry must be an event's first date and lie in `(from, to]`.
5. A phase with an event first-date in `(from, to]` must cite `event_dates` or `context_sources`.
6. `context_sources` URLs and `next.source.url` must be in the ledger.
7. Shape: headline at most 24 words; each title at most 6 words; each `text` at most 18 words;
   at most 5 phases.
8. **Language:** headline, optional `dek`, and every title and text: no story-language word, no
   broker.
9. **Figures.** Build the allowed sets:
   - percent set: `round(|v| * 100)` for summary `total_ret`, `bench_ret`, `mkt_part`
     (compounded `beta*bench_ret` over all days), `spec_part` (compounded `abn`),
     `event_days_ret`, `other_days_ret` (both over `used` dates), and for every phase its
     `ret` (`close_to / close_from - 1`), `mkt` (compounded `expl`), `spec` (compounded `abn`),
     `flagged`, `other`, and `refs` (compounded `ret` over the dates of its cited events);
   - dollar set: rounded window high and low closes, and each phase's rounded from/to closes;
   - sourced text: label + summary + guidance_check of every cited event.

   In each prose string (original case), first replace with a space every match of
   `\b(19|20)\d\d\b|\bQ[1-4]\b|\bFY\d{4}\b|\b\d{1,2} (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\b`
   (years, quarters, fiscal years, and day-month forms like `9 Sep`; three-letter month names
   only, so `9 Sept` or `9 September` is not blanked). Then for each match of
   `(\$)?(\d[\d,]*(?:\.\d+)?)(?:-(\d+))?(%)?`, with `val` its first number (commas removed):
   pass if the whole token appears verbatim in the sourced text; else pass a `%` figure with no
   range part when `val` is within 1 of the percent set; else pass a `$` figure when `val` is
   within 1 of the dollar set; else pass a figure with neither `$` nor `%` when `val` is under 20
   (small counts); otherwise block. So only a percent range matching `\d+-\d+%` (such as `9-11%`)
   must appear verbatim in a cited event; a bare range such as `3-5` is checked by its first
   number like any bare number.

### 1f. Not a gate

When no BLOCK line printed, print for review: how many events are prominent (section 2), the
headline, market and stock-specific parts and the total, flagged-day and other-session returns,
and one line per event (date, return, `abn`, rvol, tier, label).

## 2. Page data (what the page embeds)

Built only after section 1 passes. Embed it as one JSON object (see `page.md`).

**Per event**, computed from the day records: `ret` = compounded `ret` over its dates;
`bench_ret` = compounded; `abn` = sum of `abn`; `mkt` = sum of `expl`; `z` = the day `z` with the
largest absolute value; `rvol` = largest `rvol` (missing as 0); `signal` = `strong` if any date is
strong, else `price` if any is price, else `rank`.

**Prominence.** `size(event)` = sum over its dates of `|ln(1 + abn)|`. Order events by size,
largest first; add them to the prominent set until the running total reaches 75% of the total
(check before adding each). Also add the three largest, and every event whose category starts with
"Earnings" or that contains a release `t0`. `anchor` = the three largest plus those results
events. Each event gets `prominent` and `anchor` booleans.

**Summary** = out.json summary plus `event_days_ret`, `other_days_ret` (recomputed over `used`),
`n_event_sessions`, `mkt_part`, `spec_part`.

**Phases (`chapters`)**: each phase's own fields plus `ret`, `mkt`, `spec`, `flagged`, `other`,
`refs`, `from_c`, `to_c`, and `events` (indices of its cited events).

**Runs**: each `events.json` run plus `n` (sessions from start to end), `price` (last close in the
run / close of the session before `start` - 1, or the run's first close if none), `mkt`
(compounded `expl`) and `abn` (compounded `abn`, replacing any value in the entry).

**Market moves**: for each `market_days` date, `{date, ret, bench_ret, beta, mkt: expl, abn,
rvol}`.

**Integrity** (the source of the page's Data notes), built from the integrity log
(`computation.md` section 3) and out.json:

```json
"integrity": {"repairs": ["dates shifted +1 day(s): correlation with SPY ..."],
              "issues": ["vendor gap: no genuine bar for 2026-03-12; returns span the gap on both series"],
              "gaps": ["2026-03-12"],
              "sector": null, "exclude": null,
              "weight_path": {"start": null, "end": null, "max": null}}
```

- `repairs`: the log's `repair` line as a one-item list, or `[]` when it is null.
- `issues`: every `issues` line from the log, in log order (vendor gaps, bars dropped at the
  edges), or `[]`.
- `gaps`: the log's `gaps` dates (ISO, ascending), or `[]`.
- `sector`, `exclude`, `weight_path`: copied from out.json, for the sector-factor and
  constituent-removal lines.

All keys are always present. The Data notes must state every `repairs` and `issues` line.

The object:

```json
{"ticker": UPPER, "company", "benchmark": UPPER, "benchmark_name", "window", "as_of",
 "base_close", "params", "headline": story.headline, "standfirst": story.dek or "",
 "chapters", "next", "context_events", "mechanical_days", "summary", "sources",
 "market_days", "market_moves", "turning_points", "releases", "other_flagged": [],
 "log_scale_note", "events", "runs", "factor_label", "integrity", "days"}
```

- `events[]` keep: `dates, label, category, tier, timing, summary, follow_on, sources, ret,
  bench_ret, abn, mkt, z, rvol, signal, single_source, prominent, anchor`.
- `log_scale_note`: "The price axis is logarithmic because the range is wide, so equal distances
  are equal percentage moves." when `hi / lo > 2.2`, else "The price axis is linear."
- `factor_label`: "Market + sector part" with a sector factor, else "Market part".
- `days[]`: `date, o, h, l, c, v, bench` (rebuilt level), `ret, bench_ret, abn, mkt` (`expl`;
  these four rounded to 6 dp), `beta` (3 dp), `sig` (sigma, 6 dp), `rvol` (3 dp, missing as 0),
  `medv` (the 50-session median volume), `mech`, `ah` (true when the date is in
  `after_hours_days`).

## 3. Coverage audit

An independent check of the finished research against the data. It does not trust the research.

- `n` = `params.top_n` from out.json.
- `status(day)`: `flagged/<tier>` if the date is in an event; else `in run` if inside any
  `events.json` run `[start, end]`; else `market/normal` if it is a market day or `|z| < 2.0`;
  else `NOT COVERED`.
- Print the `n` days with the largest `|ret|` and the `n` with the largest `|abn|`, each with
  date, `ret`, `abn`, `z`, rvol and status. Each `NOT COVERED` is an issue.
- Print the callouts an older, stricter gate would have dropped (event dates where not
  `|z| >= 4` and not `|z| >= 2.5` on `rvol >= 1.75` off a mech day), for information.
- Print near misses: unflagged days outside any run with `2.0 <= |z| < 2.5`.
- For each phase: compounded `ret` over sessions in `(from, to]`, and compounded `abn` over those
  that are not event dates. When the latter's absolute value is over 0.08, the phase contains no
  run and has no `context_sources`, it is an issue: "drift needs phase research".
- Print the tier mix and the count of sources by `source_name`.
- Result: **PASS** when there are no issues; otherwise the number of issues. Each issue must be
  fixed (research the day or phase and rerun everything downstream) or explained to the person.

## 4. Page checks before delivery

- The embedded JSON parses, and every `</` inside it is written as `<\/`.
- No placeholder or unfilled slot text remains in the HTML.
- Run `node --version` first. Only if it succeeds (exit 0 and prints a version), extract the
  page's main inline script to a scratch file and run `node --check` on it; a parse error blocks
  delivery. If `node --version` fails, including a version-manager shim that reports no version
  set, node is unavailable: skip this check and say so; it is not a parse failure.
- If a headless browser is available, open the page at a desktop width (about 1280px) and a phone
  width (about 390px), confirm there are no script errors in the console, and look at the result:
  markers readable, no horizontal page scroll, panel and tables populated, all three views draw.
