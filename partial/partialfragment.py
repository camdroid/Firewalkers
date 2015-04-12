from scapy.all import *

"""
This client sends fragmented packets with data on one side on the fragment!
"""

# DigitalOcean IPv6 Adress
destIP = '2604:a880:800:10::7df:6001'
srcIP = 'fe80::dead:beef'
payload = 'hello'

def constructPacket():
    base = IPv6(src=srcIP, dst=destIP)
    extension = IPv6ExtHdrHopByHop()

    jumbo = Jumbo()
    jumbo.jumboplen = 2**30
    extension.options = jumbo

    #packet = base/IPv6ExtHdrDestOpt()/IPv6ExtHdrRouting()/IPv6ExtHdrHopByHop()
    return base/extension/payload


if __name__ == '__main__':
    packet = constructPacket()
    packet.show2()
    send(packet) 
