#scapy tcp handshake code.

from scapy.all import *

sock = socket.socket()
sock.connect(("192.168.1.38", 8000))
ssock=StreamSocket(sock)

scapy=IP(dst="192.168.1.38")/TCP(dport=8000)/"Get dunked"
ssock.send("Some Data")