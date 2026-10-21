# Octoparse AI Recipes

**Collect web data with Octoparse, analyze it with your AI agent.**
Works with Claude Code, Claude, Codex and any MCP client.

[日本語](README.ja.md)

Octoparse runs the collection — ready-made templates for Amazon, Google Maps and many other sites, cloud execution and anti-blocking. Your agent decides what to collect, runs the template through MCP, and turns the data into findings.

```
You: "Collect reviews for these 6 earbuds since January and find what the low-rated ones get wrong."
 → Agent picks the Amazon review template → Octoparse collects 1,023 reviews in the cloud
 → Agent classifies complaints → "17% of low-star reviews: one earbud stops charging (competitors: 4%)"
```

## Install

### Claude Code (plugin: MCP server + skills)

```
/plugin marketplace add octoparse/octoparse-ai-recipes
/plugin install octoparse@octoparse
```

Then run `/mcp`, select `octoparse` and sign in with your Octoparse account.

### Codex

```
codex mcp add octoparse --url https://mcp.octoparse.com
codex mcp login octoparse
```

Clone this repo to use the skills and `AGENTS.md`, or copy `plugins/octoparse/skills/` into your own project.

### Claude (web / desktop)

Add a custom connector with the URL `https://mcp.octoparse.com`. To use the skills, zip a folder under `plugins/octoparse/skills/` and upload it in Settings → Skills.

## What's inside

| Path | What it is |
|---|---|
| `plugins/octoparse/.mcp.json` | Octoparse MCP server (`https://mcp.octoparse.com`) |
| `plugins/octoparse/skills/octoparse-scraping/` | How to pick and run templates, export data, and fall back to the Octoparse CLI for custom pages |
| `plugins/octoparse/skills/voc-analysis/` | Review (VOC) analysis workflow + `analyze_reviews.py` for first-pass counts |
| `examples/` | Worked examples: Amazon review VOC, Google Maps store-by-store VOC |
| `AGENTS.md` / `CLAUDE.md` | Instructions for agents working in this repo |

## Try it

After installing, ask your agent:

- "Find the Amazon.co.jp review template and collect reviews for ASIN XXXXX since 2025-01-01, then summarize the top complaints."
- "Collect the Google Maps store list for '<chain> Shibuya', pick the 2 best and 2 worst rated, collect 80 reviews each and compare."
- "Every Monday, collect new reviews for my product and two competitors and tell me which complaints increased."

## Requirements

- An Octoparse account (free plan available; template runs via MCP and CLI share a monthly row quota on the free plan).
- For custom pages: Node 20+ and `npm i -g @octoparse-ai/octoparse-cli`.

## Links

- Octoparse MCP docs: https://www.octoparse.com/docs?utm_source=github&utm_medium=referral&utm_campaign=ai-recipes
- Templates: https://www.octoparse.com/template?utm_source=github&utm_medium=referral&utm_campaign=ai-recipes

Collect only public data and follow each website's terms of use.

## License

MIT
