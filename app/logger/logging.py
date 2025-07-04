import logging
import os
import sys
from logging.config import dictConfig

import yaml  # type: ignore

from app.settings import LOGGER_CONFIG_FILE


def _is_exc_info() -> bool:
    return sys.exc_info()[0] is not None


class DefaultLogger(object):
    """Logger object.

    ログを出力する際はこれを利用すること

    Example:
        >>> logger = DefaultLogger(__name__)
        >>> logger.debug("debug message")
    """

    def __init__(self, name: str) -> None:
        self.logger = logging.getLogger(name)

    def debug(self, msg: object) -> None:
        # stacklevel=2を指定することで、このメソッドを呼び出したメソッドの情報を出力する
        # エラーが発生している場合のみexc_infoを付与する
        self.logger.debug(msg, stacklevel=2, exc_info=_is_exc_info())

    def info(self, msg: object) -> None:
        self.logger.info(msg, stacklevel=2, exc_info=_is_exc_info())

    def warning(self, msg: object) -> None:
        self.logger.warning(msg, stacklevel=2, exc_info=_is_exc_info())

    def error(self, msg: object) -> None:
        self.logger.error(msg, stacklevel=2, exc_info=_is_exc_info())

    def critical(self, msg: object) -> None:
        self.logger.critical(msg, stacklevel=2, exc_info=_is_exc_info())


def init_logger() -> None:
    """Loggerを初期化する"""
    logger_config_path = os.path.join(os.path.dirname(__file__), LOGGER_CONFIG_FILE)
    with open(logger_config_path) as f:
        logger_config = yaml.safe_load(f)
    dictConfig(logger_config)


init_logger()
