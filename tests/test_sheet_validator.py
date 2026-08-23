import pytest
from src.tools.sheet_validator import (
    SheetValidator,
    SHEET_AUDITOR_PROMPT,
    _detect_item_save_bonus,
    _parse_signed_int,
    CLASS_CANONICAL_DATA
)

def test_sheet_validator_init():
    validator = SheetValidator(api_key="")
    assert "Auditor Mestre Oficial de Fichas" in SHEET_AUDITOR_PROMPT
    assert "Matriz de Auditoria de Atributos" in SHEET_AUDITOR_PROMPT
    assert "Bônus de Proficiência" in SHEET_AUDITOR_PROMPT
    assert "Livro do Jogador" in SHEET_AUDITOR_PROMPT

def test_sheet_validator_no_key():
    validator = SheetValidator(api_key="")
    res = validator.validate_sheet_file(
        file_bytes=b"dummy",
        filename="ficha.pdf",
        mime_type="application/pdf"
    )
    assert res["success"] is False
    assert "GEMINI_API_KEY" in res["report"]

def test_item_bonus_and_saving_throw_detection():
    # 1. Teste de detecção de Capa de Proteção
    data_with_cape = {
        "magic_items": ["Cloth of Protection"],
        "feats_and_traits": ["Fighting Style"]
    }
    assert _detect_item_save_bonus(data_with_cape) == 1

    data_without_item = {
        "magic_items": ["Tocha", "Corda"],
        "feats_and_traits": []
    }
    assert _detect_item_save_bonus(data_without_item) == 0

    # 2. Teste de parser de inteiros com sinal
    assert _parse_signed_int("+8") == 8
    assert _parse_signed_int("+2") == 2
    assert _parse_signed_int("0") == 0
    assert _parse_signed_int("-1") == -1

    # 3. Teste de salvaguardas canônicas
    warrior_saves = CLASS_CANONICAL_DATA["guerreiro"]["saves"]
    assert "Força" in warrior_saves
    assert "Constituição" in warrior_saves
    assert "Destreza" not in warrior_saves
