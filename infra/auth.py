import requests
import random
import string
import qrcode
import streamlit as st
from io import BytesIO
from typing import Optional
from infra.config import Config as config

from schemas.person import Person

def get_pubkey(application_id: str = None) -> Optional[dict | None]:
    if application_id:
        payload = {"installation_id": application_id}
        res = requests.post(config.DEVICE_ENDPOINT, json=payload, timeout=10)

        if res.status_code != 200:
            st.error(
                f"STATUS CODE: {res.status_code} - Não foi possível obter a chave do cliente"
            )
            return None
        else:
            return res.json()
    else:
        return None

def generate_code() -> str:
    caracteres = string.ascii_letters + string.digits
    res = ''.join(random.choices(caracteres, k=6))
    return f"getBRAZA:{res.upper()}"

def generate_qr_code(code: str):
    qr = qrcode.make(code)
    
    # Salva a imagem em memória
    img_buffer = BytesIO()
    qr.save(img_buffer, format="PNG")
    img_buffer.seek(0)  # Move o cursor para o início do buffer
    
    return img_buffer  # Retorna a imagem no formato BytesIO

def login(installation_id: str):
    res = get_pubkey(installation_id)
    if res:
        person = {
            "application_id": installation_id,
            "pubkey": res.get("pubkey"),
            "account_number": res.get("account_number"),
            "static_qr_code_img": res.get("static_qr_code_img"),
            "wallet": res.get("wallet")
        }
        st.session_state["account"] = Person(**person)
