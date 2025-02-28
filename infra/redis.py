import fakeredis

class RedisInMemory:
    def __init__(self):
        """Inicializa um Redis fake que roda somente em memória."""
        self.client = fakeredis.FakeRedis(decode_responses=True)
    
    def set(self, key, value):
        """Define um valor para uma chave no Redis."""
        self.client.set(key, value)
    
    def get(self, key):
        """Obtém o valor de uma chave no Redis."""
        return self.client.get(key)
    