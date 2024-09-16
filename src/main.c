// ############################################################################
// #
// #    Author:      Lorenzo D. Moon
// #    Description:
// #
// ############################################################################

#include "main.h"

// Globals
App app;

int main(int argc, char *argv[]) {
    int color = 0;
    initialize();

    // while running
    //  Handle Events Input
    //  Update Game Logic
    //  Render the Frame
    //  Cap the Frame Rate
    //  End Loop
    // Clean up

    // Main game loop
    while (app.isRunning) {
        // Handle events (input)
        handleEvents(); // From events.c
        
        // This next part forces the window to scale and redraw
        // Get the current window size
        SDL_GetWindowSize(app.window, &app.width, &app.height);

        // Clear the screen
        color = (color + 1) % 255;
        SDL_SetRenderDrawColor(app.renderer, color, color, color, 255);
        SDL_RenderClear(app.renderer);

        // Render the image stretched to the entire window size
        {
            //SDL_Rect dst = {0, 0, app.width,
            //                app.height}; // Stretch to window dimensions
            //SDL_RenderCopy(app.renderer, texture, NULL, &dst);
        }

        // Present the rendered image
        SDL_RenderPresent(app.renderer);

        // Update the game clock
        clock_tick(&app.clock); // From game_clock.h
    }

    cleanUp(); // From init.c
    return EXIT_SUCCESS;
}

void initialize(void){
    memset(&app, 0, sizeof(App)); // Zero out the App struct
    initApp(&app);                // From init.h
    clock_init(&app.clock, FPS);        // From game_clock.h, init the game clock
}

void cleanUp(void) {
    // Clean up SDL2
    if (app.renderer != NULL) {
        SDL_DestroyRenderer(app.renderer);
        app.renderer = NULL;
    }

    if (app.window != NULL) {
        SDL_DestroyWindow(app.window);
        app.window = NULL;
    }

    IMG_Quit();
    SDL_Quit();
}
