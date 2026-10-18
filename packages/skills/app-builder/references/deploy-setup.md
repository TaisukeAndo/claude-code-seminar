# 公開の設定手順（工程4・初回）

初回の構築で、作ったアプリをCloudflareに公開するまでの手順。
外部に作られるもの（GitHubのリポジトリ、本番用D1、公開URL）は、工程1の実施計画で承認を得た範囲で行う。
コマンドやAPIの書式は変わりやすいので、実行前に公開ドキュメントで確認する。
PR・確認用の環境（Previews）は、公開したあとの運用で使うので、ここでは設定しない
（[operation-setup.md](operation-setup.md)）。

- [Secrets](https://developers.cloudflare.com/workers/configuration/secrets/)
- [Roles and permissions](https://developers.cloudflare.com/workers/authorization/)

## Cloudflareの操作は、MCPを優先する

第2セッションで接続した **Cloudflare MCP**（`https://mcp.cloudflare.com/mcp`）には、
`search`（APIを探す）・`execute`（APIを呼ぶ）・`docs`（公式ドキュメントを検索する）の3つのツールがある。
Cloudflareの設定は、まずこのMCPで行い、できないときだけ `wrangler` のコマンドに切り替える。

| 作業 | 手段 | 理由 |
|---|---|---|
| 接続・アカウントの確認 | **MCP** | `wrangler login` は不要になる |
| D1データベースの作成 | **MCP**（APIの `D1 Write` 権限） | 公式APIに作成の機能がある |
| 作成結果・公開結果の確認（DB一覧、表の有無、デプロイの状態） | **MCP**（読み取りのみ） | 画面やコマンドを開かずに確認できる |
| D1の表の作成（マイグレーション） | GitHub Actions（`wrangler`） | 適用済みの履歴をwranglerが管理するため。MCPで直接SQLを実行すると、その履歴に残らず、あとで二重に適用される恐れがある |
| アプリのデプロイ | GitHub Actions（`wrangler`） | MCPでは、手元のファイルを1つずつ検査用の値（ハッシュ）つきでアップロードする必要があり、実用的でない |
| APIトークンの作成 | **利用者がダッシュボードで行う** | トークンの値は作成時に一度しか表示されない。MCPで作ると値が会話に出てしまうため、行わない |
| `npm run dev`・`npm run db:local`（localhost） | `wrangler`（ローカルのみ） | 自分のパソコンの中だけで動く。Cloudflareへの接続は不要 |

MCPは、OAuthで許可した権限の範囲でしか操作できない。権限が足りないときは、
利用者に「どの権限を追加で許可するか」を説明して再認証してもらうか、CLIに切り替える。

## 全体の仕組み

| きっかけ | 動くもの | 結果 |
|---|---|---|
| mainにpushする | `.github/workflows/deploy.yml` | D1の表を作り・更新し、本番にデプロイする |

## 1. Cloudflareに接続できているか確認する（MCP）

1. MCPのツール（`search` / `execute` / `docs`）が使えるか確認する。使えなければ、第2セッションの
   手順（`/mcp` で `cloudflare-api` を選んで認証）に戻る
2. **読み取りだけ**で、接続先のアカウントを確認する
   - 「このMCPで操作できるCloudflareのアカウントの一覧を教えてください」
3. アカウントが複数あるときは、どのアカウントに公開するか、利用者に確認する。
   選んだアカウントのID（`account_id`）を、この先の作業で使う

`wrangler login` は、このセミナーの手順では不要。公開（デプロイ）はGitHub Actionsが行うため、
自分のパソコンからCloudflareへ直接ログインして操作することがないため。

## 2. 本番用のD1データベースを作る（MCP）

**MCPでの作り方**

1. `search` で、D1データベースを作るAPIを探し、必要な項目を確認する
   - 参考: `POST /accounts/{account_id}/d1/database`（必要な権限は `D1 Write`）
2. 作る名前（`<アプリ名>-db`）は、実施計画で承認済み。承認した名前と違う場合は、確認する
3. `execute` で作る。結果に含まれる `uuid`（`database_id`）を、利用者に見せて記録する
4. 作ったあと、読み取りでD1データベースの一覧を取得し、並んでいることを確認する

**MCPで作れないとき**（権限不足、ツールの不具合など）は、CLIに切り替える。
その場合は、先に `npx wrangler login` と `npx wrangler whoami` で認証とアカウントを確認する。

```bash
npx wrangler d1 create <アプリ名>-db
```

**どちらの方法でも**、得られた `database_id` を `wrangler.jsonc` の最上位の `d1_databases` に書く。
IDは秘密情報ではない。

**表の作成（マイグレーション）はここでは行わない。** 公開のためのpush（手順5）で、
GitHub Actionsが `migrations/` のSQLを本番のDBに適用する。

## 3. GitHubにリポジトリを作る（pushはまだしない）

```bash
gh repo create <リポジトリ名> --<public|private> --source=. --remote=origin
```

- 公開範囲（public / private）は、実施計画で承認した内容に従う
- **`--push` は付けない。** 次の手順でSecretsを登録してからpushする
  （登録前にpushすると、GitHub Actionsが認証エラーで失敗する）

## 4. APIトークンを作り、GitHub Secretsに登録する（利用者自身が行う）

GitHub ActionsがCloudflareに接続するための認証情報。**トークンの作成と登録は、利用者自身が行う。**
トークンの値は作成時に一度しか表示されず、AIとの会話に出すと漏れるため、MCPでは作らない。

1. Cloudflareのダッシュボードで、APIトークンを作成する（アカウントのAPIトークン）
   - 必要な権限（Workersスクリプトの編集、D1の編集など）は、公式ドキュメントの
     [Roles and permissions](https://developers.cloudflare.com/workers/authorization/)
     で確認し、**必要最小限**にする
2. トークンは**会話に貼らない**。GitHubへの登録は、利用者が自分のターミナルで行う

```bash
gh secret set CLOUDFLARE_API_TOKEN
```

3. アカウントID（`CLOUDFLARE_ACCOUNT_ID`）は秘密情報ではない。手順1でMCPで確認したIDを使い、
   AIが登録してよい

```bash
gh secret set CLOUDFLARE_ACCOUNT_ID --body "<手順1で確認したアカウントID>"
```

4. 登録後、`gh secret list` で2つの名前が並ぶことだけを確認する（値は表示されない）。
   並ぶまで、次の手順に進まない

## 5. ワークフローを配置して、pushする

1. `assets/template/.github/workflows/deploy.yml` を、アプリの `.github/workflows/` に置いてコミットする
   （テンプレートをコピーしたときに、すでに入っている）
2. mainをpushする

```bash
git push -u origin main
```

`deploy.yml` は、mainへのpushで、D1の表を本番に作り・更新し、本番にデプロイする。

## 6. 動作を確認する

1. GitHubのActionsの画面で、`Deploy` が成功していることを確認する（`gh run watch` でも見られる）
2. 公開されたURL（Workerのアドレス）を、パソコンとスマートフォンで開く。URLは、
   Actionsのログ、またはCloudflare MCPでWorkerの情報を読み取って確認する
3. **MCPで確認する（読み取りのみ）**
   - 本番のD1に表ができているか（表の名前の一覧を取得するSQLを `execute` で実行する。データは変更しない）
   - Workerが作られ、最新のデプロイがあるか（Workerの一覧とデプロイの状態を取得する）

## うまくいかないとき

| 症状 | 確認すること |
|---|---|
| MCPで「権限がない」と出る | OAuthで許可した権限（D1の編集など）。足りなければ、`/mcp` で再認証して権限を追加する。難しければCLIに切り替える |
| Actionsで認証エラー | Secretsの名前（`CLOUDFLARE_API_TOKEN` / `CLOUDFLARE_ACCOUNT_ID`）と、トークンの権限。Secretsを登録する前にpushしていないか |
| 本番にデータが入らない・表がない | 本番の `database_id` が `wrangler.jsonc` の最上位の `d1_databases` に書かれているか。`deploy.yml` のマイグレーションの手順が成功しているか |
| URLが分からない | Actionsのログの `Deploy` の手順、またはCloudflare MCPでWorkerの情報を読み取る |
