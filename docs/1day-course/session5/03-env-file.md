# 3. .envファイル

## このセクションで学ぶこと

- .env ファイルとは何か（定義）
- なぜ .env ファイルを学ぶのか、.env ファイルがあると何が変わるのか
- .env ファイルのセキュリティ面での利点
- permission と組み合わせた保護

## .envファイルとは何か

::: info .envファイルの定義
.env ファイルとは、API キーやパスワードなどの「秘密情報」をコード本体から切り離して保管するための設定ファイルです。  
ファイル名の先頭にある「.（ドット）」は「隠しファイル」を意味します。このファイルの中に秘密情報を書いておき、プログラムはここから読み取ります。  
コード自体には秘密情報を書かずに済むため、GitHub などにコードを公開しても秘密情報が漏れにくくなります。
:::

**この資料に出てくる用語の補足：**
- **API キー**：外部のサービスを利用するための「合言葉のような鍵」です。他人に知られると、自分の権限で勝手にサービスを使われてしまいます。
- **GitHub**：コードをインターネット上で保存・共有できるサービスです。
- **.gitignore**：GitHub などにアップロードしたくないファイルを書いておくリストのことです。

ソース：[Best Practices for Environment Variables Secrets Management - GitGuardian](https://blog.gitguardian.com/secure-your-secrets-with-env/)

## なぜ学ぶのか・何が変わるか

秘密情報をコードに直接書いてしまうと、そのコードを共有・公開した瞬間に秘密情報まで一緒に広まってしまいます。.env ファイルを学ぶと、秘密情報を「コードとは別の場所」にまとめて、共有から除外できるようになります。

**補足：**
- .env ファイル自体は `.gitignore` というリストに追加することで、GitHub などにアップロードされないように除外します。
- チームメンバーには「`.env.example`」というサンプルファイル（実際の値は書かない）を共有して、何の設定が必要かだけ伝えます。

ソース：[Best Practices for Environment Variables Secrets Management - GitGuardian](https://blog.gitguardian.com/secure-your-secrets-with-env/)

## .envファイルのセキュリティ面での利点

| 利点 | 内容 |
|---|---|
| コードへの直接記述を防ぐ | API キーをコードに直接書くと、GitHub にアップした瞬間に世界中から見える状態になります。.env ファイルに分離し、`.gitignore` でバージョン管理から除外することで、この漏洩リスクを防げます。 |
| 影響範囲の限定 | OS の環境変数として設定すると他のアプリにも影響しますが、.env ファイルはそのプロジェクトの実行中のみ使用されます。被害範囲を最小化できます。 |
| 発見されにくい場所への保管 | ファイルをプロジェクトのルートディレクトリ外に配置することで、サーバーの設定ミスがあっても発見されにくくなります。 |
| Claude Code と組み合わせた保護 | permission で `.env` ファイルへの読み取りを `Read(./.env)` の Deny ルールで禁止することで、Claude Code が誤って .env の内容を読み上げたり漏洩させるリスクを防げます。 |

ソース：[Best Practices for Environment Variables Secrets Management - GitGuardian](https://blog.gitguardian.com/secure-your-secrets-with-env/)、[How Does .env Protect Sensitive Information? - Medium](https://medium.com/@uyanhewagetr/how-does-env-protect-sensitive-information-7902b43b28c7)

## permission と組み合わせた保護

前のセクションで学んだ permission と、この章の .env ファイルは組み合わせて使うと効果的です。

- .env ファイルに API キーや設定値を記述し、permission ルールでそのファイルへのアクセス可否（例：`Read(./.env)` を Deny にする）を制御します。
- .env に何を入れるかが決まってはじめて、permission で保護する対象が定まります。

::: tip .envファイルは permissionの前提
「どの秘密情報を守るか」を .env ファイルで決め、「どう守るか」を permission で決める、という流れです。  
.env ファイルは permission の前提となる設定ファイルです。
:::

ソース：[Configure permissions - Claude Code Docs](https://code.claude.com/docs/en/permissions)

## このセクションのまとめ

- .env ファイルは、秘密情報をコードから切り離して保管する設定ファイルです。
- `.gitignore` で除外することで、秘密情報の漏洩リスクを減らせます。
- permission の `Read(./.env)` の Deny ルールと組み合わせると、Claude Code からの漏洩も防げます。

::: tip 次のセクションへ
第 1 章から第 3 章で学んだ「Hooks・permission・.env ファイル」の 3 つは、合わせて**セキュリティ基盤**となります。  
次の **4. skill-creator** では、このセキュリティ基盤を前提として、いよいよ自分でスキルを作ります。
:::
