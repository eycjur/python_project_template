import os
from enum import Enum

from environs import Env
from pytz import timezone  # type: ignore


class CloudType(Enum):
    GCP = "GCP"
    AWS = "AWS"
    AZURE = "Azure"


IS_GITHUB_ACTIONS = "GITHUB_ACTIONS" in os.environ
IS_GCP = "K_SERVICE" in os.environ  # Cloud Run
IS_AWS = "AWS_EXECUTION_ENV" in os.environ  # App Runner/ECS
IS_AZURE = "CONTAINER_APP_REPLICA_NAME" in os.environ  # Container Apps


def judge_cloud() -> CloudType:
    if IS_GCP:
        return CloudType.GCP
    elif IS_AWS:
        return CloudType.AWS
    elif IS_AZURE:
        return CloudType.AZURE

    cloud_env = env.str("CLOUD", default="None")
    for cloud in CloudType:
        if cloud.value == cloud_env:
            return cloud
    if not IS_GITHUB_ACTIONS:
        raise ValueError(f"Invalid cloud type: {cloud_env}")
    return CloudType.GCP  # CI環境の場合は適当にGCPとする


# HACK: CI環境の場合は環境変数がなくてもエラーとしないように、遅延バリデーションとする
env = Env(eager=not IS_GITHUB_ACTIONS)

CLOUD = judge_cloud()

CONTAINER_PORT = env.int("CONTAINER_PORT")
# CI環境でもloggerのinitに必要なため、デフォルト値を設定
LOGGER_CONFIG_FILE_DEFAULT = env.str(
    "LOGGER_CONFIG_FILE_DEFAULT", default="logger_config_default.yaml"
)
LOGGER_CONFIG_FILE_GCP = env.str("LOGGER_CONFIG_FILE_GCP")
LOGGER_CONFIG_FILE_AWS = env.str("LOGGER_CONFIG_FILE_AWS")
LOGGER_CONFIG_FILE_AZURE = env.str("LOGGER_CONFIG_FILE_AZURE")
if IS_GCP:
    LOGGER_CONFIG_FILE = LOGGER_CONFIG_FILE_GCP
elif IS_AWS:
    LOGGER_CONFIG_FILE = LOGGER_CONFIG_FILE_AWS
elif IS_AZURE:
    LOGGER_CONFIG_FILE = LOGGER_CONFIG_FILE_AZURE
else:
    LOGGER_CONFIG_FILE = LOGGER_CONFIG_FILE_DEFAULT

GCP_FIRESTORE_DB_NAME = env.str("GCP_FIRESTORE_DB_NAME")
GCP_FIRESTORE_COLLECTION_NAME_HISTORIES = env.str(
    "GCP_FIRESTORE_COLLECTION_NAME_HISTORIES"
)
AZURE_COSMOS_ENDPOINT = env.str("AZURE_COSMOS_ENDPOINT")
AZURE_COSMOS_DATABASE_NAME = env.str("AZURE_COSMOS_DATABASE_NAME")
AZURE_COSMOS_CONTAINER_NAME_HISTORIES = env.str("AZURE_COSMOS_CONTAINER_NAME_HISTORIES")
AWS_DYNAMODB_TABLE_NAME_HISTORIES = env.str("AWS_DYNAMODB_TABLE_NAME_HISTORIES")

JST = timezone("Asia/Tokyo")
