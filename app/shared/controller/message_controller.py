"""メッセージ関連の共通コントローラー実装"""

from injector import inject

from app.shared.controller.base_controller import BaseController
from app.shared.dto.message_dto import (
    ErrorResponse,
    MessageHistoryResponse,
    RegisterMessageRequest,
    RegisterMessageResponse,
)
from app.usecase.history import HistoryUsecase
from app.usecase.register import RegisterUsecase


class RegisterMessageController(BaseController[RegisterMessageRequest, RegisterMessageResponse]):
    """メッセージ登録コントローラー"""
    
    @inject
    def __init__(self, register_usecase: RegisterUsecase) -> None:
        super().__init__()
        self._register_usecase = register_usecase
    
    def _execute_impl(self, request: RegisterMessageRequest) -> RegisterMessageResponse:
        """メッセージ登録処理を実行する
        
        Args:
            request: 登録リクエスト
            
        Returns:
            RegisterMessageResponse: 登録結果
            
        Raises:
            ValueError: 入力値が不正な場合
        """
        # 入力値検証
        request.validate()
        
        # ドメインオブジェクトに変換
        message = request.to_message()
        
        # ユースケース実行
        result_message = self._register_usecase.execute(message)
        
        return RegisterMessageResponse(message=result_message)


class MessageHistoryController(BaseController[None, MessageHistoryResponse]):
    """メッセージ履歴取得コントローラー"""
    
    @inject
    def __init__(self, history_usecase: HistoryUsecase) -> None:
        super().__init__()
        self._history_usecase = history_usecase
    
    def _execute_impl(self, request: None) -> MessageHistoryResponse:
        """メッセージ履歴取得処理を実行する
        
        Args:
            request: リクエスト（不要）
            
        Returns:
            MessageHistoryResponse: 履歴取得結果
        """
        # ユースケース実行
        messages = self._history_usecase.execute()
        
        # DTOに変換
        return MessageHistoryResponse.from_messages(messages)


def handle_controller_error(error: Exception) -> ErrorResponse:
    """コントローラーのエラーを統一的に処理する
    
    Args:
        error: 発生したエラー
        
    Returns:
        ErrorResponse: エラーレスポンス
    """
    if isinstance(error, ValueError):
        return ErrorResponse(
            error_message=str(error),
            error_code="VALIDATION_ERROR"
        )
    
    return ErrorResponse(
        error_message="内部エラーが発生しました",
        error_code="INTERNAL_ERROR"
    )