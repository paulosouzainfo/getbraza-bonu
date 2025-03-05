import time
import hashlib
import base64
from io import BytesIO
import streamlit as st
from infra.auth import generate_qr_code, generate_code, login
from infra.cripto import decrypt_with_rsa
from infra.config import Config as config
from infra.cachetools import DictCache

def get_image_base64(image_bytesio):
    """Converte um BytesIO em uma string base64"""
    return base64.b64encode(image_bytesio.getvalue()).decode("utf-8")

def login_page():
    code = st.query_params.get("code", None)
    if code:
        code = decrypt_with_rsa(code, hashlib.md5(code.encode()).hexdigest())
        st.write(code)
        cache = DictCache()
        code = code.split(':')
        cache.set(code[0], ':'.join(code[1:]))

    c = st.columns([35, 30, 35])
    with c[0]:
        st.markdown(
            """
            <style>
                ol li::marker {
                    font-weight: bold;
                }
            </style>
            <div></br>
                <p style="text-align: justify; font-weight: bold;">
                Use o seu aplicativo para poder acessar suas informações através do seu navegador
                </p>
                <ol>
                    <li>Abra seu aplicativo getBRAZA;</li>
                    <li>Clique em <b>"AJUSTES"</b>;</li>
                    <li>Em <b>"CONECTAR DISPOSITIVOS"</b>, clique em <b>"ESCANEAR"</b> e aponte a câmera do seu celular para o código QR que aparece ao lado.</li>
                </ol>
            </div>
            """,
            unsafe_allow_html=True
        )
    with c[1]:
        code = generate_code()
        qr_image = generate_qr_code(code)
        qr_base64 = get_image_base64(qr_image)
        st.markdown(
            f"""
            <div style="display: flex; justify-content: center;">
                <img src="data:image/png;base64,{qr_base64}" width="200">
            </div>
            """,
            unsafe_allow_html=True
        )
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
    try:
        cache = DictCache()
        res = cache.get(code)
    except:
        res = None

    if res:
        return res.get("installation_id", None)
    else:
        return None
