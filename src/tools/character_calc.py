from typing import Dict, Any, Union

def calculate_ability_modifier(score: int) -> int:
    """Calcula o modificador para um valor de atributo (ex: 10 -> 0, 16 -> +3, 8 -> -1)."""
    return (score - 10) // 2

def calculate_proficiency_bonus(level: int) -> int:
    """Retorna o Bônus de Proficiência de acordo com o nível do personagem (1 a 20)."""
    if level < 1:
        level = 1
    if level > 20:
        level = 20
    return (level - 1) // 4 + 2

def calculate_spell_stats(
    casting_ability_score: int,
    character_level: int,
    bonus_item: int = 0
) -> Dict[str, Any]:
    """
    Calcula a Classe de Dificuldade (CD) da Magia e o Bônus de Ataque Mágico.
    
    Fórmulas:
    - CD de Magia = 8 + Bônus de Proficiência + Modificador do Atributo Chave + Bônus de Itens
    - Ataque Mágico = Bônus de Proficiência + Modificador do Atributo Chave + Bônus de Itens
    """
    mod = calculate_ability_modifier(casting_ability_score)
    pb = calculate_proficiency_bonus(character_level)
    
    spell_dc = 8 + pb + mod + bonus_item
    spell_attack = pb + mod + bonus_item
    
    return {
        "level": character_level,
        "proficiency_bonus": pb,
        "ability_score": casting_ability_score,
        "ability_modifier": mod,
        "item_bonus": bonus_item,
        "spell_save_dc": spell_dc,
        "spell_attack_modifier": spell_attack,
        "explanation": (
            f"• **Bônus de Proficiência (Nível {character_level})**: +{pb}\n"
            f"• **Modificador de Atributo (Valor {casting_ability_score})**: {mod:+d}\n"
            f"• **CD de Salvaguarda de Magia**: 8 + {pb} (Prof.) + {mod:+d} (Mod.)"
            + (f" + {bonus_item} (Item)" if bonus_item else "")
            + f" = **{spell_dc}**\n"
            f"• **Bônus de Ataque Mágico**: {pb} (Prof.) + {mod:+d} (Mod.)"
            + (f" + {bonus_item} (Item)" if bonus_item else "")
            + f" = **{spell_attack:+d}**"
        )
    }

def calculate_attack_modifier(
    ability_score: int,
    character_level: int,
    is_proficient: bool = True,
    weapon_magic_bonus: int = 0
) -> Dict[str, Any]:
    """
    Calcula o bônus de jogada de ataque com arma.
    
    Fórmula: Modificador de Atributo + (Bônus de Proficiência se for proficiente) + Bônus Mágico
    """
    mod = calculate_ability_modifier(ability_score)
    pb = calculate_proficiency_bonus(character_level) if is_proficient else 0
    total_attack_mod = mod + pb + weapon_magic_bonus
    
    return {
        "ability_modifier": mod,
        "proficiency_bonus": pb,
        "is_proficient": is_proficient,
        "magic_bonus": weapon_magic_bonus,
        "total_attack_modifier": total_attack_mod,
        "explanation": (
            f"• **Modificador de Atributo**: {mod:+d}\n"
            + (f"• **Bônus de Proficiência**: +{pb}\n" if is_proficient else "• **Não proficiente**: +0\n")
            + (f"• **Bônus Mágico da Arma**: +{weapon_magic_bonus}\n" if weapon_magic_bonus else "")
            + f"• **Modificador Total de Ataque**: **{total_attack_mod:+d}** (role 1d20 {total_attack_mod:+d} para acertar)"
        )
    }
