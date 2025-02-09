> Author:      Lorenzo D. Moon  
Instructor:  Karla Fant  
Course:      CS-302  
Assignment:  Program 4 and 5  
Description: README.md for Programs 4 and 5.
             Program #4 is a test suite for the core hierachy of the Entity
             class in the game. It also briefly tests the implementation of 
             a 2-3 Tree. 
             Program #5 is a video game called "LunaSea" where you must reach
             the moon before running out of supplies.

# Program 4: Test Suite for Entity and 2-3 Tree 
## Description
Tests most of the classes required for the game LunaSea.
- Encounter Generator
- Entity > Hero
- Entity > Crewmate > Adventurer/Lost Soul/Monster
- Item
- Tree / Node (2-3 Tree)
- Text Loaders (Loads text files into lists or dictionary) 

## Files For Test Suite 
- encounter_generator.py
- entity.py
- item.py 
- level_map.py
- text_loader.py 
- tree.py
- test_data/test_dict.txt (for text_loader.py)
- test_data/test_list.txt (for text_loader.py)
- test_encounter_generator.py
- test_entity.py 
- test_tree.py 
- test_text_loader.py
- conftest.py

## Dependencies
- Pytest
- Numpy

# Program 5: LunaSea
## Gameplay
The moon has fallen into the sea, you are compelled to sail to the moon.
You must reach the moon before you die, or your crew mutinies.
You can be as cruel or as kind as you want to your crew, but you must
reach the moon before you run out of supplies.

## How to Play
- Run `main.py` to start the game.
- All commands are given by typing in the terminal.
- The commands are always printed to screen before you are prompted for input.
- The game is case-insensitive. You can even just type the first letter
- Example: Attack == attack == a == A
- The game is turn-based. You can take as long as you want to make decisions.
- If you want to cheat, name yourself "Luffy" for extra buffs.
- Upon death, you will be given the option to restart the game or quit.
- You lose your crew, but keep your items (except what you had equipped)

## Files
- text_files/ (contains all the text files for the game)
- text_images/ (contains all the ascii art for the game)
- encounter_generator.py
- entity.py
- item.py
- level_map.py
- lunasea.py
- main.py
- ship.py
- text_loader.py
- tree.py

# Other

## Image Generator
I created the image generator for a previous class and refined it for this project.
It's packaged into a class now and outputs files that are way better than they
used to be (it used to be hardcoded into lists it was awful).
This class isn't directly used in the game, but is used to pre-generate ascii
art for the game. You can find this class in "text_images/image_generator.py".