from typing import Dict, List, Any, Optional

# =============================================================================
# 1. CLASSES & SUBCLASSES OFICIAIS D&D 2024 (COM DADO DE VIDA E SALVAGUARDAS)
# =============================================================================
CLASSES_2024: Dict[str, Dict[str, Any]] = {
    "Guerreiro": {
        "hit_die": "1d10",
        "primary_ability": "FOR ou DES",
        "saving_throws": ["str", "con"],
        "spell_ability": "None",
        "subclasses": ["Campeão", "Mestre de Batalha", "Cavaleiro Arcano", "Guerreiro Psíquico"],
        "weapon_mastery_count": 3,
        "description": "Mestre incomparável de todas as armas e táticas de batalha marciais."
    },
    "Mago": {
        "hit_die": "1d6",
        "primary_ability": "INT",
        "saving_throws": ["int", "wis"],
        "spell_ability": "int",
        "subclasses": ["Abjuração", "Adivinhação", "Evocação", "Ilusão"],
        "weapon_mastery_count": 0,
        "description": "Erudito arcano capaz de manipular a própria trama da realidade."
    },
    "Ladino": {
        "hit_die": "1d8",
        "primary_ability": "DES",
        "saving_throws": ["dex", "int"],
        "spell_ability": "None",
        "subclasses": ["Assassino", "Ladrão", "Trapaceiro Arcano", "Lâmina da Alma"],
        "weapon_mastery_count": 2,
        "description": "Especialista em furtividade, truques periciais e ataques letais."
    },
    "Clérigo": {
        "hit_die": "1d8",
        "primary_ability": "SAB",
        "saving_throws": ["wis", "cha"],
        "spell_ability": "wis",
        "subclasses": ["Domínio da Vida", "Domínio da Luz", "Domínio da Trapaça", "Domínio da Guerra"],
        "weapon_mastery_count": 0,
        "description": "Campeão divino canalizando o poder e milagres dos deuses."
    },
    "Paladino": {
        "hit_die": "1d10",
        "primary_ability": "FOR e CAR",
        "saving_throws": ["wis", "cha"],
        "spell_ability": "cha",
        "subclasses": ["Juramento de Devoção", "Juramento de Glória", "Juramento dos Anciãos", "Juramento de Vingança"],
        "weapon_mastery_count": 2,
        "description": "Guerreiro sagrado vinculado por um juramento inquebrável."
    },
    "Bárbaro": {
        "hit_die": "1d12",
        "primary_ability": "FOR",
        "saving_throws": ["str", "con"],
        "spell_ability": "None",
        "subclasses": ["Caminho do Berserker", "Coração Selvagem", "Zelote", "Árvore do Mundo"],
        "weapon_mastery_count": 2,
        "description": "Combatente feroz alimentado por uma fúria primal incontrolável."
    },
    "Bardo": {
        "hit_die": "1d8",
        "primary_ability": "CAR",
        "saving_throws": ["dex", "cha"],
        "spell_ability": "cha",
        "subclasses": ["Colégio da Dança", "Colégio do Glamour", "Colégio da Lore", "Colégio da Bravura"],
        "weapon_mastery_count": 0,
        "description": "Mestre da música, magia de palavras e inspiração de heróis."
    },
    "Bruxo": {
        "hit_die": "1d8",
        "primary_ability": "CAR",
        "saving_throws": ["wis", "cha"],
        "spell_ability": "cha",
        "subclasses": ["Patrono Arquifada", "Patrono Corruptor", "Patrono Grande Antigo", "Patrono Celestial"],
        "weapon_mastery_count": 0,
        "description": "Portador de segredos arcanos através de um pacto com uma entidade cósmica."
    },
    "Druida": {
        "hit_die": "1d8",
        "primary_ability": "SAB",
        "saving_throws": ["int", "wis"],
        "spell_ability": "wis",
        "subclasses": ["Círculo da Terra", "Círculo da Lua", "Círculo das Estrelas", "Círculo do Mar"],
        "weapon_mastery_count": 0,
        "description": "Guardião da natureza capaz de mudar de forma e invocar forças elementais."
    },
    "Feiticeiro": {
        "hit_die": "1d6",
        "primary_ability": "CAR",
        "saving_throws": ["con", "cha"],
        "spell_ability": "cha",
        "subclasses": ["Feitiçaria Dracônica", "Magia Selvagem", "Feitiçaria da Tempestade", "Alma Aberrante"],
        "weapon_mastery_count": 0,
        "description": "Conjurador com magia inata pulsando em seu sangue."
    },
    "Guardião": {
        "hit_die": "1d10",
        "primary_ability": "DES e SAB",
        "saving_throws": ["str", "dex"],
        "spell_ability": "wis",
        "subclasses": ["Caçador", "Mestre das Feras", "Rastreador Sombrio", "Guardião Feérico"],
        "weapon_mastery_count": 2,
        "description": "Rastreador implacável e guerreiro das fronteiras selvagens."
    },
    "Monge": {
        "hit_die": "1d8",
        "primary_ability": "DES e SAB",
        "saving_throws": ["str", "dex"],
        "spell_ability": "None",
        "subclasses": ["Caminho da Mão Aberta", "Caminho da Sombra", "Caminho dos Elementos", "Caminho da Misericórdia"],
        "weapon_mastery_count": 0,
        "description": "Artista marcial que canaliza a energia do Ki através de seu corpo."
    }
}

# =============================================================================
# 2. ESPÉCIES / RAÇAS OFICIAIS D&D 2024
# =============================================================================
SPECIES_2024: Dict[str, Dict[str, Any]] = {
    "Humano": {"speed": "9m (30 ft)", "traits": "Talento de Origem Adicional, Inspiração Heroica por Descanso, Proficiência Pericial"},
    "Elfo": {"speed": "9m (30 ft)", "traits": "Visão no Escuro (18m), Ancestral Feérico, Transe, Magia Élfica (Alto, Floresta ou Drow)"},
    "Anão": {"speed": "9m (30 ft)", "traits": "Visão no Escuro (36m), Resiliência Anã (Resistência a Veneno), Robustez Anã (+1 PV por nível)"},
    "Halfling": {"speed": "9m (30 ft)", "traits": "Sortudo (Rola novamente 1s no d20), Corajoso, Agilidade Halfling"},
    "Draconato": {"speed": "9m (30 ft)", "traits": "Arma de Sopro Elemental, Resistência a Dano, Visão no Escuro (18m), Voo Dracônico (Nível 5)"},
    "Gnomo": {"speed": "9m (30 ft)", "traits": "Astúcia Gnômica (Vantagem em Salvaguardas INT/SAB/CAR), Visão no Escuro (18m)"},
    "Golias": {"speed": "10,5m (35 ft)", "traits": "Ancestral Gigante (Habilidade Especial), Atleta Natural, Forma Gigante (Nível 5)"},
    "Orc": {"speed": "9m (30 ft)", "traits": "Investida Adrenérgica (Ação Bônus), Resistência Implacável (Cai para 1 PV em vez de 0)"},
    "Tiferino": {"speed": "9m (30 ft)", "traits": "Visão no Escuro (21m), Legado Sobrenatural (Infernal, Abissal ou Ctônico), Taumaturgia"},
    "Aasimar": {"speed": "9m (30 ft)", "traits": "Visão no Escuro (18m), Mãos Curativas, Transformação Celestial (Voo ou Dano Radiante)"}
}

# =============================================================================
# 3. ANTECEDENTES OFICIAIS D&D 2024 (COM TALENTOS DE ORIGEM)
# =============================================================================
BACKGROUNDS_2024: Dict[str, Dict[str, Any]] = {
    "Soldado": {"feat": "Valentão de Taverna", "attributes": "FOR, CON ou DES", "skills": ["Atletismo", "Intimidação"]},
    "Acólito": {"feat": "Iniciado em Magia (Clérigo)", "attributes": "SAB, INT ou CAR", "skills": ["Intuição", "Religião"]},
    "Sábio": {"feat": "Iniciado em Magia (Mago)", "attributes": "INT, CON ou SAB", "skills": ["Arcanismo", "História"]},
    "Guarda": {"feat": "Alerta", "attributes": "FOR, INT ou SAB", "skills": ["Atletismo", "Percepção"]},
    "Guia": {"feat": "Iniciado em Magia (Druida)", "attributes": "SAB, CON ou DES", "skills": ["Sobrevivência", "Furtividade"]},
    "Fazendeiro": {"feat": "Robusto", "attributes": "CON, FOR ou SAB", "skills": ["Lidar com Animais", "Natureza"]},
    "Criminoso": {"feat": "Alerta", "attributes": "DES, CON ou INT", "skills": ["Enganação", "Furtividade"]},
    "Artesão": {"feat": "Artesão Hábil", "attributes": "FOR, DES ou INT", "skills": ["Investigação", "Persuasão"]},
    "Artista": {"feat": "Músico", "attributes": "CAR, DES ou SAB", "skills": ["Acrobacia", "Atuação"]},
    "Charlatão": {"feat": "Habilidoso", "attributes": "CAR, DES ou CON", "skills": ["Enganação", "Prestidigitação"]},
    "Eremita": {"feat": "Curandeiro", "attributes": "SAB, CON ou CAR", "skills": ["Medicina", "Religião"]},
    "Marinheiro": {"feat": "Valentão de Taverna", "attributes": "FOR, DES ou CON", "skills": ["Atletismo", "Percepção"]},
    "Mercador": {"feat": "Sortudo", "attributes": "CAR, INT ou CON", "skills": ["Lidar com Animais", "Persuasão"]},
    "Nobre": {"feat": "Habilidoso", "attributes": "CAR, INT ou SAB", "skills": ["História", "Persuasão"]},
    "Órfão": {"feat": "Sortudo", "attributes": "DES, CON ou SAB", "skills": ["Furtividade", "Prestidigitação"]},
    "Viajante": {"feat": "Sortudo", "attributes": "DES, SAB ou CAR", "skills": ["Intuição", "Sobrevivência"]}
}

# =============================================================================
# 4. ARMAS OFICIAIS COM MAESTRIA DE ARMA 2024 (WEAPON MASTERY)
# =============================================================================
WEAPONS_2024: List[Dict[str, Any]] = [
    # Marciais Corpo a Corpo
    {"name": "Espada Longa", "category": "Marcial", "damage": "1d8", "damage_type": "Cortante", "properties": "Versátil (1d10)", "mastery": "Empurrão (Push)"},
    {"name": "Espada Grande", "category": "Marcial", "damage": "2d6", "damage_type": "Cortante", "properties": "Pesada, Duas Mãos", "mastery": "Rasgar (Graze)"},
    {"name": "Rapieira", "category": "Marcial", "damage": "1d8", "damage_type": "Perfurante", "properties": "Acuidade", "mastery": "Provocar (Vex)"},
    {"name": "Machado de Batalha", "category": "Marcial", "damage": "1d8", "damage_type": "Cortante", "properties": "Versátil (1d10)", "mastery": "Derrubar (Topple)"},
    {"name": "Machado Grande", "category": "Marcial", "damage": "1d12", "damage_type": "Cortante", "properties": "Pesada, Duas Mãos", "mastery": "Cutilada (Cleave)"},
    {"name": "Alabarda", "category": "Marcial", "damage": "1d10", "damage_type": "Cortante", "properties": "Pesada, Alcance, Duas Mãos", "mastery": "Cutilada (Cleave)"},
    {"name": "Glaive", "category": "Marcial", "damage": "1d10", "damage_type": "Cortante", "properties": "Pesada, Alcance, Duas Mãos", "mastery": "Rasgar (Graze)"},
    {"name": "Mangual", "category": "Marcial", "damage": "1d8", "damage_type": "Contundente", "properties": "-", "mastery": "Fraqueza (Sap)"},
    {"name": "Martelo de Guerra", "category": "Marcial", "damage": "1d8", "damage_type": "Contundente", "properties": "Versátil (1d10)", "mastery": "Empurrão (Push)"},
    {"name": "Maça Estrela", "category": "Marcial", "damage": "1d8", "damage_type": "Perfurante", "properties": "-", "mastery": "Fraqueza (Sap)"},
    {"name": "Cimitarra", "category": "Marcial", "damage": "1d6", "damage_type": "Cortante", "properties": "Acuidade, Leve", "mastery": "Golpe Rápido (Nick)"},
    {"name": "Espada Curta", "category": "Marcial", "damage": "1d6", "damage_type": "Perfurante", "properties": "Acuidade, Leve", "mastery": "Provocar (Vex)"},
    {"name": "Tridente", "category": "Marcial", "damage": "1d8", "damage_type": "Perfurante", "properties": "Arremesso (6/18m), Versátil (1d10)", "mastery": "Derrubar (Topple)"},
    {"name": "Pique", "category": "Marcial", "damage": "1d10", "damage_type": "Perfurante", "properties": "Pesada, Alcance, Duas Mãos", "mastery": "Empurrão (Push)"},
    
    # Simples Corpo a Corpo
    {"name": "Adaga", "category": "Simples", "damage": "1d4", "damage_type": "Perfurante", "properties": "Acuidade, Leve, Arremesso (6/18m)", "mastery": "Golpe Rápido (Nick)"},
    {"name": "Maça", "category": "Simples", "damage": "1d6", "damage_type": "Contundente", "properties": "-", "mastery": "Fraqueza (Sap)"},
    {"name": "Cajado", "category": "Simples", "damage": "1d6", "damage_type": "Contundente", "properties": "Versátil (1d8)", "mastery": "Derrubar (Topple)"},
    {"name": "Lança", "category": "Simples", "damage": "1d6", "damage_type": "Perfurante", "properties": "Arremesso (6/18m), Versátil (1d8)", "mastery": "Fraqueza (Sap)"},
    {"name": "Machadinha", "category": "Simples", "damage": "1d6", "damage_type": "Cortante", "properties": "Leve, Arremesso (6/18m)", "mastery": "Provocar (Vex)"},
    {"name": "Martelo Leve", "category": "Simples", "damage": "1d4", "damage_type": "Contundente", "properties": "Leve, Arremesso (6/18m)", "mastery": "Golpe Rápido (Nick)"},
    {"name": "Clava", "category": "Simples", "damage": "1d4", "damage_type": "Contundente", "properties": "Leve", "mastery": "Lentidão (Slow)"},
    {"name": "Clava Grande", "category": "Simples", "damage": "1d8", "damage_type": "Contundente", "properties": "Duas Mãos", "mastery": "Empurrão (Push)"},

    # Armas à Distância
    {"name": "Arco Longo", "category": "Marcial", "damage": "1d8", "damage_type": "Perfurante", "properties": "Munição (45/180m), Pesada, Duas Mãos", "mastery": "Lentidão (Slow)"},
    {"name": "Arco Curto", "category": "Simples", "damage": "1d6", "damage_type": "Perfurante", "properties": "Munição (24/96m), Duas Mãos", "mastery": "Provocar (Vex)"},
    {"name": "Besta Pesada", "category": "Marcial", "damage": "1d10", "damage_type": "Perfurante", "properties": "Munição (30/120m), Recarga, Pesada, Duas Mãos", "mastery": "Empurrão (Push)"},
    {"name": "Besta Leve", "category": "Simples", "damage": "1d8", "damage_type": "Perfurante", "properties": "Munição (24/96m), Recarga, Duas Mãos", "mastery": "Lentidão (Slow)"},
    {"name": "Besta de Mão", "category": "Marcial", "damage": "1d6", "damage_type": "Perfurante", "properties": "Munição (9/36m), Leve, Recarga", "mastery": "Provocar (Vex)"},
    {"name": "Dardo", "category": "Simples", "damage": "1d4", "damage_type": "Perfurante", "properties": "Acuidade, Arremesso (6/18m)", "mastery": "Provocar (Vex)"},
    {"name": "Funda", "category": "Simples", "damage": "1d4", "damage_type": "Contundente", "properties": "Munição (9/36m)", "mastery": "Lentidão (Slow)"}
]

# =============================================================================
# 5. ARMADURAS & DEFESAS OFICIAIS D&D 2024
# =============================================================================
ARMOR_2024: List[Dict[str, Any]] = [
    # Armaduras Leves (CA + Mod DES)
    {"name": "Acolchoada", "category": "Leve", "ac_base": 11, "stealth_disadv": True, "str_req": 0},
    {"name": "Couro", "category": "Leve", "ac_base": 11, "stealth_disadv": False, "str_req": 0},
    {"name": "Couro Batido", "category": "Leve", "ac_base": 12, "stealth_disadv": False, "str_req": 0},
    
    # Armaduras Médias (CA + Mod DES máx +2)
    {"name": "Gibão de Peles", "category": "Média", "ac_base": 12, "stealth_disadv": False, "str_req": 0},
    {"name": "Camisão de Cota de Malha", "category": "Média", "ac_base": 13, "stealth_disadv": False, "str_req": 0},
    {"name": "Brunea", "category": "Média", "ac_base": 14, "stealth_disadv": True, "str_req": 0},
    {"name": "Peitoral de Aço", "category": "Média", "ac_base": 14, "stealth_disadv": False, "str_req": 0},
    {"name": "Meia-Armadura", "category": "Média", "ac_base": 15, "stealth_disadv": True, "str_req": 0},
    
    # Armaduras Pesadas (CA Fixa, sem DES)
    {"name": "Cota de Anéis", "category": "Pesada", "ac_base": 14, "stealth_disadv": True, "str_req": 0},
    {"name": "Cota de Malha", "category": "Pesada", "ac_base": 16, "stealth_disadv": True, "str_req": 13},
    {"name": "Cota de Talas", "category": "Pesada", "ac_base": 17, "stealth_disadv": True, "str_req": 15},
    {"name": "Armadura de Placas Completa", "category": "Pesada", "ac_base": 18, "stealth_disadv": True, "str_req": 15},
    
    # Escudo
    {"name": "Escudo (+2 CA)", "category": "Escudo", "ac_base": 2, "stealth_disadv": False, "str_req": 0}
]

# =============================================================================
# 6. TALENTOS OFICIAIS D&D 2024 (ORIGEM E GERAIS)
# =============================================================================
FEATS_2024: List[Dict[str, Any]] = [
    # Talentos de Origem (Nível 1)
    {"name": "Alerta (Origem)", "type": "Origem", "description": "Adiciona PB na Iniciativa e pode trocar iniciativa com um aliado voluntário."},
    {"name": "Iniciado em Magia (Origem)", "type": "Origem", "description": "Aprende 2 truques e 1 magia de 1º nível de Clérigo, Druida ou Mago (conjurada 1x/dia grátis ou com espaços)."},
    {"name": "Sortudo (Origem)", "type": "Origem", "description": "Ganha Pontos de Sorte iguais ao PB para rolar com vantagem ou dar desvantagem a ataques inimigos."},
    {"name": "Músico (Origem)", "type": "Origem", "description": "Concede Inspiração Heroica a um número de aliados igual ao PB após Descanso Curto ou Longo."},
    {"name": "Curandeiro (Origem)", "type": "Origem", "description": "Permite gastar Dado de Vida para curar aliados com Kit de Primeiros Socorros e rolar dados de cura novamente se tirar 1."},
    {"name": "Valentão de Taverna (Origem)", "type": "Origem", "description": "Ataques desarmados causam 1d4 + FOR, pode empurrar criaturas e rolar dano novamente em 1s."},
    {"name": "Artesão Hábil (Origem)", "type": "Origem", "description": "Fabricação rápida de itens e desconto de 20% em compras de equipamentos não mágicos."},
    {"name": "Robusto (Origem)", "type": "Origem", "description": "Ganha +2 PV por nível de personagem (retroativo e futuro)."},
    {"name": "Habilidoso (Origem)", "type": "Origem", "description": "Ganha proficiência em quaisquer 3 perícias ou ferramentas à sua escolha."},
    
    # Talentos Gerais (Nível 4+)
    {"name": "Mestre em Armas Grandes (Nível 4+)", "type": "Geral", "description": "Ataque bônus ao acertar crítico ou derrotar inimigo; soma PB no dano de armas Pesadas."},
    {"name": "Conjurador de Guerra (Nível 4+)", "type": "Geral", "description": "Vantagem em salvaguardas de Concentração; pode usar magias em Ataques de Oportunidade."},
    {"name": "Sentinela (Nível 4+)", "type": "Geral", "description": "Ataques de oportunidade reduzem deslocamento a 0 e ignora a ação Desengajar."},
    {"name": "Franco-Atirador (Nível 4+)", "type": "Geral", "description": "Ignora cobertura parcial e meia cobertura; pode atirar à queima-roupa sem desvantagem."},
    {"name": "Duelista Defensivo (Nível 4+)", "type": "Geral", "description": "Usa Reação para somar PB na CA contra ataques corpo a corpo com arma de Acuidade."},
    {"name": "Mestre em Escudos (Nível 4+)", "type": "Geral", "description": "Ação Bônus para empurrar inimigos com escudo e soma bônus do escudo em salvaguardas de DES."},
    {"name": "Resiliente (Nível 4+)", "type": "Geral", "description": "+1 em um atributo e ganha proficiência na respectiva salvaguarda."}
]

# =============================================================================
# 7. ITENS MÁGICOS CANÔNICOS
# =============================================================================
MAGIC_ITEMS_2024: List[Dict[str, Any]] = [
    {"name": "Capa de Proteção (Sintonizado)", "rarity": "Incomum", "attunement": True, "bonus": "+1 em CA e todas as Salvaguardas"},
    {"name": "Anel de Proteção (Sintonizado)", "rarity": "Raro", "attunement": True, "bonus": "+1 em CA e todas as Salvaguardas"},
    {"name": "Botas Aladas (Sintonizado)", "rarity": "Incomum", "attunement": True, "bonus": "Deslocamento de voo igual ao deslocamento terrestre por até 4 horas"},
    {"name": "Braçadeiras de Defesa (Sintonizado)", "rarity": "Raro", "attunement": True, "bonus": "+2 na CA se não estiver usando armadura nem escudo"},
    {"name": "Arma +1 (Qualquer Arma)", "rarity": "Incomum", "attunement": False, "bonus": "+1 nas jogadas de ataque e dano"},
    {"name": "Arma +2 (Qualquer Arma)", "rarity": "Raro", "attunement": False, "bonus": "+2 nas jogadas de ataque e dano"},
    {"name": "Arma +3 (Qualquer Arma)", "rarity": "Muito Raro", "attunement": False, "bonus": "+3 nas jogadas de ataque e dano"},
    {"name": "Escudo +1", "rarity": "Incomum", "attunement": False, "bonus": "+3 total na CA (+2 base + 1 mágico)"},
    {"name": "Poção de Cura Comum (2d4+2)", "rarity": "Comum", "attunement": False, "bonus": "Recupera 2d4+2 PV (Ação Bônus em 2024)"},
    {"name": "Poção de Cura Maior (4d4+4)", "rarity": "Incomum", "attunement": False, "bonus": "Recupera 4d4+4 PV (Ação Bônus em 2024)"},
    {"name": "Varinha de Mísseis Mágicos", "rarity": "Incomum", "attunement": False, "bonus": "7 cargas para conjurar Mísseis Mágicos sem gastar espaço"}
]

# =============================================================================
# 8. CATÁLOGO DE MAGIAS CANÔNICAS D&D 5E / 2024
# =============================================================================
SPELLS_CATALOG: List[Dict[str, Any]] = [
    {"name_pt": "Bola de Fogo", "name_en": "Fireball", "level": 3, "school": "Evocação", "classes": ["Mago", "Feiticeiro"]},
    {"name_pt": "Curar Ferimentos", "name_en": "Cure Wounds", "level": 1, "school": "Evocação", "classes": ["Bardo", "Clérigo", "Druida", "Paladino", "Patrulheiro"]},
    {"name_pt": "Palavra Curativa", "name_en": "Healing Word", "level": 1, "school": "Evocação", "classes": ["Bardo", "Clérigo", "Druida"]},
    {"name_pt": "Escudo Arcano", "name_en": "Shield", "level": 1, "school": "Abjuração", "classes": ["Mago", "Feiticeiro"]},
    {"name_pt": "Mísseis Mágicos", "name_en": "Magic Missile", "level": 1, "school": "Evocação", "classes": ["Mago", "Feiticeiro"]},
    {"name_pt": "Raio Guiador", "name_en": "Guiding Bolt", "level": 1, "school": "Evocação", "classes": ["Clérigo"]},
    {"name_pt": "Passo Nebuloso", "name_en": "Misty Step", "level": 2, "school": "Conjuração", "classes": ["Mago", "Feiticeiro", "Bruxo"]},
    {"name_pt": "Invisibilidade", "name_en": "Invisibility", "level": 2, "school": "Ilusão", "classes": ["Bardo", "Mago", "Feiticeiro", "Bruxo"]},
    {"name_pt": "Contra-mágica", "name_en": "Counterspell", "level": 3, "school": "Abjuração", "classes": ["Mago", "Feiticeiro", "Bruxo"]},
    {"name_pt": "Velocidade", "name_en": "Haste", "level": 3, "school": "Transmutação", "classes": ["Mago", "Feiticeiro"]},
    {"name_pt": "Metamorfose", "name_en": "Polymorph", "level": 4, "school": "Transmutação", "classes": ["Bardo", "Druida", "Mago", "Feiticeiro"]},
    {"name_pt": "Porta Dimensional", "name_en": "Dimension Door", "level": 4, "school": "Conjuração", "classes": ["Bardo", "Mago", "Feiticeiro", "Bruxo"]},
    {"name_pt": "Reviver os Mortos", "name_en": "Raise Dead", "level": 5, "school": "Necromancia", "classes": ["Bardo", "Clérigo", "Paladino"]},
    {"name_pt": "Teletransporte", "name_en": "Teleport", "level": 7, "school": "Conjuração", "classes": ["Bardo", "Mago", "Feiticeiro"]},
    {"name_pt": "Desejo", "name_en": "Wish", "level": 9, "school": "Conjuração", "classes": ["Feiticeiro", "Mago"]},
    # Truques
    {"name_pt": "Raio de Fogo", "name_en": "Fire Bolt", "level": 0, "school": "Evocação", "classes": ["Mago", "Feiticeiro"]},
    {"name_pt": "Rajada Mística", "name_en": "Eldritch Blast", "level": 0, "school": "Evocação", "classes": ["Bruxo"]},
    {"name_pt": "Chama Sagrada", "name_en": "Sacred Flame", "level": 0, "school": "Evocação", "classes": ["Clérigo"]},
    {"name_pt": "Orientação", "name_en": "Guidance", "level": 0, "school": "Adivinhação", "classes": ["Clérigo", "Druida"]},
    {"name_pt": "Mãos Mágicas", "name_en": "Mage Hand", "level": 0, "school": "Conjuração", "classes": ["Bardo", "Mago", "Feiticeiro", "Bruxo"]},
    {"name_pt": "Luz", "name_en": "Light", "level": 0, "school": "Evocação", "classes": ["Bardo", "Clérigo", "Mago", "Feiticeiro"]}
]

# =============================================================================
# 9. FUNÇÕES HELPER PARA COMPONENTES DE UI
# =============================================================================
def get_classes_list() -> List[str]:
    return list(CLASSES_2024.keys())

def get_subclasses_for_class(class_name: str) -> List[str]:
    return CLASSES_2024.get(class_name, {}).get("subclasses", [])

def get_species_list() -> List[str]:
    return list(SPECIES_2024.keys())

def get_backgrounds_list() -> List[str]:
    return list(BACKGROUNDS_2024.keys())

def get_weapons_list() -> List[str]:
    return [f"{w['name']} ({w['damage']} {w['damage_type']} | Maestria: {w['mastery']})" for w in WEAPONS_2024]

def get_armor_list() -> List[str]:
    return [f"{a['name']} (CA {a['ac_base']})" for a in ARMOR_2024]

def get_spells_list(level_filter: Optional[int] = None) -> List[str]:
    if level_filter is not None:
        return [f"{s['name_pt']} ({s['name_en']})" for s in SPELLS_CATALOG if s["level"] == level_filter]
    return [f"{s['name_pt']} ({s['name_en']}) - Nível {s['level']}" for s in SPELLS_CATALOG]

def get_feats_list() -> List[str]:
    return [f"{f['name']} — {f['description'][:60]}..." for f in FEATS_2024]

def get_magic_items_list() -> List[str]:
    return [f"{i['name']} — {i['bonus']}" for i in MAGIC_ITEMS_2024]
