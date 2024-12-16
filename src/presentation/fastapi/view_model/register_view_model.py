from pydantic import BaseModel

from src.domain.message.message import Message


class RegisterRequest(BaseModel):
    content: str

    def to_message(self) -> Message:
        return Message(self.content)


class RegisterResponse(BaseModel):
    text: str
