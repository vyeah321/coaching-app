# Coaching App Prototype 実装資料

## 1. プロジェクト構成

```
coaching_app/
├── DESIGN.md                  # 設計資料
├── IMPLEMENTATION.md          # 本ファイル（実装資料）
├── README.md                  # プロジェクト概要
├── requirements.txt           # Python依存関係
├── .env.example              # 環境変数のサンプル
├── .gitignore                # Git除外設定
├── app.py                    # Streamlit メインアプリ
├── src/
│   ├── __init__.py
│   ├── report_generator.py  # レポート生成ロジック
│   ├── drive_uploader.py    # Google Drive連携
│   └── templates.py         # Markdownテンプレート
├── credentials/
│   └── service_account.json # Google Drive認証情報（Git管理外）
└── templates/
    ├── client_report.md     # クライアント向けテンプレート
    └── coach_note.md        # コーチ向けテンプレート
```

---

## 2. 技術スタック

### 2.1 必須ライブラリ

```txt
streamlit==1.29.0
google-api-python-client==2.108.0
google-auth==2.25.2
google-auth-oauthlib==1.2.0
google-auth-httplib2==0.2.0
python-dotenv==1.0.0
```

### 2.2 開発環境

- Python 3.10+
- pip または poetry

---

## 3. Google Drive API セットアップ（OAuth2認証）

### 3.1 Google Cloud Console での設定

1. [Google Cloud Console](https://console.cloud.google.com/) にアクセス
2. 新規プロジェクトを作成
   - プロジェクト名：`coaching-app-prototype`
3. Google Drive API を有効化
   - 「APIとサービス」→「ライブラリ」→「Google Drive API」→「有効にする」
4. OAuth 同意画面の設定
   - 「APIとサービス」→「OAuth 同意画面」
   - ユーザータイプ：「外部」を選択
   - アプリ名、サポートメールなどを入力
   - スコープの追加：`https://www.googleapis.com/auth/drive.file`
5. OAuth クライアント ID を作成
   - 「APIとサービス」→「認証情報」→「認証情報を作成」→「OAuth クライアント ID」
   - アプリケーションの種類：**「デスクトップアプリ」**
   - 名前：`coaching-app-client`
6. JSON をダウンロード
   - 作成された認証情報の右側のダウンロードアイコンをクリック
   - ダウンロードしたファイルを `credentials/client_secrets.json` にリネームして配置

### 3.2 初回認証

アプリ初回起動時に：
1. 自動的にブラウザが開きます
2. Google アカウントでログイン
3. アプリへのアクセスを許可
4. 認証完了後、トークンが `credentials/token.pickle` に自動保存されます

以降は自動的に認証されます（トークンの有効期限は自動更新）

### 3.3 Google Drive フォルダの準備（任意）

特定のフォルダに保存したい場合：
1. Google Drive で専用フォルダを作成（例：`CoachingApp_Reports`）
2. フォルダのURLからフォルダIDを取得
   - URL例：`https://drive.google.com/drive/folders/FOLDER_ID`
3. `.env` ファイルに `GOOGLE_DRIVE_FOLDER_ID` を設定

※ フォルダIDを設定しない場合は Drive のルートに保存されます

---

## 4. 環境変数設定

### 4.1 `.env` ファイルの作成

```bash
# Google Drive 設定（任意）
# フォルダIDを指定しない場合は Drive のルートに保存されます
GOOGLE_DRIVE_FOLDER_ID=

# アプリ設定
COACH_NAME=山田太郎
DEFAULT_CLIENT_NAME=
```

### 4.2 `.env.example` ファイル

```bash
# Google Drive 設定（任意）
# フォルダIDを指定しない場合は Drive のルートに保存されます
GOOGLE_DRIVE_FOLDER_ID=

# アプリ設定
COACH_NAME=
DEFAULT_CLIENT_NAME=
```

---

## 5. ファイル別実装詳細

### 5.1 `app.py` - メインアプリケーション

**責務：**
- Streamlit UI の構築
- ユーザー入力の受付
- レポート生成・保存の制御

**主要機能：**
- セッションメモ入力（st.text_area）
- 日付・クライアント名入力
- 「レポート生成」ボタン
- 「Google Driveに保存」ボタン
- 生成結果の表示（st.markdown）

**実装ポイント：**
```python
import streamlit as st
from src.report_generator import generate_reports
from src.drive_uploader import upload_to_drive

st.set_page_config(page_title="コーチングセッション整理")
st.title("コーチング・セッション整理（プロトタイプ）")

# 入力フォーム
session_memo = st.text_area("セッションメモ", height=300)
session_date = st.date_input("セッション日付")
client_name = st.text_input("クライアント名")

if st.button("レポート生成"):
    # レポート生成処理
    pass
```

---

### 5.2 `src/report_generator.py` - レポート生成

**責務：**
- セッションメモからレポートを生成
- Markdownフォーマットの適用

**主要関数：**

```python
def generate_reports(session_memo: str, session_date: str, client_name: str, coach_name: str) -> tuple[str, str]:
    """
    セッションメモから2つのレポートを生成
    
    Args:
        session_memo: セッションメモ（箇条書き想定）
        session_date: セッション日付
        client_name: クライアント名
        coach_name: コーチ名
    
    Returns:
        (client_report, coach_note) のタプル
    """
    pass
```

**実装アプローチ（プロトタイプ版）：**
1. フェーズ1：テンプレートベース（AI なし）
   - メモをそのまま適切なセクションに配置
   - 日付・名前などのメタ情報を埋め込み
2. フェーズ2：AI 統合（Optional）
   - OpenAI API / Claude API で要約・構造化
   - プロンプトテンプレート管理

---

### 5.3 `src/drive_uploader.py` - Google Drive 連携

**責務：**
- Google Drive API の認証
- Markdown ファイルのアップロード

**主要関数：**

```python
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaInMemoryUpload

def get_drive_service():
    """Google Drive サービスオブジェクトを取得"""
    SCOPES = ['https://www.googleapis.com/auth/drive.file']
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    return build('drive', 'v3', credentials=credentials)

def upload_to_drive(filename: str, content: str, folder_id: str) -> str:
    """
    Markdown ファイルを Google Drive にアップロード
    
    Args:
        filename: ファイル名（例：20231228_client_report.md）
        content: Markdown コンテンツ
        folder_id: アップロード先フォルダID
    
    Returns:
        アップロードされたファイルのURL
    """
    service = get_drive_service()
    
    file_metadata = {
        'name': filename,
        'parents': [folder_id],
        'mimeType': 'text/markdown'
    }
    
    media = MediaInMemoryUpload(
        content.encode('utf-8'),
        mimetype='text/markdown',
        resumable=True
    )
    
    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id, webViewLink'
    ).execute()
    
    return file.get('webViewLink')
```

---

### 5.4 `src/templates.py` - Markdown テンプレート

**責務：**
- レポートの Markdown テンプレート定義

**実装例：**

```python
def get_client_report_template(session_date: str, coach_name: str, client_name: str, insights: list, actions: list, questions: list) -> str:
    return f"""# セッションレポート

## セッション概要
- 日付：{session_date}
- コーチ：{coach_name}
- クライアント：{client_name}

## 今回の気づき

{chr(10).join(f"- {insight}" for insight in insights)}

## 次回までの行動

{chr(10).join(f"- {action}" for action in actions)}

## 次に考えたい問い

{chr(10).join(f"- {q}" for q in questions)}
"""

def get_coach_note_template(session_date: str, client_name: str, observations: list, interventions: list, hypotheses: list) -> str:
    return f"""# コーチ用メモ

**クライアント：** {client_name}  
**日付：** {session_date}

## 観察された変化

{chr(10).join(f"- {obs}" for obs in observations)}

## 介入ポイント

{chr(10).join(f"- {intervention}" for intervention in interventions)}

## 次回セッション仮説

{chr(10).join(f"- {hyp}" for hyp in hypotheses)}
"""
```

---

## 6. セットアップ手順

### 6.1 初回セットアップ

```bash
# 1. リポジトリのクローン（または初期化）
cd /Users/atsuvu/Sandbox/coaching_app

# 2. 仮想環境の作成
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# または
venv\Scripts\activate  # Windows

# 3. 依存関係のインストール
pip install -r requirements.txt

# 4. 環境変数の設定
cp .env.example .env
# .env ファイルを編集して実際の値を設定

# 5. Google Drive 認証情報の配置
# credentials/service_account.json を配置
```

### 6.2 実行

```bash
# Streamlit アプリの起動
streamlit run app.py

# ブラウザで自動的に開く（通常 http://localhost:8501）
```

---

## 7. 実装の優先順位

### Phase 1: 最小動作版（MVP）

- [ ] Streamlit UI の基本構造
- [ ] セッションメモ入力フォーム
- [ ] 固定テンプレートでのレポート生成
- [ ] Google Drive へのアップロード

**目標：** 1日で動くものを作る

### Phase 2: 実用化

- [ ] メモの自動解析・セクション分け
- [ ] 複数セッションの履歴管理
- [ ] エラーハンドリング強化
- [ ] UI の洗練

**目標：** 実コーチに触ってもらえるレベル

### Phase 3: AI 統合（Optional）

- [ ] OpenAI API / Claude API 連携
- [ ] 自動要約・構造化
- [ ] プロンプトのカスタマイズ

**目標：** 手作業ゼロでレポート生成

---

## 8. テスト方法

### 8.1 手動テスト

**テストケース1：基本フロー**
1. セッションメモを入力
2. 「レポート生成」をクリック
3. 生成されたレポートが表示される
4. 「Google Driveに保存」をクリック
5. Drive に2つのファイルが保存される

**テストケース2：空入力**
- メモが空の場合のエラーハンドリング

**テストケース3：長文メモ**
- 大量のテキスト入力でのパフォーマンス

### 8.2 確認事項

- [ ] Markdown のフォーマットが正しいか
- [ ] Google Drive にファイルが正しく保存されるか
- [ ] 日本語が文字化けしないか（UTF-8）
- [ ] ファイル名の重複時の挙動

---

## 9. トラブルシューティング
FileNotFoundError: OAuth2 認証情報ファイルが見つかりません`

**解決：**
1. Google Cloud Console で OAuth クライアント ID を作成
2. JSON を `credentials/client_secrets.json` に配置
3. アプリケーションの種類が「デスクトップアプリ」であることを確認

---

**エラー：** 初回認証時にブラウザが開かない

**解決：**
1. ターミナルに表示された URL を手動でブラウザで開く
2. ローカル環境でポート転送の問題がないか確認
3. `flow.run_local_server(port=0)` が実行されている
**解決：**
1. JSON ファイルが正しい場所にあるか確認
2. `.env` のパスが正しいか確認

---

### 9.2 Streamlit エラー

**エラー：** `ModuleNotFoundError`

**解決：**
```bash
# 仮想環境が有効化されているか確認
which python

# 依存関係を再インストール
pip install -r requirements.txt
```

---

## 10. 次のステップ

### 10.1 実装完了後

1. 実際のセッションメモでテスト
2. コーチ2-3名に触ってもらう
3. フィードバックを収集

### 10.2 改善候補

- セッションメモのフォーマットガイド表示
- 過去のレポートをアプリ内で閲覧
- テンプレートのカスタマイズ機能
- Slack / Notion への連携

---

## 11. 参考リンク

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Google Drive API Python Quickstart](https://developers.google.com/drive/api/quickstart/python)
- [Google Cloud Console](https://console.cloud.google.com/)
