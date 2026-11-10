---
name: samaya-end-market-exposure
description: >-
  "end market analysis", "exposure breakdown", "who are their customers and suppliers" — breaks a
  company or sector into end markets and geographies with revenue mix, suppliers, competitors, and
  drivers backed by historical instances.
---

# End Market / Exposure Analysis

## Samaya rules
- Use `financial_qa` for every lookup. If it returns `running`, poll `financial_qa_result` with the `job_id`. Never re-call for the same question.
- Keep relative time wording ("most recent", "latest annual filing") verbatim in the question.
- `financial_qa` returns citations, not answers. Write your own answer from the snippets. Cite each source with its date and link.
- If a source has no publication date, cite it as "undated". Never guess a date.
- "Annual filing" means the company's main annual report: 10-K, 20-F, or the local equivalent (for example a Japanese securities report or an annual report).

## Batching
Aim for about 8 `financial_qa` calls for one company and about 15 for several companies.

| Call | Content |
|---|---|
| 1 | End markets, revenue mix, customers and concentration, and geographic mix, all together |
| 2 | Suppliers and inputs |
| 3 | Competitors across all end markets |
| 4 and on | Driver evidence, 2-3 drivers per call |

- **Several companies:** cover 2-3 companies per call in call 1, and run calls 2-4 across all the companies at once.
- **Parallel calls:** run independent calls at the same time, each with a fresh session.

## Input
- **One company:** use the single-company layout.
- **A sector or a list of companies:** for a sector, first ask Samaya for its 5-8 largest public companies. Use the multi-company layout.

## Steps

1. **End markets and revenue mix.** For each end market, get the share from the most recent annual filing. Also get the latest quarter or half-year where it's disclosed on a call or in an interim filing.
   - Show both figures side by side, labelled with the fiscal year and the latest period.
   - Label the base of every percentage, for example "% of total revenue" or "% of systems revenue". Never compare figures on different bases.
   - Label management estimates such as "roughly a third" as commentary.
   - Leave undisclosed shares blank.
2. **Customers.** Customer industries and named major customers. Include concentration disclosures, such as any customer above 10% of revenue.
3. **Geographic exposure.** Revenue by region or country, from the annual filing and the latest period. Note any region-specific risks, such as export controls, tariffs or FX.
4. **Suppliers.** Major suppliers and key inputs. Note any single-source or concentration disclosures.
5. **Competitors.** Competitors and major players, with market share where it's available.
   - If only a company-wide competitor list is disclosed, show it once below the table. Don't repeat "not broken out" in every row.
6. **Drivers.** For each end market, list 2-4 drivers. A driver that affects every end market goes in one "All markets" row.
   - Upstream: input costs, supply constraints, supplier capacity.
   - Downstream: customer demand, capex cycles, regulation, macro.
7. **Evidence.** For each driver, find 2-3 historical instances where the driver moved and the company's (or peers') results or commentary followed.

## Output

1. **Takeaway:** 1-2 sentences, for example: "AI data center demand is now over 40% of revenue and the main swing factor; auto is shrinking in mix."

2. **End-market table.**
   - **Single-company layout:**

     | End market | % of revenue (annual FY__) | % latest period (__) | Base | Customer industries / key customers | Major competitors | Source |
     |---|---|---|---|---|---|---|

   - **Multi-company layout:** a grid with companies as rows and end markets as columns. Each cell holds the % and its base. Add a short customer and competitor table below.

3. **Geographic exposure table.**

   | Region | % of revenue (annual FY__) | % latest period | Base | Region-specific risks | Source |
   |---|---|---|---|---|---|

   - For several companies, use a grid with companies as rows and regions as columns.

4. **Supplier table:** supplier or input, what it supplies, and any concentration risk.

5. **Driver table.**

   | End market | Driver | Upstream / downstream | Direction of impact | Instances (date, what happened) |
   |---|---|---|---|---|

Cite every figure and instance with its source, date and link.