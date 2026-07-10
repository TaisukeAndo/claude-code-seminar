#!/bin/bash
# ファイル書き込み後に、重要な出力ファイル（.pptx / .docx）を自動で開くフック
# Write ツール実行後に呼び出される

# 書き込まれたファイルパスを取得
FILE_PATH=$(echo "$CLAUDE_TOOL_INPUT" | jq -r '.file_path // empty' 2>/dev/null)

if [ -z "$FILE_PATH" ]; then
  exit 0
fi

EXT="${FILE_PATH##*.}"
EXT_LOWER=$(echo "$EXT" | tr '[:upper:]' '[:lower:]')

# .pptx または .docx が生成された場合のみ処理
if [ "$EXT_LOWER" = "pptx" ] || [ "$EXT_LOWER" = "docx" ]; then
  # ファイルの存在確認
  if [ -f "$FILE_PATH" ]; then
    FILE_SIZE=$(du -h "$FILE_PATH" 2>/dev/null | cut -f1)
    FILE_NAME=$(basename "$FILE_PATH")

    # macOS の場合はファイルを自動オープン
    if [ "$(uname)" = "Darwin" ]; then
      open "$FILE_PATH" 2>/dev/null &
      OPENED="（自動で開きました）"
    else
      OPENED=""
    fi

    # Claude へのフィードバック
    jq -n \
      --arg name "$FILE_NAME" \
      --arg path "$FILE_PATH" \
      --arg size "$FILE_SIZE" \
      --arg opened "$OPENED" \
    '{
      hookSpecificOutput: {
        hookEventName: "PostToolUse",
        additionalContext: ("✅ ファイルが生成されました\n・ファイル名: " + $name + "\n・保存先: " + $path + "\n・サイズ: " + $size + "\n" + $opened)
      }
    }'
  fi
fi

exit 0
