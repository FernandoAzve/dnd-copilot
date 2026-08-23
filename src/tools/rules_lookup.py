import json
import os
from typing import Dict, Any, List, Optional
import unicodedata

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
RULES_PATH = os.path.join(BASE_DIR, "data", "rules", "rules_5e_2024.json")
CONDITIONS_PATH = os.path.join(BASE_DIR, "data", "conditions", "conditions.json")
GLOSSARY_PATH = os.path.join(BASE_DIR, "data", "glossary.json")

def _normalize(text: str) -> str:
    nfkd = unicodedata.normalize('NFKD', text)
    return "".join([c for c in nfkd if not unicodedata.combining(c)]).lower().strip()

def lookup_condition(condition_name: str) -> Dict[str, Any]:
    """Busca detalhes de uma condição de combate (ex: Caído, Cego, Agarrado, Enfeitiçado)."""
    if not os.path.exists(CONDITIONS_PATH):
        return {"found": False, "message": "Arquivo de condições não encontrado."}
        
    with open(CONDITIONS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
        conditions = data.get("conditions", [])
        
    norm_q = _normalize(condition_name)
    
    for c in conditions:
        pt_norm = _normalize(c.get("name_pt", ""))
        en_norm = _normalize(c.get("name_en", ""))
        if norm_q in pt_norm or norm_q in en_norm or pt_norm in norm_q:
            effects_str = "\n".join([f"• {e}" for e in c.get("effects", [])])
            if "effects_2014" in c:
                effects_str = "**Versão 2014:**\n" + "\n".join([f"• {e}" for e in c["effects_2014"]])
            if "effects_2024" in c:
                effects_str += "\n\n**Atualização 2024:**\n" + "\n".join([f"• {e}" for e in c["effects_2024"]])
                
            card = f"### ⚠️ Condição: {c['name_pt']} (*{c['name_en']}*)\n\n{effects_str}\n"
            if "changes_2024" in c:
                card += f"\n**Novidade 2024:** {c['changes_2024']}\n"
                
            return {"found": True, "condition": c, "card": card}
            
    return {"found": False, "message": f"Condição '{condition_name}' não encontrada."}

def lookup_rule(topic: str) -> Dict[str, Any]:
    """Busca uma regra de combate ou mecânica de D&D 5e e 2024."""
    if not os.path.exists(RULES_PATH):
        return {"found": False, "message": "Arquivo de regras não encontrado."}
        
    with open(RULES_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
        rules = data.get("rules", [])
        
    norm_q = _normalize(topic)
    
    for r in rules:
        topic_norm = _normalize(r.get("topic", ""))
        category_norm = _normalize(r.get("category", ""))
        faq_norm = _normalize(r.get("faq", ""))
        
        if norm_q in topic_norm or topic_norm in norm_q or norm_q in category_norm or any(w in topic_norm for w in norm_q.split()):
            card = f"### 📖 Regra: {r['topic']} ({r.get('category', 'Geral')})\n\n"
            if "rule" in r:
                card += f"**Regra Oficial:** {r['rule']}\n\n"
            if "edition_2014" in r:
                card += f"**Versão 2014 (5e):** {r['edition_2014']}\n\n"
            if "edition_2024" in r:
                card += f"**Versão 2024 (Revisão):** {r['edition_2024']}\n\n"
            if "rolls" in r:
                card += f"**Rolagens:** {r['rolls']}\n\n"
            if "damage_at_zero" in r:
                card += f"**Dano em 0 PV:** {r['damage_at_zero']}\n\n"
            if "masteries" in r:
                card += "**Propriedades de Maestria (2024):**\n" + "\n".join([f"• {m}" for m in r['masteries']]) + "\n\n"
            if "faq" in r:
                card += f"💡 *Dica/FAQ:* {r['faq']}\n"
                
            return {"found": True, "rule": r, "card": card}
            
    return {"found": False, "message": f"Regra sobre '{topic}' não encontrada no índice direto."}

def lookup_glossary(term: str) -> Dict[str, Any]:
    """Busca uma definição no glossário D&D PT-BR / EN."""
    if not os.path.exists(GLOSSARY_PATH):
        return {"found": False, "message": "Glossário não encontrado."}
        
    with open(GLOSSARY_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
        terms = data.get("terms", [])
        
    norm_q = _normalize(term)
    for t in terms:
        pt_norm = _normalize(t.get("pt", ""))
        en_norm = _normalize(t.get("en", ""))
        abbr_norm = _normalize(t.get("abbr", ""))
        if norm_q == pt_norm or norm_q == en_norm or norm_q in abbr_norm or norm_q in pt_norm or norm_q in en_norm:
            card = (
                f"### 📚 Glossário: {t['pt']} (*{t['en']}*) - [{t.get('abbr', '')}]\n"
                f"**Categoria:** {t.get('category', 'Geral')}\n\n"
                f"{t['description']}\n"
            )
            return {"found": True, "term": t, "card": card}
            
    return {"found": False, "message": f"Termo '{term}' não encontrado no glossário."}
