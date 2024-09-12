// ############################################################################
// #
// #    Author:      Lorenzo D. Moon
// #    Description:
// #
// ############################################################################

#ifndef INIT_H
#define INIT_H

#include "common.h"
#include "defs.h"

extern App app;

void initSDL();                                     // Initialize SDL for video
void initIMG();                                     // Initialize SDL_Image for image loading
SDL_Window * createWindow();                        // Create the window for the game
SDL_Renderer * createRenderer(SDL_Window * window); // Create the renderer for the game

void initApp();                                     // Initialize the App struct
void initCleanUp();                                 // Clean up SDL and SDL_Image

#endif // INIT_H
