# State detection

Moved out of `SKILL.md` to keep it lean; read it before the first edit.

## STATE DETECTION (before any edit)

Most rolls go wrong here rather than in the arithmetic. Where the model came from a
from-scratch build it carries a known row-map and a hidden `_Protocol` — read it and
skip to the last item. For an unfamiliar third-party model, establish all of it and
**state what was found in the roll plan** so the analyst can correct a
misreading before it propagates:

1. **Sheet inventory and classification** — every sheet as input, downstream or
   valuation, per the rule above.
2. **The last-actual boundary.** Which column holds the most recent actual, on each
   sheet, and how status is expressed — an explicit status row, a formula off a
   last-actual-year cell, or a formatting convention. Where status is a formula,
   an FY roll re-cascades the forward labels automatically: let it, and never
   hand-edit a label.
3. **Period grammar.** Annual only, or the eight-column interim block
   (Q1 │ Q2 │ H1 │ Q3 │ 9M │ Q4 │ H2 │ FY). Which columns are reported and which
   are derived by subtraction. Whether headers are typed or generated from a date
   cell — where generated, the block extends by extending the date, not by typing
   a header.
4. **Which interims the company actually reports.** A half-year reporter's Q2 and
   Q4 columns are derived, not reported, and must stay formulas.
5. **The input/formula map** on every sheet you intend to write to, and the
   convention that marks an input — usually a distinct font colour. Write only
   where inputs live.
6. **Analyst overrides.** Cells that deviate from the sheet's own pattern: a
   hardcode in a row of formulas, a formula edited mid-row, a value that does not
   follow its driver. These are the analyst's view, and they are the thing this
   skill most easily destroys. Enumerate them before writing and re-check them
   after.
7. **Named ranges and row codes**, if any — the safe anchors for anything
   structural.
8. **External links and UDFs** — references to another file, and consensus-feed
   functions. Both are destroyed by an openpyxl roundtrip and are the reason for
   the in-app or zip/XML rule.
9. **Identity and check rows** already present. Use the model's own checks as the
   post-roll test rather than inventing new ones.
