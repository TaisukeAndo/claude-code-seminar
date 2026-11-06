# 公開の設定手順（工程4・初回）

初回の構築で、作ったアプリをCloudflareに公開するまでの手順。
外部に作られるもの（GitHubのリポジトリ、本番用D1、公開URL）は、工程1の実施計画で承認を得た範囲で行う。
コマンドの書式は変わりやすいので、実行前に `npx wrangler <コマンド> --help` と公開ドキュメントで確認する。
PR・確認用の環境（Previews）は、公開したあとの運用で使うので、ここでは設定しない
（[operation-setup.md](operation-setup.md)）。

- [Wranglerのコマンド一覧](https://developers.cloudflare.com/workers/wrangler/commands/)
- [D1のWranglerコマンド](https://developers.cloudflare.com/d1/wrangler-commands/)
- [Secrets](https://developers.cloudflare.com/workers/configuration/secrets/)
- [Roles and permissions](https://developers.cloudflare.com/workers/authorization/)

## Cloudflareの操作は、Wranglerで行う

利用者のパソコンでログイン済みの **Wrangler**（`npx wrangler`）で、Cloudflareを操作する。
ログインは、利用者が自分で開いたターミナルで `npx --yes wrangler login` を実行して済ませておく
（[manual-steps.md](manual-steps.md) のA）。AIは `wrangler login` を実行しない。

| 作業 | 手段 | Claude Codeの確認 |
|---|---|---|
| 接続・アカウントの確認 | `npx wrangler whoami` | なし（読み取りのみ） |
| D1データベースの一覧 | `npx wrangler d1 list` | なし（読み取りのみ） |
| D1データベースの作成 | `npx wrangler d1 create <名前>` | **毎回確認**（Cloudflareの上に作る） |
| 公開結果の確認（表の有無） | `npx wrangler d1 execute <名前> --remote --command "SELECT ..."` | 確認あり（SELECTだけを実行する。データは変更しない） |
| 公開結果の確認（デプロイの状態） | `npx wrangler deployments list` | 確認あり（読み取りのみ） |
| 本番のD1の表の作成（マイグレーション） | GitHub Actions（`wrangler d1 migrations apply --remote`） | — |
| 本番へのデプロイ | GitHub Actions（`wrangler deploy`） | — |
| APIトークンの作成 | **利用者がダッシュボードで行う** | — |
| `npm run dev`・`npm run db:local`（localhost） | `wrangler`（ローカルのみ） | 自分のパソコンの中だけで動く |

本番の表の作成とデプロイを、手元の `wrangler` ではなくGitHub Actionsで行う理由:
mainにpushした内容と本番を必ず一致させ、運用の段階（PRとマージ）でも同じ仕組みで公開できるようにするため。
手元から `npx wrangler deploy` や `npx wrangler d1 migrations apply --remote` は実行しない
（実行すると、GitHubにない変更が本番に出る恐れがある）。

**作る・変える・消すコマンドは、実行の前に、何をするコマンドかを1行で伝える。**
Claude Codeの確認画面で、利用者が「はい」を押してよいか判断できるようにするため。
例:「CloudflareにD1データベース `my-app-db` を作ります。実施計画で承認いただいた名前です」

Windowsで「このシステムではスクリプトの実行が無効になっている」と出たときは、`npx` を `npx.cmd` に置き換える。

## 全体の仕組み

| きっかけ | 動くもの | 結果 |
|---|---|---|
| mainにpushする | `.github/workflows/deploy.yml` | D1の表を作り・更新し、本番にデプロイする |

## 1. Cloudflareに接続できているか確認する（Wrangler）

1. `npx wrangler whoami` を実行する
2. 「ログインしていない」と出たら、作業を止めて、manual-steps.md のAを1ステップずつ案内する。
   利用者がログインしたら、もう一度 `whoami` を実行する
3. 表示されたメールアドレスが、利用者のアカウントか確認してもらう
4. アカウントが複数表示されたときは、どのアカウントに公開するか、利用者に確認する。
   選んだアカウントのID（`account_id`）を、この先の作業で使う。複数あるときは、
   以降のWranglerのコマンドに `CLOUDFLARE_ACCOUNT_ID=<ID>` を付けるか、`wrangler.jsonc` に
   `"account_id"` を書いて、対象のアカウントを固定する（IDは秘密情報ではない）

## 2. 本番用のD1データベースを作る（Wrangler）

1. `npx wrangler d1 list` で、同じ名前のデータベースがないか確認する
2. 作る名前（`<アプリ名>-db`）は、実施計画で承認済み。承認した名前と違う場合は、確認する
3. 何をするかを1行で伝えてから、作る。Claude Codeの確認画面で、利用者に許可してもらう

```bash
npx wrangler d1 create <アプリ名>-db
```

4. 結果に表示される `database_id` を、利用者に見せて記録する
   - wranglerのバージョンによっては、作成後に「`wrangler.jsonc` に書き足すか」を聞かれる。
     先に `npx wrangler d1 create --help` を見て、設定ファイルを自動で書き換える指定があるか確認する。
     自動で書き換わった場合も、内容が次の手順5のとおりになっているか確かめる
5. `database_id` を、`wrangler.jsonc` の最上位の `d1_databases` に書く。
   `database_name` は、作った名前と同じにする。IDは秘密情報ではない
6. もう一度 `npx wrangler d1 list` を実行し、作ったデータベースが並ぶことを確認する

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

GitHub ActionsがCloudflareに接続するための認証情報。利用者のパソコンのWranglerはログイン済みだが、
GitHub ActionsはGitHubのサーバーの上で動くので、別に許可証（APIトークン）を渡す必要がある。
**トークンの作成と登録は、利用者自身が行う。** トークンの値は作成時に一度しか表示されず、
AIとの会話に出すと漏れるため。
**AIは、【あなたにお願いします】と明示して作業を止め、[manual-steps.md](manual-steps.md) の
B（トークンの作成）とC（GitHubへの登録）を、1ステップずつ案内する。**

トークンの権限について（公式ドキュメントでの確認結果）:
- Cloudflareのトークン作成画面の「Edit Cloudflare Workers」テンプレートを起点にする
- このアプリは、公開のときに `wrangler d1 migrations apply --remote` でD1の表を作る。
  公式ドキュメントは「D1にバインドしたWorkerをデプロイするだけなら、D1の権限は要らない」と
  説明しているが、**D1の表を作る（書き込む）にはD1の編集権限が必要**になる。
  テンプレートにD1の権限が含まれているかは、公式ドキュメントで確認できなかったので、
  **「D1」の「Edit」を足す**手順にしてある（manual-steps.md のB）
- 対象のアカウントは、公開する1つだけに絞る。権限は必要最小限にする
- 権限の名前は変わることがある。迷ったら公式ドキュメントで確認する

登録後、AIは `gh secret list` で `CLOUDFLARE_API_TOKEN` の名前が並ぶことだけを確認する
（値は表示されない）。並ぶまで、次の手順に進まない。

アカウントID（`CLOUDFLARE_ACCOUNT_ID`）は秘密情報ではない。手順1で `whoami` で確認したIDを使い、
AIが登録してよい。

```bash
gh secret set CLOUDFLARE_ACCOUNT_ID --body "<手順1で確認したアカウントID>"
```

## 5. ワークフローを配置して、pushする

1. `assets/template/.github/workflows/deploy.yml` を、アプリの `.github/workflows/` に置いてコミットする
   （テンプレートをコピーしたときに、すでに入っている）
2. mainをpushする

```bash
git push -u origin main
```

`deploy.yml` は、mainへのpushで、D1の表を本番に作り・更新し、本番にデプロイする。

## 6. 動作を確認する

1. GitHubのActionsの画面で、`Deploy` が成功していることを確認する（`gh run watch` でも見られる）。
   利用者には [manual-steps.md](manual-steps.md) のDの手順で、ブラウザでも確かめてもらう
2. 公開されたURL（Workerのアドレス）を、パソコンとスマートフォンで開く。URLは、Actionsのログの
   `Deploy` の手順に表示される
3. **Wranglerで確認する（読み取りのみ）**
   - 本番のD1に表ができているか（SELECTだけを実行する。データは変更しない）

     ```bash
     npx wrangler d1 execute <アプリ名>-db --remote --command "SELECT name FROM sqlite_master WHERE type='table'"
     ```

   - マイグレーションが本番に適用済みか: `npx wrangler d1 migrations list <アプリ名>-db --remote`
     （未適用のものが残っていなければよい）
   - 最新のデプロイがあるか: `npx wrangler deployments list`

## うまくいかないとき

| 症状 | 確認すること |
|---|---|
| `whoami` で「ログインしていない」と出る | manual-steps.md のAで、利用者に自分のターミナルでログインしてもらう |
| Wranglerで「Authentication error」「権限がない」と出る | ログインのときに外した権限が必要なコマンドの可能性がある。利用者に `npx wrangler login` をやり直してもらい、WorkersとD1の権限を許可する |
| `whoami` に、知らないアカウントが出る | 別のアカウントでログインしている。利用者に `npx wrangler logout` のあと、ログインし直してもらう |
| `d1 create` が質問で止まる | 対話入力を待っている。`--help` で質問を省く指定を確認するか、利用者に、自分のターミナルで同じコマンドを実行してもらい、表示された `database_id` を教えてもらう（IDは秘密情報ではない） |
| Actionsで認証エラー | Secretsの名前（`CLOUDFLARE_API_TOKEN` / `CLOUDFLARE_ACCOUNT_ID`）と、トークンの権限。Secretsを登録する前にpushしていないか |
| 本番にデータが入らない・表がない | 本番の `database_id` が `wrangler.jsonc` の最上位の `d1_databases` に書かれているか。`deploy.yml` のマイグレーションの手順が成功しているか |
| URLが分からない | Actionsのログの `Deploy` の手順を見る |
