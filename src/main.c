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
    initialize();

    while (app.isRunning) {
        clock_update(&app.clock);   // From clock.h
        clock_print(&app.clock);    // From clock.h
        handle_input_events();      // From events.c
        // GAME LOGIC HERE
        screen_clear(app.renderer); // From draw.c
        // DRAW HERE
        screen_update(app.renderer); // From draw.c
    }

    clean_up(); // From init.c
    return EXIT_SUCCESS;
}

void initialize(void) {
    memset(&app, 0, sizeof(App)); // Zero out the App struct
    initApp(&app);                // From init.h
}

void clean_up(void) {
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
