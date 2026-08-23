import pytest
import os
import json
from src.rag.pdf_ingest import clean_text, delete_pdf_book, CHUNKS_FILE

def test_clean_text():
    dirty = "Texto com quebras\n\nde linha e espaços   extras."
    cleaned = clean_text(dirty)
    assert "Texto com quebras" in cleaned
    assert "extras." in cleaned

def test_delete_pdf_book():
    # Testar exclusão de um livro fictício
    fake_book = "livro_teste_inexistente.pdf"
    res = delete_pdf_book(fake_book)
    assert res["success"] is True

def test_generate_sheet_pdf():
    from src.tools.pdf_exporter import generate_sheet_pdf
    
    mock_audit = {
        "character_name": "Magnus Brutus",
        "class_level": "Guerreiro (Campeão) Nível 5",
        "filename": "ficha_magnus.pdf",
        "created_at": "2026-08-23T12:00:00",
        "has_issues": False,
        "report": (
            "### 📋 Relatório de Auditoria da Ficha: Magnus Brutus\n\n"
            "**Classe e Nível:** Guerreiro 5\n\n"
            "### 1. Atributos e Salvaguardas\n"
            "| Atributo | Valor | Modificador | Salvaguarda |\n"
            "| :--- | :--- | :--- | :--- |\n"
            "| FOR | 18 | +4 | +7 (Proficiente + Capa) |\n"
            "| DES | 14 | +2 | +3 (Capa) |\n\n"
            "> [!NOTE]\n"
            "> Ficha 100% regular de acordo com o Livro do Jogador 2024.\n"
        ),
        "extracted_data": {
            "ability_scores": {
                "str": 18, "dex": 14, "con": 16, "int": 10, "wis": 12, "cha": 8
            },
            "saving_throws": {
                "str": "+7", "dex": "+3", "con": "+6", "int": "+1", "wis": "+2", "cha": "+0"
            }
        }
    }
    
    pdf_bytes = generate_sheet_pdf(mock_audit)
    assert pdf_bytes is not None
    assert len(pdf_bytes) > 500
    assert pdf_bytes.startswith(b"%PDF")

