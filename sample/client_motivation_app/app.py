"""
クライアント向けモチベーションアプリ 🌟

目標達成をゲーム感覚で楽しめる、ワクワクするコーチングクライアント向けアプリ
"""

import streamlit as st
from datetime import datetime, date, timedelta
import json
from pathlib import Path
from typing import Dict, List
import random

# データディレクトリの設定
DATA_DIR = Path("client_data")
DATA_DIR.mkdir(exist_ok=True)
USER_FILE = DATA_DIR / "user_profile.json"
GOALS_FILE = DATA_DIR / "goals.json"
ACHIEVEMENTS_FILE = DATA_DIR / "achievements.json"
DAILY_LOG_FILE = DATA_DIR / "daily_log.json"


def load_json(file_path: Path) -> Dict:
    """JSONファイルからデータを読み込む"""
    if file_path.exists():
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def save_json(file_path: Path, data: Dict) -> None:
    """JSONファイルにデータを保存"""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def init_session_state():
    """セッション状態の初期化"""
    if 'user_profile' not in st.session_state:
        profile = load_json(USER_FILE)
        if not profile:
            profile = {
                "name": "未設定",
                "level": 1,
                "experience": 0,
                "total_points": 0,
                "streak_days": 0,
                "badges": [],
                "created_at": datetime.now().isoformat()
            }
        st.session_state.user_profile = profile
    
    if 'goals' not in st.session_state:
        st.session_state.goals = load_json(GOALS_FILE)
    
    if 'achievements' not in st.session_state:
        achievements = load_json(ACHIEVEMENTS_FILE)
        if not achievements:
            achievements = {"unlocked": [], "history": []}
        st.session_state.achievements = achievements
    
    if 'daily_log' not in st.session_state:
        st.session_state.daily_log = load_json(DAILY_LOG_FILE)


def save_all_data():
    """全データをファイルに保存"""
    save_json(USER_FILE, st.session_state.user_profile)
    save_json(GOALS_FILE, st.session_state.goals)
    save_json(ACHIEVEMENTS_FILE, st.session_state.achievements)
    save_json(DAILY_LOG_FILE, st.session_state.daily_log)


def add_experience(points: int):
    """経験値を追加してレベルアップをチェック"""
    st.session_state.user_profile['experience'] += points
    st.session_state.user_profile['total_points'] += points
    
    # レベルアップ判定（100ポイントごとにレベルアップ）
    level_up_threshold = st.session_state.user_profile['level'] * 100
    if st.session_state.user_profile['experience'] >= level_up_threshold:
        st.session_state.user_profile['level'] += 1
        st.session_state.user_profile['experience'] = 0
        st.balloons()
        st.success(f"🎉 レベルアップ！レベル {st.session_state.user_profile['level']} になりました！")


def check_badge(badge_id: str, badge_name: str, condition: bool):
    """バッジ獲得条件をチェック"""
    if condition and badge_id not in st.session_state.user_profile['badges']:
        st.session_state.user_profile['badges'].append(badge_id)
        st.session_state.achievements['unlocked'].append({
            "badge_id": badge_id,
            "name": badge_name,
            "unlocked_at": datetime.now().isoformat()
        })
        st.success(f"🏆 新しいバッジ獲得: {badge_name}")
        save_all_data()


def get_motivational_quote() -> str:
    """モチベーショナルな引用を返す"""
    quotes = [
        "今日の小さな一歩が、明日の大きな飛躍につながる 🚀",
        "あなたの可能性は無限大です ✨",
        "毎日が成長のチャンスです 🌱",
        "信じる心が奇跡を起こします 💫",
        "一歩ずつ、着実に前進しましょう 👣",
        "あなたは既に素晴らしい存在です 🌟",
        "挑戦することで新しい自分に出会えます 🦋",
        "今この瞬間から、変化は始まります 🌈"
    ]
    return random.choice(quotes)


# ページ設定
st.set_page_config(
    page_title="モチベーションアプリ",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# カスタムCSS
st.markdown("""
<style>
    .big-font {
        font-size: 24px !important;
        font-weight: bold;
    }
    .success-box {
        padding: 20px;
        border-radius: 10px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        text-align: center;
        margin: 10px 0;
    }
    .goal-card {
        padding: 15px;
        border-radius: 8px;
        background: #f0f2f6;
        margin: 10px 0;
        border-left: 4px solid #667eea;
    }
    .badge-icon {
        font-size: 48px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# セッション状態の初期化
init_session_state()

# サイドバー - ユーザープロフィール
st.sidebar.markdown("---")
st.sidebar.markdown("### 👤 あなたのプロフィール")

user = st.session_state.user_profile
st.sidebar.markdown(f"**名前:** {user['name']}")
st.sidebar.markdown(f"**レベル:** 🎮 {user['level']}")

# 経験値バー
exp_progress = user['experience'] / (user['level'] * 100)
st.sidebar.progress(exp_progress)
st.sidebar.caption(f"経験値: {user['experience']}/{user['level'] * 100}")

st.sidebar.markdown(f"**総ポイント:** ⭐ {user['total_points']}")
st.sidebar.markdown(f"**連続日数:** 🔥 {user['streak_days']} 日")
st.sidebar.markdown(f"**バッジ数:** 🏆 {len(user['badges'])}")

st.sidebar.markdown("---")

# メインナビゲーション
page = st.sidebar.radio(
    "📱 メニュー",
    ["🏠 ダッシュボード", "🎯 目標設定", "📝 今日の振り返り", "🏆 達成バッジ", "⚙️ 設定"]
)

# ========== ダッシュボード ==========
if page == "🏠 ダッシュボード":
    st.title("🌟 ようこそ！あなたの成長ダッシュボード")
    
    # 今日のモチベーション
    st.markdown(f'<div class="success-box"><h2>{get_motivational_quote()}</h2></div>', unsafe_allow_html=True)
    
    # 統計情報
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("レベル", f"🎮 {user['level']}", "+1" if user['experience'] > 50 else "")
    
    with col2:
        total_goals = len(st.session_state.goals)
        st.metric("目標数", f"🎯 {total_goals}")
    
    with col3:
        completed = sum(1 for g in st.session_state.goals.values() if g.get('status') == '達成')
        st.metric("達成済み", f"✅ {completed}")
    
    with col4:
        st.metric("バッジ", f"🏆 {len(user['badges'])}")
    
    st.markdown("---")
    
    # 今週の目標
    st.subheader("📅 今週の注目目標")
    
    if not st.session_state.goals:
        st.info("まだ目標が設定されていません。「🎯 目標設定」から追加してみましょう！")
    else:
        active_goals = {gid: g for gid, g in st.session_state.goals.items() 
                       if g.get('status') != '達成'}
        
        if active_goals:
            for goal_id, goal in list(active_goals.items())[:3]:
                with st.container():
                    st.markdown(f'<div class="goal-card">', unsafe_allow_html=True)
                    col1, col2 = st.columns([4, 1])
                    
                    with col1:
                        st.markdown(f"**{goal['title']}** {goal.get('emoji', '🎯')}")
                        progress = goal.get('progress', 0)
                        st.progress(progress / 100)
                        st.caption(f"{progress}% 完了")
                    
                    with col2:
                        if st.button("✏️", key=f"edit_{goal_id}"):
                            st.session_state.editing_goal = goal_id
                    
                    st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.success("🎉 すべての目標を達成しました！新しい目標を設定しましょう！")
    
    st.markdown("---")
    
    # クイックアクション
    st.subheader("⚡ クイックアクション")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📝 今日の振り返りを記録", use_container_width=True):
            st.session_state.quick_action = "reflection"
    
    with col2:
        if st.button("🎯 新しい目標を追加", use_container_width=True):
            st.session_state.quick_action = "new_goal"
    
    with col3:
        if st.button("🏆 バッジを確認", use_container_width=True):
            st.session_state.quick_action = "badges"

# ========== 目標設定 ==========
elif page == "🎯 目標設定":
    st.title("🎯 あなたの目標を設定しよう")
    
    # 新規目標追加
    with st.expander("➕ 新しい目標を追加", expanded=True):
        with st.form("add_goal_form"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                goal_title = st.text_input("目標は何ですか？", placeholder="例: 毎日30分運動する")
            
            with col2:
                goal_emoji = st.selectbox("絵文字", ["🎯", "💪", "📚", "🎨", "🏃", "🧘", "💼", "🌟", "🚀", "🎵"])
            
            goal_description = st.text_area("詳細（なぜこの目標を達成したいですか？）")
            
            col1, col2 = st.columns(2)
            with col1:
                goal_category = st.selectbox("カテゴリ", 
                    ["健康・運動", "学習・成長", "仕事・キャリア", "人間関係", "趣味・楽しみ", "その他"])
            
            with col2:
                goal_deadline = st.date_input("達成期限", value=None)
            
            goal_importance = st.slider("重要度", 1, 5, 3, help="1=低い、5=非常に高い")
            
            submitted = st.form_submit_button("🚀 目標を設定する", use_container_width=True)
            
            if submitted and goal_title:
                goal_id = f"goal_{len(st.session_state.goals) + 1}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
                st.session_state.goals[goal_id] = {
                    "title": goal_title,
                    "emoji": goal_emoji,
                    "description": goal_description,
                    "category": goal_category,
                    "deadline": goal_deadline.isoformat() if goal_deadline else None,
                    "importance": goal_importance,
                    "status": "進行中",
                    "progress": 0,
                    "created_at": datetime.now().isoformat(),
                    "milestones": []
                }
                
                # 経験値とバッジ
                add_experience(10)
                check_badge("first_goal", "🎯 はじめの一歩", len(st.session_state.goals) == 1)
                check_badge("goal_master", "🏅 目標マスター", len(st.session_state.goals) >= 5)
                
                save_all_data()
                st.success(f"✨ 目標「{goal_title}」を設定しました！")
                st.balloons()
                st.rerun()
    
    st.markdown("---")
    
    # 目標一覧
    st.subheader("📋 あなたの目標リスト")
    
    if not st.session_state.goals:
        st.info("目標を追加して、ワクワクする未来への一歩を踏み出しましょう！")
    else:
        # カテゴリでフィルター
        filter_category = st.selectbox("カテゴリでフィルター", 
            ["すべて", "健康・運動", "学習・成長", "仕事・キャリア", "人間関係", "趣味・楽しみ", "その他"])
        
        filtered_goals = st.session_state.goals
        if filter_category != "すべて":
            filtered_goals = {gid: g for gid, g in st.session_state.goals.items() 
                            if g.get('category') == filter_category}
        
        for goal_id, goal in filtered_goals.items():
            with st.expander(f"{goal.get('emoji', '🎯')} {goal['title']} ({goal['status']})", expanded=False):
                st.write(f"**カテゴリ:** {goal.get('category', 'N/A')}")
                st.write(f"**重要度:** {'⭐' * goal.get('importance', 3)}")
                
                if goal.get('deadline'):
                    st.write(f"**期限:** {goal['deadline']}")
                
                if goal.get('description'):
                    st.write(f"**詳細:** {goal['description']}")
                
                st.markdown("---")
                
                # 進捗更新
                new_progress = st.slider(
                    "進捗", 0, 100, goal.get('progress', 0),
                    key=f"progress_{goal_id}"
                )
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("💾 進捗を更新", key=f"update_{goal_id}"):
                        old_progress = goal.get('progress', 0)
                        st.session_state.goals[goal_id]['progress'] = new_progress
                        
                        # 進捗に応じて経験値付与
                        if new_progress > old_progress:
                            points = (new_progress - old_progress) // 10
                            add_experience(points)
                        
                        # 達成チェック
                        if new_progress == 100 and goal['status'] != '達成':
                            st.session_state.goals[goal_id]['status'] = '達成'
                            st.session_state.goals[goal_id]['completed_at'] = datetime.now().isoformat()
                            add_experience(50)
                            check_badge("achiever", "🎉 アチーバー", True)
                            st.balloons()
                            st.success(f"🎉 おめでとうございます！目標達成です！")
                        
                        save_all_data()
                        st.rerun()
                
                with col2:
                    if new_progress < 100:
                        if st.button("⏸️ 保留", key=f"pause_{goal_id}"):
                            st.session_state.goals[goal_id]['status'] = '保留'
                            save_all_data()
                            st.rerun()
                
                with col3:
                    if st.button("🗑️ 削除", key=f"delete_{goal_id}"):
                        del st.session_state.goals[goal_id]
                        save_all_data()
                        st.rerun()

# ========== 今日の振り返り ==========
elif page == "📝 今日の振り返り":
    st.title("📝 今日の振り返り")
    
    today = date.today().isoformat()
    
    st.markdown("""
    毎日の振り返りで、自分の成長を実感しましょう！
    小さな一歩も立派な進歩です 🌟
    """)
    
    with st.form("daily_reflection"):
        st.subheader("今日の質問")
        
        mood = st.select_slider(
            "😊 今日の気分は？",
            options=["😢 最悪", "😕 良くない", "😐 普通", "🙂 良い", "😄 最高！"],
            value="😐 普通"
        )
        
        accomplishments = st.text_area(
            "🎉 今日できたこと・達成したこと",
            placeholder="どんな小さなことでもOK！"
        )
        
        learnings = st.text_area(
            "💡 今日学んだこと・気づき",
            placeholder="新しい発見はありましたか？"
        )
        
        gratitude = st.text_area(
            "🙏 今日感謝したいこと",
            placeholder="感謝の気持ちを書き出してみましょう"
        )
        
        tomorrow_plan = st.text_area(
            "🚀 明日やりたいこと",
            placeholder="明日の自分に向けたメッセージ"
        )
        
        energy_level = st.slider("⚡ エネルギーレベル", 1, 10, 5)
        
        submitted = st.form_submit_button("📝 振り返りを保存", use_container_width=True)
        
        if submitted:
            if today not in st.session_state.daily_log:
                st.session_state.daily_log[today] = []
            
            st.session_state.daily_log[today].append({
                "timestamp": datetime.now().isoformat(),
                "mood": mood,
                "accomplishments": accomplishments,
                "learnings": learnings,
                "gratitude": gratitude,
                "tomorrow_plan": tomorrow_plan,
                "energy_level": energy_level
            })
            
            # 連続日数更新
            yesterday = (date.today() - timedelta(days=1)).isoformat()
            if yesterday in st.session_state.daily_log:
                st.session_state.user_profile['streak_days'] += 1
            else:
                st.session_state.user_profile['streak_days'] = 1
            
            # 経験値とバッジ
            add_experience(20)
            check_badge("first_reflection", "📝 振り返りビギナー", True)
            check_badge("streak_7", "🔥 7日連続", st.session_state.user_profile['streak_days'] >= 7)
            check_badge("streak_30", "🔥🔥 30日連続", st.session_state.user_profile['streak_days'] >= 30)
            
            save_all_data()
            st.success("✨ 振り返りを保存しました！素晴らしい習慣です！")
            st.balloons()
    
    # 過去の振り返り
    st.markdown("---")
    st.subheader("📚 過去の振り返り")
    
    if not st.session_state.daily_log:
        st.info("まだ振り返りが記録されていません。今日から始めましょう！")
    else:
        # 日付順にソート
        sorted_logs = sorted(st.session_state.daily_log.keys(), reverse=True)
        
        for log_date in sorted_logs[:7]:  # 直近7日分
            logs = st.session_state.daily_log[log_date]
            with st.expander(f"📅 {log_date}", expanded=False):
                for log in logs:
                    st.write(f"**気分:** {log.get('mood', 'N/A')}")
                    st.write(f"**達成:** {log.get('accomplishments', 'N/A')}")
                    st.write(f"**学び:** {log.get('learnings', 'N/A')}")
                    st.write(f"**感謝:** {log.get('gratitude', 'N/A')}")

# ========== 達成バッジ ==========
elif page == "🏆 達成バッジ":
    st.title("🏆 あなたの達成バッジコレクション")
    
    st.markdown("""
    バッジは、あなたの努力と成長の証です！
    どんどんチャレンジして、コレクションを増やしましょう 🌟
    """)
    
    # バッジ定義
    all_badges = {
        "first_goal": {"name": "🎯 はじめの一歩", "desc": "最初の目標を設定した"},
        "goal_master": {"name": "🏅 目標マスター", "desc": "5つ以上の目標を設定した"},
        "achiever": {"name": "🎉 アチーバー", "desc": "目標を達成した"},
        "first_reflection": {"name": "📝 振り返りビギナー", "desc": "初めて振り返りを記録した"},
        "streak_7": {"name": "🔥 7日連続", "desc": "7日間連続で振り返りを記録した"},
        "streak_30": {"name": "🔥🔥 30日連続", "desc": "30日間連続で振り返りを記録した"},
    }
    
    unlocked_badges = st.session_state.user_profile['badges']
    
    st.subheader(f"🎁 獲得済み: {len(unlocked_badges)}/{len(all_badges)}")
    
    # 獲得済みバッジ
    if unlocked_badges:
        cols = st.columns(3)
        for idx, badge_id in enumerate(unlocked_badges):
            badge = all_badges.get(badge_id, {})
            with cols[idx % 3]:
                st.markdown(f'<div class="badge-icon">{badge.get("name", "🏆")}</div>', unsafe_allow_html=True)
                st.caption(badge.get("desc", ""))
    else:
        st.info("まだバッジを獲得していません。目標を設定して、活動を始めましょう！")
    
    st.markdown("---")
    st.subheader("🔒 未獲得バッジ")
    
    locked_badges = [bid for bid in all_badges.keys() if bid not in unlocked_badges]
    
    if locked_badges:
        cols = st.columns(3)
        for idx, badge_id in enumerate(locked_badges):
            badge = all_badges[badge_id]
            with cols[idx % 3]:
                st.markdown(f'<div class="badge-icon">🔒</div>', unsafe_allow_html=True)
                st.caption(f"**{badge['name']}**")
                st.caption(badge['desc'])
    else:
        st.success("🎉 すべてのバッジを獲得しました！おめでとうございます！")

# ========== 設定 ==========
elif page == "⚙️ 設定":
    st.title("⚙️ 設定")
    
    st.subheader("👤 プロフィール設定")
    
    with st.form("profile_settings"):
        new_name = st.text_input("名前", value=st.session_state.user_profile['name'])
        
        submitted = st.form_submit_button("💾 保存")
        
        if submitted:
            st.session_state.user_profile['name'] = new_name
            save_all_data()
            st.success("✅ プロフィールを更新しました！")
    
    st.markdown("---")
    st.subheader("📊 統計情報")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("登録日", st.session_state.user_profile.get('created_at', 'N/A')[:10])
        st.metric("総目標数", len(st.session_state.goals))
        st.metric("振り返り日数", len(st.session_state.daily_log))
    
    with col2:
        completed_goals = sum(1 for g in st.session_state.goals.values() if g.get('status') == '達成')
        st.metric("達成した目標", completed_goals)
        st.metric("現在のレベル", st.session_state.user_profile['level'])
        st.metric("総獲得ポイント", st.session_state.user_profile['total_points'])
    
    st.markdown("---")
    st.subheader("🗑️ データ管理")
    
    if st.button("🔄 すべてのデータをリセット", type="secondary"):
        if st.checkbox("本当にリセットしますか？（この操作は取り消せません）"):
            st.session_state.clear()
            for file in [USER_FILE, GOALS_FILE, ACHIEVEMENTS_FILE, DAILY_LOG_FILE]:
                if file.exists():
                    file.unlink()
            st.success("データをリセットしました。ページを再読み込みしてください。")

# フッター
st.sidebar.markdown("---")
st.sidebar.markdown("### 💫 今日も素敵な一日を！")
