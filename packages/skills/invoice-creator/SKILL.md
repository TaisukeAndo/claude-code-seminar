---
name: invoice-creator
description: >
  見積書・請求書・領収書を4形式（Excel / マネーフォワード / フリー / 弥生会計）で生成するスキル。
  個人情報（自社住所・銀行口座・取引先住所等）はLLMに渡さず、
  .envファイルとclients/*.jsonから実行時にのみ読み込む設計（プライバシー保護）。
  ユーザーが「見積書を作って」「請求書を発行したい」「領収書を作成して」
  「マネーフォワード用に請求書を」「フリー(freee)で見積書を」「弥生会計用に」
  などと要望した場合は必ずこのスキルを使うこと。
---

# invoice-creator スキル

## このスキルの最重要原則（プライバシー保護）

**Claude（LLM）は以下の情報を絶対に収集・保持・document.jsonに含めてはいけない：**
- 自社の住所・電話番号・メールアドレス・銀行口座・代表者名
- 取引先の住所・電話番号・メールアドレス・担当者名
- インボイス登録番号・法人番号

これらはすべて `.env` ファイルと `clients/*.json` ファイルに保存され、
**Pythonスクリプト実行時にのみ** 読み込まれる。
LLMが扱うのは「明細・金額・日付・件名」など業務内容のみ。

---

## ディレクトリ構成

```
.claude/skills/invoice-creator/
├── SKILL.md               ← このファイル
├── .env                   ← 自社情報・銀行口座（Git管理外・PII）
├── .env.example           ← .envのテンプレート（設定方法の案内用）
├── clients/               ← 取引先情報（PII）
│   └── {client_id}.json
├── assets/                ← 印鑑・ロゴ画像
└── scripts/
    ├── common.py                  ← 共通ユーティリティ
    ├── generate_excel.py          ← Excel出力
    ├── generate_moneyforward.py   ← マネーフォワード CSV出力
    ├── generate_freee.py          ← フリー CSV出力
    └── generate_yayoi.py          ← 弥生会計 CSV出力
```

---

## Step 1: 初回セットアップ確認

スキルを初めて使う場合、または `.env` が未設定の場合：

```bash
ls .claude/skills/invoice-creator/.env 2>/dev/null || echo "NOT_FOUND"
```

`.env` が存在しない場合はユーザーに以下を案内する：
```
.env.example を参考に .claude/skills/invoice-creator/.env を作成し、
自社情報・銀行口座情報を記入してください。
この情報はLLMには送信されず、ローカルでのみ使用されます。
```

---

## Step 2: 文書タイプと出力形式を確認

ユーザーの要望から以下を特定する：

### 文書タイプ
| タイプ | キーワード例 |
|--------|-------------|
| `estimate` | 見積書、お見積り、見積もり |
| `invoice` | 請求書、請求、インボイス |
| `receipt` | 領収書、領収、受領書 |

### 出力形式
| 形式 | キーワード例 | デフォルト |
|------|-------------|-----------|
| `excel` | Excel、エクセル、xlsx | ✅（未指定の場合） |
| `moneyforward` | マネーフォワード、MF、マネフォ |  |
| `freee` | フリー、freee |  |
| `yayoi` | 弥生、弥生会計、やよい |  |

不明な場合はユーザーに確認する。

---

## Step 3: 取引先（client）を確認

```bash
ls .claude/skills/invoice-creator/clients/
```

### 既存クライアントがある場合
ファイル一覧を表示して、どの取引先か確認する。
`client_id` はファイル名（拡張子なし）を使う。

例: `clients/abc_corp.json` → `client_id: "abc_corp"`

### クライアントファイルがない場合
ユーザーに以下を案内する。**住所などは Claude に教えなくてよい。**

```
取引先ファイルを作成してください（住所等は直接このファイルに記載、LLMには送信されません）：

ファイルパス: .claude/skills/invoice-creator/clients/{取引先ID}.json

参考: .claude/skills/invoice-creator/clients/example_client.json
```

取引先ファイルが作成されたら Step 4 に進む。

---

## Step 4: 文書内容をヒアリング（PII不要）

Claude が収集する情報（すべてビジネス内容のみ、PII不要）：

### 全文書タイプ共通
- **文書番号**: 例 `INV-2026-001`（未指定なら日付ベースで自動採番）
- **発行日**: 例 `2026-06-14`（未指定なら今日の日付）
- **件名**: 例 `Webサイト制作費用`

### 見積書・請求書の明細項目
各明細について：
- **品目名**: 例 `システム設計・開発`
- **数量**: 例 `1`
- **単位**: 例 `式`・`時間`・`個`・`ヶ月`
- **単価**: 例 `500000`
- **消費税率**: `10`（通常）または `8`（軽減税率）

### 請求書のみ
- **支払期日**: 例 `2026-07-31`
- **備考**: 例 `お振込手数料はご負担ください`

### 領収書のみ
- **金額**: 受領した金額（税込）
- **但し書き**: 例 `Webシステム開発費として`
- **受領日**: 実際に受け取った日付

---

## Step 5: document.json を作成

PII を一切含まない document.json を `/tmp/invoice_document.json` に作成する。

### 見積書・請求書の例
```json
{
  "document_type": "invoice",
  "output_format": "excel",
  "document_number": "INV-2026-001",
  "issue_date": "2026-06-14",
  "due_date": "2026-07-31",
  "client_id": "abc_corp",
  "title": "Webサイト制作費用",
  "items": [
    {
      "name": "システム設計・開発",
      "quantity": 1,
      "unit": "式",
      "unit_price": 500000,
      "tax_rate": 10
    },
    {
      "name": "デザイン制作",
      "quantity": 1,
      "unit": "式",
      "unit_price": 150000,
      "tax_rate": 10
    }
  ],
  "notes": "お振込手数料はご負担ください",
  "tax_calculation": "exclusive"
}
```

### 領収書の例
```json
{
  "document_type": "receipt",
  "output_format": "excel",
  "document_number": "REC-2026-001",
  "issue_date": "2026-06-14",
  "client_id": "abc_corp",
  "title": "Webシステム開発費として",
  "total_amount": 715000,
  "tax_amount": 65000,
  "subtotal_amount": 650000,
  "notes": ""
}
```

---

## Step 6: Pythonスクリプトを実行

出力形式に応じてスクリプトを選択：

```bash
# 依存パッケージ確認・インストール（初回のみ）
pip3 install openpyxl 2>/dev/null || pip install openpyxl 2>/dev/null

# Excel出力
python3 .claude/skills/invoice-creator/scripts/generate_excel.py \
  /tmp/invoice_document.json \
  /tmp/output_invoice.xlsx

# マネーフォワード CSV出力
python3 .claude/skills/invoice-creator/scripts/generate_moneyforward.py \
  /tmp/invoice_document.json \
  /tmp/output_moneyforward.csv

# フリー CSV出力
python3 .claude/skills/invoice-creator/scripts/generate_freee.py \
  /tmp/invoice_document.json \
  /tmp/output_freee.csv

# 弥生会計 CSV出力
python3 .claude/skills/invoice-creator/scripts/generate_yayoi.py \
  /tmp/invoice_document.json \
  /tmp/output_yayoi.csv
```

出力ファイルはユーザーが指定した場所、または `/tmp/` に保存する。

---

## Step 7: ファイルを開いて結果を報告

```bash
open /tmp/output_invoice.xlsx        # Excel
open /tmp/output_moneyforward.csv    # CSV（テキストエディタで確認）
```

ユーザーへの報告内容：
- 生成されたファイルのパス
- 主な内訳（件名・合計金額・取引先）
- CSVの場合は「〇〇からインポートしてください」と案内
- 「修正したい」「別形式でも出力したい」に対応できると伝える

---

## 注意事項

- `.env` と `clients/*.json` の内容はユーザーに読み上げたり確認したりしない
- エラー時は「`.env` ファイルを確認してください」と案内するにとどめる
- 収入印紙: 領収書の金額が50,000円以上の場合は「収入印紙が必要な場合があります」と案内
- インボイス制度: `.env` に `MY_REGISTRATION_NUMBER` が設定されていれば自動で記載される
- 弥生会計の仕訳CSV形式は弥生会計のバージョン（デスクトップ版/クラウド版）によって異なる場合がある
