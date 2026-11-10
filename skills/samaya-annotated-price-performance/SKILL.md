---
name: samaya-annotated-price-performance
description: >-
  "annotated price chart", "what moved the stock", "price performance with catalysts", "label the
  chart with the news" — for meeting, pitch or position-review prep: an interactive price-volume
  chart for one stock, split into periods, each big move and run labelled with the news that
  drove it, sourced via Samaya. Not for price alerts (samaya-trigger-price-move), co-moves
  (samaya-correlation-analysis) or insider trades.
---

# Annotated price performance

**What it includes:** an interactive price chart split into periods, each big move labelled with
the news or event that drove it, with sources.

Produces one self-contained interactive HTML page for one stock over a window (default: the
trailing 12 months to the last close):

- a one-sentence takeaway and 2 to 5 phase tiles, each titled with its own takeaway;
- a price chart (default view) with the benchmark rebased, numbered markers on every day the
  stock moved well beyond what the market explains, and open triangles for major company events
  that did not move it;
- a volume pane, because volume tells as much of the story as price;
- a daily split view (each day's move into a market part and a stock-specific part, against the
  stock's normal range) and a cumulative split view;
- a side panel per event (what happened, attribution tier, the split, sources), an event table,
  and collapsed sections for market-driven days, method and sources.

The design principle: **the numbers decide which days get a story; research decides what the
story is; a validator decides whether the page may be written.** Earlier versions of this
output invented causes for drift, pinned macro headlines on market days and missed timing. Every
rule below exists because of one of those failures, and most are enforced by the checks you run.

## Before starting

Confirm scope in one line, then proceed without waiting on anything else:
ticker and listing, window, benchmark (`references/data-pulls.md` section 4: the broad index of
the stock's own exchange, in its currency), and whether an optional sector factor is wanted.

## How the work is done

This skill ships no code. You write the helper code yourself, at run time, in a scratch working
folder: Python using only the standard library is enough for every computation and check. The
code must run on Python 3.9 (macOS `/usr/bin/python3`): no `X | Y` type hints unless `from __future__ import annotations` is first, no `match` statements. Each
step below names the reference that specifies exactly what to compute or check, with the
formulas, thresholds and output shapes. Follow those specs to the letter; do not substitute your
own method or parameters.

- Run your helper code and read its output; never compute screen numbers by hand.
- Every check that can block must pass before you go on. If one fails, fix the data, the research
  or the wording and rerun from that step. Never weaken a check and never ship a page that failed
  one.
- Never hand-edit the price data to make a check pass.

## Pipeline

Work in a scratch directory, with `raw/` for the price slices.

**1. Plan and pull prices.** Build the pull plan in `references/computation.md` section 1: one
Samaya question per slice per series, slices of at most 120 days starting 95 days before the
window. Send each as its own `financial_qa` call in a fresh session, poll until done, and save
each reply verbatim to `raw/<prefix>_<n>.txt` with the `# url=... title=...` header. Append
every Samaya URL returned, from any call, to `urls_seen.txt`. Read `references/data-pulls.md`
before the first pull: a single pull silently keeps only ~100 sessions.

**2. Check integrity.** Write and run the integrity check in `references/computation.md`
section 3. It drops copied bars, flags corrupt volume, logs vendor gaps and repairs a whole-day
date shift only when one shift is unambiguous. If it blocks, stop and tell the person what
failed. State any repair or gap on the page.

**3. Screen.** Write and run the screen in `references/computation.md` section 4 on the clean
data, producing `out.json` (add a sector factor or constituent removal only per `data-pulls.md`
section 6). It grades every day on a signal ladder, from the stock-specific move (z = move beyond
what beta x benchmark explains, divided by the stock's normal daily variation) and volume:

| Signal | Rule | Treatment |
|---|---|---|
| `strong` | z >= 2.5 on volume >= 1.75x the 50-day median, not an index-mechanics day | Callout, researched |
| `price` | z >= 3.0 on any volume (mega-caps rarely spike volume on news) | Smaller callout, "on normal volume", researched |
| `rank` | Among the window's largest stock-specific moves, about 10 per year scaled to the window (z >= 2) | Callout, researched (top-move guarantee) |
| volume-only | Volume >= 2x with z < 1.5 | Listed, never researched or storied |
| `run` | 10-session cumulative z >= 2.5 with no flagged day inside | Hatched, clickable band with its own panel and legend entry, researched as one window |

Volume on quarterly-expiry and Russell-reconstitution days cannot make a day `strong`. There is
no cap.

**4. Research every flagged day, run and drift phase.** Follow `references/attribution.md`. Go
down the source ladder and stop at the first rung that explains the move: company releases and
filings, then news asked as "Why did <company> (<ticker>) stock move <x%> on <date>?", then Web
results that report an event (not the move) from an attributable publisher, never a "why it
moved" explainer, then X posts dated that session as a last resort (tier `social`: context, not
a confirmed cause). Never use Reddit: its posts carry no date. One credible original report with
no second source is tier `reported` with `single_source: true` (shown as "single source"); a
relayed copy never counts as a second source. Any phase whose unflagged sessions add up to more
than an 8% stock-specific move must be researched as a window (`context_sources`); the validator
blocks otherwise. Apply the timing rule (a release after the close moves the next session).
Measure beat or miss against the company's own guidance from transcripts or 8-Ks, never
consensus. Treat rating changes as same-day reactions, in counts. Also collect results releases
with times, and context events (results days, management changes, large M&A) that did not clear
the screen.

Everything flagged is researched; the page decides how loudly to show it. Numbered markers go to
the moves that account for 75% of flagged stock-specific movement, plus every results reaction and
the three largest moves; the rest are small numbered circles on the price line with the same
panel. Markers cluster only when they would overflow the screen's row budget, and never the
results or top three.

**5. Write `events.json`.** Schema and limits in `references/events-schema.md`; a complete
worked example is `references/example-events-aapl.json`.

**6. Find the story, then write it.** Compute the phase numbers in `references/computation.md`
section 5: first the allowed phase boundaries, then, for the boundaries you choose, each phase's
return, market and stock-specific parts, and flagged-day versus other-session contributions.
Write the headline and phase tiles from those numbers. Say plainly when the evidence cuts
against the obvious narrative.

**7. Validate.** Write and run the validator in `references/checks.md` section 1 on `out.json`,
`events.json` and `urls_seen.txt`. If it prints any BLOCK line, do not write the page (gate
summary in `events-schema.md` section 4). Fix the data or the wording, never the validator, and
rerun until it passes cleanly.

**8. Build the page.** Build the page data in `references/checks.md` section 2, then write the
HTML page as specified in `references/page.md`, embedding that data. Title it
`<TICKER>: what moved the stock`.

**9. Audit, check and deliver.** Run the coverage audit in `references/checks.md` section 3: it
checks the page against the raw data (the window's largest raw and stock-specific moves covered,
as many as the scaled top-move guarantee, no unresearched drift phase) and must report PASS or
have each issue explained. Then run the page checks in `checks.md` section 4: the page's script
parses (`node --check`, run only when `node --version` succeeds; a node shim with no
version set counts as node unavailable, not a parse failure) and, if a headless browser is
available, the page opens at desktop and mobile widths with no script errors and looks right.
Deliver the single HTML file through the environment's publishing or file mechanism; it loads its
fonts from Google Fonts and runs nothing else externally.

## Rules the page must keep

- Only Samaya-retrieved information. No figure, date, officeholder or cause from memory.
- No investment recommendation, price target, valuation view or forecast in any text.
- Beat or miss only against the company's own prior guidance; say so when no numeric guide
  exists.
- No broker or analyst names in visible text; rating changes appear as counts, names stay in
  source titles.
- Every source names the actual document or feed and links the exact Samaya URL returned;
  Samaya is the routing layer, not the source.
- Unexplained large moves are shown, labelled "No catalyst found", not hidden or explained away.
- X posts are the last source and never a confirmed cause; Reddit is never used.
- A phase that rose or fell on unflagged days is researched as a window, never described as
  "quiet days" by default.
- Market-driven large moves get no story; they are listed with their split.
- Name the benchmark everywhere the split is shown.
- No model or vendor name as an author anywhere in the output.

## Reference files

| File | Read when |
|---|---|
| `references/data-pulls.md` | Before the first candle pull; when integrity blocks; for non-US listings |
| `references/computation.md` | Writing the pull plan, integrity check, screen and phase numbers |
| `references/attribution.md` | Before researching flagged days |
| `references/events-schema.md` | Writing `events.json` and the story; fixing a BLOCK |
| `references/example-events-aapl.json` | As the template for `events.json` |
| `references/checks.md` | Writing the validator, the page data and the coverage audit |
| `references/page.md` | Writing the HTML page |
