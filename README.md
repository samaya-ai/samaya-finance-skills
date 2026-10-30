# Samaya Finance Skills

Finance research workflows for analysts and portfolio managers, powered by
[Samaya](https://samaya.ai). Each skill walks the assistant through one job an analyst does
often, pulls every figure through the Samaya MCP server, and writes the result into Excel, Word,
PowerPoint or HTML with a citation back to the filing, transcript, estimate or research note it
came from.

The plugin needs a Samaya account. Install it, connect the Samaya connector when asked, and sign
in with the same credentials you use at [app.samaya.ai](https://app.samaya.ai).

## What is included

Eighteen workflow skills, `use-samaya`, the entry point that matches a request to the right
Samaya workflow, including the chat-only ones the server keeps behind `find_skill`, and
`get-started`, a first-run check that the connector is connected.

| Skill | Ask for it when you want |
| - | - |
| `get-started` | "get started with samaya": connect the connector, confirm it answers, pick a first task |
| `use-samaya` | "use samaya", "ask samaya": any Samaya workflow, routed to the right skill |
| `samaya-financial-model-build` | A full multi-sheet model from filings, with drivers and a DCF |
| `samaya-model-update` | Your existing model rolled forward for a new period, overrides intact |
| `samaya-variance-table` | A results-day print sheet: consensus, guidance and your numbers side by side |
| `samaya-earnings-recap` | The biggest surprises on a call against the release and the prior call |
| `samaya-guidance-credibility` | How management's guidance compared with what they delivered |
| `samaya-kpi-history` | The full primary-sourced history of one company-reported KPI |
| `samaya-risk-tracker` | Disclosed risks in the latest filing, with changes against the prior one |
| `samaya-revenue-cost-drivers` | A driver tree of revenue and cost segments, rendered as a graph |
| `samaya-end-market-exposure` | End markets, geographies, suppliers and competitors for a company or sector |
| `samaya-capital-allocation-review` | Every deal, disposal, buyback, raise and stake change, confirmed apart from reported |
| `samaya-ma-deal-breakdown` | One deal or a set of deals: multiples, price bridge, sources and uses |
| `samaya-correlation-analysis` | Which stocks in a list move together, and on what |
| `samaya-annotated-price-performance` | An interactive price and volume chart with every big move explained |
| `samaya-historical-pattern` | Precedents for a situation, rated for how close they are |
| `samaya-fact-checker` | Every figure in a deck, workbook or document verified against its source |
| `samaya-reconciliation` | Why two figures disagree, a bridge between them, and which to use |
| `samaya-trigger-doc-drop` | A standing alert for new filings, transcripts, releases or research |
| `samaya-trigger-price-move` | A standing alert on a price level or a relative move |

## Install

- **Claude** (claude.ai, the desktop app, Cowork and Claude Code): add the plugin from the
  directory under **Customize > Plugins > Discover**. In Claude Code you can also run
  `/plugin marketplace add samaya-ai/samaya-finance-skills` and then
  `/plugin install samaya-finance-skills@samaya`.
- **ChatGPT and Codex**: add the plugin from the plugin directory.
- **Microsoft 365 Copilot**: add **Samaya** from the store.
- **Any of them, by hand**: download one skill or the whole plugin from the Skills page at
  [app.samaya.ai/app/skills](https://app.samaya.ai/app/skills) and upload the zip.

## What the plugin runs and sends

- Every figure comes from the Samaya MCP server at `https://mcp.samaya.ai/mcp` over HTTPS with
  OAuth sign-in. Nothing else is contacted, and the plugin stores nothing of its own.
- The skills are Markdown instructions. Five of them bundle small Python scripts that run on
  your machine against files you give them: they add citation comments to Excel, Word, PDF and
  PowerPoint files (`openpyxl`, `pypdf`, `python-pptx`, `pdfplumber`), build workbooks, and
  render charts and reports to HTML. The scripts make no network calls; the rendered chart page
  loads its fonts from Google Fonts when opened in a browser.
- Citations in generated files link to `app.samaya.ai`, where the source document opens.

## Support

Questions and feedback: [feedback@samaya.ai](mailto:feedback@samaya.ai).
Privacy policy: [samaya.ai/privacy](https://samaya.ai/privacy).

## License

[PolyForm Shield 1.0.0](https://polyformproject.org/licenses/shield/1.0.0): use and adapt the
skills freely, except to build a product that competes with Samaya. See [LICENSE](LICENSE).
