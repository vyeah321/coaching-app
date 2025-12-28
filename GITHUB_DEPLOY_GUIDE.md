# GitHub & Streamlit Cloud デプロイ手順

## ステップ 1: GitHub リポジトリ作成

### 1.1 GitHub でリポジトリ作成

1. [GitHub](https://github.com) にアクセスしてログイン
2. 右上の「+」→「New repository」をクリック
3. リポジトリ設定：
   - **Repository name**: `coaching-app` （または好きな名前）
   - **Visibility**: `Private` （推奨）または `Public`
   - **Initialize this repository**: チェックを入れない（既存コードをプッシュするため）
4. 「Create repository」をクリック

### 1.2 ローカルリポジトリと連携

GitHub のリポジトリ作成後、表示される URL をコピー（例：`https://github.com/username/coaching-app.git`）

ターミナルで以下を実行：

```bash
cd /Users/atsuvu/Sandbox/coaching_app

# リモートリポジトリを追加
git remote add origin https://github.com/あなたのユーザー名/coaching-app.git

# ブランチ名を main に変更（GitHub の標準）
git branch -M main

# プッシュ
git push -u origin main
```

---

## ステップ 2: Google Cloud Console 設定

### 2.1 プロジェクトと API の設定

1. [Google Cloud Console](https://console.cloud.google.com/) にアクセス
2. 新規プロジェクト作成：
   - プロジェクト名：`coaching-app-cloud`
3. **Google Drive API を有効化**：
   - 「APIとサービス」→「ライブラリ」
   - 「Google Drive API」を検索して「有効にする」

### 2.2 OAuth 同意画面の設定

1. 「APIとサービス」→「OAuth 同意画面」
2. ユーザータイプ：**「外部」** を選択
3. アプリ情報を入力：
   - アプリ名：`Coaching Session Organizer`
   - ユーザーサポートメール：あなたのメールアドレス
   - デベロッパーの連絡先情報：あなたのメールアドレス
4. 「スコープ」設定：
   - 「スコープを追加または削除」をクリック
   - `https://www.googleapis.com/auth/drive.file` を追加
5. 「保存して次へ」
6. **テストユーザー**を追加：
   - あなた自身と、使用する予定のコーチのメールアドレスを追加
   - （公開前はテストユーザーのみアクセス可能）
7. 「保存して次へ」→ 完了

### 2.3 OAuth クライアント ID 作成

1. 「APIとサービス」→「認証情報」
2. 「認証情報を作成」→「OAuth クライアント ID」
3. アプリケーションの種類：**「ウェブアプリケーション」** ⚠️
4. 名前：`streamlit-cloud-oauth`
5. **承認済みのリダイレクト URI**（重要）：
   ```
   https://あなたのアプリ名.streamlit.app/_stcore/oauth
   ```
   ⚠️ 注意：アプリ名は後で確定するので、とりあえず以下を追加：
   ```
   http://localhost:8501/_stcore/oauth
   ```
   （デプロイ後に実際の URL を追加します）
6. 「作成」をクリック
7. **クライアント ID** と **クライアントシークレット** をコピーして保存

---

## ステップ 3: Streamlit Cloud デプロイ

### 3.1 アカウント作成とアプリデプロイ

1. [Streamlit Cloud](https://streamlit.io/cloud) にアクセス
2. 「Sign up」→ **GitHub アカウント**でサインイン
3. GitHub との連携を承認
4. **「New app」** をクリック
5. デプロイ設定：
   - **Repository**: `coaching-app` を選択
   - **Branch**: `main`
   - **Main file path**: `session_organizer/app.py`
6. 「Deploy!」をクリック

### 3.2 アプリ URL の確認とリダイレクト URI 更新

デプロイが完了すると、アプリの URL が表示されます（例：`https://coaching-app-xxx.streamlit.app`）

この URL をコピーして、Google Cloud Console に戻ります：

1. 「認証情報」→ 作成した OAuth クライアント ID を編集
2. **承認済みのリダイレクト URI** に追加：
   ```
   https://coaching-app-xxx.streamlit.app/_stcore/oauth
   ```
   ⚠️ 必ず `/_stcore/oauth` をつける
3. 「保存」

### 3.3 Streamlit Secrets の設定

Streamlit Cloud のアプリ管理画面で：

1. アプリ右側の「⋮」メニュー →「Settings」
2. 左メニューから「Secrets」を選択
3. 以下をコピー＆ペーストして編集：

```toml
GOOGLE_CLIENT_ID = "your-client-id.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "your-client-secret"

# 任意: 特定のフォルダに保存する場合
GOOGLE_DRIVE_FOLDER_ID = ""

# アプリ設定
COACH_NAME = "デフォルトコーチ名"
DEFAULT_CLIENT_NAME = ""
```

4. **「Save」** をクリック
5. アプリが自動的に再起動します

---

## ステップ 4: テスト

### 4.1 動作確認

1. Streamlit Cloud のアプリ URL にアクセス
2. セッション情報とメモを入力
3. 「レポートを生成」をクリック
4. 「Google Drive に保存」をクリック
5. 初回のみ Google ログイン画面が表示される
6. アクセスを許可
7. 自分の Google Drive に保存されることを確認

### 4.2 テストユーザーの追加

他のコーチに使ってもらう場合：

1. Google Cloud Console →「OAuth 同意画面」→「テストユーザー」
2. コーチのメールアドレスを追加
3. コーチに Streamlit Cloud の URL を共有

---

## ステップ 5: 本番公開（任意）

テストが完了したら、Google の OAuth アプリを本番環境に公開：

1. Google Cloud Console →「OAuth 同意画面」
2. 「アプリを公開」をクリック
3. 審査プロセス（数日〜数週間かかる場合あり）

⚠️ テストユーザーのみで運用する場合は公開不要

---

## 完了 🎉

これでユーザー（コーチ）は：
1. URL にアクセス
2. Google ログイン
3. レポート生成
4. 自動で自分の Drive に保存

**技術的な設定は一切不要！**

---

## トラブルシューティング

### エラー: `redirect_uri_mismatch`

**原因**: リダイレクト URI が一致していない

**解決**:
1. Google Cloud Console で設定したリダイレクト URI を確認
2. Streamlit Cloud の実際の URL と一致しているか確認
3. `/_stcore/oauth` サフィックスがついているか確認

### エラー: アクセスがブロックされた

**原因**: OAuth 同意画面のテストユーザーに追加されていない

**解決**:
1. Google Cloud Console →「OAuth 同意画面」→「テストユーザー」
2. ユーザーのメールアドレスを追加

### Streamlit でエラーが表示される

**原因**: Secrets が正しく設定されていない

**解決**:
1. Streamlit Cloud の Settings → Secrets
2. CLIENT_ID と CLIENT_SECRET が正しいか確認
3. 保存後、アプリを再起動
