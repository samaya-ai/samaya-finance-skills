---
name: samaya-reconciliation
description: >-
  "why don't these match", "which number do I use", "reconcile this", "does this tie out" — explains
  why conflicting figures disagree, bridges them and says which to use for what. To audit a whole
  document use samaya-fact-checker.
---

# Reconciliation

Numbers don't agree. Find out why. Say which to use.

Not a document scan — that's `samaya-fact-checker`'s job. Starts from a conflict already in hand,
two figures or more:

- "$412M vs $398M, FY24 revenue — why the gap?"
- "Bloomberg: 24.1%. 10-Q: 23.6%."
- "Segment total doesn't tie to consolidated."
- "Consensus EPS ≠ my model. Why?"
- "Three sources, three different FY25 revenue numbers — which one's right?"

## No conflict yet

One line, then ask. Nothing else — no analysis, no scoping questions first.

> "I reconcile conflicting numbers and tell you which to use. What's the conflicting information?"

## Given a conflict

**1. Same thing?** Company, metric, period, basis — all match across every figure? Half the time,
no — and that's the answer already.

**2. Verify with Samaya.** Call `financial_qa` before diagnosing anything. Don't reconcile off
memory or off what the user pasted — pull the primary source for every figure in play. Conflict
underspecified (no period, no metric, no source named)? Query Samaya first to see what real
figures actually exist near the numbers given, then ask only for whatever's still missing —
don't guess, and don't block on a question Samaya could answer first.

**3. Find the cause. Stop at the first one the sources support:**

| # | Cause |
|---|---|
| 1 | GAAP vs. non-GAAP |
| 2 | Restatement |
| 3 | Period mismatch (quarter/TTM, fiscal/calendar, pre/post M&A) |
| 4 | Consolidation basis (continuing ops vs. total) |
| 5 | FX / constant currency |
| 6 | Rounding / units |
| 7 | Segment redefinition |
| 8 | Estimate vs. actual |
| 9 | Stale source |

Don't run all nine on a case that resolves on the first. More than two figures in play, and they
don't all share one cause? Name each one's cause separately — don't force a single cause across
all of them.

**4. Bridge it.** Every figure ties back to one basis via adjustments — Number A + adjustments =
Number B, and again for C, D, however many are in play. Show the math — never just the story.

**5. Call it — scoped, never a bare verdict:**

- Non-GAAP → like-for-like comparability
- GAAP → statutory, model inputs
- Restated → anything forward-looking
- Consensus → street-expectation framing

**6. Nothing fits?** Say the gap is unexplained. Don't force a cause onto sources that don't
support it.

## Format

One number, one line. More than two or three line items → table, always:

- **Claims:** Claim | Measure | Figure | Basis | Source
- **Bridge:** Line item | $ | Running total
- **Call:** Use case | Figure | Why

Skip the prose paragraph once a table says it faster.

## Rules

- Verbatim numbers and adjustment language. Never paraphrase a figure or an add-back list.
- No source for one figure? Say so. Don't assume a cause to paper over the gap.
- The citation rules in `references/samaya-conventions.md` govern how citations get linked —
  this skill just makes sure every number and claim is actually sourced first.
- Never force-fit a cause the sources don't support. An unexplained gap is a valid answer.
- Every call names a use case. "Use X" with no reason is a defect.
- Close every answer with one line: **Checked:** what you queried, e.g. "Checked: 2 transcripts,
  1 8-K" or "Checked: 10-Q, press release."

## Before sending

- Same-thing confirmed across every figure — or each mismatch itself is named as a cause.
- Bridge ties out. Not just asserted.
- Call has a use case per figure, not one verdict.
- Every figure cited to its real source.
- Checked-sources line is there.
