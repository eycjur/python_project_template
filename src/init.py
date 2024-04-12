"""Dependency Injection用のインスタンス生成関数を定義するモジュール"""

from src.domain.message.message_repository import IMessageRepository
from src.infrastructure.repository.message.aws_message_repository import (
    AWSMessageRepository,
)
from src.infrastructure.repository.message.azure_message_repository import (
    AzureMessageRepository,
)
from src.infrastructure.repository.message.gcp_message_repository import (
    GCPMessageRepository,
)
from src.infrastructure.repository.message.sqlite_message_repository import (
    SQLiteMessageRepository,
)
from src.settings import (
    AWS_DYNAMODB_TABLE_NAME_HISTORIES,
    AZURE_COSMOS_CONTAINER_NAME_HISTORIES,
    AZURE_COSMOS_DATABASE_NAME,
    AZURE_COSMOS_ENDPOINT,
    BASE_DIR,
    CLOUD,
    GCP_FIRESTORE_COLLECTION_NAME_HISTORIES,
    GCP_FIRESTORE_DB_NAME,
    CloudType,
)


def get_message_repository() -> IMessageRepository:
    if CLOUD == CloudType.Local:
        return SQLiteMessageRepository(BASE_DIR / "db" / "db.sqlite3")
    elif CLOUD == CloudType.GCP:
        return GCPMessageRepository(
            GCP_FIRESTORE_DB_NAME, GCP_FIRESTORE_COLLECTION_NAME_HISTORIES
        )
    elif CLOUD == CloudType.AWS:
        return AWSMessageRepository(AWS_DYNAMODB_TABLE_NAME_HISTORIES)
    elif CLOUD == CloudType.AZURE:
        return AzureMessageRepository(
            AZURE_COSMOS_ENDPOINT,
            AZURE_COSMOS_DATABASE_NAME,
            AZURE_COSMOS_CONTAINER_NAME_HISTORIES,
        )
    raise ValueError("Invalid cloud type")
