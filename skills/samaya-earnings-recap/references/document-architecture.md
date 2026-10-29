# Document architecture — shared by every Samaya written-report skill

The fixed page-one layout and section order for a Samaya report in Word or a comparable
document medium. `references/samaya-conventions.md` carries the rules that apply to every
deliverable (sourcing, citation, desk, authorship); this file is the document-specific layer on
top of it.

## Contents

- DOCUMENT ARCHITECTURE — fixed, and identical in every run
- DOCUMENT VALIDATION GATES

## DOCUMENT ARCHITECTURE — fixed, and identical in every run

The reader is a portfolio manager or a research director who may read only the
first screen and act on it. Build the document in this order, every time:

1. **Masthead** — one line: house label, document type, company, ticker,
   reporting currency, as-of date.
2. **Headline** — one declarative sentence naming the finding. A sentence that
   states the subject rather than the finding ("this report reviews X") is a
   build failure. Write it after the body, from the body.
3. **The takeaway** — one paragraph, specified below. Never longer.
4. **Contents** — the sections that actually ran, one line each, in document
   order, each linked to its heading. Omit entirely where fewer than four
   sections ran.
5. **Body** — the elected sections, in menu order.
6. **Appendix** — everything the reader does not need in order to reach a view:
   sourcing, as-of and coverage lines, derived and unavailable items, the
   not-run list, and any gap statement.
7. **Conclusion** — the five-sentence close, last.

**Nothing that reports an absence appears above the body.** No data retrieved,
no analyst thesis supplied, no consensus available, sections not run, coverage
caveats: all of it sits in the appendix. A document that opens on what it could
not find reads as a failed run whatever follows it. Where an absence is material
to the finding itself, it is carried in the takeaway as part of the finding, in
words — never as an empty field.

**Never render an empty value.** No nulls, no unresolved placeholders, no `n/a`
counts, no dimension label with nothing behind it, no score against an
uncomputed denominator. A row with no content is omitted from the table and
named once in the appendix. Every score printed anywhere states its scale at
first use, and every scale in one document is the same scale.

**The provenance strip is a fixed, short set — six labelled items at most.** Last reported period
and its report date · guidance in force and its date · consensus provider and as-of date ·
evidence or entitlement mode in three words · currency and fiscal year end · anything genuinely
unretrievable. Everything else about how the run was configured — horizon, section counts, depth,
desk order — goes in the appendix. A strip that grows to ten lines has become a preamble, which
is the thing this architecture exists to prevent.

**One block only above the takeaway, and the strip is it.** No standing context block, no
separate evidential-balance block, no run-parameter list, no second summary under another name. A
reader who meets three headed blocks before the answer has been made to work for it. Anything
structural worth stating up front belongs in the headline, which is one sentence and exists for
exactly that; where it will not fit there, it is a body finding, not a preamble.

**A key-numbers strip sits directly under the takeaway.** Six to eight labelled tiles, each a
short label over a single figure — the counts, rates, dates and levels the whole report turns on,
so a reader who reads nothing else leaves with the numbers. Each tile is one figure with a unit,
never a sentence. Where the report has fewer than six figures worth surfacing, use fewer tiles
rather than padding with derived ones.

**Contents, where more than three sections ran**, as a compact two-column list with the page each
section starts on, each entry linked to its heading. The appendix and conclusion appear as one
combined entry at the end.

**A source-class legend as a footer band on page one**, naming the source classes the run drew on
and, separately, any class that was not retrieved and is therefore excluded from scoring. It
tells the reader what the findings rest on in one line without spending a paragraph on it.

**A running footer on every page** — house label, document type, ticker, window, and page number
of total. A page separated from the document must still identify itself.

**Section numbering carries through to sub-references.** Where the body refers back to a finding,
it names it by its section and sub-letter (`2c`, `4b`, `5a`) rather than by page or by
description. A reader tracing an argument should not have to search for what is being referred to.

**Findings that interrupt the flow get their own callout.** Where a paragraph contains the single
most important observation in its section, lift it into a labelled callout rather than leaving it
in the run of prose. One or two per report, never one per section.

**The provenance strip is capped at half a page.** Coverage, scope or sample, entitlement,
comparison basis and source completeness are necessary and they are not the finding. Render them
as labelled single lines — one line each, wrapped, no sub-bullets — immediately below the
headline, and put every further detail (what was not retrievable, figures omitted for conflict,
market-data as-of lines) in the appendix. Page one carries the strip and the takeaway, in that
order, and nothing else. A page of provenance before the reader learns anything is a failed
layout however accurate it is.

## DOCUMENT VALIDATION GATES — added to the common gates

- Page one carries the masthead, headline, provenance strip (six labelled items at most), the
  takeaway, the key-numbers tiles and the contents — and nothing else. No second summary block
  under any name above the takeaway; no structural-context block, no separate evidential-balance
  block, no run-parameter list.
- Key-numbers tiles are single figures with units, not sentences, and were not padded.
- Source-class legend present on page one, naming both what was drawn on and what was not
  retrieved. Running footer on every page.
- Back-references name their section and sub-letter, not a page or a description.
- The evidential balance, where the skill states one, is a clause inside the takeaway, not a
  headed block; run parameters are in the appendix.
- Nothing reporting an absence appears above the body.
