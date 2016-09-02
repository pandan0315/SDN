from scapy.all import *

queryName = "dnstest"

def DNS_Responder(localIP):
    def getResponse(pkt):
        if (DNS in pkt and pkt[IP].src != localIP \
            and pkt[DNS].opcode == 0L and pkt[DNS].ancount == 0):

            if queryName in pkt['DNS Question Record'].qname:
                spfResp = \
                    IP(dst=pkt[IP].src, src=pkt[IP].dst) \
                    /UDP(dport=pkt[UDP].sport, sport=pkt[UDP].dport) \
                    /DNS(id=pkt[DNS].id, qd=pkt[DNS].qd, aa = 1, qr=1, \
                    an=DNSRR(rrname=pkt[DNS].qd.qname, ttl=20, rdata="100.0.0.88"))

                    # aa =1  we are authoritative
                    # qr = 1 it is a response
                    # qd = pkt[DNS].qd copy question itself

                send(spfResp, verbose=0)
                return "DNS Response Sent"
        return False

    return getResponse

if __name__ == '__main__':
    DNSServerIP = "100.0.0.20"

    args = sys.argv[1:]

    if len(args) == 1:
        DNSServerIP = args[0]
    else:
        print "Invalid amount of args. Usage: dns_response.py [DNS Server local IP]"
        sys.exit()

    filter = "udp port 53 and ip dst " + DNSServerIP + " and not ip src " + DNSServerIP
    sniff(filter=filter, prn=DNS_Responder(DNSServerIP))