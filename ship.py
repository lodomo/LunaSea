################################################################################
# 
#     Author:      Lorenzo D. Moon
#     Instructor:  Karla Fant
#     Course:      CS-302
#     Assignment:  Program 4/5
#     Description: 
#
################################################################################

from tree import Tree
from entity import Crewmate
import random

class Ship:
    def __init__(self, rations: int, speed: int):
        self.__rations = rations # Rations for the crew
        self.__speed = speed     # Speed of the ship
    
    def gain_rations(self, rations: int) -> None:
        # Gain rations
        # This is used when the crew finds rations. For now it's when
        # they butcher a monster after killing it.

        self.__rations += rations
        return
    
    def feed_crew(self, crew: Crewmate) -> None:
        # Feed the crew
        # When the crew is fed, they use rations. If there are not enough
        # rations, they will starve. If they starve, they lose happiness

        spent_rations = 0
        for member in crew:
            if not member.is_alive: continue

            feed_amount = member.ration_use
            if self.__rations < feed_amount:
                member.feed(self.__rations)
                spent_rations += self.__rations
                self.__rations = 0
            else:
                member.feed(feed_amount)
                spent_rations += feed_amount
                self.__rations -= feed_amount
            
            if self.__rations <= 0:
                self.__rations == 0
        return spent_rations
    
    def starve_crew(self, crew: Crewmate) -> None:
        # If you don't feed your crew, they all lose some happiness
        for member in crew:
            if not member.is_alive(): continue
            member.feed(0)
    
    def mutiny(self, crew) -> bool:
        # If the crew is unhappy, they will mutiny
        # If more than half the crew want to mutiny, return True
        alive_crew = 0
        mutiny_count = 0 
        for member in crew:
            if not member.is_alive: continue

            alive_crew += 1

            if member.mutiny_check():
                mutiny_count += 1
        
        # If more than half the crew want to mutiny, return True
        if mutiny_count > (alive_crew // 2):
            for member in crew:
                return True
        return False
    
    def daily_rations(self, crew) -> int:
        # Calculate the daily rations used by the crew
        rations_per_day = 0
        for member in crew:
            if not member.is_alive: continue
            rations_per_day += member.ration_use
        return rations_per_day
    
    def days_left(self, crew) -> int:
        # Calculate the days left of rations
        if self.daily_rations(crew) == 0:
            return self.__rations 

        return self.__rations // self.daily_rations(crew)
    
    def rations(self) -> int:
        # Return the rations
        return self.__rations
    
    def distance_sailed(self) -> int:
        # The ship will go a random distance between 1 and the speed
        distance = random.randint(1, self.__speed + 1)
        return distance 