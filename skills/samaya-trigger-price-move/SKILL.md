---
name: samaya-trigger-price-move
description: >-
  "alert me when X hits $200", "notify me if Y drops 5% today" — sets up a standing Samaya alert on
  a stock crossing a price level or making a relative move. For document alerts use
  samaya-trigger-doc-drop.
---

# Trigger: Price Move

Watches a stock price. Notifies the moment it crosses.

Not a price check — that's `financial_qa`'s job. This sets up a standing alert:

- "Alert me if NVDA crosses $200."
- "Notify me the moment TSLA drops 5% in a day."
- "Ping me on a 2-standard-deviation move vs. yesterday's close."
- "Tell me if either of these two breaks $50, up or down."

## No details yet

Send this verbatim — keep the blank line and the numbered list, they carry the formatting — then stop. Nothing else.

```
I'll send you an analysis the moment a stock hits a threshold you set. The analysis will explain the drivers behind the movement. Tell me:

1) the ticker(s),
2) what should trigger it — crossing an absolute level (e.g., $100), moving by a set dollar amount (e.g., $10), or a relative move (e.g., 2%, or 1 standard deviation) over a rolling day, week or month, or against yesterday's close, and
3) the direction: up, down, or both.
```

## Given a ticker + condition

**1. Resolve every ticker in one batch.** US-listed only. All tickers sharing the same condition go in one `companies` list — never loop.

**2. Pick the rule:**
- A level ("crosses $200") → `rule_type=ABSOLUTE`.
- A move ("drops 5%", "moves 10 points", "a 2-stdev swing") → `rule_type=RELATIVE` — pick `unit` (percent, points, or stdev) and `time_mode` (rolling day/week/month, or vs. yesterday's close). Stdev only works with yesterday's-close mode.

**3. Direction:** UP, DOWN, or BOTH (BOTH creates one alert each way).

**4. Minimums:** 1.0 for percent/points, 0.5 for stdev — below that, Samaya rejects it. Say so up front if the user's ask is under the floor.

**5. `how_to("alerts")` first, every session** — the setup and batching rules live there.

**6. One `subscribe_to_stock_price` call, every ticker together.**

**7. Confirm what got set up** — one line per (ticker, direction) pair. A ticker that failed to resolve gets its own line.

**8. Point them to the portal, always the same link** — the tool's response doesn't return a usable per-alert URL, so don't hunt for one or show session IDs. Close with: "Check out the event-triggered agent(s) you just set up: [click here](https://app.samaya.ai/app/agents)."

**9. Tell them how they'll hear about it:** the moment it triggers, the analysis lands by email and on the Samaya platform.

## Rules

- Every ticker sharing a condition goes in one call, not a loop.
- Prices poll every 2 minutes — don't promise sub-2-minute precision.
- Portal link is always `https://app.samaya.ai/app/agents` — never a per-session or per-subscription URL, and never show a raw session ID or subscription ID to the user.
- A ticker that can't be resolved is reported, not silently skipped.

## Before sending

- Ticker batch, rule type, direction, and (for RELATIVE) unit + time_mode all confirmed before calling.
- `how_to("alerts")` called this session before `subscribe_to_stock_price`.
- Every (ticker, direction) outcome named.
- Portal link (`https://app.samaya.ai/app/agents`) included — no session IDs, no invented links.
- User told: email + Samaya platform, the moment it fires.