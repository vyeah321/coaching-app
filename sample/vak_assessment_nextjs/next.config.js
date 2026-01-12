/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // GitHub Pages用の静的エクスポート設定
  output: 'export',
  // 画像最適化を無効化（GitHub Pagesでは使えないため）
  images: {
    unoptimized: true,
  },
  // GitHub Pagesのベースパス設定
  // リポジトリ名: coaching-app、アプリ名: vak
  basePath: process.env.NODE_ENV === 'production' ? '/coaching-app/vak' : '',
}

module.exports = nextConfig
