#!/usr/bin/env python3
"""
invoice-creator: document.json + .env + clients/*.json → マネーフォワード クラウド請求書 CSV

対応: マネーフォワード クラウド請求書（請求書・見積書・領収書）
CSV インポート形式: マネーフォワード クラウド請求書 の「CSVインポート」機能に対応
※ マネーフォワードのバージョンによって列順が異なる場合があります。
   インポート前にマネーフォワードの設定画面でCSVフォーマットを確認してください。
"""

import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import (
    load_env, get_config, load_client, load_document, calc_items,
    format_date_slash, today_str,
)

# マネーフォワード クラウド請求書 CSV列定義（見積書・請求書共通）
# 参考: https://support.biz.moneyforward.com/invoice/guide/csv-import/
MF_INVOICE_COLUMNS = [
    "取引先名",
    "件名",
    "請求書番号",
    "発行日",
    "支払期日",
    "品目",
    "数量",
    "単位",
    "単価",
    "税区分",
    "摘要",
    "備考",
    "振込先",
]

# マネーフォワード 領収書CSV列定義
MF_RECEIPT_COLUMNS = [
    "取引先名",
    "領収書番号",
    "発行日",
    "金額（税込）",
    "内訳（税抜）",
    "消費税額",
    "但し書き",
    "備考",
]

TAX_CATEGORY_MAP = {
    10: "課税（10%）",
    8: "課税（8%）軽減",
    0: "不課税",
}


def generate_invoice_csv(doc: dict, config: dict, client: dict, out_path: str):
    doc_type = doc.get("document_type", "invoice")
    items, subtotal, tax_total, total = calc_items(doc.get("items", []))

    company = config["company"]
    bank = config["bank"]
    bank_str = ""
    if bank.get("name"):
        bank_str = f"{bank['name']} {bank['branch']} {bank['type']}預金 {bank['number']} {bank['holder']}"

    issue_date = format_date_slash(doc.get("issue_date") or today_str())
    due_date = format_date_slash(doc.get("due_date", "")) if doc_type == "invoice" else ""

    rows = []
    for item in items:
        tax_label = TAX_CATEGORY_MAP.get(item.get("tax_rate", 10), "課税（10%）")
        rows.append({
            "取引先名": client.get("name", ""),
            "件名": doc.get("title", ""),
            "請求書番号": doc.get("document_number", ""),
            "発行日": issue_date,
            "支払期日": due_date,
            "品目": item.get("name", ""),
            "数量": item.get("quantity", 1),
            "単位": item.get("unit", ""),
            "単価": item.get("unit_price", 0),
            "税区分": tax_label,
            "摘要": item.get("notes", ""),
            "備考": doc.get("notes", "") if item == items[-1] else "",
            "振込先": bank_str if item == items[-1] and doc_type == "invoice" else "",
        })

    _write_csv(out_path, MF_INVOICE_COLUMNS, rows)
    doc_label = "見積書" if doc_type == "estimate" else "請求書"
    print(f"✅ {doc_label}（マネーフォワード CSV）生成完了: {out_path}")
    print(f"   マネーフォワード クラウド請求書 > 請求書一覧 > CSVインポート からインポートしてください")


def generate_receipt_csv(doc: dict, config: dict, client: dict, out_path: str):
    total_amount = doc.get("total_amount", 0)
    tax_amount = doc.get("tax_amount", 0)
    subtotal_amount = doc.get("subtotal_amount", total_amount - tax_amount)

    issue_date = format_date_slash(doc.get("issue_date") or today_str())

    rows = [{
        "取引先名": client.get("name", ""),
        "領収書番号": doc.get("document_number", ""),
        "発行日": issue_date,
        "金額（税込）": total_amount,
        "内訳（税抜）": subtotal_amount,
        "消費税額": tax_amount,
        "但し書き": doc.get("title", ""),
        "備考": doc.get("notes", ""),
    }]

    _write_csv(out_path, MF_RECEIPT_COLUMNS, rows)
    print(f"✅ 領収書（マネーフォワード CSV）生成完了: {out_path}")
    print(f"   マネーフォワード クラウド請求書 > 領収書一覧 > CSVインポート からインポートしてください")


def _write_csv(out_path: str, columns: list, rows: list):
    with open(out_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def main():
    if len(sys.argv) < 3:
        print("使い方: python3 generate_moneyforward.py <document.json> <output.csv>")
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
    else:
        generate_invoice_csv(doc, config, client, out_path)


if __name__ == "__main__":
    main()
