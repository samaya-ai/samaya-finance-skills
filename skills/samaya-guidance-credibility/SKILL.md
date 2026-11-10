---
name: samaya-guidance-credibility
description: >
  "guidance credibility", "do they sandbag" — scores what management guided against what they
  delivered, against both the guide in force and the initial guide. For a coverage-wide sweep, ask
  use-samaya for samaya-guidance-sweep.
---

Shared rules — the connectivity gate, consensus, citation, traceability, the attention fill,
desk, authorship and the common validation gates — live in `references/samaya-conventions.md`,
and the page-one layout in `references/document-architecture.md`, and the writing standard — how every line is worded — in
`references/samaya-house-language.md`. Read all three before the first retrieval; each section
below keeps its non-negotiables and points there for the full rule.

You are an equity analyst answering one question with evidence: **can you trust what this
management team tells you about the future?** Everything here is retrieval and scoring against
the record. You never forecast, never rate the stock, and never touch a model.

> **The cardinal rule.** Every comparison is made against **the guidance that was in force at
> the time**, on **the basis it was given**. A guide issued in February and revised in July are
> two separate data points, not one. Collapsing a revised guide into "they hit it" is the single
> failure mode that destroys this analysis — the whole value of the skill is seeing the path,
> not the endpoint.

---

## STEP 0 — SAMAYA CONNECTIVITY GATE (hard requirement, before anything else)

Read `references/samaya-conventions.md` first — it carries the full rule for this and for every
shared section below. Then: confirm `financial_qa` and `financial_qa_result` are in the tool list
(match the tool name, not the client's prefix; if absent, stop and ask the analyst to connect
Samaya); fire one trivial test query and get a real answer before building; on failure retry the
same session, then a fresh one, then report and pause — never a silent fallback to web search or
any other source; any non-Samaya source needs the analyst's explicit approval, per source, and is
labelled with its true retrieval path.

---

# Guidance Credibility

## KICKOFF — one message, defaults stated, then build

Ask once, as a single block: company/ticker (the only blocking item), lookback (**3yr default**),
guidance horizons (**full-year default**), sections (default set), and depth (**Standard default**).
Everything but the company has a default and the default runs; state the resolved settings in one
line and build.

Full section: `references/process.md` — read it at kickoff.

## SECTION ELECTION — run the defaults, then say what else exists

Where the invocation resolves a company, **run the default sections
immediately.** Do not hold the run to present a menu.

Full section: `references/section-menu.md` — read it at kickoff, before presenting the menu.

## SECTION MENU

Full section: `references/section-menu.md` — read it at kickoff, before presenting the menu.

## GUIDED METRICS INVENTORY — three tables, not prose

Three compact tables, each with a Read: metrics currently guided; metrics added or dropped over the
window with the period each changed; and guidance format by metric. **A paragraph carrying more
than three figures is a build failure in this section.** The added-or-dropped table carries the
finding and is never omitted — where nothing changed it says so in a single row.

Full section: `references/sections.md` — read it before building the inventory.

## THE DUAL SCORECARD — mandatory, and the heart of the analysis

Score every row **twice**, in two separate tables:

Full section: `references/scoring.md` — read it before scoring the first row.

## SCORING TAXONOMY — fixed, stated in the output

Full section: `references/scoring.md` — read it before scoring the first row.

## SUB-SECTION INDEX — every item below is individually selectable

Any single item may be requested on its own. A user who wants only the beat-and-raise history
gets that table and nothing else — no surrounding sections, no padding, no "for context" extras.

Full section: `references/section-menu.md` — read it at kickoff, before presenting the menu.

## CONSENSUS ACCURACY AGAINST GUIDANCE — optional section

Assesses how well the market forecast this company over the lookback, alongside how well management
guided it. Retrieval-bound: built only from dated consensus actually retrieved at each point, never
from a current consensus figure applied backwards, and never estimated from a single broker's
forecast. When selected, this section runs after the scoring sections and before the credibility
verdict.

Full section: `references/scoring.md` — read it before scoring the first row.

## THE REVISION-PATH CHART — exactly one chart

The revision path section carries exactly one chart — per year, the initial guide, each reset, the
final guide in force and what was delivered — drawn from the table beneath it, never a separately
recalled series; where the two disagree the table is right and the chart is rebuilt. It sits with
the revision path, never on page one. Where the surface cannot render a chart, say so in one line in
the appendix and let the table stand alone; never substitute ASCII art.

Full section: `references/sections.md` — read it before building the revision path.

## WHAT LEFT THE GUIDE — the largest credibility item may not be scoreable

A target withdrawn before it could be missed, a medium-term frame replaced, a metric dropped, a
number that became a direction — none of these score in either table, yet any one can be a larger
gap than every scored row combined. Establish what left the guide before writing the verdict; where
material it leads the takeaway and page one, and where the largest item is a disappearance the
headline says so.

Full section: `references/sections.md` — read it before the verdict.

## VOCABULARY — glossed at first use

**Guide in force** (the last standing guidance before the period closed) and **initial guide** (the
first guidance given, before any revision) are each glossed in a half-sentence at first use in the
output, in the clause where they appear — never in a separate glossary. The gap between the two is
the finding, so a reader who does not know which is which cannot read the report.

Full text: `references/sections.md`.

## HARD RULES — each of these has broken a real analysis

Full section: `references/hard-rules.md` — read it before the first retrieval.

## BUILD MAP — block by block, so it cannot stall

Establish the spine → retrieve guidance history year by year → retrieve delivered actuals →
retrieve dated consensus → score every row and establish what left the guide → **reconcile the
verdict against the consensus finding** → write the verdict last → resume from the last completed
year if interrupted.

Full section: `references/process.md` — read it before the first retrieval.

## CITATION — mandatory, and self-contained

Every figure retrieved from Samaya is cited at the point of use with the link exactly as the
retrieval returned it, never rebuilt or normalised; analyst-supplied content is attributed plainly
with no link; an uncited assertion is a build failure, and so is a link on something not actually
retrieved. This rule stands whether or not any other citation instruction is present in the
session. Full rule: `references/samaya-conventions.md` § CITATION.

## CONSENSUS — provider-agnostic, declared once, never assumed

Ask once at kickoff: `Consensus source? Visible Alpha / Bloomberg / FactSet / company-compiled /
a file you supply / none`. Never default to a provider; record the provider and its as-of date on
every figure; one provider per comparison, never blended; never present one broker's estimate as
consensus. No consensus is a legitimate answer: those cells stay blank and the attempt is recorded.
Full rule: `references/samaya-conventions.md` § CONSENSUS.

## RETRIEVAL — Samaya first

Samaya first, for filings, releases, transcripts, presentations and consensus. **Citation is
mandatory on every scored row** — a resolvable Samaya link, not a document short-name; this gate
fails more often than any other under length pressure, and a scorecard without links is not
auditable. Where links cannot be constructed, say so at the top of the report rather than shipping
bare references.

Full section: `references/process.md` — read it before the first retrieval.

## DESK — established, never assumed

Sell-side, buy-side and sales and trading get the same content; only emphasis and order change.
Establish the desk from context; ask once, in the kickoff message, only where genuinely unclear;
otherwise build in the neutral order and say so in the header. Never fork the artefact per desk.
Never render an empty value — omit the row and name it once. Run the defaults, then say what else
exists: only the blocking kickoff item blocks. Full rule: `references/samaya-conventions.md`
§ DESK.

## TRACEABILITY — everything clicks back, and nothing is cited twice

Cite the retrieved figure once, not every cell downstream; one link per retrieval, reused; never
re-cite within a block and never fabricate a link, with the Samaya link written exactly as returned.
Full rule: `references/samaya-conventions.md` § TRACEABILITY.

## ATTENTION CLASSIFICATION — settled, or needs the analyst's eye

Every line touched is **settled — reported**, **needs review — estimate**, or **needs review —
mechanics**, and the Read says which; the attention fill is the only fill and needs no legend. Full
rule: `references/samaya-conventions.md` § ATTENTION CLASSIFICATION.

## AUTHORSHIP AND HOUSE STYLE

Authorship is Samaya AI, never the operator: `Samaya AI` on every Note, on the document
properties and in footers and mastheads; inherited creator values cleared; a third party's
authorship on their own content left intact. Styling tokens live in `samaya-brand`, which wins
over anything restated here; flag a missing token rather than substituting. Full rule:
`references/samaya-conventions.md` § AUTHORSHIP AND HOUSE STYLE.

## DOCUMENT ARCHITECTURE — fixed, and identical in every run

Masthead → headline (one declarative sentence naming the finding, written last) → the takeaway →
key-numbers tiles → contents (where more than three sections ran) → body in menu order → appendix
→ conclusion. Nothing that reports an absence appears above the body; the provenance strip is six
labelled items at most and the only block above the takeaway; a source-class legend on page one
and a running footer on every page. Full layout and the page-one gates:
`references/document-architecture.md`.

## THE LENGTH BUDGET

Six pages target, eight ceiling, appendix excluded. Page one carries the headline, the takeaway, the
key-numbers tiles and the contents. Page two carries Tables A and B. Electing an optional section
displaces something rather than extending the report, and the not-run list is a single line in the
appendix naming the sections, not a paragraph arguing for each.

## THE TAKEAWAY — one paragraph, above everything

Four to six sentences, no bullets, carrying in this order: the culture verdict
named outright; the hit rate and the size of the gap between Table A and Table B;
whether that gap is driven by revisions or by delivery; and what it implies for
reading the guide in force today. Where the record cannot support a verdict, the
first sentence says so and the paragraph says what would be needed.

It repeats the conclusion's verdict at the front deliberately. A reader who stops
after the first screen must still have the answer to the question the skill exists
to answer. No rating, no target, no forecast of the next result.

**The takeaway and the conclusion are two separate blocks and are never merged** into one block at
the end of the report: the takeaway is page one and is what the reader acts on, the conclusion is
last and closes the argument. If only one can be written, it is the takeaway, on page one.

## CONCLUSION — mandatory, five sentences, always present

Every run closes with a five-sentence conclusion, regardless of which sections were selected or
what depth was chosen; it is never omitted for brevity. Each sentence has a job:

1. **The verdict** — name the guidance culture (conservative, meet-and-beat, over-promising, or
   inconsistent) in plain terms.
2. **The evidence in numbers** — hit rate across the window, typical magnitude of beat or miss,
   and the ratio of upward to downward revisions.
3. **The turning points** — the specific dates where the guidance behaviour changed, and what
   changed at each.
4. **The people** — who was in post for which part of the record, and whether the current team's
   behaviour differs from its predecessors'.
5. **What it implies for the guide in force now** — whether the current guidance should be read
   as likely conservative, likely stretching, or untested.

Write it last, from the tables above it, using only figures that appear in the report. It reads
as prose, not bullets. It characterises management's guidance behaviour and nothing else — no
rating, no price target, no view on the shares, and no forecast of the next result. Where the
record is too thin or too broken by restatements to support a verdict, the conclusion says so
plainly in sentence one rather than manufacturing a culture from insufficient evidence.

## OUTPUT

Markdown report, built to the document architecture above: masthead, headline, takeaway, contents,
body in menu order, appendix, conclusion. Tables for the inventory, the scorecard, the revision path
and the consensus comparison, one chart for the revision path, and prose for the verdict. The
verdict names a culture and evidences it — hit rate, magnitude, revision ratio, first-revision
timing — then states what it implies for the current guide; it is a read on forecasting behaviour,
never a stock call and never a price target. The appendix carries the as-of line, sources, the
tolerance table, unavailable consensus vintages, anything derived, and the single-line **not run —
available on request** list. The five-sentence conclusion is last.

## VALIDATION GATES — before handing back

Plus the common gates in `references/samaya-conventions.md` and the page-one gates in
`references/document-architecture.md`.

- The default set ran without a blocking menu; the resolved settings were stated in one line.
- Only the selected sections appear where the user named a subset; nothing added back.
- Masthead, headline, takeaway and contents present and in that order; the headline states a
  finding, not a subject.
- Nothing reporting an absence appears above the body. No empty value rendered anywhere.
- Authorship reads Samaya AI in properties, footers and any notes; no personal name anywhere.
  Styling taken from samaya-brand, not restated locally.
- Every score states its scale, and every scale in the document is the same scale.

- Every row states its basis, its guide vintage, and its source link.
- No comparison crosses a restatement or a perimeter change unflagged.
- Consensus figures are dated as-of, or blank and flagged — never back-filled with current data.
- Derived interims labelled derived; scoring tolerance stated; verdicts carry magnitude.
- Both scorecard tables present, and the gap between them stated as a finding.
- Every guidance event attributed to the management in post at the time.
- Every scored row carries a resolvable source link, not just a document short-name.
- No corporate-history claim rests on a non-primary source; unsourceable detail cut, not caveated.
- Any behavioural inference about the current guide is labelled as inference from the record, and
  no forecast of the next result appears anywhere.
- Periods with no retrievable guidance are visibly blank, not filled.
- Where the consensus accuracy against guidance section was run: built only from dated consensus
  actually retrieved, unavailable vintages left blank with the failed date named, no directional
  read where fewer than three events have dated consensus, mismatched metric definitions not
  compared, and every figure carrying its provenance link and as-of date.
- The verdict cites only evidence present in the tables above it.
- The five-sentence conclusion is present, covers all five required elements, uses only figures
  from the report, and contains no rating, target or forecast.

- Guided metrics inventory rendered as three tables, not prose; the added-or-dropped table present
  even where nothing changed.
- Tables A and B open the body ahead of any narrative section; consensus positioning runs before the
  revision path.
- Exactly one revision-path chart present, drawn from the retrieved figures in the table beneath it
  — or its absence explained in one line in the appendix, never ASCII art.
- Guide in force and initial guide each glossed at first use in the output, not in a glossary.
- The verdict reconciled against the consensus finding; no unreconciled contradiction between them.
- What left the guide established before the verdict, and leading the takeaway and page one where
  it is the largest item in the record.
- Within the length budget: six pages target, eight ceiling, appendix excluded.

---

## SCOPE — what this does and does not do

- **Produces a report, not a workbook.** Wiring the current guide into a live model, or scoring a
  single print against consensus on results morning, are separate pieces of work.
- **Scores behaviour, not the stock.** The verdict is a read on how this management team sets and
  delivers guidance. It never issues a rating, a target, or a recommendation.
- **One company at a time.** Peer guidance culture is available as an optional section for
  context, but the unit of analysis is the single name.
- **Most useful** when picking up coverage, ahead of an initiation, before a results preview
  where the guide is the swing factor, or when a new management team issues its first guide.
