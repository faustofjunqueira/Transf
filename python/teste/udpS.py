#!/usr/bin/python3
import socketserver
import sys

f = open("copiado.jpg","wb")

class MyUDPHandler(socketserver.BaseRequestHandler):
    """
    This class works similar to the TCP handler class, except that
    self.request consists of a pair of data and client socket, and since
    there is no connection the client address must be given explicitly
    when sending data back via sendto().
    """    
    def handle(self):        
        
        data = self.request[0]
        print(data.decode())
        if  data != bytes("save","utf-8"):
            f.write(data)
        else:
            print("Arquivo fechado")
            f.close()            

        socket = self.request[1]
        socket.sendto(bytes("OK","utf-8"), self.client_address)


if __name__ == "__main__":
    HOST, PORT = "localhost", 9090
    server = socketserver.UDPServer((HOST, PORT), MyUDPHandler)
    server.serve_forever()