
from pox.core import core
from pox.forwarding.l2_learning import LearningSwitch
import pox.openflow.libopenflow_01 as of
import pox.lib.packet as pkt
from firewall import Firewall

log = core.getLogger()

class Firewall1(Firewall):

		def __init__ (self, connection):
			Firewall.__init__(self,connection)
		#self.drop()

		def _handle_PacketIn(self,event):

			packet = event.parsed

			if not packet.parsed:
				log.warning("Ignoring imcomplete packet")
				return

			if packet.type == pkt.ethernet.IP_TYPE:
				ip_packet = packet.payload
				ipv4_packet = ip_packet.find('ipv4')
				proto = ip_packet.protocol
				srcIP = ipv4_packet.srcip
				dstIP = ipv4_packet.dstip

				if event.port == 2:
					log.debug('\n traffic go to public zone, flow install')
					super(Firewall1,self)._handle_PacketIn(event)

				elif event.port == 1:

					log.debug('\n traffic leave public zone')

					if proto ==pkt.ipv4.TCP_PROTOCOL and ip_packet.next.dstport == 80 :
						log.debug('\n only install dstport 80 tcp traffic')
						super(Firewall1,self)._handle_PacketIn(event)

					elif proto == pkt.ipv4.UDP_PROTOCOL and ip_packet.next.dstport == 53:
						super(Firewall1,self)._handle_PacketIn(event)


					elif proto == pkt.ipv4.ICMP_PROTOCOL:
						if dstIP == '100.0.0.25' or dstIP == '100.0.0.45':
							super(Firewall1,self)._handle_PacketIn(event)
						else:
							super(Firewall1,self).drop(event)
					

					else:
						log.debug('\n')
						super(Firewall1,self).drop(event)


				else:
					log.debug('\n unrecognized port number')
					super(Firewall1,self).drop(event)

			else:
				log.debug('\n non IP traffic no restriction')

				super(Firewall1,self)._handle_PacketIn(event)





















