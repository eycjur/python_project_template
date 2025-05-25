from flask import flash, redirect, render_template, request
from injector import Injector
from werkzeug import Response

from app.shared.controller.message_controller import (
    RegisterMessageController,
    handle_controller_error,
)
from app.shared.dto.message_dto import RegisterMessageRequest


def register_get(injector: Injector) -> str:
    """メッセージ登録フォームを表示する"""
    return render_template("register.html")


def register_post(injector: Injector) -> Response:
    """メッセージ登録処理を実行する
    
    Args:
        injector: DIコンテナ
        
    Returns:
        Response: リダイレクトレスポンス
    """
    try:
        user_input = request.form["user_input"]
        
        # 共通DTOを作成
        dto_request = RegisterMessageRequest(text=user_input)
        
        # 共通コントローラーを使用
        controller = injector.get(RegisterMessageController)
        result = controller.execute(dto_request)
        
        # 成功メッセージを設定
        flash(result.message, "success")
        
    except ValueError as e:
        # バリデーションエラー
        error_response = handle_controller_error(e)
        flash(error_response.error_message, "error")
        
    except Exception as e:
        # 内部エラー
        error_response = handle_controller_error(e)
        flash(error_response.error_message, "error")
    
    return redirect("home")
