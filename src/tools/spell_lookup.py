import json
import os
from typing import Dict, Any, Optional, List
import unicodedata

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "spells", "spells_srd.json")

def _normalize_str(text: str) -> str:
    """Remove acentos e converte para minúsculas para busca flexível."""
    nfkd = unicodedata.normalize('NFKD', text)
    return "".join([c for c in nfkd if not unicodedata.combining(c)]).lower().strip()

def _load_spells() -> List[Dict[str, Any]]:
    if not os.path.exists(DATA_PATH):
        return []
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data.get("spells", [])

def lookup_spell(query: str) -> Dict[str, Any]:
    """
    Busca uma magia pelo nome em Português ou Inglês e retorna seus atributos completos.
    
    Args:
        query: Nome da magia (ex: 'Bola de Fogo', 'Fireball', 'Escudo Arcano', 'Shield')
    """
    spells = _load_spells()
    norm_query = _normalize_str(query)
    
    best_match = None
    partial_matches = []
    
    for s in spells:
        pt_norm = _normalize_str(s.get("name_pt", ""))
        en_norm = _normalize_str(s.get("name_en", ""))
        
        if norm_query == pt_norm or norm_query == en_norm:
            best_match = s
            break
        elif norm_query in pt_norm or norm_query in en_norm or pt_norm in norm_query or en_norm in norm_query:
            partial_matches.append(s)
            
    matched_spell = best_match or (partial_matches[0] if partial_matches else None)
    
    if not matched_spell:
        return {
            "found": False,
            "message": f"Nenhuma magia encontrada para '{query}'.",
            "card": f"⚠️ Magia '{query}' não encontrada no catálogo local do SRD. O assistente usará seu conhecimento geral."
        }
        
    lvl_str = "Truque (Nível 0)" if matched_spell["level"] == 0 else f"{matched_spell['level']}º Nível"
    classes_str = ", ".join(matched_spell.get("classes", []))
    
    card = (
        f"### 📜 {matched_spell['name_pt']} (*{matched_spell['name_en']}*)\n"
        f"**{lvl_str} de {matched_spell['school']}**\n\n"
        f"- **Tempo de Conjuração:** {matched_spell['casting_time']}\n"
        f"- **Alcance:** {matched_spell['range']}\n"
        f"- **Componentes:** {matched_spell['components']}\n"
        f"- **Duração:** {matched_spell['duration']}\n"
        f"- **Classes:** {classes_str}\n\n"
        f"**Descrição:**\n{matched_spell['description']}\n"
    )
    
    if "higher_levels" in matched_spell:
        card += f"\n**Em Níveis Superiores:**\n{matched_spell['higher_levels']}\n"
        
    return {
        "found": True,
        "spell": matched_spell,
        "card": card
    }
