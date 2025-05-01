import streamlit as st

from app.presentation.streamlit.layouts.injector import injector
from app.usecase.history import HistoryUsecase


def main() -> None:
    st.title("履歴")

    history_usecase = injector.get(HistoryUsecase)
    messages = history_usecase.execute()
    for m in messages:
        with st.chat_message("user"):
            st.write(m.content)


main()
