#!/usr/bin/env python3
"""
MoneyForward クラウド請求書 OAuth 2.0 初回認証スクリプト
初回のみ実行。取得したトークンは .env に保存される。

使い方:
  python3 mf_oauth_setup.py

事前準備:
  1. https://app.moneyforward.com/api_authorizations でアプリを登録
  2. リダイレクト URI: http://localhost:8085/callback を設定
  3. .env に MF_CLIENT_ID と MF_CLIENT_SECRET を記入
"""

import sys
import json
import time
import urllib.parse
import urllib.request
import http.server
import threading
import webbrowser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from mf_api_client import MoneyForwardClient, MF_AUTH_URL, MF_TOKEN_URL, ENV_FILE

REDIRECT_URI = "http://localhost:8085/callback"
SCOPES = "invoices quotations receipts partners"

_auth_code = None
_server_done = threading.Event()


class _CallbackHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        global _auth_code
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        if "code" in params:
            _auth_code = params["code"][0]
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(
                "<html><body><h2>✅ 認証完了！</h2>"
                "<p>このウィンドウを閉じて、ターミナルに戻ってください。</p>"
                "</body></html>".encode("utf-8")
            )
        else:
            self.send_response(400)
            self.end_headers()
        _server_done.set()

    def log_message(self, *args):
        pass  # suppress access logs


def _exchange_code_for_token(code: str, client_id: str, client_secret: str) -> dict:
    data = urllib.parse.urlencode({
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI,
    }).encode("utf-8")
    req = urllib.request.Request(MF_TOKEN_URL, data=data, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main():
    print("=" * 60)
    print("  MoneyForward クラウド請求書 OAuth 認証セットアップ")
    print("=" * 60)

    # .env から client_id / client_secret を読む
    if not ENV_FILE.exists():
        print(f"エラー: .env が見つかりません: {ENV_FILE}")
        print("  .env.example をコピーして MF_CLIENT_ID と MF_CLIENT_SECRET を記入してください。")
        sys.exit(1)

    env = {}
    for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            k, _, v = line.partition("=")
            env[k.strip()] = v.strip().strip('"').strip("'")

    client_id = env.get("MF_CLIENT_ID", "")
    client_secret = env.get("MF_CLIENT_SECRET", "")

    if not client_id or not client_secret:
        print("エラー: MF_CLIENT_ID または MF_CLIENT_SECRET が .env に未設定です。")
        sys.exit(1)

    # 認証 URL を生成
    params = urllib.parse.urlencode({
        "client_id": client_id,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": SCOPES,
    })
    auth_url = f"{MF_AUTH_URL}?{params}"

    # コールバックサーバーを起動
    server = http.server.HTTPServer(("localhost", 8085), _CallbackHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    print(f"\n[1] ブラウザで MoneyForward の認証画面を開きます...")
    print(f"    URL: {auth_url}\n")
    webbrowser.open(auth_url)

    print("[2] ブラウザで「許可する」をクリックしてください。")
    print("    自動的にコールバックを受信します...\n")
    _server_done.wait(timeout=120)
    server.shutdown()

    if not _auth_code:
        print("エラー: 認証コードの取得タイムアウト（120秒）。やり直してください。")
        sys.exit(1)

    print("[3] アクセストークンを取得中...")
    token_data = _exchange_code_for_token(_auth_code, client_id, client_secret)

    # .env に保存
    mf_client = MoneyForwardClient.__new__(MoneyForwardClient)
    mf_client._env = env
    mf_client.client_id = client_id
    mf_client.client_secret = client_secret
    mf_client.access_token = token_data["access_token"]
    mf_client.refresh_token = token_data.get("refresh_token", "")
    mf_client.token_expires_at = 0

    def _update_env_key(key, value):
        text = ENV_FILE.read_text(encoding="utf-8")
        lines = text.splitlines()
        found = False
        new_lines = []
        for line in lines:
            if line.startswith(f"{key}="):
                new_lines.append(f"{key}={value}")
                found = True
            else:
                new_lines.append(line)
        if not found:
            new_lines.append(f"{key}={value}")
        ENV_FILE.write_text("\n".join(new_lines) + "\n", encoding="utf-8")

    expires_at = time.time() + token_data.get("expires_in", 7200) - 120
    _update_env_key("MF_ACCESS_TOKEN", token_data["access_token"])
    _update_env_key("MF_REFRESH_TOKEN", token_data.get("refresh_token", ""))
    _update_env_key("MF_TOKEN_EXPIRES_AT", str(expires_at))

    print(f"\n✅ 認証完了！トークンを .env に保存しました。")
    print(f"   有効期限: {int(token_data.get('expires_in', 7200) / 3600)} 時間")
    print(f"   リフレッシュトークン: {'あり（自動更新）' if token_data.get('refresh_token') else 'なし'}")
    print("\nこのスクリプトは次回以降は不要です。")


if __name__ == "__main__":
    main()
