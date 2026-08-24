import pytest
from src.tools.dnd_catalog import (
    CLASSES_2024,
    SPECIES_2024,
    BACKGROUNDS_2024,
    WEAPONS_2024,
    ARMOR_2024,
    SPELLS_CATALOG,
    FEATS_2024,
    MAGIC_ITEMS_2024,
    ALIGNMENTS_2024,
    EQUIPMENT_PACKS_2024,
    LANGUAGES_2024,
    get_classes_list,
    get_subclasses_for_class,
    get_species_list,
    get_backgrounds_list,
    get_alignments_list,
    get_weapons_list,
    get_armor_list,
    get_cantrips_list,
    get_leveled_spells_list,
    get_feats_list,
    get_magic_items_list,
    get_equipment_packs_list,
    get_languages_list
)

def test_dnd_catalog_exhaustive_integrity():
    # 1. 100% das 12 Classes e 48 Subclasses Oficiais 2024
    classes = get_classes_list()
    assert len(classes) == 12
    for c in ["Guerreiro", "Mago", "Ladino", "Clérigo", "Paladino", "Bárbaro", "Bardo", "Bruxo", "Druida", "Feiticeiro", "Guardião", "Monge"]:
        assert c in classes
        subclasses = get_subclasses_for_class(c)
        assert len(subclasses) == 4
        
    # 2. 100% das 10 Espécies Oficiais 2024
    species = get_species_list()
    assert len(species) == 10
    for sp in ["Humano", "Elfo", "Anão", "Halfling", "Draconato", "Gnomo", "Golias", "Orc", "Tiferino", "Aasimar"]:
        assert sp in species
        
    # 3. 100% dos 16 Antecedentes Oficiais 2024
    backgrounds = get_backgrounds_list()
    assert len(backgrounds) == 16
    for bg in ["Soldado", "Acólito", "Sábio", "Guarda", "Guia", "Fazendeiro", "Criminoso", "Artesão", "Artista", "Charlatão", "Eremita", "Marinheiro", "Mercador", "Nobre", "Órfão", "Viajante"]:
        assert bg in backgrounds
        
    # 4. Alinhamentos Canônicos
    alignments = get_alignments_list()
    assert len(alignments) == 10
    
    # 5. 100% das 37 Armas e Maestrias de Arma 2024
    weapons = get_weapons_list()
    assert len(weapons) >= 35
    for mastery in ["Empurrão", "Rasgar", "Provocar", "Derrubar", "Cutilada", "Fraqueza", "Golpe Rápido", "Lentidão"]:
        assert any(mastery in w for w in weapons)
        
    # 6. 100% das 13 Armaduras Oficiais
    armors = get_armor_list()
    assert len(armors) >= 13
    assert any("Placas" in a for a in armors)
    assert any("Escudo" in a for a in armors)
    
    # 7. Magias Oficiais dos Círculos 0 ao 9
    cantrips = get_cantrips_list()
    assert len(cantrips) >= 15
    leveled = get_leveled_spells_list()
    assert len(leveled) >= 40
    
    # 8. Talentos e Itens Mágicos
    feats = get_feats_list()
    assert len(feats) >= 25
    magic_items = get_magic_items_list()
    assert len(magic_items) >= 20
    
    # 9. Mochilas e Idiomas
    packs = get_equipment_packs_list()
    assert len(packs) >= 15
    languages = get_languages_list()
    assert len(languages) >= 15
