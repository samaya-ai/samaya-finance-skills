---
name: samaya-trigger-doc-drop
description: >-
  "alert me when X files their 10-K", "notify me on Y's next earnings transcript" — sets up a
  standing Samaya alert for new filings, transcripts, press releases or research. For price alerts
  use samaya-trigger-price-move.
---

# Trigger: Doc Drop

Watches for new documents. Notifies the moment one lands.

Not a search — that's `financial_qa`'s job. This sets up a standing alert:

- "Alert me the next time Tesla files an 8-K."
- "Notify me on Apple's next earnings call transcript."
- "Let me know when any of these three drop a press release."
- "Ping me on new FOMC statements."

## No details yet

One line, then ask for the two things needed. Nothing else.

> "I will send you an analysis when new documents you monitor drop. Documents I support include filings, transcripts, IR presentations, press releases, and MS research. Which company (or companies), and what kind of document should I watch for?"

## Given company + document type

**1. Resolve every company in one batch.** Name or ticker, all in a single `companies` list — never loop calls per company.

**2. Map the ask to a filter:**
- Broad ("any filing", "everything they publish") → `datasource_group` (FILINGS, TRANSCRIPTS, PRESENTATIONS, RESEARCH_REPORTS, PRESS_RELEASES, CENTRAL_BANK_COMMUNICATIONS, NEWS, CORPUS_UPLOADS, THIRD_BRIDGE).
- Specific ("10-K", "earnings call", "press release") → `document_type`.
- Content-level ask on top ("...only if it mentions an acquisition") → `freeform_conditions`. These AND together — stacking more than one or two narrows the alert hard. Say so if the user's piling them on.
- More than one category asked for in one go ("filings, transcripts, and press releases") → one `subscribe_to_document_event` call per category, same company batch in each — `datasource_group` only takes one value per call.

**3. `how_to("alerts")` first, every session** — call order and batching rules live there, not in this skill.

**4. One `subscribe_to_document_event` call per category, every company together within each.**

**5. Confirm what actually got set up** — one line per company per category. A company that failed to resolve gets its own line, not a silent drop.

**6. Point them to the portal, always the same link** — the tool's response doesn't return a usable per-alert URL, so don't hunt for one or show session IDs. Close with: "Check out the event-triggered agent(s) you just set up: [click here](https://app.samaya.ai/app/agents)."

**7. Tell them how they'll hear about it:** when a matching document lands, they get the write-up by email and on the Samaya platform — nothing to check manually.

## Rules

- Every company sharing the same filter goes in one call. A loop of single-company calls is a defect.
- `freeform_conditions` are AND, not OR — flag it when several are stacked.
- Portal link is always `https://app.samaya.ai/app/agents` — never a per-session or per-subscription URL, and never show a raw session ID or subscription ID to the user.
- A company that can't be resolved is reported, not silently skipped.

## Before sending

- Company batch and document filter(s) both confirmed before calling.
- `how_to("alerts")` called this session before `subscribe_to_document_event`.
- Every company's outcome (success or error), per category, is named.
- Portal link (`https://app.samaya.ai/app/agents`) included — no session IDs, no invented links.
- User told: email + Samaya platform, the moment it fires.
