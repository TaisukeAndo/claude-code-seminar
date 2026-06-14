#!/usr/bin/env python3
"""
MoneyForward クラウド請求書 API 経由で書類を作成し PDF をダウンロードする。
LLM は document.json（PII なし）を渡すだけ。
自社情報・銀行口座・取引先情報は .env / clients/*.json から実行時に取得。

使い方:
  python3 mf_api_create.py <document.json> [--open]

オプション:
  --open  生成後に PDF を自動で開く（Mac）
"""

import json
import sys
import subprocess
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from mf_api_client import (
    MoneyForwardClient,
    MoneyForwardAPIError,
    doc_to_invoice_payload,
    doc_to_quotation_payload,
    doc_to_receipt_payload,
)
from common import load_document, SKILL_DIR

CLIENTS_DIR = SKILL_DIR / "clients"


def load_client_json(client_id: str) -> dict:
    """clients/*.json から取引先情報を読み込む"""
    f = CLIENTS_DIR / f"{client_id}.json"
    if not f.exists():
        available = [p.stem for p in CLIENTS_DIR.glob("*.json")] if CLIENTS_DIR.exists() else []
        print(f"エラー: clients/{client_id}.json が見つかりません", file=sys.stderr)
        print(f"  利用可能: {available}", file=sys.stderr)
        sys.exit(1)
    return json.loads(f.read_text(encoding="utf-8"))


def resolve_partner_id(mf: MoneyForwardClient, doc: dict) -> str:
    """
    clients/*.json に mf_partner_id が記録されていればそれを使う。
    なければ MoneyForward API で取引先名を検索して取得し、
    clients/*.json に mf_partner_id を書き戻す。
    """
    client_id = doc.get("client_id", "")
    client_json = load_client_json(client_id)

    # キャッシュがあればそのまま使う
    if partner_id := client_json.get("mf_partner_id", ""):
        return partner_id

    # API で取引先を検索
    client_name = client_json.get("name", "")
    print(f"取引先 '{client_name}' を MoneyForward で検索中...")
    partner = mf.find_partner(client_name)

    if partner:
        partner_id = partner["id"]
        print(f"  → 既存の取引先を発見: {partner_id}")
    else:
        # 存在しない場合は新規作成
        print(f"  → 取引先が見つかりません。新規作成します: {client_name}")
        result = mf._post("/partners", {
            "partner": {
                "name": client_name,
                "name_kana": client_json.get("name_kana", ""),
                "zip": client_json.get("zip", ""),
                "address": client_json.get("address", ""),
                "tel": client_json.get("tel", ""),
                "email": client_json.get("email", ""),
            }
        })
        partner_id = result["data"]["id"]
        print(f"  → 新規取引先作成: {partner_id}")

    # clients/*.json に mf_partner_id を保存（次回から API 検索を省略）
    client_json["mf_partner_id"] = partner_id
    client_file = CLIENTS_DIR / f"{client_id}.json"
    client_file.write_text(json.dumps(client_json, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  → clients/{client_id}.json に mf_partner_id を保存しました")

    return partner_id


def create_and_download(doc_path: str, auto_open: bool = False) -> str:
    """document.json を読み込み、MF API で書類を作成して PDF をダウンロードする"""
    doc = load_document(doc_path)
    doc_type = doc.get("document_type", "invoice")
    mf = MoneyForwardClient()

    # 取引先 ID を解決
    partner_id = resolve_partner_id(mf, doc)

    print(f"\n[1/3] MoneyForward に {_type_label(doc_type)} を作成中...")

    if doc_type == "invoice":
        payload = doc_to_invoice_payload(doc, partner_id)
        result = mf.create_invoice(payload)
        record_id = result["data"]["id"]
        pdf_bytes = mf.get_invoice_pdf(record_id)

    elif doc_type == "estimate":
        payload = doc_to_quotation_payload(doc, partner_id)
        result = mf.create_quotation(payload)
        record_id = result["data"]["id"]
        pdf_bytes = mf.get_quotation_pdf(record_id)

    elif doc_type == "receipt":
        payload = doc_to_receipt_payload(doc, partner_id)
        result = mf.create_receipt(payload)
        record_id = result["data"]["id"]
        pdf_bytes = mf.get_receipt_pdf(record_id)

    else:
        print(f"エラー: 未対応の document_type: {doc_type}", file=sys.stderr)
        sys.exit(1)

    attrs = result.get("data", {}).get("attributes", {})
    total = attrs.get("total_amount_with_tax", attrs.get("total_amount", "?"))
    print(f"  → 作成完了: ID={record_id}  合計={total:,}円" if isinstance(total, int) else f"  → 作成完了: ID={record_id}")

    # PDF 保存
    print(f"[2/3] PDF をダウンロード中...")
    doc_number = doc.get("document_number", record_id)
    out_name = f"{_type_label(doc_type)}_{doc_number}.pdf"
    out_path = Path("/tmp") / out_name
    out_path.write_bytes(pdf_bytes)
    print(f"  → 保存先: {out_path}")

    # 自動で開く
    if auto_open:
        print(f"[3/3] PDF を開いています...")
        subprocess.run(["open", str(out_path)], check=False)
    else:
        print(f"[3/3] 完了（自動で開くには --open オプションを追加）")

    print(f"\n✅ {_type_label(doc_type)} の作成・ダウンロード完了")
    print(f"   MoneyForward ID: {record_id}")
    print(f"   PDF: {out_path}")

    return str(out_path)


def _type_label(doc_type: str) -> str:
    return {"invoice": "請求書", "estimate": "見積書", "receipt": "領収書"}.get(doc_type, doc_type)


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)

    doc_path = args[0]
    auto_open = "--open" in args

    try:
        create_and_download(doc_path, auto_open)
    except MoneyForwardAPIError as e:
        print(f"\nAPI エラー: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
