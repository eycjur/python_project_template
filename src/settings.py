import os

from environs import Env

IS_GITHUB_ACTIONS = "GITHUB_ACTIONS" in os.environ


# HACK: CI環境の場合は環境変数がなくてもエラーとしないように、遅延バリデーションとする
env = Env(eager=not IS_GITHUB_ACTIONS)

APP_PORT = env.int("APP_PORT")
LOGGER_CONFIG_FILE = env.str("LOGGER_CONFIG_FILE")
