import asyncio
from controller.statement import Statement
from time import sleep
import streamlit as st
from controller.getbraza import GetBrazaAsyncClient as getbraza

def make_transfer():
    with st.form("TRANSFER", clear_on_submit=True):
        st.markdown(
            "<h6 style='text-align: left';>TRANSFERÊNCIA</h6>", unsafe_allow_html=True
        )
        c = st.columns([20, 20, 20, 20, 20])
        with c[0]:
            account_number = st.text_input(label="account_number", label_visibility="hidden", placeholder="CONTA DE DESTINO")
        with c[1]:
            amount = st.number_input(label="amount", label_visibility="hidden", placeholder="VALOR", min_value=0.0)
        coin_name = st.session_state["coin_name"]
        with c[2]:
            st.markdown(
                '<div style="display: flex; justify-content: center; height: 28px">',
                unsafe_allow_html=True
            )
            transfer_form = st.form_submit_button("ENVIAR")
            st.markdown('</div>', unsafe_allow_html=True)

    if transfer_form:
        temp = getbraza(
            application_id=st.session_state["account"].application_id,
            api_key=st.session_state["account"].pubkey,
            account_number=st.session_state["account"].account_number
        )
        transfer_data = {
            "to_account_number": account_number,
            "amount": amount,
            "coin_name": coin_name,
        }
        asyncio.run(temp.internal_transfer(transfer_data))
        with st.spinner("Enviando e atualizando..."):
            del st.session_state["statement_info"]
            st.session_state["statement_info"] = Statement(st.session_state["coin_name"])
        st.rerun()
