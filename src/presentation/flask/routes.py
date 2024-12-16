from functools import partial, update_wrapper
from typing import Any, Callable

from flask import Blueprint
from injector import Injector

from src.presentation.flask.controller.error_controller import error
from src.presentation.flask.controller.history_controller import history
from src.presentation.flask.controller.register_controller import (
    register_get,
    register_post,
)


def wrap_partial(func: Callable, *args: Any, **kwargs: Any) -> partial:
    """元の関数の情報を保持したまま、引数を固定した関数を返す

    Args:
        func (Callable): 元の関数
        *args (Any): 固定する引数
        **kwargs (Any): 固定する引数

    Returns:
        partial: 引数が固定された関数
    """
    partial_func = partial(func, *args, **kwargs)
    update_wrapper(partial_func, func)
    return partial_func


def get_router(injector: Injector) -> Blueprint:
    router = Blueprint("router", __name__)

    # 複数のルートを指定する場合は、以下のように記述する
    router.route("/", methods=["GET"])(
        router.route("/home", methods=["GET"])(wrap_partial(history, injector))
    )
    router.route("/register", methods=["GET"])(wrap_partial(register_get, injector))
    router.route("/register", methods=["POST"])(wrap_partial(register_post, injector))
    router.route("/error", methods=["GET"])(wrap_partial(error, injector))
    return router
