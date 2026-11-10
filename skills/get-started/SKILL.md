---
name: get-started
description: >-
  "get started with samaya", "set up samaya", "which samaya skill should I use" — first-run
  setup for the Samaya finance skills: connect the Samaya connector, confirm it answers, and
  pick the right skill for the first task. Use it once after installing, or whenever Samaya
  is not connected or a request does not obviously map to a skill. Not for the research
  itself: once connected, use use-samaya or the named skill.
---

# Get started with Samaya

Every Samaya skill pulls its figures through the Samaya MCP server, so the connector must be
connected before anything else works. Walk the user through these steps in order and stop at
the first one that fails.

## 1. Connect Samaya

The plugin bundles one connector, `samaya` (`https://mcp.samaya.ai/mcp`). The user signs in
with the same credentials they use at `https://app.samaya.ai`.

- If a Samaya tool such as `financial_qa` is available in this conversation, the connector is
  connected: go to step 2.
- If it is not, tell the user where to connect it: in Claude, the plugin's **Connectors** tab
  under **Customize > Plugins**; in ChatGPT, approve the Samaya connection when the plugin asks;
  in Copilot, sign in when prompted on first use. Then ask them to start a new conversation.
- If sign-in fails, the user has no Samaya account or their organization has not enabled
  Samaya: point them at `feedback@samaya.ai`.

## 2. Confirm it answers

Call `financial_qa` with one short question, for example "What was Apple's revenue in its most
recent fiscal year?", and poll `financial_qa_result` until it is done. A reply with citations
means everything works. Tell the user Samaya is connected and show one cited figure. If the
call returns an authorization error, go back to step 1.

## 3. Pick the first task

Suggest three things to try, then run whichever the user picks:

- "Build a results-day variance table for a company I cover" (`samaya-variance-table`).
- "Fact-check the numbers in this deck" with an attached file (`samaya-fact-checker`).
- "Recap the latest earnings call for NVDA" (`samaya-earnings-recap`).

For any other finance request, use `use-samaya`: it finds the matching Samaya workflow,
including the ones the server keeps behind `find_skill`, and runs it. A plain question that
needs no workflow goes straight to `financial_qa`.

## 4. What the user should know

- Every figure Samaya returns carries a citation to a filing, transcript, estimate or research
  note; keep those citations in anything you write.
- Samaya covers public companies, central banks and macro, plus the organization's own
  connected documents. It is not a trading or execution tool.
- The skills are installed on the user's side and do not update on their own except through
  the directory they were installed from; `use-samaya` always reaches the server's current set.
