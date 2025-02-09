################################################################################
# 
#     Author:      Lorenzo D. Moon
#     Description: Modified from a script I made a few years ago for a game
#                  called "Peasants in a Dungeon". This works much better than
#                  the original.
#
#                  This script is not ran during the game, but was used to 
#                  generate the ascii images that are used in the game intro.
#                  
#                  I also intended on using it to create character portraits
#                  and backgrounds, but couldn't get the formatting right
#                  in time.
#
################################################################################

from PIL import Image

class ImageGenerator:
    def __init__(self):
        self.__ascii_img = []
        self.__80 = '██' # ██ 80-100 White
        self.__60 = '▓▓' # ▓▓ 60-80
        self.__40 = '▒▒' # ▒▒ 40-60
        self.__20 = '░░' # ░░ 20-40
        self.__00 = '  ' #    0-20%

    def __grey_percentage(self, rgb_value):
        # It's been a long time since I wrote this function.
        # I think I found the formula on LOSPEC? Basically this turns
        # Any color into "How much grey is it" and sets the pixel to that.
        red = rgb_value[0]
        green = rgb_value[1]
        blue = rgb_value[2]
        grey = (0.3 * red) + (0.59 * green) + (0.11 * blue)
        return grey

    def render(self, img_path: str):
        # Check to make sure the file exists
        try:
            img = Image.open(img_path)
        except FileNotFoundError:
            print("File {img_path} not found.")
            return

        # Load the image and get the pixels
        pixels = img.load()
        self.__ascii_img = [] # This is what actually gets printed to screen

        # Loop through the image and convert the pixels to ascii
        for y in range(img.height):
            row = ''
            for x in range(img.width):
                grey_scale = self.__grey_percentage(pixels[x, y])
                if grey_scale > 204:
                    row += '██'
                elif grey_scale > 153:
                    row += '▓▓'
                elif grey_scale > 102:
                    row += '▒▒'
                elif grey_scale > 51:
                    row += '░░'
                else:
                    row += '  '
            self.__ascii_img.append(row) 
    
    def save(self, file_name: str):
        # Save the ascii image to a file
        with open(file_name, 'w') as file:
            for row in self.__ascii_img:
                file.write(row)
                file.write('\n')
        return

def main():
    img = ImageGenerator()
    folder = "./"
    folder += input("Enter the folder name: ")
    folder += "/"
    images = int(input("How many images?:"))

    for i in range(images):
        # Make i 3 digits long
        img_path = folder + f"{str(i).zfill(3)}.png"
        img.render(img_path)
        img.save(folder + f"{str(i).zfill(3)}.txtimg")


if __name__ == "__main__":
    main()