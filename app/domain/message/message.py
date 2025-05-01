import uuid
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass(eq=True, frozen=True)
class ID:
    """メッセージのIDを表す値オブジェクト"""

    value: str = field(default_factory=lambda: str(uuid.uuid4()))


class Message:
    """メッセージを表すエンティティ"""

    def __init__(self, content: str, *, id: Optional[ID] = None) -> None:  # noqa: A002
        self._content = content
        self._id = id if id is not None else ID()

    def __eq__(self, obj: Any) -> bool:
        if isinstance(obj, Message):
            return self._id == obj._id

        return False

    @property
    def id(self) -> str:
        return self._id.value

    @property
    def content(self) -> str:
        return self._content

    @classmethod
    def from_repository(cls, data: dict[str, str]) -> "Message":
        """リポジトリから取得したデータをエンティティに変換する

        Args:
            data (dict[str, str]): リポジトリから取得したデータ

        Returns:
            Message: エンティティ
        """
        return cls(data["content"], id=ID(data["id"]))

    def to_repository(self) -> dict[str, str]:
        """エンティティをリポジトリに保存する形式に変換する

        Returns:
            dict[str, str]: リポジトリに保存する形式のデータ
        """
        return {"id": self.id, "content": self.content}
