
# TODO: 
#	Parametros -t: Verificar se o arquivo existe

import os
from globalsVar import *
from sys import *
from classes import *
from socket import *
from config import *

if __name__ == "__main__":
	print("Esse arquivo não pode ser chamado na main")
	exit()

def creditos():
	print("Créditos:")
	print("\n\tEstudantes de Graduação UFRJ - Deparatamento de Ciências da Computação - Brasil")
	print("\n\tDesenvolvedores:\n\t\tFausto F Junqueira\n\t\tJúlio Cesar S Pereira")
	print("\tIdealizadores:\n\t\tBernardo Lins\n\t\tFausto Junqueira\n\t\tGuilherme Oki\n\t\tLeon Augusto\n\t\tJúlio Cesar Pereira")
	print("\n")

def PrintMan(msg = ""):
	if len(msg) > 0:
		print("\n")
		print(msg)
	print("\n")
	print("Faça:")
	print("\tfast-cp [opcao] [nome_arquivo]")
	print("Opções:")
	print("\t --start : inicia o ciclo de envios. Quando o programa não iniciado com esse parametro, ele já fica em modo de recepção dos pacotes, até que seja recepcionado por um arquivo\n")
	print("\t -p [PORTA] : define a porta que será usada para a transmissão. Default "+str(G.MYPORT)+"\n")
	print("\t -t : Escolhe uma lista de targets\n")
	print("\t --config : Esse parametro deve ser chamado quando se instala o software afim de configurar o software. Esse parametro deve ser chamado sozinho!. Se não for configurado! o software nao irá funcionar devidamente!\n")
	print("\t --show-config : Mostra as configurações do software. Esse parametro deve ser chamado sozinho!\n")
	print("\t --target-create: Ferramenta de criação de lista de targets\n")
	print("\t --target-list-add [LISTA] [IP] [PORTA] : Adiciona um target em uma determinada lista\n")
	print("\t --target-list-show [LISTA] : Mostra os targets de uma determinada lista\n")
	print("\n")
	creditos()
	exit()

def ReadParam():
	PORTFLAG = False
	STARTFLAG = False
	FILENAMEFLAG = False
	i = 1
	while i < len(argv):
		if argv[i] == "-p":	
			try:
				PORTFLAG = True
				i += 1
				G.MYPORT = int(argv[i])
				if G.MYPORT < 0:
					PrintMan("Porta invalida, voce sabe oq eh uma porta de rede?")
			except ValueError:
				PrintMan("Porta invalida, voce sabe oq eh uma porta de rede?")
		elif argv[i] == "--start":
			if STARTFLAG:
				PrintMan("--start já foi invocado. O que você gostaria de fazer?")
			STARTFLAG = True
		elif argv[i] == "--config":
			if i is 1 and len(argv) is 2:
				configProg()
			else:
				PrintMan("O paramentro --config so pode ser chamado sozinho! Tu num vai querer configurar e usar ao mesmo tempo neah!")
		elif argv[i] == "--show-config":
			if i is 1 and len(argv) is 2:
				showConfig()
			else:
				PrintMan("O paramentro --show-config so pode ser chamado sozinho! Tu num vai querer ver a configuração e usar ao mesmo tempo neah!")
		elif argv[i] == "--help" or argv[i] == "-h":
			if i is 1 and len(argv) is 2:
				PrintMan()
			else:
				PrintMan("O paramentro --help(-h) so pode ser chamado sozinho! Tu num vai querer ver a ajuda e usar ao mesmo tempo neah!")
		elif argv[i] == "--target-create":
			if i is 1:
				TargetList.targetListProg(G.TARGET_PATH)
			else:
				PrintMan("O paramentro --target-create deve ser o segundo parametro a ser chamado, pois ele inicia o modo de criação de lista de targets")

		elif argv[i] == "--target-show":
			if i is 1:
				l = os.listdir(G.PATH_PROGRAM+G.TARGET_PATH)
				print("Lista de targets:")
				for a in l:
					print("\t"+a)
				exit()
			else:
				PrintMan("O paramentro --target-show deve ser invocado sozinho")
		elif argv[i] == "-t":
			if os.access(G.PATH_PROGRAM+G.TARGET_PATH+argv[i+1],os.F_OK):
				i += 1
				G.TARGETLIST = argv[i]
			else:
				print("Target List inexistente")
		elif argv[i] == "--target-list-add":
			if os.access(G.PATH_PROGRAM+G.TARGET_PATH+argv[i+1],os.F_OK):
				TargetList.TargetListAdd(G.PATH_PROGRAM+G.TARGET_PATH)
			else:
				PrintMan("Target List inexistente")
		elif argv[i] == "--target-list-show":
			if os.access(G.PATH_PROGRAM+G.TARGET_PATH+argv[i+1],os.F_OK):
				TargetList.TargetListShow(G.PATH_PROGRAM+G.TARGET_PATH)
			else:
				PrintMan("Target List inexistente")
		else:
			if argv[i][0] is '-':
				PrintMan("Nome invalido para arquivo! Suponho que voce não queria copiar esse arquivo! Isso eh um arquivo?!")
			if FILENAMEFLAG:
				PrintMan("Multiplos nomes de arquivos. Até o momento esse programa so copia um por vez. Iremos melhorar!")
			if len(argv[i]) < 1:
				PrintMan("Arquivo sem nome?!")

			FILENAMEFLAG = True
			G.FILENAME = argv[i]

		i += 1
	if not FILENAMEFLAG:
		PrintMan("Se voce nao me falar o nome do arquivo fica meio dificil de saber oque eu tenho que copiar!")
	return STARTFLAG

def removeFile(path):
	files = os.listdir(path)
	for f in files:
		os.remove(path+"/"+f)
	os.removedirs(path)

def CarregaArquivo(filename):
	ListIp = list()	
	listTemp = [i.strip("\n").split(" ") for i in open(G.PATH_PROGRAM+G.TARGET_PATH+filename,"r").readlines()]
	for l in listTemp:
		target = Target.Target()
		target.id = int(l[0])
		target.ip = l[1]
		target.port = int(l[2])
		ListIp.append(target)
	return ListIp

def SendList(socketFd, ListIp):
	Request.send(socketFd,(ListIp[0].ip,ListIp[0].port),(ListIp,Request.Request.LIST))

def StartStep(socketFd):
	print(G.PATH_PROGRAM +G.TARGET_PATH+G.TARGETLIST)
	ListIp = CarregaArquivo(G.TARGETLIST)
	print(ListIp)
	Localhost = ListIp.pop(0)
	ListTemp =  ListIp[:]
	# lenFile = open(G.FILENAME,"rb").seek(0,2)
	# G.PACKSIZE = int(lenFile*0.001/ListTemp[-1].id)+1 # 38% do tamanho total
	while len(ListIp) is not 0:
		SendList(socketFd,ListIp)
		# Request.send(socketFd,(ListIp[0].ip,ListIp[0].port),(G.PACKSIZE,Request.Request.PACKSIZE))
		ListIp.pop(0)
	return (ListTemp,Localhost)

def CatFile(FILENAME,ate):		
	with open(G.PATH_CALL_PROGRAM+FILENAME,"wb") as w:
		for i in range(1,ate+1):				
			with open(G.PATH_PROGRAM+str(G.Localhost.id)+"tmpFile/"+FILENAME+str(i),"rb") as r:
				w.write(r.read())

def RecvStep(Localhost, socketFd):
	RecvThreadList = [RecvThread.RecvThread(G.PACKSIZE,socketFd) for i in range(0,Localhost.id-1)]
	for i in RecvThreadList:
		i.start()
	for i in RecvThreadList:
		i.join()
	#print("Vamos concatenar!")
	CatFile(G.FILENAME,Localhost.id-1)
	#FAzer checksum

def SendFile(socketFd,f,ListIp, lenFile):
	cur_target = ListIp.pop(0)
	print("enviando para " + str(cur_target))
	Myblock = int(lenFile/(cur_target.id-1)) # Meu bloco
	init = (G.Localhost.id-1)*Myblock
	
	if cur_target.id-1 is G.Localhost.id:
		Myblock += int(lenFile%(cur_target.id-1))

	# f.seek(init)

	npack = int(Myblock/G.PACKSIZE)
	diffPack = int(Myblock % G.PACKSIZE)

	end = init + G.PACKSIZE

	for i in range(npack):
		# print("from:{} to:{} slice:({},{}) npack:{} diffpack:{} Myblock:{} PACKSIZE:{}".format(G.Localhost.id,cur_target.id,init,end,npack,diffPack,Myblock,G.PACKSIZE))
		data = (G.Localhost.id,f[init:end])
		Request.send(socketFd,(cur_target.ip,cur_target.port),(data,Request.Request.FILE))
		init += G.PACKSIZE
		end += G.PACKSIZE

	end -= G.PACKSIZE
	# print("from:{} to:{} slice:({},{}) npack:{} diffpack:{} Myblock:{} PACKSIZE:{}".format(G.Localhost.id,cur_target.id,end,end+diffPack,npack,diffPack,Myblock,G.PACKSIZE))
	data = (G.Localhost.id,f[end:end+diffPack])
	# data = (G.Localhost.id,f.read(diffPack))
	Request.send(socketFd,(cur_target.ip,cur_target.port),(data,Request.Request.FILE))

	Request.send(socketFd,(cur_target.ip,cur_target.port),(None,Request.Request.END_FILE))

def SendStep(socketFd,ListIp,filename):
	with open(G.PATH_CALL_PROGRAM+filename,"rb") as f:
		lenFile = f.seek(0,2)
		while len(ListIp) is not 0:
			# Request.send(socketFd,(ListIp[0].ip,ListIp[0].port),(G.PACKSIZE,Request.Request.PACKSIZE)) 
			f.seek(0)
			SendFile(socketFd,f.read(),ListIp[:],lenFile)
			ListIp.pop(0)
