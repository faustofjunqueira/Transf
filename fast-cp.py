#!/usr/bin/python3

# TODO:
#	-> Fazer paramentro --config para definir o PATH_PROGRAM

import os
from globalsVar import *
from sys import *
from classes import *
from socket import *

if __name__ == "__main__":

	def removeFile(path):
		files = os.listdir(path)
		for f in files:
			os.remove(path+files)
		os.removedirs(path)

	def CarregaArquivo(filename):
		ListIp = list()	
		listTemp = [i.strip("\n").split(" ") for i in open(G.PATH_PROGRAM+filename,"r").readlines()]
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
		ListIp = CarregaArquivo(G.IP_LIST_FILENAME)
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
		with open(G.PATH_CALL_PROGRAM+filename,"wb") as w:
			for i in range(1,ate+1):				
				with open(G.PATH_PROGRAM+str(G.Localhost.id)+"tmpFile/"+G.FILENAME+str(i),"rb") as r:
					w.write(r.read())

	def RecvStep(Localhost, socketFd):
		RecvThreadList = [RecvThread.RecvThread(G.PACKSIZE,socketFd) for i in range(0,Localhost.id-1)]
		for i in RecvThreadList:
			i.start()
		for i in RecvThreadList:
			i.join()
		print("Vamos concatenar!")
		CatFile(G.FILENAME,Localhost.id-1)
		#FAzer checksum

	def SendFile(socketFd,f,ListIp, lenFile):
		cur_target = ListIp.pop(0)
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
	
	socketFd = socket(AF_INET, SOCK_DGRAM)
	if len(argv) >= 3:
		G.MYPORT = int(argv[1])
		G.FILENAME = argv[2]
		socketFd.bind(("localhost",G.MYPORT))

		if len(argv) > 3 and argv[3] == "--start":
			print("Start Step")
			G.ListIp,G.Localhost = StartStep(socketFd)
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
		if len(argv) > 4:
			print("Argumentos desnecessarios: {}".format(argv[4:]))
		print("Start Send Step")
		SendStep(socketFd,G.ListIp,G.FILENAME)
		print("End Send Step")
	else:
		print("Parametros indefinidos")
		exit(-1)

	removeFiles(G.PATH_PROGRAM+str(G.Localhost.id)+"tmpFile/")
	