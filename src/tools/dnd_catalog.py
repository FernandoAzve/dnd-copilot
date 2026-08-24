from typing import Dict, List, Any, Optional

# =============================================================================
# 1. ALINHAMENTOS / TENDÊNCIAS OFICIAIS D&D
# =============================================================================
ALIGNMENTS_2024: List[str] = [
    "Leal e Bom (Lawful Good)",
    "Neutro e Bom (Neutral Good)",
    "Caótico e Bom (Chaotic Good)",
    "Leal e Neutro (Lawful Neutral)",
    "Neutro Puro (True Neutral)",
    "Caótico e Neutro (Chaotic Neutral)",
    "Leal e Mau (Lawful Evil)",
    "Neutro e Mau (Neutral Evil)",
    "Caótico e Mau (Chaotic Evil)",
    "Sem Alinhamento (Unaligned)"
]

# =============================================================================
# 2. CLASSES & SUBCLASSES OFICIAIS D&D 2024 (COM DADO DE VIDA E SALVAGUARDAS)
# =============================================================================
CLASSES_2024: Dict[str, Dict[str, Any]] = {
    "Guerreiro": {
        "hit_die": "1d10",
        "primary_ability": "FOR ou DES",
        "saving_throws": ["str", "con"],
        "spell_ability": "None",
        "subclasses": ["Campeão", "Mestre de Batalha", "Cavaleiro Arcano", "Guerreiro Psíquico"],
        "weapon_mastery_count": 3,
        "features": [
            "Segundo Fôlego (Second Wind - 2024)",
            "Estilo de Luta (Fighting Style)",
            "Maestria de Arma (Weapon Mastery)",
            "Surto de Ação (Action Surge)",
            "Ataque Extra (Extra Attack)",
            "Indomável (Indomitable - 2024)",
            "Mente Tática (Tactical Mind - 2024)",
            "Troca Tática (Tactical Shift - 2024)"
        ],
        "description": "Mestre incomparável de todas as armas e táticas de batalha marciais."
    },
    "Mago": {
        "hit_die": "1d6",
        "primary_ability": "INT",
        "saving_throws": ["int", "wis"],
        "spell_ability": "int",
        "subclasses": ["Abjuração", "Adivinhação", "Evocação", "Ilusão"],
        "weapon_mastery_count": 0,
        "features": [
            "Conjuração de Magias (Spellcasting)",
            "Recuperação Arcana (Arcane Recovery)",
            "Grimório de Magias (Spellbook)",
            "Memorizar Magia (Memorize Spell - 2024)",
            "Maestria de Magia (Spell Mastery)"
        ],
        "description": "Erudito arcano capaz de manipular a própria trama da realidade."
    },
    "Ladino": {
        "hit_die": "1d8",
        "primary_ability": "DES",
        "saving_throws": ["dex", "int"],
        "spell_ability": "None",
        "subclasses": ["Assassino", "Ladrão", "Trapaceiro Arcano", "Lâmina da Alma"],
        "weapon_mastery_count": 2,
        "features": [
            "Especialista (Expertise)",
            "Ataque Furtivo (Sneak Attack)",
            "Gíria de Ladrão (Thieves' Cant)",
            "Ação Astuta (Cunning Action)",
            "Golpe Astuto (Cunning Strike - 2024)",
            "Esquiva Sobrenatural (Uncanny Dodge)",
            "Evasão (Evasion)",
            "Sentido Cego (Blindsense)"
        ],
        "description": "Especialista em furtividade, truques periciais e ataques letais."
    },
    "Clérigo": {
        "hit_die": "1d8",
        "primary_ability": "SAB",
        "saving_throws": ["wis", "cha"],
        "spell_ability": "wis",
        "subclasses": ["Domínio da Vida", "Domínio da Luz", "Domínio da Trapaça", "Domínio da Guerra"],
        "weapon_mastery_count": 0,
        "features": [
            "Conjuração Divina (Spellcasting)",
            "Ordem Divina: Protetor ou Taumaturgo (2024)",
            "Canalizar Divindade (Channel Divinity)",
            "Curar / Causar Ferimentos Divinos (2024)",
            "Destruir Mortos-Vivos (Turn Undead)",
            "Intervenção Divina (Divine Intervention)"
        ],
        "description": "Campeão divino canalizando o poder e milagres dos deuses."
    },
    "Paladino": {
        "hit_die": "1d10",
        "primary_ability": "FOR e CAR",
        "saving_throws": ["wis", "cha"],
        "spell_ability": "cha",
        "subclasses": ["Juramento de Devoção", "Juramento de Glória", "Juramento dos Anciãos", "Juramento de Vingança"],
        "weapon_mastery_count": 2,
        "features": [
            "Sentido Divino (Divine Sense)",
            "Cura pelas Mãos (Lay on Hands - Ação Bônus 2024)",
            "Destruição Divina (Divine Smite - 2024)",
            "Estilo de Luta",
            "Canalizar Divindade",
            "Aura de Proteção (Aura of Protection)",
            "Aura de Coragem (Aura of Courage)"
        ],
        "description": "Guerreiro sagrado vinculado por um juramento inquebrável."
    },
    "Bárbaro": {
        "hit_die": "1d12",
        "primary_ability": "FOR",
        "saving_throws": ["str", "con"],
        "spell_ability": "None",
        "subclasses": ["Caminho do Berserker", "Coração Selvagem", "Zelote", "Árvore do Mundo"],
        "weapon_mastery_count": 2,
        "features": [
            "Fúria (Rage - Manutenção de 10 min 2024)",
            "Defesa Sem Armadura (Unarmored Defense)",
            "Ataque Imprudente (Reckless Attack)",
            "Sentido de Perigo (Danger Sense)",
            "Conhecimento Primal (Primal Knowledge - 2024)",
            "Ataque Extra",
            "Movimento Rápido (+3m)",
            "Fúria Brutal (Brutal Strike - 2024)"
        ],
        "description": "Combatente feroz alimentado por uma fúria primal incontrolável."
    },
    "Bardo": {
        "hit_die": "1d8",
        "primary_ability": "CAR",
        "saving_throws": ["dex", "cha"],
        "spell_ability": "cha",
        "subclasses": ["Colégio da Dança", "Colégio do Glamour", "Colégio da Lore", "Colégio da Bravura"],
        "weapon_mastery_count": 0,
        "features": [
            "Conjuração de Magias",
            "Inspiração Bárdica (Bardic Inspiration - Reação/Ação Bônus)",
            "Especialista (Expertise)",
            "Versatilidade (Jack of All Trades)",
            "Fonte de Inspiração",
            "Segredos Mágicos (Magical Secrets - 2024)"
        ],
        "description": "Mestre da música, magia de palavras e inspiração de heróis."
    },
    "Bruxo": {
        "hit_die": "1d8",
        "primary_ability": "CAR",
        "saving_throws": ["wis", "cha"],
        "spell_ability": "cha",
        "subclasses": ["Patrono Arquifada", "Patrono Corruptor", "Patrono Grande Antigo", "Patrono Celestial"],
        "weapon_mastery_count": 0,
        "features": [
            "Magia de Pacto (Pact Magic)",
            "Invocações Místicas (Eldritch Invocations - Nível 1 em 2024)",
            "Dádiva do Pacto: Lâmina, Tomo ou Corrente",
            "Contato Místico",
            "Arcano Menor / Maior"
        ],
        "description": "Portador de segredos arcanos através de um pacto com uma entidade cósmica."
    },
    "Druida": {
        "hit_die": "1d8",
        "primary_ability": "SAB",
        "saving_throws": ["int", "wis"],
        "spell_ability": "wis",
        "subclasses": ["Círculo da Terra", "Círculo da Lua", "Círculo das Estrelas", "Círculo do Mar"],
        "weapon_mastery_count": 0,
        "features": [
            "Conjuração Primal",
            "Ordem Primal: Mago ou Protetor (2024)",
            "Forma Selvagem (Wild Shape - Ação Bônus 2024)",
            "Companheiro Selvagem (Wild Companion)",
            "Golpes Elementais (2024)"
        ],
        "description": "Guardião da natureza capaz de mudar de forma e invocar forças elementais."
    },
    "Feiticeiro": {
        "hit_die": "1d6",
        "primary_ability": "CAR",
        "saving_throws": ["con", "cha"],
        "spell_ability": "cha",
        "subclasses": ["Feitiçaria Dracônica", "Magia Selvagem", "Feitiçaria da Tempestade", "Alma Aberrante"],
        "weapon_mastery_count": 0,
        "features": [
            "Conjuração Inata",
            "Feitiçaria Inata (Innate Sorcery - Vantagem em Ataques Mágicos 2024)",
            "Fonte de Magia (Pontos de Feitiçaria)",
            "Metamagia (Metamagic)",
            "Feitiçaria Arcana"
        ],
        "description": "Conjurador com magia inata pulsando em seu sangue."
    },
    "Guardião": {
        "hit_die": "1d10",
        "primary_ability": "DES e SAB",
        "saving_throws": ["str", "dex"],
        "spell_ability": "wis",
        "subclasses": ["Caçador", "Mestre das Feras", "Rastreador Sombrio", "Guardião Feérico"],
        "weapon_mastery_count": 2,
        "features": [
            "Conjuração de Magias (Nível 1 em 2024)",
            "Inimigo Favorito (Marca do Caçador Grátis 2024)",
            "Especialista (Expertise)",
            "Estilo de Luta",
            "Vagante (Roving - +3m e Escalada/Natação)",
            "Ataque Extra",
            "Véu da Natureza (Invisibilidade como Ação Bônus)"
        ],
        "description": "Rastreador implacável e guerreiro das fronteiras selvagens."
    },
    "Monge": {
        "hit_die": "1d8",
        "primary_ability": "DES e SAB",
        "saving_throws": ["str", "dex"],
        "spell_ability": "None",
        "subclasses": ["Caminho da Mão Aberta", "Caminho da Sombra", "Caminho dos Elementos", "Caminho da Misericórdia"],
        "weapon_mastery_count": 0,
        "features": [
            "Artes Marciais (Dano 1d6 a 1d12)",
            "Defesa Sem Armadura (10 + DES + SAB)",
            "Foco Monástico (Pontos de Foco / Ki)",
            "Rajada de Golpes (Flurry of Blows)",
            "Passo do Vento / Defesa Paciente",
            "Deflexão de Ataques (Deflect Attacks - Físico e Elemental 2024)",
            "Movimento Sem Armadura",
            "Golpe Atordoante (Stunning Strike)"
        ],
        "description": "Artista marcial que canaliza a energia do Ki através de seu corpo."
    }
}

# =============================================================================
# 3. ESPÉCIES / RAÇAS OFICIAIS D&D 2024
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
# 4. ANTECEDENTES OFICIAIS D&D 2024 (COM TALENTOS DE ORIGEM)
# =============================================================================
BACKGROUNDS_2024: Dict[str, Dict[str, Any]] = {
    "Soldado": {"feat": "Valentão de Taverna (Origem)", "attributes": "FOR, CON ou DES", "skills": ["atletismo", "intimidacao"]},
    "Acólito": {"feat": "Iniciado em Magia (Origem)", "attributes": "SAB, INT ou CAR", "skills": ["intuicao", "religiao"]},
    "Sábio": {"feat": "Iniciado em Magia (Origem)", "attributes": "INT, CON ou SAB", "skills": ["arcanismo", "historia"]},
    "Guarda": {"feat": "Alerta (Origem)", "attributes": "FOR, INT ou SAB", "skills": ["atletismo", "percepcao"]},
    "Guia": {"feat": "Iniciado em Magia (Origem)", "attributes": "SAB, CON ou DES", "skills": ["sobrevivencia", "furtividade"]},
    "Fazendeiro": {"feat": "Robusto (Origem)", "attributes": "CON, FOR ou SAB", "skills": ["lidar_com_animais", "natureza"]},
    "Criminoso": {"feat": "Alerta (Origem)", "attributes": "DES, CON ou INT", "skills": ["enganacao", "furtividade"]},
    "Artesão": {"feat": "Artesão Hábil (Origem)", "attributes": "FOR, DES ou INT", "skills": ["investigacao", "persuasao"]},
    "Artista": {"feat": "Músico (Origem)", "attributes": "CAR, DES ou SAB", "skills": ["acrobacia", "atuacao"]},
    "Charlatão": {"feat": "Habilidoso (Origem)", "attributes": "CAR, DES ou CON", "skills": ["enganacao", "prestidigitacao"]},
    "Eremita": {"feat": "Curandeiro (Origem)", "attributes": "SAB, CON ou CAR", "skills": ["medicina", "religiao"]},
    "Marinheiro": {"feat": "Valentão de Taverna (Origem)", "attributes": "FOR, DES ou CON", "skills": ["atletismo", "percepcao"]},
    "Mercador": {"feat": "Sortudo (Origem)", "attributes": "CAR, INT ou CON", "skills": ["lidar_com_animais", "persuasao"]},
    "Nobre": {"feat": "Habilidoso (Origem)", "attributes": "CAR, INT ou SAB", "skills": ["historia", "persuasao"]},
    "Órfão": {"feat": "Sortudo (Origem)", "attributes": "DES, CON ou SAB", "skills": ["furtividade", "prestidigitacao"]},
    "Viajante": {"feat": "Sortudo (Origem)", "attributes": "DES, SAB ou CAR", "skills": ["intuicao", "sobrevivencia"]}
}

# =============================================================================
# 5. ARMAS OFICIAIS COM MAESTRIA DE ARMA 2024 (WEAPON MASTERY)
# =============================================================================
WEAPONS_2024: List[Dict[str, Any]] = [
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
    {"name": "Adaga", "category": "Simples", "damage": "1d4", "damage_type": "Perfurante", "properties": "Acuidade, Leve, Arremesso (6/18m)", "mastery": "Golpe Rápido (Nick)"},
    {"name": "Maça", "category": "Simples", "damage": "1d6", "damage_type": "Contundente", "properties": "-", "mastery": "Fraqueza (Sap)"},
    {"name": "Cajado", "category": "Simples", "damage": "1d6", "damage_type": "Contundente", "properties": "Versátil (1d8)", "mastery": "Derrubar (Topple)"},
    {"name": "Lança", "category": "Simples", "damage": "1d6", "damage_type": "Perfurante", "properties": "Arremesso (6/18m), Versátil (1d8)", "mastery": "Fraqueza (Sap)"},
    {"name": "Machadinha", "category": "Simples", "damage": "1d6", "damage_type": "Cortante", "properties": "Leve, Arremesso (6/18m)", "mastery": "Provocar (Vex)"},
    {"name": "Martelo Leve", "category": "Simples", "damage": "1d4", "damage_type": "Contundente", "properties": "Leve, Arremesso (6/18m)", "mastery": "Golpe Rápido (Nick)"},
    {"name": "Clava", "category": "Simples", "damage": "1d4", "damage_type": "Contundente", "properties": "Leve", "mastery": "Lentidão (Slow)"},
    {"name": "Clava Grande", "category": "Simples", "damage": "1d8", "damage_type": "Contundente", "properties": "Duas Mãos", "mastery": "Empurrão (Push)"},
    {"name": "Arco Longo", "category": "Marcial", "damage": "1d8", "damage_type": "Perfurante", "properties": "Munição (45/180m), Pesada, Duas Mãos", "mastery": "Lentidão (Slow)"},
    {"name": "Arco Curto", "category": "Simples", "damage": "1d6", "damage_type": "Perfurante", "properties": "Munição (24/96m), Duas Mãos", "mastery": "Provocar (Vex)"},
    {"name": "Besta Pesada", "category": "Marcial", "damage": "1d10", "damage_type": "Perfurante", "properties": "Munição (30/120m), Recarga, Pesada, Duas Mãos", "mastery": "Empurrão (Push)"},
    {"name": "Besta Leve", "category": "Simples", "damage": "1d8", "damage_type": "Perfurante", "properties": "Munição (24/96m), Recarga, Duas Mãos", "mastery": "Lentidão (Slow)"},
    {"name": "Besta de Mão", "category": "Marcial", "damage": "1d6", "damage_type": "Perfurante", "properties": "Munição (9/36m), Leve, Recarga", "mastery": "Provocar (Vex)"},
    {"name": "Dardo", "category": "Simples", "damage": "1d4", "damage_type": "Perfurante", "properties": "Acuidade, Arremesso (6/18m)", "mastery": "Provocar (Vex)"},
    {"name": "Funda", "category": "Simples", "damage": "1d4", "damage_type": "Contundente", "properties": "Munição (9/36m)", "mastery": "Lentidão (Slow)"}
]

# =============================================================================
# 6. ARMADURAS & DEFESAS OFICIAIS D&D 2024
# =============================================================================
ARMOR_2024: List[Dict[str, Any]] = [
    {"name": "Sem Armadura (10 + DES)", "category": "Nenhuma", "ac_base": 10, "stealth_disadv": False, "str_req": 0},
    {"name": "Acolchoada (Leve)", "category": "Leve", "ac_base": 11, "stealth_disadv": True, "str_req": 0},
    {"name": "Couro (Leve)", "category": "Leve", "ac_base": 11, "stealth_disadv": False, "str_req": 0},
    {"name": "Couro Batido (Leve)", "category": "Leve", "ac_base": 12, "stealth_disadv": False, "str_req": 0},
    {"name": "Gibão de Peles (Média)", "category": "Média", "ac_base": 12, "stealth_disadv": False, "str_req": 0},
    {"name": "Camisão de Cota de Malha (Média)", "category": "Média", "ac_base": 13, "stealth_disadv": False, "str_req": 0},
    {"name": "Brunea (Média)", "category": "Média", "ac_base": 14, "stealth_disadv": True, "str_req": 0},
    {"name": "Peitoral de Aço (Média)", "category": "Média", "ac_base": 14, "stealth_disadv": False, "str_req": 0},
    {"name": "Meia-Armadura (Média)", "category": "Média", "ac_base": 15, "stealth_disadv": True, "str_req": 0},
    {"name": "Cota de Anéis (Pesada)", "category": "Pesada", "ac_base": 14, "stealth_disadv": True, "str_req": 0},
    {"name": "Cota de Malha (Pesada)", "category": "Pesada", "ac_base": 16, "stealth_disadv": True, "str_req": 13},
    {"name": "Cota de Talas (Pesada)", "category": "Pesada", "ac_base": 17, "stealth_disadv": True, "str_req": 15},
    {"name": "Armadura de Placas Completa (Pesada)", "category": "Pesada", "ac_base": 18, "stealth_disadv": True, "str_req": 15},
    {"name": "Escudo (+2 CA)", "category": "Escudo", "ac_base": 2, "stealth_disadv": False, "str_req": 0}
]

# =============================================================================
# 7. TALENTOS OFICIAIS D&D 2024 (ORIGEM E GERAIS)
# =============================================================================
FEATS_2024: List[Dict[str, Any]] = [
    {"name": "Alerta (Origem)", "type": "Origem", "description": "Adiciona PB na Iniciativa e pode trocar iniciativa com aliado voluntário."},
    {"name": "Iniciado em Magia (Origem)", "type": "Origem", "description": "Aprende 2 truques e 1 magia de 1º nível de Clérigo, Druida ou Mago."},
    {"name": "Sortudo (Origem)", "type": "Origem", "description": "Pontos de Sorte iguais ao PB para rolar com vantagem ou dar desvantagem a inimigos."},
    {"name": "Músico (Origem)", "type": "Origem", "description": "Concede Inspiração Heroica a aliados iguais ao PB após Descanso."},
    {"name": "Curandeiro (Origem)", "type": "Origem", "description": "Gasta Dado de Vida para curar aliados com Kit de Primeiros Socorros e rola dados novamente em 1s."},
    {"name": "Valentão de Taverna (Origem)", "type": "Origem", "description": "Ataques desarmados causam 1d4 + FOR, pode empurrar criaturas e rolar dano novamente em 1s."},
    {"name": "Artesão Hábil (Origem)", "type": "Origem", "description": "Fabricação rápida de itens e desconto de 20% em compras não mágicas."},
    {"name": "Robusto (Origem)", "type": "Origem", "description": "Ganha +2 PV por nível de personagem (retroativo e futuro)."},
    {"name": "Habilidoso (Origem)", "type": "Origem", "description": "Ganha proficiência em quaisquer 3 perícias ou ferramentas à sua escolha."},
    {"name": "Mestre em Armas Grandes (Nível 4+)", "type": "Geral", "description": "Ataque bônus ao acertar crítico; soma PB no dano de armas Pesadas."},
    {"name": "Conjurador de Guerra (Nível 4+)", "type": "Geral", "description": "Vantagem em salvaguardas de Concentração; usa magias em Ataques de Oportunidade."},
    {"name": "Sentinela (Nível 4+)", "type": "Geral", "description": "Ataques de oportunidade reduzem deslocamento a 0 e ignora Desengajar."},
    {"name": "Franco-Atirador (Nível 4+)", "type": "Geral", "description": "Ignora cobertura parcial e pode atirar à queima-roupa sem desvantagem."},
    {"name": "Duelista Defensivo (Nível 4+)", "type": "Geral", "description": "Reação para somar PB na CA contra ataques corpo a corpo com arma de Acuidade."},
    {"name": "Mestre em Escudos (Nível 4+)", "type": "Geral", "description": "Ação Bônus para empurrar com escudo e soma bônus do escudo em salvaguardas de DES."},
    {"name": "Resiliente (Nível 4+)", "type": "Geral", "description": "+1 em um atributo e ganha proficiência na respectiva salvaguarda."}
]

# =============================================================================
# 8. ITENS MÁGICOS & SINTONIAS
# =============================================================================
MAGIC_ITEMS_2024: List[Dict[str, Any]] = [
    {"name": "Capa de Proteção (Sintonizado)", "rarity": "Incomum", "attunement": True, "bonus": "+1 em CA e todas as Salvaguardas"},
    {"name": "Anel de Proteção (Sintonizado)", "rarity": "Raro", "attunement": True, "bonus": "+1 em CA e todas as Salvaguardas"},
    {"name": "Botas Aladas (Sintonizado)", "rarity": "Incomum", "attunement": True, "bonus": "Deslocamento de voo por até 4 horas"},
    {"name": "Braçadeiras de Defesa (Sintonizado)", "rarity": "Raro", "attunement": True, "bonus": "+2 na CA sem armadura e sem escudo"},
    {"name": "Arma +1 (Mágica)", "rarity": "Incomum", "attunement": False, "bonus": "+1 nas jogadas de ataque e dano"},
    {"name": "Arma +2 (Mágica)", "rarity": "Raro", "attunement": False, "bonus": "+2 nas jogadas de ataque e dano"},
    {"name": "Arma +3 (Mágica)", "rarity": "Muito Raro", "attunement": False, "bonus": "+3 nas jogadas de ataque e dano"},
    {"name": "Escudo +1 (Mágico)", "rarity": "Incomum", "attunement": False, "bonus": "+3 total na CA (+2 base + 1 mágico)"},
    {"name": "Poção de Cura Comum (2d4+2)", "rarity": "Comum", "attunement": False, "bonus": "Recupera 2d4+2 PV (Ação Bônus em 2024)"},
    {"name": "Poção de Cura Maior (4d4+4)", "rarity": "Incomum", "attunement": False, "bonus": "Recupera 4d4+4 PV (Ação Bônus em 2024)"},
    {"name": "Varinha de Mísseis Mágicos", "rarity": "Incomum", "attunement": False, "bonus": "7 cargas para conjurar Mísseis Mágicos"},
    {"name": "Cinto de Força do Gigante da Colina (FOR 21)", "rarity": "Raro", "attunement": True, "bonus": "Define a Força em 21 (+5)"},
    {"name": "Amuleto de Saúde (CON 19)", "rarity": "Raro", "attunement": True, "bonus": "Define a Constituição em 19 (+4)"},
    {"name": "Tiara do Intelecto (INT 19)", "rarity": "Incomum", "attunement": True, "bonus": "Define a Inteligência em 19 (+4)"}
]

# =============================================================================
# 9. EQUIPAMENTOS, MOCHILAS & PACOTES OFICIAIS
# =============================================================================
EQUIPMENT_PACKS_2024: List[str] = [
    "Pacote de Explorador de Masmorras (Mochila, pé-de-cabra, martelo, 10 pitões, 10 tochas, pederneira, 10 rações, cantil, corda de cânhamo de 15m)",
    "Pacote de Explorador (Mochila, saco de dormir, kit de refeição, pederneira, 10 tochas, 10 rações, cantil, corda de cânhamo de 15m)",
    "Pacote de Sacerdote (Mochila, cobertor, 10 velas, pederneira, caixa de esmolas, incenso, incensário, vestimentas, 2 dias de rações, cantil)",
    "Pacote de Estudioso (Mochila, livro de estudo, vidro de tinta, pena, 10 folhas de pergaminho, saquinho de areia, faquinha)",
    "Pacote de Artista (Mochila, saco de dormir, 2 fantasias, 5 velas, 5 rações, cantil, kit de disfarce)",
    "Pacote de Diplomata (Baú, 2 estojos para mapas, roupas finas, frasco de tinta, pena, lamparina, óleo, papel, perfume, cera de lacre)",
    "Ferramentas de Ladrão (Thieves' Tools)",
    "Kit de Primeiros Socorros (Healer's Kit - 10 usos)",
    "Kit de Disfarce (Disguise Kit)",
    "Kit de Venenos (Poisoner's Kit)",
    "Kit de Herbalismo (Herbalism Kit)",
    "Símbolo Sagrado (Holy Symbol)",
    "Foco Arcano (Varinha / Cajado / Cristal)",
    "Foco Druídico (Visco / Totem)"
]

# =============================================================================
# 10. IDIOMAS OFICIAIS D&D
# =============================================================================
LANGUAGES_2024: List[str] = [
    "Comum", "Élfico", "Anão", "Dracônico", "Orc", "Halfling", "Gnômico", "Gigante",
    "Goblin", "Abissal", "Celestial", "Infernal", "Primordial", "Silvestre", "Subterrâneo (Undercommon)"
]

# =============================================================================
# 11. PROFICIÊNCIAS DE ARMAS E ARMADURAS PRESETS
# =============================================================================
PROFICIENCIES_ARMOR_WEAPONS: List[str] = [
    "Armaduras Leves", "Armaduras Médias", "Armaduras Pesadas", "Escudos",
    "Armas Simples", "Armas Marciais", "Armas de Fogo"
]

# =============================================================================
# 12. CATÁLOGO DE MAGIAS CANÔNICAS (TRUQUES E CÍRCULOS 1 A 9)
# =============================================================================
SPELLS_CATALOG: List[Dict[str, Any]] = [
    # Truques (Nível 0)
    {"name_pt": "Raio de Fogo", "name_en": "Fire Bolt", "level": 0, "school": "Evocação", "classes": ["Mago", "Feiticeiro"]},
    {"name_pt": "Rajada Mística", "name_en": "Eldritch Blast", "level": 0, "school": "Evocação", "classes": ["Bruxo"]},
    {"name_pt": "Chama Sagrada", "name_en": "Sacred Flame", "level": 0, "school": "Evocação", "classes": ["Clérigo"]},
    {"name_pt": "Orientação", "name_en": "Guidance", "level": 0, "school": "Adivinhação", "classes": ["Clérigo", "Druida"]},
    {"name_pt": "Mãos Mágicas", "name_en": "Mage Hand", "level": 0, "school": "Conjuração", "classes": ["Bardo", "Mago", "Feiticeiro", "Bruxo"]},
    {"name_pt": "Luz", "name_en": "Light", "level": 0, "school": "Evocação", "classes": ["Bardo", "Clérigo", "Mago", "Feiticeiro"]},
    {"name_pt": "Toque Chocante", "name_en": "Shocking Grasp", "level": 0, "school": "Evocação", "classes": ["Mago", "Feiticeiro"]},
    {"name_pt": "Prestidigitação", "name_en": "Prestidigitation", "level": 0, "school": "Transmutação", "classes": ["Bardo", "Mago", "Feiticeiro", "Bruxo"]},
    {"name_pt": "Ilusão Menor", "name_en": "Minor Illusion", "level": 0, "school": "Ilusão", "classes": ["Bardo", "Mago", "Feiticeiro", "Bruxo"]},
    {"name_pt": "Druidismo", "name_en": "Druidcraft", "level": 0, "school": "Transmutação", "classes": ["Druida"]},
    {"name_pt": "Taumaturgia", "name_en": "Thaumaturgy", "level": 0, "school": "Transmutação", "classes": ["Clérigo"]},
    {"name_pt": "Mensagem", "name_en": "Message", "level": 0, "school": "Transmutação", "classes": ["Bardo", "Mago", "Feiticeiro"]},
    {"name_pt": "Chicote de Espinhos", "name_en": "Thorn Whip", "level": 0, "school": "Transmutação", "classes": ["Druida"]},
    {"name_pt": "Golpe Certeiro", "name_en": "True Strike (2024)", "level": 0, "school": "Adivinhação", "classes": ["Bardo", "Mago", "Feiticeiro", "Bruxo"]},
    
    # 1º Nível
    {"name_pt": "Curar Ferimentos", "name_en": "Cure Wounds", "level": 1, "school": "Evocação", "classes": ["Bardo", "Clérigo", "Druida", "Paladino", "Patrulheiro"]},
    {"name_pt": "Palavra Curativa", "name_en": "Healing Word", "level": 1, "school": "Evocação", "classes": ["Bardo", "Clérigo", "Druida"]},
    {"name_pt": "Escudo Arcano", "name_en": "Shield", "level": 1, "school": "Abjuração", "classes": ["Mago", "Feiticeiro"]},
    {"name_pt": "Mísseis Mágicos", "name_en": "Magic Missile", "level": 1, "school": "Evocação", "classes": ["Mago", "Feiticeiro"]},
    {"name_pt": "Raio Guiador", "name_en": "Guiding Bolt", "level": 1, "school": "Evocação", "classes": ["Clérigo"]},
    {"name_pt": "Armadura Arcana", "name_en": "Mage Armor", "level": 1, "school": "Abjuração", "classes": ["Mago", "Feiticeiro"]},
    {"name_pt": "Bênção", "name_en": "Bless", "level": 1, "school": "Encantamento", "classes": ["Clérigo", "Paladino"]},
    {"name_pt": "Bruxaria", "name_en": "Hex", "level": 1, "school": "Encantamento", "classes": ["Bruxo"]},
    {"name_pt": "Marca do Caçador", "name_en": "Hunter's Mark", "level": 1, "school": "Adivinhação", "classes": ["Patrulheiro"]},
    {"name_pt": "Sono", "name_en": "Sleep", "level": 1, "school": "Encantamento", "classes": ["Bardo", "Mago", "Feiticeiro"]},
    {"name_pt": "Onda Trovejante", "name_en": "Thunderwave", "level": 1, "school": "Evocação", "classes": ["Bardo", "Druida", "Mago", "Feiticeiro"]},
    
    # 2º Nível
    {"name_pt": "Passo Nebuloso", "name_en": "Misty Step", "level": 2, "school": "Conjuração", "classes": ["Mago", "Feiticeiro", "Bruxo"]},
    {"name_pt": "Invisibilidade", "name_en": "Invisibility", "level": 2, "school": "Ilusão", "classes": ["Bardo", "Mago", "Feiticeiro", "Bruxo"]},
    {"name_pt": "Arma Espiritual", "name_en": "Spiritual Weapon", "level": 2, "school": "Evocação", "classes": ["Clérigo"]},
    {"name_pt": "Imobilizar Pessoa", "name_en": "Hold Person", "level": 2, "school": "Encantamento", "classes": ["Bardo", "Clérigo", "Druida", "Feiticeiro", "Mago", "Bruxo"]},
    {"name_pt": "Raio Ardente", "name_en": "Scorching Ray", "level": 2, "school": "Evocação", "classes": ["Feiticeiro", "Mago"]},
    {"name_pt": "Sugestão", "name_en": "Suggestion", "level": 2, "school": "Encantamento", "classes": ["Bardo", "Feiticeiro", "Mago", "Bruxo"]},
    {"name_pt": "Reflexos", "name_en": "Mirror Image", "level": 2, "school": "Ilusão", "classes": ["Feiticeiro", "Mago", "Bruxo"]},
    
    # 3º Nível
    {"name_pt": "Bola de Fogo", "name_en": "Fireball", "level": 3, "school": "Evocação", "classes": ["Mago", "Feiticeiro"]},
    {"name_pt": "Contra-mágica", "name_en": "Counterspell", "level": 3, "school": "Abjuração", "classes": ["Mago", "Feiticeiro", "Bruxo"]},
    {"name_pt": "Velocidade", "name_en": "Haste", "level": 3, "school": "Transmutação", "classes": ["Mago", "Feiticeiro"]},
    {"name_pt": "Relâmpago", "name_en": "Lightning Bolt", "level": 3, "school": "Evocação", "classes": ["Feiticeiro", "Mago"]},
    {"name_pt": "Espíritos Guardiões", "name_en": "Spirit Guardians", "level": 3, "school": "Conjuração", "classes": ["Clérigo"]},
    {"name_pt": "Reviver", "name_en": "Revivify", "level": 3, "school": "Necromancia", "classes": ["Clérigo", "Druida", "Paladino"]},
    {"name_pt": "Voo", "name_en": "Fly", "level": 3, "school": "Transmutação", "classes": ["Feiticeiro", "Mago", "Bruxo"]},
    {"name_pt": "Dissipar Magia", "name_en": "Dispel Magic", "level": 3, "school": "Abjuração", "classes": ["Bardo", "Clérigo", "Druida", "Paladino", "Feiticeiro", "Mago", "Bruxo"]},
    
    # 4º Nível
    {"name_pt": "Metamorfose", "name_en": "Polymorph", "level": 4, "school": "Transmutação", "classes": ["Bardo", "Druida", "Mago", "Feiticeiro"]},
    {"name_pt": "Porta Dimensional", "name_en": "Dimension Door", "level": 4, "school": "Conjuração", "classes": ["Bardo", "Mago", "Feiticeiro", "Bruxo"]},
    {"name_pt": "Muralha de Fogo", "name_en": "Wall of Fire", "level": 4, "school": "Evocação", "classes": ["Druida", "Feiticeiro", "Mago"]},
    {"name_pt": "Invisibilidade Maior", "name_en": "Greater Invisibility", "level": 4, "school": "Ilusão", "classes": ["Bardo", "Feiticeiro", "Mago"]},
    
    # 5º Nível
    {"name_pt": "Reviver os Mortos", "name_en": "Raise Dead", "level": 5, "school": "Necromancia", "classes": ["Bardo", "Clérigo", "Paladino"]},
    {"name_pt": "Cone de Frio", "name_en": "Cone of Cold", "level": 5, "school": "Evocação", "classes": ["Feiticeiro", "Mago"]},
    {"name_pt": "Muralha de Força", "name_en": "Wall of Force", "level": 5, "school": "Evocação", "classes": ["Mago"]},
    {"name_pt": "Curar Ferimentos em Massa", "name_en": "Mass Cure Wounds", "level": 5, "school": "Evocação", "classes": ["Bardo", "Clérigo", "Druida"]},
    
    # 6º Nível
    {"name_pt": "Desintegrar", "name_en": "Disintegrate", "level": 6, "school": "Transmutação", "classes": ["Feiticeiro", "Mago"]},
    {"name_pt": "Cura Completa", "name_en": "Heal", "level": 6, "school": "Evocação", "classes": ["Clérigo", "Druida"]},
    
    # 7º Nível
    {"name_pt": "Teletransporte", "name_en": "Teleport", "level": 7, "school": "Conjuração", "classes": ["Bardo", "Mago", "Feiticeiro"]},
    {"name_pt": "Ressurreição", "name_en": "Resurrection", "level": 7, "school": "Necromancia", "classes": ["Bardo", "Clérigo"]},
    
    # 8º Nível
    {"name_pt": "Terremoto", "name_en": "Earthquake", "level": 8, "school": "Evocação", "classes": ["Clérigo", "Druida", "Feiticeiro"]},
    {"name_pt": "Labirinto", "name_en": "Maze", "level": 8, "school": "Conjuração", "classes": ["Mago"]},
    
    # 9º Nível
    {"name_pt": "Desejo", "name_en": "Wish", "level": 9, "school": "Conjuração", "classes": ["Feiticeiro", "Mago"]},
    {"name_pt": "Parar o Tempo", "name_en": "Time Stop", "level": 9, "school": "Transmutação", "classes": ["Feiticeiro", "Mago"]},
    {"name_pt": "Ressurreição Verdadeira", "name_en": "True Resurrection", "level": 9, "school": "Necromancia", "classes": ["Clérigo", "Druida"]}
]

# =============================================================================
# 13. FUNÇÕES HELPER PARA COMPONENTES DE UI
# =============================================================================
def get_classes_list() -> List[str]:
    return list(CLASSES_2024.keys())

def get_subclasses_for_class(class_name: str) -> List[str]:
    return CLASSES_2024.get(class_name, {}).get("subclasses", [])

def get_class_features_list(class_name: str) -> List[str]:
    return CLASSES_2024.get(class_name, {}).get("features", [])

def get_species_list() -> List[str]:
    return list(SPECIES_2024.keys())

def get_backgrounds_list() -> List[str]:
    return list(BACKGROUNDS_2024.keys())

def get_alignments_list() -> List[str]:
    return ALIGNMENTS_2024

def get_weapons_list() -> List[str]:
    return [f"{w['name']} ({w['damage']} {w['damage_type']} | Maestria: {w['mastery']})" for w in WEAPONS_2024]

def get_armor_list() -> List[str]:
    return [f"{a['name']}" for a in ARMOR_2024]

def get_spells_list(level_filter: Optional[int] = None) -> List[str]:
    if level_filter is not None:
        return [f"{s['name_pt']} ({s['name_en']})" for s in SPELLS_CATALOG if s["level"] == level_filter]
    return [f"{s['name_pt']} ({s['name_en']}) - Nível {s['level']}" for s in SPELLS_CATALOG]

def get_cantrips_list() -> List[str]:
    return [f"{s['name_pt']} ({s['name_en']})" for s in SPELLS_CATALOG if s["level"] == 0]

def get_leveled_spells_list() -> List[str]:
    return [f"{s['name_pt']} ({s['name_en']}) - Nível {s['level']}" for s in SPELLS_CATALOG if s["level"] > 0]

def get_feats_list() -> List[str]:
    return [f"{f['name']}" for f in FEATS_2024]

def get_magic_items_list() -> List[str]:
    return [f"{i['name']} — {i['bonus']}" for i in MAGIC_ITEMS_2024]

def get_equipment_packs_list() -> List[str]:
    return EQUIPMENT_PACKS_2024

def get_languages_list() -> List[str]:
    return LANGUAGES_2024

def get_armor_weapon_proficiencies_list() -> List[str]:
    return PROFICIENCIES_ARMOR_WEAPONS
