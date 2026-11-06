# 定期実行の設定

新しい版の確認を、決まった曜日・時刻に自動で行うための設定。方法は2つあり、**どちらか1つを選ぶ**（両方を有効にすると、同じ更新のPRが2本できることがある）。

| 方法 | 内容 | 向いている場合 |
|---|---|---|
| A. Claude Code の定期実行（scheduled tasks。以前の名前はルーチン）（このSkillを使う） | Claude Code がクラウド上で、決まった時刻にこのSkillを実行し、条件を満たした更新だけをPRにする | 安定性・脆弱性・テストの確認をまとめて任せたい |
| B. GitHub の Dependabot | GitHub が新しい版を見つけてPRを作る。AIは使わない | Claudeの使用量を使いたくない。設定ファイル1つで済ませたい |

## A. Claude Code の定期実行（scheduled tasks）で実行する

### 前提

- Claude の Pro・Max・Ultra・Team・Enterprise のいずれかのプランで、Claude Code on the web が使えること
- アプリのリポジトリが GitHub にあり、Claude Code on the web から接続できること
- **このSkill（と、使う場合は `app-security-check`、`.claude/rules/expression-rules.md`）が、アプリのリポジトリにコミットされ、main に入っていること。**
  定期実行は、実行のたびに GitHub からリポジトリを取り出して動くため、自分のパソコンにだけあるSkillは使えない

知っておくこと（2026年11月時点の公式ドキュメント「Automate work with scheduled tasks」より）:

- 研究段階の機能（research preview）で、動きや上限は変わることがある
- 実行するたびに、ふだんの会話と同じく、プランの使用量を使う。回数の上限は1時間あたりで決まっている
- コミットやPRは、自分のGitHubアカウントの名前で作られる。ブランチ名は `claude/` で始まる
- クラウドでは `gh pr` などGraphQLを使うコマンドが使えないため、このSkillはPRを REST API（`gh api`）で作る
- 脆弱性の情報源の OSV（api.osv.dev）は、初期設定の通信許可に入っていない。使いたい場合は、環境のネットワーク設定を Custom にして許可を足す（足さなくても、npm audit で確かめられる）

### 設定のしかた

Claude Code で `/schedule` と入力し、次の内容で作る（claude.ai/code/routines の画面からも作れる）。
作ったら、一覧の **Run now** で一度だけ実行し、最後まで動くかを確かめる。

- 対象のリポジトリ: 自分のアプリのリポジトリ
- 実行のタイミング: 週に1回（例: 毎週月曜の朝7時）。毎日にすると、使用量を多く使う
- 実行する内容（プロンプト）:

```text
これは定期実行です。私はその場にいないので、質問せずに最後まで進めてください。
app-dependency-update スキルを使って、依存パッケージの更新を確認してください。
条件を満たした更新だけをコミットし、PRを作ってください。マージはしないでください。
更新するものがなければ、PRは作らずに「更新なし」と報告してください。
判断に迷うものは見送り、理由を報告に書いてください。
```

### 動いたかの確かめ方

- 実行の記録は、claude.ai/code の画面で見られる
- PRが作られたら、GitHub から通知が届く。PRの説明にある「見送ったもの」も読む

## B. GitHub の Dependabot を使う

リポジトリに `.github/dependabot.yml` を置く。ひな形は [../assets/dependabot.yml](../assets/dependabot.yml)。

- `cooldown` の `default-days: 7` で、公開から7日たった版だけをPRにする（このSkillの S3 と同じ考え方）
- メジャーバージョンは `ignore` で除いている
- 脆弱性の修正のためのPR（security updates）は、`cooldown` の対象外で、すぐに作られる
- 設定しなくても、Dependabot には既定で短い待ち期間がある。7日にそろえるため、明示して書いている
- Dependabot は、テスト・脆弱性の確認・リリースノートの確認を、このSkillほど細かくは行わない。
  PRが届いたら、プレビュー環境で動きを確かめてからマージする

設定値の細部は変わることがあるため、GitHub 公式の「Dependabot options reference」で確かめる。
