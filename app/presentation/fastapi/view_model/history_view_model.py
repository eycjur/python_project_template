from pydantic import BaseModel

from app.domain.message.message import Message


class MessageResponse(BaseModel):
    content: str


class HistoryResponse(BaseModel):
    messages: list[MessageResponse]

    @classmethod
    def from_messages(cls, messages: list[Message]) -> "HistoryResponse":
        return cls(messages=[MessageResponse(content=m.content) for m in messages])
