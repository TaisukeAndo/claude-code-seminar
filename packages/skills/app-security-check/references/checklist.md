# 点検の観点（A〜H）

各項目は「何を見るか」「探し方（読み取りだけのコマンド）」「問題ありのときの重さの目安」の順に書く。
コマンドは手がかりを見つけるためのもので、当たった箇所は必ずコードを読んで判断する（当たらないことは安全の証明にならない）。

## A. 秘密情報の置き場所

| # | 見ること | 探し方 | 重さの目安 |
|---|---|---|---|
| A1 | APIキー・トークン・パスワードが、コードや設定ファイルに直接書かれていないか | `git grep -nIiE "(api[_-]?key|secret|token|passw(or)?d|bearer |sk-[a-z0-9]|ghp_|AKIA)" -- . ':!package-lock.json'` | 重大 |
| A2 | `.env`・`.dev.vars` などの秘密のファイルが、GitHubに上がっていないか | `git ls-files \| grep -iE "(^|/)\.env|\.dev\.vars"`、`.gitignore` の中身 | 重大 |
| A3 | 過去のコミットに、秘密のファイルが残っていないか | `git log --all --oneline -- .env .dev.vars '*.env'` | 重大（残っていたら、キーを無効にして作り直す必要がある。履歴から消すだけでは足りない） |
| A4 | 画面側（`public/` などブラウザに送られるファイル）に、秘密のキーが入っていないか | `git grep -nIiE "(api[_-]?key|secret|token)" -- public/` | 重大 |
| A5 | 秘密の値を、Wrangler の secret（`wrangler secret put`）や GitHub の Secrets に置いているか | `wrangler.jsonc` の `vars` に秘密が入っていないか読む | 要対応 |

A2の例外: `.env.example` のように `.example` で終わるファイルは、値が空のひな形であれば問題なし。

A4の例外: Firebase の設定値（`apiKey`、`authDomain`、`projectId` など）は、画面に置く前提の値で、秘密ではない。
問題にはしないが、Firebase コンソールで「承認済みドメイン」が自分のアプリのドメインだけになっているかを、利用者に確認してもらう。

## B. 入力値の扱い

| # | 見ること | 探し方 | 重さの目安 |
|---|---|---|---|
| B1 | データベースへの命令（SQL）に、利用者の入力をつなげて埋め込んでいないか（SQLインジェクション） | `git grep -nE "prepare\(\s*\`" -- src/`、`git grep -nE "prepare\([^)]*\+" -- src/` で当たった箇所を読み、値が `.bind()` で渡されているか確かめる | 重大 |
| B2 | 利用者が入力した文字を、画面にHTMLとして埋め込んでいないか（他の人の画面で不正なスクリプトが動く原因になる） | `git grep -nE "innerHTML|outerHTML|insertAdjacentHTML|document\.write" -- public/ src/` | 入力が他の人の画面に表示されるなら重大、自分の画面だけなら要対応 |
| B3 | 入力の長さ・形式・必須のチェックを、サーバー側で行っているか（画面側のチェックだけでは、APIを直接呼ばれると素通りする） | APIの処理を読む | 要対応 |

## C. アクセス制御（誰が何をできるか）

1章で作ったAPIの一覧を使う。

| # | 見ること | 重さの目安 |
|---|---|---|
| C1 | 登録・変更・削除のAPI（POST／PUT／PATCH／DELETE）を、ログインせずに誰でも呼べないか | アプリが公開されていて、他人のデータを消せるなら重大。1人で使う前提なら要対応 |
| C2 | IDを指定してデータを取得・変更・削除する箇所で、「そのデータの持ち主か」を確かめているか（例: `WHERE id = ? AND user_id = ?`）。URLのIDを書き換えると他人のデータを扱えないか | ログイン機能があるなら重大 |
| C3 | 管理用の画面やAPIが、URLを知っていれば誰でも開けないか | 重大 |
| C4 | 利用者IDを、画面から送られてきた値のまま信じていないか（サーバー側で、IDトークンから取り出しているか） | 重大 |

## D. ログインの確かめ方（ログイン機能がある場合）

| # | 見ること | 重さの目安 |
|---|---|---|
| D1 | サーバー側で、IDトークン（ログインした証拠のデータ）が本物かを確かめているか。中心になるのは、署名・発行元・対象・有効期限（細かい条件は D2） | 確かめていなければ重大 |
| D2 | Firebase の IDトークンの場合、公式の条件をすべて確かめているか。ヘッダー: 方式（`alg`）が `RS256`、鍵の番号（`kid`）が Google の公開鍵の一覧にある。中身: 有効期限（`exp`）が未来、発行時刻（`iat`）とログイン時刻（`auth_time`）が過去、対象（`aud`）が `<プロジェクトID>`、発行元（`iss`）が `https://securetoken.google.com/<プロジェクトID>`、利用者ID（`sub`）が空でない。署名は Google の公開鍵（`https://www.googleapis.com/robot/v1/metadata/x509/securetoken@system.gserviceaccount.com`）で確かめる | 1つでも欠けていれば重大。最新の条件は Firebase 公式ドキュメント「Verify ID tokens」で確かめる |
| D3 | Cookie にログイン情報を入れる場合、`HttpOnly`・`Secure`・`SameSite` が付いているか | 要対応 |
| D4 | IDトークンや利用者の個人情報を、`console.log` などのログに出していないか | 要対応 |

Cloudflare Workers では、Firebase の公式の管理用ライブラリ（firebase-admin）がそのままでは動かないため、
JWT を確かめるライブラリ（`jose` など）で上の4項目を自分で確かめる形になる。ライブラリに任せた場合も、
発行元と対象を指定しているかを必ず読む。

## E. エラー表示とログ

| # | 見ること | 重さの目安 |
|---|---|---|
| E1 | エラーのとき、内部の情報（SQL文、エラーの詳細、環境変数）を、そのまま画面やAPIの応答に返していないか | 要対応 |
| E2 | `ctx.passThroughOnException()` でエラーを隠していないか | 任意 |

## F. 依存パッケージ（アプリが使っている部品）

| # | 見ること | 探し方 | 重さの目安 |
|---|---|---|---|
| F1 | 既知の脆弱性がある版を使っていないか | `npm audit --json`（`package-lock.json` があるとき。読み取りだけ。`npm audit fix` は実行しない） | critical・high は重大、moderate は要対応、low は任意 |
| F2 | `package-lock.json` がGitHubに上がっているか（なければ、入る版が実行のたびに変わる） | `git ls-files package-lock.json` | 任意 |
| F3 | 使っていないパッケージが残っていないか | `package.json` と `import` を突き合わせる | 任意 |

F1 で見つかったものは、直し方として「app-dependency-update スキルで、安定した修正版に上げる」を案内する。

## G. Cloudflare Workers 固有

G1〜G3 は Cloudflare 公式の `workers-best-practices` スキル（「Anti-Patterns to Flag」の表と、その参照先）に基づく。G4 はこのSkill独自の追加。
Cloudflare Workers のアプリでなければ、G はすべて「該当なし」とする。

| # | 見ること | 探し方 | 重さの目安 |
|---|---|---|---|
| G1 | 秘密に使う値やIDを `Math.random()` で作っていないか（予測できる。`crypto.randomUUID()` や `crypto.getRandomValues()` を使う） | `git grep -n "Math.random" -- src/` | 要対応 |
| G2 | 秘密の値を `===` で比べていないか（比べる時間の差から推測される。`crypto.subtle.timingSafeEqual` を使う） | 秘密の比較箇所を読む | 任意 |
| G3 | リクエストごとの情報（利用者IDなど）を、関数の外の変数に入れていないか（別の人のリクエストに混ざる） | `src/` の一番外側で `let` で宣言された変数を読む | 要対応 |
| G4 | `Access-Control-Allow-Origin: *` と、ログイン情報の受け渡しを組み合わせていないか | `git grep -n "Access-Control-Allow" -- src/` | 要対応 |

## H. 公開の設定

| # | 見ること | 重さの目安 |
|---|---|---|
| H1 | プレビュー環境と本番環境が、同じデータベースを使っていないか（確認用の操作で本番のデータが変わる） | 要対応 |
| H2 | 公開の自動処理（`.github/workflows/`）で、秘密の値を `echo` などでログに出していないか | 重大 |
