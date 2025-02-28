import dotenv
import warnings
import streamlit as st
from os import getenv

dotenv.load_dotenv()

class Config:
    NAMESPACE = "getbraza-bonu"
    MONGO_URI = getenv("MONGO_URI")
    REDIS_URL = getenv("REDIS_URL")
    REDIS_PORT = getenv("REDIS_PORT")

    DEVICE_ENDPOINT = getenv("DEVICE_ENDPOINT")
    STATEMENT_ENDPOINT = getenv("STATEMENT_ENDPOINT")
    COINS_ENDPOINT = getenv("COINS_ENDPOINT")

    @staticmethod
    def initial_config():
        warnings.simplefilter("ignore")
        st.set_page_config(layout="wide", page_icon="assets/B-rosa.png")
        st.image("assets/getBRAZA.png", width=200)
