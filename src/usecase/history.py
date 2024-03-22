from src.domain.message.message import Message
from src.domain.message.message_repository import IMessageRepository


class HistoryUsecase:
    def __init__(self, message_repository: IMessageRepository) -> None:
        self._message_repository = message_repository

    def execute(self) -> list[Message]:
        return self._message_repository.find_all()
