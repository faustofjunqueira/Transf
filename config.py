from sys import *
import time
import os

if __name__ == "__main__":
	print("Esse arquivo não pode ser chamado na main")
	exit()

def getPathProg():
	pathProgram = str()
	splited = argv[0].split("/")
	for i in splited[:len(splited)-1]:
		pathProgram += i+"/"
	return pathProgram

def configProg():	
	pathProgram = getPathProg() 
	nameTempFile = "".join(time.ctime().split(" "))+"junda"
	print("\n\tCUIDADO!")
	print("Uma configuração ruim pode gerar um mal funcionamento no software!\n")
	print("Para interromper a configuração digite exit. NAO USE ^C")
	print("Para nao mudar o caminho deixe vazio\n\n")

	with open(pathProgram+nameTempFile,"w") as w:
		with open(pathProgram+"globalsVar.py","r") as r:
			for line in r.readlines():
				splited = line.split("=")
				if splited[0] == "\tPATH_PROGRAM":
					path = ""
					if splited[1] != "None\n":
						print("Path configurado => "+splited[1])
					path = input("Insira o caminho para o programa(coloque a / no final do path por gentileza): ")
					if path == "exit":
						os.remove(pathProgram+nameTempFile)
						exit()
					elif path == "":
						w.write(line)
					else:
						w.write(splited[0]+'="'+path+'"\n')
				elif splited[0] == "\tMYPORT":
					port = input("Porta default atual:"+splited[1]+"Insira a nova porta default:")
					if path == "exit":
						os.remove(pathProgram+nameTempFile)
						exit()
					elif path == "":
						w.write(line)
					else:
						w.write(splited[0]+'='+port+'\n')					
				elif splited[0] == "\tTARGET_PATH":
					path = ""
					if splited[1] != "None\n":
						print("Path configurado => "+splited[1])
					path = input("Insira o caminho para o programa(coloque a / no final do path por gentileza): ")
					if path == "exit":
						os.remove(pathProgram+nameTempFile)
						exit()
					elif path == "":
						w.write(line)
					else:
						w.write(splited[0]+'="'+path+'"\n')
				else:
					w.write(line)

	os.remove(pathProgram+"globalsVar.py")
	os.rename(pathProgram+nameTempFile,pathProgram+"globalsVar.py")

	print("Programa configurado com sucesso!")
	exit()

def showConfig():
	pathProgram = getPathProg()
	with open(pathProgram+"globalsVar.py","r") as r:
		path = ""
		port = ""
		packsize = ""
		recpacksize = ""
		target_path = ""
		for line in r.readlines():
			splited = line.split("=")
			if splited[0] == "\tPATH_PROGRAM":
				path = splited[1]
			elif splited[0] == "\tMYPORT":
				port = splited[1] 
			elif splited[0] == "\tPACKSIZE":
				packsize = splited[1]
			elif splited[0] == "\tRECPACKSIZE":
				recpacksize = splited[1]
			elif splited[0] == "\tTARGET_PATH":
				target_path = splited[1]
		print("\nConfiguração do fast-cp:\n\tCaminho do fast-cp: "+path+
			  "\tPorta(default): "+port+
			  "\tTamanho do pacote: "+packsize+
			  "\tTamanho do pacote de recepção: "+recpacksize+
			  "\tCaminho das listas de targets: "+target_path)
	exit() 