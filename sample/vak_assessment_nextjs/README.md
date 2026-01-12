# VAK コミュニケーションタイプ診断 (Next.js版)

Streamlit版のVAK診断をNext.js + TypeScript + Tailwind CSS + Plotly.jsで再実装した高速版です。

## 特徴

- ⚡ **爆速**: ページ遷移なし、即座に反応
- 📱 **モバイル最適**: レスポンシブデザイン
- 🎨 **美しいUI**: Tailwind CSSによる洗練されたデザイン
- 📊 **インタラクティブチャート**: Plotly.jsのレーダーチャート
- 📧 **メール送信**: mailto:による結果送信
- 🔒 **プライバシー**: クライアントサイドのみで完結

## セットアップ

```bash
# 依存関係インストール
npm install

# 開発サーバー起動（ポート3001）
npm run dev

# ビルド（GitHub Pages用の静的ファイルを生成）
npm run build
# → out/ フォルダに静的ファイルが生成される
```

## デプロイ

### ⭐ Vercel（推奨・最も簡単）

```bash
# Vercel CLIインストール
npm i -g vercel

# デプロイ（対話形式で2分）
vercel
```

**メリット**: 設定不要、自動デプロイ、カスタムドメイン無料

---

### 🚀 GitHub Pages（完全無料・自動デプロイ）

**1. 初回設定（GitHubリポジトリで1回だけ）**

1. GitHubリポジトリの **Settings** → **Pages** に移動
2. **Source** を `GitHub Actions` に変更
3. 完了！（`.github/workflows/deploy.yml`が自動で実行される）

**2. デプロイ方法**

```bash
# コミット＆プッシュするだけで自動デプロイ
git add .
git commit -m "Update VAK assessment"
git push
```

数分後、`https://vyeah321.github.io/coaching-app/vak/` でアクセス可能

**注意**: 
- ✅ `next.config.js`で`output: 'export'`設定済み
- ✅ `basePath: '/coaching-app/vak'`設定済み（複数アプリ対応）
- 📁 他のアプリは`/coaching-app/別名/`で追加可能

---

### 📦 Netlify

```bash
# ビルド
npm run build

# Netlify CLIで手動デプロイ
npx netlify-cli deploy --dir=out --prod
```

または、Netlifyダッシュボードから`out/`フォルダをドラッグ＆ドロップ

## 技術スタック

- **Next.js 14**: App Router
- **React 18**: フロントエンド
- **TypeScript**: 型安全
- **Tailwind CSS**: スタイリング
- **Plotly.js**: チャート描画

## ディレクトリ構造

```
sample/vak_assessment_nextjs/
├── app/
│   ├── layout.tsx      # ルートレイアウト
│   ├── page.tsx        # メインページ
│   └── globals.css     # グローバルCSS
├── components/
│   ├── QuestionView.tsx  # 質問画面
│   └── ResultView.tsx    # 結果画面
└── lib/
    └── vakData.ts      # データ・ロジック
```

## Streamlit版との違い

| 項目 | Streamlit版 | Next.js版 |
|------|-------------|-----------|
| 速度 | 🐌 各操作でサーバー通信 | ⚡ 即座に反応 |
| オフライン | ❌ 不可 | ✅ 可能（PWA化で） |
| コスト | 💸 サーバー必要 | 💰 無料ホスティング可 |
| モバイル | 😐 普通 | 📱 最適化済み |
| カスタマイズ | 🔧 限定的 | 🎨 自由自在 |

## ライセンス

MIT License - 詳細は[LICENSE](../../LICENSE)を参照
