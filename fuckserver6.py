# HTTP fuckserver
import socket
import sys

HOST = None               # Symbolic name meaning all available interfaces
PORT = 80              # HTTP port
s = None
for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC,
                              socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
    af, socktype, proto, canonname, sa = res
    try:
        s = socket.socket(af, socktype, proto)
    except socket.error as msg:
        s = None
        continue
    try:
        s.bind(sa)
        s.listen(1)
    except socket.error as msg:
        s.close()
        s = None
        continue
    break
if s is None:
    print 'could not open socket'
    sys.exit(1)
conn, addr = s.accept()
print 'Connected by', addr
while 1:
    data = conn.recv(1024)
    if not data: break
    conn.send("HTTP/1.1 200 OK\nConnection: keep-alive\nServer: Python/2.7.2\nAccept-Ranges: bytes\nContent-Type: text/html\nContent-Length: 4\nLast-Modified: Tue, 31 March 2015 13:00:05 GMT\n\nfuck\n")
conn.close()