import streamlit as st

from src.domain.message.message import Message
from src.presentation.streamlit.layouts.injector import injector
from src.usecase.register import RegisterUsecase


def main() -> None:
    st.title("登録")

    user_input = st.text_input("テキストを入力してください")

    if st.button("Submit"):
        register_usecase = injector.get(RegisterUsecase)
        result = register_usecase.execute(Message(user_input))
        st.write(result)


main()
