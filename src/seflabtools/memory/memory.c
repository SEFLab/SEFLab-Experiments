/*
SEFLab Tools is a software package that provides tools for running experiments in the SEFLab
as well as for analyzing the resulting data.

Copyright (C) 2013  Software Improvement Group

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <math.h>
#include <time.h>

#define ONE_ZERO 125
#define ZERO_ONE 252

void usage(char* cmd);
int checkArguments(int argc, char **argv);
void writeBits(volatile int* array, int arrayLength, int bit);
void printArray(volatile int* array, int arrayLength);

void usage(char *cmd) {
	printf("Usage: %s <GB of memory to allocate> <run duration (s)>\n", cmd);
}

int checkArguments(int argc, char **argv) {
	if(argc != 3) {
		printf("ERROR: Program expects 2 arguments\n");
		usage(argv[0]);
		
		return 1;
	}
	
	return 0;
}

void writeBits(volatile int *array, int arrayLength, int bits) {
	int i;
	for(i = 0; i < arrayLength; i++) {
		array[i] = bits;
	}
}

void printArray(volatile int *array, int arrayLength) {
	int i;
	for(i = 0; i < arrayLength; i++) {
		printf("%d", array[i]);
	}
	printf("\n");
}

int main(int argc, char **argv) {	
	if(checkArguments(argc, argv) == 1) {
		exit(1);
	}

	long unsigned intSize = sizeof(int);
	int gbsToAllocate = atoi(argv[1]);
	long duration = atol(argv[2]);
	
	time_t startTime = time(NULL);
	int gbFactor = (int) pow((double)1024,3);
	int arrayLength =  (gbFactor / intSize) * gbsToAllocate;
	volatile int* array = malloc(sizeof(int) * arrayLength);
	
	while(startTime + duration > time(NULL)) {
		writeBits(array, arrayLength, ZERO_ONE);
		writeBits(array, arrayLength, ONE_ZERO);
	}
	
	return 0;
}