// ############################################################################
// #
// #    Author:      Lorenzo D. Moon
// #    Description:
// #
// ############################################################################

#include "game_clock.h"

uint64_t get_elapsed_usec(struct timeval *t0, struct timeval *t1) {
    // Time in microseconds between two timevals.
    // Timeval has two members: tv_sec and tv_usec, seconds and microseconds.
    uint64_t elapsed_usec = 0;
    elapsed_usec = (t1->tv_sec) * uSEC_PER_SECOND + t1->tv_usec;
    elapsed_usec -= (t0->tv_sec) * uSEC_PER_SECOND + t0->tv_usec;
    return elapsed_usec;
}

int clock_init(Clock *clock, int fps) {
    if (clock == NULL) {
        return ERR_NULL_CLOCK;
    }

    // Initialize the clock
    clock->render_time = 0;
    clock->elapsed_time = 0;
    clock->target_fps = fps;

    if (clock->target_fps == 0) {
        clock->frames_per_usec = 0;
    } else {
        clock->frames_per_usec = uSEC_PER_SECOND / clock->target_fps;
    }

    // Get the current time for the clock
    gettimeofday(&clock->init_time, NULL);
    gettimeofday(&clock->render_end, NULL);
    gettimeofday(&clock->render_start, NULL);

    return 0;
}

int clock_update(Clock *clock) {
    if (clock == NULL) {
        return ERR_NULL_CLOCK;
    }

    gettimeofday(&clock->render_end, NULL); // Get the current time

    printf("Previous time: %lu.%lu\n", clock->render_start.tv_sec,
           clock->render_start.tv_usec);
    printf("Current time : %lu.%lu\n", clock->render_end.tv_sec,
           clock->render_end.tv_usec);

    // Calculate the elapsed time
    // This might get dropped if it isn't useful.
    clock->elapsed_time = get_elapsed_usec(&clock->init_time, &clock->render_end);

    // Calculate the delta time
    clock->render_time = get_elapsed_usec(&clock->render_start, &clock->render_end);
    printf("Render time: %lu\n", clock->render_time);

    if (clock->target_fps > 0) {
        clock->frame_count = (clock->frame_count + 1) % clock->target_fps;
    }
    else
    {
        // This is for fixed updates when there is no frame rate cap.
        // This is for things that require a bit more calculation that
        // shouldn't happen every single frame.
        clock->frame_count = (clock->frame_count + 1) % FRAME_COUNT_MAX;

        // Convert render time to seconds
        clock->delta_time = (double)clock->render_time / uSEC_PER_SECOND;
    }
    printf("Frame count: %d\n", clock->frame_count);

    return 0;
}

int clock_cap_frames(Clock *clock) {
    if (clock == NULL) {
        return ERR_NULL_CLOCK;
    }
    
    // Cap the frame rate
    gettimeofday(&clock->sleep_tracker, NULL);
    clock->sleep_time = get_elapsed_usec(&clock->render_start, &clock->sleep_tracker);
    while (clock->sleep_time < clock->frames_per_usec) {
        usleep(1);
        gettimeofday(&clock->sleep_tracker, NULL);
        clock->sleep_time = get_elapsed_usec(&clock->render_start, &clock->sleep_tracker);
    }

    clock->delta_time = (double) get_elapsed_usec(&clock->render_start, &clock->sleep_tracker) / uSEC_PER_SECOND;

    printf("Delta time: %f\n", clock->delta_time);
    printf("Actual FPS: %f\n", 1.0 / clock->delta_time);

    return 0;
}

int clock_tick(Clock *clock) {
    if (clock == NULL) {
        return ERR_NULL_CLOCK;
    }

    // Update the clock
    clock_update(clock);

    // Cap the frame rate
    if (clock->target_fps > 0) {
        clock_cap_frames(clock);
    }

    // Update the render start time
    gettimeofday(&clock->render_start, NULL);
    return 0;
}
