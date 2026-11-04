---
name: samaya-trigger-news
description: >-
  "alert me to news on NVDA export controls", "notify me when there's news about Fed rate cuts" —
  sets up a standing Samaya alert on company, industry or macro news, scoped tightly so it stays
  quiet until something relevant lands. For new filings, transcripts or research use
  samaya-trigger-doc-drop; for price levels or moves use samaya-trigger-price-move.
---

# Trigger: News

Watches the news for one specific topic. Notifies when a matching story publishes.

Not a news summary — that's `financial_qa`'s job. This sets up a standing alert:

- "Alert me to any news on Apple's China supply chain."
- "Notify me if there's news of a management change at Boeing, Airbus or Embraer."
- "Ping me on news about GLP-1 drug pricing." (industry)
- "Tell me when there's news about Fed rate decisions." (macro)

## No details yet

Send this verbatim — keep the blank lines and the lists, they carry the formatting — then stop. Nothing else.

```
I'll send you a short write-up whenever news you care about is published. I can watch:

- Company news — one or more companies, on a specific topic (e.g., guidance changes, M&A, management changes, a product, a lawsuit)
- Industry or theme news — e.g., GLP-1 drug pricing, data center power demand
- Macro and policy news — e.g., Fed rate decisions, tariffs, China stimulus

Where the news comes from: MT Newswire, press release wires (Business Wire, PR Newswire and similar), free outlets such as Yahoo Finance and a web search for general market and policy news.

Keep it narrow: a broad alert ("any news on the S&P 500", "AI news") fires many times a day and gets noisy fast. Tell me:

1) the company or companies, if any, and
2) the specific topic or kind of event to watch for.
```

## Given a topic (and maybe companies)

**1. Sort the ask into the right alert.**
- New filings, transcripts, press releases, IR decks or broker research → that's `samaya-trigger-doc-drop`, not this.
- A price level or move → `samaya-trigger-price-move`.
- The user specifically asks for news from Bloomberg, WSJ, FT, NYT, Washington Post, Barron's, MarketWatch, social media or private newsletters → don't set up the alert for that outlet. Say Samaya doesn't cover it, and offer the same topic from the sources Samaya does have. Only raise this when the user names one of these outlets; never volunteer the list.

**Coverage, for answering "do you get X?":**
- Covered: MT Newswire; press releases from Business Wire, PR Newswire and similar wires; free outlets aggregated by the company news feed (AP, Yahoo Finance, Motley Fool, Benzinga, GuruFocus and others); web search for general market and policy news.
- Not covered: Bloomberg, The Wall Street Journal, Financial Times, The New York Times, The Washington Post, Barron's, MarketWatch.
- Any outlet not named above (e.g., Reuters): don't promise it. Say Samaya can't confirm coverage of that outlet, and set up the alert without restricting to it.

**2. Check the scope before calling. Too broad = noisy.** Push back, once, with a narrower version when the ask is any of:
- "Any news" / "everything" on a large company — mega caps get dozens of stories a day. Suggest the two or three event types they actually care about (guidance, M&A, management change, regulatory action, a named product).
- "Any news" across a long list of companies (more than ~5) — one alert per company, each firing on every story.
- A whole sector, index or market ("tech news", "S&P 500 news", "macro news", "AI news") — suggest a specific theme, policy or event.
- Several unrelated topics in one ask — split into one alert per topic, and confirm each is worth a ping.

Phrase it as a trade-off, not a refusal: "That will fire many times a day. Want me to narrow it to X and Y instead?" If they confirm the broad version, set it up and remind them they can pause it on the agents page.

**3. Build the call:**
- `query` — the topic in the user's own words, every condition kept, **no company named in it** (e.g., "News about supply chain disruptions", or "Any news" only when they confirmed they want everything). The company is added per alert.
- `companies` — the companies, all in one list (name and/or ticker; the company, not the product — iPhone news is Apple). Omit for industry or macro news, and for news about several companies together (a deal or dispute between them — put both names in `query`).
- `source_whitelist` — only if the user asked to restrict outlets (e.g., `apnews.com`). Never whitelist an outlet listed as not covered — the alert would never fire; say so instead. Restricting sources also moves the alert off the dedicated company feed onto the hourly web check — mention it.
- One call per distinct topic. Same topic across many companies is one call.

**4. `how_to("alerts")` first, every session** — the setup and batching rules live there.

**5. One `subscribe_to_live_news_agent` call per topic, every company together.** If the tool says it isn't available for the account, tell the user news alerts aren't enabled for them yet and to contact their Samaya team — don't retry.

**6. Confirm what got set up** — one line per company (or one line for a topic-only alert), naming the topic it watches. A company that failed to resolve gets its own line with the reason.

**7. Point them to the portal, always the same link** — the tool's response doesn't return a usable per-alert URL, so don't hunt for one or show session IDs. Close with: "Check out the event-triggered agent(s) you just set up: [click here](https://app.samaya.ai/app/agents)."

**8. Tell them how they'll hear about it:** when matching news publishes, a short write-up lands by email and on the Samaya platform. Company news on US- and Canada-listed stocks comes from a dedicated company news feed; everything else (other listings, industry, macro, or source-restricted alerts) is checked against the open web about once an hour — don't promise faster.

## Rules

- Every company sharing a topic goes in one call. A loop of single-company calls is a defect.
- Never pad `query` down to just a company name or up with topics the user didn't ask for.
- Flag a broad alert before creating it — once, with a concrete narrower option.
- Portal link is always `https://app.samaya.ai/app/agents` — never a per-session or per-subscription URL, and never show a raw session ID or subscription ID to the user.
- A company that can't be resolved is reported, not silently skipped.
- Don't claim coverage of Bloomberg, WSJ, FT, NYT, Washington Post, Barron's, MarketWatch, social media or private newsletters, and don't promise any outlet not on the covered list.

## Before sending

- Topic is specific, or the user confirmed the broad version after the noise warning.
- Filings/transcripts/research asks routed to doc-drop; price asks to price-move.
- `how_to("alerts")` called this session before `subscribe_to_live_news_agent`.
- Every company's outcome (success or error) is named, per topic.
- Portal link (`https://app.samaya.ai/app/agents`) included — no session IDs, no invented links.
- User told: email + Samaya platform when matching news publishes; open-web topics checked about hourly.
