INC=inc
SRC=src
OBJ=obj
PARAM=-Wall -I$(INC)

OBJS=$(OBJ)/ip.o $(OBJ)/main.o $(OBJ)/config.o $(OBJ)/send-recv.o $(OBJ)/bf-errors.o $(OBJ)/std-c.o

all:$(OBJS)
	gcc -o transf $(OBJS) $(PARAM) -lpthread

clean:
	rm -rf $(OBJ)
	mkdir $(OBJ)

$(OBJ)/main.o:$(SRC)/main.c
	gcc -o $(OBJ)/main.o -c $(SRC)/main.c $(PARAM)

$(OBJ)/ip.o:$(SRC)/ip.c
	gcc -o $(OBJ)/ip.o -c $(SRC)/ip.c $(PARAM)

$(OBJ)/config.o:$(SRC)/config.c
	gcc -o $(OBJ)/config.o -c $(SRC)/config.c $(PARAM)

$(OBJ)/send-recv.o:$(SRC)/send-recv.c
	gcc -o $(OBJ)/send-recv.o -c $(SRC)/send-recv.c $(PARAM) -lpthread

$(OBJ)/bf-errors.o:$(SRC)/bf-errors.c
	gcc -o $(OBJ)/bf-errors.o -c $(SRC)/bf-errors.c $(PARAM)

$(OBJ)/std-c.o:$(SRC)/std-c.c
	gcc -o $(OBJ)/std-c.o -c $(SRC)/std-c.c $(PARAM)