import streamlit as st

from src.presentation.init import get_message_repository
from src.usecase.history import HistoryUsecase

st.title("履歴ページ")

message_repository = get_message_repository()
messages = HistoryUsecase(message_repository).execute()
for m in messages:
    with st.chat_message("user"):
        st.write(m.content)
