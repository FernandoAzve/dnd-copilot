import os
import json
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DEFAULT_CHAR_DIR = os.path.join(BASE_DIR, "data", "characters")
USERS_ROOT = os.path.join(BASE_DIR, "data", "users")

def _get_char_dir(username: Optional[str] = None) -> str:
    """Retorna o diretório de personagens do usuário ou padrão."""
    if username and username.strip():
        user_clean = username.strip().lower()
        d = os.path.join(USERS_ROOT, user_clean, "characters")
    else:
        d = DEFAULT_CHAR_DIR
    os.makedirs(d, exist_ok=True)
    return d

def get_default_character_data() -> Dict[str, Any]:
    """Retorna o template estruturado padrão de uma ficha oficial de D&D 5e / 2024."""
    return {
        "id": "",
        "name": "Novo Aventureiro",
        "player_name": "",
        "species": "Humano",
        "class_name": "Guerreiro",
        "subclass": "Campeão",
        "level": 1,
        "background": "Soldado",
        "alignment": "Neutro e Bom",
        "experience_points": 0,
        
        # Atributos Base
        "abilities": {
            "str": 10,
            "dex": 10,
            "con": 10,
            "int": 10,
            "wis": 10,
            "cha": 10
        },
        
        # Salvaguardas Proficientes (chaves: 'str', 'dex', 'con', 'int', 'wis', 'cha')
        "saving_throw_proficiencies": ["str", "con"],
        
        # Combate & Vitais
        "armor_class": 10,
        "initiative_bonus": 0,
        "speed": "9m (30 ft)",
        "hit_points_max": 10,
        "hit_points_current": 10,
        "hit_points_temp": 0,
        "hit_dice": "1d10",
        "death_saves": {"successes": 0, "failures": 0},
        
        # Perícias Proficientes e Especializações
        "skill_proficiencies": ["atletismo", "percepcao"],
        "skill_expertises": [],
        
        # Ataques & Ações (lista de dicts: name, attack_bonus, damage, damage_type, mastery, notes)
        "attacks": [
            {"name": "Espada Longa", "attack_bonus": "+4", "damage": "1d8+2", "damage_type": "Cortante", "mastery": "Empurrão (Push)", "notes": "Versátil (1d10)"}
        ],
        
        # Conjuração de Magias
        "spellcasting": {
            "ability": "None",  # 'int', 'wis', 'cha' ou 'None'
            "save_dc": 10,
            "attack_bonus": "+2",
            "spell_slots": {
                "level_1": {"max": 0, "current": 0},
                "level_2": {"max": 0, "current": 0},
                "level_3": {"max": 0, "current": 0},
                "level_4": {"max": 0, "current": 0},
                "level_5": {"max": 0, "current": 0},
                "level_6": {"max": 0, "current": 0},
                "level_7": {"max": 0, "current": 0},
                "level_8": {"max": 0, "current": 0},
                "level_9": {"max": 0, "current": 0}
            },
            "cantrips": [],
            "spells_known_or_prepared": []
        },
        
        # Equipamento, Itens Mágicos e Moedas
        "equipment": "Cota de Malha, Escudo, Mochila do Aventureiro",
        "magic_items": [],
        "currency": {
            "cp": 0,
            "sp": 0,
            "ep": 0,
            "gp": 10,
            "pp": 0
        },
        
        # Talentos, Características e Idiomas
        "feats": ["Valentão de Taverna (Origem)"],
        "features_and_traits": "Segundo Fôlego, Estilo de Luta",
        "proficiencies_languages": "Armaduras: Todas | Armas: Simples, Marciais | Idiomas: Comum",
        
        # Biografia & Interpretação
        "personality_traits": "",
        "ideals": "",
        "bonds": "",
        "flaws": "",
        "backstory": "",
        "notes": "",
        
        "created_at": "",
        "updated_at": ""
    }

def save_character(char_data: Dict[str, Any], username: Optional[str] = None) -> str:
    """Salva ou atualiza uma ficha de personagem no armazenamento persistente do usuário."""
    char_dir = _get_char_dir(username)
    now_iso = datetime.now().isoformat()
    
    char_id = char_data.get("id")
    if not char_id or not char_id.strip():
        now_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        short_uuid = uuid.uuid4().hex[:6]
        char_id = f"char_{now_str}_{short_uuid}"
        char_data["id"] = char_id
        char_data["created_at"] = now_iso
        
    char_data["updated_at"] = now_iso
    if not char_data.get("created_at"):
        char_data["created_at"] = now_iso
        
    file_path = os.path.join(char_dir, f"{char_id}.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(char_data, f, ensure_ascii=False, indent=2)
        
    # Se for o único personagem, torna-o ativo automaticamente se não houver outro ativo
    active_id = get_active_character_id(username)
    if not active_id:
        set_active_character_id(char_id, username)
        
    return char_id

def get_character(char_id: str, username: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Recupera os dados completos de um personagem pelo ID."""
    if not char_id:
        return None
    char_dir = _get_char_dir(username)
    file_path = os.path.join(char_dir, f"{char_id}.json")
    
    if not os.path.exists(file_path):
        fallback = os.path.join(DEFAULT_CHAR_DIR, f"{char_id}.json")
        if os.path.exists(fallback):
            file_path = fallback
        else:
            return None
            
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Erro ao ler personagem {char_id}: {e}")
        return None

def list_characters(username: Optional[str] = None) -> List[Dict[str, Any]]:
    """Lista todos os personagens cadastrados do usuário ordenados por atualização recente."""
    char_dir = _get_char_dir(username)
    if not os.path.exists(char_dir):
        return []
        
    characters = []
    for fname in os.listdir(char_dir):
        if fname.endswith(".json") and not fname.startswith("active_"):
            file_path = os.path.join(char_dir, fname)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    characters.append({
                        "id": data.get("id", fname.replace(".json", "")),
                        "name": data.get("name", "Personagem Sem Nome"),
                        "class_name": data.get("class_name", "Classe"),
                        "subclass": data.get("subclass", ""),
                        "level": data.get("level", 1),
                        "species": data.get("species", "Humano"),
                        "armor_class": data.get("armor_class", 10),
                        "hit_points_max": data.get("hit_points_max", 10),
                        "hit_points_current": data.get("hit_points_current", 10),
                        "created_at": data.get("created_at", ""),
                        "updated_at": data.get("updated_at", "")
                    })
            except Exception as e:
                print(f"Erro ao listar personagem {fname}: {e}")
                
    characters.sort(key=lambda c: c.get("updated_at", c.get("created_at", "")), reverse=True)
    return characters

def delete_character(char_id: str, username: Optional[str] = None) -> bool:
    """Exclui um personagem do armazenamento."""
    char_dir = _get_char_dir(username)
    file_path = os.path.join(char_dir, f"{char_id}.json")
    if not os.path.exists(file_path):
        fallback = os.path.join(DEFAULT_CHAR_DIR, f"{char_id}.json")
        if os.path.exists(fallback):
            file_path = fallback
        else:
            return False
            
    try:
        os.remove(file_path)
        if get_active_character_id(username) == char_id:
            set_active_character_id("", username)
        return True
    except Exception as e:
        print(f"Erro ao excluir personagem {char_id}: {e}")
        return False

def get_active_character_id(username: Optional[str] = None) -> Optional[str]:
    """Retorna o ID do personagem atualmente ativo no contexto do usuário."""
    char_dir = _get_char_dir(username)
    pref_file = os.path.join(char_dir, "active_character.json")
    if os.path.exists(pref_file):
        try:
            with open(pref_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("active_character_id")
        except Exception:
            pass
    return None

def set_active_character_id(char_id: str, username: Optional[str] = None) -> bool:
    """Define o personagem atualmente ativo no contexto do usuário."""
    char_dir = _get_char_dir(username)
    pref_file = os.path.join(char_dir, "active_character.json")
    try:
        with open(pref_file, "w", encoding="utf-8") as f:
            json.dump({"active_character_id": char_id, "updated_at": datetime.now().isoformat()}, f, indent=2)
        return True
    except Exception as e:
        print(f"Erro ao salvar personagem ativo: {e}")
        return False

def format_character_context(char_data: Dict[str, Any]) -> str:
    """
    Gera um resumo estruturado e conciso do personagem ativo para ser
    injetado diretamente no system prompt do agente IA no Grimório.
    """
    if not char_data:
        return ""
        
    name = char_data.get("name", "Personagem")
    cls = char_data.get("class_name", "")
    subcls = char_data.get("subclass", "")
    lvl = char_data.get("level", 1)
    species = char_data.get("species", "")
    background = char_data.get("background", "")
    
    # Bônus de proficiência: 1-4 (+2), 5-8 (+3), 9-12 (+4), 13-16 (+5), 17-20 (+6)
    pb = 2 + (max(1, lvl) - 1) // 4
    
    # Atributos e Modificadores
    abilities = char_data.get("abilities", {})
    str_val = abilities.get("str", 10)
    dex_val = abilities.get("dex", 10)
    con_val = abilities.get("con", 10)
    int_val = abilities.get("int", 10)
    wis_val = abilities.get("wis", 10)
    cha_val = abilities.get("cha", 10)
    
    def mod_calc(val):
        m = (val - 10) // 2
        return f"+{m}" if m >= 0 else str(m)
        
    str_mod = mod_calc(str_val)
    dex_mod = mod_calc(dex_val)
    con_mod = mod_calc(con_val)
    int_mod = mod_calc(int_val)
    wis_mod = mod_calc(wis_val)
    cha_mod = mod_calc(cha_val)
    
    # Salvaguardas
    saving_profs = char_data.get("saving_throw_proficiencies", [])
    def save_calc(attr_key, val):
        m = (val - 10) // 2
        if attr_key in saving_profs:
            m += pb
        return f"+{m}" if m >= 0 else str(m)
        
    saves_str = (
        f"FOR {save_calc('str', str_val)} ({'●' if 'str' in saving_profs else '○'}), "
        f"DES {save_calc('dex', dex_val)} ({'●' if 'dex' in saving_profs else '○'}), "
        f"CON {save_calc('con', con_val)} ({'●' if 'con' in saving_profs else '○'}), "
        f"INT {save_calc('int', int_val)} ({'●' if 'int' in saving_profs else '○'}), "
        f"SAB {save_calc('wis', wis_val)} ({'●' if 'wis' in saving_profs else '○'}), "
        f"CAR {save_calc('cha', cha_val)} ({'●' if 'cha' in saving_profs else '○'})"
    )
    
    # Vitais
    hp_cur = char_data.get("hit_points_current", 10)
    hp_max = char_data.get("hit_points_max", 10)
    hp_temp = char_data.get("hit_points_temp", 0)
    ac = char_data.get("armor_class", 10)
    speed = char_data.get("speed", "9m")
    
    # Ataques com Maestria 2024
    attacks = char_data.get("attacks", [])
    attacks_list = []
    for a in attacks:
        if a.get("name"):
            mastery_str = f" [Maestria: {a.get('mastery')}]" if a.get("mastery") else ""
            attacks_list.append(f"{a.get('name')}: Acerto {a.get('attack_bonus')}, Dano {a.get('damage')} ({a.get('damage_type')}){mastery_str}")
    attacks_summary = " | ".join(attacks_list) if attacks_list else "Nenhum ataque configurado"
    
    # Magias
    sp_data = char_data.get("spellcasting", {})
    sp_ability = sp_data.get("ability", "None")
    sp_summary = ""
    if sp_ability and sp_ability != "None":
        sp_dc = sp_data.get("save_dc", 10)
        sp_atk = sp_data.get("attack_bonus", "+2")
        cantrips = ", ".join(sp_data.get("cantrips", []))
        spells = ", ".join(sp_data.get("spells_known_or_prepared", []))
        sp_summary = f"\n- **Conjuração ({sp_ability.upper()}):** CD {sp_dc} | Ataque {sp_atk} | Truques: {cantrips or 'Nenhum'} | Magias: {spells or 'Nenhuma'}"
        
    # Itens Mágicos e Talentos
    magic_items = ", ".join(char_data.get("magic_items", [])) or "Nenhum"
    feats = ", ".join(char_data.get("feats", [])) or "Nenhum"
    features = char_data.get("features_and_traits", "")
    
    context_lines = [
        f"### 🛡️ Personagem Ativo do Jogador (D&D 5e / 2024):",
        f"- **Nome:** {name} | **Espécie:** {species} | **Classe:** {cls} {f'({subcls})' if subcls else ''} Nível {lvl} | **Antecedente:** {background}",
        f"- **Bônus de Proficiência (PB):** +{pb} | **CA:** {ac} | **PV:** {hp_cur}/{hp_max} {f'(+{hp_temp} Temp)' if hp_temp else ''} | **Deslocamento:** {speed}",
        f"- **Atributos:** FOR {str_val} ({str_mod}), DES {dex_val} ({dex_mod}), CON {con_val} ({con_mod}), INT {int_val} ({int_mod}), SAB {wis_val} ({wis_mod}), CAR {cha_val} ({cha_mod})",
        f"- **Salvaguardas:** {saves_str}",
        f"- **Ataques & Maestrias:** {attacks_summary}",
        f"- **Itens Mágicos:** {magic_items} | **Talentos:** {feats}",
    ]
    
    if sp_summary:
        context_lines.append(sp_summary)
        
    if features:
        context_lines.append(f"- **Habilidades Chave:** {features[:300]}...")
        
    context_lines.append("\n*Instrução: Use as estatísticas, bônus, itens, maestrias e magias acima para personalizar suas respostas, cálculos e conselhos automaticamente para este personagem.*")
    
    return "\n".join(context_lines)
