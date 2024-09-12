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

void initSDL(void);                                     // Initialize SDL for video
void initIMG(void);                                     // Initialize SDL_Image for image loading
SDL_Window * createWindow(void);                        // Create the window for the game
SDL_Renderer * createRenderer(SDL_Window * window); // Create the renderer for the game

void initApp(void);                                     // Initialize the App struct

#endif // INIT_H
