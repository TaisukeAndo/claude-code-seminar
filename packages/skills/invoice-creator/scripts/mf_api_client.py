#!/usr/bin/env python3
"""
MoneyForward クラウド請求書 API v3 クライアント
PII（トークン・ID）は .env からのみ読み込み、LLM には渡さない。
"""

import json
import sys
import time
import requests
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = SKILL_DIR / ".env"

MF_BASE_URL = "https://invoice.moneyforward.com/api/v3"
MF_AUTH_URL = "https://app.moneyforward.com/oauth/authorize"
MF_TOKEN_URL = "https://app.moneyforward.com/oauth/token"

EXCISE_MAP = {10: "ten_percent", 8: "eight_percent", 0: "free"}


class MoneyForwardAPIError(Exception):
    def __init__(self, status_code: int, body: str):
        self.status_code = status_code
        self.body = body
        try:
            detail = json.loads(body).get("errors", body)
        except Exception:
            detail = body
        super().__init__(f"MoneyForward API {status_code}: {detail}")


class MoneyForwardClient:
    """MoneyForward クラウド請求書 API v3 クライアント（OAuth 2.0）"""

    def __init__(self):
        self._env = self._load_env()
        self.client_id = self._env.get("MF_CLIENT_ID", "")
        self.client_secret = self._env.get("MF_CLIENT_SECRET", "")
        self.access_token = self._env.get("MF_ACCESS_TOKEN", "")
        self.refresh_token = self._env.get("MF_REFRESH_TOKEN", "")
        self.token_expires_at = float(self._env.get("MF_TOKEN_EXPIRES_AT", "0"))

        if not self.client_id or not self.client_secret:
            print(
                "エラー: MF_CLIENT_ID / MF_CLIENT_SECRET が .env に未設定です。\n"
                "  python3 mf_oauth_setup.py を実行して初期設定を行ってください。",
                file=sys.stderr,
            )
            sys.exit(1)

        if not self.access_token:
            print(
                "エラー: MF_ACCESS_TOKEN が未設定です。\n"
                "  python3 mf_oauth_setup.py を実行して OAuth 認証を完了してください。",
                file=sys.stderr,
            )
            sys.exit(1)

    # ── .env I/O ──────────────────────────────────────────────────────────

    def _load_env(self) -> dict:
        if not ENV_FILE.exists():
            print(f"エラー: .env が見つかりません: {ENV_FILE}", file=sys.stderr)
            sys.exit(1)
        result = {}
        for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                k, _, v = line.partition("=")
                result[k.strip()] = v.strip().strip('"').strip("'")
        return result

    def _update_env_key(self, key: str, value: str):
        text = ENV_FILE.read_text(encoding="utf-8")
        lines = text.splitlines()
        replaced = False
        new_lines = []
        for line in lines:
            if line.startswith(f"{key}="):
                new_lines.append(f"{key}={value}")
                replaced = True
            else:
                new_lines.append(line)
        if not replaced:
            new_lines.append(f"{key}={value}")
        ENV_FILE.write_text("\n".join(new_lines) + "\n", encoding="utf-8")

    # ── OAuth トークン管理 ─────────────────────────────────────────────────

    def save_tokens(self, access_token: str, refresh_token: str, expires_in: int):
        expires_at = time.time() + expires_in - 120  # 2分バッファ
        self._update_env_key("MF_ACCESS_TOKEN", access_token)
        self._update_env_key("MF_REFRESH_TOKEN", refresh_token)
        self._update_env_key("MF_TOKEN_EXPIRES_AT", str(expires_at))
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.token_expires_at = expires_at

    def _refresh(self):
        resp = requests.post(
            MF_TOKEN_URL,
            data={
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "grant_type": "refresh_token",
                "refresh_token": self.refresh_token,
            },
            timeout=30,
        )
        if not resp.ok:
            raise MoneyForwardAPIError(resp.status_code, resp.text)
        d = resp.json()
        self.save_tokens(d["access_token"], d.get("refresh_token", self.refresh_token), d["expires_in"])

    def _ensure_token(self):
        if self.refresh_token and time.time() >= self.token_expires_at:
            self._refresh()

    # ── HTTP ヘルパー ───────────────────────────────────────────────────────

    def _headers(self, accept="application/json") -> dict:
        self._ensure_token()
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "Accept": accept,
        }

    def _get(self, path: str, params: dict = None) -> dict:
        r = requests.get(f"{MF_BASE_URL}{path}", headers=self._headers(), params=params, timeout=30)
        if r.status_code == 401 and self.refresh_token:
            self._refresh()
            r = requests.get(f"{MF_BASE_URL}{path}", headers=self._headers(), params=params, timeout=30)
        if not r.ok:
            raise MoneyForwardAPIError(r.status_code, r.text)
        return r.json()

    def _post(self, path: str, payload: dict) -> dict:
        r = requests.post(f"{MF_BASE_URL}{path}", headers=self._headers(), json=payload, timeout=30)
        if not r.ok:
            raise MoneyForwardAPIError(r.status_code, r.text)
        return r.json()

    def _get_pdf(self, path: str) -> bytes:
        r = requests.get(f"{MF_BASE_URL}{path}", headers=self._headers(accept="application/pdf"), timeout=60)
        if not r.ok:
            raise MoneyForwardAPIError(r.status_code, r.text)
        return r.content

    # ── 取引先（Partner） ──────────────────────────────────────────────────

    def find_partner(self, name: str) -> dict | None:
        data = self._get("/partners", params={"query": name, "page": 1, "per_page": 10})
        items = data.get("data", [])
        for p in items:
            if name in p.get("attributes", {}).get("name", ""):
                return p
        return items[0] if items else None

    def list_partners(self, query: str = None, page: int = 1, per_page: int = 20) -> dict:
        params = {"page": page, "per_page": per_page}
        if query:
            params["query"] = query
        return self._get("/partners", params=params)

    # ── 見積書（Quotation） ────────────────────────────────────────────────

    def list_quotations(self, partner_id: str = None, page: int = 1, per_page: int = 10) -> dict:
        params = {"page": page, "per_page": per_page}
        if partner_id:
            params["partner_id"] = partner_id
        return self._get("/quotations", params=params)

    def get_quotation(self, quotation_id: str) -> dict:
        return self._get(f"/quotations/{quotation_id}")

    def create_quotation(self, payload: dict) -> dict:
        return self._post("/quotations", {"quotation": payload})

    def get_quotation_pdf(self, quotation_id: str) -> bytes:
        return self._get_pdf(f"/quotations/{quotation_id}/pdf")

    # ── 請求書（Invoice） ──────────────────────────────────────────────────

    def list_invoices(self, partner_id: str = None, page: int = 1, per_page: int = 10) -> dict:
        params = {"page": page, "per_page": per_page}
        if partner_id:
            params["partner_id"] = partner_id
        return self._get("/invoices", params=params)

    def get_invoice(self, invoice_id: str) -> dict:
        return self._get(f"/invoices/{invoice_id}")

    def create_invoice(self, payload: dict) -> dict:
        return self._post("/invoices", {"invoice": payload})

    def get_invoice_pdf(self, invoice_id: str) -> bytes:
        return self._get_pdf(f"/invoices/{invoice_id}/pdf")

    # ── 領収書（Receipt） ──────────────────────────────────────────────────

    def create_receipt(self, payload: dict) -> dict:
        return self._post("/receipts", {"receipt": payload})

    def get_receipt_pdf(self, receipt_id: str) -> bytes:
        return self._get_pdf(f"/receipts/{receipt_id}/pdf")

    # ── 品目マスタ ──────────────────────────────────────────────────────────

    def list_items(self, page: int = 1, per_page: int = 50) -> dict:
        return self._get("/items", params={"page": page, "per_page": per_page})


# ── document.json → MoneyForward API ペイロード 変換ユーティリティ ──────────

def doc_to_invoice_payload(doc: dict, partner_id: str) -> dict:
    """document.json を MoneyForward 請求書作成ペイロードに変換する"""
    contents = []
    for i, item in enumerate(doc.get("items", [])):
        contents.append({
            "order": i,
            "type": "normal",
            "name": item.get("name", ""),
            "detail": item.get("detail", ""),
            "unit": item.get("unit", ""),
            "quantity": item.get("quantity", 1),
            "unit_price": item.get("unit_price", 0),
            "excise": EXCISE_MAP.get(item.get("tax_rate", 10), "ten_percent"),
        })
    return {
        "partner_id": partner_id,
        "invoice_number": doc.get("document_number", ""),
        "title": doc.get("title", ""),
        "issue_date": doc.get("issue_date", ""),
        "due_date": doc.get("due_date", ""),
        "note": doc.get("notes", ""),
        "invoice_contents": contents,
    }


def doc_to_quotation_payload(doc: dict, partner_id: str) -> dict:
    """document.json を MoneyForward 見積書作成ペイロードに変換する"""
    contents = []
    for i, item in enumerate(doc.get("items", [])):
        contents.append({
            "order": i,
            "type": "normal",
            "name": item.get("name", ""),
            "detail": item.get("detail", ""),
            "unit": item.get("unit", ""),
            "quantity": item.get("quantity", 1),
            "unit_price": item.get("unit_price", 0),
            "excise": EXCISE_MAP.get(item.get("tax_rate", 10), "ten_percent"),
        })
    return {
        "partner_id": partner_id,
        "quotation_number": doc.get("document_number", ""),
        "title": doc.get("title", ""),
        "issue_date": doc.get("issue_date", ""),
        "expiry_date": doc.get("expiry_date", ""),
        "note": doc.get("notes", ""),
        "quotation_contents": contents,
    }


def doc_to_receipt_payload(doc: dict, partner_id: str) -> dict:
    """document.json を MoneyForward 領収書作成ペイロードに変換する"""
    return {
        "partner_id": partner_id,
        "receipt_number": doc.get("document_number", ""),
        "issue_date": doc.get("issue_date", ""),
        "amount_including_tax": doc.get("total_amount", 0),
        "memo": doc.get("title", ""),
        "note": doc.get("notes", ""),
    }
