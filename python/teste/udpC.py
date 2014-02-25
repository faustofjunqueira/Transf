#!/usr/bin/python3
import socket
import sys

HOST, PORT = "localhost",9090
filename = "".join(sys.argv[1])

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

with open(filename,"rb") as f:
	totalSend = 0
	f.seek(0,2)
	lenFile = f.tell()
	f.seek(0)
	npack = 90;
	delta =int(lenFile / npack)
	dif = lenFile - npack*delta
	for x in range(0,npack):
		totalSend += (sock.sendto(f.read(delta), (HOST, PORT)))
		received = str(sock.recv(1024), "utf-8")
		print("Check {}: {} totalSend {}".format(x,received,totalSend))
	totalSend += sock.sendto(f.read(dif), (HOST, PORT))
	received = str(sock.recv(1024), "utf-8")
	print("Check DIF: {} totalSend {}".format(received,totalSend))
	sock.sendto(bytes("save","utf-8"), (HOST, PORT))
	received = str(sock.recv(1024), "utf-8")
	print("Check Close: {}".format(received))



print("Process: {}".format(received))