import streamlit as st
from infra.cripto import decrypt_string
from infra.pages import Pages as pages
from infra.config import Config as config
from infra.redis import DictCache

config.initial_config()

code = st.query_params.get("code", None)
message = st.query_params.get("message", None)
if code and message:
    message = decrypt_string(encrypted_text=message, key=code)
    messages = message.split(':')
    cache = DictCache()
    cache.save(messages[0], ":".join(messages[1:]))

pages.exec()
