from pox.core import core
from pox.lib.util import dpid_to_str
from pox.forwarding.l2_learning import LearningSwitch
from firewall import Firewall

log = core.getLogger()

class Task2_Controller(object):
	def __init__(self):
		core.openflow.addListeners(self)


	def _handle_ConnectionUp(self,event):

		dpid = event.dpid

		#log.debug("Switch %s has come up.", dpid_to_str(dpid))
		#LearningSwitch(event.connection,False)



        # switch sw1 and sw3 are regular learning switch
		if dpid == 1 or dpid ==3:
			log.debug("Switch %s has come up.", dpid_to_str(dpid))
			LearningSwitch(event.connection,False)

		# firewall 
		
		elif dpid == 6:
		
			log.debug("Firewall %s has come up.", dpid_to_str(dpid))
			Firewall(event.connection)
	

	def _handle_ConnectionDown(self,event):

		log.info("Connection from %s has shutdown.",dpid_to_str(event.dpid))


def launch():

	controller = Task2_Controller()
	core.register("controller", controller)