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
    atexit(cleanUp); // Register the cleanup function
    memset(&app, 0, sizeof(App)); // Zero out the App struct
    initApp(); // From init.c
    // while running
    //  Handle Input
    //  Update Game Logic
    //  Render the Frame
    //  Cap the Frame Rate
    //  End Loop
    // Clean up
    SDL_Surface *imageSurface = NULL;
    SDL_Texture *texture = NULL;
    SDL_Event event;
    int running = FALSE;
    int isFullscreen = FALSE; // Variable to track fullscreen state
    int windowWidth, windowHeight;


     // Load the image (replace with your actual image path)
    imageSurface = IMG_Load("./gfx/resolution-test-360.png");
    if (imageSurface == NULL) {
        printf("IMG_Load Error: %s\n", IMG_GetError());
        SDL_DestroyRenderer(renderer);
        SDL_DestroyWindow(window);
        SDL_Quit();
        return 1;
    }

    // Convert the surface to a texture
    texture = SDL_CreateTextureFromSurface(renderer, imageSurface);
    SDL_FreeSurface(imageSurface); // We don't need the surface anymore

    if (texture == NULL) {
        printf("SDL_CreateTextureFromSurface Error: %s\n", SDL_GetError());
        SDL_DestroyRenderer(renderer);
        SDL_DestroyWindow(window);
        SDL_Quit();
        return 1;
    }

    // Main game loop
    running = TRUE;
    while (running) {
        while (SDL_PollEvent(&event)) {
            if (event.type == SDL_QUIT) {
                running = 0;
            } else if (event.type == SDL_KEYDOWN) {
                // Toggle fullscreen mode with F11
                if (event.key.keysym.sym == SDLK_F11) {
                    isFullscreen = !isFullscreen;
                    if (isFullscreen) {
                        SDL_SetWindowFullscreen(window,
                                                SDL_WINDOW_FULLSCREEN_DESKTOP);
                    } else {
                        SDL_SetWindowFullscreen(window,
                                                0); // Back to windowed mode
                    }
                }
            }
        }

        // Get the current window size
        SDL_GetWindowSize(window, &windowWidth, &windowHeight);

        // Clear the screen
        SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255);
        SDL_RenderClear(renderer);

        // Render the image stretched to the entire window size
        {
            SDL_Rect dst = {0, 0, windowWidth,
                            windowHeight}; // Stretch to window dimensions
            SDL_RenderCopy(renderer, texture, NULL, &dst);
        }

        // Present the rendered image
        SDL_RenderPresent(renderer);
    }

    return EXIT_SUCCESS;
}

void cleanUp() {
    initCleanUp(); // From init.c
}
