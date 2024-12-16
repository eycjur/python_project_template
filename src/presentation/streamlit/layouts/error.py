import streamlit as st

from src.presentation.streamlit.layouts.injector import injector
from src.usecase.error import ErrorUsecase


def main() -> None:
    st.title("エラー")

    error_usecase = injector.get(ErrorUsecase)
    result = error_usecase.execute()
    st.write(result)


main()
