


from pox.core import core
from pox.forwarding.l2_learning import LearningSwitch
import pox.openflow.libopenflow_01 as of
import pox.lib.packet as pkt


log = core.getLogger()

class Firewall(LearningSwitch):

	def __init__ (self, connection):
		#initial rule
		LearningSwitch.__init__(self, connection, False)
		#self.drop()


	def _handle_PacketIn(self,event):

		#handles packet in firewall

		packet = event.parsed
		if not packet.parsed:
			log.warning("Ignoring incmplete packet")
			return
		inport = event.port

		if packet.type == pkt.ethernet.IP_TYPE:
			# allow IP traffic from prz to pbz
			
			if inport == 2: 
				log.debug('\n The packet in port is: '+str(inport)+'\n')
				ip_packet = packet.payload
				ipv4_packet = ip_packet.find('ipv4')
				proto = ip_packet.protocol
				srcIP = ipv4_packet.srcip
				dstIP = ipv4_packet.dstip
				log.debug('\n source ip is: '+str(srcIP)+'\n')
				log.debug('\n destination ip is: '+str(dstIP)+'\n')

				if proto == pkt.ipv4.ICMP_PROTOCOL:
					log.debug('\n install a ICMP forward flow from prz to pbz'+'\n')
					self.installRule(srcIP,dstIP,2,1,proto,pkt.ICMP.TYPE_ECHO_REQUEST,None)
					log.debug('\n install a ICMP reverse flow from pbz to prz'+'\n')
					self.installRule(dstIP,srcIP,1,2,proto,pkt.ICMP.TYPE_ECHO_REPLY,None)
					

				elif (proto == pkt.ipv4.TCP_PROTOCOL) or (proto == pkt.ipv4.UDP_PROTOCOL):
					
					log.debug('\n install a TCP/UDP forward flow from prz to pbz'+'\n')
					self.installRule(srcIP,dstIP,2,1,proto,ip_packet.next.srcport,ip_packet.next.dstport)
					log.debug('\n install a TCP/UDP reverse flow from prz to pbz'+'\n')
					self.installRule(dstIP,srcIP,1,2,proto,ip_packet.next.dstport,ip_packet.next.srcport)

				else:
					log.debug('\n do not process other protocol')
				super(Firewall,self)._handle_PacketIn(event)


			elif inport == 1:
				log.debug('\n The packet in port is: '+str(inport)+'\n')
				log.debug('\n Block IP traffic from PBZ to PRZ')
				self.drop()

			else:
				log.debug('\n unknown incoming port arriving at Firewall')
				self.drop()
	
		    # all non IP traffic apply the LearningSwitch model
		else:
			log.debug('\n non IP traffic can go through both direction in the firewall')
			log.debug('\nThe packet type is: ' + str(packet.type)+'\n')
			super(Firewall,self)._handle_PacketIn(event)

	def drop(self):
		msg = of.ofp_flow_mod()
		#msg.match = of.ofp_match.from_packet(packet)
		msg.match.dl_type = pkt.ethernet.IP_TYPE
		msg.match.in_port = 1
		msg.priority = 10	
		self.connection.send(msg)

	def installRule(self,nw_src,nw_dst,incoming_port,outport,proto,tp_src,tp_dsc):
		msg = of.ofp_flow_mod()
		msg.match = of.ofp_match()      	
		msg.match.dl_type = pkt.ethernet.IP_TYPE
		msg.match.nw_proto = proto				
		msg.match.in_port = incoming_port
		msg.match.nw_src = nw_src
		msg.match.nw_dst = nw_dst
		msg.match.tp_src = tp_src
		msg.match.tp_dsc = tp_dsc
		msg.priority = 1000
		msg.actions.append(of.ofp_action_output(port = outport))
		self.connection.send(msg)

	
		





