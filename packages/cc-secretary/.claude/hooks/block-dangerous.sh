#!/bin/bash
# 危険なコマンドの実行を事前にブロックするフック
# PreToolUse (Bash) で呼び出される

COMMAND=$(echo "$CLAUDE_TOOL_INPUT" | jq -r '.command // empty' 2>/dev/null)

if [ -z "$COMMAND" ]; then
  exit 0
fi

# ── PII ファイルへの Bash アクセスをブロック ──────────────────────────────
# invoice-creator の clients/ フォルダ・.env ファイルは Python スクリプト経由
# でのみ読み込む設計。LLM が直接参照しないよう Bash アクセスをブロックする。
PII_PATTERNS=(
  "invoice-creator/clients/"
  "invoice-creator/.env"
)

for PAT in "${PII_PATTERNS[@]}"; do
  if echo "$COMMAND" | grep -q "$PAT"; then
    jq -n --arg cmd "$COMMAND" --arg pat "$PAT" '{
      hookSpecificOutput: {
        hookEventName: "PreToolUse",
        permissionDecision: "deny",
        permissionDecisionReason: ("【PII保護】このファイルへの直接アクセスはブロックされています。\n対象パス: " + $pat + "\n理由: 取引先情報・自社情報はPythonスクリプトが実行時に読み込むため、LLMが直接参照する必要はありません。\nコマンド: " + $cmd)
      }
    }'
    exit 2
  fi
done

# ── 危険なコマンドのブロック ───────────────────────────────────────────────
BLOCKED_PATTERNS=(
  "rm -rf"
  "rm -r /"
  "sudo rm"
  "git push --force"
  "git push -f"
  "git reset --hard HEAD~"
  "DROP TABLE"
  "truncate"
  "> /dev/sda"
  "mkfs"
)

for PATTERN in "${BLOCKED_PATTERNS[@]}"; do
  if echo "$COMMAND" | grep -qi "$PATTERN"; then
    jq -n --arg cmd "$COMMAND" --arg pat "$PATTERN" '{
      hookSpecificOutput: {
        hookEventName: "PreToolUse",
        permissionDecision: "deny",
        permissionDecisionReason: ("安全のためブロックしました。パターン: " + $pat + "\nコマンド: " + $cmd + "\n実行したい場合はユーザーが直接実行してください。")
      }
    }'
    exit 2
  fi
done

exit 0
