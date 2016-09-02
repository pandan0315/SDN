from pox.core import core
from pox.lib.util import dpid_to_str
from pox.forwarding.l2_learning import LearningSwitch

from firewall1 import Firewall1
from firewall2 import Firewall2
import os


log = core.getLogger()

class Controller(object):
	def __init__(self):
		core.openflow.addListeners(self)


	def _handle_ConnectionUp(self,event):

		dpid = event.dpid
		#LearningSwitch(event.connection,False)

		#log.debug("Switch %s has come up.", dpid_to_str(dpid))
		#LearningSwitch(event.connection,False)

		if dpid == 9:
			log.debug("Switch %s has come up." % (dpid_to_str(dpid)))
			os.system('sudo /usr/local/bin/click nfv/task3/lb2.click &')
			#LearningSwitch(event.connection,False)

		elif dpid ==8:
			log.debug("Switch %s has come up.", dpid_to_str(dpid))
			os.system('sudo /usr/local/bin/click nfv/task3/lb1.click &')

		elif dpid == 11:
			log.debug("Switch %s has come up.", dpid_to_str(dpid))
			os.system('sudo /usr/local/bin/click nfv/task3/napt.click &')

		elif dpid == 6:
			log.debug("Switch %s has come up.", dpid_to_str(dpid))
			Firewall1(event.connection)

		
		elif dpid == 7:
			log.debug("Switch %s has come up.", dpid_to_str(dpid))
			Firewall2(event.connection)

		elif dpid == 10:
			log.debug("Switch %s has come up.", dpid_to_str(dpid))
			os.system('sudo /usr/local/bin/click nfv/task3/ids.click &')


			

		else :
			log.debug("Switch %s has come up.", dpid_to_str(dpid))
			LearningSwitch(event.connection,False)
		


		# firewall 
		


	def _handle_ConnectionDown(self,event):

		log.info("Connection from %s has shutdown.",dpid_to_str(event.dpid))


def launch():

	#controller = Task2_Controller()
	#core.register("controller", controller)
	core.registerNew(Controller)
