# アプリの種類とコマンドの調べ方

どのアプリでも使えるように、技術を決め打ちせず、リポジトリを読んで判断する。

## 見る場所と、分かること

| 見る場所 | 分かること |
|---|---|
| `README.md`・`CLAUDE.md`・`requirements.md` | アプリの目的、起動方法、決まりごと |
| `package.json` の `scripts` | `dev`（起動）・`test`・`build`・`lint`・`db:local` などのコマンド |
| `wrangler.jsonc` / `wrangler.toml` | Cloudflare Workers のアプリか。D1などの接続先 |
| `.github/workflows/` | 公開の自動化（`deploy`）、プレビュー環境（`preview`）があるか |
| `migrations/` | データの表の定義。新しいSQLファイルを足す場所 |
| `public/`・`src/` | 画面と、API（サーバー側）のコード |

## 判断の目安

- 起動コマンドが `package.json` にあれば、それを使う。なければ README に従う。分からなければ利用者に聞く
- テストコマンド（`npm test` など）があれば、まずそれを実行する。なければ app-test の確認項目を手で行う
- データの表を変えるときは、`migrations/` に新しいファイルを足す（既存のファイルは変えない）
- プレビュー環境のワークフローがなければ、PRの確認はlocalhostの結果とPRの差分で行い、その旨を利用者に伝える
