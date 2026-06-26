# 帳票フォーマット テンプレート仕様

見積書・請求書・経費精算書を1つのExcelブックにまとめて作成する。
フォーム型シート（`cells` 配列）を使い、実際のビジネス文書に近いレイアウトを実現する。

---

## シート構成（推奨）

| シート名 | タイプ | 内容 |
|----------|--------|------|
| 見積書 | forms | 商品・サービスの見積書 |
| 請求書 | forms | 見積書から転記できる請求書 |
| 経費精算書 | forms | 経費申請・精算記録 |
| 単価マスタ | table | よく使う項目の単価一覧（参照用） |

必要な帳票だけ作成すればよい（全部必須ではない）。

---

## ヒアリング必須項目

帳票生成前に以下を確認する：

```
- 会社名（発行者）:
- 郵便番号・住所:
- 電話番号・メールアドレス:
- 振込先銀行・支店・口座番号（請求書用）:
- 担当者名:
- 消費税: 税込表示 / 税別表示（10%）
- 主な取引内容・サービス名:
- 標準的な単価帯（おおよそ）:
```

---

## 見積書シートの cells 設計

**列幅設定:**
```json
"column_widths": {
  "A": 2, "B": 8, "C": 28, "D": 14, "E": 8, "F": 14, "G": 14, "H": 2
}
```

**行高設定:**
```json
"row_heights": {
  "1": 8, "2": 45, "3": 8, "4": 20, "5": 20, "6": 20, "7": 20,
  "8": 20, "9": 20, "10": 8, "11": 24, "12": 20,
  "13": 20, "14": 20, "15": 20, "16": 20, "17": 20, "18": 20,
  "19": 20, "20": 20, "21": 20, "22": 20, "23": 8,
  "24": 22, "25": 22, "26": 22, "27": 8,
  "28": 30, "29": 30
}
```

**cells 設計（主要セル）:**
```json
"cells": [
  {"cell": "B2", "value": "見 積 書", "merge": "B2:G2",
   "style": {"font_size": 22, "bold": true, "align": "center"}},

  {"cell": "B4", "value": "宛先:", "style": {"bold": true}},
  {"cell": "C4", "value": "[宛先会社名] 御中", "merge": "C4:E4",
   "style": {"font_size": 12, "bold": true, "border_bottom": true}},

  {"cell": "F4", "value": "見積番号:", "style": {"bold": true, "align": "right"}},
  {"cell": "G4", "value": "EST-2026-001"},

  {"cell": "F5", "value": "発行日:", "style": {"bold": true, "align": "right"}},
  {"cell": "G5", "value": "[発行日]", "style": {"format": "date"}},

  {"cell": "F6", "value": "有効期限:", "style": {"bold": true, "align": "right"}},
  {"cell": "G6", "value": "[有効期限（30日後など）]", "style": {"format": "date"}},

  {"cell": "B8", "value": "[自社名]", "merge": "B8:D8",
   "style": {"bold": true}},
  {"cell": "B9", "value": "〒[郵便番号] [住所]", "merge": "B9:D9"},
  {"cell": "B10", "value": "TEL: [電話番号]  Mail: [メール]", "merge": "B10:D10"},

  {"cell": "C11", "value": "件名:", "style": {"bold": true}},
  {"cell": "D11", "value": "[案件名・件名]", "merge": "D11:G11",
   "style": {"bold": true, "border_bottom": true}},

  {"cell": "B13", "value": "No.", "style": {"bold": true, "align": "center", "fill": "1E3A5F", "color": "FFFFFF", "border": true}},
  {"cell": "C13", "value": "品目・サービス内容", "style": {"bold": true, "align": "center", "fill": "1E3A5F", "color": "FFFFFF", "border": true}},
  {"cell": "D13", "value": "単価", "style": {"bold": true, "align": "center", "fill": "1E3A5F", "color": "FFFFFF", "border": true}},
  {"cell": "E13", "value": "数量", "style": {"bold": true, "align": "center", "fill": "1E3A5F", "color": "FFFFFF", "border": true}},
  {"cell": "F13", "value": "単位", "style": {"bold": true, "align": "center", "fill": "1E3A5F", "color": "FFFFFF", "border": true}},
  {"cell": "G13", "value": "金額", "style": {"bold": true, "align": "center", "fill": "1E3A5F", "color": "FFFFFF", "border": true}},

  {"cell": "B14", "value": 1, "style": {"align": "center", "border": true}},
  {"cell": "C14", "value": "[品目1]", "style": {"border": true}},
  {"cell": "D14", "value": 0, "style": {"format": "currency", "align": "right", "border": true}},
  {"cell": "E14", "value": 1, "style": {"align": "center", "border": true}},
  {"cell": "F14", "value": "式", "style": {"align": "center", "border": true}},
  {"cell": "G14", "formula": "=D14*E14", "style": {"format": "currency", "align": "right", "border": true}},

  {"cell": "B15", "value": 2, "style": {"align": "center", "border": true}},
  {"cell": "C15", "value": "[品目2]", "style": {"border": true}},
  {"cell": "D15", "value": 0, "style": {"format": "currency", "align": "right", "border": true}},
  {"cell": "E15", "value": 1, "style": {"align": "center", "border": true}},
  {"cell": "F15", "value": "式", "style": {"align": "center", "border": true}},
  {"cell": "G15", "formula": "=D15*E15", "style": {"format": "currency", "align": "right", "border": true}},

  {"cell": "B16", "value": 3, "style": {"align": "center", "border": true}},
  {"cell": "C16", "value": "[品目3]", "style": {"border": true}},
  {"cell": "D16", "value": 0, "style": {"format": "currency", "align": "right", "border": true}},
  {"cell": "E16", "value": 1, "style": {"align": "center", "border": true}},
  {"cell": "F16", "value": "式", "style": {"align": "center", "border": true}},
  {"cell": "G16", "formula": "=D16*E16", "style": {"format": "currency", "align": "right", "border": true}},

  {"cell": "F24", "value": "小計", "style": {"bold": true, "align": "right", "fill": "EEF2F7"}},
  {"cell": "G24", "formula": "=SUM(G14:G22)", "style": {"format": "currency", "align": "right", "border": true}},

  {"cell": "F25", "value": "消費税（10%）", "style": {"bold": true, "align": "right", "fill": "EEF2F7"}},
  {"cell": "G25", "formula": "=G24*0.1", "style": {"format": "currency", "align": "right", "border": true}},

  {"cell": "F26", "value": "合計（税込）", "style": {"bold": true, "align": "right", "fill": "1E3A5F", "color": "FFFFFF"}},
  {"cell": "G26", "formula": "=G24+G25", "style": {"format": "currency", "align": "right", "bold": true, "fill": "1E3A5F", "color": "FFFFFF", "border": true}},

  {"cell": "B28", "value": "備考:", "style": {"bold": true}},
  {"cell": "C28", "value": "・お振込の際は手数料をご負担ください。\n・本見積の有効期限は発行日より30日間です。",
   "merge": "C28:G29", "style": {"wrap": true, "valign": "top"}}
]
```

**merged_cells（merge をまとめて指定する場合）:**
```json
"merged_cells": ["B2:G2"]
```

---

## 請求書シート（cells 設計の要点）

見積書とほぼ同じレイアウト。以下を変更する：
- タイトル: `見 積 書` → `請 求 書`
- 見積番号 → 請求番号（例: `INV-2026-001`）
- 有効期限 → お支払期限
- 振込先情報を追加:
  ```json
  {"cell": "B28", "value": "お振込先", "style": {"bold": true}},
  {"cell": "C28", "value": "[銀行名] [支店名] 口座番号: [口座番号]  口座名義: [名義]",
   "merge": "C28:G28"}
  ```

---

## 経費精算書シート（テーブル型）

経費精算書はテーブル型で作成する（`columns` + `rows`）：

```json
{
  "name": "経費精算書",
  "tab_color": "E8700A",
  "title_row": {
    "text": "経費精算書",
    "subtitle": "[期間]  申請者: [氏名]  申請日: [日付]"
  },
  "info_rows": [
    {"label": "申請者", "value": "[氏名]"},
    {"label": "所属", "value": "[部署名]"},
    {"label": "申請日", "value": "[日付]"},
    {"label": "承認者", "value": ""}
  ],
  "columns": [
    {"header": "日付", "key": "date", "width": 12, "format": "date", "align": "center"},
    {"header": "費目", "key": "category", "width": 16,
     "dropdown": ["交通費", "宿泊費", "飲食費", "通信費", "消耗品費", "接待交際費", "その他"]},
    {"header": "内容・目的", "key": "description", "width": 30, "wrap": true},
    {"header": "訪問先・購入先", "key": "vendor", "width": 20},
    {"header": "金額（税込）", "key": "amount", "width": 16,
     "format": "currency", "align": "right", "summary": "sum"},
    {"header": "領収書", "key": "receipt", "width": 10, "align": "center",
     "dropdown": ["あり", "なし"],
     "conditional_formatting": [
       {"type": "contains", "value": "なし", "fill": "FFCCBC"}
     ]},
    {"header": "備考", "key": "remark", "width": 20}
  ],
  "rows": [],
  "empty_rows": 30
}
```

---

## 単価マスタシート（参照用テーブル）

references/ フォルダの過去データや web-researcher の相場情報をここに集約する：

```json
{
  "name": "単価マスタ",
  "tab_color": "4A90D9",
  "title_row": {"text": "単価マスタ（参照用）"},
  "columns": [
    {"header": "カテゴリ", "key": "category", "width": 18},
    {"header": "品目・サービス名", "key": "item", "width": 35},
    {"header": "標準単価", "key": "unit_price", "width": 16,
     "format": "currency", "align": "right"},
    {"header": "単位", "key": "unit", "width": 8, "align": "center"},
    {"header": "備考・出典", "key": "note", "width": 30}
  ],
  "rows": []
}
```

---

## references/ の活用方法

`references/` フォルダに過去の見積書・請求書 Excel が入っている場合：
1. ファイル名を確認して Read ツールで中身を確認する（直接読めない場合は python-openpyxl で読む）
2. 品目名・単価・消費税の扱い・レイアウトを参照する
3. 新しい帳票の `cells` 設計に反映する（特に単価マスタのデータとして活用）
