import os
from globalsVar import *
from sys import *
import time
from classes import Target

if __name__ == "__main__":
	print("Esse arquivo não pode ser chamado na main")
	exit()

class TargetList:

	def __init__(self,TARGET_PATH):
		
		self.TARGET_PATH = TARGET_PATH
		self.list = []
		self.filename = "TargetList"+time.ctime()
		self.add((1,"127.0.1.1",G.MYPORT))

	def create(self,filename = ""):
		if len(filename) > 0:
			self.filename = filename 
		if os.access(self.TARGET_PATH+self.filename,os.F_OK):
			print("Lista existente! Não foi possivel criar uma lista nova. Remova se necessario")
			exit()		
		with open(self.TARGET_PATH+self.filename,"w") as w:
			pass

	def save(self):
		with open(self.TARGET_PATH+self.filename,"w") as w:
			i = 1
			for t in self.list:
				w.write(str(t[0])+" "+t[1]+" "+str(t[2])+"\n")
				i += 1

	def add(self,t):
		self.list.append(t)
		for i in self.list:
			print(i)

	def load(filename):
		if os.access(filename,os.F_OK):
			os.rename(filename,self.TARGET_PATH+filename)
		else:
			print("Nao foi encontrado o arquivo")
			exit()

	def remove(filename):
		if os.access(self.TARGET_PATH+filename,os.F_OK):
			os.remove(self.TARGET_PATH+filename)
		else:
			print("Lista inexistente")

def targetListProg(TARGET_PATH):
	TList = TargetList(TARGET_PATH)
			
	TList.filename = input("Nome da lista de targets: ")
	if len(TList.filename) is 0:		
		print("Nome invalido! Foi gerado um nome ramdomico para sua lista => "+TList.filename)

	i = 2
	stop = False
	print("Voce sempre eh o ID 1 da sua lista de targets, então comecemos pelo 2")
	id = port =0
	ip = ""

	while not stop:		
		print("Insira o target numero "+str(i))
		id = i
		ip = input("\tIP: ")
		try:
			port = int(input("\tPorta: "))
		except ValueError:
			print("Porta Invalida")
			continue

		TList.add((id,ip,port))

		while True:
			r = input("Deseja inserir mais um target?(S/n) ")
			if r == "" or r == "S" or r == "s":				
				break
			elif r == "N" or r == "n":
				stop = True
				break
			else:
				print("Opcao errada! ")
		i += 1


	while True:
		r = input("Deseja salvar a lista(S/n) ")
		if r == "" or r == "S" or r == "s":
			TList.create()
			TList.save()
			print("Lista "+TList.filename+" salva com sucesso")
			break
		elif r == "N" or r == "n":
			break
		else:
			print("Opcao errada! ")

	exit()		