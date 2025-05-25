import streamlit as st

from app.presentation.streamlit.layouts.injector import injector
from app.shared.controller.message_controller import (
    RegisterMessageController,
    handle_controller_error,
)
from app.shared.dto.message_dto import RegisterMessageRequest


def main() -> None:
    st.title("登録")

    user_input = st.text_input("テキストを入力してください")

    if st.button("Submit"):
        try:
            # 共通DTOを作成
            dto_request = RegisterMessageRequest(text=user_input)
            
            # 共通コントローラーを使用
            controller = injector.get(RegisterMessageController)
            result = controller.execute(dto_request)
            
            st.success(result.message)
            
        except ValueError as e:
            # バリデーションエラー
            error_response = handle_controller_error(e)
            st.error(error_response.error_message)
            
        except Exception as e:
            # 内部エラー
            error_response = handle_controller_error(e)
            st.error(f"内部エラー: {error_response.error_message}")


main()
