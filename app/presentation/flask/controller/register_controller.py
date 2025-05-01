from flask import redirect, render_template, request
from injector import Injector
from werkzeug import Response

from app.domain.message.message import Message
from app.usecase.register import RegisterUsecase


def register_get(injector: Injector) -> str:
    return render_template("register.html")


def register_post(injector: Injector) -> Response:
    user_input = request.form["user_input"]

    register_usecase = injector.get(RegisterUsecase)
    register_usecase.execute(Message(user_input))
    return redirect("home")
