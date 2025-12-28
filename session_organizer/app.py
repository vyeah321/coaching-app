"""
Coaching App Prototype - Streamlit UI
コーチング・セッション整理アプリ
"""
import os
from datetime import date
import streamlit as st
from dotenv import load_dotenv

from src.report_generator import generate_reports
from src.drive_uploader import upload_reports


# 環境変数の読み込み
load_dotenv()


def main():
    """メインアプリケーション"""
    
    # ページ設定
    st.set_page_config(
        page_title="コーチングセッション整理",
        page_icon="📝",
        layout="wide"
    )
    
    # タイトル
    st.title("📝 コーチング・セッション整理")
    st.caption("プロトタイプ版 - セッションメモから2つのレポートを自動生成")
    
    st.divider()
    
    # === 入力セクション ===
    st.header("1️⃣ セッション情報の入力")
    
    col1, col2 = st.columns(2)
    
    with col1:
        session_date = st.date_input(
            "セッション日付",
            value=date.today()
        )
    
    with col2:
        client_name = st.text_input(
            "クライアント名",
            value=os.getenv("DEFAULT_CLIENT_NAME", ""),
            placeholder="例: 山田太郎"
        )
    
    coach_name = st.text_input(
        "コーチ名",
        value=os.getenv("COACH_NAME", ""),
        placeholder="例: 田中花子"
    )
    
    st.subheader("セッションメモ")
    st.caption("箇条書きで入力してください。「気づき」「行動」「問い」などのキーワードでセクション分けできます。")
    
    session_memo = st.text_area(
        "セッションメモ",
        height=300,
        placeholder="""例:
気づき
- 自分の強みは〇〇だと気づいた
- 今まで避けていた行動の理由が明確になった

行動
- 来週までに〇〇をやってみる
- 〇〇について調べる

問い
- 本当に大切にしたいことは何か？
""",
        label_visibility="collapsed"
    )
    
    st.divider()
    
    # === レポート生成セクション ===
    st.header("2️⃣ レポート生成")
    
    generate_button = st.button(
        "🔄 レポートを生成",
        type="primary",
        use_container_width=True
    )
    
    if generate_button:
        # バリデーション
        if not session_memo.strip():
            st.error("セッションメモを入力してください")
            return
        
        if not client_name.strip():
            st.error("クライアント名を入力してください")
            return
        
        if not coach_name.strip():
            st.error("コーチ名を入力してください")
            return
        
        # レポート生成
        with st.spinner("レポートを生成中..."):
            try:
                client_report, coach_note = generate_reports(
                    session_memo=session_memo,
                    session_date=str(session_date),
                    client_name=client_name,
                    coach_name=coach_name
                )
                
                # セッションステートに保存
                st.session_state['client_report'] = client_report
                st.session_state['coach_note'] = coach_note
                st.session_state['session_date'] = str(session_date)
                st.session_state['client_name'] = client_name
                
                st.success("✅ レポートを生成しました")
            
            except Exception as e:
                st.error(f"❌ エラーが発生しました: {str(e)}")
                return
    
    # === レポート表示セクション ===
    if 'client_report' in st.session_state and 'coach_note' in st.session_state:
        st.divider()
        st.header("3️⃣ 生成結果")
        
        tab1, tab2 = st.tabs(["📄 クライアント向けレポート", "📋 コーチ用メモ"])
        
        with tab1:
            st.markdown(st.session_state['client_report'])
            
            # ダウンロードボタン
            st.download_button(
                label="📥 Markdown をダウンロード",
                data=st.session_state['client_report'],
                file_name=f"{str(session_date).replace('-', '')}_{client_name}_report.md",
                mime="text/markdown"
            )
        
        with tab2:
            st.markdown(st.session_state['coach_note'])
            
            # ダウンロードボタン
            st.download_button(
                label="📥 Markdown をダウンロード",
                data=st.session_state['coach_note'],
                file_name=f"{str(session_date).replace('-', '')}_{client_name}_coach_note.md",
                mime="text/markdown"
            )
        
        # === Google Drive 保存セクション ===
        st.divider()
        st.header("4️⃣ Google Drive に保存")
        
        # OAuth2 認証状態の確認
        client_secrets_file = 'credentials/client_secrets.json'
        
        if not os.path.exists(client_secrets_file):
            st.warning(
                "⚠️ Google Drive 連携の設定が必要です\n\n"
                "**セットアップ手順:**\n"
                "1. [Google Cloud Console](https://console.cloud.google.com/) でプロジェクト作成\n"
                "2. Google Drive API を有効化\n"
                "3. OAuth クライアント ID を作成（デスクトップアプリ）\n"
                "4. JSON を `credentials/client_secrets.json` に配置\n\n"
                "詳細は [IMPLEMENTATION.md](IMPLEMENTATION.md) を参照"
            )
        else:
            upload_button = st.button(
                "☁️ Google Drive に保存",
                type="secondary",
                use_container_width=True
            )
            
            if upload_button:
                with st.spinner("Google Drive にアップロード中..."):
                    try:
                        client_result, coach_result = upload_reports(
                            client_report=st.session_state['client_report'],
                            coach_note=st.session_state['coach_note'],
                            session_date=st.session_state['session_date'],
                            client_name=st.session_state['client_name']
                        )
                        
                        st.success("✅ Google Drive に保存しました")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.info(f"📄 {client_result['name']}")
                            if client_result.get('url'):
                                st.markdown(f"[ファイルを開く]({client_result['url']})")
                        
                        with col2:
                            st.info(f"📋 {coach_result['name']}")
                            if coach_result.get('url'):
                                st.markdown(f"[ファイルを開く]({coach_result['url']})")
                    
                    except Exception as e:
                        st.error(f"❌ アップロードに失敗しました: {str(e)}")
    
    # === フッター ===
    st.divider()
    with st.expander("ℹ️ 使い方"):
        st.markdown("""
        ### 使い方
        
        1. **セッション情報を入力**
           - 日付、クライアント名、コーチ名を入力
        
        2. **セッションメモを入力**
           - 箇条書きで自由に記入
           - 「気づき」「行動」「問い」などのキーワードで自動分類
        
        3. **レポートを生成**
           - ボタンをクリックしてレポートを生成
        
        4. **Google Drive に保存**
           - 必要に応じて Drive に保存
        
        ### セットアップ
        
        Google Drive 連携を使う場合:
        - `.env` ファイルに `GOOGLE_DRIVE_FOLDER_ID` を設定
        - `credentials/service_account.json` に認証情報を配置
        
        詳細は [IMPLEMENTATION.md](IMPLEMENTATION.md) を参照
        """)


if __name__ == "__main__":
    main()
