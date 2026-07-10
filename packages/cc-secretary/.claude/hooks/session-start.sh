#!/bin/bash
# セッション開始時に現在の環境状態を Claude に伝えるフック

PPTX_REFS=$(ls "${CLAUDE_PROJECT_DIR}/.claude/skills/pptx-creator/references/" 2>/dev/null | grep -v '^\.' | wc -l | tr -d ' ')
PPTX_ASSETS=$(ls "${CLAUDE_PROJECT_DIR}/.claude/skills/pptx-creator/assets/" 2>/dev/null | grep -v '^\.' | wc -l | tr -d ' ')
DOCX_REFS=$(ls "${CLAUDE_PROJECT_DIR}/.claude/skills/docx-creator/references/" 2>/dev/null | grep -v '^\.' | wc -l | tr -d ' ')
DOCX_ASSETS=$(ls "${CLAUDE_PROJECT_DIR}/.claude/skills/docx-creator/assets/" 2>/dev/null | grep -v '^\.' | wc -l | tr -d ' ')
XLSX_REFS=$(ls "${CLAUDE_PROJECT_DIR}/.claude/skills/xlsx-creator/references/" 2>/dev/null | grep -v '^\.' | grep -v '\.md$' | wc -l | tr -d ' ')
XLSX_ASSETS=$(ls "${CLAUDE_PROJECT_DIR}/.claude/skills/xlsx-creator/assets/" 2>/dev/null | grep -v '^\.' | wc -l | tr -d ' ')

PPTX_REF_LIST=$(ls "${CLAUDE_PROJECT_DIR}/.claude/skills/pptx-creator/references/" 2>/dev/null | grep -v '^\.' | head -5 | tr '\n' ', ' | sed 's/,$//')
PPTX_ASSET_LIST=$(ls "${CLAUDE_PROJECT_DIR}/.claude/skills/pptx-creator/assets/" 2>/dev/null | grep -v '^\.' | head -5 | tr '\n' ', ' | sed 's/,$//')
DOCX_REF_LIST=$(ls "${CLAUDE_PROJECT_DIR}/.claude/skills/docx-creator/references/" 2>/dev/null | grep -v '^\.' | head -5 | tr '\n' ', ' | sed 's/,$//')
DOCX_ASSET_LIST=$(ls "${CLAUDE_PROJECT_DIR}/.claude/skills/docx-creator/assets/" 2>/dev/null | grep -v '^\.' | head -5 | tr '\n' ', ' | sed 's/,$//')
XLSX_REF_LIST=$(ls "${CLAUDE_PROJECT_DIR}/.claude/skills/xlsx-creator/references/" 2>/dev/null | grep -v '^\.' | grep -v '\.md$' | head -5 | tr '\n' ', ' | sed 's/,$//')
XLSX_ASSET_LIST=$(ls "${CLAUDE_PROJECT_DIR}/.claude/skills/xlsx-creator/assets/" 2>/dev/null | grep -v '^\.' | head -5 | tr '\n' ', ' | sed 's/,$//')

TODAY=$(date '+%Y年%m月%d日')

CONTEXT="=== Claude Code セミナー環境 — セッション開始 (${TODAY}) ===

【利用可能なスキル】
• pptx-creator: スライド作成（「プレゼン資料を作って」でトリガー）
• docx-creator: Word文書作成（「報告書を作って」「議事録にして」でトリガー）
• xlsx-creator: Excel作成（「Excelを作って」「タスク管理表」「KPIシート」「見積書」でトリガー）
• web-researcher: 情報収集（他スキルから自動呼び出し）
• excel-structure-researcher: Excel構成リサーチ（xlsx-creatorから自動呼び出し）

【pptx-creator の参照ファイル状況】
• references/: ${PPTX_REFS}件${PPTX_REF_LIST:+ (${PPTX_REF_LIST})}
• assets/: ${PPTX_ASSETS}件${PPTX_ASSET_LIST:+ (${PPTX_ASSET_LIST})}

【docx-creator の参照ファイル状況】
• references/: ${DOCX_REFS}件${DOCX_REF_LIST:+ (${DOCX_REF_LIST})}
• assets/: ${DOCX_ASSETS}件${DOCX_ASSET_LIST:+ (${DOCX_ASSET_LIST})}

【xlsx-creator の参照ファイル状況】
• references/: ${XLSX_REFS}件${XLSX_REF_LIST:+ (${XLSX_REF_LIST})}
• assets/: ${XLSX_ASSETS}件${XLSX_ASSET_LIST:+ (${XLSX_ASSET_LIST})}

参考ファイルがない場合はオリジナルデザインで生成します。"

jq -n --arg ctx "$CONTEXT" '{
  hookSpecificOutput: {
    hookEventName: "SessionStart",
    additionalContext: $ctx
  }
}'
