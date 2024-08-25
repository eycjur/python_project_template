from flask import render_template

from src.di import injector
from src.usecase.history import HistoryUsecase


def history() -> str:
    history_usecase = injector.get(HistoryUsecase)
    messages = history_usecase.execute()
    return render_template("history.html", messages=messages)
