import pytest
import os
import shutil
from src.storage.character_storage import (
    get_default_character_data,
    save_character,
    get_character,
    list_characters,
    delete_character,
    get_active_character_id,
    set_active_character_id,
    format_character_context
)
from src.tools.character_importer import extract_and_build_character_from_file

TEST_USER = "test_user_char_storage"

@pytest.fixture(autouse=True)
def cleanup_test_user():
    yield
    from src.storage.character_storage import USERS_ROOT
    test_dir = os.path.join(USERS_ROOT, TEST_USER)
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir, ignore_errors=True)

def test_character_crud_and_active_context():
    # 1. Testar template padrão limpo e neutro
    default_data = get_default_character_data()
    assert default_data["name"] == ""
    assert "abilities" in default_data
    
    # 2. Criar personagem de teste (Magnus Brutus)
    char_data = get_default_character_data()
    char_data["name"] = "Magnus Brutus"
    char_data["class_name"] = "Guerreiro"
    char_data["subclass"] = "Campeão"
    char_data["level"] = 5
    char_data["abilities"] = {
        "str": 18, "dex": 14, "con": 16, "int": 10, "wis": 12, "cha": 8
    }
    char_data["saving_throw_proficiencies"] = ["str", "con"]
    char_data["attacks"] = [
        {"name": "Espada Longa", "attack_bonus": "+7", "damage": "1d8+4", "damage_type": "Cortante", "mastery": "Empurrão (Push)", "notes": "Versátil"}
    ]
    char_data["magic_items"] = ["Capa de Proteção"]
    char_data["features_and_traits"] = "Segundo Fôlego, Surto de Ação, Crítico Aprimorado (19-20)"
    
    char_id = save_character(char_data, username=TEST_USER)
    assert char_id.startswith("char_")
    
    # 3. Recuperar e verificar se foi salvo
    retrieved = get_character(char_id, username=TEST_USER)
    assert retrieved is not None
    assert retrieved["name"] == "Magnus Brutus"
    assert retrieved["abilities"]["str"] == 18
    assert retrieved["level"] == 5
    
    # 4. Listar personagens
    all_chars = list_characters(username=TEST_USER)
    assert len(all_chars) == 1
    assert all_chars[0]["name"] == "Magnus Brutus"
    
    # 5. Ativar personagem e formatar contexto
    set_active_character_id(char_id, username=TEST_USER)
    assert get_active_character_id(username=TEST_USER) == char_id
    
    context_str = format_character_context(retrieved)
    assert "Magnus Brutus" in context_str
    assert "Guerreiro" in context_str
    assert "FOR 18 (+4)" in context_str
    assert "Espada Longa" in context_str
    assert "Empurrão" in context_str
    assert "Capa de Proteção" in context_str
    
    # 6. Excluir personagem
    deleted = delete_character(char_id, username=TEST_USER)
    assert deleted is True
    assert get_character(char_id, username=TEST_USER) is None
    assert len(list_characters(username=TEST_USER)) == 0
    assert get_active_character_id(username=TEST_USER) == ""

def test_character_importer_from_pdf():
    pdf_path = "ficha_magnus_V2_atualizado.pdf"
    if os.path.exists(pdf_path):
        with open(pdf_path, "rb") as f:
            pdf_bytes = f.read()
        char_data = extract_and_build_character_from_file(file_bytes=pdf_bytes, filename=pdf_path, api_key="")
        assert char_data is not None
        assert "name" in char_data
        assert "abilities" in char_data
