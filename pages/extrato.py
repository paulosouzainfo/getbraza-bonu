import streamlit as st
import requests  # type: ignore

from controller.statement import Statement
from controller.transfer import make_transfer
from infra.config import Config as config


def extrato():
    st.subheader(f"CONTA: {st.session_state['account'].account_number}")
    st.markdown("---")

    try:
        coin_list = requests.get(config.COINS_ENDPOINT, timeout=10).json().keys()
    except Exception:
        st.exception("Não foi possível obter a lista de moedas completa")
        coin_list = ["BRL", "USDT"]
    with st.form("Extrato", border=False):
        c = st.columns([15, 20, 20, 20, 25])
        with c[0]:
            coin = st.selectbox("MOEDA", coin_list)
        with c[1]:
            st.markdown(
                '<div style="display: flex; justify-content: center; height: 28px">',
                unsafe_allow_html=True
            )
            statement_form_submit = st.form_submit_button("Verificar")
            st.markdown("</div>", unsafe_allow_html=True)

    if statement_form_submit:
        if "statement_info" in st.session_state.keys():
            del st.session_state["statement_info"]
        if "filtros_extrato" in st.session_state:
            del st.session_state["filtros_extrato"]
        with st.spinner(f"Buscando informações do Extrato em {coin}"):
            st.session_state["coin_name"] = coin
            st.session_state["statement_info"] = Statement(coin)

    if "statement_info" in st.session_state.keys():
        if st.session_state["statement_info"].saldo > 0:
            make_transfer()
        st.markdown("---")
        st.markdown(
            "<h6 style='text-align: left';>FILTROS</h6>", unsafe_allow_html=True
        )
        c = st.columns([20, 20, 20, 40])
        if "filtros_extrato" not in st.session_state:
            st.session_state["statement_info"].mount_df()
        filtros = st.session_state.get("filtros_extrato", {})
        with c[0]:
            status = st.selectbox(
                label="STATUS",
                options=filtros.get("status", ["TODOS"]),
                index=0
            )
            status = None if status == "TODOS" else status
        with c[1]:
            origem = st.selectbox(
                label="ORIGEM",
                options=filtros.get("origin", ["TODOS"]),
                index=0
            )
            origem = None if origem == "TODOS" else origem
        with c[2]:
            tipo = st.selectbox(
                label="TIPO",
                options=filtros.get("type_transfer", ["TODOS"]),
                index=0
            )
            tipo = None if tipo == "TODOS" else tipo
        st.session_state["statement_info"].mount_df(
            status=status, origem=origem, tipo=tipo
        )
        st.session_state["statement_info"].show_info()
