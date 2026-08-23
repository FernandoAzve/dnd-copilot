import pytest
from src.tools.dice import roll_dice

def test_roll_dice_standard():
    result = roll_dice("1d20+5")
    assert "rolls" in result
    assert len(result["rolls"]) == 1
    assert 1 <= result["rolls"][0] <= 20
    assert result["modifier"] == 5
    assert result["total"] == result["rolls"][0] + 5

def test_roll_dice_multi():
    result = roll_dice("3d6+2")
    assert len(result["rolls"]) == 3
    assert result["modifier"] == 2
    assert result["total"] == sum(result["rolls"]) + 2

def test_roll_dice_advantage():
    result = roll_dice("1d20+3", advantage=True)
    assert len(result["rolls"]) == 2
    assert result["chosen_roll"] == max(result["rolls"])
    assert result["total"] == result["chosen_roll"] + 3
    assert "Vantagem" in result["breakdown"]

def test_roll_dice_disadvantage():
    result = roll_dice("1d20+3", disadvantage=True)
    assert len(result["rolls"]) == 2
    assert result["chosen_roll"] == min(result["rolls"])
    assert result["total"] == result["chosen_roll"] + 3
    assert "Desvantagem" in result["breakdown"]

def test_roll_dice_drop_lowest():
    result = roll_dice("4d6kh3")
    assert len(result["rolls"]) == 4
    assert len(result["kept"]) == 3
    assert result["total"] == sum(result["kept"])

def test_roll_dice_invalid():
    result = roll_dice("invalid_expression")
    assert result["total"] == 0
    assert "inválida" in result["breakdown"]
