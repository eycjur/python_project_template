from injector import inject

from app.domain.message.message import Message
from app.domain.message.message_repository import IMessageRepository
from app.logger.logging import DefaultLogger

logger = DefaultLogger(__name__)


class RegisterUsecase:
    @inject
    def __init__(self, message_repository: IMessageRepository) -> None:
        self._message_repository = message_repository

    def execute(self, message: Message) -> str:
        """メッセージを保存する

        Args:
            message (Message): 保存するメッセージ

        Returns:
            str: 保存完了メッセージ
        """
        self._message_repository.upsert(message)
        logger.info(f"Message: {message.content}")
        return "データの保存が完了しました。"
