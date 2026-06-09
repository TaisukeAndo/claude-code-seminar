# 6. Claude Pro でログイン

Claude Code は **Claude Pro プラン**に加入していれば、API キーなしで利用できます。  
ブラウザを使った OAuth 認証で、Google アカウントまたはメールアドレスでログインします。

## 事前確認：Claude Pro への加入

[https://claude.ai/](https://claude.ai/) にアクセスし、Pro プランに加入していることを確認してください。

::: info Claude Pro とは
Claude Pro は Anthropic の有料サブスクリプションプランです（月額 $20 程度）。  
加入することで Claude Code を従量課金なしで利用できます。
:::

---

## ログイン手順

任意のディレクトリでターミナルを開き、以下を実行してください:

```bash
claude
```

初回起動時にブラウザが自動で開き、ログイン画面が表示されます。

### ログイン方法を選択する

| 方法 | 手順 |
|---|---|
| **Google アカウント** | 「Continue with Google」をクリックし、使用する Google アカウントを選択 |
| **メールアドレス** | メールアドレスを入力 → 届いたメールの確認リンクをクリック |

ブラウザで認証が完了すると、ターミナルに Claude Code のプロンプトが表示されます。

---

## ログイン後の確認

ターミナルに以下のような表示が出れば成功です:

```
✓ Logged in as your@email.com
Claude Code v1.x.x ready.
>
```

`Ctrl + C` で終了できます。

## 次のステップ

ログインが完了したら [7. 動作確認](/setup/07-verify) に進んでください。
