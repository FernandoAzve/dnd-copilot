import pytest
import os
import shutil
from src.auth.security import (
    hash_password,
    verify_password,
    encrypt_api_key,
    decrypt_api_key
)
from src.auth.user_manager import (
    register_user,
    authenticate_user,
    update_user_api_key,
    get_user_profile,
    count_users
)
from src.storage.chat_storage import (
    create_session,
    list_sessions,
    load_session,
    delete_session
)
from src.storage.audit_storage import (
    save_audit,
    list_audits,
    get_audit,
    delete_audit
)

def test_cryptography_hashing_and_encryption():
    # 1. Teste de Senha
    pwd = "SenhaSecretaRPG@2024"
    pwd_hash, salt = hash_password(pwd)
    assert pwd_hash != pwd
    assert len(salt) == 64  # 32 bytes hex
    assert verify_password(pwd, pwd_hash, salt) is True
    assert verify_password("SenhaErrada", pwd_hash, salt) is False

    # 2. Teste de Criptografia de Chave de API
    raw_key = "AIzaSyDummyKeyForTestingDND12345"
    encrypted = encrypt_api_key(raw_key)
    assert encrypted != raw_key
    assert len(encrypted) > len(raw_key)
    decrypted = decrypt_api_key(encrypted)
    assert decrypted == raw_key

def test_user_registration_and_rbac():
    test_user_admin = "mestre_teste"
    test_user_player = "jogador_teste"

    # Registrar 1º usuário (será Admin se banco estiver vazio ou criado agora)
    ok1, msg1 = register_user(test_user_admin, "senha12345", "Mestre Teste", "key_admin_123")
    # Pode já existir de teste anterior, autenticar funciona
    auth_ok1, user_data1, _ = authenticate_user(test_user_admin, "senha12345")
    assert auth_ok1 is True
    assert user_data1["gemini_api_key"] == "key_admin_123"

    # Registrar 2º usuário
    ok2, msg2 = register_user(test_user_player, "senha12345", "Jogador Teste", "key_player_456")
    auth_ok2, user_data2, _ = authenticate_user(test_user_player, "senha12345")
    assert auth_ok2 is True
    assert user_data2["gemini_api_key"] == "key_player_456"
    assert user_data2["is_admin"] is False  # Segundo usuário não é admin

    # Teste de atualização de chave
    assert update_user_api_key(test_user_player, "new_key_player_789") is True
    updated_profile = get_user_profile(test_user_player)
    assert updated_profile["gemini_api_key"] == "new_key_player_789"

def test_multiuser_data_isolation():
    user_a = "user_alpha"
    user_b = "user_beta"

    register_user(user_a, "senha12345", "Alpha")
    register_user(user_b, "senha12345", "Beta")

    # 1. Isolamento de Chat
    sess_a = create_session(title="Aventura de Alpha", username=user_a)
    sess_b = create_session(title="Aventura de Beta", username=user_b)

    sessions_for_a = list_sessions(username=user_a)
    sessions_for_b = list_sessions(username=user_b)

    assert any(s["id"] == sess_a for s in sessions_for_a)
    assert not any(s["id"] == sess_b for s in sessions_for_a)

    assert any(s["id"] == sess_b for s in sessions_for_b)
    assert not any(s["id"] == sess_a for s in sessions_for_b)

    # 2. Isolamento de Auditoria de Fichas
    audit_a = save_audit(
        filename="ficha_alpha.pdf",
        report="# Ficha de Alpha\n- Classe: Bárbaro",
        username=user_a
    )
    audit_b = save_audit(
        filename="ficha_beta.pdf",
        report="# Ficha de Beta\n- Classe: Mago",
        username=user_b
    )

    audits_for_a = list_audits(username=user_a)
    audits_for_b = list_audits(username=user_b)

    assert any(a["id"] == audit_a for a in audits_for_a)
    assert not any(a["id"] == audit_b for a in audits_for_a)

    assert any(a["id"] == audit_b for a in audits_for_b)
    assert not any(a["id"] == audit_a for a in audits_for_b)

    # Limpeza
    delete_session(sess_a, username=user_a)
    delete_session(sess_b, username=user_b)
    delete_audit(audit_a, username=user_a)
    delete_audit(audit_b, username=user_b)
