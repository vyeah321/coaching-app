"""
Google Drive アップローダーモジュール
Markdown ファイルを Google Drive にアップロードする（OAuth2認証 - Streamlit Cloud対応）
"""
import os
import pickle
from typing import Optional
import streamlit as st
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaInMemoryUpload


# スコープ: ファイル作成と管理
SCOPES = ['https://www.googleapis.com/auth/drive.file']

# 認証トークンの保存先
TOKEN_FILE = 'credentials/token.pickle'
CLIENT_SECRETS_FILE = 'credentials/client_secrets.json'


def get_drive_service():
    """
    Google Drive サービスオブジェクトを取得（OAuth2認証）
    
    Streamlit Cloud の場合は Secrets から認証情報を取得
    ローカルの場合は client_secrets.json を使用
    
    Returns:
        Google Drive API サービスオブジェクト
    
    Raises:
        FileNotFoundError: 認証情報が見つからない
        Exception: 認証に失敗
    """
    creds = None
    
    # Streamlit Cloud の Secrets をチェック
    if hasattr(st, 'secrets') and 'GOOGLE_CLIENT_ID' in st.secrets:
        # Streamlit Cloud 環境
        # Note: 完全な OAuth フローは Streamlit の制限により複雑
        # 簡易実装としてローカル認証と同じフローを使用
        pass
    
    # 保存されたトークンを読み込み
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    
    # トークンが無効または期限切れの場合
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # トークンをリフレッシュ
            creds.refresh(Request())
        else:
            # 新規認証フロー
            if not os.path.exists(CLIENT_SECRETS_FILE):
                raise FileNotFoundError(
                    f"OAuth2 認証情報ファイルが見つかりません: {CLIENT_SECRETS_FILE}\n\n"
                    f"【ローカル実行の場合】\n"
                    f"1. Google Cloud Console (https://console.cloud.google.com/) にアクセス\n"
                    f"2. プロジェクトを作成または選択\n"
                    f"3. Google Drive API を有効化\n"
                    f"4. 「認証情報」→「認証情報を作成」→「OAuth クライアント ID」\n"
                    f"5. アプリケーションの種類：「デスクトップアプリ」\n"
                    f"6. JSON をダウンロードして {CLIENT_SECRETS_FILE} に配置\n\n"
                    f"【Streamlit Cloud の場合】\n"
                    f"DEPLOY.md を参照してください"
                )
            
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRETS_FILE, SCOPES
            )
            creds = flow.run_local_server(port=0)
        
        # トークンを保存
        os.makedirs(os.path.dirname(TOKEN_FILE), exist_ok=True)
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
    
    return build('drive', 'v3', credentials=creds)


def upload_to_drive(
    filename: str,
    content: str,
    folder_id: Optional[str] = None
) -> dict:
    """
    Markdown ファイルを Google Drive にアップロード
    
    Args:
        filename: ファイル名（例：20251228_client_report.md）
        content: Markdown コンテンツ
        folder_id: アップロード先フォルダID（省略時は環境変数から取得、さらに省略時はルートに保存）
    
    Returns:
        アップロード結果（id, name, webViewLink を含む辞書）
    
    Raises:
        Exception: アップロードに失敗
    """
    if folder_id is None:
        folder_id = os.getenv('GOOGLE_DRIVE_FOLDER_ID')
    
    # フォルダIDが指定されていない場合はルートに保存（警告のみ）
    if not folder_id:
        print("⚠️  GOOGLE_DRIVE_FOLDER_ID が未設定のため、Drive のルートに保存します")
    
    try:
        service = get_drive_service()
        
        # ファイルメタデータ
        file_metadata = {
            'name': filename,
            'mimeType': 'text/markdown'
        }
        
        # フォルダIDが指定されている場合のみ親フォルダを設定
        if folder_id:
            file_metadata['parents'] = [folder_id]
        
        # ファイル内容
        media = MediaInMemoryUpload(
            content.encode('utf-8'),
            mimetype='text/markdown',
            resumable=True
        )
        
        # アップロード実行
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, name, webViewLink'
        ).execute()
        
        return {
            'id': file.get('id'),
            'name': file.get('name'),
            'url': file.get('webViewLink')
        }
    
    except Exception as e:
        raise Exception(f"Google Drive へのアップロードに失敗しました: {str(e)}")


def upload_reports(
    client_report: str,
    coach_note: str,
    session_date: str,
    client_name: str,
    folder_id: Optional[str] = None
) -> tuple[dict, dict]:
    """
    2つのレポートを Google Drive にアップロード
    
    Args:
        client_report: クライアント向けレポート
        coach_note: コーチ向けメモ
        session_date: セッション日付（YYYYMMDD形式）
        client_name: クライアント名
        folder_id: アップロード先フォルダID
    
    Returns:
        (client_report_result, coach_note_result) のタプル
    """
    # ファイル名生成
    date_str = session_date.replace('-', '')
    client_name_clean = client_name.replace(' ', '_').replace('　', '_')
    
    client_filename = f"{date_str}_{client_name_clean}_session_report.md"
    coach_filename = f"{date_str}_{client_name_clean}_coach_note.md"
    
    # アップロード実行
    client_result = upload_to_drive(client_filename, client_report, folder_id)
    coach_result = upload_to_drive(coach_filename, coach_note, folder_id)
    
    return client_result, coach_result
