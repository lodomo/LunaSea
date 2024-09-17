// ############################################################################
// #
// #    Author:      Lorenzo D. Moon
// #    Description:
// #
// ############################################################################

#ifndef MAIN_H
#define MAIN_H

#include "defs.h"
#include "errorcodes.h" // Error codes for the program
#include "events.h"
#include "init.h"
#include "clock.h"
#include "draw.h"

int main(int argc, char *argv[]);
void initialize(void);
void clean_up(void);

#endif // MAIN_H
