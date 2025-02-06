################################################################################
# 
#     Author:      Lorenzo D. Moon
#     Instructor:  Karla Fant
#     Course:      CS-302
#     Assignment:  Program 4/5
#     Description: This class contains everything you need to run LunaSea.
#                  There is also an "OpeningSequence" class that is used to
#                  crudely animate the opening sequence.
#                  
#                  To play LunaSea run the "main.py" file in the root directory.
#
################################################################################

from encounter_generator import EncounterGenerator
from tree import Tree
from entity import Hero, Adventurer, Monster, LostSoul
from item import Item
from ship import Ship
from text_loader import TextToDict, TextToList
import os
import random
from time import sleep # To animate intro

class LunaSea():
    def __init__(self):
        self.__hero = None              # Initialized at game start
        self.__dead = Tree()            # A tree of everything that has died
        self.__crew = [] 
        self.__encounter_generator = EncounterGenerator() 
        self.__ship = None              # Initialized at game start

        self.__new_life_inventory = []  # Items that the hero had when they died
        self.__days_at_sea = 0          # Number of days passed in the current game.
        self.__distance_to_moon = 80    # Distance to the moon
        self.__traveled_distance = 0    # Distance traveled by the ship

        self.__text_to_dict = TextToDict() # Text loader
        self.__text_to_list = TextToList() # Text loader

        self.__width = 80 # Width of the console text

        self.__prompt = ">> "          # Symbol to prompt the user
        self.__is_game_over = False    # Game over flag
        self.__game_running = True     # Game running flag

        # I have a seperate class handle the opening sequence
        self.__opening_sequence = OpeningSequence(self.__width)
    
    def play(self):
        self.__opening_sequence.play()      # Play the opening sequence
        while self.__game_running:          # Outer game loop
            self.__intro()                  # Game intro
            while not self.__is_game_over:  # Inner game loop
                self.__day_cycle()          # Day cycle
                self.__encounter()          # Encounter
                self.__night_cycle()        # Night cycle
                self.__encounter()          # Encounter
                self.__end_of_day()         # End of day
            self.__game_over()              # Game over
        return
    
    def __intro(self) -> None:
        # Setup the game and display the intro

        start_rations = 100
        ship_speed = 5

        self.__is_game_over = False               # Reset game over flag
        self.__clear_screen()                     # Clear the screen
        self.__create_hero()                      # Create the hero
        self.__ship = Ship(rations=start_rations, speed=ship_speed) # Create the ship
        self.__days_at_sea = 0                    # Reset days at sea
        self.__traveled_distance = 0              # Reset traveled distance
        self.__pickup_inventory()                 # If this is the second life, pickup inventory

        # Prompt the user to set sail
        print(f"Press enter to set sail for the moon, {self.__hero.name}!".center(self.__width))
        input()
        return

    def __centered_text(self, file_name: str) -> None:
        # Takes any text file and prints, and centers it. 
        self.__text_to_list.load_file(file_name)
        for line in self.__text_to_list.data:
            print(line.center(self.__width))
        return
    
    def __create_hero(self):
        # Prompt the user to create a hero
        # Return the hero

        print(self.__moon_map()) 

        # Print the intro text with some space above and below
        for i in range(3): print()
        self.__centered_text("./text_files/text_start_journey.lunasea")
        for i in range(3): print()

        # Create hero
        print("Do you remember your name?".center(self.__width))
        # Clear input stream

        name = input(f"{self.__prompt}")
       
        while len(name) < 2 or name.lower() == "no" or name.lower() == "yes":
            # If the name is too short, or the user is being difficult
            # Prompt the user to enter a name again
            if len(name) < 1:
                print("Don't ignore me. What is your name?".center(self.__width))
                name = input(self.__prompt)
            
            if len(name) < 2:
                print("That's not a name. What is your name?".center(self.__width))
                name = input(self.__prompt)

            # If the user doesn't remember their name, give them a random one.
            if name.lower() == "no":
                print("Shame. You were a great hero.".center(self.__width))
                print("I shall give you a name.".center(self.__width))
                name = self.__random_name()
            
            # If the answer is "yes" that's not a name, still prompt for a name
            if name.lower() == "yes":
                print("Good. Do you want to tell me?".center(self.__width))
                name = input(self.__prompt)


        # Load the default hero data, and create the hero
        self.__text_to_dict.load_file("./text_files/data_default_hero.lunasea")
        data = self.__text_to_dict.data[0]
        data["name"] = name
        self.__hero = Hero(data)
        self.__cheat_check() # I put in one cheat code, read this function to find out what it is
        return
    
    def __cheat_check(self):
        # If the hero's name is Luffy, give them the Gomu Gomu no Mi, and give
        # them stupid stats. 

        if self.__hero.name == "Luffy":
            # Create a secret item data 
            secret_item = {
                "name" : "Gomu Gomu no Mi",
                "can_equip" : False,
                "can_use" : True,
                "uses" : 1,
                "strength" : 100,
                "defense" : 100,
                "hp" : 1000,
                "levels" : 0
            } 
            gomugomunomi = Item(secret_item)     # Create the item
            self.__hero.gain_items(gomugomunomi) # Give the hero the item
            self.__hero.use_item(gomugomunomi)   # Use the item
            print("I'll become the King of the Pirates!".center(self.__width))
    
    def __pickup_inventory(self):
        # When a player dies, their inventory washes up on shore, and your new
        # life picks it up on the way to the ship.
        if self.__new_life_inventory != []:
            print(f"As you make your way to the ship, you spot familiar items on the shore".center(self.__width))
            print(f"Like you had owned them in a past life... You place them in your bag".center(self.__width))
            self.__hero.gain_items(self.__new_life_inventory)

            # Clear the games inventory so there aren't duplicates if you die again
            self.__new_life_inventory = []
        return
    
    def __moon_map(self):
        # Prints a map leading to the moon.
        # Legend: > = Ship, ◯ = Moon, ~ = Sea
        # This isn't explained in the game, just some flavor at the top.

        output = ""
        for i in range(1, self.__distance_to_moon + 1):
            if i == self.__traveled_distance:
                output += '>'
            elif i == self.__distance_to_moon:
                output += '◯'
            else:
                output += '~'
        return output
    
    def __clear_screen(self):
        # Clear the screen, should work with Linux, MacOS, and Windows.
        # Tested with Linux and Windows.
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def __random_name(self) -> str:
        # Return a random name from the encounter generator
        # This takes it out of the pool if the hero gets a random name.
        return self.__encounter_generator.pop_random_name()
    
    def __day_cycle(self):
        # Once the game gets going this starts the main loop.

        if self.__is_game_over: return   # If there is a game over, return
        self.__clear_screen()            # Clear the screen
        print(self.__moon_map() + '\n')  # Print the moon map
        self.__status()                  # Print the status
        self.__day_menu()                # Handly daily tasks 
        self.__sail()                    # Sail
        return
    
    def __sail(self):
        # Move the ship based on ship speed.
        self.__traveled_distance += self.__ship.distance_sailed() 
    
    def __day_menu(self):
        # The main menu for the day cycle

        crew_fed = False # Flag to check if the crew was fed

        # Menu options
        menu = ["Feed Crew", "Sail", "Quit"]

        # If there is no crew, remove the feed crew option
        if self.__crew == []:
            menu.remove("Feed Crew")
        
        # The loop should always end in sail unless the player quits
        choice = ''
        while choice != "sail":
            choice = self.__get_input_from_menu(menu, 
                        f"Good Morning, Captain {self.__hero.name}. What are your orders?")
            if choice.lower() == "feed crew":
                spent_rations = self.__ship.feed_crew(self.__crew)
                print(f"The crew ate {spent_rations} rations.".center(self.__width))
                print(f"You have {self.__ship.rations()} rations left.".center(self.__width))
                crew_fed = True

            if choice.lower() == "quit":
                self.__quit_request()
        
        # Time to continue sailing away
        if not crew_fed:
                if not crew_fed and self.__crew != []:
                    for crew in self.__crew:
                        crew.feed(0)
                    print("You're a rotten captain. We are hungry. But orders is orders.".center(self.__width))
                    self.__enter_to_continue()

    def __quit(self):
        # Quit the game and exit the program.
        print("The moon holds no power over you. You are free.".center(self.__width))
        exit()
    
    def __status(self):
        # Print the current statuses
        print(f"Days at Sea: {self.__days_at_sea}")
        print(f"Total Rations: {self.__ship.rations()}")
        print(f"{self.__ship.days_left(self.__crew)} days of food remain")
        print(f"HP: {self.__hero.hp}")

        # Print a star for each crew member's happiness
        # If the crewmember is happy, print a full star, if not, print an empty star
        if self.__crew != []:
            happiness = [] 
            for crew in self.__crew:
                if crew.happiness > 0:
                    happiness.append("★")
                else:
                    happiness.append("☆")
            happiness.sort()
            happiness = "".join(happiness)

            print(f"Crew Happiness: {happiness}")
            
        return
    
    def __encounter(self):
        # Checks for encounters, and goes into a battle (or not) 

        if self.__is_game_over: return
        menu = ["Attack", "Recruit", "Item", "Flee", "Quit"]

        # Generate an encounter based on the current distance
        encounter = None
        encounter = self.__encounter_generator.encounter(
            self.__traveled_distance, self.__distance_to_moon)

        self.__clear_screen()
        print(self.__moon_map() + '\n')
        # If there is no encounter, continue on your journey
        if encounter == None:
            print("The seas are calm. You continue on your journey.".center(self.__width))
            self.__enter_to_continue()
            return

        # if there is an encounter, print it's name.
        print(f"You have encountered {encounter.name}!".center(self.__width)) 
        
        encounter_loop = True 
        while encounter_loop:
            # If there is an encounter, handle it
            print(encounter.talk().center(self.__width))

            # Hero Phase
            prompt = ""
            # If the enemeny is hostile, you'll know you should attack or flee
            if encounter.is_hostile:
                prompt = "Quickly Captain! What are you orders!?"
            else:
                prompt = f"What are you orders, Captain {self.__hero.name}?"
            option = self.__get_input_from_menu(menu, prompt)

            # If you attack, the encounter becomes hostile
            if option == "attack":
                if not encounter.is_hostile:
                    encounter.become_hostile()

                # Send an attack to the encounter
                self.__send_attack(self.__hero, encounter)

                # Send your whole crew to attack
                if encounter.is_alive:
                    for crew in self.__crew:
                        if crew.is_alive and encounter.is_alive:
                            self.__send_attack(crew, encounter)
            
            # If you recruit, see if the entity is recruitable.
            if option == "recruit":
                # If a success, end the encounter and add the entity to the crew
                if encounter.recruit():
                    self.__crew.append(encounter)
                    print(f"You have recruited {encounter.name} to your crew!".center(self.__width))
                    print("They will help you on your journey.".center(self.__width))
                    self.__enter_to_continue()
                    return
                else:
                    # If a failure, print a message
                    print(f"The {encounter.name} refuses to join your crew.".center(self.__width))
            
            if option == "item":
                # If you have items, go into the item menu loop
                self.__item_menu()
                
            if option == "flee":
                # Try to escape, it's roughly a 50% chance
                if self.__encounter_generator.flee():
                    print("You flee from the encounter.".center(self.__width))
                    encounter_loop = False

                    # Secretly make a leap in distance when you flee
                    # Fleeing is a great way to win the game.
                    self.__sail()
                    self.__enter_to_continue()
                    break 
                else:
                    # Print failed message
                    print("You fail to flee from the encounter.".center(self.__width))
            
            # If they want to quit, double check and quit
            if option == "quit":
                self.__quit_request()
            
            # If the encounter is dead, leave the loop, otherwise give them a turn
            if not encounter.is_alive: break 
            
            # Encounter Phase
            # If they're hostile, they're going to attack
            if encounter.is_hostile:
                # If you have a crew, it will attack a crew member first
                if self.__crew != []:
                    crew = random.choice(self.__crew)
                    if crew.is_alive:
                        self.__get_attacked(encounter, crew)
                        if not crew.is_alive:
                            # If the crew member dies, remove them from the crew
                            # Insert them into the dead tree
                            self.__dead.insert(crew)
                            self.__crew.remove(crew)
                            print(f"{crew.name} has died.".center(self.__width))
                else:
                    # If you don't have a crew, the encounter will attack you
                    self.__get_attacked(encounter, self.__hero)
                    if not self.__hero.is_alive:
                        # If you die, insert yourself into the dead tree
                        # Set the game over flag
                        self.__dead.insert(self.__hero)
                        self.__trigger_gameover()
                        return
            else:
                # Print a speech message from the encounter
                encounter.talk()
        return
    
    def __trigger_gameover(self):
        # Set the game over flag to true
        self.__is_game_over = True
        return
    
    def __item_menu(self):
        # Prints a menu of the items
        # If you have items, you can use them
        # If you have items, you can equip them
        # They automatically know to use or equip.
        menu = []

        # if you have no items, print a message and return
        if self.__hero.inventory == []:
            print(f"{self.__hero.name} has no items.".center(self.__width))
            return

        # Create the menu list
        for item in self.__hero.inventory:
            menu.append(item.name)
        
        # Add the return option
        menu.append("Return")
        
        # Print the menu, and get the user's choice
        choice = self.__get_input_from_menu(menu,
                    f"What item would you like from below deck?")

        # Find the item in the inventory and use it (or equip it)
        # To prevent using all of one item, "return" after the item is used.
        for item in self.__hero.inventory:
            item_name = item.name.lower()
            if choice == item_name:
                if item.can_equip:
                    self.__hero.equip(item)
                    print(f"{self.__hero.name} has equipped {item.name}.".center(self.__width))
                    return
                else:
                    stat_change = self.__hero.use_item(item)
                    print(f"{self.__hero.name} has used {item.name}.".center(self.__width))
                    for i in range(len(stat_change)):
                        # I regret not making this a dictionary but 
                        # I don't want to change all my testing.
                        if i == 0 and stat_change[i] != 0:
                            print(f"{self.__hero.name} gained {stat_change[i]} strength.".center(self.__width))
                        if i == 1 and stat_change[i] != 0:
                            print(f"{self.__hero.name} gained {stat_change[i]} defense.".center(self.__width))
                        if i == 2 and stat_change[i] != 0:
                            print(f"{self.__hero.name} gained {stat_change[i]} health.".center(self.__width))
                        if i == 3 and stat_change[i] != 0:
                            print(f"{self.__hero.name} gained {stat_change[i]} levels.".center(self.__width))
                return
    
    def __send_attack(self, attacker, defender):
        # Prevents the dead from attacking during a loop before they're flushed.
        if not attacker.is_alive: return

        # Send attacks as the captain (and crew)
        other_damage = attacker.attack(defender)

        # If you miss, print a miss message, or show the damage
        if other_damage == 0:
            print(f"{attacker.name} missed.".center(self.__width))
        else:
            print(f"{attacker.name} hit {defender.name} for {other_damage} damage.".center(self.__width))

        # Check if the entity dies
        if not defender.is_alive:
            self.__dead.insert(defender) # Insert the entity into the dead tree
            self.__clear_screen()        # Clear the screen
            print(self.__moon_map() + '\n') # Print the moon map

            # If the defender is NOT a hero, print a death message
            # This check I think was coded out by not using "send_attack" with
            # the monsters, but I don't want to break anything at this point
            if not isinstance(defender, Hero):
                print(f"{defender.name} has been defeated!".center(self.__width))
                loot = defender.death() # Get the loot 
                self.__hero.gain_exp(loot[0]) # Give the experience to the hero

                # If there's items, give them to the hero
                if loot[1] != []: 
                    self.__hero.gain_items(loot[1])
                    print(f"{self.__hero.name} has gained {loot[1]} items.".center(self.__width))
                else:
                    # If there's no items, print a message
                    print(f"{defender.name} dropped no items.".center(self.__width))
                # Print a message about the experience
                print(f"{self.__hero.name} has gained {loot[0]} experience.".center(self.__width))

                # If the defender is a monster, butcher it for rations
                if isinstance(defender, Monster):
                    meat = defender.butcher() # Get the ration amount
                    self.__ship.gain_rations(defender.butcher()) # Gain the rations
                    # Print a message about the rations
                    print(f"The {defender.name} has been butchered for {meat} rations.".center(self.__width))

                self.__enter_to_continue()
    
    def __get_attacked(self, attacker, defender):
        # Prevents the dead from attacking during a loop before they're flushed.
        if not attacker.is_alive: return

        # Get attacked by the attacker
        # This is used FROM the game to the Hero/Crew
        other_damage = attacker.attack(defender)
        if other_damage == 0:
            print(f"{attacker.name} missed.".center(self.__width))
        else:
            print(f"{attacker.name} hit {defender.name} for {other_damage} damage.".center(self.__width))

    def __night_cycle(self):
        # This is the night cycle after the first encounter.
        if self.__is_game_over: return   # If the game is over, return
        self.__clear_screen()            # Clear the screen
        print(self.__moon_map() + '\n')  # Print the moon map
        self.__status()                  # Print the status
        self.__night_story()             # if you have a lost soul in your crew, tell a story
        self.__night_menu()              # Show the night menu, and do night tasks
        self.__sail()                    # Sail
        return
    
    def __night_story(self):
        # If you have a lost soul in your crew, tell a story
        # This will help or hurt your crew

        lost_souls = []
        # If there's lost souls, throw them into a list
        for crew in self.__crew:
            if isinstance(crew, LostSoul):
                lost_souls.append(crew)
        
        # If the list is not empty
        if lost_souls != []:
            # Pick a lost soul at random and have them tell a story
            story_teller = random.choice(lost_souls)
            print(f"{story_teller.name} tells a story.".center(self.__width))
            story = story_teller.tell_story()

            for line in self.__format_text(story, self.__width):
                print(line.center(self.__width))

            # If they're a good story teller, make the crew happy
            if story_teller.is_positive:
                print("The crew is in good spirits.".center(self.__width))
                for crew in self.__crew:
                    crew.alter_happiness(1)
            else:
                # If they're a bad story teller, make the crew sad
                print("This depressed the crew.".center(self.__width))
                for crew in self.__crew:
                    crew.alter_happiness(-1)

            self.__enter_to_continue()
    
    def __format_text(self, text: str, width) -> str:
        # Formats to be no longer than the width.
        # Perfect for the stories told at night.
        words = text.split()
        lines = []
        line = ""
        for word in words:
            if len(line) + len(word) < width:
                line += word + " "
            else:
                lines.append(line)
                line = word + " "
        lines.append(line)
        return lines
    
    def __night_menu(self):
        # At night you can Sail or Anchor.
        # You cannoy sail if you don't have a crew.
        menu = ["Sail", "Anchor", "Quit"]
        choice = ''

        # If you have no crew, remove the sail option
        if self.__crew == []:
            print("You cannot sail at night without a crew.".center(self.__width))
            print("You must anchor for the night.".center(self.__width))
            menu.remove("Sail")

        while choice != "anchor":
            choice = self.__get_input_from_menu(menu, "Good Evening, Captain. What are your orders?")

            # If they want to sail, check if they have a crew
            if choice == "sail":
                self.__sail()
                print("You sail into the night.".center(self.__width))
                self.__enter_to_continue()
                return

            # Anchoring will rotate the watch, you will not sail.
            # If you don't have a crew, you might encounter something.
            if choice == "anchor":
                print("You anchor for the night.".center(self.__width))
                if self.__crew != []:
                    print("The crew rotates watch throughout the night.".center(self.__width))
                    self.__enter_to_continue()
                else:
                    self.__enter_to_continue()
                    self.__encounter()

            if choice == "quit":
                self.__quit_request()
        return
    
    def __end_of_day(self):
        # This just checks if you made it to the moon.
        # If I have time I want it to add stats for the day.
        self.__days_at_sea += 1

        # If enough crew is sad, they will mutiny
        if self.__ship.mutiny(self.__crew):
            self.__dead.insert(self.__hero)
            self.__bad_endings("mutiny")
            return
        
        # If the hero is dead, end the game
        if not self.__hero.is_alive:
            self.__bad_endings("died")
            return


        # If you made it to the moon, end the game
        if self.__traveled_distance >= self.__distance_to_moon:
            self.__win()
            return

    def __game_over(self):
        # If the game is over, prompt the user to play again
        prompting = True 
        while prompting:
            print("Play again? (y/n)".center(self.__width))

            user_input = input(self.__prompt)

            if user_input.lower() == "n" or user_input.lower() == "no":
                prompting = False
                print("The moon claims another soul.".center(self.__width))
                exit()
            elif user_input.lower() == "y" or user_input.lower() == "yes":
                self.__is_game_over = False
                prompting = False
                # If the user wants to play again, reset the game
                # Put all the hero's items in the games inventory
                for items in self.__hero.inventory:
                    self.__new_life_inventory.append(items)
                self.__hero = None
                self.__crew = []
                self.__ship = Ship(rations=100, speed=5) # Force the ship to start with 100 rations and a speed of 5 on subsequent plays
            else:
                print("I do not understand what you want.".center(self.__width))
    
    def __bad_endings(self, ending: str):
        # If the ending is bad, show the bad endings
        self.__is_game_over = True

        if ending == "mutiny":
            self.__clear_screen()
            print(self.__moon_map() + '\n')
            print("The crew has mutinied against you.".center(self.__width))
            print("You are left to die at sea.".center(self.__width))
        
        if ending == "died":
            self.__clear_screen()
            print(self.__moon_map() + '\n')
            print("You have died.".center(self.__width))

        self.__enter_to_continue() 
        self.__bring_out_your_dead() # Make the user feel bad with how many entities died
        return
    
    def __bring_out_your_dead(self):
        # Print the dead from the Tree
        if str(self.__dead) == "Empty Tree":
            print("No lives were lost at sea. A true miracle.".center(self.__width))
            return

        print(f"Souls lost to your cruelty, or recklessness.".center(self.__width))

        # Split the dead into a list instead of a string, with the newline to split on
        the_dead = self.__dead.list_in_order() 
        for dead in the_dead:
            print(dead.center(self.__width))
    
    def __win(self):
        self.__clear_screen()

        print(self.__moon_map() + '\n')         # Print the moon map
        print("You have arrived.".center(self.__width)) # Print the win message
        self.__enter_to_continue()             
        self.__clear_screen()

        print(self.__moon_map() + '\n')         # Print the moon map

        # Load the text for the end of the game.
        self.__text_to_list.load_file("./text_files/text_end_journey.lunasea")
        end_text = self.__text_to_list.data

        # Print each line 1.5 seconds apart.
        # I want to let the user type in between and feel helpless.
        for line in end_text:
            print(line.center(self.__width))
            sleep(1.5)

        print("\n\n\n")
        self.__bring_out_your_dead() # Show them who they are responsible for killing (or not!)
        print()
        print(f"Thanks for playing, {self.__hero.name}.".center(self.__width))
        print("The End".center(self.__width))
        input()
        exit() # Exit the program
    
    def __quit_request(self):
        # Double check since there is no save mechanism 
        print(f"Are you sure you want to quit? There is no coming back. (y/n)".center(self.__width))
        quit_input = input(self.__prompt)
        if quit_input.lower() == "y" or quit_input.lower() == "yes":
            self.__quit()
        return
    
    def __get_input_from_menu(self, menu: list, prompt) -> str:
        # Print the menu and prompt the user for input
        lower_menu = [] # Lowercase menu for input checking

        # Make the menu lowercase for input checking
        for option in menu:
            lower_menu.append(option.lower())

        # This will be the user's input
        user_input = '' 

        while user_input not in lower_menu:
            # Print the prompt and the menu
            print(f"{prompt}".center(self.__width))

            # Format the printed menu in [option] format
            options = "" 
            for option in menu:
                if len(options + f"[{option}] ") > self.__width:
                    options += "\n"
                options += f"[{option}] "

            print(f"{options}".center(self.__width)) # Print it centered

            # Get the user input
            user_input = input(self.__prompt)
            user_input = user_input.lower()

            # Check if the user input is a single character
            # Use the first letter to select the option from the menu
            if len(user_input) == 1:
                for option in lower_menu:
                    if user_input == option[0]:
                        user_input = option

            # If the user input is not in the menu, prompt them again
            if user_input not in lower_menu: 
                print("Captain, you're not making any sense.".center(self.__width))
                user_input = ''
            
            # ELSE the user_input is in the menu and return it.

        return user_input
    
    def __enter_to_continue(self):
        # Prompt the user to press enter to continue
        # used often
        print(f"Press enter to continue".center(self.__width))
        input()
        return

class OpeningSequence():
    # Class that handles the animated ascii opening sequence.
    def __init__(self, width):
        folder = "./text_images/opening_seq"
        self.__sequence = []
        self.__load_sequence(folder, 17)
        self.__width = width
    
    def __load_sequence(self, folder: str, length) -> None:
        # Load the files into a set of images
        for i in range(length):
            file = str(i).zfill(3) # Make index 3 digits long
            file += ".txtimg"
            with open(f"{folder}/{file}", "r") as f:
                ascii_art = "" 
                for line in f:
                    ascii_art += line
                self.__sequence.append(ascii_art)
        return
    
    def __clear_screen(self):
        # Clear the screen
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def play(self) -> None:
        # Play the sequence with a 0.5 second delay between each print
        for frame in self.__sequence:
            self.__clear_screen()
            print(frame) 
            sleep(0.5)
        
        # Prompt the user to press enter to play
        print(f"Press enter to play".center(self.__width))
        input()
        return