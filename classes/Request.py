if __name__ != "__main__":
	from globalsVar import *
	from socket import *
	import pickle

	class Request:

		FILE = 1
		END_FILE = 2
		LIST = 3
		PACKSIZE = 4

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
			if self.Type is Request.FILE:
				iD,dados = self.data
				with open(G.PATH_PROGRAM+str(G.Localhost.id)+"tmpFile/"+G.FILENAME+str(iD),"ab") as f:
					f.write(dados)

			elif self.Type is Request.END_FILE:
				print("Devo encerrar!")
				Thread.stop()

			elif self.Type is Request.PACKSIZE:
				G.RECPACKSIZE = 2*(int(self.data))
				print("PACKSIZE ajustado para: {}".format(G.RECPACKSIZE))

			elif self.Type is Request.LIST:
				print("Solve List Begin")
				G.ListIp = [i for i in self.data][:]
				G.Localhost = G.ListIp.pop(0)
				Thread.stop()				

	def send(socketFd,To,request):
		data = pickle.dumps(request)
		# print("Tamanho dado enviado: ",len(data), "para: ", To)
		socketFd.sendto(data,To)
		data = socketFd.recvfrom(128)
		if data[0] != b"ok":
			print("Nao recebeu ok -> {}".format(data[0]))
			exit(-1)


else:
	print("Request.py não pode ser main, e deve ser chamada em uniao a RecvThread")