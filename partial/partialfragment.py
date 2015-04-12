# python
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

from scapy.all import *
import sys

"""
This client sends fragmented packets with data on one side on the fragment!
"""

class PacketEngine:
    def __init__(self, dport):
        self.seq = 100
        self.ack = 0 
        self.dport = int(dport)
        self.sport = 5555
        self.destIP = '2604:a880:800:10::7df:6001'
        self.srcIP = '2601:4:f01:67d2:9eae:8fd9:46c:6fc3'

    def handshake(self):
        ip = IPv6(src=self.srcIP, dst=self.destIP)
        syn = ip/TCP(sport=self.sport, dport=self.dport, flags="S", seq=self.seq)
        print '[SYN] Sending, seq=' + str(self.seq)
        synack = sr1(syn)
        print '[SYNACK] Received, sport=' + str(synack.sport) + ', seq=' + str(synack.ack) + ', ack=' + str(synack.seq)

        ack = ip/TCP(sport=self.sport, dport=self.dport, flags="A", seq=synack.ack, ack=synack.seq+1)
        send(ack)
        print '[ACK] Sent, seq=' + str(synack.ack+1) + ', ack=' + str(synack.seq+1)

        self.seq = synack.ack
        self.ack = synack.seq+1

    def sendPacket(self, payload):
        ip = IPv6(src=self.srcIP, dst=self.destIP)
        extension = IPv6ExtHdrHopByHop()

        tcp = TCP(sport=self.sport, dport=self.dport, flags="PA", seq=self.seq, ack=self.ack)
        send(ip/tcp/payload)
        print '[IPv6] Sent, seq=' + str(self.seq) + ', ack=' + str(self.ack)

    def sendFragmentedPackets(self, payload1, payload2):
        ip = IPv6(src=self.srcIP, dst=self.destIP, plen=16)
        frag1 = IPv6ExtHdrFragment(offset=0, m=1 ,id=502, nh=58)
        frag2 = IPv6ExtHdrFragment(offset=1, m=1 ,id=502, nh=58)
        packet1 = ip/frag1/payload1
        packet2 = ip/frag2/payload2
        send(packet1)
        send(packet2)

    # doesn't work
    def fin(self):
        ip = IPv6(src=self.srcIP, dst=self.destIP)
        fin = ip/TCP(sport=self.sport, dport=self.dport, flags="F", seq=self.seq, ack=self.ack)
        print '[FINACK] Sending, seq=' + str(self.seq) + ', ack=' + str(self.ack)
        finack = sr1(finack)
        print '[ACK] Received, flags=' + str(finack.flags) + ', seq=' + str(finack.seq) + ', ack=' + str(finack.ack)

        fin2 = ip/TCP(sport=self.sport, dport=self.dport, flags="a", seq=finack.ack+1, ack=finack.seq+1)
        send(fin2)
        print '[FIN2] Sent, seq=' + str(finack.ack+1) + ', ack=' + str(finack.seq+1)

if __name__ == '__main__':
    if(len(sys.argv) <= 1):
        print "Destination Port Required"
        sys.exit(0)

    payload1 = Raw("AABBCCDD")
    payload2 = Raw("EEFFGGHH")

    packetEngine = PacketEngine(sys.argv[1])
    packetEngine.handshake()
    #packetEngine.sendPacket(payload1)
    packetEngine.sendFragmentedPackets(payload1, payload2)
