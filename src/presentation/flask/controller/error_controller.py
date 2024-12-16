from flask import render_template
from injector import Injector

from src.usecase.error import ErrorUsecase


def error(injector: Injector) -> str:
    error_usecase = injector.get(ErrorUsecase)
    result = error_usecase.execute()
    return render_template("error.html", message=result)
