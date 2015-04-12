# HTTP fuckserver
import socket
import sys

payload = "HTTP/1.1 200 OK\nConnection: keep-alive\nServer: Python/2.7.2\nAccept-Ranges: bytes\nContent-Type: text/html\nContent-Length: 4\nLast-Modified: Tue, 31 March 2015 13:00:05 GMT\n\nfuck\n"

if __name__ == '__main__':
    if(len(sys.argv) <= 1):
        print "Destination Port Required"
        sys.exit(0)

    sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    sock.bind(("", int(sys.argv[1])))
    sock.listen(1)

    while 1:
        conn, addr = sock.accept()
        print 'Connected by', addr
        data = conn.recv(1024)
        print data
        # conn.send(payload)
    conn.close()


