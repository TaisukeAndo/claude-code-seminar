# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## このリポジトリについて

「Claude Code セミナー環境」として構築された、AI秘書業務のための Claude Code 設定リポジトリ。
アプリケーションのソースコードは無く、`.claude/` 配下の **skills（スキル）・agents（サブエージェント）・
hooks（フック）・rules（文体ルール）** が本体。ユーザーの自然な日本語の依頼（「報告書を作って」
「議事録にまとめて」等）に応じて、該当スキルが自動トリガーされ、Word/Excel/PowerPoint 生成、
メール下書き作成、カレンダー空き確認などを行う。

ビルド・lint・単体テストの仕組みは存在しない。動作確認は各スキルの Python スクリプトを
`python3` で直接実行して行う（後述）。

## ディレクトリ構成

```
.claude/
├── rules/
│   └── writing_style.md        ← 全ドキュメント生成に適用される文体ガイド（必読・厳守）
├── agents/                     ← スキルから呼び出されるサブエージェント（Markdown指示書）
│   ├── web-researcher.md          汎用リサーチ（docx-creator等から呼び出し）
│   ├── excel-structure-researcher.md  未定義Excelの構成リサーチ（xlsx-creatorから呼び出し）
│   ├── image-researcher.md        挿入画像の収集（著作権フリー画像のみ）
│   └── speakerdeck-referencer.md  Speaker Deckからデザイン参考PDFを収集
├── skills/
│   ├── docx-creator/            Word文書生成（report/proposal/minutes/manual/seminar）
│   ├── gdoc-minutes-creator/     文字起こし→議事録→Google Docsとしてアップロード
│   ├── mail-reply-drafter/       Gmail/Outlook未読メールの返信下書き自動作成
│   └── calendar-availability-checker/  Google/Outlookカレンダーの空き時間抽出
├── hooks/
│   ├── session-start.sh         セッション開始時に利用可能スキルと参照ファイル状況を通知
│   ├── block-dangerous.sh       危険コマンド・PII直接アクセスをBashレベルで拒否
│   └── file-notify.sh           .pptx/.docx書き込み後に自動でファイルを開く
└── settings.json / settings.local.json  権限（allow/deny）とフック登録

output/   ← ユーザーに渡す最終成果物（生成したファイル・Markdown等）の保存先
tmp/      ← 作業用の一時ファイル置き場（旧・過去生成物が残っている場合がある）
```

各スキルディレクトリの内部構成（存在するもののみ）:
- `SKILL.md` — トリガー条件とワークフローの定義（frontmatterの`description`が自動起動の判定に使われる）
- `scripts/` — 決定的な処理（JSON→ファイル生成、日時計算等）をPythonに任せる部分
- `config/` — 署名・通知先チャンネル・対象カレンダーIDなど、ユーザーが直接編集してよい設定
- `templates/` / `references/` / `assets/` — スキルによっては雛形ドキュメントやロゴ・画像を配置

## 成果物の出力先

ユーザー向けの最終ファイル（生成した .docx/.pptx/.xlsx、まとめのMarkdown等）は
**`output/` フォルダに保存する。** スクリプト実行時の中間ファイル・作業用JSONなどは
スクラッチ領域（またはやむを得ない場合は `tmp/`）に置き、成果物と混在させない。
`tmp/` は過去の名残の作業フォルダであり、新規の最終成果物の置き場としては使わない。

## よく使うコマンド

```bash
# document.json から Word ファイルを生成（docx-creator / gdoc-minutes-creator共通仕様）
python3 .claude/skills/docx-creator/scripts/create_docx.py <input.json> <output.docx>

# カレンダーの空き時間を計算（busy_intervals入りJSONを渡す）
python3 .claude/skills/calendar-availability-checker/scripts/compute_free_slots.py <input.json>
```

xlsx-creator / pptx-creator は `session-start.sh` フックが存在を前提に参照件数を表示するが、
本リポジトリには未実装（`.claude/skills/` 配下に該当ディレクトリが無い）。これらのスキルを
使う依頼が来た場合は、既存スキル（docx-creator等）の構成パターンを参考に新規実装が必要。

## アーキテクチャ上の要点

- **スキルの自動トリガー**: スキル選択はユーザー発言とSKILL.mdの`description`のマッチングで
  決まる。新しいスキルを追加する際は、`description`にトリガーとなる口語表現を具体的に列挙すること
  （既存スキルのSKILL.mdを参照）。
- **サブエージェントはスキルの内部実装**: `.claude/agents/*.md` はユーザーが直接呼ぶものではなく、
  スキルのワークフロー中で「〜を読み、以下の条件でリサーチしてください」という形で指示書として
  参照される。呼び出し元は入力パラメータとJSON出力フォーマットの契約を守る。
- **重い計算はPythonに委譲**: 日時のマージ・重複判定（compute_free_slots.py）やdocument.json→docx
  変換（create_docx.py）はLLMが暗算せずスクリプトに任せる設計。新しいスキルでも決定的な処理は
  同様にスクリプト化する。
- **PII・機密情報はBashから直接触らせない**: `invoice-creator/clients/`や`.env`等はhook
  （`block-dangerous.sh`）とpermissions（`settings.json`のdeny）の二重でBash直接アクセスを
  遮断し、Pythonスクリプト経由の読み込みのみ許可する設計思想。新しい機密データを扱う場合も
  この方式に倣う。
- **文体ルールは全スキル共通で強制**: `.claude/rules/writing_style.md`はdocx-creator等の
  ドキュメント生成スキルから明示的に参照されており、AI特有の紋切り型表現（「〜の世界へ」
  「包括的な」等）を禁止し、簡潔・具体的な文章を求めている。文書・メール文面を生成する際は必ず従うこと。
- **Google Docs編集APIの制約**: gdoc-minutes-creatorはGoogle Docs本文の直接編集APIが
  存在しないため、python-docxでローカルに.docxを整形してからGoogle Driveにアップロードし
  自動変換させる方式を取っている（既存Google Docsへの追記は非対応）。
