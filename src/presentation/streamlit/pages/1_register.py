import streamlit as st
from injector import Injector

from src.di import get_di_module
from src.domain.message.message import Message
from src.usecase.register import RegisterUsecase

st.title("登録ページ")

user_input = st.text_input("テキストを入力してください")

if st.button("Submit"):
    injector = Injector([get_di_module()])
    register_usecase = injector.get(RegisterUsecase)
    result = register_usecase.execute(Message(user_input))
    st.write(result)
