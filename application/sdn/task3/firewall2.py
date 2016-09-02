from pox.core import core
from pox.forwarding.l2_learning import LearningSwitch
import pox.openflow.libopenflow_01 as of
import pox.lib.packet as pkt
from firewall import Firewall

log = core.getLogger()

class Firewall2(Firewall):

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
					log.debug('\n traffic go out from private zone, flow install')
					super(Firewall2,self)._handle_PacketIn(event)

				else:

					log.debug('\n traffic go to private zone, forbidden')
					super(Firewall2,self).drop(event)

			else:

				log.debug('\n non IP traffic no restriction')

				super(Firewall2,self)._handle_PacketIn(event)






