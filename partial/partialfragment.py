from scapy.all import *

"""
This client sends fragmented packets with data on one side on the fragment!
"""

payload = 'hello'

def handshake():
    ip = IPv6(src=srcIP, dst=destIP)
    syn = TCP(sport=sport, dport=dport, flags="S", seq=100)
    synack = sr1(ip/syn)

    my_ack = synack.seq + 1
    ack = TCP(sport=sport, dport=dport, flags="A", seq=101, ack=my_ack)
    send(ip/ack)

def constructPacket():
    base = IPv6(src=srcIP, dst=destIP)
    extension = IPv6ExtHdrHopByHop()

    #jumbo = Jumbo()
    #jumbo.jumboplen = 2**30
    #extension.options = jumbo

    #packet = base/IPv6ExtHdrDestOpt()/IPv6ExtHdrRouting()/IPv6ExtHdrHopByHop()
    return base/extension/payload

if __name__ == '__main__':
    handshake()
    packet = constructPacket()
    packet.show2()
    send(packet) 
    #response = sr1(packet)
    #print response
