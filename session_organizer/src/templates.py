"""
Markdown テンプレート生成モジュール
"""
from typing import List


def get_client_report_template(
    session_date: str,
    coach_name: str,
    client_name: str,
    insights: List[str],
    actions: List[str],
    questions: List[str]
) -> str:
    """
    クライアント向けレポートの Markdown を生成
    
    Args:
        session_date: セッション日付 (例: 2025-12-28)
        coach_name: コーチ名
        client_name: クライアント名
        insights: 気づきのリスト
        actions: 次回までの行動リスト
        questions: 次に考えたい問いのリスト
    
    Returns:
        Markdown 形式のレポート
    """
    insights_md = "\n".join(f"- {insight}" for insight in insights) if insights else "- （記録なし）"
    actions_md = "\n".join(f"- {action}" for action in actions) if actions else "- （設定なし）"
    questions_md = "\n".join(f"- {q}" for q in questions) if questions else "- （なし）"
    
    return f"""# セッションレポート

## セッション概要
- 日付：{session_date}
- コーチ：{coach_name}
- クライアント：{client_name}

## 今回の気づき

{insights_md}

## 次回までの行動

{actions_md}

## 次に考えたい問い

{questions_md}
"""


def get_coach_note_template(
    session_date: str,
    client_name: str,
    observations: List[str],
    interventions: List[str],
    hypotheses: List[str]
) -> str:
    """
    コーチ用メモの Markdown を生成
    
    Args:
        session_date: セッション日付
        client_name: クライアント名
        observations: 観察された変化のリスト
        interventions: 介入ポイントのリスト
        hypotheses: 次回セッション仮説のリスト
    
    Returns:
        Markdown 形式のコーチ用メモ
    """
    observations_md = "\n".join(f"- {obs}" for obs in observations) if observations else "- （なし）"
    interventions_md = "\n".join(f"- {intervention}" for intervention in interventions) if interventions else "- （なし）"
    hypotheses_md = "\n".join(f"- {hyp}" for hyp in hypotheses) if hypotheses else "- （なし）"
    
    return f"""# コーチ用メモ

**クライアント：** {client_name}  
**日付：** {session_date}

## 観察された変化

{observations_md}

## 介入ポイント

{interventions_md}

## 次回セッション仮説

{hypotheses_md}
"""
