################################################################################
# 
#     Author:      Lorenzo D. Moon
#     Instructor:  Karla Fant
#     Course:      CS-302
#     Assignment:  Program 4/5
#     Description: This holds all the possible entities that can be encountered
#                  in the game.
#                  When running "encounter" it will return a random entity from
#                  the list of entities.
#
################################################################################

from entity import Adventurer, Monster, LostSoul 
from item import Item
from text_loader import TextToDict, TextToList
import random

class EncounterGenerator:
    def __init__(self):
        # The text loaders
        self.__text_to_dict = TextToDict() # Load text files into a dictionary
        self.__text_to_list = TextToList() # Load text files into a list

        # All the lists of data to load
        self.__names = []            # A list of names for Adventurers and Lost Souls
        self.__monsters = []         # A list of data for monsters
        self.__lost_souls = []       # A list of data lost souls
        self.__items = []            # A list of items
        self.__adv_dialogue = []     # A list of dialogue for adventurers
        self.__adv_h_dialogue = []   # A list of hostile dialogue for adventurers
        self.__mons_dialogue = []    # A list of dialogue for monsters
        self.__mons_h_dialogue = []  # A list of hostile dialogue for monsters
        self.__lost_dialogue = []    # A list of dialogue for lost souls
        self.__lost_h_dialogue = []  # A list of hostile dialogue for lost souls
        self.__lost_sad = []         # A list of sad stories for lost souls
        self.__lost_happy = []       # A list of happy stories for lost souls
        self.__adventurers = []      # A list of data for adventurers

        # All the files that will be loaded
        self.__names_file = "./text_files/data_names.lunasea"
        self.__item_file = "./text_files/data_items.lunasea"
        self.__adv_file = "./text_files/data_adventurers.lunasea"
        self.__mons_file = "./text_files/data_monsters.lunasea"
        self.__lost_file = "./text_files/data_lostsouls.lunasea"
        self.__adv_hd_file = "./text_files/dialogue_adventurers_hostile.lunasea"
        self.__adv_d_file = "./text_files/dialogue_adventurers.lunasea"
        self.__mons_hd_file = "./text_files/dialogue_monsters_hostile.lunasea"
        self.__mons_d_file = "./text_files/dialogue_monsters.lunasea"
        self.__lost_d_file = "./text_files/dialogue_lostsouls.lunasea"
        self.__lost_hd_file = "./text_files/dialogue_lostsouls_hostile.lunasea"
        self.__lost_story_sad = "./text_files/story_lostsouls_sad.lunasea"
        self.__lost_story_happy = "./text_files/story_lostsouls_happy.lunasea"

        # Encounter Rates based on percentage of distance
        # [None, Adventurer, Monster, Lost Soul]
        self.__25 = [10, 50, 20, 20]
        self.__50 = [10, 40, 30, 20]
        self.__75 = [10, 30, 40, 20]
        self.__100 = [10, 20, 50, 20]

        self.__load_everything()
    
    def __load_everything(self):
        # Loads all the data from the files.
        # This is called in the constructor
        self.__items = self.__load_items()
        self.__names = self.__load_names()
        self.__adv_dialogue = self.__load_dialogue(self.__adv_d_file)
        self.__adv_h_dialogue = self.__load_dialogue(self.__adv_hd_file)
        self.__mons_dialogue = self.__load_dialogue(self.__mons_d_file)
        self.__mons_h_dialogue = self.__load_dialogue(self.__mons_hd_file)
        self.__lost_dialogue = self.__load_dialogue(self.__lost_d_file)
        self.__lost_h_dialogue = self.__load_dialogue(self.__lost_hd_file)
        self.__lost_story_sad = self.__load_dialogue(self.__lost_story_sad)
        self.__lost_story_happy = self.__load_dialogue(self.__lost_story_happy)
        self.__adventurers = self.__load_adventurers()
        self.__monsters = self.__load_monsters()
        self.__lost_souls = self.__load_lost_souls()
    
    def __load_items(self):
        # Loads all the items from the file, and creates an item for 
        # each item in the file. Appends it to a list, and returns the list.
        items = []
        self.__text_to_dict.load_file(self.__item_file)
        item_dict = self.__text_to_dict.data
        for item in item_dict:
            items.append(Item(item))
        return items
        
    def __load_names(self):
        # Loads all the names from the file, and returns the list of names
        names = []
        self.__text_to_list.load_file(self.__names_file)
        names = self.__text_to_list.data
        return names

    def __load_adventurers(self):
        # This takes in the data from the adventurers file and creates 100  
        # random adventurers. It returns a list of adventurers.
        adventurer_count = 100
        self.__text_to_dict.load_file(self.__adv_file)
        data = self.__text_to_dict.data 
        objects = []

        # Make a bunch of adventurers.
        for i in range(adventurer_count):
            for _dict in data:
                _dict["name"] = random.choice(self.__names)
                _dict["dialogue"] = []         # Create a list to hold dialogue
                _dict["hostile_dialogue"] = [] # Create a list to hold dialogue

                # Give the adventurer some random dialogue
                for i in range(3):
                    _dict["dialogue"].append(random.choice(self.__adv_dialogue))
                    _dict["hostile_dialogue"].append(random.choice(self.__adv_h_dialogue))

                # Give the adventurer some random items from the item list
                _dict["drops"] = self.__generate_drops() 

                # Create the adventurer and append it to the list
                objects.append(Adventurer(_dict)) 

        # Return the list of adventurers
        return objects

    def __load_monsters(self):
        # Almost same as load_adventurers, but for monsters
        monster_count = 100
        self.__text_to_dict.load_file(self.__mons_file)
        data = self.__text_to_dict.data
        monsters = []

        # Make a bunch of monsters
        for i in range(monster_count):
            for _dict in data:
                _dict["dialogue"] = []           # Create a list to hold dialogue
                _dict["hostile_dialogue"] = []   # Create a list to hold dialogue

                for i in range(3):
                    _dict["dialogue"].append(random.choice(self.__mons_dialogue))
                    _dict["hostile_dialogue"].append(random.choice(self.__mons_h_dialogue))

                _dict["drops"] = self.__generate_drops()
                monsters.append(Monster(_dict))
            
        # Return the list of monsters
        return monsters

    def __load_lost_souls(self):
        # Almost same as load_adventurers, but for lost souls
        soul_count = 100
        self.__text_to_dict.load_file(self.__lost_file)
        data = self.__text_to_dict.data 
        souls = []

        # Make a bunch of lost souls
        for i in range(soul_count):
            for _dict in data:
                _dict["name"] = random.choice(self.__names)
                _dict["drops"] = self.__generate_drops()

                _dict["dialogue"] = []           # Create a list to hold dialogue
                _dict["hostile_dialogue"] = []   # Create a list to hold dialogue

                for i in range(3):
                    _dict["dialogue"].append(random.choice(self.__lost_dialogue))
                    _dict["hostile_dialogue"].append(random.choice(self.__lost_h_dialogue))

                # Give them a positive or negative story
                if _dict["is_positive"]:
                    _dict["story"] = random.choice(self.__lost_story_happy) 
                else:
                    _dict["story"] = random.choice(self.__lost_story_sad)

                souls.append(LostSoul(_dict))
        
        # Return the list of lost souls
        return souls 
    
    def __load_dialogue(self, file):
        # Load all the dialogue lines in from file to a list 
        dialogue = []
        self.__text_to_list.load_file(file)
        dialogue = self.__text_to_list.data
        return dialogue
    
    def encounter(self, cur_distance, total_distance):
        # This will return a random encounter based on the current distance

        # Get the encounter rate
        rate = self.__encounter_rate(cur_distance, total_distance)

        # Roll for the encounter
        roll = self.__roll()

        # Choose the encounter
        next_encounter = self.__choose_encounter(rate, roll)
        return next_encounter
    
    def __roll(self):
        # Generate a random number between 1 and 100
        return random.randint(1, 100)
    
    def __encounter_rate(self, cur_distance, total_distance):
        # This will return the encounter rate based on the current distance
        percent_complete = (cur_distance / total_distance) * 100

        # Chance for each type of encounter:
        if percent_complete <= 25:
            return self.__25
        elif percent_complete <= 50:
            return self.__50
        elif percent_complete <= 75:
            return self.__75
        else:
            return self.__100

    def __choose_encounter(self, roll_options, roll):
        none_chance = roll_options[0]
        adv_chance = roll_options[1] + none_chance
        mons_chance = roll_options[2] + adv_chance
        # lost_chance = roll_options[3] + mons_chance # Not Needed

        if roll <= none_chance:
            return None
        elif roll <= adv_chance:
            return self.encounter_adventurer()
        elif roll <= mons_chance:
            return self.encounter_monster()

        return self.encounter_lost_soul()

    def encounter_adventurer(self):
        # This will return a random adventurer from the list of adventurers
        return random.choice(self.__adventurers) 

    def encounter_monster(self):
        # This will return a random monster from the list of monsters
        return random.choice(self.__monsters)

    def encounter_lost_soul(self):
        # This will return a random lost soul from the list of lost souls
        return random.choice(self.__lost_souls) 
    
    def pop_random_name(self):
        # Take a name from the list of names remove and return it
        return self.__names.pop(random.randint(0, len(self.__names)-1))
    
    def __generate_drops(self):
        # Return a list of items that will be dropped if you kill the entity
        # Theres a chance of no items
        drop_count = random.randint(0, 3)
        drops = []
        for i in range(drop_count):
            drops.append(random.choice(self.__items))
        return drops

    def flee(self):
        # Roll two die, if the first roll is higher than the second,
        # This ends the encounter
        # 50%ish chance to flee. Tie is a lose.
        roll1 = self.__roll()
        roll2 = self.__roll()
        if roll1 > roll2:
            return True
        return False