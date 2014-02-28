#!/usr/bin/python3

IP_LIST_FILENAME = "target.list"
MYPORT = 9090
MYID = 0
FILENAME = "junda"
PACKSIZE = 1024

from sys import *
from classes import *
from socket import *

if __name__ == "__main__":

	def CarregaArquivo(filename):
		ListIp = list()	
		listTemp = [i.strip("\n").split(" ") for i in open(filename,"r").readlines()]
		for l in listTemp:
			target = Target.Target()
			target.id = int(l[0])
			target.ip = l[1]
			target.port = int(l[2])
			ListIp.append(target)
		return ListIp

	def SendList(socketFd, ListIp):
		request = Request.Request()
		request.setRequest((ListIp,Request.Request.LIST))
		Request.send(socketFd,(ListIp[0].ip,ListIp[0].port),request)

	def StartStep(socketFd):
		ListIp = CarregaArquivo(IP_LIST_FILENAME)
		Localhost = ListIp.pop(0)
		ListTemp = ListIp
		while len(ListIp) is not 0:
			SendList(socketFd,ListIp)
			ListIp.pop(0)

		return (Localhost,ListTemp)

	def CatFile(filename,ate):
		global FILENAME
		with open(filename,"wb") as w:
			for i in range(1,ate+1):
				with open("tmp/"+FILENAME+str(i),"rb") as r:
					w.write(r.read())

	def RecvStep(Localhost, socketFd):
		RecvThreadList = [RecvThread.RecvThread(PACKSIZE,socketFd) for i in range(0,Localhost.id)]
		for i in RecvThreadList:
			i.start()
		for i in RecvThreadList:
			i.join()
		CatFile(FILENAME,Localhost.id-1)
		#FAzer checksum

	def SendFile(socketFd,f,ListIp, lenFile):
		global PACKSIZE
		global Localhost
		cur_target = ListIp.pop(0)
		Myblock = int(lenFile/(cur_target.id-1))
		init = (cur_target.id-1)*Myblock
		
		if cur_target.id-1 is Localhost.id:
			Myblock += int(lenFile/cur_target.id-1)

		f.seek(init)

		npack = int(Myblock/PACKSIZE)
		diffPack = int(Myblock % PACKSIZE)
		
		request = Request.Request()
		
		for i in range(npack):			
			data = (Localhost.id,f.read(PACKSIZE))
			request.setRequest((data,Request.Request.FILE))
			Request.send(socketFd,(cur_target.ip,cur_target.port),request)

		data = (Localhost.id,f.read(diffPack))
		request.setRequest((data,Request.Request.FILE))
		Request.send(socketFd,(cur_target.ip,cur_target.port),request)


	def SendStep(socketFd,ListIp,filename):
		with open(filename,"rb") as f:
			lenFile = f.seek(0,2)
			while len(ListIp) is not 0:
				f.seek(0)
				SendFile(socketFd,f,ListIp,lenFile)
				ListIp.pop(0)
		request = Request.Request()
		request.setRequest((None,Request.Request.END_FILE))
		Request.send(socketFd,(cur_target.ip,cur_target.port),request)

	Localhost = None
	ListIp = []
	socketFd = socket(AF_INET, SOCK_DGRAM)

	if len(argv) >= 3:
		
		MYPORT = int(argv[1])
		FILENAME = argv[2]
		socketFd.bind(("localhost",MYPORT))

		if len(argv) > 3 and argv[3] == "--start":
			print("Start")
			ListIp,Localhost = StartStep(socketFd)
		else:
			RecvThreadList = list()
			RecvThreadList.append(RecvThread.RecvThread(PACKSIZE,socketFd))
			RecvThreadList[0].start()
			RecvThreadList[0].join()
			RecvStep(Localhost,socketFd)
		if len(argv) > 4:
			print("Argumentos desnecessarios: {}".format(argv[4:]))

		SendStep(socketFd,ListIp,FILENAME)

	else:
		print("Parametros indefinidos")
		exit(-1)

