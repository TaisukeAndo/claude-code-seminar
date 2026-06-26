#!/usr/bin/env python3
"""
invoice-creator: document.json + .env + clients/*.json → 弥生会計 CSV

対応: 弥生会計 デスクトップ版（弥生会計 24 / 23 / 22）
     弥生会計 オンライン（一部対応）
CSV インポート形式: 弥生インポート形式（仕訳日記帳）
     + 弥生 売上・仕入伝票形式（請求書・見積書用）

※ 弥生製品のバージョンによってフォーマットが異なる場合があります。
   インポート前に弥生サポートページでご確認ください。
   参考: https://www.yayoi-kk.co.jp/support/
"""

import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import (
    load_env, get_config, load_client, load_document, calc_items,
    format_date_slash, today_str,
)

# 弥生会計 仕訳インポート形式（標準仕訳帳 CSV）
YAYOI_JOURNAL_COLUMNS = [
    "伝票No",
    "年月日",
    "借方勘定科目",
    "借方補助科目",
    "借方部門",
    "借方税区分",
    "借方金額",
    "借方税額",
    "貸方勘定科目",
    "貸方補助科目",
    "貸方部門",
    "貸方税区分",
    "貸方金額",
    "貸方税額",
    "摘要",
    "番号",
    "型",
    "決算",
]

# 弥生 売上伝票 CSV 形式（受注・売上管理）
YAYOI_SALES_COLUMNS = [
    "伝票日付",
    "伝票番号",
    "得意先コード",
    "得意先名",
    "品番",
    "品名",
    "数量",
    "単位",
    "単価",
    "金額",
    "消費税額",
    "税区分",
    "摘要",
    "備考",
]

TAX_CODE_MAP = {
    10: "課税売上10%",
    8: "課税売上8%",
    0: "不課税",
}

YAYOI_TAX_CODE_MAP = {
    10: "11",  # 課税売上 10%
    8: "17",   # 軽減税率 8%
    0: "0",    # 不課税
}


def generate_journal_csv(doc: dict, config: dict, client: dict, out_path: str):
    """
    弥生会計 標準仕訳インポート形式で出力する。
    売上の計上仕訳（売掛金 / 売上高）を生成する。
    """
    items, subtotal, tax_total, total = calc_items(doc.get("items", []))
    issue_date = format_date_slash(doc.get("issue_date") or today_str())
    doc_number = doc.get("document_number", "")
    client_name = client.get("name", "")
    doc_title = doc.get("title", "")

    rows = []
    for i, item in enumerate(items):
        tax_rate = item.get("tax_rate", 10)
        tax_code = YAYOI_TAX_CODE_MAP.get(tax_rate, "11")
        rows.append({
            "伝票No": doc_number,
            "年月日": issue_date,
            "借方勘定科目": "売掛金",
            "借方補助科目": client_name,
            "借方部門": "",
            "借方税区分": "",
            "借方金額": item.get("amount_with_tax", 0),
            "借方税額": 0,
            "貸方勘定科目": "売上高",
            "貸方補助科目": "",
            "貸方部門": "",
            "貸方税区分": tax_code,
            "貸方金額": item.get("amount", 0),
            "貸方税額": item.get("tax", 0),
            "摘要": f"{client_name}　{doc_title}　{item.get('name', '')}",
            "番号": "",
            "型": "0",
            "決算": "0",
        })

    _write_csv_yayoi(out_path, YAYOI_JOURNAL_COLUMNS, rows)
    doc_label = {"estimate": "見積書", "invoice": "請求書", "receipt": "領収書"}.get(
        doc.get("document_type", "invoice"), "請求書"
    )
    print(f"✅ {doc_label}（弥生会計 仕訳CSV）生成完了: {out_path}")
    print(f"   弥生会計 > ファイル > インポート > 仕訳日記帳 からインポートしてください")
    print(f"   ※ 文字コード: UTF-8（BOM付き）を選択してください")


def generate_sales_csv(doc: dict, config: dict, client: dict, out_path: str):
    """
    弥生 売上伝票 CSV 形式で出力する（弥生販売・農業簿記対応）。
    """
    items, subtotal, tax_total, total = calc_items(doc.get("items", []))
    issue_date = format_date_slash(doc.get("issue_date") or today_str())
    doc_number = doc.get("document_number", "")
    client_name = client.get("name", "")

    rows = []
    for i, item in enumerate(items):
        tax_rate = item.get("tax_rate", 10)
        tax_label = TAX_CODE_MAP.get(tax_rate, "課税売上10%")
        rows.append({
            "伝票日付": issue_date,
            "伝票番号": doc_number,
            "得意先コード": client.get("id", ""),
            "得意先名": client_name,
            "品番": item.get("item_code", ""),
            "品名": item.get("name", ""),
            "数量": item.get("quantity", 1),
            "単位": item.get("unit", ""),
            "単価": item.get("unit_price", 0),
            "金額": item.get("amount", 0),
            "消費税額": item.get("tax", 0),
            "税区分": tax_label,
            "摘要": doc.get("title", ""),
            "備考": doc.get("notes", "") if i == len(items) - 1 else "",
        })

    _write_csv_yayoi(out_path, YAYOI_SALES_COLUMNS, rows)
    doc_label = {"estimate": "見積書", "invoice": "請求書", "receipt": "領収書"}.get(
        doc.get("document_type", "invoice"), "請求書"
    )
    print(f"✅ {doc_label}（弥生 売上伝票CSV）生成完了: {out_path}")
    print(f"   弥生販売 / 弥生会計 > ファイル > インポート からインポートしてください")


def _write_csv_yayoi(out_path: str, columns: list, rows: list):
    """弥生インポート用 CSV（UTF-8 BOM付き）を書き出す"""
    with open(out_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main():
    if len(sys.argv) < 3:
        print("使い方: python3 generate_yayoi.py <document.json> <output.csv> [journal|sales]")
        print("  journal: 仕訳インポート形式（デフォルト）")
        print("  sales:   売上伝票形式")
        sys.exit(1)

    doc_path = sys.argv[1]
    out_path = sys.argv[2]
    mode = sys.argv[3] if len(sys.argv) > 3 else "journal"

    env = load_env()
    config = get_config(env)
    doc = load_document(doc_path)
    client = load_client(doc.get("client_id", ""))

    if mode == "sales":
        generate_sales_csv(doc, config, client, out_path)
    else:
        generate_journal_csv(doc, config, client, out_path)


if __name__ == "__main__":
    main()
