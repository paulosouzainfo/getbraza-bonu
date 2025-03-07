import streamlit as st
from infra.cripto import decrypt_string
from infra.pages import Pages as pages
from infra.config import Config as config
from infra.redis import DictCache

config.initial_config()

pages.exec()
