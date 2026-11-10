# Section election, section menu and sub-section index

Moved out of `SKILL.md` to keep it lean; read it at kickoff, before presenting the menu.

## Contents

- SECTION ELECTION
- SECTION MENU
- SUB-SECTION INDEX

## SECTION ELECTION — run the defaults, then say what else exists

Where the invocation resolves a company, **run the default sections
immediately.** Do not hold the run to present a menu.

Print one line above the body — `Default set: <sections>. <n> optional sections
available, listed in the appendix.` — and build. The not-run list goes in the
appendix, never at the top.

Present the menu and wait only where one of these holds:

- the company or the period cannot be resolved from the invocation
- the request is ambiguous between this skill and a named neighbour
- the run is expensive: a window beyond the default, more than one name, or
  Full depth
- the user asks what the skill can do

Where the user names a section or a sub-section, build exactly that and nothing
else. Do not add sections back for completeness, do not append omitted sections,
and do not widen a single-item request into its parent section.

## SECTION MENU

**Default (1–5) — these run without being asked for, and the order is deliberate (see below):**
1. **Guided metrics inventory** — what management actually guides, on what horizon, in whose
   convention, and what they have stopped or started guiding over the window. Built by retrieving
   every results release and trading statement in the window through Samaya, not from recall.
   Renders as three tables (currently guided; added or dropped; format by metric), never prose —
   see `references/sections.md`.
2. **Dual scorecard** — the same rows scored twice: once against the guide in force at
   period-end, once against the initial guide. Both tables always, and the gap between them
   named as the central finding. Every guide is retrieved from the release and the call that
   accompanied it; every outcome from the reported result. See the dual scorecard rule below.
3. **Consensus positioning** — where the Street sat versus the guide at each point, and whether
   consensus or the guide proved the better predictor. Consensus is the vintage at the time,
   retrieved through Samaya from the feed or from a dated note stating where the Street sat.
4. **Revision path** — within each year: initial guide → every reset → final, with the verbatim
   line that moved it and the date, and exactly one chart of the path (see `references/sections.md`).
   The verbatim comes from the transcript, retrieved through Samaya; guidance is routinely phased or
   qualified in question-and-answer rather than in the release, so the call is not optional here.
5. **Credibility verdict** — the culture read, evidenced, drawn only from what the retrieval
   returned and explicit about which events could not be sourced.

**The default order is deliberate and is not to be rearranged.** Tables A and B open the body ahead
of any narrative section and are never pushed behind the revision path; consensus positioning runs
before the revision path, because whether the guide beat the Street is a headline finding and a
reader should not have to reach the back of the report for it.

**Optional (6–18):**
6. Management era comparison (current team vs predecessors)
7. Segment / divisional guidance track record
8. Medium-term and CMD target scorecard (multi-year targets, hit or quietly dropped)
9. Phasing accuracy (1H/2H and quarterly cadence versus stated phasing)
10. Guidance withdrawn, suspended, or reinstated — events and reasons
11. Restatement, perimeter and FX-basis effects log
12. Peer comparison of guidance culture
13. Share price reaction to each guidance event
14. Language shifts at revision points (hedging, confidence markers)
15. Guidance width over time (range narrowing as evidence of visibility)
16. First-revision timing (how early in the year they move)
17. Capital allocation guidance (buyback, capex, dividend, leverage targets)
18. **Consensus accuracy against guidance** — how well the market forecast the company over the
    lookback, alongside how well management guided it: consensus against the guide, consensus
    against delivered, and how consensus responded to revisions. Built only from dated consensus
    actually retrieved. Runs after the scoring sections and before the credibility verdict.

## SUB-SECTION INDEX — every item below is individually selectable

Any single item may be requested on its own. A user who wants only the beat-and-raise history
gets that table and nothing else — no surrounding sections, no padding, no "for context" extras.

**1 Guided metrics inventory** — 1a metrics currently guided · 1b metrics added or dropped over the
window · 1c guidance format by metric (range, point, directional, floor)

**2 Dual scorecard** — 2a Table A, scored against the guide in force · 2b Table B, scored against
the initial guide · 2c the gap between the two tables

**3 Consensus positioning** — 3a consensus at each guidance event · 3b guide versus consensus as
the better predictor · 3c directional bias of the initial guide across the cycle

**4 Revision path** — 4a revision timeline by year · 4b the verbatim line that moved each guide ·
4c beat-and-raise history (the upgrade sequence alone) · 4d cut and downgrade history alone ·
4e unrevised years · 4f the revision-path chart

**5 Credibility verdict** — 5a hit-rate and magnitude statistics · 5b the culture verdict ·
5c read on the guide currently in force

**18 Consensus accuracy against guidance** (optional) — 18a consensus against the guide · 18b
consensus against delivered · 18c response to revisions

Optional sections 6 to 18 are each individually selectable as listed above; section 18's three
components are individually selectable as listed here.
