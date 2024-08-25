import streamlit as st

from src.di import injector
from src.usecase.error import ErrorUsecase

st.title("エラーが発生するページ")

error_usecase = injector.get(ErrorUsecase)
result = error_usecase.execute()
st.write(result)
