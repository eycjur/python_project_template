import streamlit as st

from src.domain.message.message import Message
from src.presentation.util.init import get_message_repository
from src.usecase.register import RegisterUsecase

st.title("登録ページ")

user_input = st.text_input("テキストを入力してください")

if st.button("Submit"):
    message_repository = get_message_repository()
    usecase = RegisterUsecase(message_repository)
    result = usecase.execute(Message(user_input))
    st.write(result)
