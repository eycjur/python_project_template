from pydantic import BaseModel

from src.domain.message.message import Message


class RegisterRequest(BaseModel):
    text: str

    def to_message(self) -> Message:
        return Message(self.text)


class RegisterResponse(BaseModel):
    text: str
