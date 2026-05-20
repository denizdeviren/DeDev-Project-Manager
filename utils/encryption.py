import base64
import hashlib

def encrypt_text(text, password):
    if not text or not password:
        return text
    key = hashlib.sha256(password.encode('utf-8')).digest()
    text_bytes = text.encode('utf-8')
    encrypted = bytearray()
    for i, b in enumerate(text_bytes):
        encrypted.append(b ^ key[i % len(key)])
    return base64.b64encode(encrypted).decode('utf-8')

def decrypt_text(encrypted_text, password):
    if not encrypted_text or not password:
        return encrypted_text
    try:
        key = hashlib.sha256(password.encode('utf-8')).digest()
        encrypted_bytes = base64.b64decode(encrypted_text.encode('utf-8'))
        decrypted = bytearray()
        for i, b in enumerate(encrypted_bytes):
            decrypted.append(b ^ key[i % len(key)])
        return decrypted.decode('utf-8')
    except Exception:
        return "ERROR_WRONG_PASSWORD"
