from scapy.all import *

dip = "10.3.8.239"

payload1 = "AABBAABB"
payload2 = "BBAABBAA"
payload3 = "CCCCCCCC"

ip = IPv6(dst=dip, id=12345, flags=1)
icmp = ICMP(type=8, code=0, chksum=0xe3eb)
packet = ip/icmp/payload1
packet.show2()
send(packet)

ip = IP(dst=dip, id=12345, flags=1, frag=1)
packet = ip/payload2
packet.show2()
send(packet)

ip = IP(dst=dip, id=12345, flags=1, frag=1)
packet = ip/payload3
packet.show2()
send(packet)