#include "std-c.h"
#include "struct.h"
#include "config.h"
#include "send-recv.h"



void printMan(){
	printf("Faça:\n");
	printf("\t ./transf -s0 se for portador do arquivo\n");
	printf("\tou\n");
	printf("\t./transf se for receptor\n");
	exit(-1);
}

int main(int argc, char const *argv[])
{
	
	if(argc > 2){
		printf("Parametros incorretos\n");
		printMan();		
	}
	if(!strcmp(argv[1],"-s0"))
		flag = SERVIDOR;		
	else if(!strcmp(argv[1],"--help"))
		printMan();
	else if(argc == 1)
		flag = CLIENTE;
	else{
		printf("Parametros incorretos\n");
		printMan();
	}
	
	loadConfig();
	startSockets();
//	configAllMachine();
//	startTransf();
	MSG msg = {0,1};
	AllMachine[0] = (NODE) {{127,0,0,1},10};
	
	while(1){
		int a;
		printf("Put :");
		scanf("%d",&a);
		msg.msg = a;
		sendMsg(&msg);
	}

	bf_elog(ERROR,"Operação terminada!");
	pthread_exit(NULL);	
	return 0;

}