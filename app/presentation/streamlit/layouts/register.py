import streamlit as st

from app.di import get_injector
from app.domain.message.message import Message
from app.usecase.register import RegisterUsecase


def main() -> None:
    st.title("登録")

    user_input = st.text_input("テキストを入力してください")

    if st.button("Submit"):
        injector = get_injector()
        register_usecase = injector.get(RegisterUsecase)
        result = register_usecase.execute(Message(user_input))
        st.write(result)


main()
