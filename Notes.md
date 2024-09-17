// Render the image stretched to the entire window size
        {
            SDL_Rect dst = {0, 0, app.width,
                            app.height}; // Stretch to window dimensions
            SDL_RenderCopy(app.renderer, texture, NULL, &dst);
        }
