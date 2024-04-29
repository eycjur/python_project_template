import streamlit as st
from injector import Injector

from src.di import get_di_module
from src.usecase.error import ErrorUsecase

st.title("エラーが発生するページ")

injector = Injector([get_di_module()])
error_usecase = injector.get(ErrorUsecase)
result = error_usecase.execute()
st.write(result)
