

from scapy.all import *
from scapy_http.http import HTTPRequest, HTTP

def hitUp(server="2601:4:f01:67d2:dca7:5169:52f5:71a", port= 80):	
	sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
	sock.connect((server, port))
	ssock=StreamSocket(sock)
	#h=HTTPRequest(Method="GET", Path="/?falun")
	#h.setfieldval('User-Agent', 'Python/2.7.6')
	#h.setfieldval('Http-Version', 'HTTP/1.1')
	#H=HTTP()/h#/Raw('action=WriteShit&message=\xe4\xb9\xa0\xe8\xbf\x91\xe5\xb9\xb3\xe7\x9a\x84\xe9\x80\x89\xe6\x8b\xa9') 
	return ssock

if __name__ == '__main__':
	ssock= hitUp()
	print "Sendin Sum Packetz: Jake Debolt 2015"
	with open('censorship.txt', 'r') as censorfile:
		for line in censorfile:
			packetText="GET /?"+line+"\n"
			print packetText+"\n............-----------.............."
			ssock.send(packetText)
			resp=ssock.recv(1024)
			print resp
			print "_________________________________________"

#	with open('censorship.txt', 'r') as censorf:
#		ptext=""
#		for line in censorf:
#			ptext+=line[0:len(line)-1]+"+"
#		ptext+="12\n\n"
#		print ptext
#		ssock.send(ptext)
#		print ssock.recv(65535)

	#ssock.send("GET /?\xe4\xb9\xa0\xe8\xbf\x91\xe5\xb9\xb3\xe7\x9a\x84\xe9\x80\x89\xe6\x8b\xa9 HTTP/1.0\n\n")
	print "\n"
#	ssock.send("GET /?q=vpn.*\xe5\x85\x8d\xe8\xb4\xb9\n\n")
#	print ssock.recv(1024)
#	ssock.send("GET /?q=\xe8\x8b\x8f\xe7\xbb\x8d\xe6\x99\xba\x20\x0a\n\n") 
#	print ssock.recv(1024)
	ssock.send("GET /?q=hi\n\n")
	ssock.recv(1024)
	ssock.send("GET /?q=done\n\n")
	ssock.recv(1024)
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
