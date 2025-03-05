import json
import sqlite3
import streamlit as st

class DictCache:
    def __init__(self, ttl=30):
        """
        Inicializa um banco de dados SQLite em memória.
        
        :param ttl: Tempo de expiração dos dados em segundos (padrão: 30s).
        """
        self.ttl = ttl
        self.conn = sqlite3.connect(':memory:', check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE cache (
                key TEXT PRIMARY KEY,
                data TEXT,
                ttl INTEGER
            )
        """)
    
    def save(self, key: str, value: str):
        """
        Salva um dicionário no cache SQLite em memória.
        
        :param key: Chave do cache.
        :param value: String formatada como "installation_id:account_number:pubkey:certified_account".
        """
        if not isinstance(key, str):
            raise ValueError("A chave deve ser uma string.")
        if not isinstance(value, str):
            raise ValueError("O valor deve ser uma string no formato esperado.")

        values = value.split(":")
        if len(values) < 4:
            raise ValueError("O valor deve conter exatamente 4 partes separadas por ':'.")

        dicio = {
            'installation_id': values[0],
            'account_number': values[1],
            'pubkey': values[2],
            'certified_account': values[3].lower() == "true"
        }

        self.cursor.execute("""
            INSERT OR REPLACE INTO cache (key, data, ttl) 
            VALUES (?, ?, ?)
        """, (key, json.dumps(dicio), self.ttl))
        self.conn.commit()

    def get(self, key: str):
        """
        Obtém um dicionário do cache SQLite em memória.
        
        :param key: Chave do cache.
        :return: O dicionário armazenado ou None se não existir.
        """
        self.cursor.execute("SELECT data FROM cache WHERE key=?", (key,))
        result = self.cursor.fetchone()
        if result:
            return json.loads(result[0])
        else:
            return None
