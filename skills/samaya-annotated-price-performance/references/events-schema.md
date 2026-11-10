# events.json: the one file the model writes

Everything else on the page is computed. A worked example (AAPL, 12 months) is in
`example-events-aapl.json`; copy its shape. It matches the current screen (14 flagged days, no
runs) and includes a Web source recorded with publisher, kind and evidence.

## Contents
1. Top-level fields
2. Event fields
3. Story fields
4. Validator gates
5. How the page shows events
6. Fixing a BLOCK

## 1. Top-level fields

| Field | Content |
|---|---|
| `company` | Company name as it should appear on the page |
| `benchmark_name` | Long name of the benchmark, e.g. "SPDR S&P 500 ETF" |
| `as_of` | Last session in the window (YYYY-MM-DD) |
| `releases` | Results releases with verified times: `{t0, release: "YYYY-MM-DD HH:MM", label}`. Only releases whose time came from a company source go here |
| `after_hours_days` | Release days whose daily volume includes after-hours trading on the release |
| `context_events` | Major events that did not clear the screen: `{date (reaction session), label, source{title, source_name, date, url}}` |
| `events` | One entry per flagged day (or merged run of days), in date order |
| `runs` | One entry per run in the screen's output (`computation.md` section 4f): `{start, end, label, tier, summary, sources}` (same tiers as events) |
| `story` | Headline and phases (section 3) |

## 2. Event fields

| Field | Rule |
|---|---|
| `dates` | Screened dates only (signal `strong`, `price` or `rank`; the page draws price-only days slightly smaller and notes "on normal volume"). Adjacent flagged days (within 3 sessions) with the same cause may merge into one event |
| `label` | What happened, at most 64 characters, no figures that are not in the summary |
| `category` | See `attribution.md` section 4 |
| `tier` | `confirmed`, `reported`, `social` or `none` (see `attribution.md` section 3) |
| `single_source` | Optional, `reported` only: true when one credible original report is the only source |
| `release` | `"YYYY-MM-DD HH:MM"` for `confirmed` (must map to `dates[0]` under the timing rule); date only or null otherwise |
| `timing` | Optional short note shown as a chip, e.g. "Release time not in feed" |
| `guidance_check` | Results days: actual vs the company's own guide |
| `summary` | At most 40 words, plain facts with their figures; no forecasts, no recommendations |
| `follow_on` | Same-day rating/target changes as counts, or null |
| `sources` | `{title, source_name, date, url}`; Web sources add `publisher`, `kind`, `evidence` (`attribution.md` 3b); company sources first. `none` events cite the searched news window |

## 3. Story fields

```json
"story": {
  "headline": "One sentence, at most 24 words, stating the takeaway.",
  "chapters": [
    {"from": "YYYY-MM-DD", "to": "YYYY-MM-DD", "title": "At most 6 words",
     "text": "At most 18 words of evidence.", "event_dates": ["YYYY-MM-DD"],
     "context_sources": []}
  ],
  "next": {"date": "YYYY-MM-DD", "label": "Q3 2026 results, after the close",
           "source": {"title": "...", "source_name": "Press Releases", "date": "...", "url": "..."}}
}
```

How to write it:

- **Find the story in the numbers first.** Compute the phase numbers in `computation.md` section 5 (first the
  allowed boundaries; then, for chosen boundaries, each phase's split) before writing a word. The two test names produced opposite stories: one
  fell mostly on news days, the other gained mostly on quiet days. Say which.
- **The headline is the takeaway**, not a description of the chart. State what drove the move
  and, where the evidence cuts against the obvious narrative, say so ("halved before guidance
  was ever cut").
- **Each phase title is itself a takeaway** ("Two guidance resets"), its one line the evidence.
- **2 to 5 phases.** Boundaries must be turning points, the window's high or low close, the
  window ends, or the session before a results reaction.
- **`next`** is optional: the next dated company event, if one is announced.
- **`dek`** is optional: one short line shown under the headline, checked like the headline
  for language and figures.

## 4. Validator gates

The page is not written if any of these fail. Exact rules, word lists and formulas are in
`checks.md` section 1:

| Gate | Blocks when |
|---|---|
| Completeness | A screened day or run has no entry, or an event sits on a day the screen did not flag |
| Web sources | Missing publisher/kind/evidence, publisher not in the title or byline, a blocklisted publisher, hedged evidence, an explainer headline carrying the tier alone, or a Web-only story without a primary document or two publishers |
| Social sources | Any Reddit source; a `confirmed`/`reported` tier resting only on social posts; a `social` tier without an X post dated that session or the one before |
| Results coverage | A flagged results reaction is not a callout, or a release time maps to a different session |
| Confirmed tier | No company source, no timestamped release, or the release cannot explain `dates[0]` |
| URLs | Any URL is malformed or absent from `urls_seen.txt` |
| Visible text | A broker name, consensus/estimate language, an internal id, a label over 64 characters or a summary over 40 words |
| Phase drift | A phase's unflagged sessions add up to more than an 8% stock-specific move and it has no `context_sources` or run |
| Story shape | Headline over 24 words, a title over 6 words, a tile line over 18 words, more than 5 phases, phases that do not tile the window, or a disallowed boundary |
| Story citations | A phase with flagged days that cites none of them, or cites an event outside its dates |
| Story figures | Any percentage or dollar figure that matches neither a computed number (within rounding) nor a cited event's label, summary or guidance check |
| Story language | Forecasting or recommendation words: will, should, buy, upside, cheap, undervalued, attractive, likely to, poised |
| Page script | The page's script does not parse (checked only when `node --version` succeeds; `checks.md` section 4) |

Density is a warning, not a block: above 1.5 events a month the validator suggests raising the
screen thresholds.

## 5. How the page shows events (computed, nothing to write)

Every event is researched and listed in the table. On the chart, numbered markers go to the
smallest set of events covering 75% of flagged stock-specific movement, plus every results
reaction and the three largest moves (anchors); the rest are small numbered circles on the price line
that open the same panel. Markers stack into rows; only when the stack would exceed the screen's row budget
(3 rows on desktop, 2 on a phone) do the densest non-anchor markers collapse into a badge that
expands on click. The proportions scale with the data; no count is fixed. Exact rules:
`checks.md` section 2 (prominence) and `page.md` section 6 (markers).

## 6. Fixing a BLOCK

Fix the data or the wording, never the validator. A figure that "doesn't match" usually means
the prose rounded differently or quoted a number that is not on the page; either cite the event
that contains it or drop the number. A completeness block means a flagged day still needs
research; a `none` tier is a valid outcome.
