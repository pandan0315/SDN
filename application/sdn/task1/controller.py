from pox.core import core
from pox.lib.util import dpid_to_str
from pox.forwarding.l2_learning import LearningSwitch

log = core.getLogger()

class Controller(object):
	def __init__(self):
		core.openflow.addListeners(self)

	def _handle_ConnectionUp(self,event):

		log.debug("Switch %s has come up.", dpid_to_str(event.dpid))

		LearningSwitch(event.connection,False)
		
def launch():

	#controller = Task2_Controller()
	#core.register("controller", controller)
	core.registerNew(Controller)


