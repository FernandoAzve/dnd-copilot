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
