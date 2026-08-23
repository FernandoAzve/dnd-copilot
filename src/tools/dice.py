import random
import re
from typing import Dict, Any, Optional, List

def roll_dice(
    formula: str = "1d20",
    advantage: bool = False,
    disadvantage: bool = False,
    reason: Optional[str] = None
) -> Dict[str, Any]:
    """
    Rola dados segundo uma fórmula (ex: '1d20+5', '2d6+3', '8d6', '4d6kh3') com suporte a vantagem/desvantagem.
    
    Args:
        formula: Expressão do dado (ex: '1d20+5', '2d6', 'd100')
        advantage: Se True, rola 2d20 e pega o maior
        disadvantage: Se True, rola 2d20 e pega o menor
        reason: Motivo da rolagem (ex: 'Ataque com Espada', 'Bola de Fogo')
    """
    clean_formula = formula.strip().lower().replace(" ", "")
    
    # Tratamento de Vantagem / Desvantagem para d20
    if ("d20" in clean_formula or clean_formula == "1d20" or clean_formula.startswith("d20")) and (advantage or disadvantage):
        # Extrair modificador se houver
        mod_match = re.search(r'([+-]\d+)$', clean_formula)
        modifier = int(mod_match.group(1)) if mod_match else 0
        
        roll1 = random.randint(1, 20)
        roll2 = random.randint(1, 20)
        
        if advantage and not disadvantage:
            chosen = max(roll1, roll2)
            mode_str = "Vantagem"
        elif disadvantage and not advantage:
            chosen = min(roll1, roll2)
            mode_str = "Desvantagem"
        else:
            # Vantagem e desvantagem juntas se anulam
            chosen = roll1
            mode_str = "Normal (Vantagem e Desvantagem se anularam)"
            
        total = chosen + modifier
        is_crit = (chosen == 20)
        is_fumble = (chosen == 1)
        
        mod_display = f" {modifier:+d}" if modifier != 0 else ""
        breakdown = f"🎲 [{roll1}, {roll2}] -> Escolhido: {chosen}{mod_display} = **{total}** ({mode_str})"
        if is_crit:
            breakdown += " 🔥 **ACERTO CRÍTICO! (20 Natural)**"
        elif is_fumble:
            breakdown += " 💀 **FALHA CRÍTICA! (1 Natural)**"
            
        return {
            "formula": clean_formula,
            "rolls": [roll1, roll2],
            "chosen_roll": chosen,
            "modifier": modifier,
            "total": total,
            "is_critical_success": is_crit,
            "is_critical_failure": is_fumble,
            "breakdown": breakdown,
            "reason": reason
        }

    # Tratamento de geração de atributo clássico (4d6 drop lowest / 4d6kh3)
    if clean_formula in ["4d6kh3", "4d6dl1", "4d6droplowest"]:
        rolls = [random.randint(1, 6) for _ in range(4)]
        sorted_rolls = sorted(rolls, reverse=True)
        kept = sorted_rolls[:3]
        dropped = sorted_rolls[3]
        total = sum(kept)
        return {
            "formula": "4d6 drop lowest",
            "rolls": rolls,
            "kept": kept,
            "dropped": dropped,
            "modifier": 0,
            "total": total,
            "is_critical_success": False,
            "is_critical_failure": False,
            "breakdown": f"🎲 {rolls} -> Mantidos: {kept} (Descartado: {dropped}) = **{total}**",
            "reason": reason or "Rolagem de Atributo"
        }

    # Parser genérico: NdS+M ou NdS-M ou NdS
    pattern = r'^(\d+)?d(\d+)([+-]\d+)?$'
    match = re.match(pattern, clean_formula)
    
    if not match:
        # Se for apenas um número fixo ou formato simples
        return {
            "formula": formula,
            "rolls": [],
            "modifier": 0,
            "total": 0,
            "is_critical_success": False,
            "is_critical_failure": False,
            "breakdown": f"❌ Expressão de dado inválida: '{formula}'. Use formatos como '1d20+5', '2d6+3', '8d6'.",
            "reason": reason
        }
        
    num_dice = int(match.group(1)) if match.group(1) else 1
    num_dice = min(num_dice, 100)  # Limite de segurança
    die_size = int(match.group(2))
    modifier = int(match.group(3)) if match.group(3) else 0
    
    rolls = [random.randint(1, die_size) for _ in range(num_dice)]
    dice_sum = sum(rolls)
    total = dice_sum + modifier
    
    is_crit = (num_dice == 1 and die_size == 20 and rolls[0] == 20)
    is_fumble = (num_dice == 1 and die_size == 20 and rolls[0] == 1)
    
    mod_display = f" {modifier:+d}" if modifier != 0 else ""
    rolls_str = ", ".join(str(r) for r in rolls)
    if num_dice > 1:
        breakdown = f"🎲 [{rolls_str}] (Soma: {dice_sum}){mod_display} = **{total}**"
    else:
        breakdown = f"🎲 [{rolls_str}]{mod_display} = **{total}**"
        
    if is_crit:
        breakdown += " 🔥 **ACERTO CRÍTICO! (20 Natural)**"
    elif is_fumble:
        breakdown += " 💀 **FALHA CRÍTICA! (1 Natural)**"
        
    return {
        "formula": clean_formula,
        "rolls": rolls,
        "modifier": modifier,
        "total": total,
        "is_critical_success": is_crit,
        "is_critical_failure": is_fumble,
        "breakdown": breakdown,
        "reason": reason
    }

def parse_and_roll(text: str) -> str:
    """Função utilitária para chamar a rolagem a partir do texto do agente."""
    res = roll_dice(text)
    return res["breakdown"]
