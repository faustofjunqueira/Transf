# TODO: -> Fazer paramentro --config para definir o PATH_PROGRAM

import os
from globalsVar import *
from sys import *
from classes import *
from socket import *
from utils import *
from config import *

def run():
	StartFlag,socketFd = (ReadParam(),socket(AF_INET, SOCK_DGRAM))
	try:
		socketFd.bind(("",G.MYPORT))
	except PermissionError:
		print("Voce nao tem permissao para usar essa porta. Deve ter algum software rodando nessa porta. Tente outra")
		exit()
	
	if StartFlag:
		print("Start Step")
		G.ListIp,G.Localhost = StartStep(socketFd)
		try:
			os.mkdir(G.PATH_PROGRAM+str(G.Localhost.id)+"tmpFile")
		except FileExistsError:
			print("Diretorio temporario existente, será excluido!")
			removeFile(G.PATH_PROGRAM+str(G.Localhost.id)+"tmpFile")
			os.mkdir(G.PATH_PROGRAM+str(G.Localhost.id)+"tmpFile")
		print("End Start Step")
	else:
		print("Receive List Step")
		RecvThreadList = list()
		RecvThreadList.append(RecvThread.RecvThread(G.PACKSIZE,socketFd))
		RecvThreadList[0].start()
		RecvThreadList[0].join()			
		print("Start Receive Step")
		try:
			os.mkdir(G.PATH_PROGRAM+str(G.Localhost.id)+"tmpFile")
		except FileExistsError:
			removeFile(G.PATH_PROGRAM+str(G.Localhost.id)+"tmpFile")
			os.mkdir(G.PATH_PROGRAM+str(G.Localhost.id)+"tmpFile")
	
		RecvStep(G.Localhost,socketFd)
		print("End Receive Step")
	
	print("Start Send Step")
	SendStep(socketFd,G.ListIp,G.FILENAME)
	print("End Send Step")
	
	removeFile(G.PATH_PROGRAM+str(G.Localhost.id)+"tmpFile/")
