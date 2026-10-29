---
name: samaya-annotated-price-performance
description: >-
  "annotated price chart", "what moved the stock", "price performance with catalysts", "label the
  chart with the news" — an interactive HTML price and volume chart for one stock that flags every
  day it moved beyond the market, sources each move through Samaya (results vs company guidance,
  news, rating changes) and states the takeaway. Not for valuation, peer comps or insider trades.
---

# Annotated price performance

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
rule below exists because of one of those failures, and most are enforced in code.

## Before starting

Confirm scope in one line, then proceed without waiting on anything else:
ticker and listing, window, benchmark (`references/data-pulls.md` section 4: the broad index of
the stock's own exchange, in its currency), and whether an optional sector factor is wanted.

## Pipeline

Work in a scratch directory. Scripts are in `scripts/`, the page template in `assets/`.

**1. Plan and pull prices.** `python3 scripts/plan.py <ticker> <benchmark> <start> <end>` prints
one Samaya question per slice. Send each as its own `financial_qa` call, poll until done, and
save each reply verbatim to `raw/<prefix>_<n>.txt` with the `# url=... title=...` header. Append
every Samaya URL returned, from any call, to `urls_seen.txt`. Read `references/data-pulls.md`
before the first pull: a single pull silently keeps only ~100 sessions.

**2. Check integrity.** `python3 scripts/integrity.py <stock> <bench> raw clean`. It drops copied
bars, flags corrupt volume, logs vendor gaps and repairs a whole-day date shift only when one
shift is unambiguous. If it blocks, stop and tell the person what failed; never hand-edit data.
State any repair or gap on the page.

**3. Screen.** `python3 scripts/compute.py <stock> <bench> <start> <end> clean out.json clean=1`
(add `sector=`, `exclude=` options only per `data-pulls.md` section 6). A day is flagged when its
stock-specific move is at least 2.5x the stock's normal daily variation on at least 1.75x median
volume, or at least 4x on any volume. Volume on index-mechanics days (quarterly expiry, Russell
reconstitution) does not count. There is no cap.

**4. Research every flagged day.** Follow `references/attribution.md`: company releases first,
news in 1 to 2 day windows, the timing rule (a release after the close moves the next session),
tiers `confirmed` / `reported` / `none`, beat or miss against the company's own guidance from
transcripts or 8-Ks (never consensus), rating changes as same-day reactions in counts. Also
collect results releases with times, and context events (results days, management changes,
large M&A) that did not clear the screen.

**5. Write `events.json`.** Schema and limits in `references/events-schema.md`; a complete
worked example is `references/example-events-aapl.json`.

**6. Find the story, then write it.** `python3 scripts/phases.py out.json events.json` lists the
allowed phase boundaries; add boundaries to print each phase's return, market and
stock-specific parts, and flagged-day versus other-session contributions. Write the headline
and phase tiles from those numbers. Say plainly when the evidence cuts against the obvious
narrative.

**7. Render.** `python3 scripts/render.py out.json events.json urls_seen.txt
assets/template.html <out>.html`. It writes nothing if any gate fails (list in
`events-schema.md` section 4). Fix the data or the wording, never the validator.

**8. Check and deliver.** If a headless browser is available, open the page at desktop and
mobile widths, confirm no script errors, and look at it. Deliver the single HTML file through
the environment's publishing or file mechanism; it loads its fonts from Google Fonts and runs
nothing else externally.

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
- Market-driven large moves get no story; they are listed with their split.
- Name the benchmark everywhere the split is shown.
- No model or vendor name as an author anywhere in the output.

## Reference files

| File | Read when |
|---|---|
| `references/data-pulls.md` | Before the first candle pull; when integrity blocks; for non-US listings |
| `references/attribution.md` | Before researching flagged days |
| `references/events-schema.md` | Writing `events.json` and the story; fixing a render BLOCK |
| `references/example-events-aapl.json` | As the template for `events.json` |
