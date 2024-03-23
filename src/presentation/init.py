from src.domain.message.message_repository import IMessageRepository
from src.infrastructure.repository.message.gcp_message_repository import (
    GCPMessageRepository,
)
from src.settings import (
    CLOUD,
    GCP_FIRESTORE_COLLECTION_NAME,
    GCP_FIRESTORE_DB_NAME,
    CloudType,
)


def get_message_repository() -> IMessageRepository:
    if CLOUD == CloudType.GCP:
        return GCPMessageRepository(
            GCP_FIRESTORE_DB_NAME, GCP_FIRESTORE_COLLECTION_NAME
        )
    raise ValueError("Invalid cloud type")
