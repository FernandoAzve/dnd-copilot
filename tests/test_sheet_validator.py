import pytest
from src.tools.sheet_validator import SheetValidator, SHEET_AUDITOR_PROMPT

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
