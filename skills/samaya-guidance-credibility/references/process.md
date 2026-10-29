# Kickoff, retrieval and the build map

Moved out of `SKILL.md` to keep it lean; read the kickoff block at kickoff, and retrieval and the
build map before the first retrieval.

## Contents

- KICKOFF
- RETRIEVAL
- BUILD MAP

## KICKOFF — one message, defaults stated, then build

Ask once, as a single block. Do not interrogate turn by turn.

1. **Company / ticker** *(blocking)*
2. **Lookback:** last print / 1yr / **3yr (default)** / 5yr / 10yr / since IPO. If the requested
   window pre-dates the current reporting basis or the listing, say so and score what exists.
3. **Guidance horizons in scope:** quarterly / half-year / **full-year (default)** / medium-term
   and CMD targets / all.
4. **Sections:** default set, or select from the menu.
5. **Depth:** Brief (both scorecards + conclusion, ~2pp) / **Standard (default, ~5pp)** /
   Full (~10pp+). Depth is binding: at Standard, prose sections are tightened to hold the
   length rather than allowed to run. Both scorecard tables and the conclusion are exempt and
   always appear in full.

Only item 1 blocks. Everything else has a default and the default runs — see the section election
rule. Where the analyst supplies nothing but a company name, state the resolved settings in one line
and build.

## RETRIEVAL — Samaya first

Samaya covers filings, releases, transcripts, presentations and consensus — lead with it. Guidance
verbatim comes from the release and the call Q&A. Consensus follows the ranking: the provider is
whichever the analyst declared at kickoff, per CONSENSUS — never assumed to be Visible Alpha, never
blended, and always recorded with its as-of date.

**Citation is mandatory on every scored row — this gate fails more often than any other under
length pressure, and a scorecard without links is not auditable.** Document short-names alone
("FY21 call") are not sufficient; each row needs the resolvable link. If links cannot be constructed
for a run, say so explicitly at the top of the report rather than shipping bare references as though
they were sourced.

Each scored row's source line reads `Samaya — [document] ([date])` plus the link in the form
`https://app.samaya.ai/app/chat/{chatId}?artifactId={artifactId}&referencesVisible=true`, built from
the retrieval's chat and artifact IDs. A source line without a link is incomplete. Rows from an
uploaded document or the analyst are attributed plainly, no link.

## BUILD MAP — block by block, so it cannot stall

1. **Establish the spine** — reporting calendar, current management and the tenure map, any
   restatements or perimeter events in the window. Write it before pulling anything else.
2. **Retrieve the guidance history through Samaya, year by year, one compound query per year** —
   initial guide, every revision, final position. This is a retrieval task before it is an
   analytical one: the record has to be pulled from the primary documents rather than reconstructed,
   and a year that cannot be retrieved is reported as unretrieved. Source from the release *and* the
   call: management routinely phases or qualifies guidance in Q&A rather than the release. Write each
   year to the report before moving to the next.
3. **Retrieve delivered actuals** on the matched basis, per metric per period.
4. **Retrieve dated consensus** at each guidance event where available, from the provider elected at
   kickoff.
5. **Score** every row against the taxonomy, and establish what left the guide — the targets,
   frames and metrics that dropped out of the record and so score in neither table.
6. **Reconcile the verdict against the consensus finding.** Before writing the verdict, read the
   consensus positioning finding back: where the guide predicted the outcome better than the Street
   did, the verdict must say so, and an unreconciled contradiction between the two is a build
   failure, not a nuance.
7. **Write the verdict last**, from the assembled evidence only.
8. **Resume rule:** if interrupted, find the last completed year and continue from the next. Never
   restart, never leave a half-scored year.
