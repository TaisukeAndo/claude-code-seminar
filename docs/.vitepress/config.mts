import { defineConfig } from 'vitepress'

export default defineConfig({
  title: 'Claude Code ワンデイセミナー',
  description: 'セミナー前の事前セットアップガイド',
  lang: 'ja-JP',
  base: '/claude-code-seminar/',

  head: [
    ['link', { rel: 'icon', href: '/claude-code-seminar/favicon.ico' }],
  ],

  themeConfig: {
    siteTitle: 'Claude Code セミナー',

    nav: [
      { text: 'ホーム', link: '/' },
      { text: 'セットアップ', link: '/setup/' },
      { text: 'よくある質問', link: '/faq' },
    ],

    sidebar: [
      {
        text: '事前準備',
        collapsed: false,
        items: [
          { text: 'セットアップの全体像', link: '/setup/' },
          { text: '① 動作環境の確認', link: '/setup/01-requirements' },
          { text: '② Node.js インストール', link: '/setup/02-nodejs-install' },
          { text: '③ Claude Code CLI インストール', link: '/setup/03-claude-code-install' },
          { text: '④ API キーの取得・設定', link: '/setup/04-api-key' },
          { text: '⑤ 動作確認', link: '/setup/05-verify' },
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
      message: 'Claude Code ワンデイセミナー',
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
