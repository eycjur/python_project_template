import boto3
from boto3.dynamodb.conditions import Key

from app.domain.message.message import Message
from app.domain.message.message_repository import IMessageRepository
from app.infrastructure.repository.message.util import current_time_iso
from app.logger.logging import DefaultLogger

logger = DefaultLogger(__name__)


class AWSMessageRepository(IMessageRepository):
    def __init__(self, table_name: str) -> None:
        dynamodb = boto3.resource("dynamodb")
        self._table = dynamodb.Table(table_name)

    def upsert(self, message: Message) -> None:
        self._table.put_item(
            Item={
                "partition_key": "default",
                "update_at": current_time_iso(),
                **message.to_repository(),
            }
        )

    def find_all(self, limit: int = 10) -> list[Message]:
        response = self._table.query(
            Limit=limit,
            ScanIndexForward=False,  # to get results ordered by update_at descending
            KeyConditionExpression=Key("partition_key").eq("default"),
        )

        messages = []
        for item in response["Items"]:
            try:
                message = Message.from_repository(item)
                messages.append(message)
            except Exception as e:
                logger.error(f"DynamoDBからのデータの読み込みに失敗しました。: {e}")
                continue
        return messages
