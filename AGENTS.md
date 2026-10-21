# Agent instructions: Octoparse AI recipes

This repository shows AI agents (Codex, Claude Code, Cursor, etc.) how to **collect web data with Octoparse and analyze it**. Octoparse handles collection (templates, cloud runs, anti-blocking); the agent plans the collection and analyzes the results.

## Setup

Connect the Octoparse MCP server `https://mcp.octoparse.com` (OAuth):

- Codex: `codex mcp add octoparse --url https://mcp.octoparse.com` then `codex mcp login octoparse`
- Claude Code: `claude mcp add --transport http octoparse https://mcp.octoparse.com`, then `/mcp` to sign in
  (or install the plugin: `/plugin marketplace add octoparse/octoparse-ai-recipes` → `/plugin install octoparse@octoparse`)

Never ask the user to paste an API key into the conversation, and never print or commit keys.

## How to work

Follow the two skill files; they are the source of truth:

1. Collection: `plugins/octoparse/skills/octoparse-scraping/SKILL.md`
   - Templates first (`search_templates` → read the input schema → `execute_task` → `get_task_status` → `export_data`).
   - Custom tasks with the Octoparse CLI only when no template fits.
2. Analysis: `plugins/octoparse/skills/voc-analysis/SKILL.md`
   - First-pass counts: `python3 plugins/octoparse/skills/voc-analysis/scripts/analyze_reviews.py <csv> --group <col>`
   - Then read the low-star reviews, classify themes, compare groups, and report findings + what to collect next.

Worked examples with prompts and results are in `examples/`.

## Rules

- Confirm with the user before large runs; start with a small test.
- Collect only public data, respect site terms, remove personal data from outputs.
- Do not delete or modify the user's existing Octoparse tasks unless asked.
