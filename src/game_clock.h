// ############################################################################
// #
// #    Author:      Lorenzo D. Moon
// #    Description:
// #
// ############################################################################

#ifndef GAME_CLOCK_H
#define GAME_CLOCK_H

#define uSEC_PER_SECOND 1000000.0
#define FRAME_COUNT_MAX 60

#include <sys/time.h>        // For gettimeofday and timeval
#include <unistd.h>          // Unix standard library for usleep
#include <stdint.h>          // Standard integer types for uint64_t
#include <stdio.h>           // Standard I/O for printf
#include <stdlib.h>          // Standard library for calloc
#include "errorcodes.h"      // Error codes for the program

typedef struct {
    struct timeval init_time;
    struct timeval render_end;
    struct timeval render_start;
    struct timeval sleep_tracker;
    uint64_t sleep_time;        // in microseconds
    uint64_t elapsed_time;      // in microseconds
    uint64_t render_time;       // in microseconds
    double delta_time;          // in seconds 
    int target_fps;
    float actual_fps;
    int frame_count;
    uint64_t frames_per_usec; 
} Clock;


uint64_t get_elapsed_usec(struct timeval *t0, struct timeval *t1);

int clock_init(Clock * clock, int fps);
int clock_update(Clock * clock);
int clock_cap_frames(Clock * clock);
int clock_tick(Clock * clock);

#endif // GAME_CLOCK_H
