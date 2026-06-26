# ステップ④ MCP サーバーの接続設定

Claude Code に外部サービスを連携させる **MCP（エムシーピー）** の設定を行います。  
Gmail・Microsoft 365・Google カレンダー・Google ドライブを Claude から操作できるようになります。

## MCP とは？

MCP（Model Context Protocol）は、**Claude Code に外部サービスを接続する仕組み**です。

MCP を設定することで、Claude が直接 Gmail の内容を読んだり、  
Google カレンダーの予定を確認したり、Google ドライブのファイルを操作したりできるようになります。

Claude Code Desktop では、`/mcp` というコマンドで接続済みのサービス一覧を確認・管理できます。

## 今回接続するサービス

| サービス | できること |
|---|---|
| **Gmail** | メールの確認・検索・下書き作成 |
| **Microsoft 365** | Outlook メール・OneDrive・予定表の操作 |
| **Google カレンダー** | 予定の確認・追加・変更 |
| **Google ドライブ** | ファイルの検索・閲覧・作成 |

## 接続手順

### ① Claude Code を起動する

Claude Desktop を開き、ホーム画面で Claude Code を起動してください。  
入力欄に **「/mcp」** と入力して `Enter` を押します。

```
/mcp
```

接続可能な MCP サーバーの一覧が表示されます。

### ② Gmail を接続する

1. `/mcp` の一覧から **「Gmail」** を選択
2. **「Connect」** または **「接続」** をクリック
3. ブラウザが開き、Google のログイン画面が表示される
4. Gmail に使用している **Google アカウント** でログイン
5. 「Claude Code が Gmail にアクセスすることを許可しますか？」と表示されたら **「許可」** をクリック
6. ブラウザを閉じ、Claude Code に戻ると接続完了

### ③ Microsoft 365 を接続する

1. `/mcp` の一覧から **「Microsoft 365」** を選択
2. **「Connect」** または **「接続」** をクリック
3. ブラウザが開き、Microsoft のログイン画面が表示される
4. **Microsoft アカウント**（職場・学校アカウントまたは個人アカウント）でログイン
5. 「Claude Code がアクセスを要求しています」と表示されたら **「承諾」** をクリック
6. ブラウザを閉じ、Claude Code に戻ると接続完了

::: info Microsoft 365 アカウントについて
会社や学校から付与された職場アカウント（`名前@会社名.com` など）、  
または個人の Microsoft アカウント（`名前@outlook.com` など）でログインしてください。
:::

### ④ Google カレンダーを接続する

1. `/mcp` の一覧から **「Google Calendar」** を選択
2. **「Connect」** または **「接続」** をクリック
3. ブラウザが開き、Google のログイン画面が表示される
4. カレンダーに使用している **Google アカウント** でログイン
5. 「Claude Code が Google カレンダーにアクセスすることを許可しますか？」→ **「許可」**
6. ブラウザを閉じ、Claude Code に戻ると接続完了

### ⑤ Google ドライブを接続する

1. `/mcp` の一覧から **「Google Drive」** を選択
2. **「Connect」** または **「接続」** をクリック
3. ブラウザが開き、Google のログイン画面が表示される
4. ドライブに使用している **Google アカウント** でログイン
5. 「Claude Code が Google ドライブにアクセスすることを許可しますか？」→ **「許可」**
6. ブラウザを閉じ、Claude Code に戻ると接続完了

## 接続の確認

すべて接続したら、Claude Code で再度 `/mcp` と入力して一覧を確認してください。

```
/mcp
```

以下の 4 つのサービスに **「Connected」** または緑のチェックマークが表示されれば設定完了です:

- Gmail ✅
- Microsoft 365 ✅
- Google Calendar ✅
- Google Drive ✅

## トラブルシューティング

**ブラウザが自動で開かない場合**  
Claude Code の画面に表示される URL をコピーして、ブラウザのアドレスバーに貼り付けてください。

**「アクセスがブロックされました」と表示される場合**  
使用している Google アカウントに制限がかかっている可能性があります。  
別のブラウザやシークレットモードで試してみてください。

**接続後に「Disconnected」と表示される場合**  
一度 Claude Desktop を再起動し、`/mcp` で再確認してください。

## セットアップ完了

4 つのサービスの接続が確認できたら、セットアップはすべて完了です。  
Claude Code Desktop から Gmail・Google カレンダー・Google ドライブ・Microsoft 365 を使った操作ができるようになりました。
