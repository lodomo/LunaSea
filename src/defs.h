// ############################################################################
// #
// #    Author:      Lorenzo D. Moon
// #    Description: All #defines and typedefs go here
// #
// ############################################################################

#ifndef DEFS_H
#define DEFS_H

#include "common.h"
#include "game_clock.h"

// Game Resolution. Pixel Perfect scale for 1080p, 720p screens 16:9 screens.
#define INTERNAL_WIDTH 640
#define INTERNAL_HEIGHT 360

#define TRUE 1
#define FALSE 0

#define FPS 60 

typedef struct {
    SDL_Window *window;
    SDL_Renderer *renderer;
    SDL_Event event;
    int width;
    int height;
    int isRunning;
    int isFullscreen;
    Clock clock;                // Defined in game_clock.h
} App;


#endif // DEFS_H
