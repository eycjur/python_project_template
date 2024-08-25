import streamlit as st

from src.di import injector
from src.domain.message.message import Message
from src.usecase.register import RegisterUsecase

st.title("登録ページ")

user_input = st.text_input("テキストを入力してください")

if st.button("Submit"):
    register_usecase = injector.get(RegisterUsecase)
    result = register_usecase.execute(Message(user_input))
    st.write(result)
