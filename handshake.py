#!/usr/bin/python
from scapy.all import *

if (len(sys.argv) == 5):
	dip = sys.argv[2]
	sip = sys.argv[1]
	length = int(sys.argv[3])
	myoffset = int(sys.argv[4])

	src_addr=""
	dst_addr=""
	sport=""
	dport=""
else:
	print """it takes four arguments (in the following order): 
	the source IPv6 address, the destination IPv6 address, 
	the length of the fragments (in octets) 
	and the offset of the second fragment (in octets too)"""
	sys.exit(1)

ip=IPv6(src="10.1.2.3", dst="10.2.3.4")
SYN=TCP(sport=1050, dport=80, flags="S", seq=100)
SYNACK=sr1(ip/SYN)

my_ack = SYNACK.seq + 1
ACK=TCP(sport=1050, dport=80, flags="A", seq=101, ack=my+ack)
send(ip/ACK)

payload="stuff"
PUSH=TCP(sport=1050, dport=80, flags="PA", seq=11, ack=my_ack)
send(ip/PUSH/payload)

#stuff from the blackhat paper


myid=random.randrange(1,B94967296,1) #generate a random fragmentation id
payload1=Raw("AABBCCDD"*(length-1))
payload2=Raw("BBDDAACC"*length)
payload=str(Raw("AABBCCDD"*(length+myoffset-1)))
icmpv6=ICMPv6EchoRequest(data=payload)
ipv6_1=IPv6(src=sip, dst=dip, plen=(length+myoffset)*8)
csum=in6_chksum(58, ipv6_1/icmpv6, str(icmpv6))
print 8*(length+1)
ipv6_1=IPv6(src=sip, dst=dip, plen=8*(length+1)) #plus 1 for the length of the Fragment Extension header
icmpv6=ICMPv6EchoRequest(cksum=csum, data=payload1)
frag1=IPv6ExtHdrFragment(offset=0, m=1, id=myid, nh=58)
frag2=IPv6ExtHdrFragment(offset=myoffset, m=0, id=myid, nh=58)
packet1=ipv6_1/frag1/icmpv6
packet2=ipv6_1/frag2/payload2
send(packet1)
send(packet2) 