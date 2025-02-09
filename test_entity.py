################################################################################
# 
#     Author:      Lorenzo D. Moon
#     Instructor:  Karla Fant
#     Course:      CS-302
#     Assignment:  Program 4/5
#     Description: Test Suite for Entity Hierachy 
#                  There is a split between the hero and the NPCs.
#                  Entity > CrewMate > Adventurer/Monster/LostSoul
#                  Entity > Hero
#
################################################################################

from entity import Entity, Hero, Crewmate, Adventurer, Monster, LostSoul
from item import Item
import pytest

def test_entity_instantiation(entity_fixture):
    """ Test the instantiation of the entity class.
    Deep check to make sure all the properties are set correctly.
    """
    entity = entity_fixture
    assert entity._Entity__name == "Entity Name"
    assert entity._Entity__hp_max == 100
    assert entity._Entity__hp == 100
    assert entity._Entity__strength == 10
    assert entity._Entity__defense == 5
    assert entity._Entity__exp_val == 5
    assert entity._Entity__drops == []

def test_bad_instantiation(entity_data):
    ''' Test the instantiation of the entity class with bad data.
    This test will check to make sure that the entity class will raise
    a TypeError if the data is not correct.
    '''
    datas = [] # Create an empty list for bad data

    # Give that list good data
    for i in range(8):
        datas.append(entity_data)
    
    # Make one of the data points bad for each of the properties
    datas[0]["name"] = 0
    datas[1]["hp"] = "String"
    datas[2]["hp_max"] = "String"
    datas[3]["strength"] = "String"
    datas[4]["defense"] = "String"
    datas[5]["exp_val"] = "String"
    datas[6]["image"] = 0
    datas[7]["drops"] = "String"

    # Check to make sure that the entity class raises a TypeError
    with pytest.raises(TypeError):
        for data in datas:
            Entity(data)


def test_entity_roll(entity_fixture):
    ''' Test the roll function of the entity class.
    This test will check to make sure that the roll function will
    return a number between 1 and 20. It will also check to make sure
    that the roll function is random enough.
    '''
    entity = entity_fixture
    roll_dict = {} # Create a dictionary to hold the rolls
    num_rolls = 20000 # Number of rolls to make

    # Prep the keys for the dictionary 
    for i in range(0, 21):
        roll_dict[str(i + 1)] = 0

    # Roll the dice 20,000 times and check to make sure that the rolls are
    # between 1 and 20. Also check to make sure that the rolls are random enough
    for i in range(num_rolls):
        temp_roll = entity.roll()
        assert temp_roll in range(1, 21)
        roll_dict[str(temp_roll)] += 1; 
    
    # Check to make sure that the rolls are random enough
    # I didn't want to over engineer this, so I just checked to make sure that
    # the roll count was += 200 for each number when ran 20,000 times.
    for i in range(1, 21):
        assert roll_dict[str(i)] in range(800, 1200)

def test_attack(entity_fixture):
    '''Test the attack function of the entity class.'''
    attacker = entity_fixture
    defender = entity_fixture 

    # Run the attack function 100 times and check to make sure that the damage
    # is between 0 and 5.
    for i in range(100):
        damage = attacker.attack(defender)
        assert damage in range(0, 11) 
    
    # Check to make sure that the attack function raises a TypeError if the
    # defender is not an entity.
    with pytest.raises(TypeError):
        attacker.attack("Test")

def test_take_damage(entity_fixture):
    ''' Test the take_damage function of the entity class.'''
    entity = entity_fixture 

    # Check for damage on regular hits
    for i in range(100):
        damage = entity.take_damage(False, i)
        assert damage in range(0, 4)
        assert entity._Entity__hp >= 0
    
    # and crits
    for i in range(100):
        damage = entity.take_damage(True, i)
        assert damage in range(2, 11)
        assert entity._Entity__hp >= 0
    
    # Type checking
    with pytest.raises(TypeError):
        entity.take_damage("Test", 10)
        entity.take_damage(False, "Test")
        entity.take_damage(False, 0.1) 
        entity.take_damage([], 10)

def test_alter_hp(entity_fixture):
    ''' Test the alter_hp function of the entity class.'''
    entity = entity_fixture 

    # Check to make sure that the hp is between 0 and hp_max
    for i in range(1000):
        entity.alter_hp(i)
        assert entity._Entity__hp >= 0
        assert entity._Entity__hp <= entity._Entity__hp_max
        entity.alter_hp(2 * -i)
        assert entity._Entity__hp >= 0
        assert entity._Entity__hp <= entity._Entity__hp_max
    
    # Type checking
    with pytest.raises(TypeError):
        entity.alter_hp("Test")
        entity.alter_hp(0.1)
        entity.alter_hp(False)

def test_alter_strength(entity_fixture):
    ''' Test the alter_strength function of the entity class.'''
    entity = entity_fixture 

    # Check to make sure that the strength never drops below 0 
    for i in range(1000):
        entity.alter_strength(i)
        assert entity._Entity__strength >= 0
        entity.alter_strength(2 * -i)
        assert entity._Entity__strength >= 0
    
    # Type checking
    with pytest.raises(TypeError):
        entity.alter_strength("Test")
        entity.alter_strength(0.1)
        entity.alter_strength(False)

def test_alter_defense(entity_fixture):
    ''' Test the alter_defense function of the entity class.'''
    entity = entity_fixture 

    # Check to make sure that the defense never drops below 0
    for i in range(1000):
        entity.alter_defense(i)
        assert entity._Entity__defense >= 0
        entity.alter_defense(2 * -i)
        assert entity._Entity__defense >= 0
    
    # Type checking
    with pytest.raises(TypeError):
        entity.alter_defense("Test")
        entity.alter_defense(0.1)
        entity.alter_defense(False)

def test_is_alive(entity_fixture):
    ''' Test the is_alive function of the entity class.'''
    entity = entity_fixture 
    assert entity.is_alive == True
    entity.alter_hp(-100)
    assert entity.is_alive == False

def test_death(entity_fixture):
    ''' Test the death function of the entity class.'''
    entity = entity_fixture 

    # Assert that it will raise an exception if the entity is still alive
    with pytest.raises(Exception):
        entity.death()

    # Kill the entity and check to make sure that the death function returns
    # the correct values (exp_val, drops)
    entity.alter_hp(-100)
    assert entity.death() == [5, []] 

def test_operators(entity_data):
    ''' Test the operators of the entity class.'''
    temp_data = entity_data

    temp_data["name"] = "A"
    a = Entity(temp_data)
    temp_data["name"] = "Z"
    z = Entity(temp_data)

    assert a.name == "A"
    assert z.name == "Z" 
    assert a < z
    assert a < 'Z'
    assert a <= z
    assert a <= 'Z'
    assert not a == z
    assert not a == 'Z'
    assert not a > z
    assert not a > 'Z'
    assert not a >= z
    assert not a >= 'Z'
    assert a != z
    assert a != 'Z'
    assert a == "A"

    # Type checking 
    with pytest.raises(TypeError):
        a < 0
        a <= 0
        a == 0
        a > 0
        a >= 0
        a != 0
# End Entity Tests

# Start Hero Tests
def test_create_hero(hero_fixture):
    ''' Test the instantiation of the hero class.'''
    hero = hero_fixture

    assert hero._Hero__inventory == []
    assert hero._Hero__equip == None 
    assert hero._Hero__exp == 0
    assert hero._Hero__level == 1
    assert hero._Hero__level_map[1] == [0, 1, 1, 1]
    assert hero._Hero__max_level == 11  # 11 based on levelmap class

def test_bad_hero_instantiation(hero_data):
    ''' Test the instantiation of the hero class with bad data.'''
    bad_data = hero_data
    bad_data["name"] = 0

    # Check to make sure that the entity class raises a TypeError
    with pytest.raises(TypeError):
            Hero(bad_data)

def test_gain_exp(hero_fixture):
    ''' Test the gain_exp function of the hero class.'''
    hero = hero_fixture

    # Check to make sure that the hero gains exp and levels up
    assert hero.gain_exp(10)
    assert hero._Hero__exp == 10
    assert hero._Hero__level == 2

    hero.gain_exp(10)
    assert hero._Hero__exp == 20
    assert hero._Hero__level == 3

    hero.gain_exp(20)
    assert hero._Hero__exp == 40
    assert hero._Hero__level == 5

def test_force_gain_level(hero_fixture):
    ''' Test the force_gain_level function of the hero class.'''
    hero = hero_fixture

    assert hero.force_gain_level(2)
    assert hero._Hero__exp == 20
    assert hero._Hero__level == 3

    # Type checking
    with pytest.raises(Exception):
        hero.force_gain_level("String")
        hero.force_gain_level(-100)

def test_gain_items(hero_fixture, consumable_item_fixture, equip_item_fixture):
    ''' Test the gain_items function of the hero class.'''
    hero = hero_fixture
    item1 = consumable_item_fixture
    item2 = equip_item_fixture

    assert hero.gain_items(item1) == 1
    assert hero._Hero__inventory == [item1] 
    assert hero.gain_items([item1, item2]) == 2
    assert hero._Hero__inventory == [item1, item1, item2]

    # Check to make sure heros can only get items
    with pytest.raises(TypeError):
        hero.gain_items("String")
        hero.gain_items(0)
        hero.gain_items(False)
        hero.gain_items([0, "String"])
    
def test_equip(hero_fixture, equip_item_fixture, consumable_item_fixture):
    ''' Test the equip function of the hero class.'''
    hero = hero_fixture 
    equippable = equip_item_fixture 
    usable = consumable_item_fixture 
    inventory = [equippable, usable]
    hero.gain_items(inventory)

    assert equippable in hero._Hero__inventory
    assert hero.equip(equippable) == True
    assert hero._Hero__equip == equippable
    assert equippable not in hero._Hero__inventory
    
    # Check to make sure heros can only equip items
    with pytest.raises(Exception):
        hero.equip(usable)
        hero.equip("String")
        hero.equip(0)
        hero.equip(False)

def test_use_item(hero_fixture, equip_item_fixture, consumable_item_fixture):
    ''' Test the use_item function of the hero class.'''
    hero = hero_fixture 
    equippable = equip_item_fixture 
    usable = consumable_item_fixture 
    inventory = [equippable, usable]
    hero.gain_items(inventory)

    assert usable in hero._Hero__inventory
    assert hero.use_item(usable) == [1, 2, 3, 0]
    assert usable in hero._Hero__inventory
    assert hero.use_item(usable) == [1, 2, 3, 0]
    assert usable not in hero._Hero__inventory

    # Check to make sure heros can only use "use" items
    with pytest.raises(Exception):
        hero.use_item(equippable)
        hero.use_item(usable) # This should flag since the item was used up
        hero.use_item("String")
        hero.use_item(0)
        hero.use_item(False)

def test_crewmate_instantiation(crewmate_fixture):
    ''' Test the instantiation of the crewmate class.'''
    crewmate = crewmate_fixture

    assert crewmate._Crewmate__happiness == 100 
    assert crewmate._Crewmate__is_hostile == False 
    assert crewmate._Crewmate__ration_use == 1
    assert crewmate._Crewmate__dialogue == ["Hello there.", "I love the sea."] 
    assert crewmate._Crewmate__hostile_dialogue == ["You're doomed", "I'm going to drown you"] 

def test_feed(crewmate_fixture):
    ''' Test the feed function of the crewmate class.'''
    crewmate = crewmate_fixture
    
    crewmate.feed(1) 
    assert crewmate.happiness == 101
    crewmate.feed(2)
    assert crewmate.happiness == 102

    # Take the happiness down to 0
    for i in range(1000):
        crewmate.feed(0)
    if i < 102:
        assert crewmate.happiness == 102 - (i + 1)
    else:
        assert crewmate.happiness == 0
    
    # Type checking
    with pytest.raises(TypeError):
        crewmate.feed("String")
        crewmate.feed(1.5)
    
    # Bad data
    with pytest.raises(ValueError):
        crewmate.feed(-100)

@pytest.mark.parametrize("change, happiness", [(1, 101), (-1, 99), (-1000, 0)])
def test_alter_happiness(crewmate_fixture, change, happiness):
    ''' Test the alter_happiness function of the crewmate class.'''
    crewmate = crewmate_fixture
    
    crewmate.alter_happiness(change)
    assert crewmate._Crewmate__happiness == happiness 

def test_bad_alter_happiness(crewmate_fixture):
    ''' Test the alter_happiness function of the crewmate class with bad data.'''
    crewmate = crewmate_fixture
    with pytest.raises(TypeError):
        crewmate.alter_happiness("String")
        crewmate.alter_happiness(1.5)

def test_recruit(crewmate_fixture):
    ''' Test the recruit function of the crewmate class.'''
    crewmate = crewmate_fixture

    # This should raise a NotImplementedError, since the recruit function is
    # not implemented in the crewmate class. It "dynamically bound" to the
    # subclasses. (Adventurer, Monster, LostSoul)
    with pytest.raises(NotImplementedError):
        crewmate.recruit()

def test_mutiny_check(crewmate_fixture):
    ''' Test the mutiny_check function of the crewmate class.'''
    crewmate = crewmate_fixture

    # Check to make sure that the mutiny_check function returns the correct
    # values.
    assert crewmate.mutiny_check() == False
    crewmate.alter_happiness(-100)
    assert crewmate._Crewmate__happiness == 0
    assert crewmate.mutiny_check() == True
    crewmate.alter_happiness(1)
    assert crewmate.mutiny_check() == False

def test_talk_and_hostility(crewmate_fixture):
    ''' Test the talk, become_hostile, and become_friendly functions 
    of the crewmate class.'''
    crewmate = crewmate_fixture
    
    assert crewmate.talk() in ["Hello there.", "I love the sea."]
    assert crewmate.become_hostile() == True
    assert crewmate.talk() in ["You're doomed", "I'm going to drown you"]
    assert crewmate.become_friendly() == True
    assert crewmate.talk() in ["Hello there.", "I love the sea."]

def test_adventurer_recruit(adventurer_fixture):
    ''' Test the recruit function of the adventurer class.'''
    adventurer = adventurer_fixture
    
    assert adventurer.recruit() == True
    adventurer.become_hostile()
    assert adventurer.recruit() == False 


@pytest.mark.parametrize("damage, is_recruited", 
                         [(0, False), (-99, True), (-1000, False)])
def test_monster_recruit(monster_fixture, damage, is_recruited):
    '''
    # Test 1: No damage, should not be recruited
    # Test 2: Take enough damage to be recruited
    # Test 3: Take enough damage to die, should not be recruited
    '''
    monster = monster_fixture

    monster.alter_hp(damage)
    assert monster.recruit() == is_recruited

def test_monster_butcher(monster_fixture):
    ''' Test the butcher function of the monster class.'''
    monster = monster_fixture

    assert monster._Monster__ration_val == 5 
    monster.butcher() == monster._Monster__ration_val
    assert monster.is_alive == False

def test_lost_soul_pos(lost_soul_fixture_pos):
    ''' Test the lost_soul class with a positive story.'''
    pos_soul = lost_soul_fixture_pos
    assert pos_soul.is_positive == True
    assert pos_soul.recruit() == True
    assert pos_soul.tell_story() == "This is a positive story the soul will tell"

    pos_soul.alter_hp(-100)
    assert pos_soul.recruit() == False

def test_lost_soul_neg(lost_soul_fixture_neg):
    ''' Test the lost_soul class with a negative story.'''
    neg_soul = lost_soul_fixture_neg

    assert neg_soul.is_positive == False
    assert neg_soul.recruit() == True

    assert neg_soul.tell_story() == "This is a sad story the soul will tell"

    neg_soul.alter_hp(-100)
    assert neg_soul.recruit() == False 

if __name__ == "__main__":
    pytest.main(["-v", "test_entity.py"])