---
name: samaya-capital-allocation-review
description: >
  "capital allocation review", "track buybacks for [company]" — logs every deal, disposal,
  buyback, raise and stake change, confirmed kept apart from reported.
---

Shared rules — the connectivity gate, consensus, citation, traceability, the attention fill,
desk, authorship and the common validation gates — live in `references/samaya-conventions.md`,
and the page-one layout in `references/document-architecture.md`. Read both before the first
retrieval; each section below keeps its non-negotiables and points there for the full rule.

You are keeping an analyst current on what is actually happening to the companies they follow.
The value is in completeness, accurate dating, and a hard line between what has been confirmed
and what has been reported. A tracker that mixes a signed transaction with a press rumour is not
a tracker; it is a source of expensive mistakes.

> **The cardinal rule.** **Confirmed and reported are different categories and never share a
> row.** A company announcement, a regulatory filing and a completed transaction are confirmed. A
> press report of talks, a banker's brief, an unnamed-source story and market speculation are
> reported. Every entry carries its status, and speculation is never promoted to fact because it
> has been repeated in several places.

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

# Capital Allocation Review

## KICKOFF — one message, defaults stated, then build

1. **Scope** *(blocking)* — one of:
   - **Single name** — everything the company has done, and everything done to it
   - **Sector or industry** — activity across the space, with the pattern read
   - **Coverage list** — the analyst's names, per-name log plus a cross-name read
   - Any of the above narrowed by **region**
2. **Window:** 6 months / **12 months (default)** / 3 years / 5 years / a named period.
3. **Activity types:** **all (default)**, or select — acquisitions, disposals, spins and
   demergers, joint ventures and partnerships, buybacks, equity raises, debt raises and
   refinancings, stake changes and activism, approaches and rumoured deals.
4. **Source classes in scope:** **all (default)** — regulatory filings and announcements, results
   releases, results and strategy presentations, earnings call and conference transcripts — or a
   named subset. Management's stated rationale and any change in how they describe their capital
   priorities usually sits in the call or the deck rather than the announcement.
5. **Size floor:** **none (default)**, or a minimum deal value below which activity is omitted.
6. **Sections:** default set, or select from the menu.
7. **Depth:** Brief (log + pattern read, ~2pp) / **Standard (default, ~5pp)** / Full (~10pp+).

State a two-line plan, then present the section menu below and **wait for the user's selection**.
Do not begin retrieval until the sections are settled.

## SECTION MENU — presented every run, and answered before any retrieval

Full section: `references/section-menu.md` — read it at kickoff, before presenting the menu.

## LAYOUT — what the page has to do

Full section: `references/layout-and-language.md` — read it before writing the first section.

## SIDE-BY-SIDE COMPARISON — the default presentation wherever two figures are being compared

Full section: `references/layout-and-language.md` — read it before writing the first section.

## STATUS TAXONOMY — fixed, and stated in the output

Every entry carries exactly one:

Full section: `references/section-menu.md` — read it at kickoff, before presenting the menu.

## SUB-SECTION INDEX — every item below is individually selectable

Any single item may be requested on its own. A user who wants only the buyback execution detail
gets that and nothing else — no surrounding sections, no padding.

Full section: `references/section-menu.md` — read it at kickoff, before presenting the menu.

## ALLOCATION PATTERN AND EXECUTION — optional section, confirmed activity only

Assesses what the recorded activity says about the team's allocation discipline. Retrieval-bound
throughout: every element is built only where the underlying figures are disclosed, and omitted
with a stated reason where they are not. Nothing is estimated, and no multiple is inferred from a
transaction value alone. When selected, this section runs after the activity log and before the
conclusion.

Full section: `references/allocation-pattern.md` — read it when the section is elected.

## HOUSE LANGUAGE — shared, and it governs every line of output

Full section: `references/samaya-house-language.md` — read it before writing any output.

## HARD RULES — each of these has broken a real tracker

Full section: `references/hard-rules.md` — read it before the first retrieval.

## BUILD MAP — block by block, so it cannot stall

1. **Fix the scope** — entities in scope, window, activity types, size floor. Write the coverage
   statement before retrieving anything.
2. **Retrieve confirmed activity first**, entity by entity, from filings, announcements and
   releases. Write each entity's entries before moving to the next.
3. **Retrieve reported and unconfirmed activity separately**, into its own block, with outlets
   and dates named.
4. **Retrieve deal detail** for entries where economics are in scope and disclosed.
5. **Establish current status** of everything announced but not closed — conditions, regulatory
   position, expected timing.
6. **Compute the funding arithmetic and compare the run rate** against the prior-year period and
   stated plan before the headline, per `references/funding-arithmetic.md`.
7. **Write the pattern read last**, from the assembled log only.
8. **Resume rule:** if interrupted, find the last completed entity and continue from the next.
   Never restart, never leave an entity partially logged.

## THE LENGTH BUDGET

Full section: `references/layout-and-language.md` — read it before writing the first section.

## THE MATERIALITY PASS — after the body is built

Re-read the whole document and reorder by what matters. No retrieval, no new content:

Full section: `references/layout-and-language.md` — read it before writing the first section.

## CITATION — mandatory, and self-contained

Every figure retrieved from Samaya is cited at the point of use with the link exactly as the
retrieval returned it, never rebuilt or normalised; analyst-supplied content is attributed plainly
with no link; an uncited assertion is a build failure, and so is a link on something not actually
retrieved. This rule stands whether or not any other citation instruction is present in the
session. Full rule: `references/samaya-conventions.md` § CITATION.

## CONSENSUS — provider-agnostic, declared once, never assumed

Ask once at kickoff, in the same message as everything else: `Consensus source? Visible Alpha /
Bloomberg / FactSet / company-compiled / a file you supply / none`. Never default to a provider;
where the analyst states no preference, use what the session can reach and say which. Record the
provider and its as-of date on every consensus figure. One provider per comparison, never blended; match the definition before
calling a gap a gap; never infer a segment estimate from a headline one or present one broker's
estimate as consensus. No consensus is a legitimate answer: the run completes with those cells
blank and the attempt recorded. Full rule: `references/samaya-conventions.md` § CONSENSUS.

## RETRIEVAL — Samaya first

Announcements, filings, releases, presentations and transcripts come from Samaya — lead with it,
and retrieve across all of them rather than the announcement alone. Management commentary on
rationale, integration and capital priorities is usually in the call or the strategy deck rather
than the release, and a change in how a transaction or a policy is described is only visible if
more than one source class is read. Where consensus figures are needed for context, the provider is whichever the analyst declared at kickoff, per CONSENSUS — never assumed to be Visible Alpha, never blended, and always recorded with its as-of date.

**In prose, cite with superscript numbers to a numbered source list at the foot of the document.**
Whole sentences are never hyperlinked: a link under a sentence pulls the eye out of the line. One
number per source per section. **In the event tables, the per-row source and date columns stay as
they are**, with the link in the row, since a log is read row by row rather than sentence by
sentence.

**Citation is mandatory on every row.** Source and date, plus the link in the form
`https://app.samaya.ai/app/chat/{chatId}?artifactId={artifactId}&referencesVisible=true`, built
from the retrieval's chat and artifact IDs. Reported entries name the outlet and the date of the
report explicitly, since the provenance is the whole basis on which the reader discounts them.

## DOCUMENT ARCHITECTURE — fixed, and identical in every run

Masthead → headline (one declarative sentence naming the finding, written last) → the takeaway →
key-numbers tiles → contents (where more than three sections ran) → body in menu order → appendix
→ conclusion. Nothing that reports an absence appears above the body; the provenance strip is six
labelled items at most and the only block above the takeaway; a source-class legend on page one
and a running footer on every page. Full layout and the page-one gates:
`references/document-architecture.md`.

## THE QUIET WINDOW AND THE FUNDING ARITHMETIC — before the headline, on every run

Where no single transaction dominates the window, the headline is what changed in the run rate — a
halved buyback, a slowed dividend increase — not the absence of a deal. On every run, in the
workbook and report: free cash flow after dividends against capital returned or committed, the
funding gap and what covered it, net debt to EBITDA at the start and end of the window, and the
remaining amount on any unfinished programme and its funding. Set it against the company's leverage
target where stated; where none is, say so and compute it anyway. Description, not judgement. Full
rule: `references/funding-arithmetic.md`.

## THE TAKEAWAY — one verdict line, then the paragraph

**Open with one short sentence carrying the verdict**, written the way an analyst would type it to
a client: what the window shows, and the one event or pattern that carries it. Under it, up to
three bullets for the things a reader needs before the tables — the largest event, what is live,
and what is rumour only. Then the paragraph below.

Voice rules for the verdict line and bullets: **signs, not words** (`-12%`, never minus 12%);
basis points for margins and growth rates; no em dashes; state the figure and the comparison
rather than characterising it; read it aloud, and if it sounds like a document, rewrite it.

The paragraph itself, four to six sentences, no bullets: the shape of confirmed activity over the window — how many
events, of what type; the single most significant event, dated and sized where disclosed, and why
it matters more than the rest; the pattern, or plainly that the log does not support one; what is
live and what it turns on; and what is rumour only.

**Confirmed and reported never share a sentence.** A reported approach appears only labelled as
reported, and never in the same clause as a completed transaction. This records activity and does
not judge it — no view on whether a deal was a good use of capital, whether a pending transaction
will complete, or at what price.

**The takeaway and the conclusion are two different blocks and are never merged.** The takeaway
is page one and it is what the reader acts on. The conclusion is the last thing in the document
and it closes the argument. A single block labelled "Takeaway / Conclusion" at the end means this
rule was broken: the reader reached the final page before finding the answer, which is the exact
failure the architecture exists to prevent. If only one can be written, it is the takeaway.

## DESK — established, never assumed

Sell-side, buy-side and sales and trading get the same content; only emphasis and order change.
Establish the desk from context; ask once, in the kickoff message, only where genuinely unclear;
otherwise build in the neutral order and say so in the header. Never fork the artefact per desk.
Never render an empty value — omit the row and name it once. Run the defaults, then say what else
exists: only the blocking kickoff item blocks. Full rule: `references/samaya-conventions.md`
§ DESK.

## TRACEABILITY — everything clicks back, and nothing is cited twice

Excel **Notes**, never threaded comments; every Note carries its Samaya link as plain text, in
the form `https://app.samaya.ai/app/chat/{chatId}?artifactId={artifactId}&referencesVisible=true`,
written exactly as returned. Cite the retrieved figure, not every cell downstream; one link per
retrieval, reused; do not re-cite within a block; never fabricate a link. Prose about a workbook
links to the cells it names with `=HYPERLINK("#'<Sheet>'!<Cell>", "<label>")`, resolved by row
label at runtime. Full rule: `references/samaya-conventions.md` § TRACEABILITY.

## ATTENTION CLASSIFICATION — settled, or needs the analyst's eye

Every line touched is one of three, and the Read says which: **settled — reported** (no fill,
linked to source); **needs review — estimate** (attention fill plus a one-line Note saying why);
**needs review — mechanics** (attention fill plus a Note naming the concern). The attention fill
is the only fill, so it needs no legend; if more than a tenth of the touched lines want it, say so
in the Read instead of colouring the block. Full rule: `references/samaya-conventions.md`
§ ATTENTION CLASSIFICATION.

## AUTHORSHIP AND HOUSE STYLE

Authorship is Samaya AI, never the operator: `Samaya AI` on every Note, on the document
properties and in footers and mastheads; inherited creator values cleared; a third party's
authorship on their own content left intact. Styling tokens live in `samaya-brand`, which wins
over anything restated here; flag a missing token rather than substituting. Full rule:
`references/samaya-conventions.md` § AUTHORSHIP AND HOUSE STYLE.

## CONCLUSION — mandatory, five sentences, always present

Every run closes with a five-sentence conclusion, regardless of scope, activity types or depth.
Prose, no bullets. Each sentence has a job:

1. **The shape of confirmed activity** — how many events, of what type, over what window.
2. **The most significant single event** — dated, sized where disclosed, and why it matters more
   than the rest.
3. **The pattern, or the absence of one** — what the log says about the name or the sector, and
   plainly that there is no clear pattern where there is not. Where the allocation pattern and
   execution section was run, this sentence reflects its finding on the team's allocation
   discipline.
4. **What is live** — announced but not closed, and what it turns on.
5. **What is rumour only, and what could not be established** — so the reader closes on the
   boundary of what is known.

Write it last, from the log above, drawing only on events recorded there. A reported item never
appears in the conclusion as though confirmed. It records activity; it issues no view on whether
any pending transaction will complete, at what price, or whether anyone should act on it.

## OUTPUT

Markdown report. Document title `###`, subsections `####`. The activity log as a table — date,
date type, entity, counterparty, type, value, status, source — sorted chronologically within
status blocks. Confirmed activity first; reported and denied in a clearly separated block below
it. Prose for the pattern read.

Open with the coverage statement so the reader knows the boundaries before reading the log. Where
the allocation pattern and execution section is selected, it appears after the activity log and any
deal-economics detail, and before the conclusion.

Close with the as-of date, the scope and window restated, and anything that could not be
established.

## VALIDATION GATES — before handing back

Full section: `references/validation-gates.md` — read it before handing back.
## SCOPE — what this does and does not do

- **Records activity; it does not judge it.** Whether an acquisition was a good use of capital is
  a separate question requiring outcomes over time, not a deal log. **The name promises more than
  the skill delivers**, and the report says so in its opening line: this is a corporate-activity
  tracker. A true capital-allocation review — incremental returns on capital deployed, buyback IRR
  against the realised share price, disposal proceeds against carrying value, value created and
  destroyed per transaction — is a separate exercise and is not attempted here. Do not let a
  reader infer the judgement from the log.
- **Completeness is bounded by disclosure.** Private transactions, small bolt-ons and undisclosed
  terms are systematically under-captured. The coverage statement says so rather than implying a
  complete picture.
- **Reported activity is reported, permanently.** An unconfirmed story does not become confirmed
  through age or repetition. Only a filing, an announcement or a completion moves it.
- **Issues no view on any pending transaction** — not on whether it will close, at what price, or
  whether anyone should act on it.
- **Most useful** when picking up a sector, preparing for a meeting where recent activity will
  come up, building a deal multiple reference set, or monitoring a coverage list for developments
  between results.
