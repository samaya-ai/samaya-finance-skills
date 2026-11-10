---
name: use-samaya
description: >-
  "use samaya", "ask samaya", "samaya skill" — the entry point to Samaya's finance research
  workflows: build or update a model, variance table or earnings recap, fact-check or reconcile
  figures, track guidance, risks or KPIs, break down a deal, or run any multi-step analysis of
  companies, sectors or a coverage list. Finds the matching Samaya skill on the server and
  follows it.
---

# Use Samaya

Samaya keeps most of its finance skills on the Samaya server. This skill finds the right one for
the request and runs it.

1. Call Samaya's `find_skill` with the user's request exactly as they wrote it. Add only facts
   from the conversation that the request leaves out, such as an attached file or the company a
   follow-up refers to. Do not add a format, length or scope the user did not ask for. If the
   user names a Samaya skill, keep the name in the request.
2. `find_skill` returns `skills`: every Samaya skill that helps with this task, best first.
   - A skill with `visible: true` is meant to be installed next to this skill and carries no
     `instructions`: tell the user which skill fits and run that installed skill. If it is not
     installed, tell the user to install it, then answer with `financial_qa` for now, following
     the `companions` rules.
   - Every other skill comes with its full `instructions`. Follow the instructions of each, as
     if it were installed, and follow every rule in `companions`.
   - If a skill is not visible and its `instructions` are empty (Samaya could not choose), pick
     the skills that fit and load each with `read_skill_file(<name>, "SKILL.md")`.
3. This copy of `use-samaya` ships without the templates and scripts (paths under `assets/` and
   `scripts/`) that some Samaya skills use. When the instructions say to copy, open or run one,
   do that step yourself with the tools you have, or skip it and tell the user what was left out.
   Fetch reference notes (paths under `references/`) with `read_skill_file(skill, path)`.
4. If `skills` is empty, no Samaya skill applies: answer the user directly with `financial_qa`,
   following the `companions` rules.
