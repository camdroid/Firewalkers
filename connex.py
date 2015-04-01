

from scapy.all import *
from scapy_http.http import HTTPRequest, HTTP

def hitUp(server="115.159.1.117", port= 80):	
	sock = socket.socket()
	sock.connect((server, port))
	ssock=StreamSocket(sock)
	return ssock

#ss=IP(dst="192.168.1.38")/TCP(dport=8000)/"Get fucked"
if __name__ == '__main__':
	ssock=hitUp()
	h=HTTPRequest(Method="POST", Path="/", Host= 'dingus.cn', Accept='*/*', Connection = 'Keep-Alive')
	h.setfieldval('User-Agent', 'Python/2.7.6')
	h.setfieldval('Http-Version', 'HTTP/1.1')
	H=HTTP()/h/Raw('action=WriteShit&message=\xe4\xb9\xa0\xe8\xbf\x91\xe5\xb9\xb3\xe7\x9a\x84\xe9\x80\x89\xe6\x8b\xa9') #习近平的选择

	ssock.send(H)

	ssock.close()

def splitUp(server="115.159.1.117", port= 80):
	ip=IP(dst=server)
	tcp=TCP(dport=80)
	h=HTTPRequest(Method="POST", Path="/", Host= 'www.github.com', Accept='*/*', Connection = 'Keep-Alive')
	h.setfieldval('User-Agent', 'Python/2.7.6')
	h.setfieldval('Http-Version', 'HTTP/1.1')
	http=HTTP()/h
	pack=ip/tcp/http/Raw("action=WriteShit&message='"+"dingus "*16+"'") 
	pack.show()
	frags=fragment(pack, 16)
	for frag in frags:
		frag.show()
