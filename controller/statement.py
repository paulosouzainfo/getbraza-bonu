import requests  # type: ignore
import pandas as pd
import streamlit as st
from typing import Optional
from infra.config import Config as config

from schemas.person import Person

class Statement:
    def __init__(self, coin: str) -> None:
        self.coin: str = coin.upper().strip()
        self.statement: pd.DataFrame = pd.DataFrame()
        self.df: pd.DataFrame = pd.DataFrame()
        self.saldo: float = 0
        self.__get_statement()

    def __get_statement(self) -> None:
        conta: Person = st.session_state["account"]
        if conta.pubkey:
            headers = {
                "x-account-number": conta.account_number,
                "x-application-id": conta.application_id,
                "x-api-key": conta.pubkey,
                "x-coin-name": self.coin,
            }

            res = requests.get(
                url=config.STATEMENT_ENDPOINT, headers=headers, timeout=10
            )

            if res.status_code != 200:
                st.error(
                    f"STATUS CODE: {res.status_code} - Não foi possível obter o extrato do cliente"
                )
            else:
                res = res.json()
                self.saldo = res.get("balance", -1)
                statement = res.get("transactions", None)
                if statement:
                    statement = pd.DataFrame(statement)
                    colunas = [
                        "updated_at",
                        "coin_name",
                        "amount",
                        "brl_value",
                        "status",
                        "origin",
                        "to_account_number",
                        "from_account_number",
                        "type_transfer",
                    ]
                    filtro_colunas = []
                    for item in colunas:
                        if item in statement.columns:
                            filtro_colunas.append(item)
                    statement = statement[filtro_colunas]

                    status_dict = {
                        'expired': 'Expirado', 
                        'paid': 'Pago', 
                        'rejected': 'Rejeitado', 
                        'pending': 'Pendente'
                    }

                    statement['status'] = statement['status'].map(status_dict).fillna("Erro")

                    origin_dict = {
                        "transfer": "Transferência",
                        "pix": "Pix",
                        "transaction": "Saque"
                    }
                    statement["origin"] = statement["origin"].map(origin_dict)

                    self.statement = statement

    def mount_df(
            self, 
            status: Optional[str] = None,
            origem: Optional[str] = None,
            tipo: Optional[str] = None
    ) -> None:
        df = self.statement
        # FILTROS
        if "filtros_extrato" in st.session_state:
            del st.session_state["filtros_extrato"]
        st.session_state["filtros_extrato"] = {}
        if "status" in df.columns:
            st.session_state["filtros_extrato"]["status"] = ["TODOS"] + df["status"].unique().tolist()
        if "origin" in df.columns:
            st.session_state["filtros_extrato"]["origin"] = ["TODOS"] + df["origin"].unique().tolist()
        if "type_transfer" in df.columns:
            st.session_state["filtros_extrato"]["type_transfer"] = ["TODOS"] + df["type_transfer"].unique().tolist()

        if status and "status" in df.columns:
            df = df.query("status == @status")
        if origem and "origin" in df.columns:
            df = df.query("origin == @origem")
        if tipo and "type_transfer" in df.columns:
            df = df.query("type_transfer  == @tipo")
        self.df = df

    def show_info(self) -> None:
        st.info(f"Saldo: {self.saldo} {self.coin}")
        st.markdown(
            f"<h2>EXTRATO {self.coin}",
            unsafe_allow_html=True,
        )
        df = self.df
        if not df.empty:
            df["updated_at"] = pd.to_datetime(df["updated_at"]).dt.strftime("%d/%m/%Y %H:%M:%S")
            if "coin_name" in df.columns:
                df = df.drop(columns="coin_name")

            colunas = {
                "updated_at": "Data", 
                "amount": f"Valor {self.coin}", 
                "brl_value": "valor BRL pago",
                "status": "Status", 
                "origin": "Origem",
                "to_account_number": "Conta destino", 
                "from_account_number": "Conta origem",
                "type_transfer": "Tipo"
            }
            df = df.rename(columns=colunas)
        st.dataframe(df, use_container_width=True)
