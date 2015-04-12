# HTTP fuckserver
import socket
import sys

HOST = ''               # Symbolic name meaning all available interfaces
PORT = 80              # HTTP port
s = None
s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
print "lol"
s.bind((HOST, PORT))
print "lol"
s.listen(1)
print "lol"

while 1:
	conn, addr = s.accept()
	print 'Connected by', addr
	data = conn.recv(1024)
	print data
	conn.send("HTTP/1.1 200 OK\nConnection: keep-alive\nServer: Python/2.7.2\nAccept-Ranges: bytes\nContent-Type: text/html\nContent-Length: 4\nLast-Modified: Tue, 31 March 2015 13:00:05 GMT\n\nfuck\n")

conn.close()

