from datetime import datetime

from src.settings import JST


def current_time_iso() -> str:
    return datetime.now(JST).isoformat()
