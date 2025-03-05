import cachetools

class DictCache:
    def __init__(self, max_size=100, ttl=30):
        """
        Inicializa o cache com um tamanho máximo e um tempo de expiração (TTL).
        
        :param max_size: Número máximo de itens no cache.
        :param ttl: Tempo de vida dos itens no cache, em segundos.
        """
        self.cache = cachetools.TTLCache(maxsize=max_size, ttl=ttl)

    def save(self, key: str, value: str):
        """
        Salva um dicionário no cache com a chave especificada.

        :param key: Chave do cache (deve ser uma string).
        :param value: String formatada como "installation_id:account_number:pubkey:certified_account".
        """
        if not isinstance(key, str):
            raise ValueError("A chave deve ser uma string.")
        if not isinstance(value, str):
            raise ValueError("O valor deve ser uma string no formato esperado.")

        values = value.split(":")
        import streamlit as st
        st.write(values)
        if len(values) < 4:
            raise ValueError("O valor deve conter exatamente 4 partes separadas por ':'.")

        dicio = {
            'installation_id': values[0],
            'account_number': values[1],
            'pubkey': values[2],
            'certified_account': values[3].lower() == "true"
        }

        self.cache[key.replace('-', '')] = dicio

    def get(self, key: str):
        """
        Obtém um dicionário do cache através da chave.

        :param key: Chave do cache.
        :return: O dicionário armazenado ou None se não existir.
        """
        return self.cache.get(key)
