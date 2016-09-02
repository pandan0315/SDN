

//define the different counter
input_ctr1, output_ctr1:: AverageCounter;

arp_req_ctr1,arp_res_ctr1,icmp_ctr,dropped_ctr1, ip_ctr1:: Counter;


input_ctr2, output_ctr2:: AverageCounter;

arp_req_ctr2,arp_res_ctr2,dropped_ctr2, dropped_ctr3,ip_ctr2 :: Counter;


client_side :: FromDevice(s9-eth2,METHOD LINUX,SNIFFER false);
out1 :: Queue -> output_ctr1->ToDevice(s9-eth2,METHOD LINUX);

server_side :: FromDevice(s9-eth1,METHOD LINUX,SNIFFER false);
out2 :: Queue -> output_ctr2->ToDevice(s9-eth1,METHOD LINUX);



client_side_class, server_side_class :: Classifier(12/0806 20/0001,12/0806 20/0002, 12/0800,-);

server_side_arpq :: ARPQuerier(100.0.0.45,s9-eth1);
client_side_arpq :: ARPQuerier(100.0.0.45,s9-eth2);

ip_to_client :: GetIPAddress(16)
                ->CheckIPHeader
                ->IPPrint("ip_to_client")
                ->[0]client_side_arpq
                ->IPPrint("clientarp")
                ->out1;

ip_to_server :: GetIPAddress(16)
                ->CheckIPHeader
                ->IPPrint("ip_to_server")
                ->[0]server_side_arpq
                ->IPPrint("serverarp")
                ->out2;


client_side ->input_ctr1-> client_side_class;

client_side_class[0] -> arp_req_ctr1-> ARPResponder(100.0.0.45 s9-eth2)-> out1;


client_side_class[1] -> arp_res_ctr1 -> [1]client_side_arpq;

client_side_class[3] -> dropped_ctr1 -> Discard;


server_side -> input_ctr2->server_side_class;

server_side_class[0] ->arp_req_ctr2-> ARPResponder(100.0.0.45 s9-eth1)->out2;


server_side_class[1] -> arp_res_ctr2->[1]server_side_arpq;

server_side_class[3]  -> dropped_ctr2->Discard;


rr_mapper :: RoundRobinIPMapper(100.0.0.45 - 100.0.0.40 80 0 1,
                                100.0.0.45 - 100.0.0.41 80 0 1,
                                100.0.0.45 - 100.0.0.42 80 0 1);

rw :: IPRewriter(rr_mapper,pattern 100.0.0.45 - - - 1 0);

rw[0]->IPPrint("out1")->ip_to_server;
rw[1]->IPPrint("out2")->ip_to_client;




client_ip_classifier1 :: IPClassifier(dst host 100.0.0.45,-);

client_ip_classifier2 :: IPClassifier(icmp,dst tcp port 80,-);

client_side_class[2] ->ip_ctr1-> Strip(14)
                    -> CheckIPHeader
                    -> client_ip_classifier1;
                    
client_ip_classifier1[0]->client_ip_classifier2;

client_ip_classifier1[1]->ICMPError(10.0.0.45,unreachable) -> out1;

client_ip_classifier2[0]->icmp_ctr->icmppr :: ICMPPingResponder() 
                        ->ip_to_client;


client_ip_classifier2[1]-> IPPrint("to server")
                        -> [0]rw;

client_ip_classifier2[2]->dropped_ctr3-> Discard;

server_side_class[2]->ip_ctr2-> Strip(14)
                    -> CheckIPHeader
                    -> IPPrint("to client")
                    -> [1]rw;

//--------------------------------Generate Output Report--------------------------------------
DriverManager(wait , 
print > lb2.report  "=================LB2 Report============================
    Input Packet Rate (pps): $(add $(input_ctr1.rate) $(input_ctr2.rate)) 
    Output Packet Rate(pps): $(add $(output_ctr1.rate) $(output_ctr2.rate))
    
    Total # of input packets: $(add $(input_ctr1.count) $(input_ctr2.count)) 
    Total # of output packets: $(add $(output_ctr1.count) $(output_ctr2.count)) 

    Total # of ARP requests packets: $(add $(arp_req_ctr1.count) $(arp_req_ctr2.count))
    Total # of ARP respondes packets: $(add $(arp_res_ctr1.count) $(arp_res_ctr2.count))

    Total # of service requests packets: $(add $(ip_ctr1.count) $(ip_ctr2.count))
    Total # of ICMP packets: $(icmp_ctr.count)
    Total # of dropped packets: $(add $(dropped_ctr1.count) $(dropped_ctr2.count))

   ========================================================= " ,
stop);
