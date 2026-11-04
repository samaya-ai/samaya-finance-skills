---
name: samaya-risk-tracker
description: >-
  "risk factors", "what changed in the risks", "risk tracker" — extracts disclosed risks from a
  company's latest filing, shows material changes vs the prior filing side by side, verifies new
  risks, and scores likelihood against current events via Samaya.
---

# Risk Tracker

## Samaya rules
- Use `financial_qa` for every lookup. If it returns `running`, poll `financial_qa_result` with the `job_id`. Never re-call for the same question.
- Keep relative time wording ("most recent 10-K", "prior 10-K") verbatim in the question.
- `financial_qa` returns citations, not answers. Write your own answer from the snippets. Cite each source with its date and link.
- If a source has no publication date, cite it as "undated". Never guess a date.
- Batch related lookups into one call. Aim for 10-14 `financial_qa` calls per company.

## Input
One or more companies. Run the steps for each company.

## Steps

1. **Current risks.** Call `financial_qa` for the risk-factor headings and text in the most recent 10-K or 20-F.

2. **Interim updates.** In a separate call, ask for every risk factor listed in Item 1A of each 10-Q filed since that annual filing, with its full text and the 10-Q's filing date. A 10-Q lists only risks it adds or changes ("Other than the risk factors listed below…"), so each one is a candidate change. Skip this step for a 20-F filer with no 10-Qs.
   - **Completeness check:** ask in one batched call how many risk factors each 10-Q's Item 1A lists, and fetch any you are missing. A 10-Q risk is easily crowded out of a broad answer.

3. **Prior risks.** Call `financial_qa` for the risk-factor headings and text in the prior annual filing.

4. **Compare.**
   - **Match headings first.**
   - **10-Q risks:** compare each one with the current annual filing. A heading not in it is New, labelled "New (10-Q, <filing date>)". A heading that is in it is Escalated, Softened or Wording only against the annual text.
   - **Removed headings:** for any heading that looks removed, make one batched call that asks whether it appears in the current filing. Tag it Removed only if it doesn't.
   - **Change types.** Tag each remaining risk with one:
     - **New:** not in the prior filing. Provisional until step 5.
     - **Removed:** in the prior filing but not the current one.
     - **Escalated or Softened:** a material change. A change is material only if it adds or drops a named event, a figure, or new scope (a product, region, counterparty or regulation).
     - **Wording only:** any other edit, such as "may" to "is" or an added adverb.
     - **Unchanged.**
   - **Quotes:** for every New, Removed, Escalated or Softened risk, capture the prior text and the new text, quoted.

5. **Verify new risks.** For each provisional New risk, make one batched call against the prior annual filing (and, for a 10-Q risk, the current one too). Search on the risk's topic and key terms (for example "financial guarantees", "counterparty", "capacity commitments"), not just its heading.
   - **Same risk under another heading:** re-tag it against that heading as Escalated, Softened or Wording only. Put the prior text in the Prior text column.
   - **Nothing on the topic:** keep it as New and mark it "New (verified)".
   - **Only partial coverage** (the topic is mentioned but not as a risk): keep it as New and quote the partial prior text.

6. **Current events.** Group related risks into 5-6 `financial_qa` calls for recent news, management commentary and research.

7. **Score likelihood (1-5)** that the risk comes into play over the next 12 months:
   - 5: already happening
   - 4: clear, active catalyst
   - 3: plausible, with some signals
   - 2: few signals
   - 1: no current signal

   Any score of 3 or higher needs at least one dated, direct source. Give a one-line reason for every score. Removed risks get "n/a".

## Output

**1. Takeaway.** 1-2 sentences naming the most important change and the risk most likely to come into play.

**2. Main table.** New, Escalated, Softened and Removed risks only.

| Risk | Change | Prior text | New text | Likelihood (1-5) | Current-event evidence |
|---|---|---|---|---|---|

- Sort by change type: New, Escalated, Softened, Removed. Within each type, sort by likelihood, high to low.
- For New risks, write "—" in Prior text (or the partial text found in step 5).
- For Removed risks, write "—" in New text.
- For a change made in a 10-Q, name that 10-Q and its filing date in the Change cell.

**3. Notes** (at the end, short).
- **Wording-only edits:** one line per risk giving the risk name and what changed, for example "'may be subject to' → 'is subject to'".
- **Unchanged risks:** one line per risk with name, likelihood and a short reason. List any risk scored 4-5 first.

Cite each filing by form type and filing date, and each event by source, date and link.