"""
コーチングサポートアプリ

クライアントのセッション記録、目標設定、進捗管理をサポートするStreamlitアプリ
"""

import streamlit as st
from datetime import datetime, date
import json
from pathlib import Path
from typing import Dict, List, Optional

# データディレクトリの設定
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
CLIENTS_FILE = DATA_DIR / "clients.json"
SESSIONS_FILE = DATA_DIR / "sessions.json"


def load_data(file_path: Path) -> Dict:
    """JSONファイルからデータを読み込む"""
    if file_path.exists():
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def save_data(file_path: Path, data: Dict) -> None:
    """JSONファイルにデータを保存"""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def init_session_state():
    """セッション状態の初期化"""
    if 'clients' not in st.session_state:
        st.session_state.clients = load_data(CLIENTS_FILE)
    if 'sessions' not in st.session_state:
        st.session_state.sessions = load_data(SESSIONS_FILE)


def save_all_data():
    """全データをファイルに保存"""
    save_data(CLIENTS_FILE, st.session_state.clients)
    save_data(SESSIONS_FILE, st.session_state.sessions)


# ページ設定
st.set_page_config(
    page_title="コーチングサポートアプリ",
    page_icon="🎯",
    layout="wide"
)

# セッション状態の初期化
init_session_state()

# サイドバー - ナビゲーション
st.sidebar.title("🎯 コーチングサポート")
page = st.sidebar.radio(
    "メニュー",
    ["クライアント管理", "セッション記録", "目標トラッキング", "レポート"]
)

# ========== クライアント管理ページ ==========
if page == "クライアント管理":
    st.header("👥 クライアント管理")
    
    # 新規クライアント追加
    with st.expander("➕ 新規クライアント追加", expanded=False):
        with st.form("add_client_form"):
            client_name = st.text_input("クライアント名", key="new_client_name")
            client_email = st.text_input("メールアドレス", key="new_client_email")
            client_phone = st.text_input("電話番号", key="new_client_phone")
            client_notes = st.text_area("メモ", key="new_client_notes")
            
            submitted = st.form_submit_button("クライアントを追加")
            
            if submitted and client_name:
                client_id = f"client_{len(st.session_state.clients) + 1}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
                st.session_state.clients[client_id] = {
                    "name": client_name,
                    "email": client_email,
                    "phone": client_phone,
                    "notes": client_notes,
                    "created_at": datetime.now().isoformat(),
                    "goals": []
                }
                save_all_data()
                st.success(f"✅ {client_name} を追加しました！")
                st.rerun()
    
    # クライアント一覧
    st.subheader("📋 クライアント一覧")
    
    if not st.session_state.clients:
        st.info("まだクライアントが登録されていません。上のフォームから追加してください。")
    else:
        for client_id, client in st.session_state.clients.items():
            with st.expander(f"👤 {client['name']}", expanded=False):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(f"**メール:** {client.get('email', 'N/A')}")
                    st.write(f"**電話:** {client.get('phone', 'N/A')}")
                    st.write(f"**登録日:** {client.get('created_at', 'N/A')[:10]}")
                    if client.get('notes'):
                        st.write(f"**メモ:** {client['notes']}")
                
                with col2:
                    if st.button("🗑️ 削除", key=f"delete_{client_id}"):
                        del st.session_state.clients[client_id]
                        save_all_data()
                        st.rerun()

# ========== セッション記録ページ ==========
elif page == "セッション記録":
    st.header("📝 セッション記録")
    
    if not st.session_state.clients:
        st.warning("まず「クライアント管理」からクライアントを登録してください。")
    else:
        # クライアント選択
        client_options = {cid: c['name'] for cid, c in st.session_state.clients.items()}
        selected_client_id = st.selectbox(
            "クライアントを選択",
            options=list(client_options.keys()),
            format_func=lambda x: client_options[x]
        )
        
        # 新規セッション記録
        with st.expander("➕ 新規セッション記録", expanded=True):
            with st.form("add_session_form"):
                session_date = st.date_input("セッション日", value=date.today())
                session_duration = st.number_input("時間（分）", min_value=15, max_value=240, value=60, step=15)
                session_topic = st.text_input("セッションのテーマ")
                session_summary = st.text_area("セッション概要", height=150)
                session_insights = st.text_area("気づき・インサイト", height=100)
                session_actions = st.text_area("アクションアイテム", height=100)
                
                submitted = st.form_submit_button("セッションを記録")
                
                if submitted:
                    session_id = f"session_{len(st.session_state.sessions) + 1}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
                    st.session_state.sessions[session_id] = {
                        "client_id": selected_client_id,
                        "date": session_date.isoformat(),
                        "duration": session_duration,
                        "topic": session_topic,
                        "summary": session_summary,
                        "insights": session_insights,
                        "actions": session_actions,
                        "created_at": datetime.now().isoformat()
                    }
                    save_all_data()
                    st.success("✅ セッションを記録しました！")
                    st.rerun()
        
        # セッション履歴
        st.subheader(f"📚 {client_options[selected_client_id]} のセッション履歴")
        
        client_sessions = {
            sid: s for sid, s in st.session_state.sessions.items() 
            if s['client_id'] == selected_client_id
        }
        
        if not client_sessions:
            st.info("まだセッションが記録されていません。")
        else:
            # 日付順にソート（新しい順）
            sorted_sessions = sorted(
                client_sessions.items(),
                key=lambda x: x[1]['date'],
                reverse=True
            )
            
            for session_id, session in sorted_sessions:
                with st.expander(f"📅 {session['date']} - {session.get('topic', 'テーマなし')}", expanded=False):
                    st.write(f"**時間:** {session['duration']}分")
                    st.write(f"**概要:** {session.get('summary', 'N/A')}")
                    st.write(f"**気づき:** {session.get('insights', 'N/A')}")
                    st.write(f"**アクション:** {session.get('actions', 'N/A')}")
                    
                    if st.button("🗑️ 削除", key=f"delete_session_{session_id}"):
                        del st.session_state.sessions[session_id]
                        save_all_data()
                        st.rerun()

# ========== 目標トラッキングページ ==========
elif page == "目標トラッキング":
    st.header("🎯 目標トラッキング")
    
    if not st.session_state.clients:
        st.warning("まず「クライアント管理」からクライアントを登録してください。")
    else:
        # クライアント選択
        client_options = {cid: c['name'] for cid, c in st.session_state.clients.items()}
        selected_client_id = st.selectbox(
            "クライアントを選択",
            options=list(client_options.keys()),
            format_func=lambda x: client_options[x],
            key="goal_client_select"
        )
        
        # 新規目標追加
        with st.expander("➕ 新規目標設定", expanded=False):
            with st.form("add_goal_form"):
                goal_title = st.text_input("目標")
                goal_description = st.text_area("詳細")
                goal_deadline = st.date_input("期限", value=None)
                goal_category = st.selectbox("カテゴリ", ["キャリア", "スキル", "ライフスタイル", "人間関係", "その他"])
                
                submitted = st.form_submit_button("目標を追加")
                
                if submitted and goal_title:
                    if 'goals' not in st.session_state.clients[selected_client_id]:
                        st.session_state.clients[selected_client_id]['goals'] = []
                    
                    goal = {
                        "id": f"goal_{len(st.session_state.clients[selected_client_id]['goals']) + 1}",
                        "title": goal_title,
                        "description": goal_description,
                        "deadline": goal_deadline.isoformat() if goal_deadline else None,
                        "category": goal_category,
                        "status": "進行中",
                        "progress": 0,
                        "created_at": datetime.now().isoformat()
                    }
                    
                    st.session_state.clients[selected_client_id]['goals'].append(goal)
                    save_all_data()
                    st.success("✅ 目標を追加しました！")
                    st.rerun()
        
        # 目標一覧
        st.subheader(f"🎯 {client_options[selected_client_id]} の目標")
        
        goals = st.session_state.clients[selected_client_id].get('goals', [])
        
        if not goals:
            st.info("まだ目標が設定されていません。")
        else:
            for i, goal in enumerate(goals):
                with st.expander(f"{goal['title']} ({goal['status']})", expanded=False):
                    st.write(f"**カテゴリ:** {goal['category']}")
                    st.write(f"**詳細:** {goal.get('description', 'N/A')}")
                    if goal.get('deadline'):
                        st.write(f"**期限:** {goal['deadline']}")
                    
                    # 進捗更新
                    new_progress = st.slider(
                        "進捗",
                        0, 100,
                        goal.get('progress', 0),
                        key=f"progress_{selected_client_id}_{i}"
                    )
                    
                    new_status = st.selectbox(
                        "ステータス",
                        ["未着手", "進行中", "完了", "保留"],
                        index=["未着手", "進行中", "完了", "保留"].index(goal.get('status', '進行中')),
                        key=f"status_{selected_client_id}_{i}"
                    )
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("💾 更新", key=f"update_goal_{i}"):
                            st.session_state.clients[selected_client_id]['goals'][i]['progress'] = new_progress
                            st.session_state.clients[selected_client_id]['goals'][i]['status'] = new_status
                            save_all_data()
                            st.success("更新しました！")
                            st.rerun()
                    
                    with col2:
                        if st.button("🗑️ 削除", key=f"delete_goal_{i}"):
                            st.session_state.clients[selected_client_id]['goals'].pop(i)
                            save_all_data()
                            st.rerun()

# ========== レポートページ ==========
elif page == "レポート":
    st.header("📊 レポート")
    
    if not st.session_state.clients:
        st.warning("まず「クライアント管理」からクライアントを登録してください。")
    else:
        # 統計情報
        st.subheader("📈 統計情報")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("総クライアント数", len(st.session_state.clients))
        
        with col2:
            st.metric("総セッション数", len(st.session_state.sessions))
        
        with col3:
            total_minutes = sum(s.get('duration', 0) for s in st.session_state.sessions.values())
            st.metric("総セッション時間", f"{total_minutes}分")
        
        # クライアント別レポート
        st.subheader("👥 クライアント別レポート")
        
        for client_id, client in st.session_state.clients.items():
            with st.expander(f"📋 {client['name']}", expanded=False):
                # クライアントのセッション数
                client_sessions = [s for s in st.session_state.sessions.values() if s['client_id'] == client_id]
                st.write(f"**セッション数:** {len(client_sessions)}")
                
                # セッション時間の合計
                total_time = sum(s.get('duration', 0) for s in client_sessions)
                st.write(f"**総セッション時間:** {total_time}分 ({total_time/60:.1f}時間)")
                
                # 目標の進捗
                goals = client.get('goals', [])
                if goals:
                    st.write(f"**目標数:** {len(goals)}")
                    completed = len([g for g in goals if g.get('status') == '完了'])
                    st.write(f"**完了した目標:** {completed}/{len(goals)}")
                    
                    avg_progress = sum(g.get('progress', 0) for g in goals) / len(goals)
                    st.progress(avg_progress / 100)
                    st.write(f"平均進捗: {avg_progress:.0f}%")
                else:
                    st.write("**目標:** 未設定")
                
                # 最終セッション日
                if client_sessions:
                    latest_session = max(client_sessions, key=lambda s: s['date'])
                    st.write(f"**最終セッション:** {latest_session['date']}")

# フッター
st.sidebar.markdown("---")
st.sidebar.info("💡 このアプリはコーチングセッションの管理をサポートします")
