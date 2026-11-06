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

Research every day in `compute.py`'s `candidates` list (both `strong` and `price` signals),
every multi-session `run`, and every story phase that contains no flagged day. There is no
cap; anything left unresearched blocks the render.

Go down the source ladder and stop at the first rung that explains the move:

1. **Company releases and filings.** Ask for "<company> (<ticker>) press releases and company
   news headlines from <day-1> to <day>, with the date and time of each." The press-release feed
   (`source_name` Market Data, titled "Company Press Releases") carries reliable times.
2. **News, asked as a "why".** Ask "Why did <company> (<ticker>) stock move <x%> on <date>?
   Company news coverage from <day-1> to <date>, with the date and time of each." This phrasing
   makes Samaya match news against the price move and returns newswire items (`source_name`
   News) whose text carries an explicit time (e.g. "05:56 AM EDT, 07/02/2026").
3. **Web, tested on what it is.** Web results from rungs 1-2 can explain a move only if they
   pass section 3b. Never cite a "why the stock moved" piece; follow it to the event it names.
4. **X, last.** Only when rungs 1-3 explain nothing: "Posts on X about <company> (<ticker>)
   stock on <date>." Rules in section 3a. Never ask for or cite Reddit.

Also:

- **Keep news windows to 1-2 days.** Feeds return newest-first and truncate.
- **Runs and drift phases** get one "why" question over the whole window ("Why did <company>
  (<ticker>) stock rise between <start> and <end>?"); record the answer or "none found".
- **Filings and transcripts for content.** Guidance figures and management's stated reasons
  come from the 8-K, 10-Q or call transcript, one quarter per question where possible.

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
| `reported` | News or Web coverage inside the window names the cause | Outlined marker, "Reported in news" |
| `social` | Nothing above; X posts dated that session (or the prior one) discuss it | Dotted marker, "Context from X posts that day, not a confirmed cause" |
| `none` | Nothing explains the move | Hollow dashed marker, shown by default |

`none` is a finding, not a failure: a large stock-specific move with no cause is information.
Coverage that only describes a move ("traders re-priced", "risk-off selling") is not a cause.

Source ranking comes from each reference's `source_name`, not the answer text:

| `source_name` | Can set | Timing |
|---|---|---|
| Filings, Press Releases, press-release feed | `confirmed` | Release time |
| Transcripts | supports any tier (company words) | No release time |
| News with a time in the text | `reported` | Usable for the before/after-close rule |
| News without a time | `reported` | Date-level only |
| Web, passing section 3b | `reported` | Date-level only |
| Social Media, X posts only | `social` (never higher) | Date-level only; no time of day |
| Social Media, Reddit | nothing: excluded | Posts carry no date at all |

### 3b. Rules for Web sources (no allowlist)

A Web result counts toward an explanation only if it passes all four tests, whoever publishes
it, in any language:

1. **It reports an event, not the move**: a scoop, announcement, filing, ruling or data
   release, with specifics. "Shares rose 4%" is not an event.
2. **It is attributable**: a named publication with a byline, and named sourcing (company
   statement, documents, "people familiar").
3. **It is not a rationalization**: no "why the stock moved" explainer, opinion piece,
   price-target blog, aggregator or data page, or auto-generated mover note.
4. **It is dated no later than the reaction day.**

Record each Web source with `publisher`, `kind` (`original_report`, `primary_document` or
`wire_relay`) and `evidence` (a quote of at most 30 words stating the event). The validator
blocks: missing fields; a publisher not visible in the title (or a stored `byline`); hedged
evidence ("appears to", "may have", "likely"); explainer headlines carrying a tier on their own;
a Web-only explanation without a primary document or two independent publishers, unless the
event is marked `single_source: true` with exactly one original report (shown as "Reported, single
source"; a `wire_relay` copy of the same article never counts as a second source); and a short
blocklist of publishers seen producing post-hoc move explainers (StockStory, Quiver, MarketBeat,
Finbold, Invezz, 24/7 Wall St, TipRanks, Simply Wall St, chart and social-tracker pages). Add to
the blocklist only when a publisher causes a real false story.

### 3a. Rules for X

- Last resort only, and only for the session date (or the prior session). X posts carry a date
  but no time, so they can never satisfy the before/after-close rule.
- Write what the posts discussed, not a cause: "Posts on X that day focused on ...".
- When a post relays a newswire headline, find and cite the underlying news item instead; that
  makes the day `reported`.
- Drop posts that are price ticks, consensus comparisons, price targets or buy/sell calls. Keep
  account handles out of visible text (they may stay in source titles), as with broker names.
- Expect coverage only for recent weeks; older dates usually return no posts.

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
- **"Quiet days" as an explanation.** A phase that rose on unflagged days still gets researched
  as a window; describe its shape ("five moderate up days did most of the work"), never imply
  that nothing happened.
- **Social chatter promoted to a cause.** X is context; Reddit is never used.
- **Internal ids or broker names in visible text.** Blocked by the validator.
