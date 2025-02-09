################################################################################
# 
#     Author:      Lorenzo D. Moon
#     Instructor:  Karla Fant
#     Course:      CS-302
#     Assignment:  Program 4/5
#     Description: The moon has fallen into the sea, and strange monsters have 
#                  taken over the world’s oceans. Countless adventurers took to 
#                  their boats and aim to be first to conquer this new land. 
#                  Will you be first to conquer the moon, or will you succumb to
#                                              LunaSea
#
################################################################################

from lunasea import LunaSea

def main():
    game = LunaSea() # Create/Load the game
    game.play()      # Play the game

if __name__ == "__main__":
    main()