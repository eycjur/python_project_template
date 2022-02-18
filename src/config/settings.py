import logging
import os
import random
from pathlib import Path
from typing import Any, Dict, Tuple

import matplotlib.pyplot as plt
import numpy as np
import yaml

np.set_printoptions(suppress=True)
plt.rcParams["font.size"] = 16

BASE_DIR = Path(__file__).resolve().parents[2]  # python_project_template
SRC_DIR = BASE_DIR / "src"
LOG_FILE = BASE_DIR / "logs" / "log.txt"


class CFG:
    def __init__(self) -> None:
        with open(SRC_DIR / "config" / "config.yml") as file:
            self._config = yaml.safe_load(file.read())

    def __getattr__(self, name: str) -> Any:
        if name in self._config:
            return self._config[name]
        raise AttributeError(f"{name} is not found in config")


def set_seed(seed: int = 4) -> None:
    """seedを固定

    Args:
        seed (int, optional): シードの値 Defaults to 4.
    """
    np.random.seed(seed)
    random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    # tf.random.set_seed(CFG.seed)  # type: ignore


cfg = CFG()
set_seed(cfg.seed)


class CustomLoggerAdapter(logging.LoggerAdapter):
    """ロガーをカスタマイズするためのクラス

    - ログのextraにkeyが渡されなかったときにデフォルト値を追加する

    Args:
        logging (Logger): カスタマイズするロガー
    """

    def process(  # type: ignore[override]
        self, msg: str, kwargs: Dict[str, Any]
    ) -> Tuple[str, Dict[str, Any]]:
        """ログをとる処理で呼び出される

        Args:
            msg (str): ログメッセージ
            kwargs (Dict[str, Any]): ログメッセージに渡す引数 ex{'extra': {'key': 'deprecated'}}

        Returns:
            Tuple[str, Dict[str, Any]]: {"key": self.extra}を追加したログメッセージと引数
        """
        if "extra" not in kwargs or "key" not in kwargs["extra"]:
            kwargs["extra"] = self.extra
        return msg, kwargs


def set_logger(modname: str, set_level: str = cfg.mode) -> logging.Logger:
    """loggingに関する設定

    Args:
        modname (str): モジュールの名前(__name__を推奨)
        set_level (str): loggingを出力するレベル

    Raises:
        ValueError: set_levelがレベルでない場合

    Example:
        >>> import settings
        >>> logger = settings.set_logger(__name__, set_level="WARNING")
        >>> logger.warning(
        >>>     list(self.model.parameters()),
        >>>     extra={"key": "2dimensional_data"}
        >>> )
    """
    set_level = set_level.upper()

    if set_level not in ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"]:
        raise ValueError("set_levelが不正です: {set_level}")

    formatter = logging.Formatter(
        "----------\n{asctime} [{levelname}] {filename} {funcName} {lineno}\n"
        "{key}\n\n{message}\n",
        "%Y-%m-%d %H:%M:%S",
        style="{",
    )

    # ストリームハンドラの設定
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(getattr(logging, set_level))

    # ファイルハンドラの設定
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(getattr(logging, set_level))

    logger = logging.getLogger(modname)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
    logger.propagate = False

    default_extra = {"key": "None"}
    logger = CustomLoggerAdapter(logger, default_extra)  # type: ignore

    return logger
