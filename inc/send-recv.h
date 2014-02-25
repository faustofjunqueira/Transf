#ifndef SEND_RECV_H
#define SEND_RECV_H


#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <netdb.h>
#include <ifaddrs.h>

#include <pthread.h>

#include "ip.h"
#include "struct.h"
#include "bf-errors.h"

void startSockets();
void sendMsg(MSG *msg);
void *recv_thread(void *arg);
void treatMsg(MSG msg);

#endif