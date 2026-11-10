# Samaya conventions — shared by every Samaya skill

The rules every Samaya deliverable follows, whatever it builds. A skill's `SKILL.md` carries a
short stub for each section and points here; the stub states the non-negotiables, this file is
the full rule. Where a skill's own body says something more specific, the skill wins on that
point and this file covers everything it does not say.

Read this file once, before the first retrieval.

## Contents

- STEP 0 — Samaya connectivity gate
- CONSENSUS — provider-agnostic, declared once, never assumed
- CITATION — mandatory, and self-contained
- TRACEABILITY — everything clicks back, and nothing is cited twice
- ATTENTION CLASSIFICATION — settled, or needs the analyst's eye
- DESK — established, never assumed (with the empty-value and run-the-defaults rules)
- AUTHORSHIP AND HOUSE STYLE — Samaya AI, never the operator
- COMMON VALIDATION GATES

## STEP 0 — SAMAYA CONNECTIVITY GATE (hard requirement, before anything else)

**Do not begin the build until the Samaya MCP is verified live.** Every figure in every Samaya
skill routes through it.

1. **Check the tool list** for `financial_qa` and `financial_qa_result` from the Samaya server.
   Some clients prefix tool names (e.g. `Samaya:financial_qa`), so match on the tool name, not
   the prefix. If absent: **STOP.** Tell the analyst Samaya is not connected in this session and
   ask them to enable it, then wait — claude.ai: Settings > Connectors · Claude Code: `/mcp` or
   the plugin's `.mcp.json` · ChatGPT: Settings > Apps · Codex: `codex mcp` or the plugin's MCP
   server (a managed workspace may need an admin). Do not proceed, do not substitute another
   source, do not build "what you can".
2. **Call Samaya directly as your first action, before anything else** — do not wait for the
   user's phrasing to imply the connector, and do not ask whether they want you to use it. **Fire
   one trivial test query** (e.g. the company's last reported revenue) and confirm a real response
   comes back before starting the build proper. A tool that exists but errors counts as NOT live —
   apply the retry ladder.
3. **Retry ladder on any mid-build failure:** retry same session_id → fresh session → report
   the auth/connection issue to the analyst and pause. **Never silently fall back to web
   search or any other source.**
4. **Non-Samaya sources require explicit analyst approval, per source, before use** — including
   company-compiled consensus from the company's own website. If approved, the citation on
   every figure and the header note must state the true retrieval path (e.g. `Source: web —
   nestle.com/investors, company-compiled, as-of Apr 2026`), never implying it came via Samaya
   or a consensus feed. An unlabelled or mislabelled source is a build failure.

## CONSENSUS — provider-agnostic, declared once, never assumed

Consensus matters too much to this job to be optional, and it is far too
provider-specific to be hardcoded. **This skill is not anchored to any one feed.**
Where consensus is used, the provider is established at kickoff, recorded on every
figure, and never inferred.

**Establish the provider before retrieving any consensus figure**, in this order:

1. **What the analyst declares.** Asked once at kickoff, in the same message as
   everything else: `Consensus source? Visible Alpha / Bloomberg / FactSet /
   company-compiled / a file you supply / none`. Their answer governs the whole run.
2. **What is actually reachable.** Where they express no preference, use what the
   session can reach and say which. Do not present Visible Alpha as the default
   because the skill was written against it — a great many users will not have it.
3. **What the analyst supplies.** A pasted table, an uploaded sheet or a tab in the
   workbook is a first-class source, not a fallback. Attribute it as
   analyst-supplied with its stated as-of date and no link, since there is nothing
   retrievable behind it.
4. **Company-compiled consensus** from the IR page, where the company publishes one.
   Common outside the US and often the only source a smaller name has.
5. **None.** A legitimate answer, and the run proceeds under the no-consensus rule
   below rather than stopping.

**Rules that hold whatever the provider is:**

- **Record the provider on every consensus figure**, with its as-of date and, where
  the feed gives one, the contributor count. A consensus number without its provider
  and vintage is not usable and is not written.
- **Never blend providers in one comparison.** One provider per line, and where two
  are available, name the primary and use it throughout. A variance computed against
  a mean assembled from two feeds is arithmetic nobody can reproduce.
- **Match the definition before calling a gap a gap.** Providers compile differently:
  underlying against reported, pre- against post-IFRS 16, and differing treatment of
  exceptionals and of associates. A divergence produced by a definition mismatch is an
  artefact. Resolve it, or state the mismatch and leave the line unscored.
- **Respect the granularity the provider actually offers.** Some feeds carry
  line-item and driver-level estimates; others carry headline revenue, EBIT and EPS
  only. Where a section needs a granularity the chosen provider does not offer, say
  so on that line and build what the provider supports — never infer a segment or
  driver estimate from a headline one, and never present a single broker's estimate
  as consensus.
- **A vendor number relayed by a third party is not the vendor's feed.** A figure
  labelled as one provider's but retrieved from an aggregator, a news page or a
  broker note is recorded as coming from where it was actually retrieved.

**When there is no consensus at all**, the run completes. The skill:

- builds every section that does not require it, in full;
- leaves consensus cells blank, with the attempt and its date recorded, rather than
  filling them from a stale vintage, a guided range, a single broker, or inference;
- says once, in the appendix, which lines were left blank and why;
- carries the absence into the takeaway only where it changes the finding — a
  guidance comparison that stands on its own does not need the caveat on page one;
- and never treats the absence as a reason to stop, to narrow scope silently, or to
  substitute a source without saying so.

A no-consensus run is a legitimate output and, for most users of this skill, the
common one.

## CITATION — mandatory, and self-contained

Every piece of information retrieved from Samaya is cited in the output, with its provenance link,
on the row or sentence that uses it. This rule stands on its own: it does not depend on any
citation instruction being present elsewhere in the session, and it applies identically whether or
not such an instruction appears.

- Cite at the point of use, not in a footnote block. A figure the reader cannot trace is not usable.
- Use the resolvable link exactly as the retrieval returns it. Never reconstruct, reformat or
  normalise a link into an expected shape — a rebuilt link that does not resolve is worse than an
  opaque one that does.
- Where several figures come from one document, each still carries the link. Density is preferable
  to a reader guessing which source a number came from.
- Content from an uploaded document or supplied by the user is attributed plainly, with no link.
- Where a figure could not be retrieved, the gap is stated. An uncited assertion is a build
  failure, and so is a citation attached to something that was not actually retrieved.

## TRACEABILITY — everything clicks back, and nothing is cited twice

Every figure this skill produces must be traceable to where it came from in one click, and the
cost of that must not be a run that takes twice as long. Both halves matter.

**Notes, never comments.** Excel has two annotation types and only one is right here: the classic
**Note**, never a threaded comment. Threaded comments are a conversation thread — they carry a
reply chain, they render differently across Excel versions and Sheets, and they read as someone
talking rather than as a source record. Notes are the house standard, in every skill, without
exception. Where a host workbook already carries threaded comments, leave the analyst's own
alone and still add new annotation as Notes.

**Every Note carries its Samaya link.** In the form
`https://app.samaya.ai/app/chat/{chatId}?artifactId={artifactId}&referencesVisible=true`, built
from the retrieval's chat and artifact IDs and written exactly as returned — never reconstructed,
reformatted or normalised. A Note reading "per the H1 release" with no link is half a citation:
the reader has to go and find the release themselves, which is the work the skill was meant to
remove. Notes carry the link as plain text so it survives a copy into a browser, and where the
cell can also hold a live hyperlink, it does both.

**Proportionate, not exhaustive.** Sourcing that slows a run to a crawl defeats the purpose, so:

- **Cite the retrieved figure, not every cell downstream of it.** A reported revenue number
  carries its link; the four formulas that divide into it do not. Anyone tracing the margin gets
  there through the revenue cell.
- **One link per retrieval, reused.** Where six figures came from one document in one retrieval,
  that is one link on six cells, not six retrievals. Do not re-query a document you have already
  read in order to generate a fresh link.
- **Do not re-cite within a block.** A table sourced entirely from one release carries the link
  on the block header and on any row that came from somewhere else, rather than on all thirty
  rows.
- **Never fabricate a link to satisfy the rule.** Where a figure was supplied by the analyst, it
  is attributed as analyst-supplied with no link. Where a retrieval returned no usable ID, say so
  on that row rather than attaching a link that will not resolve.

**Internal links, so the reader can jump to what moved.** Where this skill writes prose about a
workbook — a Read block, a change log, a summary — every line naming a model line is a live
internal hyperlink to the cell or block it refers to, so the reader clicks the sentence and lands
on the number. Build them with `=HYPERLINK("#'<Sheet>'!<Cell>", "<label>")`, resolving the target
by finding its row label at runtime rather than by a remembered address. Where a target cannot be
resolved, write the label as plain text rather than a broken link.

## ATTENTION CLASSIFICATION — settled, or needs the analyst's eye

Not everything a skill writes deserves the same scrutiny, and treating it all the same wastes the
analyst's attention on numbers that are simply what the company reported. Classify every line the
skill touches into one of three, and say which in the Read:

- **Settled — reported.** A figure taken from a release, a filing or a statement. There is
  nothing to question: it is what the company said. No fill, link to source, and grouped together
  in the Read so the analyst can skip the group entirely.
- **Needs review — estimate.** A forecast or assumption, where the skill has a view on whether it
  still holds: it sits against guidance, against the analyst's own prior, and against consensus
  where a provider was declared. Carries the **attention fill** and a Note stating in one line why
  it is flagged — guidance moved, the prior no longer follows from its driver, the deviation grew.
- **Needs review — mechanics.** A formula, a link or a structural item worth a second look:
  a hardcode sitting in a row of formulas, a reference that had to be re-pointed, a range that was
  widened, an identity that ties only after a rounding difference. Carries the **attention fill**
  and a Note naming the concern.

**The attention fill is the only fill used, so it cannot be misread.** One fill meaning "look at
this" needs no legend and survives a colour-blind reader and a greyscale print. Do not add a
second colour to distinguish good from bad — direction goes in glyphs and in the Note text, per
the house convention. Where the analyst's workbook already uses fills for its own purpose, follow
the workbook and carry the flag in the Note and the Read instead.

**Flag sparingly.** A workbook where forty cells are filled is a workbook where nothing is
flagged. If more than roughly a tenth of the touched lines want the fill, the Read says so in a
sentence — "the whole forecast block needs revisiting after this guide change" — rather than
colouring the block.

## DESK — established, never assumed

This skill serves sell-side research, buy-side research and sales and trading. The **content does
not change by desk** — the same figures, the same sourcing, the same discipline. What changes is
emphasis and ordering, and only where the skill says so.

Establish the desk from what is already in front of you before asking: how the analyst phrases
the request, whether they refer to their own published research or to brokers', whether a rating
and target exist, what they supply. Where genuinely unclear, ask once, in the same message as any
other kickoff question, never as a second round trip. Where it cannot be established, build in
the neutral order the skill specifies and say in the header which order was used. Do not default
silently to one desk and do not fork the artefact per desk.

**Never render an empty value.** No nulls, no unresolved placeholders, no `n/a` counts, no
orphaned label with nothing behind it, no score against an uncomputed denominator. A row with no
content is omitted and named once — in the sourcing note of a workbook, in the appendix of a
document — never left blank or zeroed. Every score states its scale at first use, and every scale
in one deliverable is the same scale.

**Run the defaults, then say what else exists.** Only the kickoff item the skill marks as blocking
blocks; everything else has a default and the default runs. Where the analyst supplies the subject
and nothing more, resolve the settings, state them in one line, and build. Do not hold the run to
present a menu of options — name in one line what else is available and carry on. In a document
skill this means the default sections run immediately and the rest of the menu is named in one
line; in a workbook skill it means the build starts on the elected sources with the rest stated in
the header.

## AUTHORSHIP AND HOUSE STYLE — Samaya AI, never the operator

**Authorship is Samaya AI, never the operator.** Every artefact this skill
produces is a Samaya deliverable, so no personal name appears anywhere in it:

- **Excel Notes** carry `Samaya AI` as the note author. Excel stamps the author
  from whoever's session created the note, so it must be set explicitly — a note
  reading a staff member's name in a customer's workbook is a defect, and in a
  sample report shipped to a prospect it is worse than a defect.
- **Document properties** — author, company, last modified by, manager — are set
  to `Samaya AI` on every file written, and any inherited creator or company
  value from a host workbook or template is cleared.
- **Footers, mastheads and title blocks** carry `Samaya` and the document type,
  not an individual's name, unless the analyst explicitly asks for their own by-line
  on their own work.
- Where a host workbook already carries a third party's properties (a broker model
  the analyst downloaded), leave their authorship intact on their content and do
  not claim it — set Samaya authorship only on notes and tabs this skill creates.

**Styling is not defined here.** The canonical tokens — Samaya Blue is `#0019FF`
and only `#0019FF`, Inter Variable for everything with JetBrains Mono for
citations and tabular figures, and the colour, type and spacing tokens — live in
the `samaya-brand` skill and its rendered styleguide, and the styleguide wins over
any value restated elsewhere. Read it and apply it rather than reproducing a
partial palette here. Where a token needed for this artefact is missing, flag it
rather than choosing a substitute.

## COMMON VALIDATION GATES — every skill checks these before handing back

Each skill's own VALIDATION GATES list adds to these; none of them replaces one.

- Samaya was called directly as the first action, not conditionally on the user's phrasing, and
  the connectivity gate passed before any figure was written.
- Every retrieved figure carries its provenance link at the point of use, written exactly as the
  retrieval returned it; analyst-supplied figures are attributed as such with no link; no
  fabricated link anywhere.
- Notes used throughout in any workbook, never threaded comments; every Note carries its Samaya
  link as plain text.
- Sourcing is proportionate: the retrieved figure is cited, not every cell downstream; one link
  per retrieval reused rather than re-queried.
- Prose about a workbook carries live internal hyperlinks to the cells it names, resolved by
  label at runtime; unresolvable targets written as plain text, never as broken links.
- Every touched line classified settled / estimate-to-review / mechanics-to-check, and the Read
  states which; the attention fill is the only fill used and is applied sparingly.
- Every consensus figure names its provider and as-of date; one provider per comparison, never
  blended, never assumed to be any one feed.
- No empty value rendered anywhere: a line with nothing behind it is omitted and listed once,
  never left as a blank labelled row, a zero or an `n/a` count.
- Note authors and document properties read `Samaya AI`; no personal name anywhere in the
  artefact; inherited creator and company values cleared. Styling taken from `samaya-brand`, not
  restated locally.
