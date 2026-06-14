#!/usr/bin/env python3
"""invoice-creator: 共通ユーティリティ（.env / clients/*.json の読み込み）"""

import json
import sys
from pathlib import Path
from datetime import datetime, date

SKILL_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = SKILL_DIR / "assets"
CLIENTS_DIR = SKILL_DIR / "clients"


def load_env() -> dict:
    """
    .env ファイルをスキルディレクトリから読み込む。
    LLM には渡されず、Python 実行時にのみ読み込まれる。
    """
    env_file = SKILL_DIR / ".env"
    if not env_file.exists():
        print(f"エラー: .envファイルが見つかりません: {env_file}", file=sys.stderr)
        print("  .env.example を参考に .env を作成し、自社情報を記入してください。", file=sys.stderr)
        sys.exit(1)

    result = {}
    with open(env_file, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, _, value = line.partition("=")
                result[key.strip()] = value.strip().strip('"').strip("'")
    return result


def get_config(env: dict) -> dict:
    """env dict から構造化した設定を返す"""
    return {
        "company": {
            "name": env.get("MY_COMPANY_NAME", ""),
            "zip": env.get("MY_COMPANY_ZIP", ""),
            "address": env.get("MY_COMPANY_ADDRESS", ""),
            "tel": env.get("MY_COMPANY_TEL", ""),
            "fax": env.get("MY_COMPANY_FAX", ""),
            "email": env.get("MY_COMPANY_EMAIL", ""),
            "registration_number": env.get("MY_REGISTRATION_NUMBER", ""),
            "corporate_number": env.get("MY_CORPORATE_NUMBER", ""),
            "representative": env.get("MY_REPRESENTATIVE_NAME", ""),
            "representative_title": env.get("MY_REPRESENTATIVE_TITLE", "代表取締役"),
            "seal_image": env.get("MY_SEAL_IMAGE", "seal.png"),
            "logo_image": env.get("MY_LOGO_IMAGE", "logo.png"),
        },
        "bank": {
            "name": env.get("BANK_NAME", ""),
            "branch": env.get("BANK_BRANCH", ""),
            "type": env.get("BANK_TYPE", "普通"),
            "number": env.get("BANK_NUMBER", ""),
            "holder": env.get("BANK_HOLDER", ""),
        },
        "bank2": {
            "name": env.get("BANK2_NAME", ""),
            "branch": env.get("BANK2_BRANCH", ""),
            "type": env.get("BANK2_TYPE", "普通"),
            "number": env.get("BANK2_NUMBER", ""),
            "holder": env.get("BANK2_HOLDER", ""),
        },
        "defaults": {
            "tax_calculation": env.get("DEFAULT_TAX_CALCULATION", "exclusive"),
            "tax_rate": int(env.get("DEFAULT_TAX_RATE", "10")),
        },
    }


def load_client(client_id: str) -> dict:
    """clients/ ディレクトリから取引先情報を読み込む"""
    if not client_id:
        print("エラー: client_id が指定されていません", file=sys.stderr)
        sys.exit(1)

    # 直接ファイル名で検索
    client_file = CLIENTS_DIR / f"{client_id}.json"
    if client_file.exists():
        with open(client_file, encoding="utf-8") as f:
            return json.load(f)

    # name または id フィールドで検索
    if CLIENTS_DIR.exists():
        for f in CLIENTS_DIR.glob("*.json"):
            try:
                data = json.loads(f.read_text(encoding="utf-8"))
                if data.get("name") == client_id or data.get("id") == client_id:
                    return data
            except Exception:
                continue

    available = [f.stem for f in CLIENTS_DIR.glob("*.json")] if CLIENTS_DIR.exists() else []
    print(f"エラー: 取引先 '{client_id}' が見つかりません", file=sys.stderr)
    print(f"  利用可能: {available}", file=sys.stderr)
    print(f"  clients/ フォルダに {client_id}.json を作成してください", file=sys.stderr)
    sys.exit(1)


def load_document(path: str) -> dict:
    """document.json を読み込む"""
    p = Path(path)
    if not p.exists():
        print(f"エラー: document.json が見つかりません: {path}", file=sys.stderr)
        sys.exit(1)
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def calc_items(items: list) -> tuple:
    """
    明細リストから小計・消費税・合計を計算する。
    Returns: (processed_items, subtotal, tax_total, grand_total)
    """
    subtotal = 0
    tax_total = 0
    processed = []

    for item in items:
        qty = item.get("quantity", 1)
        price = item.get("unit_price", 0)
        tax_rate = item.get("tax_rate", 10) / 100
        amount = int(qty * price)
        tax = int(amount * tax_rate)

        processed.append({
            **item,
            "amount": amount,
            "tax": tax,
            "amount_with_tax": amount + tax,
        })
        subtotal += amount
        tax_total += tax

    return processed, subtotal, tax_total, subtotal + tax_total


def format_date_jp(date_str: str) -> str:
    """YYYY-MM-DD → 令和/西暦年月日（日本語表記）"""
    if not date_str:
        return ""
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return f"{dt.year}年{dt.month}月{dt.day}日"
    except ValueError:
        return date_str


def format_date_slash(date_str: str) -> str:
    """YYYY-MM-DD → YYYY/MM/DD"""
    if not date_str:
        return ""
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return dt.strftime("%Y/%m/%d")
    except ValueError:
        return date_str


def today_str() -> str:
    return date.today().strftime("%Y-%m-%d")


def get_doc_label(doc_type: str) -> str:
    return {"estimate": "見　積　書", "invoice": "請　求　書", "receipt": "領　収　書"}.get(doc_type, "請　求　書")


def get_amount_label(doc_type: str) -> str:
    return {"estimate": "お見積金額", "invoice": "ご請求金額", "receipt": "お受取金額"}.get(doc_type, "ご請求金額")
