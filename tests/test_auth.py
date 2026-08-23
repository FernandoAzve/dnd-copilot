import pytest
import os
import tempfile
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
    init_db
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

@pytest.fixture
def temp_test_db(tmp_path):
    db_file = str(tmp_path / "test_users.db")
    init_db(db_file)
    return db_file

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

def test_user_registration_and_rbac(temp_test_db):
    test_user_admin = "mestre_unit_test"
    test_user_player = "jogador_unit_test"

    # Registrar 1º usuário no banco temporário (será Admin)
    ok1, msg1 = register_user(test_user_admin, "senha12345", "Mestre Teste", "key_admin_123", db_path=temp_test_db)
    assert ok1 is True
    
    auth_ok1, user_data1, _ = authenticate_user(test_user_admin, "senha12345", db_path=temp_test_db)
    assert auth_ok1 is True
    assert user_data1["gemini_api_key"] == "key_admin_123"
    assert user_data1["is_admin"] is True

    # Registrar 2º usuário no mesmo banco temporário (será Jogador)
    ok2, msg2 = register_user(test_user_player, "senha12345", "Jogador Teste", "key_player_456", db_path=temp_test_db)
    assert ok2 is True
    
    auth_ok2, user_data2, _ = authenticate_user(test_user_player, "senha12345", db_path=temp_test_db)
    assert auth_ok2 is True
    assert user_data2["gemini_api_key"] == "key_player_456"
    assert user_data2["is_admin"] is False  # Segundo usuário não é admin

    # Teste de atualização de chave
    assert update_user_api_key(test_user_player, "new_key_player_789", db_path=temp_test_db) is True
    updated_profile = get_user_profile(test_user_player, db_path=temp_test_db)
    assert updated_profile["gemini_api_key"] == "new_key_player_789"

def test_multiuser_data_isolation(temp_test_db):
    user_a = "user_alpha_test"
    user_b = "user_beta_test"

    register_user(user_a, "senha12345", "Alpha", db_path=temp_test_db)
    register_user(user_b, "senha12345", "Beta", db_path=temp_test_db)

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
