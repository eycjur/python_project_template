from flask import Blueprint

from src.presentation.flask.controller.error_controller import error
from src.presentation.flask.controller.history_controller import history
from src.presentation.flask.controller.register_controller import (
    register_get,
    register_post,
)

router = Blueprint("router", __name__)

router.route("/", methods=["GET"])(history)
router.route("/home", methods=["GET"])(history)
router.route("/register", methods=["GET"])(register_get)
router.route("/register", methods=["POST"])(register_post)
router.route("/error", methods=["GET"])(error)
