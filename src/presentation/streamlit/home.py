import streamlit as st
from src.di import injector
from src.usecase.history import HistoryUsecase

st.title("履歴ページ")

hisotry_usecase = injector.get(HistoryUsecase)
messages = hisotry_usecase.execute()
for m in messages:
    with st.chat_message("user"):
        st.write(m.content)
