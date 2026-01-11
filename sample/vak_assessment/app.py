"""
VAK学習スタイル診断アプリ 🎯

Visual（視覚型）、Auditory（聴覚型）、Kinesthetic（体感覚型）の
学習スタイルを診断するアプリ
"""

import streamlit as st
from datetime import datetime
import json
from pathlib import Path
import plotly.graph_objects as go
from typing import Dict, List

# データディレクトリの設定
DATA_DIR = Path("results")
DATA_DIR.mkdir(exist_ok=True)
RESULTS_FILE = DATA_DIR / "vak_results.json"


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


# VAK診断質問（ビジネス・人間関係スタイル・全12問）
VAK_QUESTIONS = [
    # 順番をシャッフルして、パターンが見えないように配置
    {"id": 1, "type": "A", "question": "会話を通じて相手のことを理解し、信頼関係を築くのが得意だ"},
    {"id": 2, "type": "V", "question": "新しい情報や提案を受けるとき、資料やデータで見せてもらうと理解しやすい"},
    {"id": 3, "type": "K", "question": "実際に体験することで、最も深く理解し記憶に残る"},
    {"id": 4, "type": "V", "question": "人と会ったとき、相手の表情や雰囲気から多くの情報を読み取る"},
    {"id": 5, "type": "A", "question": "人の話を聞いて、その背景や想いを汲み取ることができる"},
    {"id": 6, "type": "K", "question": "直感や雰囲気を大切にして、判断することが多い"},
    {"id": 7, "type": "V", "question": "場所や人の顔を視覚的に覚えるのが得意で、次に会ったときすぐに分かる"},
    {"id": 8, "type": "A", "question": "声のトーンや話し方から、相手の本音や感情を読み取れる"},
    {"id": 9, "type": "K", "question": "理論より実践、まず試してみることで学ぶのが好きだ"},
    {"id": 10, "type": "V", "question": "プレゼンや説明を受けるとき、図やグラフがあると理解が早い"},
    {"id": 11, "type": "A", "question": "ストーリーや事例を聞くことで、物事への興味や理解が深まる"},
    {"id": 12, "type": "K", "question": "人と話すとき、その場の空気感や雰囲気から相手の気持ちを感じ取る"},
]


def create_vak_chart(scores: Dict[str, int]) -> go.Figure:
    """VAKスコアのレーダーチャートを作成"""
    categories = ['Visual<br>視覚型', 'Auditory<br>聴覚型', 'Kinesthetic<br>体感覚型']
    values = [scores['V'], scores['A'], scores['K']]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='あなたのスコア',
        line=dict(color='rgb(99, 110, 250)', width=3),
        fillcolor='rgba(99, 110, 250, 0.3)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 20]
            )
        ),
        showlegend=False,
        height=500,
        title=dict(
            text='あなたのVAK学習スタイル',
            font=dict(size=20)
        )
    )
    
    return fig


def get_dominant_style(scores: Dict[str, int]) -> str:
    """優勢な学習スタイルを判定"""
    max_score = max(scores.values())
    dominant = [k for k, v in scores.items() if v == max_score]
    
    style_names = {
        'V': '見るタイプ（視覚優位）',
        'A': '聞くタイプ（聴覚優位）',
        'K': '体感タイプ（体験重視）'
    }
    
    return '・'.join([style_names[s] for s in dominant])


def get_style_description(style_type: str) -> Dict[str, str]:
    """各学習スタイルの説明を返す"""
    descriptions = {
        'V': {
            'title': '👀 見るタイプ（視覚優位）',
            'description': '目から入る情報が得意で、見て理解するタイプです。',
            'strengths': '- データや資料、図解で理解しやすい\n- 相手の表情やボディランゲージを読み取る\n- 視覚的な記憶が得意\n- 見た目や雰囲気を大切にする',
            'tips': '💼 **ビジネスでの活かし方**\n- プレゼンには視覚資料を効果的に使う\n- 商談では実物やサンプルを見せる\n- ホワイトボードや図解で説明する\n- 身だしなみや会議室の雰囲気づくりを意識\n\n🍷 **ワイン会での活かし方**\n- ワインの色や輝きの違いを楽しむ\n- ラベルや産地の写真に注目\n- テーブルセッティングを楽しむ\n\n🤝 **相手がこのタイプなら**\n- 資料やビジュアルを用意して説明\n- 身振りや表情豊かに話す\n- 清潔感のある身だしなみを心がける'  
        },
        'A': {
            'title': '👂 聞くタイプ（聴覚優位）',
            'description': '耳から入る情報が得意で、会話や説明を通じて理解するタイプです。',
            'strengths': '- 話を聞いて理解するのが得意\n- 会話で信頼関係を築く\n- 声のトーンから感情を読み取る\n- ストーリーや背景に興味を持つ',
            'tips': '💼 **ビジネスでの活かし方**\n- 丁寧な説明と対話を大切に\n- 電話やオンライン会議を効果的に活用\n- グループディスカッションに積極参加\n- 相手の話をよく聞き、質問する\n\n🍷 **ワイン会での活かし方**\n- ソムリエの説明に耳を傾ける\n- ワインの背景やストーリーを楽しむ\n- 参加者との会話を楽しむ\n\n🤝 **相手がこのタイプなら**\n- じっくり話を聞く時間を作る\n- 背景や理由を丁寧に説明\n- ストーリーを交えて伝える'
        },
        'K': {
            'title': '✋ 体感タイプ（体験重視）',
            'description': '体で感じて理解するのが得意で、体験や実践を通じて学ぶタイプです。',
            'strengths': '- 実際に体験することで深く理解\n- 直感や雰囲気を大切にする\n- 実践的なアプローチが好き\n- 身体で感じる感覚に敏感',
            'tips': '💼 **ビジネスでの活かし方**\n- 実践的なワークショップに参加\n- まず試してみる、体験する\n- ロールプレイで理解を深める\n- 現場や実物を見て判断\n\n🍷 **ワイン会での活かし方**\n- 実際に味わいながら学ぶ\n- 香りをじっくり楽しむ\n- 料理とのペアリングを試す\n\n🤝 **相手がこのタイプなら**\n- 実際に体験できる機会を提供\n- デモやサンプルを用意\n- 理論より実践を重視\n- リラックスできる雰囲気づくり'
        }
    }
    return descriptions.get(style_type, {})


def main():
    st.set_page_config(
        page_title="VAK学習スタイル診断",
        page_icon="🎯",
        layout="wide"
    )
    
    st.title("🎯 あなたの強みを活かす！コミュニケーションタイプ診断")
    st.markdown("---")
    
    # セッション状態の初期化
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'answers' not in st.session_state:
        st.session_state.answers = {}
    if 'completed' not in st.session_state:
        st.session_state.completed = False
    
    # サイドバー
    with st.sidebar:
        st.header("📋 診断について")
        st.markdown("""
        ### あなたの強みを知って、人間関係をもっと豊かに
        
        仕事でも、プライベートでも、人との関わり方には個性があります。
        自分のタイプを知ることで、より効果的な人間関係が築けます。
        
        **V** - Visual（視覚型）  
        見た目や資料から情報を得るのが得意
        
        **A** - Auditory（聴覚型）  
        会話や説明を通じて理解するのが得意
        
        **K** - Kinesthetic（体感覚型）  
        体験や実践を通じて理解するのが得意
        
        ### 診断方法
        12の質問に答えて、あなたのタイプを診断します。
        
        ### こんな場面で活用できます
        - **ビジネスの商談や提案**
        - **ワイン会などの交流の場**
        - **チームでのプロジェクト**
        - **部下や後輩の育成**
        """)
    
    # メインコンテンツ
    if not st.session_state.completed:
        # 診断完了チェック
        if st.session_state.current_question >= len(VAK_QUESTIONS):
            st.session_state.completed = True
            st.rerun()
        
        # 診断中
        st.subheader(f"質問 {st.session_state.current_question + 1} / {len(VAK_QUESTIONS)}")
        
        progress = st.session_state.current_question / len(VAK_QUESTIONS)
        st.progress(progress)
        
        current_q = VAK_QUESTIONS[st.session_state.current_question]
        
        st.markdown("---")
        st.markdown(f"### {current_q['question']}")
        st.markdown("")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            if st.button("全く当てはまらない\n1", use_container_width=True, key=f"btn_1_{current_q['id']}"):
                st.session_state.answers[current_q['id']] = {'type': current_q['type'], 'score': 1}
                st.session_state.current_question += 1
                st.rerun()
        
        with col2:
            if st.button("やや当てはまらない\n2", use_container_width=True, key=f"btn_2_{current_q['id']}"):
                st.session_state.answers[current_q['id']] = {'type': current_q['type'], 'score': 2}
                st.session_state.current_question += 1
                st.rerun()
        
        with col3:
            if st.button("どちらとも言えない\n3", use_container_width=True, key=f"btn_3_{current_q['id']}"):
                st.session_state.answers[current_q['id']] = {'type': current_q['type'], 'score': 3}
                st.session_state.current_question += 1
                st.rerun()
        
        with col4:
            if st.button("やや当てはまる\n4", use_container_width=True, key=f"btn_4_{current_q['id']}"):
                st.session_state.answers[current_q['id']] = {'type': current_q['type'], 'score': 4}
                st.session_state.current_question += 1
                st.rerun()
        
        with col5:
            if st.button("とても当てはまる\n5", use_container_width=True, key=f"btn_5_{current_q['id']}"):
                st.session_state.answers[current_q['id']] = {'type': current_q['type'], 'score': 5}
                st.session_state.current_question += 1
                st.rerun()
        
        st.markdown("---")
        
        if st.session_state.current_question > 0:
            if st.button("⬅️ 前の質問に戻る"):
                st.session_state.current_question -= 1
                st.rerun()
    
    else:
        # 結果表示
        st.subheader("🎉 診断完了！")
        
        # スコア計算
        scores = {'V': 0, 'A': 0, 'K': 0}
        for answer in st.session_state.answers.values():
            scores[answer['type']] += answer['score']
        
        # 結果を保存
        result = {
            'timestamp': datetime.now().isoformat(),
            'scores': scores,
            'dominant_style': get_dominant_style(scores)
        }
        save_result(result)
        
        # チャート表示
        st.plotly_chart(create_vak_chart(scores), use_container_width=True)
        
        # スコア表示
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("👀 見るタイプ", f"{scores['V']}/20")
            st.progress(scores['V'] / 20)
        
        with col2:
            st.metric("👂 聞くタイプ", f"{scores['A']}/20")
            st.progress(scores['A'] / 20)
        
        with col3:
            st.metric("✋ 体感タイプ", f"{scores['K']}/20")
            st.progress(scores['K'] / 20)
        
        # 優勢なスタイル
        st.markdown("---")
        st.subheader("🌟 あなたのコミュニケーションタイプ")
        st.success(f"**{get_dominant_style(scores)}**")
        
        # 各スタイルの詳細説明
        st.markdown("---")
        st.subheader("📚 各タイプの詳細")
        
        for style_type in ['V', 'A', 'K']:
            desc = get_style_description(style_type)
            max_score = 20
            
            with st.expander(f"{desc['title']} - スコア: {scores[style_type]}/{max_score}"):
                st.markdown(desc['description'])
                st.markdown("")
                st.markdown("**💪 強み**")
                st.markdown(desc['strengths'])
                st.markdown("")
                st.markdown("**💡 学習のヒント**")
                st.markdown(desc['tips'])
        
        # 総合アドバイス
        st.markdown("---")
        st.subheader("💡 あなたのタイプの活かし方")
        
        max_score = max(scores.values())
        min_score = min(scores.values())
        
        if max_score - min_score < 5:
            st.info("""
            **バランス型：あらゆる場面に対応できる才能**
            
            あなたは状況に応じて柔軟にコミュニケーションスタイルを変えられる才能があります！
            視覚、聴覚、体感覚のすべてをバランスよく使えるため、
            相手のタイプに合わせた効果的なアプローチが可能です。
            
            **この特性を活かせる場面**
            - ビジネスの商談や提案：相手に合わせて柔軟に対応
            - ワイン会などの社交の場：様々なタイプの人と良好な関係を築く
            - チームマネジメント：メンバーの個性に合わせた指導
            
            あなたのこの才能は、人の可能性を引き出すプロフェッショナルに最適です。
            """)
        else:
            dominant_type = max(scores, key=scores.get)
            st.info(f"""
            **{get_style_description(dominant_type)['title']} 優勢型**
            
            あなたは特に{get_style_description(dominant_type)['title']}の特徴が強く表れています。
            この強みを活かしながら、他のタイプも意識することで、
            より幅広い人との効果的なコミュニケーションが可能になります。
            
            **ビジネスシーンでの活用**
            - 自分の強みを活かした提案スタイルの確立
            - 相手のタイプを見極めて、アプローチを調整
            - チームの多様性を理解し、効果的に協働
            
            **人間関係での活用**
            - ワイン会などの社交の場で、相手に合わせた会話
            - 自分のタイプを理解することで、ストレスなく関係構築
            - 他者との違いを楽しみ、より深い理解へ
            """)
        
        # CTA
        st.markdown("---")
        st.markdown("### 💭 こんな経験、ありませんか？")
        st.markdown("""
        今回の診断で、あなた自身のコミュニケーションタイプが分かりました。
        
        でも実際の場面では…
        
        - 部下にもっと自分で考えて動いてほしいのに、つい指示を出してしまう
        - お客様が本当に求めているものを知りたいのに、話を聞き出せない
        - 相手の良いところをもっと引き出してあげたいのに、どうしたらいいか分からない
        
        **もしかしたら、必要なのは「聞く力」なのかもしれません。**
        
        相手の話を聞く。本音を引き出す。可能性を見つける。
        
        そんな「引き出す力」があれば、
        仕事も、人間関係も、きっと変わっていくはずです。
        
        興味がある方は、詳しい情報をチェックしてみてください。
        """)
        st.link_button(
            "もっと詳しく見てみる",
            "https://pro-coach.net/p/r/8uCeXl3l?free20=0030005",
            use_container_width=True
        )


if __name__ == "__main__":
    main()
