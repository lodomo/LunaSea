// ############################################################################
// #
// #    Author:      Lorenzo D. Moon
// #    Description:
// #
// ############################################################################

#include "init.h"

void initSDL(void) {
    // Initialize SDL2
    if (SDL_Init(SDL_INIT_VIDEO) != 0) {
        // If initialization fails, print an error message
        printf("SDL_Init Error: %s\n", SDL_GetError());
        exit(ERR_SDL_INIT);
    }
}

void initIMG(void) {
    // Initialize SDL2_image for loading images
    if (!(IMG_Init(IMG_INIT_PNG) & IMG_INIT_PNG)) {
        printf("IMG_Init Error: %s\n", IMG_GetError());
        SDL_Quit();
        exit(ERR_IMG_INIT);
    }
}

SDL_Window * createWindow(void) {
    // Create a resizable window (not fullscreen initially)
    SDL_Window * window = SDL_CreateWindow("Resolution Test", SDL_WINDOWPOS_CENTERED,
                                          SDL_WINDOWPOS_CENTERED, INTERNAL_WIDTH,
                                          INTERNAL_HEIGHT, SDL_WINDOW_RESIZABLE);
    if (window == NULL) {
        printf("SDL_CreateWindow Error: %s\n", SDL_GetError());
        SDL_Quit();
        exit(ERR_WINDOW_CREATE);
    }

    return window;
}

SDL_Renderer * createRenderer(SDL_Window * window) {
    // Create a renderer
    SDL_Renderer * renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);
    if (renderer == NULL) {
        printf("SDL_CreateRenderer Error: %s\n", SDL_GetError());
        SDL_DestroyWindow(window);
        SDL_Quit();
        exit(ERR_RENDERER_CREATE);
    }

    return renderer;
}

void initApp(void) {
    // Initialize the App struct
    app.window = createWindow();
    app.renderer = createRenderer(app.window);

    app.isRunning = TRUE;
    app.isFullscreen = FALSE;
}
