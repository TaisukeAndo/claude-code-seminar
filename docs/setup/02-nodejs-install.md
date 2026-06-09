# 2. Node.js インストール

Claude Code CLI の実行には **Node.js v18 以上** が必要です。

## インストール済みか確認する

ターミナルで以下を実行してください:

```bash
node --version
```

`v18.x.x` 以上が表示されればインストール済みです。  
→ [3. テキストエディタのインストール](/setup/03-editor) に進んでください。

エラーが出た場合や古いバージョンの場合は以下の手順でインストールします。

---

## macOS の場合

### Homebrew を使う方法（推奨）

```bash
# Homebrew のインストール（未インストールの場合）
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Node.js のインストール
brew install node
```

### 公式インストーラーを使う方法

1. [https://nodejs.org/](https://nodejs.org/) にアクセス
2. **LTS（推奨版）** をダウンロード
3. ダウンロードした `.pkg` ファイルを実行してインストール

---

## Windows の場合

1. [https://nodejs.org/](https://nodejs.org/) にアクセス
2. **LTS（推奨版）** をダウンロード（`.msi` ファイル）
3. インストーラーを実行し、すべてデフォルト設定で進める

インストール後、PowerShell を**再起動**してから確認コマンドを実行してください。

---

## インストール確認

```bash
node --version   # v20.x.x などが表示されれば OK
npm --version    # 10.x.x などが表示されれば OK
```

## 次のステップ

Node.js のインストールが完了したら [3. テキストエディタのインストール](/setup/03-editor) に進んでください。
