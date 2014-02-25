#include "std-c.h"
#include "bf-errors.h"

FILE *bf_fopen(char *filename, char *type){
	FILE *file;
	if((file = fopen(filename,type)) == NULL){
		printf("File %s: %s\n",filename, BF_ERRORMSG[FILE_OPEN_ERROR]);
		bf_exit(FILE_OPEN_ERROR);
	}
	return file;
}

void bf_exit(int code){
	exit(code);
}

char *bf_now(){
	char *str = (char *)malloc (sizeof(char)*32);
	    time_t     now = time(0);
    struct tm  tstruct;
    tstruct = *localtime(&now);
    strftime(str, sizeof(char)*32, "%Y-%m-%d %H:%M:%S", &tstruct);
	return str;
}

