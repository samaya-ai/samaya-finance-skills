---
name: samaya-historical-pattern
description: >-
  "historical pattern", "has this happened before", "precedents for X" — confirms and generalizes
  the situation, finds 3-5 similar cases via Samaya, rates how close each is, and says what they
  suggest for the current one.
---

# Historical Pattern

## Samaya rules
- Use `financial_qa` for every lookup. If it returns `running`, poll `financial_qa_result` with the `job_id`. Never re-call for the same question.
- Keep relative time wording ("last 5 years", "most recent") verbatim in the question.
- `financial_qa` returns citations, not answers. Write your own answer from the snippets. Cite each source with its date and link.
- If a source has no publication date, cite it as "undated". Never guess a date.
- Batch related lookups into one call. Aim for 6-10 `financial_qa` calls per run.

## Steps

1. **Confirm the situation.** Call `financial_qa` for the facts: who did what, when, and why.
   - If the sources don't confirm the situation as the user described it, say so in one line. Then generalize from what the sources show actually happened.
   - Record the event date.

2. **Generalize it.** Write one sentence that removes the company names and keeps the mechanism.
   - Example: RELY lowers price to match WU promotions becomes "A company responds to competitor pricing pressure by cutting its own price."
   - Note 2-3 features that matter for matching: industry structure, relative size of the players, whether the move is temporary or permanent.

3. **Search for precedents.** Run 2-4 `financial_qa` calls in parallel, each with a fresh `session_id`. Phrase them around the general situation:
   - The general situation across industries, in the last 5 years
   - The same, limited to the current company's industry
   - The same, limited to adjacent industries

   Only use instances dated before the event. You may include a later instance, labelled "peer case (after the event)".

4. **Pick and rate 3-5 instances.**
   - Rate each one for similarity:
     - **3:** same mechanism, same industry, similar structure
     - **2:** same mechanism, different industry or structure
     - **1:** same mechanism only
   - Drop 1s unless fewer than 3 instances remain. Drop any instance with no clear outcome.
   - Get outcomes (margins, share, stock reaction, and management commentary on later calls) in 1-2 batched calls.

5. **Check what happened since.** If the current event is more than 3 months old, make one call on what has happened since: results, guidance, stock move.

## Output

1. **Takeaway:** 1-2 sentences giving the main conclusion. For example: "The precedents point to share gains with modest take-rate pressure. The main risk is a de-rating, not margin damage."
2. **Situation:** the generalized situation in one line. Add a premise note if step 1 didn't confirm the situation as described.
3. **Instances:** one table per instance, ordered by similarity with the highest first:

| Field | Content |
|---|---|
| Similarity | 1-3, with a one-line reason |
| Historical situation | Company, date, what they did |
| Why it resembles now | Shared mechanism and features |
| Outcome | What happened to price, share, margin, stock, with dates |
| Implication for now | What this case suggests for the current situation |

4. **Since the event:** include only if step 5 ran. A few lines on what has already played out.
5. **Overall read:** 2-3 lines covering where the precedents agree, where they split, and the key difference from the current case.

Cite every fact with the source name, date and link.