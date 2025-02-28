import time
import requests
import streamlit as st
from infra.auth import generate_qr_code, generate_code, login

def login_page():
    c = st.columns([35, 30, 35])
    with c[1]:
        st.markdown(
            f'<h4 style="text-align: center;">Escaneie com seu aplicativo getBRAZA</h4>',
            unsafe_allow_html=True,
        )
        code = generate_code()
        st.markdown(
            '<div style="display: flex; justify-content: center;">',
            unsafe_allow_html=True
        )
        st.image(generate_qr_code(code))
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown(
            f'<h5 style="text-align: center;">{code.split(":")[1][:3]}-{code.split(":")[1][3:]}</h5>',
            unsafe_allow_html=True
        )
    contador = 0
    while True:
        installation_id = trigger(code)
        if installation_id:
            with st.spinner("Carregando dados da conta"):
                login(installation_id)
                break
        time.sleep(1)
        contador += 1
        if contador >= 30:
            st.rerun()
            break
    
    if "account" in st.session_state:
        st.rerun()

def trigger(code: str) -> str | None:
    # url ="http://lalaland.com"
    # temp = requests.post(url, json={"code": code})

    # if temp.status_code == 200:
    #     res = temp.json()
    # else:
    #     res = None

    res = None

    if res:
        return res.get("installation_id", None)
    else:
        return None
