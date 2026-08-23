import pytest
import os
from src.storage.chat_storage import (
    create_session,
    save_session,
    load_session,
    list_sessions,
    delete_session,
    rename_session
)
from src.storage.audit_storage import (
    save_audit,
    list_audits,
    get_audit,
    delete_audit
)

def test_chat_storage_lifecycle():
    # 1. Criar sessão
    sess_id = create_session(title="Conversa de Teste")
    assert sess_id.startswith("chat_")

    # 2. Carregar sessão
    sess_data = load_session(sess_id)
    assert sess_data is not None
    assert sess_data["title"] == "Conversa de Teste"
    assert len(sess_data["messages"]) > 0

    # 3. Salvar mensagens adicionais
    messages = sess_data["messages"] + [{"role": "user", "content": "Qual a CD de magia?"}]
    save_session(sess_id, messages=messages)
    
    updated_data = load_session(sess_id)
    assert len(updated_data["messages"]) == len(messages)

    # 4. Renomear
    rename_session(sess_id, "Novo Título Teste")
    assert load_session(sess_id)["title"] == "Novo Título Teste"

    # 5. Listar
    all_sess = list_sessions()
    assert any(s["id"] == sess_id for s in all_sess)

    # 6. Deletar
    assert delete_session(sess_id) is True
    assert load_session(sess_id) is None

def test_audit_storage_lifecycle():
    # 1. Salvar auditoria
    sample_report = (
        "# 📋 Relatório de Auditoria da Ficha: Thorgar Martelo de Ferro\n\n"
        "- **Classe e Subclasse:** Guerreiro Nível 3\n"
        "### ⚠️ Inconsistências & Correções Necessárias\n"
        "• Modificador de Força deveria ser +3 em vez de +2.\n"
    )
    
    audit_id = save_audit(
        filename="ficha_thorgar.pdf",
        report=sample_report,
        user_notes="Teste automatizado",
        file_type="pdf"
    )
    assert audit_id.startswith("audit_")

    # 2. Obter auditoria
    audit_data = get_audit(audit_id)
    assert audit_data is not None
    assert "Thorgar" in audit_data["character_name"]
    assert "Guerreiro" in audit_data["class_level"]

    # 3. Listar auditorias
    all_audits = list_audits()
    assert any(a["id"] == audit_id for a in all_audits)

    # 4. Deletar auditoria
    assert delete_audit(audit_id) is True
    assert get_audit(audit_id) is None
