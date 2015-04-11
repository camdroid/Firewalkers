from scapy.all import *

"""
This client sends fragmented packets with data on one side on the fragment!
"""

# EC2 Server IP
# serverIP = "54.149.134.250"
destIP = 'fe80::82e6:50ff:fe1b:93c2'
srcIP = 'fe80::dead:beef'
payload = 'hello'

def constructPacket():
    base = IPv6(src=srcIP, dst=destIP)
    extension = IPv6ExtHdrHopByHop()

    jumbo = Jumbo()
    jumbo.jumboplen = 2++30
    extension.options = jumbo

    #packet = base/IPv6ExtHdrDestOpt()/IPv6ExtHdrRouting()/IPv6ExtHdrHopByHop()
    return base/extension/payload


if __name__ == '__main__':
    packet = constructPacket()
    #packet.show2()
    send(packet) 
