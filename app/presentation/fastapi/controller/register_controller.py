from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from injector import Injector

from app.presentation.fastapi.controller.get_injector import get_injector
from app.presentation.fastapi.view_model.register_view_model import (
    RegisterRequest,
    RegisterResponse,
)
from app.shared.controller.message_controller import (
    RegisterMessageController,
    handle_controller_error,
)
from app.shared.dto.message_dto import RegisterMessageRequest

router = APIRouter()


@router.post("/messages")
def register(
    request: RegisterRequest, injector: Annotated[Injector, Depends(get_injector)]
) -> RegisterResponse:
    """メッセージを登録する
    
    Args:
        request: 登録リクエスト
        injector: DIコンテナ
        
    Returns:
        RegisterResponse: 登録結果
        
    Raises:
        HTTPException: 入力値エラーまたは内部エラー
    """
    try:
        # FastAPI形式のリクエストを共通DTOに変換
        dto_request = RegisterMessageRequest(text=request.text)
        
        # 共通コントローラーを使用
        controller = injector.get(RegisterMessageController)
        result = controller.execute(dto_request)
        
        # FastAPI形式のレスポンスに変換
        return RegisterResponse(text=result.message)
        
    except ValueError as e:
        # バリデーションエラー
        error_response = handle_controller_error(e)
        raise HTTPException(status_code=400, detail=error_response.to_dict())
        
    except Exception as e:
        # 内部エラー
        error_response = handle_controller_error(e)
        raise HTTPException(status_code=500, detail=error_response.to_dict())
