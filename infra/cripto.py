import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from infra.config import Config as config

def decrypt_string(encrypted_text: str, key: str) -> str:
    encrypted_data = base64.b64decode(encrypted_text)  # Decodifica base64

    iv = encrypted_data[:16]  # Primeiro bloco é o IV
    cipher_text = encrypted_data[16:]  # Resto é o conteúdo criptografado

    cipher = AES.new(eval(config.PRIVATE_KEY), AES.MODE_CBC, iv)  # Inicializa AES com CBC
    decrypted = cipher.decrypt(cipher_text)  # Descriptografa

    return unpad(decrypted, AES.block_size).decode('utf-8')  # Remove padding corretamente
