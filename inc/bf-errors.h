#ifndef BF_ERRORS
#define BF_ERRORS

#include "std-c.h"

extern char *bf_stderr_filename;
extern FILE *bf_stderr;
extern char *bf_stdlog_filename;
extern FILE *bf_stdlog;
extern char *bf_stdinfo_filename;
extern FILE *bf_stdinfo;
extern char *bf_stdwarn_filename;
extern FILE *bf_stdwarn;

// bf_stddebug -> esta sendo usado o stdout, alterar nas funções que escrevem no arquivo


enum BF_ERRORSTYPE_ENUM{
	DEBUG = 0,
	LOG,
	WARNING,
	INFO,
	ERROR
};

typedef enum BF_ERRORSTYPE_ENUM BF_ERRORSTYPE;


enum BF_ERRORSCODE_ENUM{
	CUSTOM_ERROR = -1,
	SOCKET_ERROR = 0,
	BIND_ERROR,
	PTHREAD_CREATE_ERROR,
	FILE_OPEN_ERROR,
	MALLOC_ERROR,
	NULL_POINTER_ERROR
};

typedef enum BF_ERRORSCODE_ENUM BF_ERRORSCODE;

extern char *BF_ERRORMSG[];

/*
 Função que inicializa os ponteiros para os arquivos de log e error
 Essa função deve ser invocada na abertura do programa
*/
void bf_error_start_file();

void bf_error_msg(BF_ERRORSTYPE ErrorType, BF_ERRORSCODE ErrorCode);

void bf_error_end_file();

//Será basicamente nosso printf
void bf_elog(BF_ERRORSTYPE ErrorType,char *fmt, ...);

#endif