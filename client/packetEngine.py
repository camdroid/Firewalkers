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
        self.srcIP = '2400:a480:f:190:a5::2a'

    def handshake(self):
        print '[START HANDSHAKE]'
        ip = IPv6(src=self.srcIP, dst=self.destIP)
        syn = ip/TCP(sport=self.sport, dport=self.dport, flags="S", seq=self.seq)
        print '[SYN] Sending, seq=' + str(self.seq)
        synack = sr1(syn)
        print '[SYNACK] Received, sport=' + str(synack.sport) + ', seq=' + str(synack.ack) + ', ack=' + str(synack.seq)

        ack = ip/TCP(sport=self.sport, dport=self.dport, flags="A", seq=synack.ack, ack=synack.seq+1)
        send(ack)
        print '[ACK] Sent, seq=' + str(synack.ack) + ', ack=' + str(synack.seq+1)

        self.seq = synack.ack
        self.ack = synack.seq+1
        print '[END HANDSHAKE]'

    def sendPacket(self, payload):
        ip = IPv6(src=self.srcIP, dst=self.destIP)
        extension = IPv6ExtHdrHopByHop()

        tcp = TCP(sport=self.sport, dport=self.dport, flags="PA", seq=self.seq, ack=self.ack)
        sr1(ip/tcp/payload)
        print '[IPv6] Sent, seq=' + str(self.seq) + ', ack=' + str(self.ack)
        self.seq += len(payload)

    def recvPacket(self):
        lf=lambda (r): TCP in r and r[TCP].port==self.dport and r[IPv6].src == self.destIP
        ip = IPv6(src=self.srcIP, dst=self.destIP)
        pack=sniff(count=1, lfilter=lf)[0]
        data=str(pack[Raw])
        self.ack+=len(data)
        ack=TCP(sport=self.sport, dport=self.dport, flags="A", seq=self.seq, ack=self.ack)
        send(ip/ack)
        return data

    def traceroute(self, payload):
        print '[START TRACEROUTE]'
        ip = IPv6(src=self.srcIP, dst=self.destIP, hlim=(1,18))
        tcp = TCP(sport=self.sport, dport=self.dport, flags="PA", seq=self.seq, ack=self.ack)
        ans,unans=sr(ip/tcp/payload)

        for snd,rcv in ans:
            print snd.hlim, rcv.src, isinstance(rcv.payload, TCP)
        print '[END TRACEROUTE]'

    def sendFragmentedPackets(self, payload1, payload2):
        ip = IPv6(src=self.srcIP, dst=self.destIP, plen=16)
        frag1 = IPv6ExtHdrFragment(offset=0, m=1 ,id=502, nh=58)
        frag2 = IPv6ExtHdrFragment(offset=1, m=1 ,id=502, nh=58)
        packet1 = ip/frag1/payload1
        packet2 = ip/frag2/payload2
        send(packet1)
        send(packet2)

    def fragmentNormal(self, payload, octets=160, ident=133876465):
        ip=IPv6(src=self.srcIP, dst=self.destIP)
        tcp = TCP(sport=self.sport, dport=self.dport, flags="PA", seq=self.seq, ack=self.ack)
        fragpt=str(ip/tcp/payload)[40:]
        rem=fragpt
        for off in range(0, len(fragpt), octets*8):
            m=1
            if (off+octets*8) > len(fragpt):
                m=0
            print off/8
            fraghead=IPv6ExtHdrFragment(offset=(off/8), m=m, id=ident, nh=6)
            load=fragpt[off:min(off+(octets*8), len(fragpt))]
            pack=ip/fraghead/load
            send(pack)

    def fragmentSmallMTU(self, payload, octets=1, ident=133706465):
        ip=IPv6(src=self.srcIP, dst=self.destIP)
        tcp = TCP(sport=self.sport, dport=self.dport, flags="PA", seq=self.seq, ack=self.ack)
        fragpt=str(ip/tcp/payload)[40:]
        rem=fragpt
        for off in range(0, len(fragpt), octets*8):
            m=1
            if (off+octets*8) > len(fragpt):
                m=0
            print off/8
            fraghead=IPv6ExtHdrFragment(offset=(off/8), m=m, id=ident, nh=6)
            load=fragpt[off:min(off+(octets*8), len(fragpt))]
            pack=ip/fraghead/load
            send(pack)
            if off==0: send(pack)

        print '[IPv6] Sent, seq=' + str(self.seq) + ', ack=' + str(self.ack)

    def fragmentTotalOverlap(self, payload, targets, octets=3, originalFirst=True):
        targets=set(targets)
        ip=IPv6(src=self.srcIP, dst=self.destIP)
        tcp = TCP(sport=self.sport, dport=self.dport, flags="PA", seq=self.seq, ack=self.ack)
        fragpt=str(ip/tcp/payload)[40:]
        rem=fragpt
        for off in range(0, len(fragpt), octets*8):
            m=1
            if (off+octets*8) > len(fragpt):
                m=0
            print off/8
            fraghead=IPv6ExtHdrFragment(offset=(off/8), m=m, id=ident, nh=6)
            if off/8 in targets and not originalFirst:
                send(ip/fraghead/Raw("CENSORED"*octets))
            load=fragpt[off:min(off+(octets*8), len(fragpt))]
            pack=ip/fraghead/load
            send(pack)
            if off/8 in targets and originalFirst:
                send(ip/fraghead/Raw("CENSORED"*octets))
            
    def fragmentPartialOverlap():
        pass

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

    #censoredPayload = Raw('GET /?q=vpn.*\xe5\x85\x8d\xe8\xb4\xb9\n\n') 
    benignPayload = Raw("GET /?q=poopypants")
    bigCensored=Raw("GET /?q="+"lol+"*300+"vpn.*\xe5\x85\x8d\xe8\xb4\xb9+"+"hoh+"*5+"done\n\n")

    packetEngine = PacketEngine(sys.argv[1])
    packetEngine.handshake()
    packetEngine.fragmentSmallMTU(benignPayload)
    #packetEngine.traceroute(payload1)
