#ifndef STRUCT_H
#define STRUCT_H

typedef struct{
	unsigned short a,b,c,d;
}IP;

typedef struct{
	IP ip;
	unsigned short id;
}NODE;

enum MSG_TYPE_ENUM{
	CHECK = 1,
	REPLY
};

typedef enum MSG_TYPE_ENUM MSG_TYPE;

typedef struct{
	unsigned short id;
	MSG_TYPE msg;
}MSG;


extern IP bcast;
extern unsigned short PORT;
extern NODE MyMachine;
extern NODE AllMachine[255];
extern char flag;
extern MSG Recv_msg;
extern int SocketFd;
#endif