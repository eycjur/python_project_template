from datetime import datetime

from app.settings import JST


def current_time_iso() -> str:
    """現在時刻をISO8601形式で返す

    Returns:
        str: 現在時刻のISO8601形式
    """
    return datetime.now(JST).isoformat()
