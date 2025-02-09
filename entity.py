################################################################################
# 
#     Author:      Lorenzo D. Moon
#     Instructor:  Karla Fant
#     Course:      CS-302
#     Assignment:  Program 4/5
#     Description: Hierarchy of classes to represent any entities in the game.
#                  There is a split between the hero and the NPCs.
#                  Entity > CrewMate > Adventurer/Monster/LostSoul
#                  Entity > Hero
#
################################################################################

import numpy as np
from numpy import random
from item import Item
from level_map import LevelMap

class Entity:
    # The Entity class is the base class for all entities in the game.
    # It gets initialized with a dictionary of data loaded from a file/generated
    # By the game NPC generator.

    def __init__(self, data: dict, die_size: int = 20):

        try:
            self.__name = data["name"]           # Name of the entity
            self.__hp_max = data["hp_max"]       # Maximum health points
            self.__hp = data["hp"]               # Current health points
            self.__strength = data["strength"]   # Strength for attack 
            self.__defense = data["defense"]     # Defense for defending 
            self.__exp_val = data["exp_val"]     # Experience value when killed
            self.__drops = data["drops"]         # List of items dropped when killed
        except KeyError as e:
            # Raise error if the key is not found in the data
            raise KeyError(f"Key {e} not found in data") 

        # Make sure all the data types are correct
        if not isinstance(self.__name, str):
            raise TypeError("name must be a string")
        
        if not isinstance(self.__hp_max, int):
            raise TypeError("hp_max must be an integer")
        
        if not isinstance(self.__hp, int):
            raise TypeError("hp must be an integer")
        
        if not isinstance(self.__strength, int):
            raise TypeError("strength must be an integer")
        
        if not isinstance(self.__defense, int):
            raise TypeError("defense must be an integer")
        
        if not isinstance(self.__exp_val, int):
            raise TypeError("exp_val must be an integer")
        
        elif not isinstance(self.__drops, list) and self.__drops is not None:
            raise TypeError("drops must be a list")
        
        # np array for rolling the die - default is a 20 sided die
        # used array because of program requirements
        self.__die_array = np.array([i for i in range(1, die_size + 1)])
        
    
    def __del__(self):
        self.__name = None
        self.__hp_max = None
        self.__hp = None
        self.__strength = None
        self.__defense = None
        self.__exp_val = None
        self.__drops = None
        return
    
    # Read-Only getters
    @property 
    def name(self) -> str:
        return self.__name
    
    @property
    def hp(self) -> int:
        return self.__hp

    @property
    def hp_max(self) -> int:
        return self.__hp_max
    
    def __gt__(self, other: "Entity") -> bool:
        # Use name for comparison. > 

        # If it's a list of entities, use the first one (needed for Tree insertion)
        if isinstance(other, list):
            other = other[0]

        # If it's not a string or an Entity, raise an error
        if not isinstance(other, Entity) and not isinstance(other, str):
            raise TypeError("Other must be an Entity or a string. But was " + str(type(other)))
        
        # If it's a string, compare the name to the string
        if isinstance(other, str):
            return self.name > other

        # If it's an Entity, compare the names of eachother
        return self.name > other.name
    
    def __ge__(self, other: "Entity") -> bool:
        # Use name for comparison. >=

        # If it's a list of entities, use the first one (needed for Tree insertion)
        if isinstance(other, list):
            other = other[0]

        # If it's not a string or Entity, raise an error
        if not isinstance(other, Entity) and not isinstance(other, str):
            raise TypeError("Other must be an Entity or a string. But was " + str(type(other)) + str(other))
        
        # If it's a string, compare the name to the string
        if isinstance(other, str):
            return self.name >= other

        # If it's an Entity, compare the names of eachother
        return self.name >= other.name
    
    def __lt__(self, other: "Entity") -> bool:
        # Use the same logic as the greater than or equal to, just reversed
        return not self >= other 
    
    def __le__(self, other: "Entity") -> bool:
        # Use the same logic as the greater than, just reversed
        return not self > other 
    
    def __eq__(self, other: "Entity") -> bool:
        # Use name for comparison. ==
        
        # This is needed for "== None" since this method throws type errors
        # later on if it's not handled here.
        if other is None: return False

        # If it's a list of entities, use the first one (needed for Tree insertion)
        if isinstance(other, list):
            other = other[0]

        # If it's not a string or an Entity, raise an error
        if not isinstance(other, Entity) and not isinstance(other, str):
            raise TypeError("Other must be an Entity or a string. But was " + str(type(other)) + str(other))
        
        # If it's a string, compare the name to the string
        if isinstance(other, str):
            return self.name == other

        # If it's an Entity, compare the names of eachother
        return self.name == other.name
    
    def __ne__(self, other: "Entity") -> bool:
        # Use the same logic as the equal to, just reversed
        return not self == other 
    
    def __str__(self) -> str:
        # Return the name of the entity, plus the derived type.
        # Ex:  Lorenzo: Lost Soul
        # I could have added this to the __str__ of each class, but I wanted
        # to have a central place for the format of the return

        string = f"{self.name}"
        if isinstance(self, Hero):
            string += f": Fallen Hero"
        if isinstance(self, Monster):
            string += f": Monster"
        if isinstance(self, LostSoul):
            string += f": Lost Soul"
        if isinstance(self, Adventurer):
            string += f": Adventurer"
        return string

    # I decided to keep this public so that game events could be implemented
    # that would just change HP of entities (say something kills your whole crew?)
    # Same with the rest of the "alter" methods
    # It wasn't implemented into the game, but I might keep working on this game
    # after the class is over.
    def alter_hp(self, amount: int) -> None:
        # Instantly change the HP of the entity. Keep it within the 
        # bounds of 0 and the max hp.

        # Type checking
        if not isinstance(amount, int):
            raise TypeError("amount must be an integer")

        # Dead entities can't be healed
        if not self.is_alive:
            return

        self.__hp += amount

        # Make sure the hp doesn't go over the max or under 0
        if self.__hp <= 0:
            self.__hp = 0
            return
        
        if self.__hp > self.hp_max:
            self.__hp = self.hp_max
        return
    
    def alter_strength(self, amount: int) -> None:
        # Instantly change the strength of the entity.
        # Keeps the bounds of the strength >= 0 

        # Type checking
        if not isinstance(amount, int):
            raise TypeError("amount must be an integer")

        self.__strength += amount

        # Make sure the strength doesn't go under 0
        if self.__strength < 0:
            self.__strength = 0
        return
    
    def alter_defense(self, amount: int) -> None:
        # Instantly change the defense of the entity.
        # Keeps the bounds of the defense >= 0

        # Type checking
        if not isinstance(amount, int):
            raise TypeError("amount must be an integer")

        self.__defense += amount

        # Make sure the defense doesn't go under 0
        if self.__defense < 0:
            self.__defense = 0
        return
    
    def roll(self) -> int:
        # Roll a 20 sided die
        # This is where the np array is used
        next_roll = int(random.choice(self.__die_array))
        return next_roll 

    def attack(self, other: "Entity") -> int:
        # This roll gets send to the other entity to see if it takes damage.
        # It returns how much damage it took.

        # If it's not an Entity, raise an error
        if not isinstance(other, Entity):
            raise TypeError("other must be an Entity")

        # Roll for the attack
        attack_roll = self.roll()

        # If the roll is a 1, the attack missed
        if attack_roll == 1:
            return 0
        
        # If the roll is a 20, it's a critical hit
        if attack_roll == 20:
            return other.take_damage(True, attack_roll)

        # Calculate the attack
        # This might be higher than 20, but the bool keeps it from being a crit.
        attack = attack_roll + self.__strength
        return other.take_damage(False, attack)
    
    def take_damage(self, crit: bool, attack: int) -> int:
        # This gets called during "attacK" from another entity (or event)
        # It returns how much damage it took.
        min_crit = 2
        max_crit = 10
        min_damage = 1
        max_damage = 3
        def_fail = -5


        # Type checking
        if not isinstance(crit, bool):
            raise TypeError("crit must be a boolean")
        
        if not isinstance(attack, int):
            raise TypeError("attack must be an integer")

        # Roll for defense
        defense_roll = self.roll()

        # If it's a crit, ignore the defense roll
        if crit:
            damage = random.randint(min_crit, max_crit + 1)
            self.alter_hp(-damage)
            return damage
        
        # If the roll is a 1, the defense failed
        if defense_roll == 1:
            # Failed defense roll, take 2 damage.
            self.alter_hp(def_fail)
            return 2
        
        # If the roll is a 20, the attack was a dodge
        if defense_roll == 20:
            # Dodged the attack 
            return 0
        
        # Calculate the defense
        defense = self.__defense + defense_roll

        # If the attack hits, deal 1-3 damage 
        if attack > defense:
            damage = random.randint(min_damage, max_damage + 1)
            self.alter_hp(-damage)
            return damage
        
        # The attack was defended against
        return 0

    def death(self) -> list:
        # Return the experience value and the drops
        # If the entity is still alive, raise an error
        if self.is_alive:
            raise Exception("Entity is still alive")

        return [self.__exp_val, self.__drops]

    @property
    def is_alive(self) -> bool:
        # If the hp is greater than 0, the entity is alive
        return self.__hp > 0

class Hero(Entity):
    # Same as the Entity class, the Hero class gets initialized with a dictionary
    def __init__(self, data: dict):

        super().__init__(data)

        self.__inventory = []  # List of items
        self.__equip = None    # List of equipped items
        self.__exp = 0         # Experience points
        self.__level = 1       # Level

        self.__level_map = LevelMap().get_map() # Level map
        self.__max_level = max(self.__level_map.keys()) 
    
    def __del__(self):
        # Clean up the data
        super().__del__()
        self.__inventory = None
        self.__equip = None
        self.__exp = None
        self.__level = None
        self.__level_map = None
        return
    
    @property
    def inventory(self) -> list:
        return self.__inventory
    
    def gain_exp(self, amount: int) -> int:
        # Gain experience points

        # Type checking
        if not isinstance(amount, int):
            raise TypeError("amount must be an integer")

        self.__exp += amount

        # Return 0 if the exp has not gone over the level threshold
        # Else return the amount of levels gained.
        return self.gain_level()
    
    def gain_level(self) -> int:
        # If the exp has gone over the level threshold, gain a level
        # and repeat until the exp is less than the level threshold
        count = 0

        # The order of this while loop matters or else it will crash looking
        # for a key that doesn't exist.
        while (self.__level < self.__max_level and 
               self.__exp >= self.__level_map[self.__level + 1][0]):
            self.__level += 1
            self.alter_hp(self.__level_map[self.__level][1])
            self.alter_strength(self.__level_map[self.__level][2])
            self.alter_defense(self.__level_map[self.__level][3])
            count += 1
        return count 

    def force_gain_level(self, levels) -> None:
        # Force a level gain (like with an Item or event)

        # Type checking
        if not isinstance(levels, int):
            raise TypeError("trigger must be an integer")
        
        # Error checking
        if levels < 0:
            raise ValueError("trigger must be a non-negative integer")
        
        # If the levels are 0, return 0 (Useful for items passing data)
        if levels == 0:
            return 0

        # Can't level up past max level
        if self.__level == self.__max_level:
            return 0

        # If the levels are greater than the max level, set the exp to the max level
        if self.__level + levels > self.__max_level:
            self.__exp = self.__level_map[self.__max_level][0]
        else:
            self.__exp = self.__level_map[self.__level + levels][0]
        return self.gain_level()
    
    def gain_items(self, incoming_drops) -> int:
        # Get items dropped from a monster, event, or murder and put them in inventory

        # Make sure the drop is a list or a single item
        if not isinstance(incoming_drops, list) and not isinstance(incoming_drops, Item):
            raise TypeError("incoming_drops must be a list or single item")
        
        # If it's just one item, add it to the inventory
        if isinstance(incoming_drops, Item):
            self.__inventory.append(incoming_drops)
            return 1
        
        # Loop through drops and make sure they're all items, and add them to 
        # the inventory
        for drop in incoming_drops: 
            if not isinstance(drop, Item):
                raise TypeError("incoming_drops must be a list of Items")

            self.__inventory.append(drop)

        return len(incoming_drops)
    
    def equip(self, item: Item) -> bool:
        # Equip an item
        if not isinstance(item, Item):
            raise TypeError("item must be an Item")
        
        if item not in self.__inventory:
            raise ValueError("item must be in the inventory")
        
        if not item.can_equip:
            raise ValueError("item must be equippable")
        
        # Move current equipment to the inventory
        if self.__equip is not None:
            self.unequip()
        
        # Set the item, and use it to set new stats
        self.__equip = item                 
        stats = item.equip()

        # Alter the stats
        self.alter_hp(stats[0])
        self.alter_strength(stats[1])
        self.alter_defense(stats[2])
        self.force_gain_level(stats[3])

        # Remove the item from the inventory
        self.__inventory.remove(item)
        return True
    
    def unequip(self) -> bool:
        # Public so it can be called from the game
        # Unequip an item
        if self.__equip is None:
            return False
        
        # Use the item to set the old stats
        # Get the stats from the item
        stats = self.__equip.unequip()

        # Altthe stats
        self.alter_hp(stats[0])
        self.alter_strength(stats[1])
        self.alter_defense(stats[2])
        self.force_gain_level(stats[3])
        
        # Add the item back to the inventory
        self.__inventory.append(self.__equip)
        self.__equip = None
        return True
    
    def use_item(self, item: Item) -> None:
        # Use an item to alter stats
        if not isinstance(item, Item):
            raise TypeError("item must be an Item")
        
        if item not in self.__inventory:
            raise ValueError("item must be in the inventory")
        
        # Get the stats from the item
        stats = item.use()

        # Alter the stats
        self.alter_hp(stats[0])
        self.alter_strength(stats[1])
        self.alter_defense(stats[2])
        self.force_gain_level(stats[3])

        # Remove the item from the inventory if it's empty (like a potion)
        if item.empty: 
            self.__inventory.remove(item)

        return stats

class Crewmate(Entity):
    # The Crewmate class is the base class for all NPCs in the game.
    # It gets initialized with a dictionary of data loaded from a file/generated
    # By the game NPC generator.

    def __init__(self, data):
        super().__init__(data)

        # Make sure all the data is in the dictionary
        try:
            self.__happiness = data["happiness"]
            self.__is_hostile = data["is_hostile"] 
            self.__ration_use = data["ration_use"] 
            self.__dialogue = data["dialogue"] 
            self.__hostile_dialogue = data["hostile_dialogue"] 
        except KeyError as e:
            raise KeyError(f"Key {e} not found in data")
    
        # Make sure all the data types are correct
        if not isinstance(self.__happiness, int):
            raise TypeError("happiness must be an integer")
        
        if not isinstance(self.__is_hostile, bool):
            raise TypeError("is_hostile must be a boolean")
        
        if not isinstance(self.__ration_use, int):
            raise TypeError("ration_use must be an integer")
        
        if not isinstance(self.__dialogue, list):
            raise TypeError("dialogue must be a list")
        
        if not isinstance(self.__hostile_dialogue, list):
            raise TypeError("hostile_dialogue must be a list")
       
    @property
    def ration_use(self) -> int:
        # Getter for the ration use, used for feeding the crew
        return self.__ration_use
        
    @property
    def happiness(self):
        # Getter for the happiness, used for mutiny checks
        return self.__happiness
    
    @property
    def is_hostile(self) -> bool:
        # Getter for the hostility, used for talking and mutiny checks
        return self.__is_hostile
    
    def feed(self, rations) -> None:
        # Feed the crew, and alter the happiness based on the rations

        # Type checking
        if not isinstance(rations, int):
            raise TypeError("rations must be an integer")

        # You can't negative feed the crew 
        if rations < 0:
            raise ValueError("rations must be a non-negative integer")

        # If the rations are less than the ration use, lower the happiness
        if rations < self.__ration_use:
            self.alter_happiness(-1)

        # If the rations are greater than the ration use, raise the happiness 
        if rations >= self.__ration_use:
            self.alter_happiness(1)
        
    def alter_happiness(self, amount: int) -> None:
        # Alter the happiness of the crewmate

        # Type checking
        if not isinstance(amount, int):
            raise TypeError("amount must be an integer")
        
        
        self.__happiness += amount

        # Make sure the happiness doesn't go under 0
        if self.__happiness < 0:
            self.__happiness = 0
        return
    
    def recruit(self) -> None:
        # You cannot recruit a 'crewmate', must be called from a derived class
        # This makes sure that the recruit method is implemented in the derived class
        raise NotImplementedError("Recruit method not implemented for Crewmate."
                                  "Must be called from a derived class")
    
    def mutiny_check(self) -> bool:
        # Check if the crewmate is unhappy enough to start a mutiny
        # This will be used by the ship class to determine a gameover
        if self.__happiness == 0:
            return True
        return False
    
    def talk(self) -> str:
        # Talk to the crewmate, get a response based on hostility
        # Responses will be randomly selected from the dialogue list
        if self.__is_hostile:
            return random.choice(self.__hostile_dialogue)
        return random.choice(self.__dialogue)
    
    def become_hostile(self) -> bool:
        # Make the crewmate hostile
        # Useful for attacking adventurers, or good monsters
        self.__is_hostile = True
        return self.__is_hostile
    
    def become_friendly(self) -> bool:
        # Make the crewmate friendly
        # A monster will become friendly after being recruited.
        # Lost souls will also become friendly after being recruited.
        self.__is_hostile = False
        return not self.__is_hostile

class Adventurer(Crewmate):
    # The Adventurer class is a derived class from the Crewmate class
    # They are intended to be recruited to help with your journey
    # It gets initialized with a dictionary of data loaded from a file/generated
    # By the game NPC generator.
    def __init__(self, data):
        # There are no unique attributes for the adventurer class
        # Just the way they are recruited
        super().__init__(data)
    
    def recruit(self) -> bool:
        if self.is_hostile and self.is_alive:
            return False
        self.alter_hp(self.hp_max)
        return True

class Monster(Crewmate):
    # The Monster class is a derived class from the Crewmate class
    # They are to be killed for rations, or be a strong crewmember
    # It gets initialized with a dictionary of data loaded from a file/generated
    # By the game NPC generator.

    def __init__(self, data):
        super().__init__(data)

        self.recruit_health = 2
        
        # Monsters have a "ration value" for butchering
        # Make sure it's in the dictionary
        try:
            self.__ration_val = data["ration_val"] 
        except KeyError as e:
            raise KeyError(f"Key {e} not found in data")

        # Type Checking 
        if not isinstance(self.__ration_val, int):
            raise TypeError("ration_val must be an integer")
    
    def recruit(self) -> bool:
        # As long as they're alive, they can be recruited when their hp is low 
        if self.hp <= self.recruit_health and self.is_alive:
            # Heal the monster when they join
            self.alter_hp(self.hp_max)
            return True 
        return False
    
    def butcher(self) -> int:
        # Butcher can be forced ran when the monster is in the crew.
        if self.is_alive:
            # Kill the monster
            self.alter_hp(-self.hp)
        # Return the rations
        return self.__ration_val

class LostSoul(Crewmate):
    # The LostSoul class is a derived class from the Crewmate class
    # Lost souls will always be recruitable. They will either help with
    # Keeping the entire crew happy, or make every sadder.
    # It gets initialized with a dictionary of data loaded from a file/generated
    # By the game NPC generator.

    def __init__(self, data):
        super().__init__(data)
        
        # Make sure all the data is in the dictionary
        try: 
            self.__is_positive = data["is_positive"] # If the lost soul is going to be helpful or hurtful 
            self.__story = data["story"]             # The story of the lost soul
        except KeyError as e:
            raise KeyError(f"Key {e} not found in data")

        # Type checking
        if not isinstance(self.__is_positive, bool):
            raise TypeError("is_positive must be a boolean")
        
        if not isinstance(self.__story, str):
            raise TypeError("story must be a string")
                
    @property
    def is_positive(self) -> bool:
        return self.__is_positive

    def recruit(self) -> bool:
        # As long as they're alive, they can be recruited
        return self.is_alive
    
    def tell_story(self) -> str:
        # Flavor text for the game
        return self.__story