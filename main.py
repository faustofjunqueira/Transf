#!/usr/bin/python3

import pickle
from sys import *
import socket
import threading
import socketserver

ID = 0
IP = 1
PORT = 9090
FILENAME = 3

LISTA = 1
MSG = 2
FINAL = 3

TERMINADOS = 0

ListaIp = list()
server = None

def cat(filename,ate):
	with open(filename,"wb") as w:
		for i in range(1,ate+1):
			with open(filename+str(i),"rb") as r:
				w.write(r.read())

def Enviando():
	checksum = "junda"
	npack = 50

	global ID
	global IP
	global PORT
	global FILENAME
	global LISTA
	global MSG
	global FINAL
	global TERMINADOS

	global ListaIp

	Localhost = ListaIp.pop(0)
	f = open(Localhost[FILENAME],"rb")
	init = int(Localhost[ID]) +1
	end = int(ListaIp[-1][ID]) +1
	for i in range(init,end):
		cur_dest = ListaIp[0]	
		f.seek(0,2)
		sizeFile = f.tell()
		f.seek(0)
		diffFile = sizeFile % (int(cur_dest[ID])-1)
		sizeFile /= int(cur_dest[ID])-1
		
		myFileSize = sizeFile
		if int(Localhost[ID]) is int(cur_dest[ID])-1:
			myFileSize += diffFile
			
		deltaPack = int(myFileSize/npack)
		diffPack = int(myFileSize % npack)
		initWidth = int((int(Localhost[ID])-1)*sizeFile)

		socketFd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    

		enviar(socketFd,ListaIp,ListaIp,LISTA,Localhost[ID])

		f.seek(initWidth)
		for i in range(0,npack):
			enviar(socketFd, ListaIp, f.read(deltaPack),MSG,Localhost[ID])
		enviar(socketFd, ListaIp, f.read(diffPack),MSG,Localhost[ID])
		print("TERMINAR PACOTE")
		enviar(socketFd, ListaIp, 1,FINAL,Localhost[ID])
		ListaIp.pop(0)
		f.seek(0)

	f.close()


class ThreadedUDPRequestHandler(socketserver.BaseRequestHandler):

	def handle(self):
		sock = self.request[1]
		msg = pickle.loads(self.request[0])
		global ListaIp
		if msg[1] is LISTA:
			ListaIp = msg[0]
		elif msg[1] is MSG:
			with open(ListaIp[0][FILENAME]+msg[2],"ab") as f:
				f.write(msg[0])
		elif msg[1] is FINAL:
			global TERMINADOS
			TERMINADOS += 1
			if int(ListaIp[0][ID])-1 is TERMINADOS:
				print("Terminado a recepção de pacotes")
				cat(ListaIp[0][FILENAME],int(ListaIp[0][ID])-1)
				Enviando()
		sock.sendto(bytes("OK","utf-8"), self.client_address)

class ThreadingUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
	pass

def enviar(socketFd, Ips,data,tipo,id):
	a = (data,tipo,id)
	msg = pickle.dumps(a)

	socketFd.sendto(msg, (Ips[0][IP],PORT))
	received = str(socketFd.recv(5), "utf-8")
	if received != "OK":
		print("Deu ruim no envio do pacote id {}".format(Ips[0][ID]))

def CarregarListaIp(filename):
		return [i.strip("\n").split(" ") for i in open(filename,"r").readlines()]

if __name__ == "__main__":	
	
	if len(argv) > 1:
		if argv[1] == "junda":
			ListaIp = CarregarListaIp("ip.config")
			Enviando()
	else:		
		server = ThreadingUDPServer(("localhost", PORT), ThreadedUDPRequestHandler)
		ip, port = server.server_address
		server_thread = threading.Thread(target=server.serve_forever)
		server_thread.daemon = False
		server_thread.start()
		server_thread.join()
		server.shutdown()

