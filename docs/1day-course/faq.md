# よくある質問

## インストール・セットアップ

### `npm: command not found` と表示される

Node.js がインストールされていないか、PATH が通っていません。

1. [② Node.js インストール](/1day-course/setup/02-nodejs-install) の手順を再確認
2. ターミナルを**再起動**してから再度試す

### `claude: command not found` と表示される

Claude Code CLI が正しくインストールされていません。

```bash
npm install -g @anthropic-ai/claude-code
```

を再実行してください。それでも解決しない場合:

```bash
npm list -g @anthropic-ai/claude-code
```

でインストール状況を確認してください。

### Windows で `スクリプトの実行が無効` とエラーが出る

PowerShell を**管理者として実行**して以下を入力してください:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## API キー・認証

### API キーはどこで取得できますか？

[Anthropic Console](https://console.anthropic.com/) の「API Keys」から取得できます。  
詳しくは [④ API キーの取得・設定](/1day-course/setup/04-api-key) を参照してください。

### `AuthenticationError` や `Invalid API key` と表示される

API キーが正しく設定されていない可能性があります。

```bash
# macOS / Linux で確認
echo $ANTHROPIC_API_KEY

# Windows (PowerShell) で確認
echo $env:ANTHROPIC_API_KEY
```

`sk-ant-...` で始まる文字列が表示されない場合は、[④ API キーの設定手順](/1day-course/setup/04-api-key) を再確認してください。

### `credit balance is too low` と表示される

クレジット残高が不足しています。[Anthropic Console](https://console.anthropic.com/) の Billing からクレジットを追加してください。

---

## 接続・ネットワーク

### タイムアウトやネットワークエラーが出る

- インターネット接続を確認してください
- VPN を使用している場合は一時的に無効にしてみてください
- 会社や学校のネットワークで Anthropic API (`api.anthropic.com`) がブロックされている場合があります。モバイルデータ通信（テザリング）で試してください

---

## セミナー当日

### 当日また確認することはありますか？

セミナー開始 10 分前に以下を確認してください:

```bash
claude --version   # バージョンが表示されるか
claude             # 起動するか（Ctrl+C で終了）
```

それでも解決しない問題は当日会場で講師にお声がけください。
