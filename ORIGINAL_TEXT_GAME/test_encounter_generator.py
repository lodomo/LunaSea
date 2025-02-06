################################################################################
# 
#     Author:      Lorenzo D. Moon
#     Instructor:  Karla Fant
#     Course:      CS-302
#     Assignment:  Program 4/5
#     Description: Tests for the encounter generator
#
################################################################################

import pytest
from encounter_generator import EncounterGenerator
from entity import Adventurer, Monster, LostSoul

def test_encounter_generator_init():
    # Test the encounter generator
    eg = EncounterGenerator()
    assert isinstance(eg, EncounterGenerator) == True

def test_forced_encounters():
    # Force an encounter of each type
    eg = EncounterGenerator()
    adventurer = eg.encounter_adventurer()
    monster = eg.encounter_monster()
    lost_soul = eg.encounter_lost_soul()

    assert isinstance(adventurer, Adventurer) == True
    assert isinstance(monster, Monster) == True
    assert isinstance(lost_soul, LostSoul) == True

if __name__ == "__main__":
    pytest.main(["-v", "test_encounter_generator.py"])