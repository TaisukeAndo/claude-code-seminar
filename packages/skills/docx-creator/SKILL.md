---
name: docx-creator
description: >
  Word文書（.docx）を作成するスキル。レポート・報告書、提案書・企画書、議事録・会議メモ、
  マニュアル・手順書、セミナー資料に対応。ユーザーがMarkdownや口頭で伝えた内容をもとに
  document.json を設計し、python-docx でプロフェッショナルな Word ファイルを生成する。
  情報が不足している場合や客観的なエビデンスが必要な場合は、web-researcher サブエージェントを
  起動してインターネットから信頼できるソースを収集・引用する。
  ユーザーが「Word文書を作って」「報告書を書いて」「議事録にまとめて」「提案書を作成して」
  「マニュアルを作りたい」「セミナー資料をWordで」など、文書作成に関する要望を述べたときは
  必ずこのスキルを使うこと。
---

# DOCX Creator スキル

## ディレクトリ構成

```
.claude/
├── agents/
│   └── web-researcher.md      ← 情報収集サブエージェント（他スキルと共有）
└── skills/docx-creator/
    ├── SKILL.md               ← このファイル
    ├── references/            ← Wordテンプレート (.docx) を置く
    ├── assets/                ← ロゴ・アイコン・図解画像を置く
    └── scripts/
        └── create_docx.py    ← document.json → .docx を生成
```

---

## ワークフロー

### Step 1: ユーザーにヒアリングする

以下を確認する（会話から推測できる場合はスキップ）：

| 確認事項 | 例 |
|----------|-----|
| ドキュメントの種類 | report / proposal / minutes / manual / seminar |
| タイトルと目的 | 「〇〇に関する提案書、経営層向け」 |
| 主なコンテンツ | 提供済みのMarkdown・メモ・口頭説明 |
| ページ数の目安 | 「5〜8ページ程度」 |
| エビデンスの必要性 | 市場データ・統計など外部情報が必要か |

---

### Step 2: 情報収集サブエージェントの判断

以下のいずれかに当てはまる場合、**web-researcher サブエージェントを起動**する：

- ユーザーが統計・調査データ・市場規模などを求めている
- 提案書や報告書で「客観的エビデンスがあると説得力が増す」と判断できる
- ユーザーが「最新情報も含めて」「調べながら書いて」と述べた場合

**起動方法：** `.claude/agents/web-researcher.md` を読み、以下の形式でサブエージェントに渡す：

```
.claude/agents/web-researcher.md の指示に従ってリサーチを実施してください。
- topic: "リサーチテーマ"
- aspects: ["調べたい観点1", "調べたい観点2"]
- context: "文書の用途と読者"
- depth: "thorough"
- language: "ja"
```

サブエージェントの結果（JSON）から `key_findings` と `citations` を document.json に組み込む。

---

### Step 3: テンプレートとアセットを確認する

```bash
ls .claude/skills/docx-creator/references/
ls .claude/skills/docx-creator/assets/
```

- `references/` に `.docx` ファイルがあれば `metadata.template` に指定（スタイルを継承）
- `assets/` にロゴがあれば `metadata.logo` に指定
- 適切なものがなければテンプレートなしでオリジナルデザインで生成する

---

### Step 4: document.json を設計する

ドキュメント種別に応じた構成を設計する。

#### 種別ごとの標準構成

**report（報告書）**
```
title_page → toc → heading(エグゼクティブサマリー) → paragraph
→ heading(背景・目的) → heading(調査結果) → table/image
→ heading(考察) → heading(結論・提言) → references
```

**proposal（提案書）**
```
title_page → toc → heading(提案概要) → heading(現状と課題)
→ heading(提案内容) → heading(期待効果) → table(費用・スケジュール)
→ heading(まとめ) → references
```

**minutes（議事録）**
```
minutes_header → heading(議題) → heading(決定事項) → bullets
→ heading(議論内容) → paragraph → heading(アクションアイテム) → table
→ heading(次回予定)
```

**manual（マニュアル）**
```
title_page → toc → heading(概要) → heading(前提条件) → bullets
→ heading(手順) → numbered → image(スクリーンショット等)
→ heading(トラブルシューティング) → table
```

**seminar（セミナー資料）**
```
title_page → heading(セミナー概要) → heading(アジェンダ) → bullets
→ heading(第1章: ...) → paragraph → heading(第2章: ...) → ...
→ heading(まとめ) → references
```

#### document.json の完全フォーマット

```json
{
  "metadata": {
    "title": "ドキュメントタイトル",
    "subtitle": "サブタイトル（任意）",
    "author": "著者名",
    "date": "YYYY-MM-DD",
    "doc_type": "report",
    "logo": "logo.png",
    "template": "report_template.docx",
    "location": "会議室A（minutesのみ）",
    "attendees": "田中、鈴木、佐藤（minutesのみ）"
  },
  "style": {
    "primary_color": "1E3A5F",
    "heading_font": "游明朝",
    "body_font": "游明朝",
    "body_size": 10.5
  },
  "sections": [
    {"type": "title_page"},
    {"type": "toc"},
    {"type": "heading", "text": "1. はじめに", "level": 1},
    {"type": "paragraph", "text": "本文テキスト。引用がある場合は[1]のように番号を付ける。"},
    {"type": "bullets", "items": [
      "項目1",
      {"text": "項目2（子要素あり）", "children": ["子項目A", "子項目B"]}
    ]},
    {"type": "numbered", "items": ["手順1", "手順2", "手順3"]},
    {"type": "table",
     "caption": "表1: ○○の比較",
     "headers": ["項目", "A案", "B案"],
     "rows": [["コスト", "100万円", "80万円"], ["期間", "3ヶ月", "4ヶ月"]]},
    {"type": "image", "file": "chart.png", "caption": "図1: ○○の推移", "width_cm": 14.0},
    {"type": "page_break"},
    {"type": "references", "citations": [
      {
        "id": 1,
        "title": "記事タイトル",
        "source": "発行機関名",
        "url": "https://example.com",
        "accessed": "YYYY-MM-DD"
      }
    ]}
  ]
}
```

---

### Step 4.5: 画像アセスメント（重要）

document.json を設計する際、**必ず** 画像の必要性を判断してユーザーに確認する。

#### 文書タイプ別の画像ニーズ

| 文書タイプ | 画像の必要性 | 推奨する画像 |
|-----------|------------|-------------|
| 議事録（minutes） | **不要** | テキスト重視。画像は原則なし |
| マニュアル（manual） | **有効** | 操作画面のスクリーンショット |
| 提案書（proposal） | **有効** | フロー図・比較図・実績グラフ |
| 報告書（report） | **ケースバイケース** | グラフ・データ可視化 |
| セミナー資料（seminar） | **有効** | フロー図・手順のスクリーンショット |

#### `image` セクションの書き方（document.json）

```json
{
  "type": "image",
  "file": "ai_workflow.png",
  "alt": "AIがリサーチ→構成→執筆→テストの4ステップを実行するフローチャート",
  "caption": "図1: AI文書作成プロセス",
  "width_cm": 14.0
}
```

- `alt` フィールド: 画像が見つからない場合のプレースホルダーに表示される説明。**必須**
- 画像が存在しない場合は自動的に「視覚的プレースホルダーボックス」を生成する

#### ユーザーへの確認フレーズ
```
以下の箇所に画像を追加すると理解しやすくなります。
- 第X章「○○」→ ai_workflow.png（4ステップフロー図）
- 第Y章「○○」→ screenshot.png（操作画面のスクリーンショット）
画像を自分で用意しますか？それともAIがインターネットから探しますか？
（「不要」を選ぶとテキストのみで生成します）
```

### Step 5: .docx を生成する

```bash
python3 .claude/skills/docx-creator/scripts/create_docx.py \
  /tmp/document.json \
  /tmp/output.docx
```

---

### Step 6: 画像収集（必要な場合）

document.json に `image` セクションがあり、`assets/` に該当ファイルがない場合：

**A. ユーザーが画像を自分で用意する場合**

生成後に以下の指示を出す：
```
以下の画像を準備して assets/ フォルダに配置してください。
[PLACEHOLDER一覧]
- assets/ai_workflow.png　→　AIの4ステップフロー図
- assets/screenshot.png　→　操作画面のスクリーンショット

配置が完了したら「画像差し替えお願いします」と入力してください。
Pythonスクリプトを自動再実行して画像込みのファイルを生成します。
```

**B. ユーザーが画像を用意できない場合**

`.claude/agents/image-researcher.md` に従い image-researcher サブエージェントを起動する：
```
image-researcher を起動してください。
- filename: "ai_workflow.png"
- description: "4ステップのビジネスワークフロー フローチャート ブルー"
- context: "Word文書のセミナー資料"
- assets_dir: ".claude/skills/docx-creator/assets"
- license_required: "free"
```

収集した画像の引用情報は文書末尾の `references` セクションに追記する。

### Step 7: 結果を報告する・再実行トリガーを案内する

- 出力ファイルのパスを伝える
- セクション数・引用数の概要を報告する
- プレースホルダーが1件以上ある場合、必ず以下を添える：

```
[プレースホルダーがある箇所]
- 第X章: assets/ai_workflow.png に画像を配置
- 第Y章: assets/screenshot.png に画像を配置

画像の準備ができたら「画像差し替えお願いします」と入力してください。
```

### 画像差し替えの自動再実行トリガー

ユーザーが以下のいずれかを入力した場合、`last_run.json` を読んで DOCX を再生成する：
- 「画像差し替えお願いします」
- 「画像準備できました」
- 「画像を入れて再生成して」

```bash
cat .claude/skills/docx-creator/last_run.json
# rerun_cmd の値を実行する
```

---

## スタイルガイドライン

### デフォルトスタイル（style セクション省略時）

```json
{
  "primary_color": "1E3A5F",
  "heading_font":  "游明朝",
  "body_font":     "游明朝",
  "body_size":     10.5
}
```

### フォントの選択方針

- 日本語の公式文書: `游明朝`（フォーマル）または `游ゴシック`（読みやすさ重視）
- references/ に `.docx` テンプレートがある場合: テンプレートのスタイルを優先

### 引用の書き方

本文中では `[1]` のように番号を振り、末尾の `references` セクションにまとめる。
web-researcher の結果を使う場合は `citations` 配列をそのまま流用できる。

---

## 注意事項

- 目次（`toc` セクション）は Word で開いた後に「フィールドの更新」が必要
- テンプレートを使う場合、スタイル定義はテンプレートが優先される
- `assets/` に画像がない場合はスキップし警告のみ出す（エラーにはならない）
- 議事録（minutes）は `minutes_header` セクションを `title_page` の代わりに使う
