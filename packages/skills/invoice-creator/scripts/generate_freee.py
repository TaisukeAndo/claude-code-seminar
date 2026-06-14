#!/usr/bin/env python3
"""
invoice-creator: document.json + .env + clients/*.json → freee CSV

対応: freee 会計 / freee 請求書
CSV インポート形式: freee の「取引のインポート」および「請求書のCSV出力」に準拠
※ freee のバージョン・プランによって対応列が異なる場合があります。
   インポート前に freee のヘルプページでフォーマットを確認してください。
   参考: https://support.freee.co.jp/hc/ja/articles/202848880
"""

import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import (
    load_env, get_config, load_client, load_document, calc_items,
    format_date_slash, today_str,
)

# freee 請求書 CSV 列定義
# freee では請求書を「取引」としてインポートする形式が一般的
FREEE_INVOICE_COLUMNS = [
    "発生日",
    "収支区分",
    "取引先",
    "勘定科目",
    "税区分",
    "金額",
    "税計算区分",
    "税額",
    "備考",
    "品目",
    "部門",
    "メモタグ（複数指定可、カンマ区切り）",
    "口座",
    "入金・支払日",
    "入金・支払口座",
    "請求書番号",
    "件名",
    "期日",
]

# freee 見積書 CSV 列定義
FREEE_ESTIMATE_COLUMNS = [
    "見積日",
    "見積書番号",
    "取引先",
    "件名",
    "品目",
    "数量",
    "単位",
    "単価",
    "消費税率",
    "メモ",
]

# freee 領収書（収入取引）CSV 列定義
FREEE_RECEIPT_COLUMNS = [
    "発生日",
    "収支区分",
    "取引先",
    "勘定科目",
    "税区分",
    "金額",
    "税計算区分",
    "税額",
    "備考",
    "品目",
]

TAX_CATEGORY_MAP = {
    10: "課税売上10%",
    8: "課税売上8%（軽減）",
    0: "不課税売上",
}


def generate_invoice_csv(doc: dict, config: dict, client: dict, out_path: str):
    items, subtotal, tax_total, total = calc_items(doc.get("items", []))
    issue_date = format_date_slash(doc.get("issue_date") or today_str())
    due_date = format_date_slash(doc.get("due_date", ""))

    rows = []
    for i, item in enumerate(items):
        tax_label = TAX_CATEGORY_MAP.get(item.get("tax_rate", 10), "課税売上10%")
        rows.append({
            "発生日": issue_date,
            "収支区分": "収入",
            "取引先": client.get("name", ""),
            "勘定科目": "売上高",
            "税区分": tax_label,
            "金額": item.get("amount", 0),
            "税計算区分": "内税" if doc.get("tax_calculation") == "inclusive" else "外税",
            "税額": item.get("tax", 0),
            "備考": doc.get("notes", "") if i == 0 else "",
            "品目": item.get("name", ""),
            "部門": "",
            "メモタグ（複数指定可、カンマ区切り）": "",
            "口座": "",
            "入金・支払日": "",
            "入金・支払口座": "",
            "請求書番号": doc.get("document_number", "") if i == 0 else "",
            "件名": doc.get("title", "") if i == 0 else "",
            "期日": due_date if i == 0 else "",
        })

    _write_csv(out_path, FREEE_INVOICE_COLUMNS, rows)
    print(f"✅ 請求書（freee CSV）生成完了: {out_path}")
    print(f"   freee > 取引 > インポート > 取引のインポート からインポートしてください")


def generate_estimate_csv(doc: dict, config: dict, client: dict, out_path: str):
    items, _, _, _ = calc_items(doc.get("items", []))
    issue_date = format_date_slash(doc.get("issue_date") or today_str())

    rows = []
    for i, item in enumerate(items):
        rows.append({
            "見積日": issue_date if i == 0 else "",
            "見積書番号": doc.get("document_number", "") if i == 0 else "",
            "取引先": client.get("name", "") if i == 0 else "",
            "件名": doc.get("title", "") if i == 0 else "",
            "品目": item.get("name", ""),
            "数量": item.get("quantity", 1),
            "単位": item.get("unit", ""),
            "単価": item.get("unit_price", 0),
            "消費税率": f"{item.get('tax_rate', 10)}%",
            "メモ": doc.get("notes", "") if i == len(items) - 1 else "",
        })

    _write_csv(out_path, FREEE_ESTIMATE_COLUMNS, rows)
    print(f"✅ 見積書（freee CSV）生成完了: {out_path}")
    print(f"   freee > 見積書 > 新規作成 > CSVインポート からインポートしてください")


def generate_receipt_csv(doc: dict, config: dict, client: dict, out_path: str):
    total_amount = doc.get("total_amount", 0)
    tax_amount = doc.get("tax_amount", 0)
    subtotal_amount = doc.get("subtotal_amount", total_amount - tax_amount)
    issue_date = format_date_slash(doc.get("issue_date") or today_str())

    rows = [{
        "発生日": issue_date,
        "収支区分": "収入",
        "取引先": client.get("name", ""),
        "勘定科目": "売上高",
        "税区分": "課税売上10%",
        "金額": subtotal_amount,
        "税計算区分": "外税",
        "税額": tax_amount,
        "備考": doc.get("title", ""),
        "品目": doc.get("notes", ""),
    }]

    _write_csv(out_path, FREEE_RECEIPT_COLUMNS, rows)
    print(f"✅ 領収書（freee CSV）生成完了: {out_path}")
    print(f"   freee > 取引 > インポート > 取引のインポート からインポートしてください")


def _write_csv(out_path: str, columns: list, rows: list):
    with open(out_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main():
    if len(sys.argv) < 3:
        print("使い方: python3 generate_freee.py <document.json> <output.csv>")
        sys.exit(1)

    doc_path = sys.argv[1]
    out_path = sys.argv[2]

    env = load_env()
    config = get_config(env)
    doc = load_document(doc_path)
    client = load_client(doc.get("client_id", ""))

    doc_type = doc.get("document_type", "invoice")
    if doc_type == "receipt":
        generate_receipt_csv(doc, config, client, out_path)
    elif doc_type == "estimate":
        generate_estimate_csv(doc, config, client, out_path)
    else:
        generate_invoice_csv(doc, config, client, out_path)


if __name__ == "__main__":
    main()
