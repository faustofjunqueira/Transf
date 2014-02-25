#ifndef IP_H
#define IP_H

#include "std-c.h"
#include "struct.h"

#define IP_LEN 16

void charptr2ip(IP *ip, char *st);
void ip2charptr(IP *ip,char *st);

#endif