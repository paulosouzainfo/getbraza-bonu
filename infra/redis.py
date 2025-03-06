import json
import sqlite3
import time

class DictCache:
    def __init__(self, db_path="temp.db", ttl=30):
        """
        Inicializa um banco de dados SQLite.

        :param db_path: Caminho do banco de dados SQLite.
        :param ttl: Tempo de expiração dos dados em segundos (padrão: 30s).
        """
        self.ttl = ttl
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS cache (
                key TEXT PRIMARY KEY,
                data TEXT NOT NULL,
                expires_at INTEGER NOT NULL
            )
        """)
        self.conn.commit()  # Garante que a tabela seja criada

    def save(self, key: str, value: str):
        """
        Salva um dicionário no cache SQLite.

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

        expires_at = int(time.time()) + self.ttl  # Calcula o timestamp de expiração
        key = key.replace('-', '')
        self.cursor.execute("""
            INSERT OR REPLACE INTO cache (key, data, expires_at) 
            VALUES (?, ?, ?)
        """, (key, json.dumps(dicio), expires_at))
        self.conn.commit()

    def get(self, key: str):
        """
        Obtém um dicionário do cache SQLite, verificando se não está expirado.
        Se o registro estiver expirado, ele é removido do banco.

        :param key: Chave do cache.
        :return: O dicionário armazenado ou None se não existir ou estiver expirado.
        """
        now = int(time.time())

        # Apaga todos os registros expirados antes de buscar
        self.cursor.execute("DELETE FROM cache WHERE expires_at <= ?", (now,))
        self.conn.commit()

        self.cursor.execute("SELECT data FROM cache WHERE key=? AND expires_at > ?", (key, now))
        result = self.cursor.fetchone()
        if result:
            return json.loads(result[0])
        return None

    def delete(self, key: str):
        """
        Remove um item do cache com a chave informada.

        :param key: Chave do cache.
        """
        self.cursor.execute("DELETE FROM cache WHERE key=?", (key,))
        self.conn.commit()
