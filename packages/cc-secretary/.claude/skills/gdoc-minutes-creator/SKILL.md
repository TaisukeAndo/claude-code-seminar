---
name: gdoc-minutes-creator
description: >
  文字起こし（会議の音声起こしテキスト・トランスクリプト）から議事録を作成し、
  Google Docs形式でGoogle Driveに保存して、そのリンクをユーザーに返すスキル。
  ローカルのWordファイル（.docx）ではなく、Google Docs／Google Driveへの保存が
  目的のときに必ず使うこと。
  ユーザーが「文字起こしから議事録を作って」「この文字起こしをGoogle Docsの議事録にして」
  「議事録をGoogle Driveに保存して」「文字起こしをまとめてDriveに入れておいて」
  「さっきの会議のトランスクリプトを議事録化してリンクちょうだい」などと述べたときは
  必ずこのスキルを使うこと。単に「Wordで議事録を作って」「議事録をdocxで」など
  ローカルファイル・Word指定の場合は docx-creator スキルを使う（このスキルではない）。
---

# gdoc-minutes-creator スキル

文字起こしテキストを受け取り、テンプレートに沿って議事録を構成し、Word形式（.docx）で
組み立てたうえでGoogle Driveにアップロードし、Google Docsへ自動変換させる。
できあがったGoogle DocsのリンクをユーザーIC返す。

## なぜこの手順か

利用可能なGoogle Drive連携ツールには、Google Docsの本文を直接編集するAPI（段落の
差し込み・置換など）が無い。できるのは「新規ファイル作成」「既存ファイルのコピー」
「読み取り」のみ。そのため見出し・表・箇条書きなどの体裁を正しく再現するには、
docx-creator スキルと同じ方法（python-docxでの.docx生成）でローカルに整形済みの
Wordファイルを作り、それをDriveにアップロードして自動でGoogle Docsに変換させるのが
最も確実。plainテキストをそのままGoogle Docs化すると見出しや表が失われる。

## ディレクトリ構成

```
.claude/skills/gdoc-minutes-creator/
├── SKILL.md
├── templates/
│   └── standard.json      ← 議事録の骨組み（document.json形式）。用途が増えたら追加する
└── scripts/
    └── create_docx.py     ← document.json → .docx を生成（docx-creatorと同じ仕組み）
```

---

## ワークフロー

### Step 1: 文字起こしを受け取る

以下のいずれかで受け取る：
- チャットに直接貼り付けられたテキスト
- ローカルファイルのパス（.txt など）→ Read で読む
- 既存のGoogle Docs/Driveファイルへのリンクやファイル名 → `search_files` で探し、
  `read_file_content` で本文を取得する

長すぎて全文を一度に読み切れない場合は、章・話題のまとまりごとに分けて把握してから
要約する。憶測で内容を創作しないこと。文字起こしに無い情報（日時・出席者など）は
「不明」と記載するか、ユーザーに確認する。

### Step 2: テンプレートを選ぶ

```bash
ls .claude/skills/gdoc-minutes-creator/templates/
```

- テンプレートが1つしかない場合はそれを使う（現時点では `standard.json` のみ）
- 複数ある場合は一覧を示してユーザーに選んでもらう（会議の性質を聞いて提案してもよい）
- ユーザーが「もっとシンプルに」「決定事項だけ」など具体的な構成を口頭で指定した場合は、
  テンプレートを土台にしつつ自由に見出しやセクションを増減してよい。テンプレートは
  絶対のルールではなく骨組みである

### Step 3: 文字起こしから内容を抽出し document.json を作る

テンプレート（例: `templates/standard.json`）の `sections` 構造をお手本にしながら、
実際の内容で埋めた新しい document.json をスクラッチ領域に書き出す（テンプレート自体は
上書きしない）。

抽出のポイント：

| 項目 | 抽出方法 |
|------|----------|
| 会議名 | 文字起こし冒頭やユーザーの発言から。無ければユーザーに確認 |
| 日時 | 文字起こしに記載があれば使用。無ければ今日の日付か「不明」 |
| 出席者 | 発言者ラベル（「田中:」等）があればそこから拾う |
| 議題 | 話題の切り替わりから章立てする |
| 決定事項 | 「〜に決定」「〜で合意」等の発言を抽出。無ければ「特になし」 |
| 議論内容 | 議題ごとに要点を要約（一言一句の書き起こしにはしない） |
| アクションアイテム | 「〜さんが〜する」「次までに〜」等をタスク・担当者・期限の表にする |
| 次回予定 | 次回日程の言及があれば記載。無ければ「未定」 |

`metadata.doc_type` は必ず `"minutes"` にする（`create_docx.py` の見出しラベル解決に使われる）。

### Step 4: .docx を生成する

```bash
python3 .claude/skills/gdoc-minutes-creator/scripts/create_docx.py \
  /path/to/scratchpad/document.json \
  /path/to/scratchpad/議事録_YYYY-MM-DD.docx
```

### Step 5: Google Driveの保存先フォルダを確認・用意する

デフォルトの保存先はマイドライブ直下の「議事録」フォルダ。ユーザーが会話中に別のフォルダ
（プロジェクトフォルダ等）を指定した場合はそちらを優先する。

1. `search_files` で `title = '議事録' and mimeType = 'application/vnd.google-apps.folder' and parentId = 'root'` を検索
2. 見つからなければ `create_file` で作成する（`title: "議事録"`, `parentId: "root"`,
   `contentMimeType: "application/vnd.google-apps.folder"`, content系フィールドは省略）
3. 取得/作成したフォルダの `id` を控える

### Step 6: Google Docsとしてアップロードする

1. `.docx` ファイルをbase64エンコードする
   ```bash
   base64 -i /path/to/scratchpad/議事録_YYYY-MM-DD.docx | tr -d '\n'
   ```
2. `create_file` を呼ぶ：
   - `title`: `"YYYY-MM-DD_会議名_議事録"` のような分かりやすい名前
   - `parentId`: Step 5 で控えたフォルダID
   - `base64Content`: 手順1で得たbase64文字列
   - `contentMimeType`: `"application/vnd.openxmlformats-officedocument.wordprocessingml.document"`
   - `disableConversionToGoogleType` は指定しない（省略＝false のまま）。これにより
     アップロード時に自動でGoogle Docs（`application/vnd.google-apps.document`）に変換される

### Step 7: リンクを取得してユーザーに報告する

- `create_file` のレスポンスに `webViewLink`（または同等のリンクフィールド）が含まれて
  いればそれを使う
- 含まれていない、またはフィールドが分からない場合は `get_file_metadata`（返ってきた
  `fileId` を指定）で取得し直す
- ユーザーには「保存先フォルダ名」「ファイル名」「リンク」をまとめて伝える
- ローカルの一時.docxはバックアップとして残しておいてよいが、成果物として案内するのは
  Google Docsのリンクである

---

## 注意事項

- このスキルは新規のGoogle Docsを作るのみ。既存のGoogle Docsへの追記・更新はサポート
  対象外（Google Docsの本文編集APIが無いため）。追記したい場合はユーザーに新規作成で
  よいか確認する
- 表・見出し・箇条書きの体裁は python-docx → Google Docs変換に依存する。変換後に多少の
  見た目差異が出ることがある旨は把握しておく
- 文字起こしに機密情報（人事評価・契約金額等）が含まれる場合、Google Driveへの保存で
  問題ないかユーザーに確認してから進める
- `create_docx.py` は docx-creator スキルのスクリプトと同一仕様（document.json format:
  `title_page` / `heading` / `paragraph` / `bullets` / `numbered` / `table` / `image` /
  `minutes_header` / `references` など）。議事録以外の凝った構成が必要になった場合も
  同じセクションタイプがそのまま使える
