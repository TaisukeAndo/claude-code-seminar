---
name: seminar-tech
category: seminar
purpose: 技術セミナー・ハンズオン・勉強会
tags: [seminar, tech, hands-on, dark, impactful]
---

# スタイルガイド：技術セミナー向け（Seminar Tech）

## カラーパレット

| ロール | カラーコード | 用途 |
|--------|-------------|------|
| Primary | #1A1A2E | ヘッダーバー・タイトル背景・Section背景 |
| Secondary | #16213E | Section スライド背景（Primary よりやや薄め） |
| Accent | #E94560 | アクセントマーカー・強調色・グラフメイン色 |
| Background | #FFFFFF | 通常スライド背景 |
| Text | #1A1A2E | 本文テキスト |
| Dim | #64748B | サブテキスト・注釈・補足 |
| Snow | #F8FAFC | カード・ボックス背景 |
| AltBg | #EDF2F8 | 左カラム背景 |
| WarmBg | #FFF0F3 | 右カラム背景 |
| Border | #CBD5E1 | 枠線・区切り線 |

## タイポグラフィ

| 要素 | フォント | サイズ | スタイル |
|------|---------|--------|---------|
| タイトルスライド見出し | Meiryo | 36pt | Bold |
| スライドヘッダータイトル | Meiryo | 22pt | Bold / 白 |
| セクションタイトル | Meiryo | 34〜40pt | Bold / 白 |
| 本文 Level 0 | Meiryo | 18pt | Bold / Primary色 |
| 本文 Level 1 | Meiryo | 14pt | Regular / Dim色 |
| Stat 値 | Meiryo | 52pt | Bold / Accent色 |
| Stat ラベル | Meiryo | 14pt | Regular / Dim色 |
| グラフラベル | Meiryo | 11pt | Regular |

## スライドタイプ別デザイン仕様

### `title` — タイトルスライド
- 背景: Primary (#1A1A2E) でフル塗りつぶし
- 中央白ボックス（左右余白0.6"）にタイトルとサブタイトル
- 下部: Accent色の帯（高さ 0.35"）

### `section` — セクション区切り
- 背景: Secondary (#16213E)
- 左端にAccent色の縦バー
- 下部にAccent色の横バー
- テキスト: 白、大きく中央寄せ

### `content` — 箇条書きスライド
- 背景: 白
- ヘッダーバー: Primary、その下にAccent色の細線
- Level 0: Accent色の小矩形マーカー + Primaryテキスト Bold
- Level 1: インデント + Dimテキスト

### `two_column` — 2カラム比較
- 左パネル背景: AltBg (#EDF2F8)、左ヘッダー: Primary
- 右パネル背景: WarmBg (#FFF0F3)、右ヘッダー: Accent
- 各アイテム: "▸ " プレフィックス + Textカラー

### `stat` — 数値インパクト強調
- 背景: Primary (#1A1A2E)
- タイトル: 白、上部
- 数値（value）: Accent色 (#E94560) または 白、52pt Bold
- ラベル（label）: Slate色、14pt
- 強調フラグ（highlight: true）の stat は Accent色で表示

### `chart` — グラフスライド
- 背景: 白
- ヘッダーバー: Primary
- グラフメインカラー: Accent (#E94560)
- グラフサブカラー: Primary (#1A1A2E)、Dim (#64748B)
- 軸ラベル・凡例: Dim色

### `closing` — クロージング
- title スライドと同じスタイル

## デザイン原則

1. **1スライド1メッセージ** — 伝えることを1つに絞る
2. **数値は視覚化** — Before/After 比較やパーセンテージはグラフまたはstatスライドで
3. **箇条書きは最大5項目** — 超える場合は複数スライドに分割
4. **コマンドはモノスペース風** — コマンド例はインデントして強調
5. **セクション間は必ずsectionスライド** — 話題転換を視覚的に明示

## 推奨スライド枚数の目安

| セッション時間 | 推奨枚数 |
|-------------|---------|
| 15分 | 8〜12枚 |
| 30分 | 15〜20枚 |
| 60分 | 25〜35枚 |
| 90分 | 35〜45枚 |

## このスタイルが適した用途

- 技術ハンズオン・ワークショップ
- エンジニア向け勉強会
- AI・ツール導入セミナー
- 社内技術共有会

## このスタイルが適さない用途（他のスタイルを選択）

- 対外的な営業・提案プレゼン → `business-clean` を使用
- インパクト重視の発表 → `bold-visual` を使用
- 学術・研究発表 → `academic` を使用
