# Coaching App

コーチング関連のプロトタイプアプリケーション集

## 🌐 デプロイ済みアプリ

### [VAK コミュニケーションタイプ診断](https://vyeah321.github.io/coaching-app/vak/)
**URL**: https://vyeah321.github.io/coaching-app/vak/  
ワイン会向けのVAKコミュニケーションタイプ診断アプリ（Next.js版）

**コード**: [sample/vak_assessment_nextjs/](./sample/vak_assessment_nextjs/)

---

## 📁 プロジェクト一覧

### [session_organizer](./session_organizer/)
コーチがセッション後に行う「整理・振り返り・次回準備」を短時間で完了できるアプリ

**機能:**
- セッションメモからレポート自動生成
- クライアント向けレポート
- コーチ向けメモ
- Google Drive 連携

**技術:** Streamlit, Python, Google Drive API

### [sample/vak_assessment](./sample/vak_assessment/)
VAK診断アプリ（Streamlit版・ローカル開発用）

### [sample/vak_assessment_nextjs](./sample/vak_assessment_nextjs/)
VAK診断アプリ（Next.js版・本番デプロイ済み）

**URL**: https://vyeah321.github.io/coaching-app/vak/

---

## 🚀 複数アプリのデプロイ構成

このリポジトリは1つのGitHub Pagesで複数のアプリをホストできます：

- `/vak/` - VAK診断アプリ
- `/personality/` - 性格診断アプリ（今後追加予定）
- `/motivation/` - モチベーション診断アプリ（今後追加予定）

各アプリは`basePath`を設定することで、サブパスでアクセス可能になります。

---

## セットアップ

各プロジェクトのフォルダに移動して、それぞれの README を参照してください。

```bash
# Streamlitアプリ
cd session_organizer
# README.md を確認

# Next.jsアプリ
cd sample/vak_assessment_nextjs
npm install
npm run dev
```

## ライセンス

MIT License - 詳細は[LICENSE](./LICENSE)を参照
