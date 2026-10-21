# Example: Google Maps store-by-store VOC (café chain, Shibuya)

**Question:** Why do some branches of the same chain rate lower than others?

## 1. Prompt

```
渋谷エリアの店舗を探して、評価の高い店と低い店を2店ずつ選び、口コミを各店80件集めて。
低評価の店に多い不満を、高評価の店と比べて分析して。
```

## 2. Collection (two templates, chained)

| Step | Template | Inputs | Result |
|---|---|---|---|
| Store list | `google-maps-store-listing-scraper` | keyword (chain name + area) | 20 stores (name, rating, review count, URL) |
| Reviews | `google-maps-review-scraper-cloud` | 4 place URLs from step 1, `number_of_Pages: 8` (10 reviews/page) | 320 reviews |

The URLs from the store list feed directly into the review template.

## 3. Analysis

| Store (rating) | A (4.2) | B (4.1) | C (3.8) | D (3.7) |
|---|---:|---:|---:|---:|
| 1–2 star reviews | 6 | 6 | 14 | 16 |
| Order mistakes | 0 | 2 | 6 | 6 |
| Staff attitude | 2 | 0 | 7 | 5 |

**Finding:** the low-rated branches are not hurt by product quality but by order accuracy and staff attitude — an operations issue.

**Pitfall caught:** over 70% of store B's reviews were not in Japanese (tourist area), so comparing B on Japanese keywords alone would be misleading. Check language mix first.

Store names are anonymized. Raw review text is not included in this repository.
