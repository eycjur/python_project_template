from google.cloud import firestore

from app.domain.message.message import Message
from app.domain.message.message_repository import IMessageRepository
from app.infrastructure.repository.message.util import current_time_iso
from app.logger.logging import DefaultLogger

logger = DefaultLogger(__name__)


class GCPMessageRepository(IMessageRepository):
    def __init__(self, database_name: str, collection_name: str) -> None:
        firestore_client = firestore.Client(database=database_name)
        self._collection = firestore_client.collection(collection_name)

    def upsert(self, message: Message) -> None:
        doc = self._collection.document(message.id)
        doc.set(message.to_repository() | {"update_at": current_time_iso()})

    def find_all(self, limit: int = 10) -> list[Message]:
        result = (
            self._collection.order_by("update_at", direction=firestore.Query.DESCENDING)
            .limit(limit)
            .get()
        )

        messages = []
        for doc in result:
            try:
                message = Message.from_repository(doc.to_dict())
                messages.append(message)
            except Exception as e:
                logger.error(f"Firestoreからのデータの読み込みに失敗しました。: {e}")
                continue
        return messages
