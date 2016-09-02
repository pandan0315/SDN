# SDN

This design consists of:
1. A public zone (PbZ) with two hosts and one L2 switch  that interconnects the entire
network to the Internet.
2. A firewall that controls the access to the demilitarized zone (DmZ).
3. A DmZ that contains two clusters of servers interconnected with one core switch (sw2).
The servers (ds1, ds2, and ds3) formulate a cluster that provides Domain
Name System (DNS) services. The IP of the DNS service is virtual
(does not correspond to a physical network element). A load balancer (lb1) sits between
the core switch  and the three DNS servers ensuring that incoming requests, which
target the virtual IP, will be modified accordingly with the destination IP address of a
server in a round­robin fashion. a Switch is used to connect the load balancer with the
DNS cluster.
The servers (ws1, ws2, and ws3) formulate a cluster that provides
Hypertext Transfer Protocol (HTTP) services. The IP of the Web service is 100.0.0.45
(virtual too). A load balancer (lb2) sits between the core switch  and the three Web
servers ensuring that incoming requests, which target the virtual IP, will be modified
accordingly with the destination IP address of a server in a round­robin fashion. Switch
sw34 is used to connect the load balancer with the Web cluster. Before lb2, the incoming
packets must be inspected by ids, an Intrusion Detection System (IDS) module. This
module will search at the incoming packets’ payload for certain “suspicious” patterns. If
such a pattern is identified, the packet will be redirected to the inspector (insp) server for
further processing. Otherwise, legal traffic will pass through lb2 as described afore.
4. A firewall  that controls the access to the private zone (PrZ).
5. A Network Address and Port Translator (NAPT) that translates the private IP addresses
of hosts in PrZ into public IP addresses within the range of DmZ and PbZ.
6. A PrZ with two hosts and one L2 switch (sw5) that interconnects this zone with DmZ
(through napt and fw2).
