# Streamlit Cloud デプロイガイド

## 前提条件

- GitHub アカウント
- Google Cloud Console のプロジェクト
- Streamlit Cloud アカウント（無料）

---

## 1. Google Cloud Console での設定

### 1.1 OAuth 同意画面の設定

1. [Google Cloud Console](https://console.cloud.google.com/) にアクセス
2. プロジェクトを作成または選択
3. 「APIとサービス」→「OAuth 同意画面」
4. ユーザータイプ：**「外部」**
5. 必須項目を入力：
   - アプリ名：`Coaching Session Organizer`
   - サポートメール：あなたのメールアドレス
   - スコープ追加：`https://www.googleapis.com/auth/drive.file`
6. テストユーザー追加（公開前）

### 1.2 OAuth クライアント ID 作成

1. 「認証情報」→「認証情報を作成」→「OAuth クライアント ID」
2. アプリケーションの種類：**「ウェブアプリケーション」** ⚠️（デスクトップではない）
3. 名前：`streamlit-cloud-oauth`
4. 承認済みのリダイレクト URI：
   ```
   https://あなたのアプリ名.streamlit.app/_stcore/oauth
   ```
   ※ 後で Streamlit Cloud の URL が確定したら追加
5. クライアント ID とクライアントシークレットをコピー

---

## 2. GitHub へのプッシュ

```bash
cd /Users/atsuvu/Sandbox/coaching_app
git remote add origin https://github.com/あなたのユーザー名/coaching_app.git
git push -u origin master
```

---

## 3. Streamlit Cloud へのデプロイ

### 3.1 デプロイ

1. [Streamlit Cloud](https://streamlit.io/cloud) にアクセス
2. GitHub アカウントでサインイン
3. 「New app」をクリック
4. リポジトリ選択：`coaching_app`
5. Main file path：`session_organizer/app.py`
6. 「Deploy」をクリック

### 3.2 Secrets の設定

1. デプロイ後、アプリ設定画面を開く
2. 「Secrets」タブを選択
3. 以下を入力：

```toml
GOOGLE_CLIENT_ID = "your-client-id.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "your-client-secret"

# 任意: 特定フォルダに保存する場合
GOOGLE_DRIVE_FOLDER_ID = ""

# アプリ設定
COACH_NAME = "デフォルトコーチ名"
DEFAULT_CLIENT_NAME = ""
```

4. 「Save」をクリック

### 3.3 リダイレクト URI の更新

1. Streamlit Cloud のアプリ URL をコピー（例：`https://coaching-app-xxx.streamlit.app`）
2. Google Cloud Console に戻る
3. OAuth クライアント ID の「承認済みのリダイレクト URI」に追加：
   ```
   https://coaching-app-xxx.streamlit.app/_stcore/oauth
   ```
4. 保存

---

## 4. アプリの公開

### テスト

1. Streamlit Cloud の URL にアクセス
2. Google アカウントでログイン
3. レポート生成とアップロードをテスト

### 公開範囲の設定

**Option A: プライベート（推奨）**
- Streamlit Cloud でアクセス制限を設定
- 招待したユーザーのみアクセス可能

**Option B: パブリック**
- 誰でもアクセス可能
- Google Cloud Console で OAuth アプリを「本番環境」に公開する必要あり

---

## トラブルシューティング

### リダイレクト URI エラー

**エラー:** `redirect_uri_mismatch`

**解決:**
1. Google Cloud Console でリダイレクト URI を確認
2. Streamlit Cloud の正確な URL を設定
3. `/_stcore/oauth` のサフィックスを忘れずに

### 認証が通らない

**解決:**
1. Streamlit Secrets に正しい CLIENT_ID と CLIENT_SECRET が設定されているか確認
2. Google Cloud Console で Drive API が有効化されているか確認

---

## 完了！

ユーザー（コーチ）は以下だけで使えます：
1. URL にアクセス
2. Google アカウントでログイン
3. レポート生成
4. 自動的に自分の Drive に保存
