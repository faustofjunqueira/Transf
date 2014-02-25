#ifndef STD_C_H
#define STD_C_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <stdarg.h>

char *bf_now();
void bf_exit(int code);
FILE *bf_fopen(char *filename, char *type);

#endif
