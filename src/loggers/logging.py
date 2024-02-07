import logging
import os
from logging.config import dictConfig
from typing import Any

import yaml  # type: ignore

from src.settings import LOGGER_CONFIG_FILE


class Singleton(object):
    """シングルトン（あるクラスのインスタンスがプログラム内で1つだけ存在することを保証する）

    Singleton interface:
    http://www.python.org/download/releases/2.2.3/descrintro/#__new__
    """

    def __new__(cls, *args: Any, **kwds: Any) -> "Singleton":
        it = cls.__dict__.get("__it__")
        if it is not None:
            return it  # type: ignore
        cls.__it__ = it = object.__new__(cls)
        it.init(*args, **kwds)
        return it

    def init(self, *args: Any, **kwds: Any) -> None:
        pass


class LoggerManager(Singleton):
    """ロガーを管理するクラス

    直接は利用しないこと
    """

    def init(self) -> None:
        self.logger = logging.getLogger()

        logger_config_path = os.path.join(os.path.dirname(__file__), LOGGER_CONFIG_FILE)
        dictConfig(yaml.load(open(logger_config_path).read(), Loader=yaml.SafeLoader))

    def debug(self, logger_name: str, msg: object) -> None:
        self.logger = logging.getLogger(logger_name)
        self.logger.debug(msg)

    def info(self, logger_name: str, msg: object) -> None:
        self.logger = logging.getLogger(logger_name)
        self.logger.info(msg)

    def warning(self, logger_name: str, msg: object) -> None:
        self.logger = logging.getLogger(logger_name)
        self.logger.warning(msg)

    def error(self, logger_name: str, msg: object) -> None:
        self.logger = logging.getLogger(logger_name)
        self.logger.error(msg)


class DefaultLogger(object):
    """Logger object.

    ログを出力する際はこれを利用すること

    Example:
        >>> logger = DefaultLogger(__name__)
        >>> logger.debug("debug message")
    """

    def __init__(self, logger_name: str = "root") -> None:
        self.log_manager = LoggerManager()
        self.logger_name = logger_name

    def debug(self, msg: object) -> None:
        self.log_manager.debug(self.logger_name, msg)

    def info(self, msg: object) -> None:
        self.log_manager.info(self.logger_name, msg)

    def warning(self, msg: object) -> None:
        self.log_manager.warning(self.logger_name, msg)

    def error(self, msg: object) -> None:
        self.log_manager.error(self.logger_name, msg)
