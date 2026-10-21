# Example: Amazon.co.jp review VOC (wireless earbuds)

**Question:** Why are three earbuds stuck at a 3.9 rating while competitors score higher?

## 1. Prompt

```
評価3.9の3商品と、比較用に評価の高い3商品のレビューを、2025年1月以降の分だけ集めて。
集めたら星1〜3のレビューを不満のテーマ別に分類して、低評価の3商品に特有の不満を見つけて。
(ASIN: <low-rated x3>, <well-rated x3>)
```

## 2. Collection (Octoparse MCP)

| Step | Call | Result |
|---|---|---|
| Find template | `search_templates("amazon jp review")` | `amazon-jp-review-details-scraper` |
| Run | `execute_task` with `aSIN: [6 ASINs]`, `review_Date_Time: "2025-1-1"` | completed, 1,023 rows |
| Export | `export_data` in pages of 100 | 1,020 unique reviews |

## 3. Analysis

First pass: `python3 plugins/octoparse/skills/voc-analysis/scripts/analyze_reviews.py reviews.csv --group ASIN`, then Claude read and classified every low-star review.

| Complaint theme (low-star reviews) | Low-rated 3 (n=236) | Well-rated 3 (n=91) |
|---|---:|---:|
| Charging | 46 | 19 |
| Connection | 41 | 25 |
| Sound | 22 | 31 |
| Fit | 18 | 21 |
| Defective on arrival | 16 | 4 |
| Broke after use | 14 | 10 |
| **One earbud stops charging** | **40 (17%)** | **4 (4%)** |

**Finding:** "one earbud does not charge" is the complaint that separates the 3.9 products from the competitors. Sound and fit complaints are not higher for the weak products.

**Next collection the agent proposed:** reviews of the same products on another marketplace, and a weekly re-run to see if the charging complaint drops after a hardware revision.

Raw review text is not included in this repository. `sample_reviews_synthetic.csv` is synthetic data for testing the script.
