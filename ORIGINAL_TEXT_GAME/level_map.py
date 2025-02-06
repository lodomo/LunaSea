################################################################################
# 
#     Author:      Lorenzo D. Moon
#     Instructor:  Karla Fant
#     Course:      CS-302
#     Assignment:  Program 4/5
#     Description: Level map for the hero. I chose to use a class to represent the
#                  level map because it will just bloat the hero class.
#                  If I had time I would make it load from file.
#
################################################################################

class LevelMap():
    def __init__(self):
        # Format: LEVEL NUMBER: [EXP NEEDED, HP UP, STRENGTH UP, DEFENSE UP]

        # This is good enough for now.
        # I'd like to make this better if I make this a full game
        self.__levels = {
            1: [0, 1, 1, 1],
            2: [10, 1, 1, 1],
            3: [20, 1, 1, 1],
            4: [30, 1, 1, 1],
            5: [40, 1, 1, 1],
            6: [50, 2, 2, 2],
            7: [60, 2, 2, 2],
            8: [70, 2, 2, 2],
            9: [80, 2, 2, 2],
            10: [90, 2, 2, 2],
            11: [100, 3, 3, 3]
        }
    
    def get_map(self):
        # Return the level map.
        return self.__levels