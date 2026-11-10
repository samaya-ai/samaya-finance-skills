# Retrieval, gap pass and reconciliation — samaya-kpi-history

Read before the first retrieval call. These rules apply in full to every run.

## RETRIEVAL — chunked internally, parallel, delivered once

1. **Chunk by cadence** so each call asks for roughly 8–12 data points; asking for more is what
   produces sparse answers:
   - Monthly metrics: **one year per call** (12 points).
   - Quarterly metrics: **two years per call** (8 points).
   - Half-yearly or annual: **the whole window in one call**.
   - Multiple metrics for one company: keep them in the same call only while the chunk stays
     inside the point budget.
2. **Anchor each chunk to the documents, not just the periods.** Name the documents the map says
   carry the figure — "from the Q1–Q4 2024 earnings call transcripts and the monthly operating-data
   8-Ks filed in 2024" — so Samaya reads known documents instead of searching for periods. A chunk
   is the set of documents that report its periods, which may be filed after the period ends.
3. **Run chunks in parallel**, up to five at a time, each with a fresh session_id. Each call asks
   for, per period: the value, the unit, the company's period label, the document and its date,
   and the sentence or table row containing the figure.
4. **Keep only what the grid needs.** As each result lands, take per period the value, unit,
   status, document title, date, URL and the one sentence or table row containing the figure.
   Do not quote or carry the rest of the snippet text forward.
5. **Poll in rounds.** Poll every running job in the same round, not one job repeatedly, and
   leave time between rounds; each poll returns the job's whole progress log, so frequent polls
   cost tokens without speeding anything up.
6. **Estimate up front.** Before the first call: `8 years quarterly · 4 parallel pulls · about
   2–3 minutes.`
7. **Progress lines, not partial files.** As each chunk lands, post one line in chat:
   `2019–20 ✓ 8/8 · 2021–22 ✓ 7/8 (Q3 2021 queued for re-query)`. Do not send partial workbooks;
   the analyst should never have to stitch chunks together.
8. **Slow-chunk rule.** If one chunk is still running about two minutes after the others have
   finished, split its period into two narrower queries, each in a fresh session, and leave the
   original running; use whichever answer lands first and reconcile any overlap. Never re-send
   the same question.
9. **Large-job exception.** Where the run exceeds roughly 20 Samaya calls (many companies × many
   years), deliver the **most recent chunk first** as a clearly labelled preview Excel (attached,
   downloadable), then fill backwards and deliver the complete workbook at the end.
10. **Record the clock.** Note the timestamp of the first retrieval call and of the final
   workbook; the elapsed time goes in the scorecard.

## GAP PASS — re-query only the missing periods

After the parallel pass, every empty or unsourced cell is re-queried. Never re-run a whole chunk
to fill one cell.

1. **One batched, targeted query.** Ask for all the missing periods together, naming for each the
   document it should be in: "XPO shipments per day YoY for September 2025 (Q3 2025 earnings
   call) and March 2026 (Q1 2026 earnings call)." Any period the batch leaves empty is re-asked
   on its own. Gaps in the first (combined) block are batched and sent alongside the remaining
   chunks rather than after them. A value cut off mid-snippet ("March was up 7.") is a gap, never
   a guess.
2. **Alternative source class, period-based.** If still empty, drop the document anchor and ask
   by period, or try the other places the disclosure map says the figure can live — the call
   transcript instead of the release, the 10-Q instead of the presentation, or the **prior-year
   comparative in the following year's disclosure** (the Q3 2024 release usually restates Q3
   2023). A value recovered from a comparative is labelled as such.
3. **Then stop and say why.** After two targeted attempts the cell is final, with a status and a
   reason: `Not disclosed — company reports Q3 only as a quarterly total` or `Not retrieved —
   transcript unavailable in Samaya`. Never estimate a missing period silently; where a value can
   be derived (a quarter from a half less the prior quarter), it may be added only as `Derived`,
   with the calculation in its Note.

## RECONCILIATION — before anything is written as final

- **Final over preliminary.** A monthly flash later revised in the quarterly release takes the
  revised value; the Note records both.
- **Restatements.** Where a later disclosure restates a period, use the figure on the basis the
  series is presented on, and say which.
- **Definition breaks split the series.** A redefined metric is two series with a marked break,
  not one stitched line.
- **Units and basis are fixed per column**: currency, reported vs constant currency, organic vs
  reported, absolute vs YoY %, short vs metric tons.
- **Fiscal vs calendar.** Keep the company's period label; add the calendar period alongside.
- **Latest disclosure wins.** A preliminary monthly release is superseded by the later release or
  call that restates it; the row records both values.
- **Window end.** The default window ends at the latest period the company has reported. Where a
  named window runs past it, the unreported periods carry `Not yet reported` with the expected
  release, and are not counted as gaps.
- **Status on every row**: `Final`, `Preliminary`, `Derived`, `Comparative`, `Proxy`,
  `Not disclosed`, `Not retrieved`, `Not yet reported`.
