# 5. Claude Code CLI インストール

Node.js のインストールが完了したら、**Claude Code CLI** をインストールします。

## CLI とは？

**CLI**（Command Line Interface）とは、**ターミナル（コマンド入力画面）から操作するタイプのアプリ**のことです。

画面をクリックして使う通常のアプリ（GUI）とは異なり、CLI はキーボードでコマンドを入力して操作します。エンジニアがよく使う形式で、自動化や細かい操作が得意です。

---

## インストールコマンドの意味

以下のコマンドで Claude Code をインストールします。**まず意味を理解してから実行しましょう:**

```bash
npm install -g @anthropic-ai/claude-code
```

このコマンドを分解すると:

| 部分 | 意味 |
|---|---|
| `npm` | Node.js に付属するソフト管理ツール（App Store のようなもの） |
| `install` | 「インストールして」という命令 |
| `-g` | 「このパソコン全体で使えるように（グローバルに）」という指定 |
| `@anthropic-ai/claude-code` | インストールするソフトの名前（Claude Code） |

---

## インストール手順

### ① ターミナル（PowerShell）を開く

**ターミナルの開き方がわからない場合は [1. 動作環境の確認](/1day-course/setup/01-requirements#ターミナル-コマンド入力画面-とは) を参照してください。**

### ② コマンドを入力して実行する

ターミナルに以下をコピー＆ペーストして `Enter` を押してください:

```bash
npm install -g @anthropic-ai/claude-code
```

::: tip コピーの方法
上のコードブロック右上にある📋アイコンをクリックするとコマンドをコピーできます。  
ターミナルに貼り付けるには **macOS: `⌘ Command + V`** / **Windows: `Ctrl + V`** を使ってください。
:::

### ③ インストールの完了を待つ

ネットワーク環境によって **1〜3 分程度かかります**。  
画面に文字が流れている間は待ってください。以下のような表示が出れば完了です:

```
added 123 packages in 45s
```

---

## Windows の場合の注意点

PowerShell でインストール後、以下のようなエラーが出ることがあります:

```
claude : このシステムではスクリプトの実行が無効になっているため、
ファイル C:\...\claude.ps1 を読み込むことができません。
```

**解決方法:**

1. PowerShell を **管理者として実行** する  
   （スタートメニューで「PowerShell」を右クリック → 「**管理者として実行**」）
2. 以下のコマンドを入力して `Enter` を押す:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

「実行ポリシーの変更」と聞かれたら **`Y`** を入力して `Enter` を押してください。

::: info このコマンドの意味
`Set-ExecutionPolicy` = 「スクリプトの実行ルールを設定して」  
`RemoteSigned` = 「ダウンロードしたスクリプトは署名が必要、自分で作ったものは実行OK」  
`-Scope CurrentUser` = 「このユーザーだけに適用」  

Windows はデフォルトで外部スクリプトの実行を制限しているため、この設定変更が必要です。
:::

---

## インストールの確認

以下のコマンドでバージョン番号が表示されれば成功です:

```bash
claude --version
```

**表示例:**
```
1.x.x (claude-code)
```

## 次のステップ

Claude Code CLI のインストールが完了したら [6. Claude Pro でログイン](/1day-course/setup/06-login) に進んでください。
