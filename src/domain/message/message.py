import uuid
from dataclasses import dataclass
from typing import Any, Optional


@dataclass(eq=True, frozen=True)
class ID:
    value: str = str(uuid.uuid4())


class Message:
    def __init__(self, content: str, *, id: Optional[ID] = None) -> None:
        if id is None:
            id = ID()
        self.content = content
        self._id = id

    def __eq__(self, obj: Any) -> bool:
        if isinstance(obj, Message):
            return self._id == obj._id

        return False

    @property
    def id(self) -> str:
        return self._id.value

    @classmethod
    def from_repository(cls, data: dict[str, str]) -> "Message":
        return cls(data["content"], id=ID(data["id"]))

    def to_repository(self) -> dict[str, str]:
        return {"id": self.id, "content": self.content}
