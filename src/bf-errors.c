#include "bf-errors.h"

char *bf_stderr_filename = "logs/errors";
FILE *bf_stderr;
char *bf_stdlog_filename = "logs/log.log";
FILE *bf_stdlog;
char *bf_stdinfo_filename = "logs/info";
FILE *bf_stdinfo;
char *bf_stdwarn_filename = "logs/warn";
FILE *bf_stdwarn;
char *bf_sttest_filename = "logs/warn";
FILE *bf_sttest;

char *BF_ERRORMSG[] ={
	"Was not possible to create the socket",
	"Bind Error",
	"Was not possible to create the thread",
	"Was not possible to open the file",
	"Malloc failed",
	"Null pointer error"
};

/*
 Função que inicializa os ponteiros para os arquivos de log e error
 Essa função deve ser invocada na abertura do programa
*/
void bf_error_start_file(){
	//Ler os bf_std##_filename de um XML
	bf_stderr = bf_fopen(bf_stderr_filename,"a");
	bf_stdlog = bf_fopen(bf_stdlog_filename,"a");
	bf_stdwarn = bf_fopen(bf_stdwarn_filename,"a");
	bf_stdinfo = bf_fopen(bf_stdinfo_filename,"a");
}
/*
  Essa função deve ser chamada quando finaliza o programa
*/
void bf_error_end_file(){
	fclose(bf_stderr);
	fclose(bf_stdlog);
	fclose(bf_stdwarn);
	fclose(bf_stdinfo);
}

/*
 Função mostra o erro
*/
void bf_error_msg(BF_ERRORSTYPE ErrorType, BF_ERRORSCODE ErrorCode){
	switch(ErrorType){
		case LOG: fprintf(bf_stdlog, "[%s]:%s\n",bf_now(), BF_ERRORMSG[ErrorCode]); break;
		case DEBUG: fprintf(stdout, "[%s]:%s\n",bf_now(), BF_ERRORMSG[ErrorCode]); break;
		case WARNING: fprintf(bf_stdwarn, "[%s]:%s\n",bf_now(), BF_ERRORMSG[ErrorCode]); break;
		case INFO: fprintf(bf_stdinfo, "[%s]:%s\n",bf_now(), BF_ERRORMSG[ErrorCode]); break;
		case ERROR:
			fprintf(bf_stderr, "[%s]:%s\n",bf_now(), BF_ERRORMSG[ErrorCode]);
			bf_exit(ErrorCode);
			break;
	}
	
}

void bf_elog(BF_ERRORSTYPE ErrorType,char *fmt, ...){	
	FILE *fpt;
	va_list ap;
	char *p, *sval;

	va_start(ap, fmt);
	switch(ErrorType){
		case LOG: fpt = bf_stdlog; break;
		case DEBUG: fpt = stdout; break;
		case WARNING: fpt = bf_stdwarn; break;
		case INFO: fpt = bf_stdinfo; break;
		case ERROR: fpt = bf_stderr; break;
	}
	fprintf(fpt, "[%s]: ", bf_now());
	for (p = fmt; *p; p++) {
		if (*p != '%') {
			fprintf(fpt,"%c",*p);
			continue;
		}
		switch (*++p) {
			case 'd':
				fprintf(fpt,"%d", va_arg(ap, int));
				break;
			case 'f':
				fprintf(fpt,"%f", va_arg(ap, double));
				break;
			case 's':
				for (sval = va_arg(ap, char *); *sval; sval++)
					fputc(*sval,fpt);
				break;
			default:
				fprintf(fpt,"%c", *p);
				break;
		}
	}
	fprintf(fpt,"\n");
	va_end(ap);
	if(ErrorType == ERROR)
		bf_exit(CUSTOM_ERROR);
} 
