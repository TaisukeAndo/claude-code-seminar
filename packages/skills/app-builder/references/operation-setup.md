# 運用の段階の設定（PRと確認用の環境）

公開したあとのアプリは、次の流れで変えていく。**これは初回の構築（このスキルの工程0〜4）では行わない。**
初回に公開したアプリに、運用の段階で、変更を加え始めるときに設定する。

> mainからブランチを作る → 編集 → GitHubにPushしてPRを作る → 確認用の環境（Preview）でPC・スマホから確認
> → 問題なければ、利用者がmainにマージ → 本番に自動で反映

この流れは、実装・テスト・PR作成のSkillを自作して、毎回の指示なしで行う。
（実装Skillは、ブランチを切って実装し、テストして、PR作成Skillを呼ぶ。マージは利用者が行う）

コマンドやAPIの書式は変わりやすいので、実行前に公開ドキュメントで確認する。

- [Workers Previews](https://developers.cloudflare.com/workers/previews/get-started/)（wrangler 4.135.0以降）
- [Previewsの設定](https://developers.cloudflare.com/workers/previews/configuration/)
- [リソースの分離（D1は自動では分離されない）](https://developers.cloudflare.com/workers/previews/resources/)

## 全体の仕組み

| きっかけ | 動くもの | 結果 |
|---|---|---|
| PRを作る・更新する | `.github/workflows/preview.yml` | 確認用の環境（Preview）が作られ、URLがPRにコメントされる |
| PRを閉じる | 同上 | そのPRのPreviewが削除される |
| mainにマージする | `.github/workflows/deploy.yml`（初回に設定済み） | D1の表を更新し、本番にデプロイする |

## 1. 確認用のD1データベースを作る（承認後・MCP）

**PreviewのD1は自動では分離されない。** 本番と別のデータベースを用意し、確認用の操作が本番のデータに
触れないようにする。

1. `search` でD1作成のAPIを確認し、`execute` で `<アプリ名>-db-staging` を作る
   （参考: `POST /accounts/{account_id}/d1/database`。作る前に、名前を利用者に伝えて承認を得る）
2. 得られた `database_id` を記録する（秘密情報ではない）
3. MCPで作れないときは、`npx wrangler d1 create <アプリ名>-db-staging`

## 2. 設定ファイルを追加する

- `assets/operation/wrangler.previews.snippet.jsonc` の `previews` ブロックを、アプリの
  `wrangler.jsonc` に足す。`database_id` は手順1のIDにする
- `assets/operation/wrangler.preview-migrations.jsonc` をアプリのフォルダにコピーする。
  `database_id` は、`wrangler.jsonc` の `previews.d1_databases` と**同じ値にそろえる**
  （書き間違えると、マイグレーションが別のDBに適用される）
- wranglerが4.135.0以降か確認する（`npx wrangler --version`）。古ければ、更新を提案して承認を得る

## 3. プレビューのワークフローを配置する

`assets/operation/.github/workflows/preview.yml` を、アプリの `.github/workflows/` にコピーする。

- PRごとにPreviewを作成・更新し、URLをコメントする。PRを閉じると削除する
- フォークからのPRには秘密情報を渡さない（`head.repo.full_name == github.repository` の判定済み）
- 確認用のD1にマイグレーションを適用してからPreviewを作る（組み込み済み）
- 必要なSecrets（`CLOUDFLARE_API_TOKEN` / `CLOUDFLARE_ACCOUNT_ID`）は、初回の公開で登録済み

Previewの注意:
- Preview URLは、アクセス制限を設定しない限り、URLを知っている人なら誰でも開ける。
  公開してよい情報だけのアプリであることを、もう一度確認する

## 4. 動作を確認する

1. 作業ブランチをpushしてPRを作る
2. Actionsの画面で `Preview` が成功していることを確認する
3. PRのコメントに出たURLを、パソコンとスマートフォンで開く
4. 利用者がマージしたあと、`Deploy` が成功し、本番のURLで変更が見えることを確認する

## うまくいかないとき

| 症状 | 確認すること |
|---|---|
| Previewが作られない | wranglerが4.135.0以降か。`previews` ブロックが `wrangler.jsonc` にあるか |
| Previewで表が見つからない | `wrangler.preview-migrations.jsonc` のIDと、`previews.d1_databases` のIDが同じか。`preview.yml` のマイグレーションの手順が成功しているか |
| Actionsで認証エラー | Secretsの名前と、トークンの権限（Previewの作成に必要な権限が含まれているか） |
