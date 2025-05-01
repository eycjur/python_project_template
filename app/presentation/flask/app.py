from flask import Flask
from injector import Injector

from app.di import get_di_module
from app.presentation.flask.routes import get_router
from app.settings import CONTAINER_PORT

injector = Injector(get_di_module())
app = Flask(__name__)
app.register_blueprint(get_router(injector))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=CONTAINER_PORT)  # nosec  # noqa: S104,S201
