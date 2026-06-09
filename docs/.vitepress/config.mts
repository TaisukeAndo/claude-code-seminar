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
      { text: 'セミナー資料', link: '/seminar/' },
      { text: 'よくある質問', link: '/faq' },
    ],

    sidebar: [
      {
        text: '事前準備',
        collapsed: false,
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
        text: 'セミナー当日資料',
        collapsed: false,
        items: [
          { text: 'プログラム', link: '/seminar/' },
          { text: 'オープニング・Claude Code とは', link: '/seminar/01-intro' },
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
