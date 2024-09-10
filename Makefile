###############################################################################
#
# Author: Lorenzo Moon    
# Project: Lunasea
# Description: 
# Targets: all (default)
#            $(PROGRAM)      : compile the program
#            $(PROGRAM).o    : compile the object file
#            clean           : remove all generated files
#            tar             : create a tarball of the files
#            git             : add, commit, and push to git
#            debug           : compile with debug flags
#            memcheck        : run valgrind on the program
#
###############################################################################

# Directories
SRC_DIR = src
OBJ_DIR = obj

# Source files
CSRCS = $(wildcard $(SRC_DIR)/*.c)
HSRCS = $(wildcard $(SRC_DIR)/*.h)
OBJS = $(patsubst $(SRC_DIR)/%.c, $(OBJ_DIR)/%.o, $(CSRCS))

# Flags
CFLAGS = -Wall -Wextra -Wshadow -Wunreachable-code \
         -Wredundant-decls -Wmissing-declarations \
         -Wold-style-definition -Wmissing-prototypes \
         -Wdeclaration-after-statement -Wno-return-local-addr \
         -Wunsafe-loop-optimizations -Wuninitialized -Werror \
         -Wno-unused-parameter -Wno-string-compare -Wno-stringop-overflow \
         -Wno-stringop-overread -Wno-stringop-truncation \
         `sdl2-config --cflags`  # Correctly use SDL2 flags
LIBS = `sdl2-config --libs` -lSDL2_image  # Correctly link SDL2 libraries
DFLAGS = -g -DNOISY_DEBUG

PROGRAM = lunasea
CC = gcc
TAR_FILE = ${PROGRAM}.tar.gz

all: $(PROGRAM)

.PHONY: clean tar git debug memcheck

# Rule to build object files from .c files
# -c can use automatic variables with automatic rename from .c to .o
$(OBJ_DIR)/%.o: $(SRC_DIR)/%.c
	$(CC) $(CFLAGS) -c $< -o $@

$(PROGRAM): $(OBJS)
	$(CC) $(CFLAGS) -o $(@) $(OBJS) $(LIBS)

clean:
	rm -f $(PROGRAM) $(OBJS) *~ \#*
	rm -f *.output *.error

tar:
	tar -cvaf ${TAR_FILE} *.c [Mm]akefile

git:
	git add . 
	git commit -m "Lazy commit via Make"
	git push

debug: $(CSRCS)
	$(CC) $(CFLAGS) $(DFLAGS) -o $(PROGRAM) $(CSRCS) $(LIBS)

memcheck: $(PROGRAM)
	valgrind --track-origins=yes --leak-check=full ./$(PROGRAM)
