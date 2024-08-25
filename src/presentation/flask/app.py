from flask import Flask
from src.presentation.flask.routes import router
from src.settings import CONTAINER_PORT

app = Flask(__name__)
app.register_blueprint(router)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=CONTAINER_PORT)
