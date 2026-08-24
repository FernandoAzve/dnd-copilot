import io
import json
import re
from typing import Dict, Any, Optional
from ..tools.sheet_validator import SheetValidator, _extract_pdf_form_fields
from ..storage.character_storage import get_default_character_data

def extract_and_build_character_from_file(file_bytes: bytes, filename: str, api_key: str = "") -> Dict[str, Any]:
    """
    Extrai dados estruturados de um arquivo PDF ou imagem de ficha
    e monta um dicionário completo e normalizado de personagem.
    """
    validator = SheetValidator(api_key=api_key)
    
    # 1. Executar extração multimodal do validador de fichas
    result = validator.validate_sheet_file(file_bytes=file_bytes, filename=filename)
    extracted = result.get("extracted_data", {})
    
    # Se a extração do Gemini estiver vazia (ex: sem API key ou erro), tentar extrair campos AcroForm de PDF
    if not extracted and filename.lower().endswith(".pdf"):
        form_fields = _extract_pdf_form_fields(file_bytes)
        if form_fields:
            extracted = {
                "character_name": form_fields.get("CharacterName") or form_fields.get("CharacterName 2") or filename.replace(".pdf", ""),
                "class_name": form_fields.get("ClassLevel", "").split()[0] if form_fields.get("ClassLevel") else "Guerreiro",
                "level": 1,
                "species_race": form_fields.get("Race", "Humano"),
                "background": form_fields.get("Background", "Soldado"),
                "attributes": {
                    "FOR": {"score": int(form_fields.get("STR", 10)) if str(form_fields.get("STR")).isdigit() else 10},
                    "DES": {"score": int(form_fields.get("DEX", 10)) if str(form_fields.get("DEX")).isdigit() else 10},
                    "CON": {"score": int(form_fields.get("CON", 10)) if str(form_fields.get("CON")).isdigit() else 10},
                    "INT": {"score": int(form_fields.get("INT", 10)) if str(form_fields.get("INT")).isdigit() else 10},
                    "SAB": {"score": int(form_fields.get("WIS", 10)) if str(form_fields.get("WIS")).isdigit() else 10},
                    "CAR": {"score": int(form_fields.get("CHA", 10)) if str(form_fields.get("CHA")).isdigit() else 10}
                },
                "armor_class_written": form_fields.get("AC", 10),
                "hit_points_max_written": form_fields.get("HPMax", 10)
            }
    
    char_data = get_default_character_data()
    
    # 2. Mapear Dados Básicos
    if extracted.get("character_name"):
        char_data["name"] = str(extracted["character_name"]).strip()
    elif filename:
        char_data["name"] = filename.replace(".pdf", "").replace(".png", "").replace("_", " ").title()
        
    char_data["species"] = str(extracted.get("species_race") or "Humano").strip()
    char_data["class_name"] = str(extracted.get("class_name") or "Guerreiro").strip()
    char_data["subclass"] = str(extracted.get("subclass_name") or "").strip()
    
    try:
        char_data["level"] = int(extracted.get("level", 1))
    except Exception:
        char_data["level"] = 1
        
    char_data["background"] = str(extracted.get("background") or "Aventureiro").strip()
    
    # 3. Mapear Atributos
    attrs_raw = extracted.get("attributes", {})
    for k_orig, k_dest in [("FOR", "str"), ("DES", "dex"), ("CON", "con"), ("INT", "int"), ("SAB", "wis"), ("CAR", "cha")]:
        score_val = 10
        if k_orig in attrs_raw:
            val_entry = attrs_raw[k_orig]
            if isinstance(val_entry, dict):
                score_val = val_entry.get("score", 10)
            elif isinstance(val_entry, (int, str)):
                score_val = val_entry
        try:
            char_data["abilities"][k_dest] = int(score_val)
        except Exception:
            char_data["abilities"][k_dest] = 10
            
    # 4. Mapear Salvaguardas Marcadas
    marked_saves_raw = extracted.get("saving_throws_marked", [])
    valid_save_keys = []
    for s in marked_saves_raw:
        s_upper = str(s).upper().strip()
        if "FOR" in s_upper or "STR" in s_upper:
            valid_save_keys.append("str")
        elif "DES" in s_upper or "DEX" in s_upper:
            valid_save_keys.append("dex")
        elif "CON" in s_upper:
            valid_save_keys.append("con")
        elif "INT" in s_upper:
            valid_save_keys.append("int")
        elif "SAB" in s_upper or "WIS" in s_upper:
            valid_save_keys.append("wis")
        elif "CAR" in s_upper or "CHA" in s_upper:
            valid_save_keys.append("cha")
            
    if valid_save_keys:
        char_data["saving_throw_proficiencies"] = list(set(valid_save_keys))
        
    # 5. Mapear Combate e Vitais
    try:
        char_data["armor_class"] = int(extracted.get("armor_class_written", 10))
    except Exception:
        char_data["armor_class"] = 10
        
    try:
        hp_max = int(extracted.get("hit_points_max_written", 10))
        char_data["hit_points_max"] = hp_max
        char_data["hit_points_current"] = hp_max
    except Exception:
        char_data["hit_points_max"] = 10
        char_data["hit_points_current"] = 10
        
    # 6. Mapear Ataques
    attacks_raw = extracted.get("weapons_attacks", [])
    if attacks_raw and isinstance(attacks_raw, list):
        char_attacks = []
        for a in attacks_raw:
            if isinstance(a, dict):
                char_attacks.append({
                    "name": str(a.get("name", "Arma")),
                    "attack_bonus": str(a.get("attack_bonus", "+0")),
                    "damage": str(a.get("damage", "1d6")),
                    "damage_type": str(a.get("damage_type", "Cortante")),
                    "mastery": str(a.get("mastery", "")),
                    "notes": str(a.get("notes", ""))
                })
        if char_attacks:
            char_data["attacks"] = char_attacks
            
    # 7. Mapear Itens Mágicos, Talentos e Características
    magic_items = extracted.get("magic_items", [])
    if isinstance(magic_items, list):
        char_data["magic_items"] = [str(i) for i in magic_items]
    elif isinstance(magic_items, str) and magic_items:
        char_data["magic_items"] = [magic_items]
        
    feats_raw = extracted.get("feats_and_traits", [])
    if isinstance(feats_raw, list):
        char_data["feats"] = [str(f) for f in feats_raw]
    elif isinstance(feats_raw, str) and feats_raw:
        char_data["feats"] = [feats_raw]
        
    # 8. Mapear Perícias
    skills_marked = extracted.get("skills_marked", [])
    if skills_marked and isinstance(skills_marked, list):
        char_data["skill_proficiencies"] = [str(s).lower().strip() for s in skills_marked]
        
    return char_data
