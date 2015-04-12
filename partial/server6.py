# HTTP fuckserver
import socket
import sys

# Symbolic name meaning all available interfaces
HOST = ''
# HTTP port
PORT = 1234

s = None
s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)

while 1:
    conn, addr = s.accept()
    print 'Connected by', addr
    data = conn.recv(1024)
    print data
    conn.send("HTTP/1.1 200 OK\nConnection: keep-alive\nServer: Python/2.7.2\nAccept-Ranges: bytes\nContent-Type: text/html\nContent-Length: 4\nLast-Modified: Tue, 31 March 2015 13:00:05 GMT\n\nfuck\n")
conn.close()

