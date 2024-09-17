// ############################################################################
// #
// #    Author:      Lorenzo D. Moon
// #    Description:
// #
// ############################################################################

#include "clock.h"

void clock_init(Clock *clock) {
    if (clock == NULL) {
        printf("Clock struct is NULL\n");
        exit(ERR_NULL_CLOCK);
    }

    clock->previous_time = SDL_GetTicks64();
    clock->current_time = SDL_GetTicks64();
    clock->delta_time = 0.0;
    clock->frame_count = 0;
}

void clock_update(Clock *clock) {
    if (clock == NULL) {
        printf("Clock struct is NULL\n");
        exit(ERR_NULL_CLOCK);
    }
    clock->previous_time = clock->current_time;
    clock->current_time = SDL_GetTicks64();
    clock->delta_time = (clock->current_time - clock->previous_time) / MS_PER_SEC;
    clock->frame_count = (clock->frame_count + 1) % MAX_FRAME_COUNT;
}

void clock_print(Clock *clock) {
    if (clock == NULL) {
        printf("Clock struct is NULL\n");
        exit(ERR_NULL_CLOCK);
    }
    printf("Previous Time: %lu\n", clock->previous_time);
    printf("Current Time: %lu\n", clock->current_time);
    printf("Delta Time: %f\n", clock->delta_time);
    printf("Frame Count: %lu\n", clock->frame_count);
}
