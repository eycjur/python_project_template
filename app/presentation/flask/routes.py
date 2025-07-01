from flask import Blueprint, redirect, render_template, request
from injector import Injector
from werkzeug import Response

from app.di import get_injector
from app.domain.message.message import Message
from app.usecase.error import ErrorUsecase
from app.usecase.history import HistoryUsecase
from app.usecase.register import RegisterUsecase

router = Blueprint("app", __name__)

injector = get_injector()


@router.route("/", methods=["GET"])
@router.route("/home", methods=["GET"])
def history(injector: Injector = injector) -> str:
    history_usecase = injector.get(HistoryUsecase)
    messages = history_usecase.execute()
    return render_template("history.html", messages=messages)


@router.route("/register", methods=["GET"])
def register_get(injector: Injector = injector) -> str:
    return render_template("register.html")


@router.route("/register", methods=["POST"])
def register_post(injector: Injector = injector) -> Response:
    user_input = request.form["user_input"]

    register_usecase = injector.get(RegisterUsecase)
    register_usecase.execute(Message(user_input))
    return redirect("home")


@router.route("/error", methods=["GET"])
def error(injector: Injector = injector) -> str:
    error_usecase = injector.get(ErrorUsecase)
    result = error_usecase.execute()
    return render_template("error.html", message=result)
