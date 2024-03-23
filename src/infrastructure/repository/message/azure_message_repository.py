from azure.cosmos import CosmosClient, PartitionKey
from azure.identity import DefaultAzureCredential

from src.domain.message.message import Message
from src.domain.message.message_repository import IMessageRepository
from src.infrastructure.repository.message.util import current_time_iso
from src.logger.logging import DefaultLogger

logger = DefaultLogger(__name__)


class AzureMessageRepository(IMessageRepository):
    """

    Note:
        Microsoft.DocumentDB/databaseAccounts/readMetadataという権限が必要というエラーが出るので、以下のコマンドで権限を付与する必要がある。
        az cosmosdb sql role assignment create --account-name <CosmosDBのアカウント名> --resource-group <リソースグループ名> --scope "/" --principal-id <EntraIDのエンタープライズアプリケーションの該当アプリケーションのオブジェクトID> --role-definition-id <ロールid=00000000-0000-0000-0000-000000000002>
        cf. https://learn.microsoft.com/ja-jp/azure/cosmos-db/how-to-setup-rbac
    """  # noqa

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
        query = f"SELECT TOP {limit} * FROM c ORDER BY c.update_at DESC"
        result = self._container.query_items(
            query=query, enable_cross_partition_query=True
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
