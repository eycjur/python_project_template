"""プレゼンテーション層の共通コントローラー基底クラス"""

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from app.logger.logging import DefaultLogger

InputT = TypeVar("InputT")
OutputT = TypeVar("OutputT")


class IController(ABC, Generic[InputT, OutputT]):
    """コントローラーの共通インターフェース"""
    
    @abstractmethod
    def execute(self, request: InputT) -> OutputT:
        """リクエストを処理してレスポンスを返す
        
        Args:
            request: 入力データ
            
        Returns:
            処理結果
        """
        pass


class BaseController(IController[InputT, OutputT]):
    """コントローラーの基底クラス
    
    共通的な処理やログ出力を提供する。
    """
    
    def __init__(self) -> None:
        self._logger = DefaultLogger(self.__class__.__name__)
    
    def execute(self, request: InputT) -> OutputT:
        """リクエストを処理してレスポンスを返す
        
    Args:
            request: 入力データ
            
        Returns:
            処理結果
        """
        try:
            self._logger.info(f"Controller execution started: {self.__class__.__name__}")
            result = self._execute_impl(request)
            self._logger.info(f"Controller execution completed: {self.__class__.__name__}")
            return result
        except Exception as e:
            self._logger.error(f"Controller execution failed: {self.__class__.__name__}, Error: {e}")
            raise
    
    @abstractmethod
    def _execute_impl(self, request: InputT) -> OutputT:
        """実際の処理実装
        
        サブクラスでオーバーライドする。
        
        Args:
            request: 入力データ
            
        Returns:
            処理結果
        """
        pass