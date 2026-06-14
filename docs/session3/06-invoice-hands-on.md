# invoice-creator ハンズオン

**所要時間: 約 20 分（手を動かす作業）**

このページはすべて実際に操作する作業です。  
1 ステップずつ確認しながら進めてください。

---

## 3.19. invoice-creator スキルをダウンロードする

**① プロジェクトフォルダに移動する**

```bash
cd ~/Desktop/claude-code-seminar
```

**② invoice-creator スキルをダウンロードする**

```bash
npx degit TaisukeAndo/claude-code-seminar/packages/skills/invoice-creator .claude/skills/invoice-creator
```

**③ ダウンロードされたファイルを確認する**

```bash
ls .claude/skills/invoice-creator/
```

以下のファイルとフォルダが表示されれば成功です。

```
SKILL.md    .env.example    clients/    scripts/
```

| ファイル・フォルダ | 役割 |
|---|---|
| `SKILL.md` | スキルの設定ファイル |
| `.env.example` | 自社情報の設定テンプレート |
| `clients/` | 取引先情報を保存するフォルダ |
| `scripts/` | 各形式のファイルを生成する Python スクリプト |

---

## 3.20. 自社情報を設定する（.env ファイルの作成）

**.env ファイルとは何か**

`.env` ファイルは、プログラムが実行時に読み込む設定ファイルです。  
自社の住所・口座番号などの個人情報をここに書いておくことで、  
**Claude（AI）にこれらの情報を渡さず**に帳票を生成できます。

**① テンプレートをコピーして .env ファイルを作成する**

```bash
cp .claude/skills/invoice-creator/.env.example .claude/skills/invoice-creator/.env
```

**② Cursor で .env ファイルを開いて編集する**

1. Cursor でプロジェクトフォルダを開く
2. 左側のファイルツリーで `.claude` → `skills` → `invoice-creator` → `.env` をクリック
3. 各項目を自分の情報に書き換える

```bash
# .env の主な設定項目（例）
MY_COMPANY_NAME=株式会社〇〇
MY_COMPANY_ADDRESS=東京都〇〇区〇〇1-2-3
MY_COMPANY_PHONE=03-XXXX-XXXX
MY_COMPANY_EMAIL=info@example.com
MY_BANK_NAME=〇〇銀行
MY_BANK_BRANCH=〇〇支店
MY_BANK_ACCOUNT_TYPE=普通
MY_BANK_ACCOUNT_NUMBER=1234567
MY_BANK_ACCOUNT_HOLDER=カブシキガイシャ〇〇
MY_REGISTRATION_NUMBER=T0000000000000  # インボイス登録番号（任意）
```

::: tip .env ファイルは Git に含まれません
`.env` ファイルは自動的に Git の管理対象から除外されています（`.gitignore` に記載済み）。  
誤って GitHub に公開される心配はありません。
:::

**③ 取引先情報ファイルを作成する**

取引先ごとに JSON ファイルを作成します。  
スキルフォルダ内の `clients/example_client.json` を参考に作成してください。

```bash
# 例: 田中商事 というクライアントのファイルを作る場合
cp .claude/skills/invoice-creator/clients/example_client.json .claude/skills/invoice-creator/clients/tanaka_shoji.json
```

ファイルを開いて取引先情報を記入してください。

---

## 3.21. Excel で見積書を生成する

**① プロジェクトのルートフォルダに戻る**

```bash
cd ~/Desktop/claude-code-seminar
```

**② Claude Code を起動する**

```bash
claude
```

**③ 見積書の生成を指示する**

```
見積書を作成してください。
取引先: tanaka_shoji
件名: Webサイト制作費用
品目1: システム設計・開発、1式、500,000円（税10%）
品目2: デザイン制作、1式、150,000円（税10%）
出力形式: Excel
```

::: tip 自分の取引で試してみる
実際の取引内容を使って試すと、出力の確認がしやすくなります。  
金額が大きく異なる場合でも、仮の数値に置き換えて試してください。
:::

**④ 生成されたファイルを確認する**

処理が完了すると `.xlsx` ファイルが生成されます。  
Excel または Numbers で開いて内容を確認してください。

::: info Excel で会計処理をしている方はここで完了です
このスキルで生成した Excel の見積書・請求書をそのまま使えます。  
3.22. 以降は会計ソフトとの API 連携が必要な方向けの内容です。
:::

---

## 3.22. 会計ソフトとの API 連携を設定する

使っている会計ソフトに応じて、以下のいずれかの手順を実施してください。

---

### マネーフォワード クラウドを使っている場合

**① API キーを発行する**

1. マネーフォワード クラウド会計・請求書にログインする
2. 画面右上のアカウント名をクリック →「API 連携」を選択する
3. 「新しいトークンを発行する」をクリックする
4. アクセストークンが発行されたらコピーしておく

::: info API の利用にはプランの確認が必要です
マネーフォワード クラウド請求書の API は、スモールビジネスプラン以上で利用できます。  
ご利用のプランをご確認ください。
:::

**② .env ファイルに API キーを追加する**

Cursor で `.env` ファイルを開いて以下を追記してください。

```bash
MONEYFORWARD_API_TOKEN=ここにアクセストークンを貼り付ける
```

**③ 動作確認：マネーフォワード形式で見積書を出力する**

Claude Code で以下を入力してください。

```
先ほどの見積書をマネーフォワード形式でも出力してください。
```

---

### freee（フリー）を使っている場合

**① freee の API アプリを作成する**

1. freee デベロッパー（`dev.freee.co.jp`）にアクセスする
2. freee アカウントでログインする
3. 「アプリを作成する」をクリックして新しいアプリを登録する
4. 「クライアントID」と「クライアントシークレット」をコピーしておく

**② .env ファイルに API キーを追加する**

```bash
FREEE_CLIENT_ID=ここにクライアントIDを貼り付ける
FREEE_CLIENT_SECRET=ここにクライアントシークレットを貼り付ける
```

**③ 動作確認：freee CSV を出力する**

```
先ほどの見積書を freee 形式でも出力してください。
```

---

### 弥生会計 / やよいの青色申告を使っている場合

弥生会計は CSV の取り込みで連携します。API キーの発行は不要です。

**① 動作確認：弥生会計 CSV を出力する**

```
先ほどの見積書を弥生会計の仕訳形式 CSV で出力してください。
```

**② 弥生会計に取り込む**

1. 弥生会計（またはやよいの青色申告）を起動する
2. 「ファイル」メニュー →「インポート」を選択する
3. 生成された CSV ファイルを選択して取り込む

::: tip 弥生会計のバージョンについて
弥生会計のデスクトップ版とクラウド版では、CSV の形式が異なる場合があります。  
うまく取り込めない場合は講師に声をかけてください。
:::

---

## 3.23. SKILL.md を確認してカスタマイズする

使いながら「毎回同じことを指示している」と感じたら、`SKILL.md` を編集して自動化できます。

**確認のポイント**

Cursor で `.claude/skills/invoice-creator/SKILL.md` を開き、  
`description` の部分に自分がよく使う言葉を追加してみましょう。

```yaml
# 変更前
description: >
  見積書・請求書を作成する。

# 変更後の例（よく使う言葉を追加）
description: >
  見積書・請求書・領収書を作成する。
  「お見積りを作って」「請求書を田中商事宛に発行して」「マネーフォワード用に請求書を」
  などのリクエストに使う。
```

---

[次へ：3.24.〜3.27. まとめ](/session3/07-summary)
