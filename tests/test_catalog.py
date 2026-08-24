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
    get_classes_list,
    get_subclasses_for_class,
    get_species_list,
    get_backgrounds_list,
    get_weapons_list,
    get_spells_list
)

def test_dnd_catalog_integrity():
    # 1. Classes e Subclasses
    classes = get_classes_list()
    assert "Guerreiro" in classes
    assert "Mago" in classes
    assert "Ladino" in classes
    assert len(classes) == 12
    
    fighter_subclasses = get_subclasses_for_class("Guerreiro")
    assert "Campeão" in fighter_subclasses
    assert "Mestre de Batalha" in fighter_subclasses
    
    # 2. Espécies
    species = get_species_list()
    assert "Humano" in species
    assert "Elfo" in species
    assert "Golias" in species
    assert len(species) >= 10
    
    # 3. Antecedentes
    backgrounds = get_backgrounds_list()
    assert "Soldado" in backgrounds
    assert "Acólito" in backgrounds
    assert "Sábio" in backgrounds
    assert len(backgrounds) >= 16
    
    # 4. Armas com Maestria de Arma 2024
    weapons = get_weapons_list()
    assert len(weapons) >= 20
    assert any("Espada Longa" in w and "Empurrão" in w for w in weapons)
    assert any("Espada Grande" in w and "Rasgar" in w for w in weapons)
    
    # 5. Magias Oficiais
    spells = get_spells_list()
    assert len(spells) > 15
    assert any("Bola de Fogo" in s for s in spells)
    assert any("Curar Ferimentos" in s for s in spells)
