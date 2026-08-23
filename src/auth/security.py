import os
import secrets
import hashlib
import hmac
import base64
import time
from typing import Tuple, Optional
from cryptography.fernet import Fernet

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
SECRET_FILE = os.path.join(DATA_DIR, ".app_secret")

def _get_or_create_app_secret() -> bytes:
    """Obtém ou gera uma chave mestra persistente para criptografia simétrica AES-256."""
    env_secret = os.getenv("APP_SECRET_KEY")
    if env_secret:
        # Se fornecido via env, deriva chave de 32 bytes em base64
        key_bytes = hashlib.sha256(env_secret.encode("utf-8")).digest()
        return base64.urlsafe_b64encode(key_bytes)
        
    os.makedirs(DATA_DIR, exist_ok=True)
    if os.path.exists(SECRET_FILE):
        try:
            with open(SECRET_FILE, "rb") as f:
                key = f.read().strip()
                if key:
                    return key
        except Exception:
            pass

    # Gerar nova chave Fernet válida
    new_key = Fernet.generate_key()
    try:
        with open(SECRET_FILE, "wb") as f:
            f.write(new_key)
    except Exception as e:
        print(f"Aviso: Não foi possível salvar .app_secret: {e}")
    return new_key

def hash_password(password: str) -> Tuple[str, str]:
    """
    Gera um hash PBKDF2-HMAC-SHA256 irreversível com 100.000 iterações e salt aleatório de 32 bytes.
    Retorna (hash_hex, salt_hex).
    """
    if not password:
        raise ValueError("A senha não pode ser vazia.")
        
    salt = secrets.token_hex(32)
    pwd_bytes = password.encode("utf-8")
    salt_bytes = salt.encode("utf-8")
    
    hash_bytes = hashlib.pbkdf2_hmac("sha256", pwd_bytes, salt_bytes, 100000)
    return hash_bytes.hex(), salt

def verify_password(password: str, stored_hash: str, salt: str) -> bool:
    """Verifica se a senha informada corresponde ao hash com salt de forma segura contra timing attacks."""
    if not password or not stored_hash or not salt:
        return False
        
    pwd_bytes = password.encode("utf-8")
    salt_bytes = salt.encode("utf-8")
    
    calculated_hash = hashlib.pbkdf2_hmac("sha256", pwd_bytes, salt_bytes, 100000).hex()
    return hmac.compare_digest(calculated_hash, stored_hash)

def encrypt_api_key(api_key: str) -> str:
    """Criptografa a chave de API do Gemini com AES-256 (Fernet)."""
    if not api_key or not api_key.strip():
        return ""
    try:
        cipher = Fernet(_get_or_create_app_secret())
        encrypted_bytes = cipher.encrypt(api_key.strip().encode("utf-8"))
        return encrypted_bytes.decode("utf-8")
    except Exception as e:
        print(f"Erro ao criptografar chave: {e}")
        return ""

def decrypt_api_key(encrypted_key: str) -> str:
    """Descriptografa a chave de API do Gemini em memória."""
    if not encrypted_key or not encrypted_key.strip():
        return ""
    try:
        cipher = Fernet(_get_or_create_app_secret())
        decrypted_bytes = cipher.decrypt(encrypted_key.strip().encode("utf-8"))
        return decrypted_bytes.decode("utf-8")
    except Exception as e:
        print(f"Erro ao descriptografar chave: {e}")
        return ""

def create_session_token(username: str) -> str:
    """Gera um token de sessão assinado e criptografado com AES-256 para persistência no navegador."""
    clean_user = username.strip().lower()
    payload = f"{clean_user}:{int(time.time())}"
    cipher = Fernet(_get_or_create_app_secret())
    return cipher.encrypt(payload.encode("utf-8")).decode("utf-8")

def validate_session_token(token: str, max_age_days: int = 14) -> Optional[str]:
    """Valida o token de sessão e retorna o username se for válido e não expirado."""
    if not token or not token.strip():
        return None
    try:
        cipher = Fernet(_get_or_create_app_secret())
        decrypted = cipher.decrypt(token.strip().encode("utf-8")).decode("utf-8")
        username, timestamp_str = decrypted.split(":", 1)
        timestamp = int(timestamp_str)
        if time.time() - timestamp > (max_age_days * 86400):
            return None
        return username
    except Exception:
        return None
