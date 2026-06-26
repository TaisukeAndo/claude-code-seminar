# KPI・マーケティング・実績管理シート テンプレート仕様

マーケティング施策のKPI管理、実績追跡、データ分析を行うExcel。
web-researcher で業界ベンチマーク・成功事例・平均値を調査した後、このテンプレートに沿って workbook.json を設計する。

---

## シート構成（推奨）

| シート名 | 内容 |
|----------|------|
| KPIサマリー | 主要KPIの目標vs実績ダッシュボード（メインシート） |
| 月次実績 | 月別の詳細データ入力シート |
| 施策管理 | 施策ごとの効果測定（オプション） |

---

## KPIサマリーシートの列定義

KPIの数と種類はヒアリングと web-researcher の結果で決定する。

```json
{
  "name": "KPIサマリー",
  "tab_color": "1E3A5F",
  "title_row": {
    "text": "[業種・サービス名] KPI管理表",
    "subtitle": "[計測期間]  作成日: [日付]"
  },
  "info_rows": [
    {"label": "サービス名", "value": "[サービス・プロジェクト名]"},
    {"label": "計測期間", "value": "[開始月] 〜 [終了月]"},
    {"label": "更新頻度", "value": "月次 / 週次 / 日次"},
    {"label": "担当者", "value": "[担当者名]"}
  ],
  "columns": [
    {"header": "KPI名", "key": "kpi_name", "width": 28},
    {"header": "カテゴリ", "key": "category", "width": 16,
     "dropdown": ["集客", "エンゲージメント", "コンバージョン", "売上", "顧客維持"],
     "conditional_formatting": [
       {"type": "contains", "value": "コンバージョン", "fill": "E8F5E9"},
       {"type": "contains", "value": "売上", "fill": "FFF3E0"}
     ]},
    {"header": "単位", "key": "unit", "width": 10, "align": "center"},
    {"header": "年間目標", "key": "annual_target", "width": 14, "format": "number", "align": "right"},
    {"header": "今月目標", "key": "monthly_target", "width": 14, "format": "number", "align": "right"},
    {"header": "今月実績", "key": "monthly_actual", "width": 14, "format": "number", "align": "right"},
    {"header": "達成率", "key": "achievement_rate", "width": 12, "format": "percent", "align": "center",
     "formula": "=IF({col:monthly_target}{row}=0,\"\",{col:monthly_actual}{row}/{col:monthly_target}{row})",
     "conditional_formatting": [
       {"type": "data_bar", "color": "4A90D9"}
     ]},
    {"header": "前月比", "key": "mom_rate", "width": 10, "format": "percent", "align": "center"},
    {"header": "業界平均", "key": "industry_avg", "width": 14, "format": "number", "align": "right"},
    {"header": "出典・メモ", "key": "source_note", "width": 24, "wrap": true},
    {"header": "ステータス", "key": "status", "width": 14, "align": "center",
     "dropdown": ["目標達成", "順調", "要注意", "未集計"],
     "conditional_formatting": [
       {"type": "contains", "value": "目標達成", "fill": "C8E6C9", "font_color": "1B5E20"},
       {"type": "contains", "value": "順調", "fill": "DCEDC8"},
       {"type": "contains", "value": "要注意", "fill": "FFCCBC", "font_color": "BF360C"},
       {"type": "contains", "value": "未集計", "fill": "ECEFF1", "font_color": "90A4AE"}
     ]}
  ],
  "rows": [],
  "empty_rows": 20
}
```

---

## 月次実績シートの列定義

```json
{
  "name": "月次実績",
  "tab_color": "4A90D9",
  "title_row": {"text": "月次実績データ"},
  "columns": [
    {"header": "月", "key": "month", "width": 10, "format": "date_short", "align": "center"},
    {"header": "KPI名", "key": "kpi_name", "width": 28},
    {"header": "目標値", "key": "target", "width": 14, "format": "number", "align": "right"},
    {"header": "実績値", "key": "actual", "width": 14, "format": "number", "align": "right",
     "summary": "sum"},
    {"header": "達成率", "key": "rate", "width": 12, "format": "percent", "align": "center",
     "formula": "=IF({col:target}{row}=0,\"\",{col:actual}{row}/{col:target}{row})",
     "conditional_formatting": [{"type": "data_bar"}]},
    {"header": "前月差", "key": "diff", "width": 12, "format": "number", "align": "right"},
    {"header": "備考", "key": "remark", "width": 24, "wrap": true}
  ],
  "rows": [],
  "empty_rows": 50
}
```

---

## rows の設計方針（KPIサマリー）

web-researcher の結果をもとに、業界平均・ベンチマーク値を `industry_avg` に設定する。

KPI例（業種・目的に合わせて選択する）:

| カテゴリ | KPI例 | 単位 |
|----------|-------|------|
| 集客 | ウェブサイト訪問数, SNSフォロワー数, 広告インプレッション | 件/人 |
| エンゲージメント | 滞在時間, 開封率, エンゲージメント率 | 秒/% |
| コンバージョン | リード獲得数, 商談件数, 成約件数, CVR | 件/% |
| 売上 | 売上金額, 平均受注単価, 顧客単価 | 円 |
| 顧客維持 | リピート率, 解約率, NPS | % |

目標値の設定は：
1. web-researcher の業界平均を `industry_avg` に設定
2. 初月は控えめ（業界平均の70〜80%）を `annual_target` の目安として提示
3. ユーザーに最終確認を求める（「目標値はこの数値でよいですか？」）

---

## 施策管理シート（オプション）

施策の一覧と効果測定を管理する：

```json
{
  "name": "施策管理",
  "tab_color": "E8700A",
  "title_row": {"text": "施策・キャンペーン管理"},
  "columns": [
    {"header": "施策名", "key": "action", "width": 30},
    {"header": "チャネル", "key": "channel", "width": 16,
     "dropdown": ["SNS", "メール", "検索広告", "展示会", "ウェビナー", "その他"]},
    {"header": "開始日", "key": "start", "width": 12, "format": "date", "align": "center"},
    {"header": "終了日", "key": "end", "width": 12, "format": "date", "align": "center"},
    {"header": "予算", "key": "budget", "width": 14, "format": "currency", "align": "right", "summary": "sum"},
    {"header": "実績コスト", "key": "actual_cost", "width": 14, "format": "currency", "align": "right", "summary": "sum"},
    {"header": "獲得リード数", "key": "leads", "width": 14, "format": "number", "align": "right", "summary": "sum"},
    {"header": "CPL", "key": "cpl", "width": 12, "format": "currency",
     "formula": "=IF({col:leads}{row}=0,\"\",{col:actual_cost}{row}/{col:leads}{row})"},
    {"header": "評価", "key": "eval", "width": 12, "align": "center",
     "dropdown": ["◎ 優秀", "○ 良好", "△ 改善余地", "✕ 不採用"]}
  ],
  "rows": [],
  "empty_rows": 20
}
```
