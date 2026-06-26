# まとめ

**所要時間: 約 5 分**

---

## 3.24. このセッションで行ったこと

**導入ワーク（3.1.〜3.4.）**
- セッション終了時の完成形（KPI管理表・見積書の自動生成）を確認した
- 「普段の Excel 活用」をグループで話し合い、手作業になっている工程を言語化した
- 自分の Excel 作成フローを書き出した

**xlsx-creator スキル設計（3.5.〜3.8.）**
- Excel 作成の 3 つの課題（数値収集・構成設計・フォーマット整形）を確認した
- web-researcher と excel-structure-researcher の 2 種類のサブエージェントが役割分担していることを理解した
- KPI管理・タスク管理・帳票・その他の 4 タイプに自動対応していることを確認した

**xlsx-creator ハンズオン（3.9.〜3.13.）**
- `npx degit` でスキルとエージェントをダウンロードした
- Claude Code を使って KPI管理表や業務 Excel を自動生成した
- 修正指示の出し方を確認した

**会計処理ワーク（3.14.〜3.16.）**
- 普段の帳票作業（見積書・請求書・経費精算）をグループで話し合った
- 自分が使っている会計ソフトを確認した

**invoice-creator スキル設計（3.17.〜3.18.）**
- MCP と API の違いを整理した
- 会計データの書き込みに API を使う理由（精密さ・書き込み制限）を理解した
- invoice-creator スキルの処理フロー（ヒアリング → JSON → 出力）を確認した

**invoice-creator ハンズオン（3.19.〜3.23.）**
- スキルをダウンロードして .env ファイルに自社情報を設定した
- 見積書を Excel 形式で生成した
- 使用する会計ソフトに応じて API キーを設定した（マネーフォワード・freee・弥生会計）

---

## 3.25. 重要なポイントの整理

::: info ポイント 1：「調べる」と「作る」をサブエージェントで分ける
xlsx-creator では web-researcher が業界データを収集し、excel-structure-researcher が構成を設計する。  
役割を分けることで、メインのスキルが精度の高い Excel を生成できる。
:::

::: info ポイント 2：MCP と API は得意・不得意が違う
MCP はテキストで柔軟に指示できるが、書き込みに制限があることが多い。  
API は操作を細かく指定できるため、金銭が絡む会計データの書き込みに向いている。
:::

::: info ポイント 3：個人情報は AI に渡さない設計
invoice-creator は住所・口座番号などの個人情報を .env ファイルと clients/*.json で管理し、  
Claude（LLM）には渡さない設計になっている。この原則は自分でスキルを作るときにも応用できる。
:::

::: info ポイント 4：スキルは使いながら育てる
「毎回同じ言葉でトリガーしている」「毎回同じ設定を指示している」と気づいたら  
SKILL.md を編集してスキル側に組み込む。使うたびに自分の業務に最適化されていく。
:::

---

## 3.26. 今日使ったコマンドの一覧

```bash
# プロジェクトフォルダに移動する
cd ~/Desktop/claude-code-seminar

# エージェントフォルダのダウンロード（Session 2 で実施済みの場合はスキップ）
npx degit TaisukeAndo/claude-code-seminar/.claude/agents .claude/agents

# xlsx-creator スキルのダウンロード
npx degit TaisukeAndo/claude-code-seminar/packages/skills/xlsx-creator .claude/skills/xlsx-creator

# invoice-creator スキルのダウンロード
npx degit TaisukeAndo/claude-code-seminar/packages/skills/invoice-creator .claude/skills/invoice-creator

# ダウンロードされたフォルダの確認
ls .claude/skills/xlsx-creator/
ls .claude/skills/invoice-creator/

# .env ファイルの作成（自社情報の設定）
cp .claude/skills/invoice-creator/.env.example .claude/skills/invoice-creator/.env

# 依存ライブラリのインストール
pip3 install openpyxl

# Claude Code を起動する
claude
```

---

## 3.27. 参考文献

### Anthropic 公式ドキュメント

1. **Claude Code — 概要とセットアップ**  
   Claude Code の機能・インストール方法・基本操作の公式リファレンスです。  
   https://docs.anthropic.com/en/docs/claude-code/overview

2. **マルチエージェントシステムの構築**  
   複数の AI エージェントを連携させる設計パターンを解説しています。  
   xlsx-creator スキルの web-researcher・excel-structure-researcher による役割分担設計の理論的根拠となる章です。  
   https://docs.anthropic.com/en/docs/build-with-claude/agents

3. **プロンプトエンジニアリングガイド — 効果的な指示の書き方**  
   AI に高品質な出力を生成させるための指示（プロンプト）の設計原則を解説しています。  
   「どんな情報を渡すと出力品質が上がるか」の理論的な裏付けとなる章です。  
   https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview

### ライブラリドキュメント

4. **openpyxl — Python で Excel ファイルを操作するライブラリ**  
   `xlsx-creator` と `invoice-creator` スキルが内部で使用しているライブラリの公式ドキュメントです。  
   https://openpyxl.readthedocs.io/en/stable/

### 会計ソフト API ドキュメント

5. **マネーフォワード クラウド API ドキュメント**  
   マネーフォワード クラウドシリーズの API 仕様です。invoice-creator との連携設定に使用します。  
   https://invoice.moneyforward.com/api/index.html

6. **freee API ドキュメント**  
   freee 会計・freee 請求書の API 仕様です。  
   https://developer.freee.co.jp/

7. **弥生会計 仕訳インポート仕様**  
   弥生会計への CSV 取り込み形式の仕様です。  
   https://support.yayoi-kk.co.jp/

### 関連情報

8. **degit — GitHub からフォルダをダウンロードするツール**  
   本セッションでスキルのダウンロードに使用した `npx degit` コマンドのドキュメントです。  
   https://github.com/Rich-Harris/degit

---

## 次のセッションに向けて

Session 4 では **定常業務の自動化** に取り組みます。  
Slack・Gmail・Google Tasks などの日常ツールと Claude Code を連携させ、  
毎日繰り返している確認・返信・タスク登録を自動化します。

このセッションで学んだ「スキルのダウンロード → .env の設定 → 使う → カスタマイズする」という流れは、Session 4 以降でも同じです。

[Session 4: 定常業務の自動化](/1day-course/session4/) へ進む
