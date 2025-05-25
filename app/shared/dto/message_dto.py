"""メッセージ関連のDTO（Data Transfer Object）を定義する"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from app.domain.message.message import Message


class IMessageRequestDTO(ABC):
    """メッセージ登録リクエストの共通インターフェース"""
    
    @abstractmethod
    def to_message(self) -> Message:
        """DTOからドメインオブジェクトに変換する
        
        Returns:
            Message: ドメインオブジェクト
        """
        pass
    
    @abstractmethod
    def validate(self) -> None:
        """入力値を検証する
        
        Raises:
            ValueError: 入力値が不正な場合
        """
        pass


class IMessageResponseDTO(ABC):
    """メッセージ操作レスポンスの共通インターフェース"""
    
    @abstractmethod
    def to_dict(self) -> dict[str, Any]:
        """辞書形式に変換する
        
        Returns:
            dict: 辞書形式のデータ
        """
        pass


@dataclass(frozen=True)
class RegisterMessageRequest(IMessageRequestDTO):
    """メッセージ登録リクエスト"""
    
    text: str
    
    def to_message(self) -> Message:
        """DTOからドメインオブジェクトに変換する
        
        Returns:
            Message: ドメインオブジェクト
        """
        return Message(self.text)
    
    def validate(self) -> None:
        """入力値を検証する
        
        Raises:
            ValueError: 入力値が不正な場合
        """
        if not self.text:
            raise ValueError("メッセージが入力されていません")
        if len(self.text) > 1000:
            raise ValueError("メッセージは1000文字以内で入力してください")


@dataclass(frozen=True)
class RegisterMessageResponse(IMessageResponseDTO):
    """メッセージ登録レスポンス"""
    
    message: str
    success: bool = True
    
    def to_dict(self) -> dict[str, Any]:
        """辞書形式に変換する
        
        Returns:
            dict: 辞書形式のデータ
        """
        return {
            "message": self.message,
            "success": self.success
        }


@dataclass(frozen=True)
class MessageHistoryResponse(IMessageResponseDTO):
    """メッセージ履歴レスポンス"""
    
    messages: list[dict[str, str]]
    count: int
    
    def to_dict(self) -> dict[str, Any]:
        """辞書形式に変換する
        
        Returns:
            dict: 辞書形式のデータ
        """
        return {
            "messages": self.messages,
            "count": self.count
        }
    
    @classmethod
    def from_messages(cls, messages: list[Message]) -> "MessageHistoryResponse":
        """ドメインオブジェクトからDTOを作成する
        
        Args:
            messages: メッセージのリスト
            
        Returns:
            MessageHistoryResponse: DTOオブジェクト
        """
        message_dicts = [{"id": msg.id, "content": msg.content} for msg in messages]
        return cls(messages=message_dicts, count=len(message_dicts))


@dataclass(frozen=True)
class ErrorResponse(IMessageResponseDTO):
    """エラーレスポンス"""
    
    error_message: str
    error_code: str = "INTERNAL_ERROR"
    success: bool = False
    
    def to_dict(self) -> dict[str, Any]:
        """辞書形式に変換する
        
        Returns:
            dict: 辞書形式のデータ
        """
        return {
            "error_message": self.error_message,
            "error_code": self.error_code,
            "success": self.success
        }