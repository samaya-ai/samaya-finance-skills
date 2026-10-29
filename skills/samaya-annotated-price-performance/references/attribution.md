# Attribution: what moved the stock, and how sure we are

Read this before researching the flagged days. The screen decides *which* days get a story;
this file decides *what* story, if any, each day is allowed to carry.

## Contents
1. Order of work per flagged day
2. The timing rule
3. Attribution tiers
4. Categories
5. Results days and the guidance check
6. Rating changes
7. Context events
8. False-story patterns to refuse

## 1. Order of work per flagged day

Research every day in `compute.py`'s `candidates` list. There is no cap; a flagged day left
unresearched blocks the render.

1. **Company releases first.** Ask for "<company> (<ticker>) press releases and company news
   headlines from <day-1> to <day>, with the date and time of each." The press-release feed
   (`source_name` Market Data, titled "Company Press Releases") carries reliable times.
2. **Keep news windows to 1-2 days.** Feeds return newest-first and truncate; a 10-day window
   came back missing the day that mattered. Re-query a single day if needed.
3. **Filings and transcripts for content.** Guidance figures and management's stated reasons
   come from the 8-K, 10-Q or call transcript, one quarter per question where possible.
4. **Write the event as you go**, straight into `events.json`.

## 2. The timing rule

A cause must be public before the close of the session it is said to have moved.

- Release at or after 16:00 local close: it moves the **next** session (`t0`).
- Release before the open or during the session: it moves the same session.
- Only press-release-feed times are trusted. News-feed times mix time zones across outlets
  (one outlet in UTC, another in ET), so secondary items are used at date level only.
- A release whose time is unknown cannot be "confirmed"; describe it as context and attribute
  the move to the reported reaction (example: a Friday developer conference, then Monday's
  price-target raises).

## 3. Attribution tiers

| Tier | Requirement | On the page |
|---|---|---|
| `confirmed` | A company filing or press release, timestamped, inside the timing window | Filled marker, "Company-confirmed" |
| `reported` | Only secondary coverage (News/Web) inside the window names the cause | Outlined marker, "Reported in news" |
| `none` | Nothing in the window explains the move | Hollow dashed marker, shown by default |

`none` is a finding, not a failure: a large stock-specific move with no cause is information.
Coverage that only describes a move ("traders re-priced", "risk-off selling") is not a cause;
those days are `none`.

Source tier comes from each reference's `source_name`, not the answer text: `Filings` and
`Press Releases` (and the press-release feed) are company sources; `Transcripts` are company
words but carry no release time; `News` and `Web` are secondary.

## 4. Categories

Use one of: `Earnings and guidance`, `Product and demand`, `Product and pricing`,
`Product and strategy`, `Regulatory and legal`, `Management change`, `M&A and capital`,
`Sell-side rating change`, `Sell-side commentary`, `Sector rotation`, `Macro`, `Unattributed`
(for tier `none`). A new category is acceptable if none fits; keep it short.

## 5. Results days and the guidance check

- Every results reaction the screen flags must be a callout (enforced).
- Beat or miss is measured against the **company's own prior guidance**, never consensus.
  Consensus is not available on the account, and headlines quoting "estimates" are dropped.
- Put the check in `guidance_check` (e.g. "March-quarter revenue +17% vs a 13-16% guide: above
  range"). If the company gives no numeric guide, say so rather than inventing a comparison.
- A results day that does *not* clear the screen still appears as a context event.

## 6. Rating changes

- Rating changes and price-target moves on the same day as a company release are a
  **reaction**, listed in `follow_on` as counts ("5 downgrades, 5 further price-target cuts"),
  not the cause.
- On a day with no company event, a rating change can be the cause (`Sell-side rating change`).
- Broker names never appear in visible text; they stay in the source titles. Deduplicate the
  same broker/action/day re-posted by a second outlet before counting.

## 7. Context events

Major company events that did **not** clear the screen still belong on the chart, as open
triangles on the axis, with no causal claim: results days, management changes, large M&A,
capital-return announcements. Put them in `context_events` with their reaction-day date and a
company source. "Apple's CEO succession barely moved the stock" is itself a takeaway.

## 8. False-story patterns to refuse

Each of these appeared in earlier outputs and is now blocked or ruled out:

- **Macro headline on a single-stock day without checking the market.** If the benchmark
  explains the move, it is a market-driven day (grey diamond), not a story.
- **One day-one headline "explaining" a multi-week drift.** Drift between events stays
  unexplained; only flagged sessions carry causes.
- **Period bands that end on the event.** Phases are bounded by turning points or results
  eves, and the event sits inside the phase it moved.
- **After-close releases attributed to the release day.** Use `t0`.
- **Consensus "beats" from headlines.** Compare to company guidance.
- **Internal ids or broker names in visible text.** Blocked by the validator.
