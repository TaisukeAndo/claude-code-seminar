# まとめ

**所要時間: 約 5 分**

---

## 2.24. このセッションで行ったこと

**導入ワーク（2.1.〜2.4.）**
- セッション終了時の完成形を確認した
- 「ドキュメント作成の課題」をグループで話し合い、共通の問題を言葉にした
- 自分のドキュメント作成フローを書き出した

**DOCX 設計（2.5.〜2.8.）**
- AI の出力品質が「渡す情報の量と質」によって変わることを確認した
- 企画書作成の現行フローと、AI に置き換えた場合のフローを比較した
- サブエージェントが情報収集を担う設計の理由を理解した

**DOCX ハンズオン（2.9.〜2.13.）**
- `npx degit` コマンドを使って GitHub からスキルをダウンロードした
- Claude Code を起動して Word ファイルの自動生成を実行した
- 具体的な修正指示の出し方を練習した

**PPTX ワーク（2.14.〜2.16.）**
- 自分のスライド作成フローを言語化した

**PPTX 設計（2.17.〜2.18.）**
- スライド作成フローを整理し、どの部分を AI が担当するかを確認した
- PPTX スキルの内部処理（サブエージェントとエバリュエーター）の役割を理解した

**PPTX ハンズオン（2.19.〜2.23.）**
- アウトラインファイルを使ってスライドを自動生成した
- `SKILL.md` を編集してトリガー文言をカスタマイズする方法を確認した

---

## 2.25. 重要なポイントの整理

::: info ポイント 1：出力品質はコンテキストで決まる
目的・対象・ページ数・構成を明示することで出力の精度が上がる。
:::

::: info ポイント 2：修正指示は具体的に
「何が」「どのように」問題で「どうしてほしいか」を具体的に伝える。
:::

::: info ポイント 3：スキルは使いながら改善する
使うたびに気づいた点を `SKILL.md` に追記することで、自分の業務に合ったスキルに育てていく。
:::

::: info ポイント 4：サブエージェントで品質を保つ
情報収集をメインの処理から分離する設計が、コンテキスト汚染を防いで出力品質を維持している。
:::

---

## 2.26. 今日使ったコマンドの一覧

```bash
# プロジェクトフォルダに移動する
cd ~/Desktop/claude-code-seminar

# エージェントフォルダのダウンロード（セッション全体で最初に1回）
npx degit TaisukeAndo/claude-code-seminar/.claude/agents .claude/agents

# DOCX スキルのダウンロード
npx degit TaisukeAndo/claude-code-seminar/packages/skills/docx-creator .claude/skills/docx-creator

# PPTX スキルのダウンロード
npx degit TaisukeAndo/claude-code-seminar/packages/skills/pptx-creator .claude/skills/pptx-creator

# ファイル・フォルダの中身を確認する
ls .claude/skills/docx-creator/
ls .claude/skills/pptx-creator/

# Claude Code を起動する
claude
```

---

## 2.27. 参考文献

### Anthropic 公式ドキュメント

1. **Claude Code — 概要とセットアップ**  
   Claude Code の機能・インストール方法・基本操作の公式リファレンスです。  
   https://docs.anthropic.com/en/docs/claude-code/overview

2. **プロンプトエンジニアリングガイド — 効果的な指示の書き方**  
   AI に高品質な出力を生成させるための指示（プロンプト）の設計原則を解説しています。  
   本セッションの「コンテキストが品質を決める」という考え方の理論的な裏付けとなる章です。  
   https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview

3. **マルチエージェントシステムの構築**  
   複数の AI エージェントを連携させる設計パターンを解説しています。  
   本セッションのサブエージェント（情報収集担当）とエバリュエーター（品質チェック担当）の設計根拠となる章です。  
   https://docs.anthropic.com/en/docs/build-with-claude/tool-use/computer-use

### ライブラリドキュメント

4. **python-docx — Python で Word ファイルを操作するライブラリ**  
   `docx-creator` スキルが内部で使用しているライブラリの公式ドキュメントです。  
   https://python-docx.readthedocs.io/en/latest/

5. **python-pptx — Python で PowerPoint ファイルを操作するライブラリ**  
   `pptx-creator` スキルが内部で使用しているライブラリの公式ドキュメントです。  
   https://python-pptx.readthedocs.io/en/latest/

### 関連情報

6. **degit — GitHub からフォルダをダウンロードするツール**  
   本セッションでスキルのダウンロードに使用した `npx degit` コマンドのドキュメントです。  
   https://github.com/Rich-Harris/degit

---

## 次のセッションに向けて

Session 3 では **会計処理の自動化** に取り組みます。

このセッションで学んだ「スキルのダウンロード → 使う → カスタマイズする」という流れは、Session 3 以降でも同じです。

[Session 3: 会計処理の自動化](/1day-course/session3/) へ進む
