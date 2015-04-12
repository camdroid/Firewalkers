from scapy.all import *

if (len(sys.argv) == 4):
    dip = sys.argv[2]
    sip = sys.argv[1]
    sport = int(sys.argv[3])
    dport = int(sys.argv[4])
else:
    print """it takes four arguments (in the following order): 
    the source IPv6 address, the destination IPv6 address, 
    the length of the fragments (in octets) 
    and the offset of the second fragment (in octets too)"""
    sys.exit(1)

handshake=False

payload="GET /?q=fuck HTTP/1.0\n\n"
PUSH=TCP(sport=sport, dport=dport, flags="PA", seq=101, ack=my_ack)/payload
fragpt=str(ip/PUSH)[40:]
size=1
frags=[]
finpt=""

for off in range(0,len(fragpt),size*8):
    ext=IPv6ExtHdrFragment(m=1, id=12343, nh=6, offset=off/8)
    pack=ip/ext/fragpt[offset:offset+(size*8)]
    frags.append(pack)
    finpt=fragpt[offset+(size*8):]

frags.append(ip/IPv6ExtHdrFragment(m=0, id=12343, nh=6, offset=len(fragpt)/8)/finpt)

#send(ip/PUSH/payload)

#handshake
if handshake:
	ip=IPv6(src=sip, dst=dip)
	SYN=TCP(sport=sport, dport=dport, flags="S", seq=100)
	SYNACK=sr1(ip/SYN)

	my_ack = SYNACK.seq + 1
	ACK=TCP(sport=sport, dport=dport, flags="A", seq=101, ack=my_ack)
	send(ip/ACK)
