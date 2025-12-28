# Coaching App Prototype

コーチがセッション後に行う「整理・振り返り・次回準備」を短時間で完了できるプロトタイプアプリ

## 概要

セッションメモを入力すると、以下の2つのレポートを自動生成し、Google Drive に保存します：

- **クライアント向けレポート**: セッションの気づき、行動、問いをまとめたもの
- **コーチ向けメモ**: 観察、介入ポイント、次回仮説をまとめたもの

## セットアップ

### 1. 依存関係のインストール

```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

### 2. Google Drive API 設定

1. [Google Cloud Console](https://console.cloud.google.com/) でプロジェクト作成
2. Google Drive API を有効化
3. OAuth クライアント ID を作成（**デスクトップアプリ**）
4. JSON をダウンロードして `credentials/client_secrets.json` に配置

初回実行時にブラウザで Google ログインが求められます。

詳細は [IMPLEMENTATION.md](IMPLEMENTATION.md) を参照

### 3. 環境変数の設定

```bash
cp .env.example .env
# .env を編集して実際の値を設定
```

## 実行

```bash
streamlit run app.py
```

ブラウザで http://localhost:8501 が開きます

## ドキュメント

- [DESIGN.md](DESIGN.md) - 設計思想とスコープ
- [IMPLEMENTATION.md](IMPLEMENTATION.md) - 実装詳細と技術仕様

## ライセンス

Prototype / Private Use
