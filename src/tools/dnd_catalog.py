from typing import Dict, List, Any, Optional

# =============================================================================
# 1. ALINHAMENTOS / TENDÊNCIAS OFICIAIS D&D (100% COMPLETO)
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
    "Sem Alinhamento / Não Alinhado (Unaligned)"
]

# =============================================================================
# 2. TODAS AS 12 CLASSES & 48 SUBCLASSES OFICIAIS D&D 2024
# =============================================================================
CLASSES_2024: Dict[str, Dict[str, Any]] = {
    "Guerreiro": {
        "hit_die": "1d10",
        "primary_ability": "FOR ou DES",
        "saving_throws": ["str", "con"],
        "spell_ability": "None",
        "subclasses": [
            "Campeão (Champion)",
            "Mestre de Batalha (Battle Master)",
            "Cavaleiro Arcano (Eldritch Knight)",
            "Guerreiro Psíquico (Psi Warrior)"
        ],
        "weapon_mastery_count": 3,
        "features": [
            "Segundo Fôlego (Second Wind - Ação Bônus 2024)",
            "Estilo de Luta (Fighting Style)",
            "Maestria de Arma (Weapon Mastery - 3 armas)",
            "Mente Tática (Tactical Mind - Adiciona 1d10 em testes de perícia)",
            "Surto de Ação (Action Surge - 1 Ação adicional)",
            "Ataque Extra (Extra Attack - 2 ataques no Nível 5, 3 no Nv 11, 4 no Nv 20)",
            "Troca Tática (Tactical Shift - Movimento sem provocar oportunidade)",
            "Indomável (Indomitable - Rola novamente salvaguarda com +Nível)",
            "Mestre das Armas (Master of Armaments)",
            "Mestre Tático (Tactical Master - Aplica Push, Sap ou Slow)",
            "Vigor Inabalável (Unwavering Vigor)"
        ],
        "description": "Mestre incomparável de todas as armas, armaduras e manobras táticas marciais."
    },
    "Mago": {
        "hit_die": "1d6",
        "primary_ability": "INT",
        "saving_throws": ["int", "wis"],
        "spell_ability": "int",
        "subclasses": [
            "Escola de Abjuração (Abjuration)",
            "Escola de Adivinhação (Divination)",
            "Escola de Evocação (Evocation)",
            "Escola de Ilusão (Illusion)"
        ],
        "weapon_mastery_count": 0,
        "features": [
            "Conjuração Arcana (Spellcasting)",
            "Recuperação Arcana (Arcane Recovery - Recupera espaços em descanso)",
            "Grimório de Magias (Spellbook - Grava rituais e magias)",
            "Erudito (Scholar - Especialista em perícia de INT)",
            "Memorizar Magia (Memorize Spell - Troca 1 magia preparada por descanso)",
            "Maestria de Magia (Spell Mastery - Truques de 1º e 2º círculo infinitos)",
            "Assinatura Mágica (Signature Spells - Magias de 3º círculo preparadas grátis)"
        ],
        "description": "Erudito supremo capaz de manipular a própria trama da realidade e do multiverso."
    },
    "Ladino": {
        "hit_die": "1d8",
        "primary_ability": "DES",
        "saving_throws": ["dex", "int"],
        "spell_ability": "None",
        "subclasses": [
            "Assassino (Assassin)",
            "Ladrão (Thief)",
            "Trapaceiro Arcano (Arcane Trickster)",
            "Lâmina da Alma (Soulknife)"
        ],
        "weapon_mastery_count": 2,
        "features": [
            "Especialista (Expertise - Dobro do PB em 2 perícias)",
            "Ataque Furtivo (Sneak Attack - Dano extra escalando de 1d6 a 10d6)",
            "Gíria de Ladrão (Thieves' Cant)",
            "Maestria de Arma (Weapon Mastery - 2 armas)",
            "Ação Astuta (Cunning Action - Disparada, Desengajar ou Esconder como Ação Bônus)",
            "Golpe Astuto (Cunning Strike - Troca 1d6 de dano furtivo por Efeitos de Controle)",
            "Esquiva Sobrenatural (Uncanny Dodge - Reduz dano sofrido pela metade)",
            "Evasão (Evasion - 0 dano em sucesso de DES, metade em falha)",
            "Talento Confiável (Reliable Talent - Mínimo 10 no d20 em perícias)",
            "Sentido Cego (Blindsense - 3m)",
            "Mente Escorregadia (Slippery Mind - Proficiência em SAB e CAR)",
            "Golpe de Sorte (Stroke of Luck - Transforma erro em sucesso automático)"
        ],
        "description": "Especialista letal em furtividade, truques periciais, infiltração e ataques de precisão."
    },
    "Clérigo": {
        "hit_die": "1d8",
        "primary_ability": "SAB",
        "saving_throws": ["wis", "cha"],
        "spell_ability": "wis",
        "subclasses": [
            "Domínio da Vida (Life Domain)",
            "Domínio da Luz (Light Domain)",
            "Domínio da Trapaça (Trickery Domain)",
            "Domínio da Guerra (War Domain)"
        ],
        "weapon_mastery_count": 0,
        "features": [
            "Conjuração Divina (Spellcasting)",
            "Ordem Divina: Protetor (Armaduras Pesadas/Armas Marciais) ou Taumaturgo (Truque extra/INT+SAB)",
            "Canalizar Divindade (Channel Divinity)",
            "Centelha Divina (Divine Spark - Cura ou Dano Radiante/Necrótico por Canalizar)",
            "Destruir Mortos-Vivos (Turn Undead - Afasta ou destrói mortos-vivos)",
            "Ataque Abençoado / Golpe Radiante (+1d8 de dano)",
            "Intervenção Divina (Divine Intervention - Conjurada sem falha 1x/dia no Nv 10)",
            "Intervenção Divina Maior (Desejo concedido no Nível 20)"
        ],
        "description": "Campeão divino canalizando o poder, milagres e ira dos deuses."
    },
    "Paladino": {
        "hit_die": "1d10",
        "primary_ability": "FOR e CAR",
        "saving_throws": ["wis", "cha"],
        "spell_ability": "cha",
        "subclasses": [
            "Juramento de Devoção (Oath of Devotion)",
            "Juramento de Glória (Oath of Glory)",
            "Juramento dos Anciãos (Oath of the Ancients)",
            "Juramento de Vingança (Oath of Vengeance)"
        ],
        "weapon_mastery_count": 2,
        "features": [
            "Sentido Divino (Divine Sense - Detecta celestiais, ínferos e mortos-vivos)",
            "Cura pelas Mãos (Lay on Hands - Reserva de 5x Nível PV, Ação Bônus 2024)",
            "Conjuração Divina (Spellcasting - Nível 1)",
            "Maestria de Arma (Weapon Mastery - 2 armas)",
            "Estilo de Luta (Fighting Style)",
            "Destruição Divina (Divine Smite - Dano radiante concentrado)",
            "Canalizar Divindade (Channel Divinity)",
            "Ataque Extra (Extra Attack)",
            "Aura de Proteção (Aura of Protection - Soma Mod CAR em todas as salvaguardas)",
            "Aura de Coragem (Aura of Courage - Imunidade a Amedrontado)",
            "Golpe Radiante Aprimorado (+1d8 radiante permanente em todos os ataques)",
            "Aura Expandida (9 metros)",
            "Campeão Sagrado (Transformação final de Juramento)"
        ],
        "description": "Guerreiro sagrado vinculado por um juramento inquebrável de honra, luz e justiça."
    },
    "Bárbaro": {
        "hit_die": "1d12",
        "primary_ability": "FOR",
        "saving_throws": ["str", "con"],
        "spell_ability": "None",
        "subclasses": [
            "Caminho do Berserker (Path of the Berserker)",
            "Caminho do Coração Selvagem (Wild Heart)",
            "Caminho do Zelote (Path of the Zealot)",
            "Caminho da Árvore do Mundo (World Tree)"
        ],
        "weapon_mastery_count": 2,
        "features": [
            "Fúria Primal (Rage - Duração de 10 min, mantida com Ação Bônus ou Forçar Salvaguarda)",
            "Defesa Sem Armadura (10 + DES + CON)",
            "Maestria de Arma (Weapon Mastery - 2 armas)",
            "Ataque Imprudente (Reckless Attack - Vantagem em ataques corpo a corpo)",
            "Sentido de Perigo (Danger Sense - Vantagem em salvaguardas de DES)",
            "Conhecimento Primal (Primal Knowledge - Usa FOR para Percepção, Furtividade, Sobrevivência)",
            "Ataque Extra (Extra Attack)",
            "Movimento Rápido (+3 metros)",
            "Instinto Feral (Vantagem na Iniciativa)",
            "Golpe Brutal (Brutal Strike - Troca vantagem por efeitos de empurrão ou redução de velocidade)",
            "Fúria Implacável (Permanece consciente com teste de CON)",
            "Fúria Persistente (A Fúria só termina se cair inconsciente)",
            "Poder Primal (+4 em FOR e CON até o máximo de 25)"
        ],
        "description": "Combatente feroz alimentado por uma fúria primal incontrolável que desafia a morte."
    },
    "Bardo": {
        "hit_die": "1d8",
        "primary_ability": "CAR",
        "saving_throws": ["dex", "cha"],
        "spell_ability": "cha",
        "subclasses": [
            "Colégio da Dança (College of Dance)",
            "Colégio do Glamour (College of Glamour)",
            "Colégio do Conhecimento (College of Lore)",
            "Colégio da Bravura (College of Valor)"
        ],
        "weapon_mastery_count": 0,
        "features": [
            "Conjuração de Magias (Spellcasting)",
            "Inspiração Bárdica (Bardic Inspiration - Dado d6 a d12, Ação Bônus ou Reação)",
            "Especialista (Expertise - Dobro de proficiência em 4 perícias)",
            "Versatilidade (Jack of All Trades - Metade do PB em testes sem proficiência)",
            "Canção de Descanso (Song of Rest)",
            "Fonte de Inspiração (Recupera dados de Inspiração em Descanso Curto)",
            "Contra-feitiço Bárdico (Countercharm)",
            "Segredos Mágicos (Magical Secrets - Escolhe magias de Clérigo, Druida ou Mago)",
            "Inspiração Superior (Ganha dado de inspiração no início do combate se estiver sem)"
        ],
        "description": "Mestre da música, magia de palavras, conhecimento enciclopédico e inspiração de heróis."
    },
    "Bruxo": {
        "hit_die": "1d8",
        "primary_ability": "CAR",
        "saving_throws": ["wis", "cha"],
        "spell_ability": "cha",
        "subclasses": [
            "Patrono Arquifada (Archfey Patron)",
            "Patrono Corruptor (Fiend Patron)",
            "Patrono Grande Antigo (Great Old One)",
            "Patrono Celestial (Celestial Patron)"
        ],
        "weapon_mastery_count": 0,
        "features": [
            "Magia de Pacto (Pact Magic - Espaços sempre no nível máximo, recuperados em Descanso Curto)",
            "Invocações Místicas (Eldritch Invocations - Nível 1, escolhe até 8 invocações)",
            "Dádiva do Pacto: Pacto da Lâmina, Tomo ou Corrente",
            "Mestre Místico (Magical Cunning - Recupera metade dos espaços em 1 minuto)",
            "Arcano Menor / Maior (Mystic Arcanum - Magias de 6º, 7º, 8º e 9º nível)",
            "Mestre do Éter (Eldritch Master - Recupera todos os espaços de pacto em 1 minuto)"
        ],
        "description": "Portador de segredos cósmicos arcanos através de um pacto com uma entidade transcendental."
    },
    "Druida": {
        "hit_die": "1d8",
        "primary_ability": "SAB",
        "saving_throws": ["int", "wis"],
        "spell_ability": "wis",
        "subclasses": [
            "Círculo da Terra (Circle of the Land)",
            "Círculo da Lua (Circle of the Moon)",
            "Círculo das Estrelas (Circle of Stars)",
            "Círculo do Mar (Circle of the Sea)"
        ],
        "weapon_mastery_count": 0,
        "features": [
            "Conjuração Primal (Spellcasting)",
            "Ordem Primal: Magista (Truque extra/INT+SAB) ou Protetor (Armaduras Médias/Armas Marciais)",
            "Forma Selvagem (Wild Shape - Ação Bônus 2024, ganha PV temporários iguais ao dobro do nível)",
            "Companheiro Selvagem (Wild Companion - Invoca familiar espiritual)",
            "Golpes Elementais (Elemental Fury - Dano de Fogo, Frio, Relâmpago ou Trovoada nos ataques)",
            "Resistência da Natureza",
            "Forma Selvagem Melhorada (Voo, Natação e Tamanho Grande)",
            "Arquidruida (Usos ilimitados de Forma Selvagem e ignora componentes verbais/somáticos)"
        ],
        "description": "Guardião supremo da natureza capaz de mudar de forma física e invocar forças elementais."
    },
    "Feiticeiro": {
        "hit_die": "1d6",
        "primary_ability": "CAR",
        "saving_throws": ["con", "cha"],
        "spell_ability": "cha",
        "subclasses": [
            "Feitiçaria Dracônica (Draconic Sorcery)",
            "Magia Selvagem (Wild Magic)",
            "Feitiçaria da Tempestade (Storm Sorcery)",
            "Alma Aberrante (Aberrant Mind)"
        ],
        "weapon_mastery_count": 0,
        "features": [
            "Conjuração Inata (Spellcasting)",
            "Feitiçaria Inata (Innate Sorcery - Ação Bônus: +1 na CD e Vantagem em Ataques Mágicos 2024)",
            "Fonte de Magia (Font of Magic - Pontos de Feitiçaria para criar espaços de magia)",
            "Metamagia (Metamagic - Magia Acelerada, Duplicada, Sutil, Estendida, Cuidadosa, Potente)",
            "Feitiçaria Arcana",
            "Metamagia Espontânea (Troca opções de metamagia em descanso longo)",
            "Restauração Feiticeira (Sorcerous Restoration - Recupera pontos de feitiçaria em descanso curto)",
            "Apoteose Feiticeira (Usa 1 opção de metamagia sem custo todo turno)"
        ],
        "description": "Conjurador nato com magia pura e primordial pulsando diretamente em seu sangue."
    },
    "Guardião": {
        "hit_die": "1d10",
        "primary_ability": "DES e SAB",
        "saving_throws": ["str", "dex"],
        "spell_ability": "wis",
        "subclasses": [
            "Caçador (Hunter)",
            "Mestre das Feras (Beast Master)",
            "Rastreador Sombrio (Gloom Stalker)",
            "Guardião Feérico (Fey Wanderer)"
        ],
        "weapon_mastery_count": 2,
        "features": [
            "Conjuração Selvagem (Spellcasting - Nível 1 em 2024)",
            "Inimigo Favorito (Favored Enemy - Marca do Caçador grátis sem gastar espaço)",
            "Maestria de Arma (Weapon Mastery - 2 armas)",
            "Especialista (Expertise - Dobro de PB em 2 perícias)",
            "Estilo de Luta (Fighting Style)",
            "Vagante (Roving - +3m de deslocamento, escalada e natação)",
            "Ataque Extra (Extra Attack)",
            "Sem Rastro (Pass Without Trace aprimorado)",
            "Alívio da Natureza (Tireless - PV temporários por descanso e remove exaustão)",
            "Véu da Natureza (Nature's Veil - Invisibilidade como Ação Bônus)",
            "Sentidos Ferais (Feral Senses - Visão às cegas)",
            "Matador Supremo (Soma SAB no ataque ou dano)"
        ],
        "description": "Rastreador implacável, atirador mestre e guerreiro das fronteiras selvagens e inexploradas."
    },
    "Monge": {
        "hit_die": "1d8",
        "primary_ability": "DES e SAB",
        "saving_throws": ["str", "dex"],
        "spell_ability": "None",
        "subclasses": [
            "Caminho da Mão Aberta (Open Hand)",
            "Caminho da Sombra (Shadow)",
            "Caminho dos Elementos (Four Elements)",
            "Caminho da Misericórdia (Mercy)"
        ],
        "weapon_mastery_count": 0,
        "features": [
            "Artes Marciais (Martial Arts - Dano desarmado 1d6 a 1d12 com DES)",
            "Defesa Sem Armadura (10 + DES + SAB)",
            "Foco Monástico (Focus Points / Ki)",
            "Rajada de Golpes (Flurry of Blows - 2 ataques desarmados extras)",
            "Passo do Vento (Step of the Wind - Desengajar e Disparada com salto duplo)",
            "Defesa Paciente (Patient Defense - Esquiva como Ação Bônus)",
            "Deflexão de Ataques (Deflect Attacks - Reduz dano Físico e Elemental 2024)",
            "Movimento Sem Armadura (+3m a +9m, anda sobre água e paredes)",
            "Queda Lenta (Slow Fall)",
            "Golpe Atordoante (Stunning Strike - Atordoa criaturas atingidas)",
            "Golpes Fortificados (Dano de Força nos ataques desarmados)",
            "Evasão (Evasion)",
            "Mente Tranquila (Imunidade a Amedrontado e Enfeitiçado)",
            "Defesa Perfeita (Resistência a quase todos os danos)",
            "Auto-Restauração (Remove condições negativas)",
            "Corpo Vazio (Invisibilidade e Resistência Astral)",
            "Corpo Perfeito (Recupera pontos de Foco ao rolar iniciativa)"
        ],
        "description": "Artista marcial lendário que canaliza a energia do Ki através de seu corpo e alma."
    }
}

# =============================================================================
# 3. TODAS AS 10 ESPÉCIES / RAÇAS OFICIAIS D&D 2024
# =============================================================================
SPECIES_2024: Dict[str, Dict[str, Any]] = {
    "Humano": {
        "speed": "9m (30 ft)",
        "traits": "Talento de Origem Adicional, Inspiração Heroica após cada Descanso Longo, Proficiência em 1 Perícia à sua escolha."
    },
    "Elfo": {
        "speed": "9m (30 ft)",
        "traits": "Visão no Escuro (18m), Ancestral Feérico (Vantagem contra Enfeitiçado), Transe (Descanso Longo em 4 horas), Linhagem Élfica (Alto Elfo: Truque de Mago; Elfo da Floresta: Deslocamento 10,5m; Drow: Visão no Escuro 36m e Magia Drow)."
    },
    "Anão": {
        "speed": "9m (30 ft)",
        "traits": "Visão no Escuro (36m), Resiliência Anã (Resistência a Dano de Veneno e Vantagem contra Envenenado), Robustez Anã (+1 PV por nível de personagem), Sentido das Rochas (Visão de Tremor em pedra)."
    },
    "Halfling": {
        "speed": "9m (30 ft)",
        "traits": "Sortudo (Rola novamente qualquer resultado 1 em jogadas de ataque, testes de atributo ou salvaguardas no d20), Corajoso (Vantagem contra Amedrontado), Agilidade Halfling (Pode mover-se através do espaço de qualquer criatura maior)."
    },
    "Draconato": {
        "speed": "9m (30 ft)",
        "traits": "Arma de Sopro Dracônica (Cone de 4,5m ou Linha de 9m causando 1d10 a 4d10 do tipo do dragão), Resistência Elemental ao dano do sopro, Visão no Escuro (18m), Asas Dracônicas (Voo no Nível 5 por 10 minutos)."
    },
    "Gnomo": {
        "speed": "9m (30 ft)",
        "traits": "Astúcia Gnômica (Vantagem em todas as Salvaguardas de Inteligência, Sabedoria e Carisma), Visão no Escuro (18m), Linhagem Gnômica (Gnomo da Floresta: Ilusão Menor e Falar com Pequenos Animais; Gnomo das Rochas: Prestidigitação e Criação de Mecanismos)."
    },
    "Golias": {
        "speed": "10,5m (35 ft)",
        "traits": "Ancestral Gigante (Poder Sobrenatural: Gigante da Nuvem [Teletransporte 9m], Fogo [1d10 fogo], Gelo [1d6 frio e lentidão], Colina [Derruba], Pedra [Reduz dano], Tempestade [Reação com raio]), Atleta Natural, Forma Gigante (Torna-se Grande com Vantagem em FOR e +3m no Nv 5)."
    },
    "Orc": {
        "speed": "9m (30 ft)",
        "traits": "Investida Adrenérgica (Disparada como Ação Bônus ganhando PV temporários iguais ao PB), Resistência Implacável (Quando reduzido a 0 PV, cai para 1 PV em vez disso 1x/dia), Visão no Escuro (36m), Porte Robusto (Capacidade de carga dobrada)."
    },
    "Tiferino": {
        "speed": "9m (30 ft)",
        "traits": "Visão no Escuro (21m), Legado Sobrenatural (Infernal: Resistência a Fogo, Taumaturgia, Mãos Flamejantes, Raio Ardente; Abissal: Resistência a Veneno, Rajada de Veneno, Raio de Enfraquecimento; Ctônico: Resistência a Necrótico, Toque Necrótico, Vitalidade Falsa)."
    },
    "Aasimar": {
        "speed": "9m (30 ft)",
        "traits": "Visão no Escuro (18m), Mãos Curativas (Cura criatura com dados d4 iguais ao PB), Resistência Celestial (Resistência a Dano Radiante e Necrótico), Transformação Celestial (Nível 3: Asas Radiantes de Voo ou Sudário Necrótico com dano extra)."
    }
}

# =============================================================================
# 4. TODOS OS 16 ANTECEDENTES OFICIAIS D&D 2024 (BACKGROUNDS)
# =============================================================================
BACKGROUNDS_2024: Dict[str, Dict[str, Any]] = {
    "Soldado": {"feat": "Valentão de Taverna (Origem)", "attributes": "FOR, CON ou DES", "skills": ["atletismo", "intimidacao"]},
    "Acólito": {"feat": "Iniciado em Magia: Clérigo (Origem)", "attributes": "SAB, INT ou CAR", "skills": ["intuicao", "religiao"]},
    "Sábio": {"feat": "Iniciado em Magia: Mago (Origem)", "attributes": "INT, CON ou SAB", "skills": ["arcanismo", "historia"]},
    "Guarda": {"feat": "Alerta (Origem)", "attributes": "FOR, INT ou SAB", "skills": ["atletismo", "percepcao"]},
    "Guia": {"feat": "Iniciado em Magia: Druida (Origem)", "attributes": "SAB, CON ou DES", "skills": ["sobrevivencia", "furtividade"]},
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
# 5. TODAS AS 37 ARMAS OFICIAIS COM MAESTRIA DE ARMA 2024 (WEAPON MASTERY)
# =============================================================================
WEAPONS_2024: List[Dict[str, Any]] = [
    # Marciais Corpo a Corpo
    {"name": "Espada Longa (Longsword)", "category": "Marcial", "damage": "1d8", "damage_type": "Cortante", "properties": "Versátil (1d10)", "mastery": "Empurrão (Push - Empurra o alvo até 3m)"},
    {"name": "Espada Grande (Greatsword)", "category": "Marcial", "damage": "2d6", "damage_type": "Cortante", "properties": "Pesada, Duas Mãos", "mastery": "Rasgar (Graze - Causa Mod de FOR mesmo errando o ataque)"},
    {"name": "Rapieira (Rapier)", "category": "Marcial", "damage": "1d8", "damage_type": "Perfurante", "properties": "Acuidade", "mastery": "Provocar (Vex - Vantagem no próximo ataque contra o mesmo alvo)"},
    {"name": "Machado de Batalha (Battleaxe)", "category": "Marcial", "damage": "1d8", "damage_type": "Cortante", "properties": "Versátil (1d10)", "mastery": "Derrubar (Topple - Força salvaguarda de CON ou alvo cai Caído)"},
    {"name": "Machado Grande (Greataxe)", "category": "Marcial", "damage": "1d12", "damage_type": "Cortante", "properties": "Pesada, Duas Mãos", "mastery": "Cutilada (Cleave - Faz ataque extra contra criatura adjacente)"},
    {"name": "Alabarda (Halberd)", "category": "Marcial", "damage": "1d10", "damage_type": "Cortante", "properties": "Pesada, Alcance, Duas Mãos", "mastery": "Cutilada (Cleave - Ataque extra em criatura adjacente)"},
    {"name": "Glaive", "category": "Marcial", "damage": "1d10", "damage_type": "Cortante", "properties": "Pesada, Alcance, Duas Mãos", "mastery": "Rasgar (Graze - Causa Mod FOR mesmo errando)"},
    {"name": "Mangual (Flail)", "category": "Marcial", "damage": "1d8", "damage_type": "Contundente", "properties": "-", "mastery": "Fraqueza (Sap - Alvo tem desvantagem no próximo ataque)"},
    {"name": "Martelo de Guerra (Warhammer)", "category": "Marcial", "damage": "1d8", "damage_type": "Contundente", "properties": "Versátil (1d10)", "mastery": "Empurrão (Push - Empurra o alvo até 3m)"},
    {"name": "Malho (Maul)", "category": "Marcial", "damage": "2d6", "damage_type": "Contundente", "properties": "Pesada, Duas Mãos", "mastery": "Derrubar (Topple - Alvo cai Caído se falhar na salvaguarda)"},
    {"name": "Maça Estrela (Morningstar)", "category": "Marcial", "damage": "1d8", "damage_type": "Perfurante", "properties": "-", "mastery": "Fraqueza (Sap - Desvantagem no próximo ataque do inimigo)"},
    {"name": "Cimitarra (Scimitar)", "category": "Marcial", "damage": "1d6", "damage_type": "Cortante", "properties": "Acuidade, Leve", "mastery": "Golpe Rápido (Nick - Ataque com segunda arma faz parte da Ação de Ataque)"},
    {"name": "Espada Curta (Shortsword)", "category": "Marcial", "damage": "1d6", "damage_type": "Perfurante", "properties": "Acuidade, Leve", "mastery": "Provocar (Vex - Vantagem no próximo ataque)"},
    {"name": "Tridente (Trident)", "category": "Marcial", "damage": "1d8", "damage_type": "Perfurante", "properties": "Arremesso (6/18m), Versátil (1d10)", "mastery": "Derrubar (Topple - Alvo cai Caído se falhar na salvaguarda)"},
    {"name": "Pique (Pike)", "category": "Marcial", "damage": "1d10", "damage_type": "Perfurante", "properties": "Pesada, Alcance, Duas Mãos", "mastery": "Empurrão (Push - Empurra até 3m)"},
    {"name": "Lança de Montaria (Lance)", "category": "Marcial", "damage": "1d10", "damage_type": "Perfurante", "properties": "Alcance, Pesada, Uma mão montado", "mastery": "Derrubar (Topple - Alvo cai Caído)"},
    {"name": "Chicote (Whip)", "category": "Marcial", "damage": "1d4", "damage_type": "Cortante", "properties": "Acuidade, Alcance", "mastery": "Lentidão (Slow - Reduz velocidade do alvo em 3m)"},
    {"name": "Picareta de Guerra (War Pick)", "category": "Marcial", "damage": "1d8", "damage_type": "Perfurante", "properties": "Versátil (1d10)", "mastery": "Fraqueza (Sap - Desvantagem no ataque inimigo)"},

    # Simples Corpo a Corpo
    {"name": "Adaga (Dagger)", "category": "Simples", "damage": "1d4", "damage_type": "Perfurante", "properties": "Acuidade, Leve, Arremesso (6/18m)", "mastery": "Golpe Rápido (Nick - Ataque bônus integrado na ação)"},
    {"name": "Maça (Mace)", "category": "Simples", "damage": "1d6", "damage_type": "Contundente", "properties": "-", "mastery": "Fraqueza (Sap - Desvantagem no ataque do alvo)"},
    {"name": "Cajado (Quarterstaff)", "category": "Simples", "damage": "1d6", "damage_type": "Contundente", "properties": "Versátil (1d8)", "mastery": "Derrubar (Topple - Derruba o inimigo)"},
    {"name": "Lança (Spear)", "category": "Simples", "damage": "1d6", "damage_type": "Perfurante", "properties": "Arremesso (6/18m), Versátil (1d8)", "mastery": "Fraqueza (Sap - Desvantagem no ataque inimigo)"},
    {"name": "Machadinha (Handaxe)", "category": "Simples", "damage": "1d6", "damage_type": "Cortante", "properties": "Leve, Arremesso (6/18m)", "mastery": "Provocar (Vex - Vantagem no próximo ataque)"},
    {"name": "Martelo Leve (Light Hammer)", "category": "Simples", "damage": "1d4", "damage_type": "Contundente", "properties": "Leve, Arremesso (6/18m)", "mastery": "Golpe Rápido (Nick - Ataque duplo integrado)"},
    {"name": "Clava (Club)", "category": "Simples", "damage": "1d4", "damage_type": "Contundente", "properties": "Leve", "mastery": "Lentidão (Slow - Reduz velocidade do inimigo em 3m)"},
    {"name": "Clava Grande (Greatclub)", "category": "Simples", "damage": "1d8", "damage_type": "Contundente", "properties": "Duas Mãos", "mastery": "Empurrão (Push - Empurra o alvo até 3m)"},
    {"name": "Foice Curta (Sickle)", "category": "Simples", "damage": "1d4", "damage_type": "Cortante", "properties": "Leve", "mastery": "Golpe Rápido (Nick)"},
    {"name": "Lança Curta (Javelin)", "category": "Simples", "damage": "1d6", "damage_type": "Perfurante", "properties": "Arremesso (9/36m)", "mastery": "Lentidão (Slow - Reduz velocidade)"},

    # Armas à Distância
    {"name": "Arco Longo (Longbow)", "category": "Marcial", "damage": "1d8", "damage_type": "Perfurante", "properties": "Munição (45/180m), Pesada, Duas Mãos", "mastery": "Lentidão (Slow - Reduz velocidade em 3m)"},
    {"name": "Arco Curto (Shortbow)", "category": "Simples", "damage": "1d6", "damage_type": "Perfurante", "properties": "Munição (24/96m), Duas Mãos", "mastery": "Provocar (Vex - Vantagem no próximo disparo)"},
    {"name": "Besta Pesada (Heavy Crossbow)", "category": "Marcial", "damage": "1d10", "damage_type": "Perfurante", "properties": "Munição (30/120m), Recarga, Pesada, Duas Mãos", "mastery": "Empurrão (Push - Empurra o alvo 3m para trás)"},
    {"name": "Besta Leve (Light Crossbow)", "category": "Simples", "damage": "1d8", "damage_type": "Perfurante", "properties": "Munição (24/96m), Recarga, Duas Mãos", "mastery": "Lentidão (Slow - Reduz velocidade em 3m)"},
    {"name": "Besta de Mão (Hand Crossbow)", "category": "Marcial", "damage": "1d6", "damage_type": "Perfurante", "properties": "Munição (9/36m), Leve, Recarga", "mastery": "Provocar (Vex - Vantagem no próximo ataque)"},
    {"name": "Dardo (Dart)", "category": "Simples", "damage": "1d4", "damage_type": "Perfurante", "properties": "Acuidade, Arremesso (6/18m)", "mastery": "Provocar (Vex - Vantagem no ataque)"},
    {"name": "Funda (Sling)", "category": "Simples", "damage": "1d4", "damage_type": "Contundente", "properties": "Munição (9/36m)", "mastery": "Lentidão (Slow - Reduz velocidade em 3m)"},
    {"name": "Zarabatana (Blowgun)", "category": "Marcial", "damage": "1", "damage_type": "Perfurante", "properties": "Munição (7,5/30m), Recarga", "mastery": "Provocar (Vex)"},
    {"name": "Rede (Net)", "category": "Simples", "damage": "0", "damage_type": "Especial", "properties": "Arremesso (1,5/4,5m), Deixa alvo Preso", "mastery": "Lentidão (Slow)"}
]

# =============================================================================
# 6. TODAS AS 13 ARMADURAS & DEFESAS OFICIAIS D&D 2024
# =============================================================================
ARMOR_2024: List[Dict[str, Any]] = [
    {"name": "Sem Armadura (10 + DES)", "category": "Nenhuma", "ac_base": 10, "stealth_disadv": False, "str_req": 0},
    {"name": "Armadura Acolchoada (Padded - Leve, CA 11 + DES)", "category": "Leve", "ac_base": 11, "stealth_disadv": True, "str_req": 0},
    {"name": "Armadura de Couro (Leather - Leve, CA 11 + DES)", "category": "Leve", "ac_base": 11, "stealth_disadv": False, "str_req": 0},
    {"name": "Armadura de Couro Batido (Studded Leather - Leve, CA 12 + DES)", "category": "Leve", "ac_base": 12, "stealth_disadv": False, "str_req": 0},
    {"name": "Gibão de Peles (Hide - Média, CA 12 + DES máx +2)", "category": "Média", "ac_base": 12, "stealth_disadv": False, "str_req": 0},
    {"name": "Camisão de Cota de Malha (Chain Shirt - Média, CA 13 + DES máx +2)", "category": "Média", "ac_base": 13, "stealth_disadv": False, "str_req": 0},
    {"name": "Brunea (Scale Mail - Média, CA 14 + DES máx +2)", "category": "Média", "ac_base": 14, "stealth_disadv": True, "str_req": 0},
    {"name": "Peitoral de Aço (Breastplate - Média, CA 14 + DES máx +2)", "category": "Média", "ac_base": 14, "stealth_disadv": False, "str_req": 0},
    {"name": "Meia-Armadura (Half Plate - Média, CA 15 + DES máx +2)", "category": "Média", "ac_base": 15, "stealth_disadv": True, "str_req": 0},
    {"name": "Cota de Anéis (Ring Mail - Pesada, CA 14 Fixa)", "category": "Pesada", "ac_base": 14, "stealth_disadv": True, "str_req": 0},
    {"name": "Cota de Malha (Chain Mail - Pesada, CA 16 Fixa, FOR 13)", "category": "Pesada", "ac_base": 16, "stealth_disadv": True, "str_req": 13},
    {"name": "Cota de Talas (Splint - Pesada, CA 17 Fixa, FOR 15)", "category": "Pesada", "ac_base": 17, "stealth_disadv": True, "str_req": 15},
    {"name": "Armadura de Placas Completa (Full Plate - Pesada, CA 18 Fixa, FOR 15)", "category": "Pesada", "ac_base": 18, "stealth_disadv": True, "str_req": 15},
    {"name": "Escudo de Batalha (Shield - +2 CA)", "category": "Escudo", "ac_base": 2, "stealth_disadv": False, "str_req": 0}
]

# =============================================================================
# 7. TODOS OS TALENTOS OFICIAIS D&D 2024 (ORIGEM, GERAIS E ÉPICOS)
# =============================================================================
FEATS_2024: List[Dict[str, Any]] = [
    # Talentos de Origem (Nível 1)
    {"name": "Alerta (Alert - Origem)", "type": "Origem", "description": "Soma PB na Iniciativa e pode trocar sua iniciativa com um aliado voluntário."},
    {"name": "Iniciado em Magia: Mago (Magic Initiate: Wizard - Origem)", "type": "Origem", "description": "Aprende 2 truques e 1 magia de 1º nível de Mago (usa INT)."},
    {"name": "Iniciado em Magia: Clérigo (Magic Initiate: Cleric - Origem)", "type": "Origem", "description": "Aprende 2 truques e 1 magia de 1º nível de Clérigo (usa SAB)."},
    {"name": "Iniciado em Magia: Druida (Magic Initiate: Druid - Origem)", "type": "Origem", "description": "Aprende 2 truques e 1 magia de 1º nível de Druida (usa SAB)."},
    {"name": "Sortudo (Lucky - Origem)", "type": "Origem", "description": "Pontos de Sorte iguais ao PB para rolar com vantagem ou dar desvantagem no d20."},
    {"name": "Músico (Musician - Origem)", "type": "Origem", "description": "Concede Inspiração Heroica a um número de aliados igual ao PB após Descanso."},
    {"name": "Curandeiro (Healer - Origem)", "type": "Origem", "description": "Gasta Dado de Vida para curar aliados com Kit Médico e rola novamente dados que derem 1."},
    {"name": "Valentão de Taverna (Tavern Brawler - Origem)", "type": "Origem", "description": "Ataques desarmados causam 1d4 + FOR, pode empurrar criaturas e rola dano novamente em 1s."},
    {"name": "Artesão Hábil (Crafter - Origem)", "type": "Origem", "description": "Fabricação rápida de itens e desconto de 20% em compras não mágicas."},
    {"name": "Robusto (Tough - Origem)", "type": "Origem", "description": "Ganha +2 PV por nível de personagem (retroativo e futuro)."},
    {"name": "Habilidoso (Skilled - Origem)", "type": "Origem", "description": "Ganha proficiência em quaisquer 3 perícias ou ferramentas à sua escolha."},
    {"name": "Combatente Selvagem (Savage Attacker - Origem)", "type": "Origem", "description": "Rola duas vezes o dano de armas corpo a corpo e escolhe o maior resultado."},

    # Talentos Gerais (Nível 4+)
    {"name": "Mestre em Armas Grandes (Great Weapon Master - Nível 4+)", "type": "Geral", "description": "Ataque bônus ao acertar crítico ou derrotar inimigo; soma PB no dano de armas Pesadas."},
    {"name": "Conjurador de Guerra (War Caster - Nível 4+)", "type": "Geral", "description": "Vantagem em salvaguardas de Concentração; usa magias como Ataques de Oportunidade."},
    {"name": "Sentinela (Sentinel - Nível 4+)", "type": "Geral", "description": "Ataques de oportunidade reduzem deslocamento a 0 e ignora a ação Desengajar."},
    {"name": "Franco-Atirador (Sharpshooter - Nível 4+)", "type": "Geral", "description": "Ignora cobertura parcial; atira à queima-roupa sem desvantagem; alcance longo sem penalidade."},
    {"name": "Especialista em Besta (Crossbow Expert - Nível 4+)", "type": "Geral", "description": "Ignora propriedade Recarga; dispara à queima-roupa sem desvantagem; ataque bônus."},
    {"name": "Mestre de Armas de Haste (Polearm Master - Nível 4+)", "type": "Geral", "description": "Ataque com a coronha como Ação Bônus (1d4); ataque de oportunidade quando entram no alcance."},
    {"name": "Duelista Defensivo (Defensive Duelist - Nível 4+)", "type": "Geral", "description": "Usa Reação para somar PB na CA contra ataques corpo a corpo com arma de Acuidade."},
    {"name": "Mestre em Escudos (Shield Master - Nível 4+)", "type": "Geral", "description": "Ação Bônus para empurrar com escudo; soma bônus do escudo em salvaguardas de DES."},
    {"name": "Mestre em Armaduras Pesadas (Heavy Armor Master - Nível 4+)", "type": "Geral", "description": "Reduz dano contundente, perfurante e cortante sofrido em um valor igual ao PB."},
    {"name": "Mestre em Armaduras Médias (Medium Armor Master - Nível 4+)", "type": "Geral", "description": "Soma até +3 da DES na CA e elimina desvantagem em Furtividade."},
    {"name": "Resiliente: Constituição (Resilient: CON - Nível 4+)", "type": "Geral", "description": "+1 em CON e ganha proficiência em Salvaguardas de Constituição."},
    {"name": "Resiliente: Sabedoria (Resilient: WIS - Nível 4+)", "type": "Geral", "description": "+1 em SAB e ganha proficiência em Salvaguardas de Sabedoria."},
    {"name": "Resiliente: Destreza (Resilient: DEX - Nível 4+)", "type": "Geral", "description": "+1 em DES e ganha proficiência em Salvaguardas de Destreza."},
    {"name": "Líder Inspirador (Inspiring Leader - Nível 4+)", "type": "Geral", "description": "Concede PV temporários iguais a Nível + Mod CAR para até 6 aliados após descanso."},
    {"name": "Atacante Móvel (Charger / Mobile - Nível 4+)", "type": "Geral", "description": "+3m de deslocamento; +1d8 no dano ou empurra 3m ao correr e atacar."},
    {"name": "Combatente Montado (Mounted Combatant - Nível 4+)", "type": "Geral", "description": "Vantagem em ataques contra criaturas menores que sua montaria e proteção à montaria."},
    {"name": "Atleta (Athlete - Nível 4+)", "type": "Geral", "description": "+1 em FOR ou DES; levantar gasta apenas 1,5m; escalada sem custo extra de movimento."},
    {"name": "Resistência Elemental (Elemental Adept - Nível 4+)", "type": "Geral", "description": "Suas magias ignoram resistência ao tipo de dano escolhido (Fogo, Frio, Relâmpago, etc.)."},

    # Dádivas Épicas (Epic Boons - Nível 19+)
    {"name": "Dádiva da Recuperação Épica (Epic Boon of Recovery - Nível 19+)", "type": "Épico", "description": "Cura metade do PV máximo ao cair para 0 PV 1x por descanso longo."},
    {"name": "Dádiva da Destreza Dimensional (Epic Boon of Dimensional Travel - Nível 19+)", "type": "Épico", "description": "Teletransporte de até 9m como parte de qualquer Ação de Ataque ou Magia."},
    {"name": "Dádiva da Vontade Indomável (Epic Boon of the Unfettered - Nível 19+)", "type": "Épico", "description": "Imunidade a Agarrado, Preso e Paralisado; Ação Bônus para escapar de efeitos."},
    {"name": "Dádiva da Fortitude Irresistível (Epic Boon of Fortitude - Nível 19+)", "type": "Épico", "description": "+40 PV Máximo permanente e recupera PV todo início de turno."}
]

# =============================================================================
# 8. TODOS OS ITENS MÁGICOS CANÔNICOS OFICIAIS (SRD / LIVRO DO MESTRE)
# =============================================================================
MAGIC_ITEMS_2024: List[Dict[str, Any]] = [
    {"name": "Capa de Proteção (Cloak of Protection - Sintonizado)", "rarity": "Incomum", "attunement": True, "bonus": "+1 em CA e todas as Salvaguardas"},
    {"name": "Anel de Proteção (Ring of Protection - Sintonizado)", "rarity": "Raro", "attunement": True, "bonus": "+1 em CA e todas as Salvaguardas"},
    {"name": "Botas Aladas (Winged Boots - Sintonizado)", "rarity": "Incomum", "attunement": True, "bonus": "Deslocamento de voo por até 4 horas"},
    {"name": "Braçadeiras de Defesa (Bracers of Defense - Sintonizado)", "rarity": "Raro", "attunement": True, "bonus": "+2 na CA se estiver sem armadura e sem escudo"},
    {"name": "Arma +1 (Mágica)", "rarity": "Incomum", "attunement": False, "bonus": "+1 nas jogadas de ataque e dano"},
    {"name": "Arma +2 (Mágica)", "rarity": "Raro", "attunement": False, "bonus": "+2 nas jogadas de ataque e dano"},
    {"name": "Arma +3 (Mágica)", "rarity": "Muito Raro", "attunement": False, "bonus": "+3 nas jogadas de ataque e dano"},
    {"name": "Escudo +1 (Mágico)", "rarity": "Incomum", "attunement": False, "bonus": "+3 total na CA (+2 base + 1 mágico)"},
    {"name": "Escudo +2 (Mágico)", "rarity": "Raro", "attunement": False, "bonus": "+4 total na CA (+2 base + 2 mágico)"},
    {"name": "Espada Flamejante (Flame Tongue - Sintonizado)", "rarity": "Raro", "attunement": True, "bonus": "Causa +2d6 de dano de fogo e ilumina"},
    {"name": "Espada Congelante (Frost Brand - Sintonizado)", "rarity": "Muito Raro", "attunement": True, "bonus": "Causa +1d6 de dano de frio e concede resistência a fogo"},
    {"name": "Vingadora Sagrada (Holy Avenger - Sintonizado por Paladino)", "rarity": "Lendário", "attunement": True, "bonus": "+3 no ataque/dano, +2d10 contra mortos-vivos/ínferos e Aura com Vantagem em salvaguardas"},
    {"name": "Cinto de Força do Gigante da Colina (FOR 21 - Sintonizado)", "rarity": "Raro", "attunement": True, "bonus": "Define a Força em 21 (+5)"},
    {"name": "Cinto de Força do Gigante de Fogo (FOR 25 - Sintonizado)", "rarity": "Muito Raro", "attunement": True, "bonus": "Define a Força em 25 (+7)"},
    {"name": "Amuleto de Saúde (CON 19 - Sintonizado)", "rarity": "Raro", "attunement": True, "bonus": "Define a Constituição em 19 (+4)"},
    {"name": "Tiara do Intelecto (INT 19 - Sintonizado)", "rarity": "Incomum", "attunement": True, "bonus": "Define a Inteligência em 19 (+4)"},
    {"name": "Manto Élfico (Cloak of Elvenkind - Sintonizado)", "rarity": "Incomum", "attunement": True, "bonus": "Vantagem em testes de Furtividade e desvantagem para quem tentar avistar"},
    {"name": "Botas Élficas (Boots of Elvenkind)", "rarity": "Incomum", "attunement": False, "bonus": "Passos totalmente silenciosos e vantagem em Furtividade ao andar"},
    {"name": "Bolsa de Carga (Bag of Holding)", "rarity": "Incomum", "attunement": False, "bonus": "Suporta até 225 kg (500 lbs) em espaço extradimensional de 1,8m³"},
    {"name": "Varinha de Mísseis Mágicos (Wand of Magic Missiles)", "rarity": "Incomum", "attunement": False, "bonus": "7 cargas para conjurar Mísseis Mágicos"},
    {"name": "Varinha de Teia (Wand of Web - Sintonizado)", "rarity": "Incomum", "attunement": True, "bonus": "7 cargas para conjurar Teia (CD 15)"},
    {"name": "Cajado de Cura (Staff of Healing - Sintonizado)", "rarity": "Raro", "attunement": True, "bonus": "10 cargas para conjurar Curar Ferimentos, Restauração Menor e Curar Ferimentos em Massa"},
    {"name": "Poção de Cura Comum (2d4+2)", "rarity": "Comum", "attunement": False, "bonus": "Recupera 2d4+2 PV (Ação Bônus em 2024)"},
    {"name": "Poção de Cura Maior (4d4+4)", "rarity": "Incomum", "attunement": False, "bonus": "Recupera 4d4+4 PV (Ação Bônus em 2024)"},
    {"name": "Poção de Cura Superior (8d4+8)", "rarity": "Raro", "attunement": False, "bonus": "Recupera 8d4+8 PV (Ação Bônus em 2024)"},
    {"name": "Poção de Cura Suprema (10d4+20)", "rarity": "Muito Raro", "attunement": False, "bonus": "Recupera 10d4+20 PV (Ação Bônus em 2024)"},
    {"name": "Poção de Invisibilidade", "rarity": "Muito Raro", "attunement": False, "bonus": "Fica invisível por 1 hora"},
    {"name": "Poção de Velocidade", "rarity": "Muito Raro", "attunement": False, "bonus": "Efeito da magia Velocidade por 1 minuto sem concentração"},
    {"name": "Poção de Voo", "rarity": "Muito Raro", "attunement": False, "bonus": "Ganha velocidade de voo de 18m por 1 hora"}
]

# =============================================================================
# 9. EQUIPAMENTOS, MOCHILAS, PACOTES & FERRAMENTAS OFICIAIS
# =============================================================================
EQUIPMENT_PACKS_2024: List[str] = [
    "Pacote de Explorador de Masmorras (Mochila, pé-de-cabra, martelo, 10 pitões, 10 tochas, pederneira, 10 rações, cantil, corda de 15m)",
    "Pacote de Explorador (Mochila, saco de dormir, kit de refeição, pederneira, 10 tochas, 10 rações, cantil, corda de 15m)",
    "Pacote de Sacerdote (Mochila, cobertor, 10 velas, pederneira, caixa de esmolas, incenso, incensário, vestimentas, 2 dias de rações, cantil)",
    "Pacote de Estudioso (Mochila, livro de estudo, vidro de tinta, pena, 10 folhas de pergaminho, saquinho de areia, faquinha)",
    "Pacote de Artista (Mochila, saco de dormir, 2 fantasias, 5 velas, 5 rações, cantil, kit de disfarce)",
    "Pacote de Diplomata (Baú, 2 estojos para mapas, roupas finas, frasco de tinta, pena, lamparina, óleo, papel, perfume, cera de lacre)",
    "Ferramentas de Ladrão (Thieves' Tools)",
    "Kit de Primeiros Socorros (Healer's Kit - 10 usos)",
    "Kit de Disfarce (Disguise Kit)",
    "Kit de Falsificação (Forgery Kit)",
    "Kit de Venenos (Poisoner's Kit)",
    "Kit de Herbalismo (Herbalism Kit)",
    "Kit de Navegação (Navigator's Tools)",
    "Ferramentas de Ferreiro (Smith's Tools)",
    "Ferramentas de Alquimista (Alchemist's Supplies)",
    "Ferramentas de Cervejeiro (Brewer's Supplies)",
    "Ferramentas de Carpinteiro (Carpenter's Tools)",
    "Ferramentas de Cartógrafo (Cartographer's Tools)",
    "Ferramentas de Coureiro (Leatherworker's Tools)",
    "Ferramentas de Joalheiro (Jeweler's Tools)",
    "Ferramentas de Cozinheiro (Cook's Utensils)",
    "Instrumento Musical: Alaúde (Lute)",
    "Instrumento Musical: Flauta (Flute)",
    "Instrumento Musical: Lira (Lyre)",
    "Instrumento Musical: Tambor (Drum)",
    "Símbolo Sagrado: Amuleto Divino / Relicário",
    "Foco Arcano: Varinha de Cristal / Cajado",
    "Foco Druídico: Ramo de Visco / Totem de Madeira"
]

# =============================================================================
# 10. TODOS OS IDIOMAS OFICIAIS D&D
# =============================================================================
LANGUAGES_2024: List[str] = [
    "Comum (Common)",
    "Élfico (Elvish)",
    "Anão (Dwarvish)",
    "Dracônico (Draconic)",
    "Orc",
    "Halfling",
    "Gnômico (Gnomish)",
    "Gigante (Giant)",
    "Goblin",
    "Abissal (Abyssal)",
    "Celestial",
    "Infernal",
    "Primordial (Aquan, Auran, Ignan, Terran)",
    "Silvestre (Sylvan)",
    "Subterrâneo (Undercommon)",
    "Gíria de Ladrão (Thieves' Cant)",
    "Druídico (Druidic)"
]

# =============================================================================
# 11. PROFICIÊNCIAS DE ARMAS E ARMADURAS
# =============================================================================
PROFICIENCIES_ARMOR_WEAPONS: List[str] = [
    "Armaduras Leves (Light Armor)",
    "Armaduras Médias (Medium Armor)",
    "Armaduras Pesadas (Heavy Armor)",
    "Escudos (Shields)",
    "Armas Simples (Simple Weapons)",
    "Armas Marciais (Martial Weapons)",
    "Armas de Fogo Marciais (Firearms)"
]

# =============================================================================
# 12. CATÁLOGO COMPLETO DE MAGIAS (TRUQUES AO 9º CÍRCULO - 100% OFICIAL)
# =============================================================================
SPELLS_CATALOG: List[Dict[str, Any]] = [
    # TRUQUES (NÍVEL 0)
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
    {"name_pt": "Proteção contra Lâminas", "name_en": "Blade Ward (2024)", "level": 0, "school": "Abjuração", "classes": ["Bardo", "Mago", "Feiticeiro", "Bruxo"]},
    {"name_pt": "Zombaria Viciosa", "name_en": "Vicious Mockery", "level": 0, "school": "Encantamento", "classes": ["Bardo"]},
    {"name_pt": "Bordão Mágico", "name_en": "Shillelagh", "level": 0, "school": "Transmutação", "classes": ["Druida"]},
    {"name_pt": "Toque Necrótico", "name_en": "Chill Touch", "level": 0, "school": "Necromancia", "classes": ["Mago", "Feiticeiro", "Bruxo"]},
    {"name_pt": "Raio de Gelo", "name_en": "Ray of Frost", "level": 0, "school": "Evocação", "classes": ["Mago", "Feiticeiro"]},
    {"name_pt": "Espirro Ácido", "name_en": "Acid Splash", "level": 0, "school": "Conjuração", "classes": ["Mago", "Feiticeiro"]},
    {"name_pt": "Palavra Radiante", "name_en": "Word of Radiance", "level": 0, "school": "Evocação", "classes": ["Clérigo"]},
    {"name_pt": "Consertar", "name_en": "Mending", "level": 0, "school": "Transmutação", "classes": ["Bardo", "Clérigo", "Druida", "Mago", "Feiticeiro"]},

    # 1º CÍRCULO
    {"name_pt": "Curar Ferimentos", "name_en": "Cure Wounds (2024: 2d8)", "level": 1, "school": "Evocação", "classes": ["Bardo", "Clérigo", "Druida", "Paladino", "Patrulheiro"]},
    {"name_pt": "Palavra Curativa", "name_en": "Healing Word (2024: 2d4)", "level": 1, "school": "Evocação", "classes": ["Bardo", "Clérigo", "Druida"]},
    {"name_pt": "Escudo Arcano", "name_en": "Shield", "level": 1, "school": "Abjuração", "classes": ["Mago", "Feiticeiro"]},
    {"name_pt": "Mísseis Mágicos", "name_en": "Magic Missile", "level": 1, "school": "Evocação", "classes": ["Mago", "Feiticeiro"]},
    {"name_pt": "Raio Guiador", "name_en": "Guiding Bolt", "level": 1, "school": "Evocação", "classes": ["Clérigo"]},
    {"name_pt": "Armadura Arcana", "name_en": "Mage Armor", "level": 1, "school": "Abjuração", "classes": ["Mago", "Feiticeiro"]},
    {"name_pt": "Bênção", "name_en": "Bless", "level": 1, "school": "Encantamento", "classes": ["Clérigo", "Paladino"]},
    {"name_pt": "Bruxaria", "name_en": "Hex", "level": 1, "school": "Encantamento", "classes": ["Bruxo"]},
    {"name_pt": "Marca do Caçador", "name_en": "Hunter's Mark", "level": 1, "school": "Adivinhação", "classes": ["Patrulheiro"]},
    {"name_pt": "Sono", "name_en": "Sleep", "level": 1, "school": "Encantamento", "classes": ["Bardo", "Mago", "Feiticeiro"]},
    {"name_pt": "Onda Trovejante", "name_en": "Thunderwave", "level": 1, "school": "Evocação", "classes": ["Bardo", "Druida", "Mago", "Feiticeiro"]},
    {"name_pt": "Absorver Elementos", "name_en": "Absorb Elements", "level": 1, "school": "Abjuração", "classes": ["Druida", "Mago", "Patrulheiro", "Feiticeiro"]},
    {"name_pt": "Fogo das Fadas", "name_en": "Faerie Fire", "level": 1, "school": "Evocação", "classes": ["Bardo", "Druida"]},
    {"name_pt": "Queda Suave", "name_en": "Feather Fall", "level": 1, "school": "Transmutação", "classes": ["Bardo", "Mago", "Feiticeiro"]},
    {"name_pt": "Compreender Idiomas", "name_en": "Comprehend Languages", "level": 1, "school": "Adivinhação", "classes": ["Bardo", "Mago", "Feiticeiro", "Bruxo"]},
    {"name_pt": "Detectar Magia", "name_en": "Detect Magic", "level": 1, "school": "Adivinhação", "classes": ["Bardo", "Clérigo", "Druida", "Paladino", "Patrulheiro", "Mago", "Feiticeiro", "Bruxo"]},
    {"name_pt": "Graxa", "name_en": "Grease", "level": 1, "school": "Conjuração", "classes": ["Mago", "Feiticeiro"]},
    {"name_pt": "Riso Histérico de Tasha", "name_en": "Tasha's Hideous Laughter", "level": 1, "school": "Encantamento", "classes": ["Bardo", "Mago", "Bruxo"]},
    {"name_pt": "Santuário", "name_en": "Sanctuary", "level": 1, "school": "Abjuração", "classes": ["Clérigo"]},
    {"name_pt": "Comando", "name_en": "Command", "level": 1, "school": "Encantamento", "classes": ["Clérigo", "Paladino"]},
    {"name_pt": "Sussurros Dissonantes", "name_en": "Dissonant Whispers", "level": 1, "school": "Encantamento", "classes": ["Bardo"]},
    {"name_pt": "Heroísmo", "name_en": "Heroism", "level": 1, "school": "Encantamento", "classes": ["Bardo", "Paladino"]},
    {"name_pt": "Repreensão Infernal", "name_en": "Hellish Rebuke", "level": 1, "school": "Evocação", "classes": ["Bruxo"]},
    {"name_pt": "Vitalidade Falsa", "name_en": "False Life", "level": 1, "school": "Necromancia", "classes": ["Mago", "Feiticeiro", "Bruxo"]},
    {"name_pt": "Mãos Flamejantes", "name_en": "Burning Hands", "level": 1, "school": "Evocação", "classes": ["Mago", "Feiticeiro"]},

    # 2º CÍRCULO
    {"name_pt": "Passo Nebuloso", "name_en": "Misty Step", "level": 2, "school": "Conjuração", "classes": ["Mago", "Feiticeiro", "Bruxo"]},
    {"name_pt": "Invisibilidade", "name_en": "Invisibility", "level": 2, "school": "Ilusão", "classes": ["Bardo", "Mago", "Feiticeiro", "Bruxo"]},
    {"name_pt": "Arma Espiritual", "name_en": "Spiritual Weapon", "level": 2, "school": "Evocação", "classes": ["Clérigo"]},
    {"name_pt": "Imobilizar Pessoa", "name_en": "Hold Person", "level": 2, "school": "Encantamento", "classes": ["Bardo", "Clérigo", "Druida", "Feiticeiro", "Mago", "Bruxo"]},
    {"name_pt": "Raio Ardente", "name_en": "Scorching Ray", "level": 2, "school": "Evocação", "classes": ["Feiticeiro", "Mago"]},
    {"name_pt": "Sugestão", "name_en": "Suggestion", "level": 2, "school": "Encantamento", "classes": ["Bardo", "Feiticeiro", "Mago", "Bruxo"]},
    {"name_pt": "Reflexos", "name_en": "Mirror Image", "level": 2, "school": "Ilusão", "classes": ["Feiticeiro", "Mago", "Bruxo"]},
    {"name_pt": "Escuridão", "name_en": "Darkness", "level": 2, "school": "Evocação", "classes": ["Feiticeiro", "Mago", "Bruxo"]},
    {"name_pt": "Levitação", "name_en": "Levitate", "level": 2, "school": "Transmutação", "classes": ["Mago", "Feiticeiro"]},
    {"name_pt": "Teia", "name_en": "Web", "level": 2, "school": "Conjuração", "classes": ["Mago", "Feiticeiro"]},
    {"name_pt": "Silêncio", "name_en": "Silence", "level": 2, "school": "Ilusão", "classes": ["Bardo", "Clérigo", "Patrulheiro"]},
    {"name_pt": "Restauração Menor", "name_en": "Lesser Restoration", "level": 2, "school": "Abjuração", "classes": ["Bardo", "Clérigo", "Druida", "Paladino", "Patrulheiro"]},
    {"name_pt": "Vínculo de Proteção", "name_en": "Warding Bond", "level": 2, "school": "Abjuração", "classes": ["Clérigo", "Paladino"]},
    {"name_pt": "Oração de Cura", "name_en": "Prayer of Healing", "level": 2, "school": "Evocação", "classes": ["Clérigo", "Paladino"]},
    {"name_pt": "Aprimorar Habilidade", "name_en": "Enhance Ability", "level": 2, "school": "Transmutação", "classes": ["Bardo", "Clérigo", "Druida", "Feiticeiro", "Mago"]},

    # 3º CÍRCULO
    {"name_pt": "Bola de Fogo", "name_en": "Fireball", "level": 3, "school": "Evocação", "classes": ["Mago", "Feiticeiro"]},
    {"name_pt": "Contra-mágica", "name_en": "Counterspell", "level": 3, "school": "Abjuração", "classes": ["Mago", "Feiticeiro", "Bruxo"]},
    {"name_pt": "Velocidade", "name_en": "Haste", "level": 3, "school": "Transmutação", "classes": ["Mago", "Feiticeiro"]},
    {"name_pt": "Relâmpago", "name_en": "Lightning Bolt", "level": 3, "school": "Evocação", "classes": ["Feiticeiro", "Mago"]},
    {"name_pt": "Espíritos Guardiões", "name_en": "Spirit Guardians", "level": 3, "school": "Conjuração", "classes": ["Clérigo"]},
    {"name_pt": "Reviver", "name_en": "Revivify", "level": 3, "school": "Necromancia", "classes": ["Clérigo", "Druida", "Paladino", "Patrulheiro"]},
    {"name_pt": "Voo", "name_en": "Fly", "level": 3, "school": "Transmutação", "classes": ["Feiticeiro", "Mago", "Bruxo"]},
    {"name_pt": "Dissipar Magia", "name_en": "Dispel Magic", "level": 3, "school": "Abjuração", "classes": ["Bardo", "Clérigo", "Druida", "Paladino", "Feiticeiro", "Mago", "Bruxo"]},
    {"name_pt": "Padrão Hipnótico", "name_en": "Hypnotic Pattern", "level": 3, "school": "Ilusão", "classes": ["Bardo", "Feiticeiro", "Mago", "Bruxo"]},
    {"name_pt": "Fome de Hadar", "name_en": "Hunger of Hadar", "level": 3, "school": "Conjuração", "classes": ["Bruxo"]},
    {"name_pt": "Muralha de Vento", "name_en": "Wind Wall", "level": 3, "school": "Evocação", "classes": ["Druida", "Patrulheiro"]},
    {"name_pt": "Convocar Relâmpagos", "name_en": "Call Lightning", "level": 3, "school": "Conjuração", "classes": ["Druida"]},
    {"name_pt": "Pequena Cabana de Leomund", "name_en": "Leomund's Tiny Hut", "level": 3, "school": "Evocação", "classes": ["Bardo", "Mago"]},
    {"name_pt": "Falar com os Mortos", "name_en": "Speak with Dead", "level": 3, "school": "Necromancia", "classes": ["Bardo", "Clérigo"]},

    # 4º CÍRCULO
    {"name_pt": "Metamorfose", "name_en": "Polymorph", "level": 4, "school": "Transmutação", "classes": ["Bardo", "Druida", "Mago", "Feiticeiro"]},
    {"name_pt": "Porta Dimensional", "name_en": "Dimension Door", "level": 4, "school": "Conjuração", "classes": ["Bardo", "Mago", "Feiticeiro", "Bruxo"]},
    {"name_pt": "Muralha de Fogo", "name_en": "Wall of Fire", "level": 4, "school": "Evocação", "classes": ["Druida", "Feiticeiro", "Mago"]},
    {"name_pt": "Invisibilidade Maior", "name_en": "Greater Invisibility", "level": 4, "school": "Ilusão", "classes": ["Bardo", "Feiticeiro", "Mago"]},
    {"name_pt": "Banimento", "name_en": "Banishment", "level": 4, "school": "Abjuração", "classes": ["Clérigo", "Paladino", "Feiticeiro", "Mago", "Bruxo"]},
    {"name_pt": "Tempestade de Gelo", "name_en": "Ice Storm", "level": 4, "school": "Evocação", "classes": ["Druida", "Mago", "Feiticeiro"]},
    {"name_pt": "Escudo de Fogo", "name_en": "Fire Shield", "level": 4, "school": "Evocação", "classes": ["Mago"]},
    {"name_pt": "Tentáculos Negros de Evard", "name_en": "Evard's Black Tentacles", "level": 4, "school": "Conjuração", "classes": ["Mago"]},

    # 5º CÍRCULO
    {"name_pt": "Reviver os Mortos", "name_en": "Raise Dead", "level": 5, "school": "Necromancia", "classes": ["Bardo", "Clérigo", "Paladino"]},
    {"name_pt": "Cone de Frio", "name_en": "Cone of Cold", "level": 5, "school": "Evocação", "classes": ["Feiticeiro", "Mago"]},
    {"name_pt": "Muralha de Força", "name_en": "Wall of Force", "level": 5, "school": "Evocação", "classes": ["Mago"]},
    {"name_pt": "Curar Ferimentos em Massa", "name_en": "Mass Cure Wounds", "level": 5, "school": "Evocação", "classes": ["Bardo", "Clérigo", "Druida"]},
    {"name_pt": "Telecinésia", "name_en": "Telekinesis", "level": 5, "school": "Transmutação", "classes": ["Feiticeiro", "Mago"]},
    {"name_pt": "Coluna de Chamas", "name_en": "Flame Strike", "level": 5, "school": "Evocação", "classes": ["Clérigo"]},
    {"name_pt": "Imobilizar Monstro", "name_en": "Hold Monster", "level": 5, "school": "Encantamento", "classes": ["Bardo", "Feiticeiro", "Mago", "Bruxo"]},
    {"name_pt": "Dominar Pessoa", "name_en": "Dominate Person", "level": 5, "school": "Encantamento", "classes": ["Bardo", "Feiticeiro", "Mago"]},

    # 6º CÍRCULO
    {"name_pt": "Desintegrar", "name_en": "Disintegrate", "level": 6, "school": "Transmutação", "classes": ["Feiticeiro", "Mago"]},
    {"name_pt": "Cura Completa", "name_en": "Heal", "level": 6, "school": "Evocação", "classes": ["Clérigo", "Druida"]},
    {"name_pt": "Corrente de Relâmpagos", "name_en": "Chain Lightning", "level": 6, "school": "Evocação", "classes": ["Feiticeiro", "Mago"]},
    {"name_pt": "Globo de Invulnerabilidade", "name_en": "Globe of Invulnerability", "level": 6, "school": "Abjuração", "classes": ["Mago", "Feiticeiro"]},
    {"name_pt": "Banquete dos Heróis", "name_en": "Heroes' Feast", "level": 6, "school": "Conjuração", "classes": ["Clérigo", "Druida"]},
    {"name_pt": "Visão da Verdade", "name_en": "True Seeing", "level": 6, "school": "Adivinhação", "classes": ["Bardo", "Clérigo", "Mago", "Feiticeiro", "Bruxo"]},

    # 7º CÍRCULO
    {"name_pt": "Teletransporte", "name_en": "Teleport", "level": 7, "school": "Conjuração", "classes": ["Bardo", "Mago", "Feiticeiro"]},
    {"name_pt": "Ressurreição", "name_en": "Resurrection", "level": 7, "school": "Necromancia", "classes": ["Bardo", "Clérigo"]},
    {"name_pt": "Prisão de Energia", "name_en": "Forcecage", "level": 7, "school": "Evocação", "classes": ["Bardo", "Mago", "Bruxo"]},
    {"name_pt": "Dedo da Morte", "name_en": "Finger of Death", "level": 7, "school": "Necromancia", "classes": ["Feiticeiro", "Mago", "Bruxo"]},
    {"name_pt": "Mansão Magnífica de Mordenkainen", "name_en": "Mordenkainen's Magnificent Mansion", "level": 7, "school": "Conjuração", "classes": ["Bardo", "Mago"]},

    # 8º CÍRCULO
    {"name_pt": "Terremoto", "name_en": "Earthquake", "level": 8, "school": "Evocação", "classes": ["Clérigo", "Druida", "Feiticeiro"]},
    {"name_pt": "Labirinto", "name_en": "Maze", "level": 8, "school": "Conjuração", "classes": ["Mago"]},
    {"name_pt": "Aura Sagrada", "name_en": "Holy Aura", "level": 8, "school": "Abjuração", "classes": ["Clérigo"]},
    {"name_pt": "Campo Antimagia", "name_en": "Antimagic Field", "level": 8, "school": "Abjuração", "classes": ["Clérigo", "Mago"]},
    {"name_pt": "Dominar Monstro", "name_en": "Dominate Monster", "level": 8, "school": "Encantamento", "classes": ["Bardo", "Feiticeiro", "Mago", "Bruxo"]},
    {"name_pt": "Explosão Solar", "name_en": "Sunburst", "level": 8, "school": "Evocação", "classes": ["Clérigo", "Druida", "Feiticeiro", "Mago"]},

    # 9º CÍRCULO
    {"name_pt": "Desejo", "name_en": "Wish", "level": 9, "school": "Conjuração", "classes": ["Feiticeiro", "Mago"]},
    {"name_pt": "Parar o Tempo", "name_en": "Time Stop", "level": 9, "school": "Transmutação", "classes": ["Feiticeiro", "Mago"]},
    {"name_pt": "Ressurreição Verdadeira", "name_en": "True Resurrection", "level": 9, "school": "Necromancia", "classes": ["Clérigo", "Druida"]},
    {"name_pt": "Chuva de Meteoros", "name_en": "Meteor Swarm", "level": 9, "school": "Evocação", "classes": ["Feiticeiro", "Mago"]},
    {"name_pt": "Palavra de Poder Matar", "name_en": "Power Word Kill", "level": 9, "school": "Encantamento", "classes": ["Bardo", "Feiticeiro", "Mago", "Bruxo"]},
    {"name_pt": "Metamorfose Verdadeira", "name_en": "True Polymorph", "level": 9, "school": "Transmutação", "classes": ["Bardo", "Bruxo", "Mago"]},
    {"name_pt": "Portal Dimensional Supremo", "name_en": "Gate", "level": 9, "school": "Conjuração", "classes": ["Clérigo", "Feiticeiro", "Mago"]},
    {"name_pt": "Sexto Sentido", "name_en": "Foresight", "level": 9, "school": "Adivinhação", "classes": ["Bardo", "Druida", "Mago", "Bruxo"]}
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

def get_cantrips_list(class_filter: Optional[str] = None) -> List[str]:
    if class_filter and class_filter.strip():
        cf = class_filter.strip()
        filtered = [s for s in SPELLS_CATALOG if s["level"] == 0 and cf in s.get("classes", [])]
        if filtered:
            return [f"{s['name_pt']} ({s['name_en']})" for s in filtered]
    return [f"{s['name_pt']} ({s['name_en']})" for s in SPELLS_CATALOG if s["level"] == 0]

def get_leveled_spells_list(class_filter: Optional[str] = None, max_level: int = 9) -> List[str]:
    if class_filter and class_filter.strip():
        cf = class_filter.strip()
        filtered = [s for s in SPELLS_CATALOG if 1 <= s["level"] <= max_level and cf in s.get("classes", [])]
        if filtered:
            return [f"{s['name_pt']} ({s['name_en']}) - Nível {s['level']} ({s['school']})" for s in filtered]
    return [f"{s['name_pt']} ({s['name_en']}) - Nível {s['level']} ({s['school']})" for s in SPELLS_CATALOG if s["level"] > 0]

def is_spellcaster_class(class_name: str, subclass_name: str = "") -> bool:
    if class_name in ["Mago", "Clérigo", "Druida", "Bardo", "Bruxo", "Feiticeiro", "Paladino", "Guardião"]:
        return True
    if "Cavaleiro Arcano" in subclass_name or "Trapaceiro Arcano" in subclass_name:
        return True
    return False

def get_class_default_spell_ability(class_name: str) -> str:
    return CLASSES_2024.get(class_name, {}).get("spell_ability", "None")

def get_background_details(background_name: str) -> Dict[str, Any]:
    return BACKGROUNDS_2024.get(background_name, {})

def get_species_details(species_name: str) -> Dict[str, Any]:
    return SPECIES_2024.get(species_name, {})

def get_feats_list() -> List[str]:
    return [f"{f['name']} — {f['description'][:60]}..." for f in FEATS_2024]

def get_magic_items_list() -> List[str]:
    return [f"{i['name']} — {i['bonus']}" for i in MAGIC_ITEMS_2024]

def get_equipment_packs_list() -> List[str]:
    return EQUIPMENT_PACKS_2024

def get_languages_list() -> List[str]:
    return LANGUAGES_2024

def get_armor_weapon_proficiencies_list() -> List[str]:
    return PROFICIENCIES_ARMOR_WEAPONS
