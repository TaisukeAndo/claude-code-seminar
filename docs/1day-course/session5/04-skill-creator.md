# 4. skill-creator（スキルクリエーター）

## このセクションで学ぶこと

- skill-creator とは何か（定義）
- なぜ skill-creator を学ぶのか、skill-creator があると何が変わるのか
- skill-creator のインストール手順
- skill-creator で何ができるか

## skill-creator とは何か

::: info skill-creator の定義
skill-creator とは「**スキルを作るためのスキル**」です。  
Anthropic が公式に提供しているツールで、自分だけのスキル（Claude Code に特定の作業を自動化させる命令セット）をゼロから作ったり、すでにあるスキルを改善したりするのを手伝ってくれます。  
「どんなスキルを作りたいか」を Claude Code に伝えると、設計・テスト・改善を一緒にやってくれます。
:::

スキルは `SKILL.md` というマークダウンファイルで定義します。skill-creator はそのファイルの作成から、テストケースの実行、品質評価、改善まで、スキル開発の全サイクルをサポートします。

ソース：[skills/skills/skill-creator/SKILL.md - GitHub anthropics/skills](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md)

## なぜ学ぶのか・何が変わるか

これまで毎回手順を説明していた作業を、一度「スキル」として登録すれば、Claude Code がそれを覚えて自動でこなしてくれるようになります。skill-creator を使うと、プログラミングの知識がなくても、「自分専用のスキル」を体系的に作れるようになります。

そして、第 1 章から第 3 章で学んだセキュリティ基盤（Hooks・permission・.env ファイル）が、ここで活きてきます。

| 準備するもの | 役割 |
|---|---|
| Hooks | 危険な操作を自動でブロックする |
| permission | 実行できるコマンドの範囲を絞る |
| .envファイル | 秘密情報をコードから分離する |

::: warning セキュリティ基盤が前提
これら 3 つを理解・設定しておくことが、skill-creator を使う前の基礎知識となります。
:::

## skill-creator のインストール手順

skill-creator は以下のコマンドでインストールします。

```bash
npx degit anthropics/skills/skills/skill-creator .claude/skills/skill-creator
```

このコマンドは、GitHub の `anthropics/skills` リポジトリから `skill-creator` フォルダだけを取り出し、現在のプロジェクトの `.claude/skills/skill-creator` ディレクトリに保存します。`npx degit` を使うため、Git のインストール履歴を引き継がずにファイルだけをダウンロードできます。

**手順：**
1. ターミナル（コマンドプロンプト）を開く
2. skill-creator を使いたいプロジェクトのフォルダに移動する
3. 上記のコマンドを実行する
4. `.claude/skills/skill-creator` フォルダが作成されたことを確認する
5. Claude Code を起動すると、skill-creator が使えるようになる

ソース：[GitHub - anthropics/skills](https://github.com/anthropics/skills)

::: tip 補足（参考情報）
公式サイトや一部のドキュメントでは、上記とは別に `npx skills add` という形式のインストールコマンドが案内されている場合もあります。  
この資料では、要件で指定された `npx degit` 形式のコマンドを採用しています。`npx degit` 形式は技術的に有効で、リポジトリの構造とも整合しています。
:::

## skill-creator で何ができるか

skill-creator は「スキルを作るためのスキル（メタスキル）」です。できることは次のとおりです。

| できること | 内容 |
|---|---|
| ゼロからスキルを作成 | どんなスキルを作りたいかを Claude Code に伝えると、仕様の決定・SKILL.md ファイルの作成・テストケースの設計まで一緒にやってくれます。 |
| 既存スキルの改善 | すでにあるスキルの動作を確認し、フィードバックをもとに改善できます。 |
| テストと品質評価 | スキルを使ったときと使わなかったときの結果を並べて比較し、定量的な評価（成功率・処理時間・使用トークン数）で品質を測れます。 |
| 説明文の最適化 | スキルが正しいタイミングで呼び出されるように、トリガー文章を繰り返しテストして精度を高められます。 |

::: info まとめ
プログラミングの知識がなくても「Claude Code に覚えさせたい作業」を体系的にスキル化できるツールです。
:::

ソース：[Anthropic/skill-creator - officialskills.sh](https://officialskills.sh/anthropics/skills/skill-creator)、[Skill Creator - claudemarketplaces.com](https://claudemarketplaces.com/skills/anthropics/claude-plugins-official/skill-creator)

## このセクションのまとめ

- skill-creator は「スキルを作るためのスキル」で、ゼロからの作成・改善・テスト・説明文の最適化ができます。
- インストールは `npx degit anthropics/skills/skills/skill-creator .claude/skills/skill-creator` で行います。
- 安全に使うために、第 1 章から第 3 章のセキュリティ基盤が前提になります。

::: tip 次のセクションへ
次の **5. まとめ** では、ここまでの内容全体を振り返り、4 つの要素がどうつながっているかを整理します。
:::
