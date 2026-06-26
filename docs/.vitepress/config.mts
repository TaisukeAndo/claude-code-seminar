import { defineConfig } from 'vitepress'

export default defineConfig({
  title: 'Claude Code セミナー',
  description: 'Claude Code セミナー ドキュメントサイト',
  lang: 'ja-JP',
  base: '/claude-code-seminar/',

  ignoreDeadLinks: true,

  head: [
    ['link', { rel: 'icon', href: '/claude-code-seminar/favicon.ico' }],
  ],

  themeConfig: {
    siteTitle: 'Claude Code セミナー',

    nav: [],

    sidebar: {
      '/1day-course/': [
        {
          text: '事前準備',
          collapsed: true,
          items: [
            { text: '0. セットアップの全体像', link: '/1day-course/setup/' },
            { text: '1. 動作環境の確認', link: '/1day-course/setup/01-requirements' },
            { text: '2. Node.js インストール', link: '/1day-course/setup/02-nodejs-install' },
            { text: '3. テキストエディタのインストール', link: '/1day-course/setup/03-editor' },
            { text: '4. Claude Desktop のインストール', link: '/1day-course/setup/04-claude-desktop' },
            { text: '5. Claude Code CLI インストール', link: '/1day-course/setup/05-claude-code-install' },
            { text: '6. Claude Pro でログイン', link: '/1day-course/setup/06-login' },
            { text: '7. 動作確認', link: '/1day-course/setup/07-verify' },
          ],
        },
        {
          text: 'Session 1: 概念と仕組みを理解する',
          collapsed: false,
          items: [
            { text: 'セッション概要', link: '/1day-course/session1/' },
            { text: '1. イントロ', link: '/1day-course/session1/01-intro' },
            { text: '2. プロンプトエンジニアリングとは', link: '/1day-course/session1/04-prompt-engineering' },
            { text: '3. Claudeってなんだ', link: '/1day-course/session1/05-claude' },
            { text: '4. Claude Codeってなんだ', link: '/1day-course/session1/06-claude-code' },
            { text: '5. コンテキストエンジニアリングとは', link: '/1day-course/session1/07-context-engineering' },
            { text: '6. 7つの道具', link: '/1day-course/session1/08-seven-tools' },
            { text: 'まとめ', link: '/1day-course/session1/09-summary' },
          ],
        },
        {
          text: 'Session 2: ドキュメント生成の効率化',
          collapsed: false,
          items: [
            { text: 'セッション概要', link: '/1day-course/session2/' },
            { text: '2.1.〜2.4. 導入ワーク', link: '/1day-course/session2/01-intro-workshop' },
            { text: '2.5.〜2.8. DOCX 設計', link: '/1day-course/session2/02-docx-design' },
            { text: '2.9.〜2.13. DOCX ハンズオン', link: '/1day-course/session2/03-docx-hands-on' },
            { text: '2.14.〜2.16. PPTX ワーク', link: '/1day-course/session2/04-pptx-workshop' },
            { text: '2.17.〜2.18. PPTX 設計', link: '/1day-course/session2/05-pptx-design' },
            { text: '2.19.〜2.23. PPTX ハンズオン', link: '/1day-course/session2/06-pptx-hands-on' },
            { text: '2.24.〜2.27. まとめ', link: '/1day-course/session2/07-summary' },
          ],
        },
        {
          text: 'Session 3: Excelデータ分析と会計処理',
          collapsed: false,
          items: [
            { text: 'セッション概要', link: '/1day-course/session3/' },
            { text: '3.1.〜3.4. 導入ワーク', link: '/1day-course/session3/01-intro-workshop' },
            { text: '3.5.〜3.8. xlsx-creator 設計', link: '/1day-course/session3/02-xlsx-design' },
            { text: '3.9.〜3.13. xlsx-creator ハンズオン', link: '/1day-course/session3/03-xlsx-hands-on' },
            { text: '3.14.〜3.16. 会計処理ワーク', link: '/1day-course/session3/04-invoice-workshop' },
            { text: '3.17.〜3.18. invoice-creator 設計', link: '/1day-course/session3/05-invoice-design' },
            { text: '3.19.〜3.23. invoice-creator ハンズオン', link: '/1day-course/session3/06-invoice-hands-on' },
            { text: '3.24.〜3.27. まとめ', link: '/1day-course/session3/07-summary' },
          ],
        },
        {
          text: 'Session 4: 定常業務の自動化',
          collapsed: false,
          items: [
            { text: 'セッション概要', link: '/1day-course/session4/' },
          ],
        },
        {
          text: 'Session 5: セキュリティ対応スキル作成',
          collapsed: false,
          items: [
            { text: 'セッション概要', link: '/1day-course/session5/' },
            { text: '1. Hooks（フック）', link: '/1day-course/session5/01-hooks' },
            { text: '2. permission（パーミッション）', link: '/1day-course/session5/02-permission' },
            { text: '3. .envファイル', link: '/1day-course/session5/03-env-file' },
            { text: '4. skill-creator', link: '/1day-course/session5/04-skill-creator' },
            { text: '5. まとめ', link: '/1day-course/session5/05-summary' },
          ],
        },
        {
          text: 'サポート',
          items: [
            { text: 'よくある質問', link: '/1day-course/faq' },
          ],
        },
      ],
      '/online-course/': [
        {
          text: 'Desktop版 環境構築',
          collapsed: false,
          items: [
            { text: '0. セットアップの全体像', link: '/online-course/setup/' },
            { text: '1. Claude Pro プランへの加入', link: '/online-course/setup/01-pro-subscription' },
            { text: '2. Claude Desktop のインストール', link: '/online-course/setup/02-desktop-install' },
            { text: '3. Git のインストール', link: '/online-course/setup/03-git-install' },
            { text: '4. MCP サーバーの接続設定', link: '/online-course/setup/04-mcp-setup' },
          ],
        },
      ],
    },

    socialLinks: [
      { icon: 'github', link: 'https://github.com/TaisukeAndo/claude-code-seminar' },
    ],

    footer: {
      message: 'Claude Code セミナー',
      copyright: `© ${new Date().getFullYear()} TaisukeAndo`,
    },

    lastUpdated: {
      text: '最終更新',
      formatOptions: {
        dateStyle: 'full',
      },
    },

    search: {
      provider: 'local',
    },
  },
})
