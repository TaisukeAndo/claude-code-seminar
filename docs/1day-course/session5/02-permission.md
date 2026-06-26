# 2. permission（パーミッション）

## このセクションで学ぶこと

- permission とは何か（定義）
- なぜ permission を学ぶのか、permission があると何が変わるのか
- permission のセキュリティ面での利点
- Hooks と permission の違いと連携

## permission とは何か

Claude Code には「permission（パーミッション）」という仕組みがあります。

::: info permission の定義
permission とは「Claude Code が何をしていいか・してはいけないかを決めるルール」です。  
たとえば「このコマンドは実行してもいい」「このファイルは読み込んでいいが変更は不可」「ウェブへのアクセスは禁止」といったことを、あらかじめ細かく設定できます。
:::

設定は 3 種類で管理します。

| 設定の種類 | 意味 |
|---|---|
| Allow（許可） | その操作をしてよい |
| Ask（確認） | その操作をする前に人間に確認する |
| Deny（禁止） | その操作を禁止する |

ソース：[Configure permissions - Claude Code Docs](https://code.claude.com/docs/en/permissions)

## なぜ学ぶのか・何が変わるか

::: warning 重要なポイント
permission のルールは Claude の **AI モデルではなく、Claude Code のシステムが強制**します。  
プロンプトや CLAUDE.md で「やらないで」と書くだけでは制限できません。必ず permission 設定で行う必要があります。
:::

つまり、お願いベースの「やらないでね」ではなく、システムが物理的に止める「できない」を作れるのが permission です。これを学ぶことで、Claude Code に任せられる範囲を安全に決められるようになります。

ソース：[Configure permissions - Claude Code Docs](https://code.claude.com/docs/en/permissions)

## permission のセキュリティ面での利点

permission を設定すると、Claude Code が「やろうとしても物理的にできないこと」を決められます。

| 利点 | 内容 |
|---|---|
| 意図しない操作の防止 | Deny ルールを設定すると、そのツールやコマンドは Claude の AI モデルの判断に関係なく、システムレベルで実行が止まります。プロンプトで「やらないで」と指示するより確実です。 |
| 最小権限の原則の実践 | 必要な操作だけを許可（Allow）し、それ以外はすべて禁止（Deny）するという「最小権限の原則」を簡単に実現できます。万一システムに侵入されても、Claude を通じてできることを最小限に抑えられます。 |
| 組織全体のポリシー強制 | チームや組織全体で同じ permission ルールを `settings.json` で管理し、全員に適用できます。個人の設定ミスによるリスクを減らせます。 |
| 階層的な上書き防止 | 管理者設定（Managed Settings）を使うと、ユーザーが設定を変更しても上書きできないルールを作れます。 |

::: tip 最小権限の原則とは
「必要なことだけを許可し、それ以外はすべて禁止する」という考え方です。  
Claude Code では、使う操作だけを Allow にして、それ以外を Deny にすることで実践できます。
:::

ソース：[Configure permissions - Claude Code Docs](https://code.claude.com/docs/en/permissions)、[Understanding Claude Code Permissions and Security Settings](https://www.petefreitag.com/blog/claude-code-permissions/)

## Hooks と permission の違いと連携

Hooks と permission は、どちらもセキュリティに使えますが役割が異なります。

| 観点 | permission | Hooks |
|---|---|---|
| 性質 | 「何を許可・禁止するか」という**静的なルール設定** | 「操作の直前・直後に何かを実行する」という**動的な自動処理** |
| 主な役割 | できること・できないことの線引き | 線引きに加えて、ログ記録やマスクなどの自動処理 |

**連携のしくみ（事実）：**
- Hooks の PreToolUse（ツール実行前）を使うと、ツール実行前にカスタムのアクセス制御（権限チェック）を行えます。ただし、Hooks が Allow を返しても Deny ルールは上書きされません。両者は補い合って働きます。
- Hooks は permission システムの PreToolUse フックを通じて拡張機能として動作します。permission の枠組みの中に Hooks が位置づけられており、Hooks による Deny は permission ルールとして扱われます。

ソース：[Configure permissions - Claude Code Docs](https://code.claude.com/docs/en/permissions)

## このセクションのまとめ

- permission は「許可・確認・禁止」の 3 種類で、Claude Code にできること・できないことをシステムレベルで決めるルールです。
- permission は AI モデルではなくシステムが強制するため、プロンプトでのお願いより確実です。
- Hooks は動的、permission は静的という違いがあり、両者は補い合います。

::: tip 次のセクションへ
次の **3. .envファイル** では「守るべき秘密情報をどこに置くか」を学びます。  
permission は「どのファイルを読んでよいか」を決められますが、その「守るべき秘密情報」がどこにあるかが決まっていないと、守りようがありません。.env ファイルはその前提となる設定ファイルです。
:::
