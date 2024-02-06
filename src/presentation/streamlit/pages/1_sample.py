import streamlit as st

from src.usecase.sample import func

st.title("サンプルページ")

user_input = st.text_input("テキストを入力してください")

if st.button("Submit"):
    result = func(user_input)
    st.write(result)
