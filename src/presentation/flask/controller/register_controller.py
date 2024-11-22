from flask import redirect, render_template, request
from werkzeug import Response

from src.di import injector
from src.domain.message.message import Message
from src.usecase.register import RegisterUsecase


def register_get() -> str:
    return render_template("register.html")


def register_post() -> Response:
    user_input = request.form["user_input"]

    register_usecase = injector.get(RegisterUsecase)
    register_usecase.execute(Message(user_input))
    return redirect("home")
