# For Linux or any machines with gcc compiler
CC = gcc 
CFLAGS = -std=c99 -Wall -pedantic
BIN = ../bin

all: FilterImage

clean:
	/bin/rm *.o $(BIN)/*

OBJ = tiff.o allocate.o filters.o

FilterImage: FilterImage.o $(OBJ) 
	$(CC) $(CFLAGS) -o FilterImage FilterImage.o $(OBJ) -lm
	mv FilterImage $(BIN)

