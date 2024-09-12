// ############################################################################
// #
// #    Author:      Lorenzo D. Moon
// #    Description:
// #
// ############################################################################

#include "events.h"

// This needs to be prettier and more robust
// but this works for a placeholder for now
void handleEvents(void) {
    while (SDL_PollEvent(&app.event)) {
        if (app.event.type == SDL_QUIT) {
            app.isRunning = 0;
        } else if (app.event.type == SDL_KEYDOWN) {
            // Toggle fullscreen mode with F11
            if (app.event.key.keysym.sym == SDLK_F11) {
                app.isFullscreen = !app.isFullscreen;
                if (app.isFullscreen) {
                    SDL_SetWindowFullscreen(app.window,
                                            SDL_WINDOW_FULLSCREEN_DESKTOP);
                } else {
                    SDL_SetWindowFullscreen(app.window,
                                            0); // Back to windowed mode
                }
            }

            if (app.event.type == SDL_KEYDOWN &&
                app.event.key.keysym.sym == SDLK_q) {
                app.isRunning = FALSE;
            }
        }
    }
}
