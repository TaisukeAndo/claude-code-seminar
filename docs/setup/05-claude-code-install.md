# 5. Claude Code CLI インストール

Node.js のインストールが完了したら、Claude Code CLI をインストールします。

## インストールコマンド

ターミナルで以下を実行してください:

```bash
npm install -g @anthropic-ai/claude-code
```

::: info インストールには数分かかることがあります
ネットワーク環境によって 1〜3 分程度かかる場合があります。
:::

---

## Windows の場合の注意点

PowerShell でインストール後、以下のエラーが出ることがあります:

```
claude : このシステムではスクリプトの実行が無効になっているため...
```

この場合、PowerShell を**管理者として実行**して以下を入力してください:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## インストール確認

```bash
claude --version
```

バージョン番号（例: `1.x.x`）が表示されれば成功です。

## 次のステップ

Claude Code CLI のインストールが完了したら [6. Claude Pro でログイン](/setup/06-login) に進んでください。
