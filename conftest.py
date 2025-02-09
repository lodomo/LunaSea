################################################################################
# 
#     Author:      Lorenzo D. Moon
#     Instructor:  Karla Fant
#     Course:      CS-302
#     Assignment:  Program 4/5
#     Description: Test fixtures for entity and item classes
#
################################################################################

import pytest
from entity import Entity, Hero, Crewmate, Monster, Adventurer, LostSoul
from item import Item
from tree import Node, Tree

@pytest.fixture
def entity_data():
    # Test data to create an Entity
    # This test data will be loaded from file in the game
    data = {
        "name": "Entity Name",
        "hp": 100,
        "hp_max": 100,
        "strength": 10,
        "defense": 5,
        "exp_val": 5,
        "drops": [],
    }
    return data

@pytest.fixture
def entity_fixture(entity_data):
    # Fixture of an Entity
    return Entity(entity_data)

@pytest.fixture
def hero_data(entity_data):
    # Default data for a hero
    data = entity_data

    # Levelmap class implemented in level_map.py. This no longer needed
    # data["level_map"] = {
    #     1: [0, 1, 1, 1],
    #     2: [10, 1, 1, 1],
    #     3: [20, 1, 1, 1],
    #     4: [30, 1, 1, 1],
    #     5: [40, 1, 1, 1],
    # }
    return data

@pytest.fixture
def hero_fixture(hero_data):
    # Fixture of a hero
    return Hero(hero_data)

@pytest.fixture
def crewmate_data(entity_data):
    # Default data for a crewmate
    # Takes in the default entity data and adds crewmate specific data
    data = entity_data
    crewmate_specific = {
        "happiness": 100,
        "is_hostile": False,
        "ration_use": 1,
        "dialogue": ["Hello there.", "I love the sea."],
        "hostile_dialogue": ["You're doomed", "I'm going to drown you"],
    }
    data.update(crewmate_specific)
    return data

@pytest.fixture
def crewmate_fixture(crewmate_data):
    # Fixture of a crewmate
    return Crewmate(crewmate_data)

@pytest.fixture
def adventurer_data(crewmate_data):
    # Default data for an adventurer, same as a crewmate
    data = crewmate_data 
    return data

@pytest.fixture
def adventurer_fixture(adventurer_data):
    # Fixture of an adventurer
    return Adventurer(adventurer_data)

@pytest.fixture
def monster_data(crewmate_data):
    # Default data for a monster, same as a crewmate + ration value
    data = crewmate_data 
    data['ration_val'] = 5
    return data

@pytest.fixture
def monster_fixture(monster_data):
    # Fixture of a monster
    return Monster(monster_data)

@pytest.fixture
def lost_soul_data_positive(crewmate_data):
    # Create a lost soul data with positive story
    data = crewmate_data 
    soul_specific = {
        "is_positive" : True,
        "story" : "This is a positive story the soul will tell",
    }
    data.update(soul_specific)
    return data

@pytest.fixture
def lost_soul_data_negative(crewmate_data):
    # Create a lost soul data with negative story
    data = crewmate_data 
    soul_specific = {
        "is_positive" : False,
        "story" : "This is a sad story the soul will tell",
    }
    data.update(soul_specific)
    return data

@pytest.fixture
def lost_soul_fixture_pos(lost_soul_data_positive):
    # Fixture of a lost soul with positive story
    return LostSoul(lost_soul_data_positive)

@pytest.fixture
def lost_soul_fixture_neg(lost_soul_data_negative):
    # Fixture of a lost soul with negative story
    return LostSoul(lost_soul_data_negative)

@pytest.fixture
def consumable_item_data():
    # Default data for a consumable item
    # In game this will be loaded from file 
    data = {
        "name": "Consumable Item",
        "can_equip": False,
        "can_use": True,
        "uses": 2,
        "strength": 1,
        "defense": 2,
        "hp": 3,
        "levels": 0,        
    }
    return data

@pytest.fixture
def consumable_item_fixture(consumable_item_data):
    # Fixture of a consumable item
    return Item(consumable_item_data)

@pytest.fixture
def equip_item_data():
    # Default data for an equip item
    # In game this will be loaded from file 
    data = {
        "name": "Equip Item",
        "can_equip": True,
        "can_use": False,
        "uses": 1,
        "strength": 10,
        "defense": 5,
        "hp": 10,
        "levels": 0,
    }
    return data

@pytest.fixture
def equip_item_fixture(equip_item_data):
    # Fixture of an equip item
    return Item(equip_item_data)

@pytest.fixture
def tree_fixture(tree_data):
    # Fixture of a tree
    tree = Tree()
    for data in tree_data:
        tree.insert(data)
    return tree 

@pytest.fixture
def tree_data():
    # Test data for a tree
    data = [10, 20, 15, 9, 8, 12, 11]
    return data