from flask import render_template

from src.di import injector
from src.usecase.error import ErrorUsecase


def error() -> str:
    error_usecase = injector.get(ErrorUsecase)
    result = error_usecase.execute()
    return render_template("error.html", message=result)
