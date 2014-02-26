#!/usr/bin/python3
import socket
from sys import *

HOST, PORT = "localhost",9090
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(bytes(str(10),"utf-8"), (HOST, PORT))

