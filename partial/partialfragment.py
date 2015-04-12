from scapy.all import *

"""
This client sends fragmented packets with data on one side on the fragment!
"""

class PacketEngine:
    def __init__(self):
        self.seq = 100
        self.ackNum = 0
        self.dport = 80
        self.sport = 1234
        self.destIP = ''
        self.srcIP = ''

    def handshake(self):
        ip = IPv6(src=self.srcIP, dst=self.destIP)
        syn = TCP(sport=self.sport, dport=self.dport, flags="S", seq=self.seq)
        synack = sr1(ip/syn)
        self.seq += 1

        self.ackNum = synack.seq + 1
        ack = TCP(sport=self.sport, dport=self.dport, flags="A", seq=self.seq, ack=self.ackNum)
        send(ip/ack)
        self.seq += 1

    def sendPacket(self, payload):
        ip = IPv6(src=self.srcIP, dst=self.destIP)
        extension = IPv6ExtHdrHopByHop()

        tcp = TCP(sport=self.sport, dport=self.dport, flags="PA", seq=self.seq, ack=self.ackNum)
        self.seq += 1

        #jumbo = Jumbo()
        #jumbo.jumboplen = 2**30
        #extension.options = jumbo
        #packet = base/IPv6ExtHdrDestOpt()/IPv6ExtHdrRouting()/IPv6ExtHdrHopByHop()

        response = sr1(ip/extension/tcp/packet)
        self.ackNum = response.ackNum
        print response
        self.fin()

    def fin(self):
        ip = IPv6(src=self.srcIP, dst=self.destIP)
        tcp = TCP(sport=self.sport, dport=self.dport, flags="A", seq=ackNum+10, ack=ackNum)
        send(ip/tcp)

if __name__ == '__main__':
    packetEngine = PacketEngine()
    packetEngine.handshake()
#    packetEngine.sendPacket("hello")
