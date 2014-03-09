#!/usr/bin/python3

# TODO:
#	-> Fazer paramentro --config para definir o PATH_PROGRAM

import os
from globalsVar import *
from sys import *
from classes import *
from socket import *
from utils import *

if __name__ != "__main__":
	exit()

StartFlag = ReadParam()

print("Porta "+str(G.MYPORT))
print("Filename "+str(G.FILENAME))
print("Start "+str(StartFlag))

socketFd = socket(AF_INET, SOCK_DGRAM)
while True:
	try:
		socketFd.bind(("localhost",G.MYPORT))
	except PermissionError:
		print("Voce nao tem permissao para usar essa porta. Tente outra")
		exit()

if StartFlag:
	print("Start Step")
	G.ListIp,G.Localhost = StartStep(socketFd)
	
	try:
		os.mkdir(G.PATH_PROGRAM+str(G.Localhost.id)+"tmpFile")
	except FileExistsError:
		removeFiles(G.PATH_PROGRAM+str(G.Localhost.id)+"tmpFile")
		os.mkdir(G.PATH_PROGRAM+str(G.Localhost.id)+"tmpFile")	
	print("End Start Step")
else:
	print("Receive List Step")
	RecvThreadList = list()
	RecvThreadList.append(RecvThread.RecvThread(G.PACKSIZE,socketFd))
	RecvThreadList[0].start()
	RecvThreadList[0].join()			
	print("Start Receive Step")
	os.mkdir(G.PATH_PROGRAM+str(G.Localhost.id)+"tmpFile")
	RecvStep(G.Localhost,socketFd)
	print("End Receive Step")

print("Start Send Step")
SendStep(socketFd,G.ListIp,G.FILENAME)
print("End Send Step")

removeFiles(G.PATH_PROGRAM+str(G.Localhost.id)+"tmpFile/")
