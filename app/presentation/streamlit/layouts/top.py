import streamlit as st

from app.di import get_injector
from app.usecase.history import HistoryUsecase


def main() -> None:
    st.title("履歴")

    injector = get_injector()
    history_usecase = injector.get(HistoryUsecase)
    messages = history_usecase.execute()
    for m in messages:
        with st.chat_message("user"):
            st.write(m.content)


main()
