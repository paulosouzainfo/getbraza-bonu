import json
import fakeredis
import streamlit as st

class DictCache:
    def __init__(self, ttl=30):
        """
        Inicializa um Redis fake que roda somente em memória.
        
        :param ttl: Tempo de expiração dos dados em segundos (padrão: 30s).
        """
        self.client = fakeredis.FakeRedis(decode_responses=True)  # Aqui, altere para conectar-se a um Redis real
        self.ttl = ttl
    
    def save(self, key: str, value: str):
        """
        Salva um dicionário no cache Redis e exibe um feedback no Streamlit.
        
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

        try:
            key = key.replace('-', '')
            # Salva no Redis e define TTL
            self.client.setex(key, self.ttl, json.dumps(dicio))
        except Exception as e:
            pass

    def get(self, key: str):
        """
        Obtém um dicionário do cache Redis.
        
        :param key: Chave do cache.
        :return: O dicionário armazenado ou None se não existir.
        """
        # Obtém o valor do Redis
        key = key.replace('-', '')
        data = self.client.get(key)
        if data:
            return json.loads(data)
        else:
            return None
