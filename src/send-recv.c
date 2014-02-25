#include "send-recv.h"

enum STATUS_TRANSITION{
	LOST_PAC = 1,
	SUCCESS
};

int SocketFd;

pthread_mutex_t ReplyMutex;
pthread_cond_t ReplyCond;
enum STATUS_TRANSITION status;
char ip_rem[IP_LEN];
MSG Recv_msg;

void startSockets(){
	pthread_t Recv_t;
	struct sockaddr_in MyAddr;
	if((SocketFd = socket(AF_INET, SOCK_DGRAM, 0)) < 0 )
		bf_error_msg(ERROR,SOCKET_ERROR);

	memset((char *)&MyAddr, 0, sizeof(MyAddr));
	MyAddr.sin_family = AF_INET;
	MyAddr.sin_addr.s_addr = htonl(INADDR_ANY);
	MyAddr.sin_port = htons(PORT);
	if (bind(SocketFd, (struct sockaddr *)&MyAddr, sizeof(MyAddr)) < 0) 
		bf_error_msg(ERROR,BIND_ERROR);
	
	pthread_mutex_init(&ReplyMutex,NULL);
	pthread_cond_init(&ReplyCond,NULL);
	if (pthread_create(&Recv_t, NULL, recv_thread, NULL)) {
      bf_elog(ERROR,"--ERRO: pthread_create()\n");
    }
}

void sendMsg(MSG *msg){

	struct sockaddr_in remaddr;
	size_t n_byte_msg = sizeof(MSG);
	size_t n_byte_addr = sizeof(remaddr);
	char ip_loc[IP_LEN];	

	ip2charptr(&(AllMachine[msg->id].ip),ip_loc);
	memset((char *) &remaddr, 0, sizeof(remaddr));
	remaddr.sin_family = AF_INET;
	remaddr.sin_port = htons(PORT);
	if(inet_aton(ip_loc, &remaddr.sin_addr)==0)
		bf_elog(WARNING,"Problem in sendMsg, don't get convert in SEND inet_aton");

	while(1){
		if (sendto(SocketFd, msg, n_byte_msg, 0, (struct sockaddr *)&remaddr, n_byte_addr) < 0)
			bf_elog(ERROR,"Could not send the request");
		
		pthread_cond_wait(&ReplyCond,&ReplyMutex);
		
		if(status == SUCCESS && !strcmp(ip_rem,ip_loc))
			break;	
	}

}

void *recv_thread(void *arg){
	MSG reply = {MyMachine.id,REPLY};
	struct sockaddr_in remaddr;
	size_t n_byte_msg;
	size_t n_byte_addr;
	char ip_loc[IP_LEN];
	n_byte_msg = sizeof(MSG);
	n_byte_addr = sizeof(remaddr);
	ip2charptr(&MyMachine.ip,ip_loc);

	while(1){

		memset(&Recv_msg,0,sizeof(MSG));
		if(recvfrom(SocketFd, &Recv_msg, n_byte_msg, 0,
                      (struct sockaddr *) &remaddr,(socklen_t *) &n_byte_addr) < 0) //Analizar se todos os pacotes tem o tamanho da request, já q o recvfrom retorna o numero de bytes recebidos, teoriamente tem que ser do tamanho do sizeof(request)
			bf_elog(ERROR,"Could not recv the request");
		
		if(Recv_msg.msg != REPLY){
			printf("aqui\n");
			if (sendto(SocketFd, &reply, n_byte_msg, 0, (struct sockaddr *)&remaddr, n_byte_addr) < 0)
				bf_elog(ERROR,"Could not send the request");
			treatMsg(Recv_msg);
		}else{
			if(inet_ntop( AF_INET, &remaddr, ip_rem, INET_ADDRSTRLEN ) == 0){
				bf_elog(WARNING,"Problem in sendMsg, don't get convert in SEND inet_nton");
				status = LOST_PAC;
				pthread_cond_signal(&ReplyCond);
			}
			if(Recv_msg.msg == REPLY){
				status = SUCCESS;
				pthread_cond_signal(&ReplyCond);
				continue;
			}
		}
	}

	pthread_exit(NULL);
}

void treatMsg(MSG msg){
	printf("Rec\n\tID:%d\n\t%d\n", msg.id,msg.msg);
	return;
}