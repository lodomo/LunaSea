// ############################################################################
// #
// #    Author:      Lorenzo D. Moon
// #    Description:
// #
// ############################################################################

#include <SDL2/SDL.h>
#include <SDL2/SDL_image.h>
#include <stdio.h>

// Define internal resolution (1920 / 3 = 640, 1080 / 3 = 360)
#define INTERNAL_WIDTH 640
#define INTERNAL_HEIGHT 360

#define TRUE 1
#define FALSE 0

typedef struct {
    SDL_Window *window;
    SDL_Renderer *renderer;
    SDL_Texture *texture;
    SDL_Surface *imageSurface;
    SDL_Event event;
} Lunasea;

