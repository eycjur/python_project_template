import os


def get_env_variable(name: str) -> str:
    """環境変数を取得する

    環境変数が設定されていない場合は例外を発生させる
    """
    env = os.getenv(name, None)
    if env is None:
        raise ValueError(f"{name} is not set.")
    return env


APP_PORT = int(get_env_variable("APP_PORT"))
LOGGER_CONFIG_FILE = get_env_variable("LOGGER_CONFIG_FILE")
