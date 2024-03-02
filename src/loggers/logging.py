import logging
import os
import sys
from logging.config import dictConfig

import yaml  # type: ignore

from src.settings import LOGGER_CONFIG_FILE


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
        # exc_infoを利用するとなぜかログが出力されずstack_infoのみが出力されるので、
        # エラーが発生している場合のみstack_infoを出力するようにしている
        self.logger.debug(msg, stacklevel=2, stack_info=sys.exc_info()[0] is not None)

    def info(self, msg: object) -> None:
        self.logger.info(msg, stacklevel=2, stack_info=sys.exc_info()[0] is not None)

    def warning(self, msg: object) -> None:
        self.logger.warning(msg, stacklevel=2, stack_info=sys.exc_info()[0] is not None)

    def error(self, msg: object) -> None:
        self.logger.error(msg, stacklevel=2, stack_info=sys.exc_info()[0] is not None)


def init_logger() -> None:
    logger_config_path = os.path.join(os.path.dirname(__file__), LOGGER_CONFIG_FILE)
    dictConfig(yaml.load(open(logger_config_path).read(), Loader=yaml.SafeLoader))


init_logger()
