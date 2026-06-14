import { defineConfig } from 'vitepress'

export default defineConfig({
  title: 'ClaudeCode 1Day Seminar',
  description: 'ClaudeCode 1Day Seminar 事前セットアップガイド',
  lang: 'ja-JP',
  base: '/claude-code-seminar/',

  head: [
    ['link', { rel: 'icon', href: '/claude-code-seminar/favicon.ico' }],
  ],

  themeConfig: {
    siteTitle: 'ClaudeCode 1Day Seminar',

    nav: [
      { text: 'ホーム', link: '/' },
      { text: 'セットアップ', link: '/setup/' },
      {
        text: 'セッション',
        items: [
          { text: 'Session 1: 概念と仕組み', link: '/session1/' },
          { text: 'Session 2: スキルのカスタマイズ', link: '/session2/' },
          { text: 'Session 3: 会計処理の自動化', link: '/session3/' },
          { text: 'Session 4: 定常業務の自動化', link: '/session4/' },
          { text: 'Session 5: オリジナルスキル作成', link: '/session5/' },
        ],
      },
      { text: 'よくある質問', link: '/faq' },
    ],

    sidebar: [
      {
        text: '事前準備',
        collapsed: true,
        items: [
          { text: '0. セットアップの全体像', link: '/setup/' },
          { text: '1. 動作環境の確認', link: '/setup/01-requirements' },
          { text: '2. Node.js インストール', link: '/setup/02-nodejs-install' },
          { text: '3. テキストエディタのインストール', link: '/setup/03-editor' },
          { text: '4. Claude Desktop のインストール', link: '/setup/04-claude-desktop' },
          { text: '5. Claude Code CLI インストール', link: '/setup/05-claude-code-install' },
          { text: '6. Claude Pro でログイン', link: '/setup/06-login' },
          { text: '7. 動作確認', link: '/setup/07-verify' },
        ],
      },
      {
        text: 'Session 1: 概念と仕組みを理解する',
        collapsed: false,
        items: [
          { text: 'セッション概要', link: '/session1/' },
          { text: '1. イントロ', link: '/session1/01-intro' },
          { text: '2. プロンプトエンジニアリングとは', link: '/session1/04-prompt-engineering' },
          { text: '3. Claudeってなんだ', link: '/session1/05-claude' },
          { text: '4. Claude Codeってなんだ', link: '/session1/06-claude-code' },
          { text: '5. コンテキストエンジニアリングとは', link: '/session1/07-context-engineering' },
          { text: '6. 7つの道具', link: '/session1/08-seven-tools' },
          { text: 'まとめ', link: '/session1/09-summary' },
        ],
      },
      {
        text: 'Session 2: ドキュメント生成の効率化',
        collapsed: false,
        items: [
          { text: 'セッション概要', link: '/session2/' },
          { text: '2.1.〜2.4. 導入ワーク', link: '/session2/01-intro-workshop' },
          { text: '2.5.〜2.8. DOCX 設計', link: '/session2/02-docx-design' },
          { text: '2.9.〜2.13. DOCX ハンズオン', link: '/session2/03-docx-hands-on' },
          { text: '2.14.〜2.16. PPTX ワーク', link: '/session2/04-pptx-workshop' },
          { text: '2.17.〜2.18. PPTX 設計', link: '/session2/05-pptx-design' },
          { text: '2.19.〜2.23. PPTX ハンズオン', link: '/session2/06-pptx-hands-on' },
          { text: '2.24.〜2.27. まとめ', link: '/session2/07-summary' },
        ],
      },
      {
        text: 'Session 3: 会計処理の自動化',
        collapsed: false,
        items: [
          { text: 'セッション概要', link: '/session3/' },
        ],
      },
      {
        text: 'Session 4: 定常業務の自動化',
        collapsed: false,
        items: [
          { text: 'セッション概要', link: '/session4/' },
        ],
      },
      {
        text: 'Session 5: セキュリティ対応スキル作成',
        collapsed: false,
        items: [
          { text: 'セッション概要', link: '/session5/' },
          { text: '1. Hooks（フック）', link: '/session5/01-hooks' },
          { text: '2. permission（パーミッション）', link: '/session5/02-permission' },
          { text: '3. .envファイル', link: '/session5/03-env-file' },
          { text: '4. skill-creator', link: '/session5/04-skill-creator' },
          { text: '5. まとめ', link: '/session5/05-summary' },
        ],
      },
      {
        text: 'サポート',
        items: [
          { text: 'よくある質問', link: '/faq' },
        ],
      },
    ],

    socialLinks: [
      { icon: 'github', link: 'https://github.com/TaisukeAndo/claude-code-seminar' },
    ],

    footer: {
      message: 'ClaudeCode 1Day Seminar',
      copyright: '© 2026 bitcraft',
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
