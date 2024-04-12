import streamlit as st

from src.usecase.error import ErrorUsecase

st.title("エラーが発生するページ")

result = ErrorUsecase().execute()
st.write(result)
