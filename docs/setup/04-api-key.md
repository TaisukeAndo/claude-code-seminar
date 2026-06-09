# ④ API キーの取得・設定

Claude Code の動作には Anthropic API キーが必要です。

## 1. Anthropic Console でキーを取得する

1. [https://console.anthropic.com/](https://console.anthropic.com/) にアクセス
2. アカウントを作成（または既存アカウントでログイン）
3. 左メニューの **「API Keys」** をクリック
4. **「Create Key」** をクリックして新しいキーを生成
5. 表示された `sk-ant-...` で始まる文字列をコピー

::: warning キーは一度しか表示されません
生成直後のみ全文が確認できます。必ずコピーして安全な場所に保存してください。
:::

---

## 2. 支払い情報の登録（必要な場合）

API を使うには Billing（支払い）の設定が必要です。

1. Console の左メニュー **「Billing」** をクリック
2. クレジットカードを登録
3. **$5〜$10 程度のクレジット**をチャージ（セミナーでの使用量は数十円程度）

::: tip セミナー中の使用量の目安
ワンデイセミナーでの API 使用料は通常 **$1〜$3 程度**です。
:::

---

## 3. 環境変数に API キーを設定する

### macOS / Linux の場合

```bash
# 現在のセッションのみ有効にする場合
export ANTHROPIC_API_KEY="sk-ant-ここにキーを貼り付け"

# 永続化する場合（~/.zshrc または ~/.bashrc に追記）
echo 'export ANTHROPIC_API_KEY="sk-ant-ここにキーを貼り付け"' >> ~/.zshrc
source ~/.zshrc
```

### Windows（PowerShell）の場合

```powershell
# 現在のセッションのみ
$env:ANTHROPIC_API_KEY = "sk-ant-ここにキーを貼り付け"

# 永続化（ユーザー環境変数として保存）
[System.Environment]::SetEnvironmentVariable("ANTHROPIC_API_KEY", "sk-ant-ここにキーを貼り付け", "User")
```

::: danger キーは絶対にコードに直書きしない
API キーを `.py`、`.js` などのファイルに直接書かないでください。  
`.gitignore` に `.env` を追加したうえで `.env` ファイルを使うか、環境変数で管理してください。
:::

---

## 次のステップ

API キーの設定が完了したら [⑤ 動作確認](/setup/05-verify) に進んでください。
