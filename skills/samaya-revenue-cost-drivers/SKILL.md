---
name: samaya-revenue-cost-drivers
description: >-
  "revenue and cost drivers", "driver tree", "what moves the P&L" — breaks a company's revenue and
  cost segments into their drivers via Samaya and renders an HTML relationship graph.
---

# Revenue and Cost Drivers (Visual)

## Samaya rules
- Use `financial_qa` for every lookup. If it returns `running`, poll `financial_qa_result` with the `job_id`. Never re-call for the same question.
- Keep relative time wording ("most recent quarter") verbatim in the question.
- `financial_qa` returns citations, not answers. Write your own answer from the snippets. Cite each source with its date and link.
- If a source has no publication date, cite it as "undated". Never guess a date.
- Batch related lookups into one call. Aim for 6-8 `financial_qa` calls per run.

## Input
- A company.
- The period. It defaults to the most recent reported quarter.

## Steps

1. **Segments.** Call `financial_qa` for the period's revenue segments, cost lines and the rest of the P&L, with dollar values.
   - Keep the 4 largest revenue lines and the 4 largest cost lines.
   - Combine the remaining lines on each side into "Other revenue" or "Other costs", marked as calculated.
   - Rest of the P&L, fixed list:
     - Operating income
     - Net interest and other
     - Pretax income
     - Tax
     - Net income
     - Diluted shares
     - EPS

2. **Formulas.** Write how each line is built from its inputs, for example: Passenger revenue = ASMs × Load factor × Yield. Mark each value as either "reported" (it appears in a filing) or "calculated".

3. **Drivers.** Use one call for revenue drivers and one for cost drivers. Ask for each driver's current value and management's commentary on it.
   - Sort each driver into Revenue driver, Capacity / supply, or Macro.
   - Show each driver in the units the company reports it in (%, bp, units, price). Don't convert drivers to dollars.
   - If some lines get no drivers back, make one follow-up call covering all of them.

4. **Catalysts.** Ask for events that moved a macro driver during the period.
   - Record the category (for example GEOPOLITICAL or MACRO), the status (confirmed or expected), and the impact.
   - Tag any event dated after the period ended as "POST-PERIOD".
   - A catalyst that doesn't move a macro driver may point straight to the P&L line it hits.

5. **Takeaways.**
   - The 3 main earnings takeaways from the most recent call.
   - A 1-2 sentence main takeaway naming the driver that moved the quarter most.

6. **Build the HTML** (layout below), then publish it with the Artifact tool.

## HTML layout (from Scenario Analysis v3)

- **Main takeaway:** 1-2 sentences at the top, above the takeaways strip.
- **Header:**
  - Logo tile, name, ticker, exchange and sector. Leave out any field Samaya didn't return. Never show "—".
  - Title: "Drivers of the [period] P&L".
  - Include a period selector or Export button only if it works. A CSV export is fine; label it "CSV".
- **Takeaways strip:** 3 numbered one-line takeaways, labelled "REPORTED · EARNINGS TAKEAWAYS".
- **Canvas:**
  - Dotted-grid background.
  - Columns from left to right: THE P&L, REVENUE DRIVERS, CAPACITY & SUPPLY, MACRO DRIVERS, PERIOD CATALYSTS.
  - On load, scale the canvas to fit the window width so every column, including catalysts, is fully visible.
  - Zoom controls: −, + and a % readout.
- **Bands:**
  - REVENUE: green tint, green label.
  - COSTS: red tint, red label.
  - REST OF THE P&L: neutral, laid out left to right in P&L order.
- **Node card** (white, thin border, small radius):
  - Status dot and name. Dot colours: grey = calculated, green = reported input, blue = headline output.
  - Value in large monospace.
  - A formula line in small monospace, or "drives $X.XB" (the size of the line the driver feeds).
  - A citation line with a link icon, for example "10-Q Q3'26A", or "Calculated — N inputs, not reported".
  - Optional commentary below a divider:
    - At most 3 lines, with the full text on hover.
    - A source line, for example "Q3'26 call · CFO".
  - Badge "ENT" for entitled broker research.
  - Footer "ALSO IN COSTS" or "ALSO IN REVENUE" for a driver that feeds both bands.
  - Operating income, net income and EPS get a pink fill and a teal border.
  - Two node heights only: with commentary and without.
- **Edges:**
  - Smooth curved grey lines (bezier) from each driver to the line it feeds, with the arrowhead pointing into the P&L.
  - Draw the edge layer beneath the cards. Lines may pass behind cards.
  - Give each incoming edge its own attachment point, spaced along the target card's edge, so arrowheads never stack.
  - Line weight scales with the size of the line fed.
- **Catalyst card:**
  - Orange border.
  - A category tag and a status tag, including "POST-PERIOD" where it applies.
  - A one-line headline, the impact in orange monospace, and a short explanation.
  - A dashed orange curved arrow to the driver or P&L line it moves.

Every value and commentary line carries its source and date. Leave a value blank rather than estimate it.