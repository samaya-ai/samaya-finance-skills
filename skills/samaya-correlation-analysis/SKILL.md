---
name: samaya-correlation-analysis
description: >-
  "correlation analysis", "which of these stocks move together", "what drives co-moves" — the 10
  most correlated groups of outsized co-moves across a ticker list, with return correlation, beta
  and a Samaya-proven driver for each shared day, published as a report.
---

# Correlation Analysis

Two ready-made scripts sit in `scripts/` next to this file. They do all the math and build the whole page, so you never write that code yourself:

- `scripts/analyze.py` — moves, market-wide days, top 10 groups, return correlation and beta.
- `scripts/build_report.py` — builds the page: driver chart, tables, per-date proof, each group's common driver and benchmark caveat, and the methodology. Every source id links straight to its source. It checks the numbers and source ids, and refuses to build if they don't agree.

Both use the Python standard library only. Your work is the Samaya lookups, tagging each date with a driver and its source ids, writing each source once, and writing a few short sentences.

## Samaya rules
- Use `financial_qa` for every lookup. If it returns `running`, poll `financial_qa_result` with the `job_id`. Never re-call for the same question.
- Keep the user's range wording verbatim in the question, for example "last 6 months" or "Jan 1 2026 to Jun 30 2026".
- `financial_qa` returns citations, not answers. Write your own answer from the snippets.
- Use each reference's `publication_date` as its date. If it has none, write "undated". Never guess a date.
- Batch related lookups into one call. Aim for 6-10 `financial_qa` calls per run.

## Input
- A list of tickers.
- A date range. If the user doesn't give one, ask for it before starting.
- A benchmark. Default to SPY unless the user names another.

## Steps

1. **Pull prices.** Call `financial_qa` for daily closing prices over the range for every ticker and for the benchmark.
   - Include the close on the trading day before the range starts, so the first day has a % change.
   - For long lists, split into parallel calls of about 5 tickers each, with fresh sessions.
   - Write the closes to `prices.csv`: first column `date` (YYYY-MM-DD), then one column per ticker plus the benchmark, oldest row first. The first row is the close before the range starts.
   - Keep each ticker's price reference `url` for `prices_sources` in step 4.
   - If a series comes back incomplete, report it and ask the user for a price file. Never fill gaps with estimates. (The script also stops and lists any empty cell.)

2. **Run the math.**

   ```
   python scripts/analyze.py prices.csv --benchmark SPY --out analysis.json
   ```

   Don't rewrite this logic. The page's Methodology section explains it to the reader. `analysis.json` lists each group's co-move dates, with direction, a market-wide flag and the benchmark's move that day. Every date has `"driver": null` and `"sources": []` for you to fill.

3. **Find and prove the driver for each date.**
   - Collect the co-move dates across the 10 groups.
   - **List the usual drivers first.** For each group, write down the 3-5 things that usually move that industry, using your own judgment. For example: banks → Fed decisions and speeches, 2-year and 10-year yields, capital returns, earnings; airlines → jet fuel, travel demand, labor news; semis → peer earnings, export rules, AI spending news. Ask about these in your Samaya questions, and name them in `proof_note`.
   - Call `financial_qa` in batches of 5-8 dates. Name the tickers and ask for news plus the move in the market variable that drives them, and say you don't need stock price history (you already have it). For example: "For Sept 3, Sept 10 and Sept 17, 2026: what news moved XOM, CVX and COP, and how did crude oil move each day? News and commodity moves only, no stock price history."
   - Pick the market variable for each group: crude for oil names, Treasury yields for banks, and so on (gold for gold miners, the US dollar for exporters).
   - For market-wide dates, also ask what moved the broad market.
   - Tag **every** date in every group with exactly one driver key:

     | Key | Category |
     |---|---|
     | `oil` | Oil or commodity prices |
     | `fed` | Fed / interest rates (rate moves, Fed commentary, Treasury yields) |
     | `earnings` | Earnings, dividends, buybacks (the company's or a peer's) |
     | `inflation` | Inflation and macro data (CPI, PPI, PCE, payrolls, PMI, GDP) |
     | `consumer` | Consumer demand data |
     | `sector` | Sector news or regulation |
     | `none` | No clear news found |

   - **Proof rule.** A date gets a driver only if a dated Samaya source shows one of these:
     - news about that driver on that day, or the evening before for a move at the next open (say "prior evening" in the source's fact); or
     - a meaningful same-day move in the driving market variable that fits the stocks' move (for example "WTI −5%" on a day the oil names fell).

     Otherwise tag it `none`. Never guess. Record the proof as source ids on the date (`"sources": ["S3"]`).
   - **What counts as meaningful is your judgment.** There is no fixed cut-off, because a normal day differs by market and period. As a guide, a move is usually meaningful if it is larger than that variable's normal daily move over the range. Weigh the market and the event: a small move on a Fed decision day can matter; a large move with no news may not.
   - **Direction.** Usually the market variable and the stocks move in the way you'd expect (crude down, oil names down). Where the link can go either way, for example yields and banks, don't reject a day on direction alone; rely on what the source says.
   - **Show the judgment.** Every source's `fact` must include the size of the move or the specific event ("WTI −2.0%", "2-year +14 bp", "Fed hikes 25 bp"), so the reader can judge whether it convinces them.
   - If one day has several candidate causes, use the market variable to decide. If yields jumped, it was rates.

4. **Fill in report.json.** Copy `analysis.json` to `report.json`. Keep every number as is. Add only these fields:

   | Field | What to write |
   |---|---|
   | `title` | Short page name, 2-4 words, for example "Energy and Banks Co-moves" |
   | `range_label` | The user's range wording, for example "last 3 months" |
   | `takeaway` | 1-2 plain sentences: the main driver of each cluster, no dates or detail. If no cluster of 3 or more names survived, say so briefly. Then **one implication sentence**: what this means for someone holding or hedging these stocks, based only on numbers in the report (beta, return correlation, driver share). For example: "Implication: the energy names act as a hedge against the market (beta about -1 vs SPY) but share one risk, oil, so holding several of them adds little diversification." State what the data shows; don't recommend trades. If the numbers don't support a clear implication (for example weak correlations, mixed betas, or mostly grey days), write "Implication: no clear implication from this data." Never stretch weak evidence to fill this sentence. |
   | `driver_how_to_read` | One sentence on which colors dominate which bars and what that means |
   | `driver_themes` | Optional. The main theme behind a category, for the legend, for example `{"oil": "mostly US-Iran news"}` |
   | `drivers_summary` | At most 3 short bullets, one per main driver, under 50 words each: `[{"name": "Rates and the Fed", "text": "..."}]`. See below. |
   | `proof_note` | One or two sentences for the Methodology: the usual drivers you checked for each group, which market variable you used, and what you treated as a meaningful move. For example: "Crude (WTI, Brent) for the energy names; 2-year and 10-year Treasury yields for the banks. Moves under about half a normal day's move were not counted unless a source tied them to a specific event." |
   | `evidence_sources` | Every source you cite, written once (the page has no separate source list: each id in the groups table links to the url, and hovering shows the title, date and fact): `{"S1": {"title": ..., "date": "YYYY-MM-DD" or "undated", "url": ..., "fact": "WTI -5% as US-Iran fears eased."}}`. The fact is one short line with the number or event that proves the date. |
   | `prices_sources` | One per ticker and the benchmark: `[{"ticker": "XOM", "url": ..., "date": "YYYY-MM-DD"}]` |
   | per date: `driver` | One key from the table in step 3 |
   | per date: `sources` | The ids of the sources that prove it, for example `["S1", "S2"]`. Empty for `none`. |

   Do **not** write the per-group evidence, common driver, benchmark caveat or methodology. The script builds them from the per-date tags.

   **Writing `drivers_summary`.** Short and factual. Each bullet gives: the counts (how many groups or days it explains), 2-4 dated examples, and one caveat if it changes the reading. Example:

   ```json
   {"name": "Oil, mostly US-Iran news",
    "text": "Leads 3 of 7 energy pairs (8-9 days each) and about half of the rest. Crude rose on Hormuz attacks (07-31, 08-10, 08-31) and fell when tensions eased (08-03, 09-16). 5-10 days per energy pair have no clear news."}
   ```

5. **Build and publish.**

   ```
   python scripts/build_report.py report.json --out report.html --fragment
   ```

   - Use `--fragment` when publishing with the Artifact tool (it adds the page skeleton). Leave it out for a standalone HTML file.
   - If the script stops with a list of problems (a missing driver, a driver with no source id, an unknown source id, counts that don't add up, a Drivers bullet that is too long), fix `report.json` and run it again. Never edit the HTML by hand.
   - Publish `report.html` with the Artifact tool. In the chat reply, give the takeaway in 1-2 sentences.

## What the page shows (built by the script)

1. **Takeaway.**
2. **Driver chart:** one horizontal bar per group, sorted by score, on a 0-100% axis, split into colored parts by driver with the day count in each part. "61% · 19 days" sits to the right. Fixed colors: oil orange, Fed blue, earnings teal, macro data purple, consumer pink, sector olive, no clear news light grey. Legend and "How to read it" line below.
3. **What drove the co-moves:** up to 3 short bullets.
4. **Groups table:** score (with the fraction), return correlation, each member's beta vs the benchmark, co-move days with ↑/↓ split, market-wide days and how many of them the benchmark moved the other way, the common driver (named only when one driver covers more than half the days) with the day mix and a benchmark caveat, and every date with ↑/↓, * for market-wide, its driver and source ids that link straight to each source.
5. **Dates with no supporting source.**
6. **Average moves table:** each ticker's average daily move, beta and correlation vs the benchmark, sorted high to low, benchmark row last.
7. **Market-wide days.**
8. **Methodology:** how prices (with links to the price data), big moves, market-wide days, scores, groups, correlation, beta and the proof rule work.

Light and dark mode both work. On a phone, the chart and tables scroll sideways inside their box, and the page itself never scrolls sideways.
