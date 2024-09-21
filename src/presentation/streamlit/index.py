import streamlit as st
from streamlit.navigation.page import StreamlitPage


def page_component() -> StreamlitPage:
    history_page = st.Page(page="layouts/top.py", title="履歴")
    register_page = st.Page(page="layouts/register.py", title="登録")
    error_page = st.Page(page="layouts/error.py", title="エラー")
    return st.navigation(
        [
            history_page,
            register_page,
            error_page,
        ]
    )


def main() -> None:
    st.set_page_config(page_title="Python Project Template", page_icon=":snake:")

    pg = page_component()
    pg.run()


if __name__ == "__main__":
    main()
