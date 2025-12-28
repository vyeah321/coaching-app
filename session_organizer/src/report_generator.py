"""
レポート生成モジュール
セッションメモから2つのレポートを生成する
"""
from typing import Tuple, List
from .templates import get_client_report_template, get_coach_note_template


def parse_session_memo(session_memo: str) -> dict:
    """
    セッションメモを解析して構造化データに変換（MVP版：シンプルな実装）
    
    Args:
        session_memo: セッションメモ（箇条書き想定）
    
    Returns:
        解析されたデータ（気づき、行動、問い、観察、介入、仮説）
    """
    lines = [line.strip() for line in session_memo.split('\n') if line.strip()]
    
    # MVP版：すべてのメモを「気づき」として扱う
    # 後で改善：セクション分け、キーワード検出など
    insights = []
    actions = []
    questions = []
    observations = []
    interventions = []
    hypotheses = []
    
    current_section = "insights"  # デフォルト
    
    for line in lines:
        line_lower = line.lower()
        
        # セクション判定（簡易版）
        if any(keyword in line_lower for keyword in ['気づき', 'きづき', '発見', '気付', '気がつ']):
            current_section = "insights"
            continue
        elif any(keyword in line_lower for keyword in ['行動', 'アクション', 'やる', 'する', '実行']):
            current_section = "actions"
            continue
        elif any(keyword in line_lower for keyword in ['問い', '問', '質問', '考えたい']):
            current_section = "questions"
            continue
        elif any(keyword in line_lower for keyword in ['観察', 'かんさつ', '変化', 'へんか']):
            current_section = "observations"
            continue
        elif any(keyword in line_lower for keyword in ['介入', '働きかけ', 'はたらきかけ']):
            current_section = "interventions"
            continue
        elif any(keyword in line_lower for keyword in ['仮説', '次回', 'じかい']):
            current_section = "hypotheses"
            continue
        
        # 行頭記号を除去
        clean_line = line.lstrip('- •*#').strip()
        if not clean_line:
            continue
        
        # セクションに追加
        if current_section == "insights":
            insights.append(clean_line)
        elif current_section == "actions":
            actions.append(clean_line)
        elif current_section == "questions":
            questions.append(clean_line)
        elif current_section == "observations":
            observations.append(clean_line)
        elif current_section == "interventions":
            interventions.append(clean_line)
        elif current_section == "hypotheses":
            hypotheses.append(clean_line)
    
    # デフォルト値設定（空の場合）
    if not insights and not actions and not questions:
        # すべて空の場合、メモ全体を気づきとして扱う
        insights = lines[:3] if len(lines) >= 3 else lines
    
    # コーチ用メモは insights から自動生成（MVP版）
    if not observations:
        observations = insights[:2] if len(insights) >= 2 else insights
    if not interventions:
        interventions = ["クライアントの気づきを深める質問"]
    if not hypotheses:
        hypotheses = ["次回セッションでさらに掘り下げる"]
    
    return {
        "insights": insights,
        "actions": actions,
        "questions": questions,
        "observations": observations,
        "interventions": interventions,
        "hypotheses": hypotheses
    }


def generate_reports(
    session_memo: str,
    session_date: str,
    client_name: str,
    coach_name: str
) -> Tuple[str, str]:
    """
    セッションメモから2つのレポートを生成
    
    Args:
        session_memo: セッションメモ
        session_date: セッション日付
        client_name: クライアント名
        coach_name: コーチ名
    
    Returns:
        (client_report, coach_note) のタプル
    """
    # メモを解析
    parsed_data = parse_session_memo(session_memo)
    
    # クライアント向けレポート生成
    client_report = get_client_report_template(
        session_date=session_date,
        coach_name=coach_name,
        client_name=client_name,
        insights=parsed_data["insights"],
        actions=parsed_data["actions"],
        questions=parsed_data["questions"]
    )
    
    # コーチ向けメモ生成
    coach_note = get_coach_note_template(
        session_date=session_date,
        client_name=client_name,
        observations=parsed_data["observations"],
        interventions=parsed_data["interventions"],
        hypotheses=parsed_data["hypotheses"]
    )
    
    return client_report, coach_note
