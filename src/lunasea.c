// ############################################################################
// #
// #    Author:      Lorenzo D. Moon
// #    Description:
// #
// ############################################################################



#include "lunasea.h"

int main(int argc, char* argv[]) {
    SDL_Window* window = NULL;
    SDL_Renderer* renderer = NULL;
    SDL_Surface* imageSurface = NULL;
    SDL_Texture* texture = NULL;
    SDL_Event event;
    int running = FALSE;

    if (SDL_Init(SDL_INIT_VIDEO) != 0) {
        printf("SDL_Init Error: %s\n", SDL_GetError());
        return 1;
    }

    // Initialize SDL2_image for loading images
    if (!(IMG_Init(IMG_INIT_PNG) & IMG_INIT_PNG)) {
        printf("IMG_Init Error: %s\n", IMG_GetError());
        SDL_Quit();
        return 1;
    }

    // Create a window in windowed mode
    window = SDL_CreateWindow("Resolution Test",
                                      SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED,
                                      INTERNAL_WIDTH, INTERNAL_HEIGHT,
                                      SDL_WINDOW_FULLSCREEN_DESKTOP);
    if (window == NULL) {
        printf("SDL_CreateWindow Error: %s\n", SDL_GetError());
        SDL_Quit();
        return 1;
    }


    // Create a renderer
    renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);

    SDL_RenderSetLogicalSize(renderer, INTERNAL_WIDTH, INTERNAL_HEIGHT);

    if (renderer == NULL) {
        printf("SDL_CreateRenderer Error: %s\n", SDL_GetError());
        SDL_DestroyWindow(window);
        SDL_Quit();
        return 1;
    }

    // Load the image (replace with your actual image path)
    imageSurface = IMG_Load("./sprites/resolution-test-360.png");
    if (imageSurface == NULL) {
        printf("IMG_Load Error: %s\n", IMG_GetError());
        SDL_DestroyRenderer(renderer);
        SDL_DestroyWindow(window);
        SDL_Quit();
        return 1;
    }

    // Convert the surface to a texture
    texture = SDL_CreateTextureFromSurface(renderer, imageSurface);
    SDL_FreeSurface(imageSurface);  // We don't need the surface anymore

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
            }
        }

        // Clear the screen
        SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255);
        SDL_RenderClear(renderer);

        // Render the image
        {
        SDL_Rect dst = { 0, 0, INTERNAL_WIDTH, INTERNAL_HEIGHT }; // Adjust the position and size
        SDL_RenderCopy(renderer, texture, NULL, &dst);
        }

        // Present the rendered image
        SDL_RenderPresent(renderer);
    }

    // Clean up
    SDL_DestroyTexture(texture);
    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    IMG_Quit();
    SDL_Quit();

    return 0;
}

