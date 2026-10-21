---
name: voc-analysis
description: Analyze customer reviews (Voice of Customer) collected with Octoparse or from any CSV — complaint themes, low-star drivers, competitor comparison, store-by-store differences, weekly change reports. Use when the user asks to analyze reviews, 口コミ, レビュー, VOC分析, or customer feedback.
---

# VOC analysis of collected reviews

Goal: turn raw reviews into a small number of findings the user can act on, each backed by counts and a few representative quotes.

## 1. Frame the comparison

A VOC analysis needs a comparison, otherwise every product "has complaints about battery". Set one up before reading:

- **Low vs high**: low-rated products vs well-rated competitors in the same category.
- **Store vs store**: low-rated vs high-rated branches of the same chain.
- **Before vs after**: this week vs last week, before vs after a release or firmware update.

If the data lacks a comparison group, propose what to collect (with Octoparse) to create one.

## 2. Get the numbers first

Run the bundled script for reproducible counts:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/voc-analysis/scripts/analyze_reviews.py" reviews.csv --group ASIN
```

- It auto-detects the rating and text columns (or pass `--rating` / `--text`), de-duplicates, and reports per group: review count, low-star (≤3) share, and theme hit counts in low-star reviews.
- Themes come from a keyword dictionary (Japanese + English defaults). Pass `--themes my_themes.json` to customize: `{"Theme": ["keyword", ...]}`.
- Keyword counts are a first pass. Read the low-star reviews yourself to correct the themes, split vague ones, and find complaints the dictionary misses.

## 3. Read and classify

1. Read every low-star review (or a stratified sample of 200+ if there are thousands).
2. Assign each to one primary complaint theme. Keep themes concrete ("one earbud stops charging", "wrong order handed over"), not generic ("quality").
3. Count themes per group and compute shares. A theme matters when it is clearly larger in the weak group than in the comparison group.
4. Pick 1–2 short representative quotes per key theme. Paraphrase if quoting would expose personal details.

## 4. Report

Structure:

1. **Headline finding** in one sentence with the decisive numbers (e.g. "17% of low-star reviews of the weak products mention one earbud not charging, vs 4% for competitors").
2. **Theme table** per group: count and share.
3. **What it means**: product, support, store operations or listing copy actions.
4. **What to collect next** with Octoparse (more competitors, more periods, another platform), and offer a weekly re-run.

Save the report as Markdown (and the theme table as CSV) next to the data.

## Pitfalls

- De-duplicate before counting; templates may return the same review under several filters.
- Language mix matters for stores (tourist areas): report the share of non-native-language reviews before comparing themes.
- Do not over-read small numbers: say "n=6" when a group is small.
- Do not present AI-assigned themes as exact; state they were classified from the review text.
