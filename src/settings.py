import os

from environs import Env

IS_GITHUB_ACTIONS = "GITHUB_ACTIONS" in os.environ
IS_GCP = "K_SERVICE" in os.environ

# HACK: CI環境の場合は環境変数がなくてもエラーとしないように、遅延バリデーションとする
env = Env(eager=not IS_GITHUB_ACTIONS)

CONTAINER_PORT = env.int("CONTAINER_PORT")
# CI環境でもloggerのinitに必要なため、デフォルト値を設定
LOGGER_CONFIG_FILE_DEFAULT = env.str(
    "LOGGER_CONFIG_FILE_DEFAULT", default="logger_config_default.yaml"
)
LOGGER_CONFIG_FILE_GCP = env.str("LOGGER_CONFIG_FILE_GCP")
LOGGER_CONFIG_FILE = LOGGER_CONFIG_FILE_GCP if IS_GCP else LOGGER_CONFIG_FILE_DEFAULT
