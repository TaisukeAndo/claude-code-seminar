---
name: pptx-creator
description: >
  PowerPoint（.pptx）ファイルを作成するスキル。ユーザーがMarkdownまたはdocxで提供したコンテンツをもとにスライドを生成する。
  references/styles/ フォルダ内のMarkdownスタイルガイドを言語処理で読み込み、目的・用途に合ったデザインを自動適用する。
  ユーザーが「プレゼン資料を作って」「スライドを作成して」「PPTXを作りたい」「発表資料」「deckを作って」など
  スライド・プレゼンテーション作成に関する要望を述べたとき、または .md / .docx ファイルをプレゼン化したいと述べたときは
  必ずこのスキルを使うこと。
---

# PPTX Creator スキル

ユーザーが提供したコンテンツを読み込み、`references/styles/` のMarkdownスタイルガイドをLLMが解釈し、
PptxGenJS（Node.js）で `.pptx` ファイルを生成するスキル。

## ディレクトリ構成

```
.claude/skills/pptx-creator/
├── SKILL.md                      ← このファイル
├── references/
│   └── styles/                   ← Markdown スタイルガイド（追加・選択可）
│       ├── seminar-tech.md       ← 技術セミナー・ハンズオン向け
│       ├── business-clean.md     ← 社内プレゼン・提案書向け
│       └── bold-visual.md        ← カンファレンス・外部登壇向け
├── assets/                       ← ロゴ・アイコン・図解画像（スライドに直接埋め込む）
└── scripts/
    └── create_pptx.js            ← slides.json → .pptx を生成（Node.js / PptxGenJS）
```

### スタイルガイドの追加方法

`references/styles/` フォルダに新しい `.md` ファイルを追加するだけでスタイルが増える。
ファイルの先頭に YAML フロントマターで `name`, `category`, `purpose`, `tags` を定義する。

```markdown
---
name: my-style
category: custom
purpose: 自社ブランド向けプレゼン
tags: [custom, brand]
---

# スタイルガイド：My Style
...（カラー・フォント・レイアウト仕様を Markdown で記述）
```

複数のスタイルガイドを組み合わせることもできる。たとえば
「business-clean をベースにして、accent だけ seminar-tech に合わせて」のような指示も可能。

---

## ワークフロー

### Step 1: 入力ファイルを読み込む

ユーザーが渡したコンテンツファイル（`.md` または `.docx`）を読む。

- **Markdown**: Read ツールでそのまま読む
- **docx**: Bash で以下を実行してテキスト抽出する
  ```bash
  python3 -c "
  from docx import Document
  doc = Document('<path>')
  for p in doc.paragraphs:
      print(p.style.name, '|', p.text)
  "
  ```
- **ディレクトリ**: 複数の `.md` ファイルがある場合は全て読み込んで内容を統合する

---

### Step 2: スタイルガイドを選択・読み込む（言語処理）

`references/styles/` フォルダのスタイルガイドを確認し、目的に合うものを Read で読み込む。

```bash
ls .claude/skills/pptx-creator/references/styles/
```

**選択の基準（スクリプト不要・LLMが判断）:**

| 用途 | 選択するスタイルガイド |
|------|---------------------|
| 技術セミナー・ハンズオン・AI勉強会 | `seminar-tech` |
| 社内プレゼン・提案書・報告書 | `business-clean` |
| 外部登壇・カンファレンス・発表会 | `bold-visual` |
| ユーザーが明示した場合 | 指示通りのファイルを使う |

スタイルガイドの内容を読んでカラーコード・フォント・レイアウト仕様を把握し、
slides.json の `style` セクションに反映する。**スクリプト実行は不要。**

複数のガイドを読み込んで組み合わせることも可能（例: ベースは business-clean、accent だけ変更）。

---

### Step 3: スライド構成を設計する

コンテンツとスタイルガイドをもとに、Claude 自身がスライドの構成を判断する。

**スライドの設計原則:**
- タイトルスライドは必ず1枚目
- 大セクションの区切りには `section` タイプを挿入する
- 1スライドの箇条書きは原則5項目以内（多い場合は複数スライドに分割）
- 最終スライドは `closing` タイプ
- 比較・対比は `two_column` タイプで
- 数値・インパクトデータは `stat` タイプで
- グラフ・データは `chart` タイプで

**スライドタイプ一覧:**

| type | 用途 | 主なフィールド |
|------|------|-------------|
| `title` | タイトルページ | `title`, `subtitle` |
| `section` | セクション区切り | `title`, `subtitle`（任意） |
| `content` | 箇条書き | `title`, `content[]`, `image`（任意） |
| `two_column` | 2カラム比較 | `title`, `left_title`, `left[]`, `right_title`, `right[]` |
| `stat` | 数値インパクト強調 | `title`, `subtitle`, `stats[]` |
| `chart` | グラフ・チャート | `title`, `chart_type`, `chart_data[]`, `chart_options` |
| `image` | 画像メイン | `title`, `image`, `caption` |
| `closing` | 最終スライド | `title`, `subtitle` |

---

### Step 3.5: assets/ フォルダを確認する

```bash
ls .claude/skills/pptx-creator/assets/
```

ロゴ・アイコンがあれば `slides.json` の `metadata.logo` や各スライドの `image` フィールドで参照できる。

---

### Step 4: slides.json を作成する

スタイルガイドから読み取った値を `style` セクションに明示して書く。

```json
{
  "metadata": {
    "title": "プレゼンタイトル",
    "widescreen": true,
    "logo": "",
    "logo_slides": "none"
  },
  "style": {
    "primary_color": "#1A1A2E",
    "secondary_color": "#16213E",
    "accent_color": "#E94560",
    "text_color": "#1A1A2E",
    "heading_font": "Meiryo",
    "body_font": "Meiryo"
  },
  "slides": [
    {
      "type": "title",
      "title": "タイトル",
      "subtitle": "サブタイトル"
    },
    {
      "type": "stat",
      "title": "数値で見る効果",
      "stats": [
        { "value": "2〜3時間", "label": "従来の作業時間" },
        { "value": "15分", "label": "AIを使った場合", "highlight": true },
        { "value": "85%", "label": "削減率", "highlight": true }
      ]
    },
    {
      "type": "chart",
      "title": "工程別作業時間の比較（分）",
      "chart_type": "bar",
      "chart_data": [
        {
          "name": "従来フロー",
          "labels": ["情報収集", "構成作成", "執筆", "修正確認"],
          "values": [30, 20, 90, 30]
        },
        {
          "name": "AIフロー",
          "labels": ["情報収集", "構成作成", "執筆", "修正確認"],
          "values": [2, 1, 10, 15]
        }
      ],
      "chart_options": {
        "bar_dir": "col",
        "show_value": true,
        "show_legend": true
      }
    },
    {
      "type": "section",
      "title": "Chapter 1\n概要"
    },
    {
      "type": "content",
      "title": "箇条書きスライド",
      "content": [
        "Level 0 の項目（太字・アクセントマーカー付き）",
        { "text": "Level 1 の補足説明（インデント・グレー）", "level": 1 },
        "Level 0 の別項目"
      ]
    },
    {
      "type": "two_column",
      "title": "Before / After 比較",
      "left_title": "従来の方法",
      "left": ["項目A", "項目B"],
      "right_title": "AI を使った場合",
      "right": ["改善A", "改善B"]
    },
    {
      "type": "closing",
      "title": "ご清聴ありがとうございました",
      "subtitle": "補足メッセージ"
    }
  ]
}
```

**`stat` スライドの `stats` フィールド:**
```json
{ "value": "表示する数値や文字列", "label": "説明ラベル", "highlight": true }
```
- `highlight: true` の stat は Accent カラーで強調表示される
- 最大4つまで並べられる

**`chart` スライドの `chart_type`:**
- `"bar"` — 棒グラフ（複数系列の比較に最適）
- `"pie"` — 円グラフ（割合・構成比）
- `"doughnut"` — ドーナツグラフ
- `"line"` — 折れ線グラフ（推移・トレンド）

**`chart_options` の主なパラメータ:**
- `bar_dir`: `"col"`（縦棒）/ `"bar"`（横棒）
- `show_value`: `true` / `false`（値ラベル表示）
- `show_legend`: `true` / `false`（凡例表示）

---

### Step 5: PPTX を生成する

```bash
node .claude/skills/pptx-creator/scripts/create_pptx.js \
  /tmp/slides.json \
  /tmp/output.pptx
```

出力先はユーザーが指定した場所、または入力ファイルと同じディレクトリに置く。

---

### Step 6: 画像収集（必要な場合）

slides.json に `image` フィールドがあり、`assets/` に該当ファイルがない場合：

プレースホルダーボックスで生成し、以下の指示を出す：
```
以下の画像を準備して assets/ フォルダに配置してください。
- assets/xxx.png → [説明]

配置が完了したら「画像差し替えお願いします」と入力してください。
Node.js スクリプトを自動再実行して画像込みのファイルを生成します。
```

---

### Step 7: 結果を報告する

- 出力ファイルのパスと枚数を伝える
- 使用したスタイルガイドを1行で報告する
- プレースホルダーがある場合は一覧を添える

---

### 画像差し替えの自動再実行

ユーザーが「画像差し替えお願いします」「画像準備できました」と入力した場合:

```bash
cat .claude/skills/pptx-creator/last_run.json
# rerun_cmd を実行する
```
