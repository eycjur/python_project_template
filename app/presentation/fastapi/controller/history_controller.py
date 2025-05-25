from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from injector import Injector

from app.presentation.fastapi.controller.get_injector import get_injector
from app.presentation.fastapi.view_model.history_view_model import HistoryResponse
from app.shared.controller.message_controller import (
    MessageHistoryController,
    handle_controller_error,
)

router = APIRouter()


@router.get("/messages")
def get_history(
    injector: Annotated[Injector, Depends(get_injector)],
) -> HistoryResponse:
    """メッセージ履歴を取得する
    
    Args:
        injector: DIコンテナ
        
    Returns:
        HistoryResponse: 履歴取得結果
        
    Raises:
        HTTPException: 内部エラー
    """
    try:
        # 共通コントローラーを使用
        controller = injector.get(MessageHistoryController)
        result = controller.execute(None)
        
        # FastAPI形式のレスポンスに変換
        return HistoryResponse(
            messages=result.messages,
            count=result.count
        )
        
    except Exception as e:
        # 内部エラー
        error_response = handle_controller_error(e)
        raise HTTPException(status_code=500, detail=error_response.to_dict())
