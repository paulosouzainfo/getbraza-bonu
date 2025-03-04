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
            pg = st.navigation(page_list)
        else:
            page_list.append(st.Page(login_page, title="Login"))
            # page_list.append(st.Page(healthcheck, title="Healthcheck", url_path="healthz"))

            pg = st.navigation(page_list, position='hidden')
        pg.run()
