import pytest
from src.agent.gemini_agent import DnDAgent
from src.agent.prompts import get_system_prompt

def test_system_prompt_modes():
    mentor_p = get_system_prompt("mentor")
    assert "MENTOR DE INICIANTES" in mentor_p

    arbitro_p = get_system_prompt("arbitro")
    assert "ÁRBITRO RÁPIDO EM JOGO" in arbitro_p

    regras_2024_p = get_system_prompt("regras_2024")
    assert "REGRAS DE 2024" in regras_2024_p

def test_agent_fallback_mode():
    # Sem chave de API, deve responder via fallback de contingência
    agent = DnDAgent(api_key="")
    
    # Teste de rolagem no fallback
    res_dice = agent.answer_query("Role 1d20+5")
    assert "🎲" in res_dice["text"]

    # Teste de busca de regra no fallback
    res_rule = agent.answer_query("Como funciona Concentração?")
    assert "Grimório" in res_rule["text"] or "Concentração" in res_rule["text"]
