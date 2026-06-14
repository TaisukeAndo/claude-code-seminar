# 1. Hooks（フック）

## このセクションで学ぶこと

- Hooks とは何か（定義）
- なぜ Hooks を学ぶのか、Hooks があると何が変わるのか
- Hooks のセキュリティ面での利点

## Hooks とは何か

Claude Code には「Hooks（フック）」という仕組みがあります。

::: info Hooks の定義
Hooks とは、Claude Code が何かをする「直前」や「直後」に、**自動的に動く命令**のことです。  
たとえば「ファイルを削除しようとしたとき、必ず確認を求める」「作業内容を自動でログに記録する」といったルールをあらかじめ設定しておける仕組みです。  
Claude Code が動くたびに、人間が毎回チェックしなくても自動でルールが働きます。
:::

設定ファイル（`.claude/settings.json`）に書いておくことで有効になります。動くタイミングは細かく指定でき、代表的なものは次のとおりです。

| タイミングの名前 | いつ動くか |
|---|---|
| PreToolUse | Claude Code がツールを実行する「前」 |
| PostToolUse | Claude Code がツールを実行した「後」 |
| SessionStart | 作業（セッション）を開始したとき |

ソース：[Hooks reference - Claude Code Docs](https://code.claude.com/docs/en/hooks)

## なぜ学ぶのか・何が変わるか

Hooks を使う前は、危険な操作やうっかりミスを防ぐために、人間が毎回画面を見て判断する必要がありました。Hooks を設定すると、その判断をルールとして自動化できます。

::: tip ポイント
「気をつける」を「自動で気をつけてくれる」に変えられるのが、Hooks を学ぶ意味です。
:::

## Hooks のセキュリティ面での利点

Hooks を使うと、Claude Code が操作を実行する前（PreToolUse）に自動でチェックを走らせることができます。

| 利点 | 内容 |
|---|---|
| 危険な操作の自動ブロック | `rm -rf`（全ファイル削除）や本番環境への変更など、あらかじめ「危険」と定めたコマンドを自動で止められます。人間がうっかり見逃しても、Hooks が防いでくれます。 |
| 機密情報の自動マスク | PostToolUse フックを使うと、ツールの実行結果に含まれるパスワードや API キーなどをマスクして表示させないようにできます。 |
| 監査ログの自動記録 | 誰がいつ何を操作したかを自動でログファイルに残せます。問題が起きたときの調査に役立ちます。 |
| 環境の安全検証 | 「main ブランチには直接プッシュしない」などのルールを Hooks で強制できます。 |

::: info ポイント
これらが「人間の判断を毎回必要とせず、自動で動く」ことが重要です。  
良いやり方をルール化して、常に機能させられます。
:::

ソース：[Hooks reference - Claude Code Docs](https://code.claude.com/docs/en/hooks)、[Claude Code Hooks: The Deterministic Control Layer for AI Agents - Dotzlaw Consulting](https://www.dotzlaw.com/insights/claude-hooks/)

## このセクションのまとめ

- Hooks は、Claude Code の動作の「直前・直後」に自動で動く命令で、危険な操作のブロックや監査ログなどに使えます。
- Hooks は「操作のたびに自動で何かを実行する」**動的な仕組み**です。

::: tip 次のセクションへ
次の **2. permission** では「そもそも何を許可・禁止するか」をあらかじめ決めるルールを学びます。  
Hooks が「操作のたびに何かを実行する仕組み」だったのに対し、permission は**静的なルール設定**です。両者がどう連携するかも見ていきます。
:::
