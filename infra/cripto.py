import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

def decrypt_string(encrypted_text: str, key_md5: str) -> str:
    """Descriptografa uma string usando AES CBC e uma chave MD5 já fornecida."""
    key = key_md5[:32].encode()  # Garante que a chave tem 32 bytes
    encrypted_data = base64.b64decode(encrypted_text)  # Decodifica base64

    iv = encrypted_data[:16]  # Primeiro bloco é o IV
    cipher_text = encrypted_data[16:]  # Resto é o conteúdo criptografado

    cipher = AES.new(key, AES.MODE_CBC, iv)  # Inicializa AES com CBC
    decrypted = cipher.decrypt(cipher_text)  # Descriptografa

    return unpad(decrypted, AES.block_size).decode('utf-8')  # Remove padding corretamente

