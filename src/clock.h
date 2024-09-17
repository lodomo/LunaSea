// ############################################################################
// #
// #    Author:      Lorenzo D. Moon
// #    Description:
// #
// ############################################################################

#ifndef CLOCK_H
#define CLOCK_H

#define MS_PER_SEC 1000.0f
#define MAX_FRAME_COUNT 60

#include <stdint.h>     // uint64_t (Standard Integer Types)
#include <SDL2/SDL.h>   // SDL_GetTicks

#include "errorcodes.h" // Error codes for the program

typedef struct {
    uint64_t previous_time;
    uint64_t current_time;
    double delta_time;
    uint64_t frame_count; // No need to count more than 60 fps for any logic
} Clock;

void clock_init(Clock *clock);
void clock_update(Clock *clock);
void clock_print(Clock *clock);

#endif // CLOCK_H
