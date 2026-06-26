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
          collapsed: false,
          items: [
            { text: 'セットアップの全体像', link: '/1day-course/setup/' },
            { text: '① 動作環境の確認', link: '/1day-course/setup/01-requirements' },
            { text: '② Node.js インストール', link: '/1day-course/setup/02-nodejs-install' },
            { text: '③ Claude Code CLI インストール', link: '/1day-course/setup/03-claude-code-install' },
            { text: '④ API キーの取得・設定', link: '/1day-course/setup/04-api-key' },
            { text: '⑤ 動作確認', link: '/1day-course/setup/05-verify' },
          ],
        },
        {
          text: 'セミナー当日資料',
          collapsed: false,
          items: [
            { text: 'プログラム', link: '/1day-course/seminar/' },
            { text: 'オープニング・Claude Code とは', link: '/1day-course/seminar/01-intro' },
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
          text: 'Desktop 版 環境構築',
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
