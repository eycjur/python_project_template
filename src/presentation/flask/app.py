from werkzeug import Response

from flask import Flask, redirect, render_template, request
from src.domain.message.message import Message
from src.init import get_message_repository
from src.settings import CONTAINER_PORT
from src.usecase.error import ErrorUsecase
from src.usecase.history import HistoryUsecase
from src.usecase.register import RegisterUsecase

app = Flask(__name__)


@app.route("/")
def history() -> str:
    message_repository = get_message_repository()
    messages = HistoryUsecase(message_repository).execute()
    return render_template("history.html", messages=messages)


@app.route("/register", methods=["GET"])
def register() -> str:
    return render_template("register.html")


@app.route("/register", methods=["POST"])
def submit() -> Response:
    user_input = request.form["user_input"]
    message_repository = get_message_repository()
    usecase = RegisterUsecase(message_repository)
    usecase.execute(Message(user_input))
    return redirect("/")


@app.route("/error")
def error() -> str:
    result = ErrorUsecase().execute()
    return render_template("error.html", message=result)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=CONTAINER_PORT)
