// reference :https://github.com/kohler/click/blob/master/conf/thomer-nat.click



define(

     $in_eth    s11-eth1,
     $out_eth    s11-eth2,
     $in_side_ip     10.0.0.1,
     $in_side_mac     00:00:00:00:11:01,
     $out_side_ip       100.0.0.1,
     $out_side_mac      00:00:00:00:11:02,

);

AddressInfo(
inside $in_side_ip     $in_side_mac,
ouside  $out_side_ip  $out_side_mac,
);



//define the different counter
input_ctr1, output_ctr1:: AverageCounter;

arp_req_ctr1,arp_res_ctr1,icmp_ctr1,dropped_ctr1, ip_ctr1 :: Counter;

input_ctr2, output_ctr2 :: AverageCounter;

arp_req_ctr2,arp_res_ctr2,icmp_ctr2,dropped_ctr2, dropped_ctr3,dropped_ctr4, dropped_ctr5,ip_ctr2 :: Counter;



in_side :: FromDevice($in_eth , METHOD LINUX,SNIFFER false);
out1 :: Queue(2000) ->output_ctr1-> ToDevice(s11-eth1,METHOD LINUX);

out_side :: FromDevice($out_eth , METHOD LINUX, SNIFFER false);
out2 :: Queue(2000) ->output_ctr2-> ToDevice(s11-eth2,METHOD LINUX);


in_side_class, out_side_class :: Classifier(12/0806 20/0001,12/0806 20/0002, 12/0800,-);

in_side_arpq :: ARPQuerier(inside);
out_side_arpq :: ARPQuerier(ouside);

ip_to_outside :: GetIPAddress(16)
                ->CheckIPHeader
                ->IPPrint("ip_to_out")
                ->[0]out_side_arpq
                ->IPPrint("outarp")
                ->out2;

ip_to_inside :: GetIPAddress(16)
                ->CheckIPHeader
                ->IPPrint("ip_to_inside")
                ->[0]in_side_arpq
                ->IPPrint("inarp")
                ->out1;


out_side->input_ctr2 -> out_side_class;

out_side_class[0]->arp_req_ctr2 -> ARPResponder(ouside)-> out2;


out_side_class[1]->arp_res_ctr2 -> [1]out_side_arpq;

out_side_class[3]->dropped_ctr1-> Discard;


in_side->input_ctr1-> in_side_class;

in_side_class[0]->arp_req_ctr1-> ARPResponder(inside)-> out1;

in_side_class[1] ->arp_res_ctr1-> [1]in_side_arpq;

in_side_class[3]->dropped_ctr2-> Discard;



// rules for TCP/UDP packets, 
ip_rw :: IPRewriter(pattern 100.0.0.1 20000-65535 - - 0 1,drop);


//rewriting for icmp echo packets
icmp_rw :: ICMPPingRewriter(pattern 100.0.0.1 20000-65535 - - 0 1,drop);

//request are emitted on output 0, replies on output 1

icmp_rw[0]->ip_to_outside;
icmp_rw[1]->ip_to_inside;



// output 0 is from inside to outside
ip_rw[0]->IPPrint("iprewriter out")->ip_to_outside;

// output 1 is for reverse traffic
ip_rw[1]->IPPrint("iprewriter in")->ip_to_inside;


//traffic initialize from inside
in_side_class[2]->ip_ctr1-> Strip(14)-> CheckIPHeader -> IPPrint("ip traffic from inside")->inside_ipclass :: IPClassifier(dst net 10.0.0.0/24,-);

//inside traffic still stay in the inside
inside_ipclass[0] ->IPPrint("still in side")->ip_to_inside;

//inside traffic go outside
inside_ipclass[1] -> IPPrint("go outside") -> proto_ipclass :: IPClassifier(udp or tcp,icmp type echo,-);

proto_ipclass[0] -> [0]ip_rw;
proto_ipclass[1] ->icmp_ctr1-> [0]icmp_rw;
proto_ipclass[2] ->dropped_ctr3->Discard;



//traffic from outside
out_side_class[2] ->ip_ctr2-> Strip(14) -> CheckIPHeader ->filter_out_ip :: IPClassifier(dst host 100.0.0.1,-)
                                                ->IPPrint("ip traffic from outside")
                                                ->outside_class :: IPClassifier(icmp type echo-reply, udp or tcp,-)
filter_out_ip[1] ->dropped_ctr4->Discard;

                                              outside_class[0]->icmp_ctr2->[1]icmp_rw;
                                              outside_class[1]->[1]ip_rw;
                                              outside_class[2]->dropped_ctr5->Discard;


//--------------------------------Generate Output Report--------------------------------------

DriverManager(wait , 
  print > napt.report  "=================NAPT Report============================
    Input Packet Rate (pps): $(add $(input_ctr1.rate) $(input_ctr2.rate)) 
    Output Packet Rate(pps): $(add $(output_ctr1.rate)  $(output_ctr2.rate))
    
    Total # of input packets: $(add $(input_ctr1.count) $(input_ctr2.count))
    Total # of output packets: $(add $(output_ctr1.count)  $(output_ctr2.count))

    Total # of ARP requests packets: $(add $(arp_req_ctr1.count) $(arp_req_ctr2.count))
    Total # of ARP respondes packets: $(add $(arp_res_ctr1.count) $(arp_res_ctr2.count))

    Total # of service requests packets: $(add $(ip_ctr1.count) $(ip_ctr2.count))

    Total # of ICMP packets: $(add $(icmp_ctr1.count) $(icmp_ctr2.count))

    Total # of dropped packets: $(add $(dropped_ctr1.count) $(dropped_ctr2.count)
                                   $(dropped_ctr3.count) $(dropped_ctr4.count)
                                   $(dropped_ctr5.count))

   ========================================================= " ,
  stop);
