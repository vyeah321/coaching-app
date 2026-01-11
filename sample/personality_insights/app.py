"""
パーソナリティインサイト診断アプリ 🎯

あなたの強み、コミュニケーションスタイル、リーダーシップタイプを発見する診断アプリ
"""

import streamlit as st
from datetime import datetime
import json
from pathlib import Path
from typing import Dict, List
import math

# データディレクトリの設定
DATA_DIR = Path("results")
DATA_DIR.mkdir(exist_ok=True)
RESULTS_FILE = DATA_DIR / "diagnosis_results.json"


def load_results() -> Dict:
    """過去の診断結果を読み込む"""
    if RESULTS_FILE.exists():
        with open(RESULTS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"history": []}


def save_result(result: Dict):
    """診断結果を保存"""
    data = load_results()
    data["history"].append(result)
    with open(RESULTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# 診断質問データ
QUESTIONS = {
    "strengths": {
        "title": "💪 あなたの強み診断",
        "description": "あなたの持っている才能と強みを発見しましょう",
        "categories": ["分析力", "創造力", "共感力", "実行力", "リーダーシップ"],
        "questions": [
            {"q": "複雑な問題を論理的に分解して考えることが得意だ", "cat": "分析力"},
            {"q": "データや数字から傾向を見つけるのが好きだ", "cat": "分析力"},
            {"q": "物事の本質や原因を深く考える傾向がある", "cat": "分析力"},
            {"q": "新しいアイデアを思いつくことが多い", "cat": "創造力"},
            {"q": "既存の枠にとらわれない発想ができる", "cat": "創造力"},
            {"q": "芸術やデザインに興味がある", "cat": "創造力"},
            {"q": "相手の気持ちを察することができる", "cat": "共感力"},
            {"q": "人の話を聞くのが得意だ", "cat": "共感力"},
            {"q": "チームの雰囲気を良くすることができる", "cat": "共感力"},
            {"q": "計画を立てて着実に実行できる", "cat": "実行力"},
            {"q": "期限を守ることを大切にしている", "cat": "実行力"},
            {"q": "一度始めたことは最後までやり遂げる", "cat": "実行力"},
            {"q": "グループをまとめる役割を任されることが多い", "cat": "リーダーシップ"},
            {"q": "困難な状況でも前向きに進める", "cat": "リーダーシップ"},
            {"q": "ビジョンを示して人を動かせる", "cat": "リーダーシップ"},
        ]
    },
    "communication": {
        "title": "💬 コミュニケーションスタイル診断",
        "description": "あなたのコミュニケーションの特徴を知りましょう",
        "categories": ["論理型", "感情型", "行動型", "観察型"],
        "questions": [
            {"q": "話すときは事実やデータを重視する", "cat": "論理型"},
            {"q": "議論では論理的な一貫性を大切にする", "cat": "論理型"},
            {"q": "問題解決は手順を踏んで進めたい", "cat": "論理型"},
            {"q": "人と話すとき感情表現が豊かだ", "cat": "感情型"},
            {"q": "ストーリーや体験談で話すことが多い", "cat": "感情型"},
            {"q": "相手の感情に配慮して話す", "cat": "感情型"},
            {"q": "話より行動で示すことを好む", "cat": "行動型"},
            {"q": "結論を先に知りたいタイプだ", "cat": "行動型"},
            {"q": "効率を重視して端的に伝える", "cat": "行動型"},
            {"q": "人の話を最後まで聞いてから意見を言う", "cat": "観察型"},
            {"q": "全体を見てから判断したい", "cat": "観察型"},
            {"q": "静かに考えを深めることが多い", "cat": "観察型"},
        ]
    },
    "leadership": {
        "title": "👑 リーダーシップスタイル診断",
        "description": "あなたのリーダーシップの型を発見しましょう",
        "categories": ["ビジョン型", "コーチ型", "民主型", "ペースセッター型"],
        "questions": [
            {"q": "大きな目標を掲げて人を鼓舞する", "cat": "ビジョン型"},
            {"q": "将来の可能性を示すことが得意だ", "cat": "ビジョン型"},
            {"q": "チームに方向性を示すことを重視する", "cat": "ビジョン型"},
            {"q": "メンバーの成長を第一に考える", "cat": "コーチ型"},
            {"q": "対話を通じて相手を理解しようとする", "cat": "コーチ型"},
            {"q": "長期的な育成に力を入れる", "cat": "コーチ型"},
            {"q": "メンバーの意見を取り入れて決める", "cat": "民主型"},
            {"q": "合意形成を大切にする", "cat": "民主型"},
            {"q": "チームワークを何より重視する", "cat": "民主型"},
            {"q": "自ら高い基準を示して引っ張る", "cat": "ペースセッター型"},
            {"q": "スピードと成果を重視する", "cat": "ペースセッター型"},
            {"q": "自分が先頭に立って動くことが多い", "cat": "ペースセッター型"},
        ]
    }
}

# アドバイスデータ
ADVICE = {
    "strengths": {
        "分析力": {
            "strength": "論理的思考と問題解決能力が高く、複雑な状況を整理できます",
            "tips": "データ分析やコンサルティング、研究職などで力を発揮できます。感情面にも目を向けるとさらにバランスが取れます。"
        },
        "創造力": {
            "strength": "新しいアイデアを生み出し、革新的な解決策を提案できます",
            "tips": "企画やデザイン、マーケティングなどで活躍できます。アイデアを形にする実行力も磨きましょう。"
        },
        "共感力": {
            "strength": "人の気持ちを理解し、良好な関係を築くことができます",
            "tips": "カウンセリング、HR、営業などで強みを活かせます。自分の感情も大切にしましょう。"
        },
        "実行力": {
            "strength": "計画を着実に実行し、確実に成果を出すことができます",
            "tips": "プロジェクト管理や運用業務で力を発揮します。柔軟性も意識するとより良くなります。"
        },
        "リーダーシップ": {
            "strength": "人をまとめ、チームを目標達成に導くことができます",
            "tips": "マネジメントや起業で活躍できます。メンバーの声を聞く姿勢も大切にしましょう。"
        }
    },
    "communication": {
        "論理型": {
            "strength": "明確で論理的なコミュニケーションができます",
            "tips": "事実を重視する場面で強みを発揮。相手の感情にも配慮するとさらに効果的です。"
        },
        "感情型": {
            "strength": "相手の心に響く、温かいコミュニケーションができます",
            "tips": "人間関係構築が得意。重要な判断では論理も加えるとバランスが取れます。"
        },
        "行動型": {
            "strength": "効率的で結果重視のコミュニケーションができます",
            "tips": "スピードが求められる場面で活躍。時には丁寧な説明も心がけましょう。"
        },
        "観察型": {
            "strength": "全体を見て慎重に判断するコミュニケーションができます",
            "tips": "深い洞察力があります。時には積極的に発信することも試してみましょう。"
        }
    },
    "leadership": {
        "ビジョン型": {
            "strength": "大きな目標を示して人を動かすリーダーシップ",
            "tips": "変革期や新規事業で力を発揮。具体的な実行計画も示すとさらに効果的です。"
        },
        "コーチ型": {
            "strength": "人を育てながら成果を出すリーダーシップ",
            "tips": "長期的な組織作りで活躍。緊急時は迅速な判断も必要です。"
        },
        "民主型": {
            "strength": "合意を形成し、チームの力を引き出すリーダーシップ",
            "tips": "チームの結束を高めます。時には決断力も必要です。"
        },
        "ペースセッター型": {
            "strength": "自ら率先して高い成果を出すリーダーシップ",
            "tips": "短期目標達成に有効。メンバーの育成にも目を向けましょう。"
        }
    }
}


def calculate_scores(answers: List[int], diagnosis_type: str) -> Dict:
    """スコアを計算"""
    questions = QUESTIONS[diagnosis_type]["questions"]
    categories = QUESTIONS[diagnosis_type]["categories"]
    
    scores = {cat: 0 for cat in categories}
    counts = {cat: 0 for cat in categories}
    
    for i, answer in enumerate(answers):
        cat = questions[i]["cat"]
        scores[cat] += answer
        counts[cat] += 1
    
    # 平均スコアを計算（1-5の範囲）
    avg_scores = {cat: scores[cat] / counts[cat] for cat in categories}
    
    # パーセンテージに変換（0-100）
    percentage_scores = {cat: (score - 1) / 4 * 100 for cat, score in avg_scores.items()}
    
    return percentage_scores


def create_radar_chart_svg(scores: Dict, size: int = 300) -> str:
    """レーダーチャートのSVGを生成"""
    categories = list(scores.keys())
    values = list(scores.values())
    n = len(categories)
    
    center_x = size / 2
    center_y = size / 2
    radius = size / 2 - 40
    
    # 背景の円を描画
    circles_svg = ""
    for i in range(5, 0, -1):
        r = radius * i / 5
        circles_svg += f'<circle cx="{center_x}" cy="{center_y}" r="{r}" fill="none" stroke="#e0e0e0" stroke-width="1"/>'
    
    # 軸を描画
    lines_svg = ""
    labels_svg = ""
    for i in range(n):
        angle = 2 * math.pi * i / n - math.pi / 2
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        
        lines_svg += f'<line x1="{center_x}" y1="{center_y}" x2="{x}" y2="{y}" stroke="#cccccc" stroke-width="1"/>'
        
        # ラベル位置
        label_radius = radius + 25
        label_x = center_x + label_radius * math.cos(angle)
        label_y = center_y + label_radius * math.sin(angle)
        labels_svg += f'<text x="{label_x}" y="{label_y}" text-anchor="middle" dominant-baseline="middle" font-size="12" fill="#333">{categories[i]}</text>'
    
    # データポリゴンを描画
    points = []
    for i in range(n):
        angle = 2 * math.pi * i / n - math.pi / 2
        value = values[i] / 100  # 0-1の範囲に正規化
        x = center_x + radius * value * math.cos(angle)
        y = center_y + radius * value * math.sin(angle)
        points.append(f"{x},{y}")
    
    polygon_svg = f'<polygon points="{" ".join(points)}" fill="rgba(102, 126, 234, 0.5)" stroke="rgb(102, 126, 234)" stroke-width="2"/>'
    
    # ポイントを描画
    dots_svg = ""
    for i in range(n):
        angle = 2 * math.pi * i / n - math.pi / 2
        value = values[i] / 100
        x = center_x + radius * value * math.cos(angle)
        y = center_y + radius * value * math.sin(angle)
        dots_svg += f'<circle cx="{x}" cy="{y}" r="4" fill="rgb(102, 126, 234)"/>'
    
    svg = f'''
    <svg width="{size}" height="{size}" xmlns="http://www.w3.org/2000/svg">
        {circles_svg}
        {lines_svg}
        {polygon_svg}
        {dots_svg}
        {labels_svg}
    </svg>
    '''
    
    return svg


# ページ設定
st.set_page_config(
    page_title="パーソナリティインサイト診断",
    page_icon="🎯",
    layout="wide"
)

# カスタムCSS
st.markdown("""
<style>
    .diagnosis-card {
        padding: 20px;
        border-radius: 10px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin: 20px 0;
        text-align: center;
    }
    .result-box {
        padding: 20px;
        border-radius: 10px;
        background: #f8f9fa;
        margin: 10px 0;
        border-left: 4px solid #667eea;
    }
    .score-high {
        color: #28a745;
        font-weight: bold;
    }
    .score-medium {
        color: #ffc107;
        font-weight: bold;
    }
    .score-low {
        color: #6c757d;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# セッション状態の初期化
if 'current_diagnosis' not in st.session_state:
    st.session_state.current_diagnosis = None
if 'answers' not in st.session_state:
    st.session_state.answers = []
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0

# メインページ
st.title("🎯 パーソナリティインサイト診断")
st.markdown("**あなたの強み、コミュニケーションスタイル、リーダーシップタイプを発見しましょう**")

# サイドバー
st.sidebar.title("📋 メニュー")
page = st.sidebar.radio("", ["診断を受ける", "診断履歴"])

if page == "診断を受ける":
    
    if st.session_state.current_diagnosis is None:
        # 診断選択画面
        st.markdown('<div class="diagnosis-card"><h2>どの診断を受けますか？</h2></div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### 💪 強み診断")
            st.write("あなたの5つの強みを発見")
            st.write("**診断時間**: 約3分")
            if st.button("この診断を受ける", key="strengths"):
                st.session_state.current_diagnosis = "strengths"
                st.session_state.answers = []
                st.session_state.current_question = 0
                st.rerun()
        
        with col2:
            st.markdown("### 💬 コミュニケーションスタイル")
            st.write("あなたの対話の特徴を分析")
            st.write("**診断時間**: 約2分")
            if st.button("この診断を受ける", key="communication"):
                st.session_state.current_diagnosis = "communication"
                st.session_state.answers = []
                st.session_state.current_question = 0
                st.rerun()
        
        with col3:
            st.markdown("### 👑 リーダーシップスタイル")
            st.write("あなたのリーダー型を判定")
            st.write("**診断時間**: 約2分")
            if st.button("この診断を受ける", key="leadership"):
                st.session_state.current_diagnosis = "leadership"
                st.session_state.answers = []
                st.session_state.current_question = 0
                st.rerun()
    
    else:
        # 診断実施中
        diagnosis_type = st.session_state.current_diagnosis
        diagnosis_data = QUESTIONS[diagnosis_type]
        questions = diagnosis_data["questions"]
        
        if st.session_state.current_question < len(questions):
            # 質問表示
            st.markdown(f"### {diagnosis_data['title']}")
            st.progress((st.session_state.current_question + 1) / len(questions))
            st.caption(f"質問 {st.session_state.current_question + 1} / {len(questions)}")
            
            question = questions[st.session_state.current_question]
            
            st.markdown(f"#### {question['q']}")
            
            col1, col2, col3, col4, col5 = st.columns(5)
            
            answer = None
            with col1:
                if st.button("1\n全く\nそう思わない", use_container_width=True):
                    answer = 1
            with col2:
                if st.button("2\nあまり\nそう思わない", use_container_width=True):
                    answer = 2
            with col3:
                if st.button("3\nどちらとも\n言えない", use_container_width=True):
                    answer = 3
            with col4:
                if st.button("4\nやや\nそう思う", use_container_width=True):
                    answer = 4
            with col5:
                if st.button("5\n非常に\nそう思う", use_container_width=True):
                    answer = 5
            
            if answer is not None:
                st.session_state.answers.append(answer)
                st.session_state.current_question += 1
                st.rerun()
            
            # 戻るボタン
            if st.session_state.current_question > 0:
                if st.button("← 前の質問に戻る"):
                    st.session_state.current_question -= 1
                    st.session_state.answers.pop()
                    st.rerun()
        
        else:
            # 結果表示
            scores = calculate_scores(st.session_state.answers, diagnosis_type)
            
            st.markdown(f"### {diagnosis_data['title']} - 結果")
            st.success("診断が完了しました！")
            
            # レーダーチャート表示
            st.markdown("#### 📊 あなたのスコア")
            chart_svg = create_radar_chart_svg(scores, 400)
            st.markdown(chart_svg, unsafe_allow_html=True)
            
            # スコア詳細
            st.markdown("#### 📈 詳細スコア")
            
            sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
            
            for category, score in sorted_scores:
                color_class = "score-high" if score >= 70 else "score-medium" if score >= 50 else "score-low"
                
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**{category}**")
                with col2:
                    st.markdown(f'<span class="{color_class}">{score:.0f}点</span>', unsafe_allow_html=True)
                
                st.progress(score / 100)
                
                # アドバイス表示
                if score == sorted_scores[0][1]:  # 最高スコア
                    advice_data = ADVICE[diagnosis_type][category]
                    st.markdown(f'<div class="result-box">', unsafe_allow_html=True)
                    st.markdown(f"**✨ あなたの最大の強み**")
                    st.markdown(f"{advice_data['strength']}")
                    st.markdown(f"**💡 活かし方**")
                    st.markdown(f"{advice_data['tips']}")
                    st.markdown('</div>', unsafe_allow_html=True)
            
            # 結果を保存
            result = {
                "timestamp": datetime.now().isoformat(),
                "diagnosis_type": diagnosis_type,
                "scores": scores,
                "top_category": sorted_scores[0][0]
            }
            save_result(result)
            
            st.markdown("---")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🏠 診断選択に戻る", use_container_width=True):
                    st.session_state.current_diagnosis = None
                    st.session_state.answers = []
                    st.session_state.current_question = 0
                    st.rerun()
            
            with col2:
                if st.button("📋 診断履歴を見る", use_container_width=True):
                    st.session_state.current_diagnosis = None
                    st.rerun()

elif page == "診断履歴":
    st.header("📋 診断履歴")
    
    results_data = load_results()
    
    if not results_data["history"]:
        st.info("まだ診断を受けていません。診断を受けてみましょう！")
    else:
        st.write(f"**診断回数:** {len(results_data['history'])}回")
        
        for i, result in enumerate(reversed(results_data["history"])):
            diagnosis_name = QUESTIONS[result["diagnosis_type"]]["title"]
            timestamp = result["timestamp"][:10]
            top_category = result["top_category"]
            
            with st.expander(f"{i+1}. {diagnosis_name} - {timestamp}", expanded=False):
                st.write(f"**最高スコア:** {top_category}")
                
                for category, score in result["scores"].items():
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(f"**{category}**")
                    with col2:
                        st.write(f"{score:.0f}点")
                    st.progress(score / 100)

# フッター
st.sidebar.markdown("---")
st.sidebar.info("💡 診断結果は自己理解のヒントです。コーチとのセッションでさらに深めましょう！")
