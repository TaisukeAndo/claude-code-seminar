---
name: xlsx-creator
description: >
  Excel（.xlsx）ファイルを作成するスキル。プロジェクト・タスク管理、マーケティング・KPI管理、
  帳票（見積書・請求書・経費精算書）、その他あらゆるExcelシートに対応する。
  web-researcherサブエージェントでインターネットから業界ベンチマークや相場情報を収集し、
  excel-structure-researcherサブエージェントで未知のExcelタイプの構成をリサーチする。
  referencesフォルダの過去ファイルを参照して実態に即した数値・構成を生成する。
  ユーザーが「Excelを作って」「スプレッドシートを作りたい」「タスク管理表を作って」
  「KPIシートを作って」「見積書をExcelで」「請求書を作って」「経費精算書」など、
  Excelや表計算ファイルの作成に関する要望を述べたときは必ずこのスキルを使うこと。
---

# XLSX Creator スキル

ユーザーのニーズをヒアリングし、サブエージェントで情報収集を行い、
openpyxl で高品質な Excel ファイルを生成するスキル。

## ディレクトリ構成

```
.claude/skills/xlsx-creator/
├── SKILL.md               ← このファイル
├── references/            ← 過去のExcel・テンプレートを置く（数値・構成の参考）
├── assets/                ← ロゴ・印鑑画像（.png/.jpg）を置く
└── scripts/
    └── create_xlsx.py     ← workbook.json → .xlsx を生成

.claude/agents/
├── web-researcher.md          ← 業界データ・相場・KPIベンチマーク収集
└── excel-structure-researcher.md  ← 未定義タイプのExcel構成リサーチ
```

---

## Step 1: Excelタイプを特定してヒアリングする

ユーザーの要望から以下のいずれかを判断する：

| タイプ | キーワード例 | 詳細参照 |
|--------|-------------|----------|
| `task` | タスク管理、工程表、プロジェクト管理、進行管理 | `references/task-management.md` |
| `kpi` | KPI、マーケティング、実績管理、データ分析、目標管理 | `references/kpi-marketing.md` |
| `forms` | 見積書、請求書、経費精算、帳票、バックオフィス | `references/business-forms.md` |
| `free` | 上記以外のすべて | `excel-structure-researcher` を起動 |

### タイプ別ヒアリング項目

**task（タスク管理）**
- プロジェクト名と目的
- 開始日・終了日（期間）
- チームメンバーと人数
- イベント・プロジェクトの業種・種類（例: 展示会、新製品ローンチ、社内イベント）

**kpi（KPI・マーケティング）**
- 業種・サービス内容
- 管理したいKPIの種類（例: 売上、リード獲得数、CVR）
- 計測期間（月次・週次・四半期）
- 目標値の有無

**forms（帳票）**
- 作成する帳票の種類（見積書 / 請求書 / 経費精算書 / 複数）
- 会社名・住所・連絡先・振込先
- 主要取引の内容・単価感（おおよその価格帯）
- 消費税の扱い（税込 / 税別）

**free（その他）**
- 何を管理・整理したいか（目的）
- 利用するメンバーと頻度
- 必要な列・項目の心当たり

---

## Step 2: サブエージェントを起動する

### web-researcher の起動タイミング

以下のいずれかに該当する場合に `.claude/agents/web-researcher.md` を参照して起動する：

- **task**: プロジェクト種別が決まったら → 類似イベントの工程・タスク事例を調査
- **kpi**: 業種・KPI種類が決まったら → 業界平均値・競合ベンチマーク・目標設定の事例を調査
- **forms**: 帳票の内容が決まったら → 業界相場・一般的な項目・標準的な単価感を調査

起動例（task の場合）:
```
.claude/agents/web-researcher.md を読み、以下でリサーチしてください：
- topic: "[プロジェクト種別] のタスク管理・工程表"
- aspects: ["一般的なタスク一覧", "工程順序", "必要なリソース", "注意点"]
- context: "タスク管理Excel作成のため"
- depth: "thorough"
- language: "ja"
```

### excel-structure-researcher の起動タイミング

タイプが `free` の場合、または定義済みタイプでも特殊な構成が必要な場合に起動する：

```
.claude/agents/excel-structure-researcher.md を読み、以下でリサーチしてください：
- excel_type: "[ユーザーが求めるExcelの種類]"
- industry: "[業種]"
- use_case: "[用途・目的]"
```

---

## Step 3: references/ と assets/ を確認する

```bash
ls .claude/skills/xlsx-creator/references/
ls .claude/skills/xlsx-creator/assets/
```

- `references/` に `.xlsx` や `.csv` があれば → 列構成・数値・フォーマットの参考にする
- `references/` に `.xlsx` の帳票があれば → 単価・レイアウトを踏襲する
- `assets/` にロゴ画像があれば → `metadata.logo` に指定する

---

## Step 4: workbook.json を設計する

タイプに応じた参照ファイルを読んで workbook.json を設計する：

- **task** → `.claude/skills/xlsx-creator/references/task-management.md` を読む
- **kpi** → `.claude/skills/xlsx-creator/references/kpi-marketing.md` を読む
- **forms** → `.claude/skills/xlsx-creator/references/business-forms.md` を読む
- **free** → excel-structure-researcher の結果をもとに自由設計する

### workbook.json の基本構造

```json
{
  "metadata": {
    "title": "ファイルタイトル",
    "author": "作成者名",
    "company": "会社名",
    "logo": "logo.png"
  },
  "style": {
    "primary_color": "1E3A5F",
    "secondary_color": "4A90D9",
    "accent_color": "E8700A",
    "header_font": "游ゴシック",
    "body_font": "游ゴシック"
  },
  "sheets": [ ... ]
}
```

### テーブル型シート（task / kpi 向け）

```json
{
  "name": "タスク一覧",
  "tab_color": "1E3A5F",
  "freeze_panes": "A3",
  "title_row": {
    "text": "プロジェクトタスク管理表",
    "subtitle": "〇〇プロジェクト  2026年6月〜8月"
  },
  "info_rows": [
    {"label": "プロジェクト名", "value": "〇〇イベント"},
    {"label": "担当者", "value": "田中 / 鈴木 / 佐藤"}
  ],
  "columns": [
    {"header": "No.", "key": "no", "width": 5, "align": "center"},
    {"header": "タスク名", "key": "task", "width": 35},
    {"header": "担当者", "key": "assignee", "width": 12, "dropdown": ["田中", "鈴木", "佐藤"]},
    {"header": "開始日", "key": "start", "width": 12, "format": "date", "align": "center"},
    {"header": "期限", "key": "due", "width": 12, "format": "date", "align": "center"},
    {"header": "ステータス", "key": "status", "width": 14, "align": "center",
     "dropdown": ["未着手", "進行中", "完了", "保留"],
     "conditional_formatting": [
       {"type": "contains", "value": "完了", "fill": "C8E6C9"},
       {"type": "contains", "value": "進行中", "fill": "FFF9C4"},
       {"type": "contains", "value": "保留", "fill": "FFCCBC"}
     ]},
    {"header": "進捗", "key": "progress", "width": 10, "format": "percent", "align": "center",
     "conditional_formatting": [{"type": "data_bar"}]}
  ],
  "rows": [
    {"no": 1, "task": "キックオフMTG", "assignee": "田中", "start": "2026-06-15", "due": "2026-06-15", "status": "完了", "progress": 1.0}
  ],
  "empty_rows": 30
}
```

### フォーム型シート（帳票向け）

帳票（見積書・請求書等）は `cells` 配列で自由にセルを配置する。
詳細フォーマットは `references/business-forms.md` を参照すること。

---

## Step 5: .xlsx を生成する

```bash
# 依存ライブラリのインストール（初回のみ）
pip3 install openpyxl

# Excel生成
python3 .claude/skills/xlsx-creator/scripts/create_xlsx.py \
  /tmp/workbook.json \
  /tmp/output.xlsx
```

出力先はユーザーが指定した場所、または `/tmp/` に保存する。

---

## Step 6: 結果を報告する

- 出力ファイルのパスとシート名一覧を伝える
- web-researcher を使った場合は参照した主なソースを添える
- references/ を参照した場合はどのファイルを参考にしたか伝える
- 「列を追加したい」「単価を変えたい」などの修正依頼に対応できることを伝える

---

## 注意事項

- `references/` に置かれた過去の Excel ファイルの数値・項目構成は積極的に参考にする
- 相場・ベンチマーク数値は web-researcher の結果を使い、出典を伝える
- 帳票（forms）は必ず会社情報をヒアリングしてから生成する（後から変更も可能）
- シートが多くなる場合は tab_color で色分けして可読性を上げる
- `free` タイプは最初に excel-structure-researcher で構成案を固めてからユーザーに確認し、了承を得てから生成する
