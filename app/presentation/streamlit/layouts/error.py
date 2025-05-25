import streamlit as st

from app.di import get_injector
from app.usecase.error import ErrorUsecase


def main() -> None:
    st.title("エラー")

    injector = get_injector()
    error_usecase = injector.get(ErrorUsecase)
    result = error_usecase.execute()
    st.write(result)


main()
