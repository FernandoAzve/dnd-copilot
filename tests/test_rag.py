import pytest
import os
from src.rag.vector_store import DnDKnowledgeBase, _cosine_similarity, _text_hash

def test_rag_lexical_and_hybrid_search():
    kb = DnDKnowledgeBase(api_key="")
    assert len(kb.documents) > 0
    
    # 1. Testar busca de Magia exata
    results = kb.search("Bola de Fogo", top_k=2)
    assert len(results) > 0
    assert any("Bola de Fogo" in r["title"] or "Fireball" in r["content"] for r in results)
    
    # 2. Testar busca de Condição de Combate
    results_cond = kb.search("Invisível", top_k=2)
    assert len(results_cond) > 0
    assert any("Invisível" in r["title"] or "Invisible" in r["content"] for r in results_cond)
    
    # 3. Testar busca de Regra de Ataque de Oportunidade
    results_rule = kb.search("Ataque de Oportunidade", top_k=2)
    assert len(results_rule) > 0
    
    # 4. Testar similaridade de cosseno
    vec1 = [1.0, 0.0, 0.0]
    vec2 = [1.0, 0.0, 0.0]
    vec3 = [0.0, 1.0, 0.0]
    assert _cosine_similarity(vec1, vec2) == 1.0
    assert _cosine_similarity(vec1, vec3) == 0.0
    
    # 5. Testar hash de texto
    h1 = _text_hash("Bola de Fogo")
    h2 = _text_hash("Bola de Fogo")
    h3 = _text_hash("Mísseis Mágicos")
    assert h1 == h2
    assert h1 != h3
