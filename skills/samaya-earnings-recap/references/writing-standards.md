# Headings and language, the length budget, retrieval completeness and the materiality pass

Moved out of `SKILL.md` to keep it lean; read it before writing the first section.

## Contents

- HEADINGS AND LANGUAGE
- THE LENGTH BUDGET
- RETRIEVAL COMPLETENESS
- THE MATERIALITY PASS

## HEADINGS AND LANGUAGE — written the way an analyst writes, not the way a model writes

**Every heading says what it is about in ordinary English.** A reader scanning the contents
should be able to tell what is in a section without opening it. Two failures recur and both are
banned:

- **Headings that are not idiomatic.** "What the call changed" is not something anyone says;
  "What changed on the call" is. Read every heading aloud before it ships — if it would sound odd
  spoken to a client, rewrite it.
- **Headings that name a topic without its subject or its metric.** "H2 step-up" leaves the
  reader asking step-up in what — organic growth, cost, margin. "Credibility of the diagnosis"
  leaves them asking which diagnosis. "The €100m question" tells them nothing at all. The
  standard to match is a heading like "Emerging markets and Eastern Europe": subject named,
  scope clear. Write **"H2 margin step-up the guide requires"**, **"Whether the NIVEA
  self-inflicted diagnosis is right"**, **"Whether the €100m repeats in 2027"** — the subject,
  the metric and the question, in a phrase.

**The voice is the analyst's, not the document's.** Short sentences. The point first. No
throat-clearing, no restating the question before answering it, no announcing what the section
will do before doing it. Where something is uncertain, say so in the way an analyst would — the
hedge belongs in the claim, not in a disclaimer around it. Avoid constructions that read as
generated: stacked appositives, "it is worth noting", symmetrical three-part lists, and any
sentence whose only work is transition. A paragraph that would not survive being pasted into a
chat window to a client does not belong in the report.

**Never address the reader, and never refer to one.** No "what the reader needs to know", no
"four things a listener knows now", no "you will see below". Analysts do not write that way, and
it reads as a document describing itself. State the thing.

**No glossary, and no defining ordinary terms.** A line explaining that organic growth strips out
currency, that sell-in is what ships to retailers, or that EBIT excluding special factors is
operating profit before one-offs is written for someone who is not the audience, and it costs the
space the finding needed. Where a term genuinely is company-specific or newly coined by
management, gloss it in the clause where it appears — never as a block of definitions at the top
of a section.

**Numbers belong in cells, not in sentences.** A paragraph carrying more than three figures is a
table that has not been built yet, and this holds on page one as much as in the body.

**Implications are part of the job, everywhere.** Where the evidence supports a read that
management did not state — an implied margin, an unquantified cost, a share position conceded,
something the market is unlikely to take well — state it and label it as implication. This is not
a feature of one sector, one company or one geography; it applies to every run. What it never
does is become a recommendation: it says what the evidence implies, not what to do about it.

## THE LENGTH BUDGET — a hard constraint

**Six pages, target and ceiling.** The template is the document. Anything that does not fit is
cut rather than appended, and anything elected beyond the default set displaces something. A debrief that runs to
fourteen pages has failed regardless of what is in it: it will be skimmed, the findings that
justified the work will be missed, and the reader will not come back. Comprehensiveness is not a
quality of this report.

- **Page one is the four blocks in the page-one specification and nothing else**, on one page.
  Where it overruns, cut a block down; never spill onto a second page. The event line — date,
  format, who spoke — is at most two lines, not a block.
- **Page two carries the surprises in full**, with the verbatim on both sides. Page one and page
  two are the report; the rest is support, and anyone who stops after page one has the view.
- **The close is stated up front, not held back.** What the reader would take away after fourteen
  pages belongs in the takeaway on page one. The conclusion at the end restates it as a close,
  and where it would say something the takeaway did not, the takeaway is wrong.
- **Anything a reader does not need in order to reach a view goes in the appendix** — method,
  transcript basis, coverage, comparison basis, source completeness, the not-run list, the full
  line-item table. None of it appears before the body. **Transcript quality in particular is
  appendix material**: which rendering was used, and which passages a speech-to-text version
  garbled, are housekeeping. A reader who meets a paragraph about mis-transcribed brand names
  before they meet the finding has been given the wrong thing first.
- **Adding costs.** Electing an optional section does not lengthen the report; it displaces
  something. Where a run cannot fit its elected sections in the ceiling, say so and ask which to
  drop rather than exceeding it.
- **Write as the analyst would write to a client who trusts them**, which is closer to a morning
  email than to a corporate document: short sentences, the point first, no throat-clearing, no
  restating the question before answering it. A paragraph that would not survive being pasted
  into a chat window does not belong here.

## RETRIEVAL COMPLETENESS — before writing "not retrievable"

**A blank in a headline comparison is a retrieval failure before it is a disclosure gap.** Where a
figure the reader expects — consensus on a headline line, a reporting date, a segment rate — does
not come back on the first attempt, exhaust the other routes before recording it as unavailable:
the consensus feed, third-party research tabulations that quote the figure, the company's own
materials, and the analyst's own file where they have supplied one. Only after those does the
line read as not retrievable, and then it says which routes were tried.

Where a figure is genuinely unavailable, it sits in the table with the gap marked and the reason
in the appendix — never as a blank cell, and never as a paragraph of explanation on page one.

## THE MATERIALITY PASS — after the body is built, before anything is handed back

**Re-read the assembled document end to end and reorder it by what actually matters.** The build
order is the order that was convenient to construct; it is rarely the order worth reading. This
pass does no retrieval, opens no source and adds no content — it only promotes, converts and
cuts:

1. **Promote.** Identify the two or three most material findings in the whole document, wherever
   they ended up, and make sure they are on page one. A finding that survives to the takeaway
   from page eight is the pass working.
2. **Convert.** Any paragraph carrying a comparison, a sequence or more than three figures
   becomes a table. Any single most important observation in a section becomes a callout.
3. **Demote.** Anything reporting method, coverage or absence moves to the appendix.
4. **Cut.** Any sentence that restates a table, any section that survived on completeness rather
   than content, any hedge that adds no information.
5. **Rewrite the title last**, from what now sits at the top. One short declarative sentence
   naming the finding, with a single line under it that elaborates. A title stating a
   circumstance of the event rather than a finding about the business — that the numbers were
   already public, that the call came two days later — has described the setup and not the news,
   and is rewritten. A title running to three lines is cut.
6. **Check page one against its specification**: one page, the bold line not repeated below, the
   what-changed and key-numbers tables both present, no prose above the key-numbers table, the
   takeaway at three sentences and reading as a message.
7. **Read every heading aloud.** Any that is not idiomatic English, or that names a topic without
   its subject and metric, is rewritten per the headings rule above.

The test at the end of the pass: **if the reader stopped after page two, would they have the
finding?** Where the answer is no, the pass is not finished.
