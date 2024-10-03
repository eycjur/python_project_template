from azure.cosmos import CosmosClient, PartitionKey
from azure.identity import DefaultAzureCredential

from src.domain.message.message import Message
from src.domain.message.message_repository import IMessageRepository
from src.infrastructure.repository.message.util import current_time_iso
from src.logger.logging import DefaultLogger

logger = DefaultLogger(__name__)


class AzureMessageRepository(IMessageRepository):
    def __init__(self, endpoint: str, database_name: str, container_name: str) -> None:
        aad_credentials = DefaultAzureCredential()
        client = CosmosClient(endpoint, credential=aad_credentials)
        database = client.create_database_if_not_exists(database_name)
        self._container = database.create_container_if_not_exists(
            container_name, partition_key=PartitionKey("/partition_key")
        )

    def upsert(self, message: Message) -> None:
        self._container.upsert_item(
            message.to_repository()
            | {"partition_key": "default", "update_at": current_time_iso()}
        )

    def find_all(self, limit: int = 10) -> list[Message]:
        query = "SELECT TOP @limit * FROM c ORDER BY c.update_at DESC"
        result = self._container.query_items(
            query=query,
            parameters=[{"name": "@limit", "value": limit}],
            enable_cross_partition_query=True,
        )

        messages = []
        for doc in result:
            try:
                message = Message.from_repository(doc)
                messages.append(message)
            except Exception as e:
                logger.error(f"CosmosDBからのデータの読み込みに失敗しました。: {e}")
                continue
        return messages
