# The dual scorecard, the scoring taxonomy and consensus accuracy against guidance

Moved out of `SKILL.md` to keep it lean; read it before scoring the first row.

## Contents

- THE DUAL SCORECARD
- SCORING TAXONOMY
- CONSENSUS ACCURACY

## THE DUAL SCORECARD — mandatory, and the heart of the analysis

Score every row **twice**, in two separate tables:

- **Table A — against the guide in force at period-end.** The final standing guide, after every
  revision.
- **Table B — against the initial guide.** The guide issued at the start of the period, before
  any revision.

**The gap between the two tables is the finding**, and the output states it explicitly. A company
that resets its guide to the current run rate late in the year will score close to perfectly in
Table A while carrying real misses in Table B. Table A alone flatters management and carries
almost no forecasting information; Table B is the one that tells the analyst whether the guide
they are reading today is worth anything.

Where the two tables diverge, say which years drive the divergence and which management team
issued them. Where a year had no revisions, the row is identical in both tables and that is
itself worth noting — an unrevised year is a stronger signal than a hit.

Both tables appear even at Brief depth. Neither is ever omitted for length.

## SCORING TAXONOMY — fixed, stated in the output

**Ranged guidance:** `Below range / Low end / Mid / High end / Above range`.
**Point or "approximately" guidance:** `Miss / In line / Beat`. In line is set by metric
class, because one tolerance across every line is a false equivalence — ±2% on revenue
is a far wider bar than ±2% on EPS:

| Metric class | In line within |
| --- | --- |
| Revenue, volume, units | ±1% |
| EBIT, EBITDA, net income | ±2% |
| EPS, DPS | ±3% |
| Margins, returns, ratios | ±25bps |
| Cash flow, capex, working capital | ±5% |
| Leverage, net debt | ±0.1x |

State the table in the appendix so the reader can disagree with it, and let the
analyst override any row at kickoff. Where a metric does not fit a class, state
the tolerance chosen and why.
**Directional guidance** ("modest growth", "improvement on last year"): score
`Consistent / Inconsistent / Cannot be checked`. A guide that cannot be checked is itself a
finding — a management team that guides in language that cannot be checked is telling you
something.

Every verdict carries a magnitude (bps or %) and the guide vintage it is scored against.

## CONSENSUS ACCURACY AGAINST GUIDANCE — optional section

Assesses how well the market forecast this company over the lookback, alongside how well management
guided it. Retrieval-bound: built only from dated consensus actually retrieved at each point, never
from a current consensus figure applied backwards, and never estimated from a single broker's
forecast. When selected, this section runs after the scoring sections and before the credibility
verdict.

Three components, each run only where dated consensus returns:

- **Consensus against the guide.** At each guidance event, record where consensus sat relative to
  the guidance issued that day — above, within or below the range, and by how much. Where consensus
  sat outside a stated range, note it explicitly.
- **Consensus against delivered.** For each period, compare the consensus in place at the initial
  guide, and the consensus immediately before the print, against what was reported. State direction
  and magnitude of error in both cases.
- **Response to revisions.** Where guidance was revised mid-period, establish whether consensus had
  already moved in that direction before the revision or only after it. Report the sequence and
  dates; do not characterise the market as having anticipated or missed anything beyond what the
  dates show.

**Hard rules for this section.** Dated historical consensus is frequently not retrievable — where a
vintage is unavailable, leave it blank, name the date that failed, and continue; never substitute a
nearby date, carry a figure forward, or estimate from a single broker. Where fewer than three
guidance events have retrievable dated consensus, state that the sample cannot support a directional
read and report individual observations only. Where consensus is on a different metric definition to
the guided metric, say so and do not compare the two. Every figure carries its Samaya provenance
link and its as-of date. This section assesses forecast accuracy against the record; it makes no
claim about whether consensus is currently mispriced.
