#include "ip.h"

void ip2charptr(IP *ip,char *st){
	memset(st,0,sizeof(char)*IP_LEN);
	sprintf(st,"%d.%d.%d.%d",ip->a,ip->b,ip->c,ip->d);
}

void charptr2ip(IP *ip, char *st){
	int a,b,c,d;
	sscanf(st,"%d.%d.%d.%d",&a,&b,&c,&d);	
	if (a > 255 || b > 255 || c > 255 || d > 255){
		fprintf(stderr,"IP incorreto %d.%d.%d.%d",a,b,c,d);
		exit(-1);
	}
	ip->a = a; ip->c = c;
	ip->b = b; ip->d = d;
}
