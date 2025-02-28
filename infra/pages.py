import streamlit as st

# =============== PAGINAS ===============
from pages.extrato import extrato
from pages.login import login_page
# ======================================

class Pages:
    @staticmethod
    def exec():
        page_list = []
        if "account" in st.session_state:
            page_list.append(st.Page(extrato, title="Extrato"))
        else:
            page_list.append(st.Page(login_page, title="Login"))

        pg = st.navigation(page_list)
        pg.run()
