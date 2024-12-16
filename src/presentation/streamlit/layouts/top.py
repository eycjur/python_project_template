import streamlit as st

from src.presentation.streamlit.layouts.injector import injector
from src.usecase.history import HistoryUsecase


def main() -> None:
    st.title("履歴")

    history_usecase = injector.get(HistoryUsecase)
    messages = history_usecase.execute()
    for m in messages:
        with st.chat_message("user"):
            st.write(m.content)


main()
