import streamlit as st

from app.presentation.streamlit.layouts.injector import injector
from app.usecase.error import ErrorUsecase


def main() -> None:
    st.title("エラー")

    error_usecase = injector.get(ErrorUsecase)
    result = error_usecase.execute()
    st.write(result)


main()
