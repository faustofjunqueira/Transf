#include "config.h"

IP bcast;
NODE MyMachine;
NODE AllMachine[255];
char flag;
unsigned short PORT;

void loadConfig(void){
	char ip_char[IP_LEN];
	IP ip_tmp;
	int opcao;
	printf("Insira o IP(nao usar espaço): ");
	if(scanf("%s",ip_char) != 1){
		bf_elog(ERROR,"Não foi possivel ler o bcast\n");
	}
	charptr2ip(&MyMachine.ip,ip_char);
	ip_tmp = MyMachine.ip;
	printf("Escolha seu broadcast:\n");	
	ip_tmp.d = 255;
	ip_tmp.c = 0;	
	ip2charptr(&ip_tmp,ip_char);
	printf("\t[1] %s\n", ip_char);
	ip_tmp.d = 255;
	ip_tmp.c = 1;	
	ip2charptr(&ip_tmp,ip_char);
	printf("\t[2] %s\n", ip_char);
	printf("\t[3] Outro\n>");
	if(scanf("%d",&opcao) != 1)
		bf_elog(ERROR,"Não foi possivel ler a opção desejada\n");

	switch(opcao){
		case 1:
			ip_tmp.c = 0;
			bcast = ip_tmp;
			break;
		case 2:
			bcast = ip_tmp;
			break;
		case 3:
			printf("Insira o Broadcast(nao usar espaço): ");
			if(scanf("%s",ip_char) != 1){
				bf_elog(ERROR,"Não foi possivel ler o bcast\n");
			}
			charptr2ip(&bcast,ip_char);
			break;
		default: bf_elog(ERROR,"Opção inexistente\n");
	}

	MyMachine.id = 0;

	printf("Insira a porta(nao usar espaço): ");
	if(scanf("%u",(unsigned int*) &PORT) != 1){
		bf_elog(ERROR,"Não foi possivel ler o a porta\n");
	}
	bf_elog(DEBUG,"Configuração local terminada\n");
}