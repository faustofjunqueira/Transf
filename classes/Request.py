if __name__ != "__main__":
	from socket import *
	import pickle
	
	class Request:

		FILE = 1
		END_FILE = 2
		LIST = 3

		def __init__(self):
			self.data = None
			self.Type = None			

		def setRequest(self,arg):
			if type(arg) is tuple:
				self.data,self.Type = arg
			else:
				print("Request: Argumento passado para o setRequest não é uma tupla.\n faça (data,tipo)")
				exit(-1)

		def solve(self,Thread):
			global FILENAME
			if self.Type is Request.FILE:
				iD,dados = self.data
				with open("tmp/"+FILENAME+str(iD),"ab"):
					f.write(dados)

			elif self.Type is Request.END_FILE:
				Thread.stop()

			elif self.Type is Request.LIST:
				global Localhost
				global ListIp
				ListIp = [i for i in self.data]
				Localhost = ListIp.pop(0)
				Thread.stop()				

	def send(socketFd,To,request):
		data = pickle.dumps(request)
		socketFd.sendto(data,To)
		data = socketFd.recvfrom(128)
		if data[0] != "ok":
			print("Nao recebeu ok!")
			exit(-1)


else:
	print("Request.py não pode ser main, e deve ser chamada em uniao a RecvThread")