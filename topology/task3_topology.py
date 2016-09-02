
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.util import quietRun
import sys

TASK_LOG = 'task3.log'


class Task3Topo(Topo):


   
	def __init__(self):
		Topo.__init__(self)
		#log.write('Start to add host:\n\n')
		#add hosts
		h1 = self.addHost('h1', ip = '100.0.0.10/24',mac = '00:00:00:00:00:01',defaultRoute='via 100.0.0.1')
		h2 = self.addHost('h2', ip = '100.0.0.11/24',mac = '00:00:00:00:00:02',defaultRoute='via 100.0.0.1')
		h3 = self.addHost('h3', ip = '10.0.0.50/24',mac = '00:00:00:00:00:03',defaultRoute='via 10.0.0.1')
		h4 = self.addHost('h4', ip = '10.0.0.51/24',mac = '00:00:00:00:00:04',defaultRoute='via 10.0.0.1')


		#add switch
		sw1 = self.addSwitch('s1')
		sw2 = self.addSwitch('s2')
		sw3 = self.addSwitch('s3')
		sw4 = self.addSwitch('s4')
		sw5 = self.addSwitch('s5')

		#add firewalls
		fw1 = self.addSwitch('s6')
		fw2 = self.addSwitch('s7')

		lb1 = self.addSwitch('s8')
		lb2 = self.addSwitch('s9')

		ids = self.addSwitch('s10')
		napt = self.addSwitch('s11')

		#add dns server
		ds1 = self.addHost('ds1',ip = '100.0.0.20/24',defaultRoute='via 100.0.0.1')
		ds2 = self.addHost('ds2',ip = '100.0.0.21/24',defaultRoute='via 100.0.0.1')
		ds3 = self.addHost('ds3',ip = '100.0.0.22/24',defaultRoute='via 100.0.0.1')

		#add web servers
		ws1 = self.addHost('ws1',ip = '100.0.0.40/24',mac = '00:00:00:00:00:40',defaultRoute='via 100.0.0.1')
		ws2 = self.addHost('ws2',ip = '100.0.0.41/24',mac = '00:00:00:00:00:41',defaultRoute='via 100.0.0.1')
		ws3 = self.addHost('ws3',ip = '100.0.0.42/24',mac = '00:00:00:00:00:42',defaultRoute='via 100.0.0.1')

		#add insp
		insp = self.addHost('insp',mac = '00:00:00:00:00:88')



		#add links
		for h in h1,h2,fw1:
			self.addLink(h,sw1)
		for h in ds1,ds2,ds3,lb1:
			self.addLink(h,sw3)

		for h in fw1,lb1,ids,fw2:
			self.addLink(h,sw2)

		for h in napt,h3,h4:
			self.addLink(h,sw5)

		self.addLink(fw2,napt)



		for h in ws1,ws2,ws3,lb2:
			self.addLink(h,sw4)

		for h in lb2,insp:
			self.addLink(h,ids)

		#self.set_route()


def task3():

	c0 = RemoteController('c0', ip = '127.0.0.1', port=6633)
	net = Mininet(topo = Task3Topo(), controller = c0)

	ds1 = net.get('ds1')
	ds2 = net.get('ds2')
	ds3 = net.get('ds3')

	ws1 = net.get('ws1')
	ws2 = net.get('ws2')
	ws3 = net.get('ws3')

	

	sw2 = net.get('s2')
	napt = net.get('s11')
	lb1 = net.get('s8')



	

	net.start()

	#self.start_httpServer()
	
	

	for ws in ws1,ws2,ws3:
		ws.cmd('python web.py %s 80 &' % ws.IP())
		#ws.cmd('python -m SimpleHTTPServer 80 &')
	for dns in ds1,ds2,ds3:
		dns.cmd('python dns.py %s & ' % dns.IP())


	net_test(net)

	CLI(net)
	#self.stop_httpServer()

	net.stop()

def net_test(net):

	log = open(TASK_LOG,'w')
	log.write('pbz-hosts connectivity test:\n\n')
	h1 = net.get('h1')
	h2 = net.get('h2')
	h3 = net.get('h3')
	h4 = net.get('h4')
	insp = net.get('insp')

	insp.cmd("tcpdump -s 0 -i insp-eth0 -w insp.pcap &")

	#start pings

	#Test 1: ping test from pbz to prz
	log.write('Test 1: ping test from pbz to prz'+'\n')
	
	result = h1.cmdPrint('ping -c4 ', h3.IP())
	log.write('h1 ping -c4 h3:\n'+result+'\n\n')
	h1.cmd('kill %ping')
	
	result = h1.cmdPrint('ping -c4 ', h4.IP())
	log.write('h1 ping -c4 h4:\n'+result+'\n\n')
	h1.cmd('kill %ping')
	
	result = h2.cmdPrint('ping -c4 ', h3.IP())
	log.write('h2 ping -c4 h3:\n'+result+'\n\n')
	h2.cmd('kill %ping')
	
	result = h2.cmdPrint('ping -c4 ', h4.IP())
	log.write('h2 ping -c4 h4:\n'+result+'\n\n')
	h2.cmd('kill %ping')

	#Test 2: ping test from prz to pbz
	log.write('Test 2: ping test from prz to pbz'+'\n')
	
	result = h3.cmdPrint('ping -c4 ', h1.IP())
	log.write('h3 ping -c4 h1:\n'+result+'\n\n')
	h3.cmd('kill %ping')
	
	result = h3.cmdPrint('ping -c4 ', h2.IP())
	log.write('h3 ping -c4 h2:\n'+result+'\n\n')
	h3.cmd('kill %ping')
	
	result = h4.cmdPrint('ping -c4 ', h1.IP())
	log.write('h4 ping -c4 h1:\n'+result+'\n\n')
	h4.cmd('kill %ping')
	
	result = h4.cmdPrint('ping -c4 ', h2.IP())
	log.write('h4 ping -c4 h2:\n'+result+'\n\n')
	h4.cmd('kill %ping')

	#Test 3: ping test from pbz & prz to dns service
	
	log.write('Test 3: ping test from pbz & prz to dns service(100.0.0.25)'+'\n')
	
	result = h1.cmdPrint('ping -c4 100.0.0.25')
	log.write('h1 ping lb1:\n'+result+'\n\n')
	h1.cmd('kill %ping')
	
	result = h2.cmdPrint('ping -c4 100.0.0.25')
	log.write('h2 ping -c4 lb1:\n'+result+'\n\n')
	h2.cmd('kill %ping')
	
	result = h3.cmdPrint('ping -c4 100.0.0.25')
	log.write('h3 ping -c4 lb1:\n'+result+'\n\n')
	h3.cmd('kill %ping')
	
	result = h4.cmdPrint('ping -c4 100.0.0.25')
	log.write('h4 ping -c4 lb1:\n'+result+'\n\n')
	h4.cmd('kill %ping')
	
	#Test 4: Ping test from pbz & prz to web service
	
	log.write('Test 4: Ping test from pbz & prz to web service(100.0.0.45)'+'\n')	
	result = h1.cmdPrint('ping -c4 100.0.0.45')
	log.write('h1 ping lb1:\n'+result+'\n\n')
	h1.cmd('kill %ping')
	
	result = h2.cmdPrint('ping -c4 100.0.0.45')
	log.write('h2 ping lb2:\n'+result+'\n\n')
	h2.cmd('kill %ping')
	
	result = h3.cmdPrint('ping -c4 100.0.0.45')
	log.write('h3 ping lb2:\n'+result+'\n\n')
	h3.cmd('kill %ping')
	
	result = h4.cmdPrint('ping -c4 100.0.0.45')
	log.write('h4 ping lb1:\n'+result+'\n\n')
	h4.cmd('kill %ping')
	
	#start TCP connnection testing
	log.write('Test 5: TCP Connection from pbz to prz'+'\n') 
	port = 1025
	result = h4.cmd('iperf -s -p '+str(port)+' &')
	log.write('Start an iperf server to h4 (port 1025)in prz\n'+result+'\n')	
	result = h2.cmdPrint('nc -v -w 5 ', h4.IP() ,str(port))
	log.write('\n Establish TCP connection from h2(pbz) to h4(prz)\n'+result+'\n')
	log.write('\n\n') 
	h4.cmd('kill $(pgrep iperf)')
	h2.cmd('kill $(pgrep iperf)')
	#TCP Traffic cannot go through from pbz to prz
	
	log.write('Test 6: TCP Connection from prz to pbz'+'\n')
	result = h2.cmd('iperf -s -p '+str(port)+' &')
	log.write('Start an iperf server to h2 (port 1025)in pbz\n'+result+'\n')
	result = h4.cmdPrint('nc -v -w 5 ',h2.IP(),str(port))	
	log.write('\n Establish TCP connection from h4(prz) to h2(pbz):\n'+result+'\n')
	result = h4.cmdPrint('iperf -c ',h2.IP(),'-p ',str(port))
	log.write(result)
	log.write('\n\n')
	h4.cmd('kill $(pgrep iperf)')
	h2.cmd('kill $(pgrep iperf)')
	
	#dns service test with dig for valid DNS query
	log.write('Test 7: dns service test with dig for valid DNS(100.0.0.25) query'+'\n')
	result = h1.cmdPrint('dig @100.0.0.25 dnstest ')
	log.write('h1 dig single host query lb1:\n'+result+'\n\n')

	
	result = h2.cmdPrint('dig @100.0.0.25 dnstest ')
	log.write('h2 dig single host query lb1:\n'+result+'\n\n')
	
	result = h3.cmdPrint('dig @100.0.0.25 dnstest ')
	log.write('h3 dig single host query lb1:\n'+result+'\n\n')
	
	result = h4.cmdPrint('dig @100.0.0.25 dnstest ')
	log.write('h4 dig single host query lb1:\n'+result+'\n\n') 
	
	#web server test with curl POST & PUT so that IDS allows the traffic to go through
	log.write('Test 8: web server test with curl POST & PUT so that IDS allows the traffic to go through'+'\n')
 
	result = h1.cmdPrint('curl http://100.0.0.45:80 -X PUT ')
	log.write('h3 getting or sending files using URL syntax(Only POST and PUT pass):\n'+result+'\n\n')
	
	result = h2.cmdPrint('curl http://100.0.0.45:80 -X POST ')
	log.write('h3 getting or sending files using URL syntax(Only POST and PUT pass):\n'+result+'\n\n')
	
	result = h3.cmdPrint('curl http://100.0.0.45:80 -X POST ')
	log.write('h3 getting or sending files using URL syntax(Only POST and PUT pass):\n'+result+'\n\n')
	
	result = h4.cmdPrint('curl http://100.0.0.45:80 -X PUT ')
	log.write('h3 getting or sending files using URL syntax(Only POST and PUT pass):\n'+result+'\n\n')

	#web server test with curl DELETE, OPTION, UPDATE, DELETE etc so that IDS blocks the traffic
	log.write('Test 9: web server test with curl DELETE, OPTION, UPDATE, DELETE etc so that IDS blocks the traffic'+'\n') 
	log.write('web server test with curl DELETE, OPTION, UPDATE, DELETE etc so that IDS blocks the traffic\n') 

	result = h1.cmdPrint('curl -m 2 http://100.0.0.45:80 -X PUT -d "UPDATE" ')
	log.write('h1 getting or sending files using URL syntax(Only POST and PUT pass blocking "UPDATE"):\n'+result+'\n\n')
	
	result = h2.cmdPrint('curl -m 2 http://100.0.0.45:80 -X PUT -d "DELETE" ')
	log.write('h2 getting or sending files using URL syntax(Only POST and PUT pass blocking "DELETE):\n'+result+'\n\n')
	
	result = h3.cmdPrint('curl -m 2 http://100.0.0.45:80 -X PUT -d "INSERT" ')
	log.write('h3 getting or sending files using URL syntax(Only POST and PUT pass blocking "INSERT"):\n'+result+'\n\n')
	
	result = h4.cmdPrint('curl -m 2 http://100.0.0.45:80 -X PUT -d "cat /etc/passwd" ')
	log.write('h4 getting or sending files using URL syntax(Only POST and PUT pass blocking "cat /etc/passwd"):\n'+result+'\n\n')
	
	result = h1.cmdPrint('curl -m 2 http://100.0.0.45:80 -X PUT -d "cat /var/log/" ')
	log.write('h1 getting or sending files using URL syntax(Only POST and PUT pass blocking "cat /var/log"):\n'+result+'\n\n')
	
	result = h2.cmdPrint('curl -m 2 http://100.0.0.45:80 ')
	log.write('h2 getting or sending files using URL syntax(Only POST and PUT pass):\n'+result+'\n\n')
	
	result = h2.cmdPrint('curl -m 2 http://100.0.0.45:80 -X GET ')
	log.write('h2 getting or sending files using URL syntax(Only POST and PUT pass blocking GET):\n'+result+'\n\n')
	
	result = h3.cmdPrint('curl -v -m 2 -X TRACE http://100.0.0.45:80 ')
	log.write('h3 getting or sending files using URL syntax(Only POST and PUT pass blocking TRACE):\n'+result+'\n\n')
	
	result = h4.cmdPrint('curl -m 2 OPTIONS http://100.0.0.45:80 ')
	log.write('h4 getting or sending files using URL syntax(Only POST and PUT pass blockinh OPTIONS):\n'+result+'\n\n')
	
	result = h1.cmdPrint('curl -m 2 DELETE http://100.0.0.45:80 ')
	log.write('h1 getting or sending files using URL syntax(Only POST and PUT pass):\n'+result+'\n\n')
	
	result = h4.cmdPrint('curl -m 2 HEAD http://100.0.0.45:80 ')
	log.write('h4 getting or sending files using URL syntax(Only POST and PUT pass):\n'+result+'\n\n')
	
	result = h3.cmdPrint('curl -m 2 CONNECT http://100.0.0.45:80 ')
	log.write('h3 getting or sending files using URL syntax(Only POST and PUT pass):\n'+result+'\n\n')


	log.close()
 
 

if __name__ == '__main__':
	setLogLevel('info')
	task3()


