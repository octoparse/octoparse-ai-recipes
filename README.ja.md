# Octoparse AI Recipes

**Octoparseでデータを集め、AIエージェントで分析する。**
Claude Code・Claude・Codexなど、MCP対応のクライアントで使えます。

[English](README.md)

収集はOctoparseが担当します。Amazon・Googleマップなど多数のサイトに対応したテンプレート、クラウド実行、ブロック対策まで含めて任せられます。AIエージェントは「何を集めるか」を決め、MCP経由でテンプレートを実行し、集まったデータを分析して次の打ち手まで提案します。

```
あなた：「この6商品のレビューを1月以降の分だけ集めて、低評価の商品に特有の不満を見つけて」
 → AIがAmazonレビューのテンプレートを選択 → Octoparseがクラウドで1,023件を収集
 → AIが不満を分類 →「低評価レビューの17%が『片耳だけ充電できない』（比較対象は4%）」
```

## インストール

### Claude Code（プラグイン：MCPサーバー＋スキル）

```
/plugin marketplace add octoparse/octoparse-ai-recipes
/plugin install octoparse@octoparse
```

インストール後に `/mcp` を実行し、`octoparse` を選んでOctoparseアカウントでログインします。

### Codex

```
codex mcp add octoparse --url https://mcp.octoparse.com
codex mcp login octoparse
```

スキルと `AGENTS.md` を使う場合は、このリポジトリをcloneするか、`plugins/octoparse/skills/` を自分のプロジェクトにコピーしてください。

### Claude（Web・デスクトップ）

カスタムコネクタとして `https://mcp.octoparse.com` を追加します。スキルを使う場合は `plugins/octoparse/skills/` 配下のフォルダをzipにして、設定のスキル画面からアップロードします。

## 収録内容

| パス | 内容 |
|---|---|
| `plugins/octoparse/.mcp.json` | Octoparse MCPサーバー（`https://mcp.octoparse.com`） |
| `plugins/octoparse/skills/octoparse-scraping/` | テンプレートの選び方・実行・データ書き出し、テンプレートがない場合のCLIでの自作タスク |
| `plugins/octoparse/skills/voc-analysis/` | レビュー（VOC）分析の手順と、集計スクリプト `analyze_reviews.py` |
| `examples/` | 実例：AmazonレビューのVOC分析、Googleマップの店舗別VOC分析 |
| `AGENTS.md` / `CLAUDE.md` | このリポジトリで作業するAIエージェント向けの指示 |

## 試してみる

インストール後、AIエージェントに次のように指示します。

- 「Amazon.co.jpのレビュー収集テンプレートで、ASIN XXXXX の2025年1月以降のレビューを集めて、主な不満をまとめて」
- 「Googleマップで『（チェーン名） 渋谷』の店舗一覧を取って、評価の高い店と低い店を2店ずつ選び、口コミを各店80件集めて比較して」
- 「毎週月曜に、自社商品と競合2商品の新着レビューを集めて、増えた不満を教えて」

## 必要なもの

- Octoparseアカウント（無料プランあり。無料プランではMCPとCLIのテンプレート実行で月間の取得件数枠を共有します）
- 自作タスクを使う場合：Node 20以上と `npm i -g @octoparse-ai/octoparse-cli`

## リンク

- 解説記事：[VOC分析とは？AIで口コミを収集・分析するやり方](https://www.octoparse.jp/blog/)
- テンプレート一覧：https://www.octoparse.jp/template
- 無料ダウンロード：https://www.octoparse.jp/download

公開されているデータのみを対象とし、各サイトの利用規約に従ってご利用ください。

## ライセンス

MIT
