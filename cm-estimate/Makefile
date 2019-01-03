CFLAGS = -O
CC = gcc
LIBS = -lm -lgsl -lgslcblas

estimate:estimate.o readgml.o
	$(CC) $(CFLAGS) -o bin/estimate bin/estimate.o bin/readgml.o $(LIBS)

estimate.o:estimate.c network.h readgml.h Makefile
	$(CC) $(CFLAGS) -c estimate.c -o bin/estimate.o

readgml.o:readgml.c readgml.h network.h
	$(CC) $(CFLAGS) -c readgml.c -o bin/readgml.o
