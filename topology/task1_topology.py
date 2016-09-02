
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel
import sys

TASK1_LOG = 'task1.log'


class Task1Topo(Topo):


   
	def __init__(self):
		Topo.__init__(self)
        #log.write('Start to add host:\n\n')
		#add hosts
		h1 = self.addHost('h1', ip = '100.0.0.10/24')
		h2 = self.addHost('h2', ip = '100.0.0.11/24')

		#add switch
		sw1 = self.addSwitch('sw1')

		#add links
		self.addLink(h1,sw1)
		self.addLink(h2,sw1)

def task1():

	c0 = RemoteController('c0', ip = '127.0.0.1', port=6633)
	net = Mininet(topo = Task1Topo(), controller = c0)

	net.start()

	net_test(net)
	CLI(net)

	net.stop()

def net_test(net):

	log = open(TASK1_LOG,'w')
	log.write('pbz-hosts connectivity test:\n\n')
	h1 = net.get('h1')
	h2 = net.get('h2')
	h1.cmd('echo > ', log)

	#start pings
	result=h1.cmdPrint('ping -c4', h2.IP())
	log.write('h1 ping -c4 h2:\n'+result+'\n\n')
	h1.cmd('kill %ping')
	log.close()
    


if __name__ == '__main__':
	setLogLevel('info')
	task1()


