import os
from enum import Enum
from pathlib import Path

from environs import Env
from pytz import timezone  # type: ignore


class RunEnv(Enum):
    """実行している環境"""

    LOCAL = "Local"
    GITHUB_ACTIONS = "GitHub Actions"
    GCP = "GCP"
    AWS = "AWS"
    AZURE = "Azure"

    @classmethod
    def judge_from_env(cls) -> "RunEnv":
        if "GITHUB_ACTIONS" in os.environ:
            return cls.GITHUB_ACTIONS
        if "K_SERVICE" in os.environ:  # Cloud Run
            return cls.GCP
        if "AWS_EXECUTION_ENV" in os.environ:  # App Runner
            return cls.AWS
        if "CONTAINER_APP_REPLICA_NAME" in os.environ:  # Container Apps
            return cls.AZURE
        return cls.LOCAL


RUN_ENV = RunEnv.judge_from_env()

# HACK: CI環境の場合は環境変数がなくてもエラーとしないように、遅延バリデーションとする
env = Env(eager=RUN_ENV != RunEnv.GITHUB_ACTIONS)


BASE_DIR = Path(__file__).resolve().parent.parent
JST = timezone("Asia/Tokyo")

CONTAINER_PORT = env.int("CONTAINER_PORT")

GCP_FIRESTORE_DB_NAME = env.str("GCP_FIRESTORE_DB_NAME")
GCP_FIRESTORE_COLLECTION_NAME_HISTORIES = env.str(
    "GCP_FIRESTORE_COLLECTION_NAME_HISTORIES"
)
AZURE_COSMOS_ENDPOINT = env.str("AZURE_COSMOS_ENDPOINT")
AZURE_COSMOS_DATABASE_NAME = env.str("AZURE_COSMOS_DATABASE_NAME")
AZURE_COSMOS_CONTAINER_NAME_HISTORIES = env.str("AZURE_COSMOS_CONTAINER_NAME_HISTORIES")
AWS_DYNAMODB_TABLE_NAME_HISTORIES = env.str("AWS_DYNAMODB_TABLE_NAME_HISTORIES")

match RUN_ENV:
    case RunEnv.LOCAL:
        LOGGER_CONFIG_FILE = env.str("LOGGER_CONFIG_FILE_DEFAULT")
    case RunEnv.GITHUB_ACTIONS:
        LOGGER_CONFIG_FILE = "logger_config_default.yaml"
    case RunEnv.GCP:
        LOGGER_CONFIG_FILE = env.str("LOGGER_CONFIG_FILE_GCP")
    case RunEnv.AWS:
        LOGGER_CONFIG_FILE = env.str("LOGGER_CONFIG_FILE_AWS")
    case RunEnv.AZURE:
        LOGGER_CONFIG_FILE = env.str("LOGGER_CONFIG_FILE_AZURE")
    case _:
        raise ValueError(f"Unexpected RUN_ENV: {RUN_ENV}")
