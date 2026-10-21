# Octoparse plugin

Collect web data with Octoparse and analyze it with Claude. This plugin connects the Octoparse MCP server (`https://mcp.octoparse.com`) and adds two skills:

- **octoparse-scraping** — pick an Octoparse template (Amazon, Google Maps and many other sites), run it in the Octoparse cloud, export the data, and fall back to the Octoparse CLI for pages without a template.
- **voc-analysis** — analyze collected reviews: complaint themes, low-star drivers, competitor and store comparisons, weekly change reports. Includes `analyze_reviews.py` for first-pass counts.

## Setup

1. Install: `/plugin marketplace add octoparse/octoparse-ai-recipes` then `/plugin install octoparse@octoparse`.
2. Run `/mcp`, select `octoparse` and sign in with your Octoparse account (a free plan is available).
3. Ask, for example: "Collect Amazon.co.jp reviews for ASIN XXXXX since 2025-01-01 and summarize the top complaints."

See the repository README and `examples/` for full walkthroughs.

- Privacy policy: https://www.octoparse.com/privacy-policy
- Terms: https://www.octoparse.com/terms-and-conditions
