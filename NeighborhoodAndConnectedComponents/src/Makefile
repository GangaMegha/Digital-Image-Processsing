# For Linux or any machines with gcc compiler
CC = gcc 
CFLAGS = -std=c99 -Wall -pedantic
BIN = ../bin

all: NeighborhoodsConnectedComponents

clean:
	/bin/rm *.o $(BIN)/*

OBJ = tiff.o allocate.o subroutines.o

NeighborhoodsConnectedComponents: NeighborhoodsConnectedComponents.o $(OBJ) 
	$(CC) $(CFLAGS) -o NeighborhoodsConnectedComponents NeighborhoodsConnectedComponents.o $(OBJ) -lm
	mv NeighborhoodsConnectedComponents $(BIN)
