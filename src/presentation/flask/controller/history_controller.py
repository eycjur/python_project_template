from flask import render_template
from injector import Injector

from src.usecase.history import HistoryUsecase


def history(injector: Injector) -> str:
    history_usecase = injector.get(HistoryUsecase)
    messages = history_usecase.execute()
    return render_template("history.html", messages=messages)
