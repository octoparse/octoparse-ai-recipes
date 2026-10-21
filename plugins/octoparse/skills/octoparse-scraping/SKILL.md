---
name: octoparse-scraping
description: Collect web data with Octoparse (templates via MCP, or the Octoparse CLI for custom pages). Use when the user wants to scrape or collect data from Amazon, Google Maps, e-commerce, review, store-listing or other websites, or mentions Octoparse / オクトパス / 八爪鱼.
---

# Collecting web data with Octoparse

Octoparse does the collection (templates, cloud runs, IP rotation and anti-blocking); you do the planning and the analysis. Prefer a **template** whenever one exists: it is the fastest, most reliable path and runs in the Octoparse cloud. Build a **custom task** with the CLI only when no template fits.

## 0. Check the connection

The Octoparse MCP server is `https://mcp.octoparse.com`. If its tools (`search_templates`, `execute_task`, `get_task_status`, `export_data`, `search_tasks`, `start_or_stop_task`) are not available, tell the user to authenticate:

- Claude Code: run `/mcp`, select `octoparse`, and sign in (OAuth).
- Codex: `codex mcp add octoparse --url https://mcp.octoparse.com` then `codex mcp login octoparse`.
- Claude (web/desktop): add Octoparse as a custom connector with the same URL.

Never ask the user to paste an API key into the chat.

## 1. Pick a template

1. Restate the goal as *site + target + fields + volume* (e.g. "Amazon.co.jp reviews for 6 ASINs since 2025-01-01").
2. Call `search_templates` with short keywords (site + data type, e.g. `amazon review`, `google maps store`). Search in English even for Japanese sites; add the country (`japan`, `jp`) if there are many hits.
3. Read the chosen template's **input schema** from the result. Do not guess parameter names: they are template-specific (e.g. `aSIN`, `review_Date_Time`, `google_Maps_Place_Details_Page_URLs`, `number_of_Pages`).
4. Check the template's limits in its description (max inputs per run, reviews per page, whether it is a "Lite" version with capped output). If a Lite template caps output below what the user needs, look for the full/cloud version.

Commonly used templates (always confirm the schema with `search_templates`):

| Goal | Template name | Key inputs |
|---|---|---|
| Amazon.co.jp search results | `amazon-japan-product-scraper` | keyword |
| Amazon.co.jp reviews | `amazon-jp-review-details-scraper` | ASIN list, start date |
| Google Maps store list | `google-maps-store-listing-scraper` | keyword, pages |
| Google Maps reviews | `google-maps-review-scraper-cloud` | place URLs, pages (10 reviews/page) |

## 2. Run it

1. Before a large run, state the expected volume and ask the user to confirm. Free accounts share a monthly template-row quota between MCP and CLI, so start small (one input, one page) when unsure.
2. Call `execute_task` with `templateName`, `parameters` and a descriptive `taskName` (e.g. `voc-amazon-jp-earphones-20261019`).
3. Poll `get_task_status` until it is `completed`. Report `collectedRows`.
4. If the result is 0 rows: re-check parameter names and formats against the schema, then try a single known-good input. Do not loop silently.

## 3. Get the data

- Call `export_data`. Large results are paged: request pages of about 100 rows and concatenate. If the tool returns a download link that you cannot fetch, keep paging through `export_data` instead.
- Save the raw data to a CSV file in the working directory before analysis, and de-duplicate (reviews can repeat across star filters or pages). Report raw and unique counts.
- Remove personal data (reviewer names, profile URLs) before sharing results.

## 4. Hand off to analysis

Data collection is only half the job. After export, analyze the data for the user's goal. For reviews, use the `voc-analysis` skill. Always end with what the data suggests doing next and, if relevant, what to collect next (e.g. competitor ASINs, another region, a weekly re-run).

## Custom pages: Octoparse CLI (advanced)

Use only when no template fits. Requires Node 20+ and `npm i -g @octoparse-ai/octoparse-cli`, then `octoparse auth login`.

- Read `octoparse capabilities --json` first and follow it; do not guess flags.
- Typical flow: `octoparse detect <url> --prepare-agent` → inspect the annotated screenshot → write an agent plan (`octopus.detect.agent-plan.v1`) → `--preview-agent-plan` → `--apply-agent-plan` → `octoparse run --task-file task.json --max-rows 10` → `octoparse data export --format csv`.
- Use **relative** XPath for the loop item (e.g. `//div[@data-component-type='s-search-result']`), never an absolute path.
- Known pitfalls: on Windows PowerShell set `[Console]::OutputEncoding = [Text.Encoding]::UTF8` and write JSON without BOM; `<placeholder>` angle brackets break PowerShell commands; in v0.1.33 `octoparse template view` returns empty `parameters` (use MCP `search_templates` for the schema).
- Sites with strong anti-bot protection (e.g. Amazon) may run locally but return 0 rows in the cloud for a custom task. In that case switch back to the official template, which runs with Octoparse's anti-blocking infrastructure.

## Rules

- Respect each site's terms of service and robots rules; collect only public data; keep volumes reasonable.
- Never print or store API keys or tokens.
- Do not delete or modify the user's existing Octoparse tasks unless explicitly asked.
