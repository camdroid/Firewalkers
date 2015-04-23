# python
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

from scapy.all import *
import sys, time, random

"""
This client sends fragmented packets with data on one side on the fragment!
"""

class PacketEngine:
    def __init__(self, dport):
        self.seq = random.randint(50,1000)
        self.ack = 0 
        self.dport = int(dport)
        self.sport = random.randint(5000,10000)
        self.destIP = '45.55.173.246'
        self.srcIP = '116.255.165.42'

    def handshake(self, payload, resetList):
        print '[START HANDSHAKE]'
        ip = IP(src=self.srcIP, dst=self.destIP)
        syn = ip/TCP(sport=self.sport, dport=self.dport, flags="S", seq=self.seq)
        print '[SYN] Sending, seq=' + str(self.seq)
        synack = sr1(syn)

        try:
            print '[SYNACK] Received, sport=' + str(synack.sport) + ', seq=' + str(synack.ack) + ', ack=' + str(synack.seq)
            ack = ip/TCP(sport=self.sport, dport=self.dport, flags="A", seq=synack.ack, ack=synack.seq+1)
            send(ack)
            print '[ACK] Sent, seq=' + str(synack.ack) + ', ack=' + str(synack.seq+1)

            self.seq = synack.ack
            self.ack = synack.seq+1
            print '[END HANDSHAKE]'
        except:
            resetList.write("[HANDSHAKE EXCEPTION] " + payload + "failed\n")
            print '[HANDSHAKE EXCEPTION] ' + payload + 'failed'
            self.fin()
            return False
        return True

    def sendKeyword(self, payload, resetList):
        ip = IP(src=self.srcIP, dst=self.destIP)
        tcp = TCP(sport=self.sport, dport=self.dport, flags="PA", seq=self.seq, ack=self.ack)
        request = Raw("GET /?q=" + payload + "\n\n")

        print '[IPv6] Sending ' + payload + ', seq=' + str(self.seq) + ', ack=' + str(self.ack)
        ans,unas = sr(ip/tcp/request, inter=0.5, retry=-2, timeout=1)

        try:
            for p in ans[0]:
                if(p[0][1].flags & 4):
                    resetList.write(payload + "\n")
                    print "RESET PACKET!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
                if(p[0][1].flags & 16):
                    self.seq = p[0][0].ack
                    self.ack = p[0][0].seq
        except:
            print "[EXCEPTION] SR didn't finish"
            self.sendKeyword(payload, resetList)

    def fin(self):
        ip = IP(src=self.srcIP, dst=self.destIP)
        tcp = TCP(sport=self.sport, dport=self.dport, flags="RA", seq=self.seq, ack=self.ack);
        send(ip/tcp)

if __name__ == '__main__':
    if(len(sys.argv) <= 1):
        print "Destination Port Required"
        sys.exit(0)

    port = sys.argv[1]
    censorfile = open(sys.argv[2], 'r')
    resetList = open('reset4.txt', 'w')

    packetEngine = PacketEngine(port)

    for word in censorfile:
        payload = word.strip()
        if (packetEngine.handshake(payload, resetList)):
            packetEngine.sendKeyword(payload, resetList)
            packetEngine.fin()
        time.sleep(random.uniform(.5, 1))

    resetList.close()
