# よくある質問

## インストール・セットアップ

### `npm: command not found` と表示される

Node.js がインストールされていないか、PATH が通っていません。

1. [2. Node.js インストール](/setup/02-nodejs-install) の手順を再確認
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

## ログイン・認証

### ログイン時にブラウザが開かない

ターミナルに表示された URL を手動でブラウザにコピー＆ペーストしてアクセスしてください。

### `You don't have an active subscription` と表示される

Claude Pro プランへの加入が必要です。[https://claude.ai/](https://claude.ai/) でプランを確認してください。

### Google アカウントでログインできない

- ブラウザで [https://claude.ai/](https://claude.ai/) に直接アクセスしてログインできるか確認
- 別のブラウザやシークレットモードで試す
- ブラウザの Cookie をクリアしてから再試行

### ログイン後に `Authentication failed` と表示される

一度ログアウトしてから再度ログインを試みてください:

```bash
claude logout
claude
```

---

## 接続・ネットワーク

### タイムアウトやネットワークエラーが出る

- インターネット接続を確認してください
- VPN を使用している場合は一時的に無効にしてみてください
- 会社や学校のネットワークでブロックされている場合があります。モバイルデータ通信（テザリング）で試してください

---

## セミナー当日

### 当日また確認することはありますか？

セミナー開始 10 分前に以下を確認してください:

```bash
claude --version   # バージョンが表示されるか
claude             # 起動するか（Ctrl+C で終了）
```

それでも解決しない問題は当日会場で講師にお声がけください。
