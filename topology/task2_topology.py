
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel
import sys

TASK1_LOG = 'task2.log'


class Task2Topo(Topo):


   
	def __init__(self):
		Topo.__init__(self)
		#log.write('Start to add host:\n\n')
		#add hosts
		h1 = self.addHost('h1', ip = '100.0.0.10/24')
		h2 = self.addHost('h2', ip = '100.0.0.11/24')
		h3 = self.addHost('h3', ip = '100.0.0.50/24')
		h4 = self.addHost('h4', ip = '100.0.0.51/24')

		#add switch
		sw1 = self.addSwitch('s1')		
		sw3 = self.addSwitch('s3')
		
		#add firewalls
		fw1 = self.addSwitch('s6')

		#add links
		for h in h1,h2:
			self.addLink(h,sw1)
		for h in h3,h4:
			self.addLink(h,sw3)
		for h in sw1,sw3:
			self.addLink(h,fw1)
		


def task2():

	c0 = RemoteController('c0', ip = '127.0.0.1', port=6633)
	net = Mininet(topo = Task2Topo(), controller = c0)

	net.start()
	
	net_test(net)

	CLI(net)

	net.stop()

def net_test(net):

	log = open(TASK1_LOG,'w')
	
	h1 = net.get('h1')
	h2 = net.get('h2')
	h3 = net.get('h3')
	h4 = net.get('h4')
     
	#start pings
	log.write('Test 1: ping test from pbz to prz'+'\n')
	result = h1.cmdPrint('ping -c4 ', h3.IP())
	
	log.write('h1 ping -c4 h3:\n'+result+'\n\n')
	h1.cmd('kill %ping')
	log.write('Test 2: ping test from prz to pbz'+'\n')
	result = h3.cmdPrint('ping -c4 ', h1.IP())
	log.write('h3 ping -c4 h1:\n'+result+'\n\n')
	h3.cmd('kill %ping')

	#start TCP connnection testing
	port = 1025
	log.write('Test 3: TCP Connection from pbz to prz'+'\n')
	result = h4.cmd('iperf -s -p '+str(port)+' &')
	log.write('Start an iperf server to h4 (port 1025)in prz\n'+result+'\n')	
	result = h2.cmdPrint('nc -v -w 5 ', h4.IP() ,str(port))
	log.write('\n Establish TCP connection from h2(pbz) to h4(prz)\n'+result+'\n')
	log.write('\n\n')
	h4.cmd('kill $(pgrep iperf)')
	h2.cmd('kill $(pgrep iperf)')

	log.write('Test 4: TCP Connection from prz to pbz'+'\n')
	result = h2.cmd('iperf -s -p '+str(port)+' &')
	log.write('Start an iperf server to h2 (port 1025)in pbz\n'+result+'\n')
	result = h4.cmdPrint('nc -v -w 5 ',h2.IP(),str(port))	
	log.write('\n Establish TCP connection from h4(prz) to h2(pbz):\n'+result+'\n')
	result = h4.cmdPrint('iperf -c ',h2.IP(),'-p ',str(port))
	log.write(result)
	log.write('\n\n')
	h4.cmd('kill $(pgrep iperf)')
	h2.cmd('kill $(pgrep iperf)')

	log.close()
 




if __name__ == '__main__':
	setLogLevel('info')
	task2()


