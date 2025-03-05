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
        :param key: Chave do cache.
        :param value: Dicionário a ser armazenado.
        """
        if not isinstance(key, str):
            raise ValueError("A chave deve ser uma string.")
        if not isinstance(value, str):
            raise ValueError("O valor deve ser um dicionário.")
        self.cache[key] = value
    
    def get(self, key: str):
        """
        Obtém um dicionário do cache através da chave.
        :param key: Chave do cache.
        :return: O dicionário armazenado ou None se não existir.
        """
        return self.cache.get(key, None)
    