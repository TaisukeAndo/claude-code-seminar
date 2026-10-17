# 公開の設定手順（工程4）

初回だけ行う準備と、PR・マージのたびに動く仕組みをまとめる。
**各コマンドの前に、利用者の承認を取る。** コマンドの書式と設定項目は変わりやすいので、
実行前に公開ドキュメントと `npx wrangler <コマンド> --help` で確認する。

- [Workers Previews](https://developers.cloudflare.com/workers/previews/get-started/)（wrangler 4.135.0以降）
- [Previewsの設定](https://developers.cloudflare.com/workers/previews/configuration/)
- [リソースの分離（D1は自動では分離されない）](https://developers.cloudflare.com/workers/previews/resources/)
- [Secrets](https://developers.cloudflare.com/workers/configuration/secrets/)

## 全体の仕組み

| きっかけ | 動くもの | 結果 |
|---|---|---|
| PRを作る・更新する | `.github/workflows/preview.yml` | 確認用の環境（Preview）が作られ、URLがPRにコメントされる |
| PRを閉じる | 同上 | そのPRのPreviewが削除される |
| mainにマージする | `.github/workflows/deploy.yml` | D1の表を更新し、本番にデプロイする |

## 1. Cloudflareにログインして確認する

```bash
npx wrangler login
npx wrangler whoami
```

- `wrangler login` は利用者自身のブラウザで認証する。アカウントが複数あるときは、
  どのアカウントに公開するか、利用者に確認する

## 2. D1データベースを2つ作る（承認後）

本番用と、Preview（確認用）用の2つ。**PreviewのD1は自動では分離されない**ので、
本番と別のデータベースを用意し、確認用の操作が本番のデータに触れないようにする。

```bash
npx wrangler d1 create <アプリ名>-db
npx wrangler d1 create <アプリ名>-db-staging
```

表示された `database_id` を、次のとおり `wrangler.jsonc` に書く。

- 本番のID → 最上位の `d1_databases`
- 確認用のID → `previews.d1_databases`
- 確認用のID → `wrangler.preview-migrations.jsonc` の `d1_databases`（同じIDにそろえる）

IDは秘密情報ではない。ただし、書き間違えるとマイグレーションが別のDBに適用されるので、
3か所のIDが一致していることを確認する。

## 3. GitHubにリポジトリを作る（承認後）

```bash
gh repo create <リポジトリ名> --<public|private> --source=. --remote=origin --push
```

公開範囲（public / private）は、利用者に確認してから決める。

## 4. APIトークンを作り、GitHub Secretsに登録する（利用者自身が行う）

1. Cloudflareのダッシュボードで、APIトークンを作成する
   - 必要な権限（Workersスクリプトの編集、D1の編集など）は、公式ドキュメントの
     [Roles and permissions](https://developers.cloudflare.com/workers/authorization/)
     で確認し、**必要最小限**にする
2. トークンは**会話に貼らない**。GitHubへの登録は、利用者が自分のターミナルで行う

```bash
gh secret set CLOUDFLARE_API_TOKEN
gh secret set CLOUDFLARE_ACCOUNT_ID
```

3. 登録後、`gh secret list` で名前が並ぶことだけを確認する（値は表示されない）

## 5. ワークフローを配置する

`assets/template/.github/workflows/` の2つを、アプリの `.github/workflows/` にコピーする。

- `deploy.yml`: mainへのpushで、D1のマイグレーションと本番デプロイ
- `preview.yml`: PRごとにPreviewを作成・更新し、URLをコメント。PRを閉じると削除。
  フォークからのPRには秘密情報を渡さない（`head.repo.full_name == github.repository` の判定済み）

Previewの注意:
- Preview URLは、アクセス制限を設定しない限り、URLを知っている人なら誰でも開ける。
  公開してよい情報だけのアプリであることを、もう一度確認する
- Previewで確認用のD1を使うには、マイグレーションを事前に適用する必要がある
  （`preview.yml` に組み込み済み）

## 6. 動作を確認する

1. 作業ブランチをpushしてPRを作る
2. Actionsの画面で `Preview` が成功していることを確認する
3. PRのコメントに出たURLを、パソコンとスマートフォンで開く
4. 利用者がマージしたあと、`Deploy` が成功し、本番のURLで変更が見えることを確認する

## うまくいかないとき

| 症状 | 確認すること |
|---|---|
| Actionsで認証エラー | Secretsの名前（`CLOUDFLARE_API_TOKEN` / `CLOUDFLARE_ACCOUNT_ID`）と、トークンの権限 |
| Previewが作られない | wranglerが4.135.0以降か（`npx wrangler --version`）。`previews` ブロックが `wrangler.jsonc` にあるか |
| Previewで表が見つからない | `wrangler.preview-migrations.jsonc` のIDと、`previews.d1_databases` のIDが同じか。マイグレーションの手順が先に実行されているか |
| 本番にデータが入らない | 本番の `database_id` が最上位の `d1_databases` に書かれているか。`deploy.yml` のマイグレーションが成功しているか |
