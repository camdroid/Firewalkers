from scapy.all import *

"""
This client sends fragmented packets with data on one side on the fragment!
"""

# EC2 Server IP
# serverIP = "54.149.134.250"
destIP = 'fe80::d328:22c0:2f25:3d69'
# destIP = '::1'
srcIP = 'fe80::dead:beef'
payload = 'hello'

def constructPacket():
    base = IPv6()
    base.dst = destIP
    base.src = srcIP
    extension = IPv6ExtHdrHopByHop()

    #jumbo = Jumbo()
    #jumbo.jumboplen = 2++30
    #extension.options = jumbo

    # return base/extension/payload

    packet = base/IPv6ExtHdrDestOpt()/IPv6ExtHdrRouting()/IPv6ExtHdrHopByHop()
    return packet

if __name__ == '__main__':
    packet = constructPacket()
    packet.show2()
    send(packet) 
