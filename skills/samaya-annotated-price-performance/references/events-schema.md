# events.json: the one file the model writes

Everything else on the page is computed. A full worked example (AAPL, 12 months) is in
`example-events-aapl.json`; copy its shape.

## Contents
1. Top-level fields
2. Event fields
3. Story fields
4. Validator gates (render.py)
5. Fixing a BLOCK

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
| `story` | Headline and phases (section 3) |

## 2. Event fields

| Field | Rule |
|---|---|
| `dates` | Screened dates only. Adjacent flagged days (within 3 sessions) with the same cause may merge into one event |
| `label` | What happened, at most 64 characters, no figures that are not in the summary |
| `category` | See `attribution.md` section 4 |
| `tier` | `confirmed`, `reported` or `none` |
| `release` | `"YYYY-MM-DD HH:MM"` for `confirmed` (must map to `dates[0]` under the timing rule); date only or null otherwise |
| `timing` | Optional short note shown as a chip, e.g. "Release time not in feed" |
| `guidance_check` | Results days: actual vs the company's own guide |
| `summary` | At most 40 words, plain facts with their figures; no forecasts, no recommendations |
| `follow_on` | Same-day rating/target changes as counts, or null |
| `sources` | `{title, source_name, date, url}`; company sources first. `none` events cite the searched news window |

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

- **Find the story in the numbers first.** Run `scripts/phases.py` (no boundaries lists the
  allowed ones; with boundaries it prints each phase's split) before writing a word. The two test names produced opposite stories: one
  fell mostly on news days, the other gained mostly on quiet days. Say which.
- **The headline is the takeaway**, not a description of the chart. State what drove the move
  and, where the evidence cuts against the obvious narrative, say so ("halved before guidance
  was ever cut").
- **Each phase title is itself a takeaway** ("Two guidance resets"), its one line the evidence.
- **2 to 5 phases.** Boundaries must be turning points, the window's high or low close, the
  window ends, or the session before a results reaction.
- **`next`** is optional: the next dated company event, if one is announced.

## 4. Validator gates (render.py)

The render refuses to write the page if any of these fail:

| Gate | Blocks when |
|---|---|
| Completeness | A screened day has no event, or an event sits on a day the screen did not flag |
| Results coverage | A flagged results reaction is not a callout, or a release time maps to a different session |
| Confirmed tier | No company source, no timestamped release, or the release cannot explain `dates[0]` |
| URLs | Any URL is malformed or absent from `urls_seen.txt` |
| Visible text | A broker name, consensus/estimate language, an internal id, a label over 64 characters or a summary over 40 words |
| Story shape | Headline over 24 words, a title over 6 words, a tile line over 18 words, more than 5 phases, phases that do not tile the window, or a disallowed boundary |
| Story citations | A phase with flagged days that cites none of them, or cites an event outside its dates |
| Story figures | Any percentage or dollar figure that matches neither a computed number (within rounding) nor a cited event's label, summary or guidance check |
| Story language | Forecasting or recommendation words: will, should, buy, upside, cheap, undervalued, attractive, likely to, poised |
| Page script | The rendered page's script does not parse (checked when node is available) |

Density is a warning, not a block: above 1.5 events a month the render suggests raising the
screen thresholds.

## 5. Fixing a BLOCK

Fix the data or the wording, never the validator. A figure that "doesn't match" usually means
the prose rounded differently or quoted a number that is not on the page; either cite the event
that contains it or drop the number. A completeness block means a flagged day still needs
research; a `none` tier is a valid outcome.
