"""
Google Drive アップローダーモジュール
Markdown ファイルを Google Drive にアップロードする
"""
import os
from typing import Optional
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaInMemoryUpload


# スコープ: ファイル作成のみ
SCOPES = ['https://www.googleapis.com/auth/drive.file']


def get_drive_service():
    """
    Google Drive サービスオブジェクトを取得
    
    Returns:
        Google Drive API サービスオブジェクト
    
    Raises:
        FileNotFoundError: 認証情報ファイルが見つからない
        Exception: 認証に失敗
    """
    service_account_file = os.getenv('GOOGLE_SERVICE_ACCOUNT_FILE', 'credentials/service_account.json')
    
    if not os.path.exists(service_account_file):
        raise FileNotFoundError(
            f"認証情報ファイルが見つかりません: {service_account_file}\n"
            f"Google Cloud Console からサービスアカウントの JSON キーをダウンロードし、\n"
            f"{service_account_file} に配置してください。"
        )
    
    credentials = service_account.Credentials.from_service_account_file(
        service_account_file, scopes=SCOPES
    )
    
    return build('drive', 'v3', credentials=credentials)


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
        folder_id: アップロード先フォルダID（省略時は環境変数から取得）
    
    Returns:
        アップロード結果（id, name, webViewLink を含む辞書）
    
    Raises:
        ValueError: フォルダIDが指定されていない
        Exception: アップロードに失敗
    """
    if folder_id is None:
        folder_id = os.getenv('GOOGLE_DRIVE_FOLDER_ID')
    
    if not folder_id:
        raise ValueError(
            "Google Drive のフォルダIDが設定されていません。\n"
            ".env ファイルに GOOGLE_DRIVE_FOLDER_ID を設定してください。"
        )
    
    try:
        service = get_drive_service()
        
        # ファイルメタデータ
        file_metadata = {
            'name': filename,
            'parents': [folder_id],
            'mimeType': 'text/markdown'
        }
        
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
