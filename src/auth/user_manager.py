import os
import sqlite3
import re
from datetime import datetime
from typing import Dict, Any, Optional, Tuple, List

from .security import (
    hash_password,
    verify_password,
    encrypt_api_key,
    decrypt_api_key
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "users.db")
USERS_DIR = os.path.join(DATA_DIR, "users")

def _get_connection(db_path: Optional[str] = None) -> sqlite3.Connection:
    target_path = db_path or DB_PATH
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    conn = sqlite3.connect(target_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(db_path: Optional[str] = None):
    """Inicializa a tabela de usuários caso não exista."""
    conn = _get_connection(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                encrypted_api_key TEXT DEFAULT '',
                is_admin INTEGER DEFAULT 0,
                created_at TEXT NOT NULL
            )
        """)
        conn.commit()
    finally:
        conn.close()

# Inicializar banco na importação
init_db()

def _ensure_user_directories(username: str):
    """Cria os diretórios privados de chat e auditoria do usuário."""
    clean_user = username.strip().lower()
    user_root = os.path.join(USERS_DIR, clean_user)
    os.makedirs(os.path.join(user_root, "chat_history"), exist_ok=True)
    os.makedirs(os.path.join(user_root, "audit_history"), exist_ok=True)

def _is_env_admin(username: str) -> bool:
    """Verifica se o usuário está listado na variável de ambiente ADMIN_USERNAMES."""
    admin_env = os.getenv("ADMIN_USERNAMES", "")
    admins = [u.strip().lower() for u in admin_env.split(",") if u.strip()]
    return username.strip().lower() in admins

def register_user(
    username: str,
    password: str,
    name: str = "",
    gemini_api_key: str = "",
    db_path: Optional[str] = None
) -> Tuple[bool, str]:
    """
    Registra um novo usuário no sistema.
    O primeiro usuário registrado é automaticamente promovido a Administrador / Mestre.
    """
    clean_username = username.strip().lower()
    clean_name = name.strip() or clean_username.capitalize()
    
    if len(clean_username) < 3:
        return False, "O nome de usuário deve ter pelo menos 3 caracteres."
        
    if not re.match(r'^[a-z0-9_.-]+$', clean_username):
        return False, "O usuário deve conter apenas letras, números, ponto, hífen ou sublinhado."
        
    if len(password) < 6:
        return False, "A senha deve ter no mínimo 6 caracteres."

    conn = _get_connection(db_path)
    try:
        cursor = conn.cursor()
        
        # Verificar se usuário já existe
        cursor.execute("SELECT id FROM users WHERE username = ?", (clean_username,))
        if cursor.fetchone() is not None:
            return False, f"O usuário '{clean_username}' já está em uso. Escolha outro."
            
        # Verificar se é o primeiro usuário do sistema ou se está na env ADMIN_USERNAMES
        cursor.execute("SELECT COUNT(*) as cnt FROM users")
        total_users = cursor.fetchone()["cnt"]
        is_admin = 1 if (total_users == 0 or _is_env_admin(clean_username)) else 0
        
        # Criptografar senha e chave de API
        pwd_hash, salt = hash_password(password)
        enc_api_key = encrypt_api_key(gemini_api_key)
        now_iso = datetime.now().isoformat()
        
        cursor.execute("""
            INSERT INTO users (username, name, password_hash, salt, encrypted_api_key, is_admin, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (clean_username, clean_name, pwd_hash, salt, enc_api_key, is_admin, now_iso))
        
        conn.commit()
        
        # Criar diretórios privados
        _ensure_user_directories(clean_username)
        
        role_msg = " (👑 Administrador / Mestre)" if is_admin else " (⚔️ Jogador)"
        return True, f"Conta criada com sucesso{role_msg}! Faça login para continuar."
    except Exception as e:
        return False, f"Erro ao registrar usuário: {str(e)}"
    finally:
        conn.close()

def authenticate_user(username: str, password: str, db_path: Optional[str] = None) -> Tuple[bool, Optional[Dict[str, Any]], str]:
    """
    Autentica o usuário com hash PBKDF2 e descriptografa sua chave de API em memória.
    """
    clean_username = username.strip().lower()
    if not clean_username or not password:
        return False, None, "Preencha o usuário e a senha."
        
    conn = _get_connection(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, username, name, password_hash, salt, encrypted_api_key, is_admin, created_at
            FROM users
            WHERE username = ?
        """, (clean_username,))
        row = cursor.fetchone()
        
        if not row:
            return False, None, "Usuário ou senha incorretos."
            
        if not verify_password(password, row["password_hash"], row["salt"]):
            return False, None, "Usuário ou senha incorretos."
            
        # Descriptografar chave do Gemini em memória
        decrypted_key = decrypt_api_key(row["encrypted_api_key"])
        
        # Garantir diretórios privados
        _ensure_user_directories(clean_username)
        
        is_admin_flag = bool(row["is_admin"]) or _is_env_admin(clean_username)
        
        user_data = {
            "id": row["id"],
            "username": row["username"],
            "name": row["name"],
            "gemini_api_key": decrypted_key,
            "is_admin": is_admin_flag,
            "created_at": row["created_at"]
        }
        return True, user_data, "Login realizado com sucesso!"
    except Exception as e:
        return False, None, f"Erro na autenticação: {str(e)}"
    finally:
        conn.close()

def update_user_api_key(username: str, new_api_key: str, db_path: Optional[str] = None) -> bool:
    """Atualiza e salva a chave de API do Gemini criptografada no banco."""
    clean_username = username.strip().lower()
    enc_key = encrypt_api_key(new_api_key)
    
    conn = _get_connection(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE users
            SET encrypted_api_key = ?
            WHERE username = ?
        """, (enc_key, clean_username))
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao atualizar chave do usuário {clean_username}: {e}")
        return False
    finally:
        conn.close()

def promote_to_admin(username: str, db_path: Optional[str] = None) -> bool:
    """Promove um usuário a Administrador / Mestre."""
    clean_username = username.strip().lower()
    conn = _get_connection(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET is_admin = 1 WHERE username = ?", (clean_username,))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()

def demote_from_admin(username: str, db_path: Optional[str] = None) -> bool:
    """Remove privilégios de Administrador de um usuário."""
    clean_username = username.strip().lower()
    conn = _get_connection(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET is_admin = 0 WHERE username = ?", (clean_username,))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()

def get_user_profile(username: str, db_path: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Obtém o perfil de um usuário."""
    clean_username = username.strip().lower()
    conn = _get_connection(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, name, encrypted_api_key, is_admin, created_at FROM users WHERE username = ?", (clean_username,))
        row = cursor.fetchone()
        if not row:
            return None
        return {
            "id": row["id"],
            "username": row["username"],
            "name": row["name"],
            "gemini_api_key": decrypt_api_key(row["encrypted_api_key"]),
            "is_admin": bool(row["is_admin"]) or _is_env_admin(clean_username),
            "created_at": row["created_at"]
        }
    finally:
        conn.close()

def count_users(db_path: Optional[str] = None) -> int:
    """Retorna o total de usuários registrados."""
    conn = _get_connection(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as cnt FROM users")
        return cursor.fetchone()["cnt"]
    finally:
        conn.close()
