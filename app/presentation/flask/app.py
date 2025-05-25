from flask import Flask

from app.presentation.flask.routes import get_router
from app.settings import CONTAINER_PORT
from app.shared.injector_factory import get_shared_injector

app = Flask(__name__)
app.secret_key = "your-secret-key-here"  # セッション用のシークレットキー
injector = get_shared_injector()
app.register_blueprint(get_router(injector))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=CONTAINER_PORT)  # nosec  # noqa: S104,S201
