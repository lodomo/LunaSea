################################################################################
# 
#     Author:      Lorenzo D. Moon
#     Instructor:  Karla Fant
#     Course:      CS-302
#     Assignment:  Program 4/5
#     Description: Item class to use in the game. Each item has a name, can be
#                  equipped, can be used, and has a number of uses. The item also
#                  has a strength, defense, hp, and levels attribute. 
#                  Takes in a dictionary of information to create the item.
#                  Data will be loaded from file using "text_to_dict" class, and
#                  then passed to the Item class to create.
#
################################################################################

class Item:
    def __init__(self, data):
        self.__name = data["name"]
        self.__can_equip = data["can_equip"] 
        self.__can_use = data["can_use"] 
        self.__uses = data["uses"]
        self.__strength = data["strength"] 
        self.__defense = data["defense"] 
        self.__hp = data["hp"] 
        self.__levels = data["levels"] 
    
    def __str__(self):
        return self.__name
    
    def __repr__(self):
        return str(self) 
    
    @property
    def can_equip(self):
        return self.__can_equip
    
    @property
    def empty(self):
        # Return true if the item has no more uses
        return self.__uses == 0

    @property
    def name(self):
        return self.__name 

    def stats(self, negative=False):
        # Return the stats of the item
        # If negative is true, return the negative of the stats
        # This is used when unequipping an item
        if negative:
            return [-self.__strength, -self.__defense, -self.__hp, -self.__levels]
        return [self.__strength, self.__defense, self.__hp, self.__levels] 

    def use(self):
        # Use the item
        
        # This error should only be seen if the game client doesn't properly
        # handle inventory
        if self.empty and self.__can_use:
            raise ValueError("Item is empty")

        # If the item can be used, decrement the uses
        if self.__uses > 0:
            self.__uses -= 1
        
        # Return the stats of the item
        return self.stats() 
    
    def equip(self):
        # Equip the item

        # This error should only be seen if the game client doesn't properly
        # handle equipping items
        if not self.__can_equip:
            raise ValueError("Item cannot be equipped")
        
        # Return the stats of the item
        return self.stats() 
    
    def unequip(self):
        # Unequip the item

        # This error should only be seen if the game client doesn't properly
        # handle unequipping items
        if not self.__can_equip:
            raise ValueError("Item cannot be equipped")

        # Return the negative of the stats of the item 
        return self.stats(negative=True) 