import pytest
from src.tools.spell_lookup import lookup_spell
from src.tools.rules_lookup import lookup_rule, lookup_condition, lookup_glossary
from src.tools.character_calc import calculate_ability_modifier, calculate_proficiency_bonus, calculate_spell_stats
from src.rag.vector_store import DnDKnowledgeBase

def test_lookup_spell_pt_and_en():
    res_pt = lookup_spell("Bola de Fogo")
    assert res_pt["found"] is True
    assert res_pt["spell"]["level"] == 3

    res_en = lookup_spell("Fireball")
    assert res_en["found"] is True
    assert res_en["spell"]["name_pt"] == "Bola de Fogo"

def test_lookup_condition():
    res = lookup_condition("Caído")
    assert res["found"] is True
    assert "Prone" in res["condition"]["name_en"]

def test_lookup_glossary():
    res = lookup_glossary("CA")
    assert res["found"] is True
    assert res["term"]["en"] == "Armor Class"

def test_character_calc():
    assert calculate_ability_modifier(10) == 0
    assert calculate_ability_modifier(16) == 3
    assert calculate_ability_modifier(8) == -1
    
    assert calculate_proficiency_bonus(1) == 2
    assert calculate_proficiency_bonus(5) == 3
    assert calculate_proficiency_bonus(9) == 4
    assert calculate_proficiency_bonus(17) == 6

    spell_stats = calculate_spell_stats(casting_ability_score=16, character_level=1)
    # CD: 8 + 2 (PB) + 3 (Mod) = 13
    assert spell_stats["spell_save_dc"] == 13
    # Ataque: 2 (PB) + 3 (Mod) = +5
    assert spell_stats["spell_attack_modifier"] == 5

def test_rag_knowledge_base():
    kb = DnDKnowledgeBase()
    results = kb.search("Concentração", top_k=2)
    assert len(results) > 0
    assert any("Concentração" in r["title"] or "Concentração" in r["content"] for r in results)
