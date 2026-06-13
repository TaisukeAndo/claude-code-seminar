# タスク管理シート テンプレート仕様

プロジェクト・イベントのタスク管理Excel。
web-researcher でプロジェクト種別の一般的なタスク事例を調査した後、このテンプレートに沿って workbook.json を設計する。

---

## シート構成（推奨）

| シート名 | 内容 |
|----------|------|
| タスク一覧 | 全タスクの一覧・ステータス管理（メインシート） |
| 担当者別 | 担当者ごとのタスク集計（オプション） |
| 進捗サマリー | KPI・進捗率ダッシュボード（オプション） |

小規模プロジェクト（タスク30件以内）であればシート1枚（タスク一覧のみ）で十分。

---

## タスク一覧シートの列定義

```json
{
  "name": "タスク一覧",
  "tab_color": "1E3A5F",
  "title_row": {
    "text": "[プロジェクト名] タスク管理表",
    "subtitle": "[開始日] 〜 [終了日]  担当: [メンバー名]"
  },
  "info_rows": [
    {"label": "プロジェクト名", "value": "[プロジェクト名]"},
    {"label": "期間", "value": "[開始日] 〜 [終了日]"},
    {"label": "メンバー", "value": "[メンバー名をカンマ区切り]"},
    {"label": "更新日", "value": "[今日の日付]"}
  ],
  "columns": [
    {"header": "No.", "key": "no", "width": 5, "align": "center"},
    {"header": "フェーズ", "key": "phase", "width": 16,
     "dropdown": ["計画", "準備", "実行", "クロージング"],
     "conditional_formatting": [
       {"type": "contains", "value": "計画", "fill": "E3F2FD"},
       {"type": "contains", "value": "準備", "fill": "FFF3E0"},
       {"type": "contains", "value": "実行", "fill": "E8F5E9"},
       {"type": "contains", "value": "クロージング", "fill": "F3E5F5"}
     ]},
    {"header": "タスク名", "key": "task", "width": 38},
    {"header": "詳細・メモ", "key": "notes", "width": 30, "wrap": true},
    {"header": "担当者", "key": "assignee", "width": 12,
     "dropdown": "[メンバー名の配列]"},
    {"header": "開始日", "key": "start_date", "width": 12, "format": "date", "align": "center"},
    {"header": "期限", "key": "due_date", "width": 12, "format": "date", "align": "center"},
    {"header": "ステータス", "key": "status", "width": 14, "align": "center",
     "dropdown": ["未着手", "進行中", "完了", "保留", "キャンセル"],
     "conditional_formatting": [
       {"type": "contains", "value": "完了", "fill": "C8E6C9", "font_color": "1B5E20"},
       {"type": "contains", "value": "進行中", "fill": "FFF9C4", "font_color": "F57F17"},
       {"type": "contains", "value": "保留", "fill": "FFCCBC", "font_color": "BF360C"},
       {"type": "contains", "value": "キャンセル", "fill": "ECEFF1", "font_color": "90A4AE"}
     ]},
    {"header": "優先度", "key": "priority", "width": 10, "align": "center",
     "dropdown": ["高", "中", "低"],
     "conditional_formatting": [
       {"type": "contains", "value": "高", "fill": "FFEBEE", "font_color": "C62828"},
       {"type": "contains", "value": "中", "fill": "FFF8E1", "font_color": "E65100"},
       {"type": "contains", "value": "低", "fill": "F1F8E9", "font_color": "33691E"}
     ]},
    {"header": "進捗", "key": "progress", "width": 10, "format": "percent", "align": "center",
     "conditional_formatting": [{"type": "data_bar"}]},
    {"header": "備考", "key": "remark", "width": 20, "wrap": true}
  ],
  "rows": [],
  "empty_rows": 40
}
```

---

## フェーズ設計の目安

web-researcher の調査結果をもとにフェーズを決定する。
以下は汎用的なフェーズ例：

| フェーズ | タスク例（担当が研究した事例を参考に展開） |
|----------|------------------------------------------|
| 計画 | 目標設定、予算確定、スケジュール策定、メンバーアサイン |
| 準備 | 会場手配、資料作成、ベンダー選定、告知・集客 |
| 実行 | 当日オペレーション、記録、対応・フォロー |
| クロージング | 振り返り、報告書、精算、次回への引継ぎ |

---

## rows の設計方針

- web-researcher が返した `key_findings` の各タスクを `rows` に展開する
- フェーズ順に並べる（計画 → 準備 → 実行 → クロージング）
- 各タスクの期限は、プロジェクトの期間を元にバックキャスティングで設定する
- タスク数は最低20件以上になるよう展開する（大タスクは分解する）
- `empty_rows` は残りの余白行数（20〜30行程度）

---

## 担当者別シート（オプション）

チームが3名以上いる場合に追加する：

```json
{
  "name": "担当者別",
  "tab_color": "4A90D9",
  "title_row": {"text": "担当者別タスク集計"},
  "columns": [
    {"header": "担当者", "key": "assignee", "width": 15},
    {"header": "総タスク数", "key": "total", "width": 12, "align": "center", "summary": "sum"},
    {"header": "完了", "key": "done", "width": 10, "align": "center", "summary": "sum"},
    {"header": "進行中", "key": "in_progress", "width": 10, "align": "center"},
    {"header": "未着手", "key": "todo", "width": 10, "align": "center"},
    {"header": "完了率", "key": "rate", "width": 10, "format": "percent",
     "formula": "={col:done}{row}/{col:total}{row}",
     "conditional_formatting": [{"type": "data_bar"}]}
  ],
  "rows": []
}
```
