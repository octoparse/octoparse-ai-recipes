#!/usr/bin/env python3
"""First-pass VOC counts for a review CSV (standard library only).

Usage:
  python3 analyze_reviews.py reviews.csv [--group COL] [--rating COL] [--text COL]
                             [--low 3] [--themes themes.json] [--out summary.md]
"""
import argparse
import csv
import json
import re
import sys
from collections import Counter, defaultdict

DEFAULT_THEMES = {
    "Charging / battery": ["充電", "バッテリー", "電池", "charge", "charging", "battery"],
    "Connection / pairing": ["接続", "ペアリング", "途切", "切れる", "bluetooth", "connect", "pairing", "disconnect"],
    "Sound": ["音質", "ノイズ", "雑音", "音が", "sound", "audio", "noise"],
    "Fit / comfort": ["装着", "フィット", "耳が痛", "落ち", "fit", "comfort", "falls out"],
    "Defective on arrival": ["初期不良", "不良品", "届いた時", "doa", "defective", "dead on arrival"],
    "Broke after use": ["故障", "壊れ", "動かなくな", "使えなくな", "broke", "stopped working"],
    "Order accuracy": ["違う", "間違", "注文と", "wrong order", "mistake"],
    "Staff attitude": ["接客", "店員", "態度", "対応", "staff", "rude", "service"],
    "Wait / crowding": ["待", "混", "行列", "wait", "crowded", "queue"],
    "Price / value": ["高い", "値段", "価格", "コスパ", "price", "expensive", "value"],
}

RATING_HINTS = ["star", "rating", "評価", "星", "stars", "score"]
TEXT_HINTS = ["review", "text", "content", "body", "レビュー", "口コミ", "本文", "comment"]


def pick(cols, hints, exclude=()):
    low = {c: c.lower() for c in cols}
    for h in hints:
        for c in cols:
            if c in exclude:
                continue
            if low[c] == h.lower():
                return c
    for h in hints:
        for c in cols:
            if c in exclude:
                continue
            if h.lower() in low[c] and "title" not in low[c] and "タイトル" not in c:
                return c
    return None


def to_rating(v):
    m = re.search(r"\d+(\.\d+)?", str(v or ""))
    return float(m.group()) if m else None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv")
    ap.add_argument("--group", help="column to compare by (e.g. ASIN, store)")
    ap.add_argument("--rating")
    ap.add_argument("--text")
    ap.add_argument("--low", type=float, default=3, help="ratings <= this count as low-star (default 3)")
    ap.add_argument("--themes", help="JSON file {theme: [keywords]}")
    ap.add_argument("--out", help="write Markdown summary here")
    a = ap.parse_args()

    with open(a.csv, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        sys.exit("No rows found.")
    cols = list(rows[0].keys())
    rcol = a.rating or pick(cols, RATING_HINTS)
    tcol = a.text or pick(cols, TEXT_HINTS, exclude=(rcol,))
    if not rcol or not tcol:
        sys.exit(f"Could not detect rating/text columns in {cols}. Pass --rating and --text.")
    themes = DEFAULT_THEMES
    if a.themes:
        with open(a.themes, encoding="utf-8") as f:
            themes = json.load(f)

    seen, uniq = set(), []
    for r in rows:
        key = (r.get(a.group, "") if a.group else "", (r.get(tcol) or "").strip())
        if not key[1]:
            uniq.append(r)  # rating-only review: keep for low-star share
        elif key not in seen:
            seen.add(key)
            uniq.append(r)

    stats = defaultdict(lambda: {"n": 0, "low": 0, "themes": Counter()})
    for r in uniq:
        g = r.get(a.group, "") if a.group else "all"
        s = stats[g]
        s["n"] += 1
        rating = to_rating(r.get(rcol))
        if rating is not None and rating <= a.low:
            s["low"] += 1
            text = (r.get(tcol) or "").lower()
            for theme, kws in themes.items():
                if any(k.lower() in text for k in kws):
                    s["themes"][theme] += 1

    out = [f"# VOC first-pass summary", "",
           f"- File: `{a.csv}`  rows: {len(rows)}  unique: {len(uniq)}",
           f"- Rating column: `{rcol}`  text column: `{tcol}`  low-star: <= {a.low:g}", ""]
    groups = sorted(stats)
    out += ["| Group | Reviews | Low-star | Low-star share |", "|---|---:|---:|---:|"]
    for g in groups:
        s = stats[g]
        share = s["low"] / s["n"] * 100 if s["n"] else 0
        out.append(f"| {g} | {s['n']} | {s['low']} | {share:.0f}% |")
    out += ["", "## Theme hits in low-star reviews (keyword match, one review can hit several)", "",
            "| Theme | " + " | ".join(groups) + " |", "|---|" + "---:|" * len(groups)]
    for theme in themes:
        cells = []
        for g in groups:
            s = stats[g]
            c = s["themes"][theme]
            cells.append(f"{c} ({c / s['low'] * 100:.0f}%)" if s["low"] else "0")
        out.append(f"| {theme} | " + " | ".join(cells) + " |")
    out += ["", "_Keyword counts are a first pass; read the low-star reviews to refine themes._"]
    text = "\n".join(out)
    print(text)
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            f.write(text + "\n")


if __name__ == "__main__":
    main()
