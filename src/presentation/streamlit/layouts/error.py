import streamlit as st

from src.di import injector
from src.usecase.error import ErrorUsecase


def main() -> None:
    st.title("エラー")

    error_usecase = injector.get(ErrorUsecase)
    result = error_usecase.execute()
    st.write(result)


main()
