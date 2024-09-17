// ############################################################################
// #
// #    Author:      Lorenzo D. Moon
// #    Description:
// #
// ############################################################################

#ifndef DRAW_H
#define DRAW_H

#include <SDL2/SDL.h>

#define BLACK 0, 0, 0, 255

void screen_clear(SDL_Renderer *renderer);
void screen_update(SDL_Renderer *renderer); 

#endif // DRAW_H
