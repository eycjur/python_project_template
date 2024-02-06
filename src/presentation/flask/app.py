from flask import Flask, render_template, request
from src.const import APP_PORT
from src.usecase.sample import func

app = Flask(__name__)


@app.route("/")
def home() -> str:
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def submit() -> str:
    user_input = request.form["user_input"]
    result = func(user_input)
    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=APP_PORT)
