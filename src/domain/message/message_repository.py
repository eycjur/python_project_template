from abc import ABC, abstractmethod

from src.domain.message.message import Message


class IMessageRepository(ABC):
    @abstractmethod
    def upsert(self, message: Message) -> None:
        pass

    @abstractmethod
    def find_all(self, limit: int = 10) -> list[Message]:
        pass
