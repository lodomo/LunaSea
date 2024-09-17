// ############################################################################
// #
// #    Author:      Lorenzo D. Moon
// #    Description:
// #
// ############################################################################

#include "draw.h"

void screen_clear(SDL_Renderer *renderer) {
    SDL_SetRenderDrawColor(renderer, BLACK);
    SDL_RenderClear(renderer);
}

void screen_update(SDL_Renderer *renderer) {
    SDL_RenderPresent(renderer);
}


        /*
        // This next part forces the window to scale and redraw
        // Get the current window size
        SDL_GetWindowSize(app.window, &app.width, &app.height);
        // Render the image stretched to the entire window size
        {
            SDL_Rect dst = {0, 0, app.width,
                            app.height}; // Stretch to window dimensions
            SDL_RenderCopy(app.renderer, texture, NULL, &dst);
        }
        */


