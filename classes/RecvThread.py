if __name__ != "__main__":

	from socket import *
	from threading import Thread
	import pickle

	import classes.Request as Request
	
	class RecvThread(Thread):

		def __init__(self,PACKSIZE,SOCKET):
			Thread.__init__(self)
			self.socketFd = SOCKET
			
			self.request = None
			self.packsize = PACKSIZE
			self.endRun = False
		
		def stop(self):
			self.endRun = True

		def run(self):
			while not self.endRun:
				data,addr = self.socketFd.recvfrom(self.packsize)
				self.data = pickle.loads(data)
				self.request = Request.Request()
				self.request.setRequest(self.data)
				self.request.solve(self)
				self.socketFd.sendto(b"ok",addr)
			print("Acabei!")

else:
	print("RecvThread.py não pode ser init")