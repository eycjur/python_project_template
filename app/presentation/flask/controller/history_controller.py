from flask import flash, render_template
from injector import Injector

from app.shared.controller.message_controller import (
    MessageHistoryController,
    handle_controller_error,
)


def history(injector: Injector) -> str:
    """メッセージ履歴を表示する
    
    Args:
        injector: DIコンテナ
        
    Returns:
        str: 履歴ページのHTML
    """
    try:
        # 共通コントローラーを使用
        controller = injector.get(MessageHistoryController)
        result = controller.execute(None)
        
        # メッセージデータを取得
        messages = [
            {"id": msg["id"], "content": msg["content"]} 
            for msg in result.messages
        ]
        
        return render_template("history.html", messages=messages)
        
    except Exception as e:
        # 内部エラー
        error_response = handle_controller_error(e)
        flash(error_response.error_message, "error")
        return render_template("history.html", messages=[])
