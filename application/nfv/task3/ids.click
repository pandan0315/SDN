

in_ctr1,  out_ctr1, out_ctr2:: AverageCounter;

dropped_ctr :: Counter;

in_ctr2 :: AverageCounter;

in0 :: FromDevice(s10-eth1,METHOD LINUX,SNIFFER false);

out0 :: Queue(200) -> out_ctr1->ToDevice(s10-eth1);

to_insp :: Queue(200)->out_ctr2->ToDevice(s10-eth3);







in1 :: FromDevice(s10-eth2, METHOD LINUX,SNIFFER false);

out1 :: Queue(2000)->ToDevice(s10-eth2);

      

// LINUX & SQL code injection & needed to be blocked http method
class3 :: Classifier(209/636174202f6574632f706173737764, 
                      209/636174202f7661722f6c6f672f, 
                      208/494E53455254, 
                      208/555044415445, 
                      208/44454C455445, 
                      66/474554, //GET
                      66/48454144,
                      66/5452414345,
                      66/4f5054494f4e53,
                      66/44454c455445,
                      66/434f4e4e454354, //CONNECT
                      -);

// forward



in0->in_ctr1->class3;
class3[0],class3[1],class3[2],class3[3],class3[4],class3[5],class3[6],class3[7],class3[8],class3[9],class3[10] ->dropped_ctr->to_insp;

class3[11] ->out1;


//reverse

in1 -> in_ctr2->IPPrint("reverse")->out0;


//--------------------------------Generate Output---------------------------- 
DriverManager(wait , 
print > ids.report  "=================IDS Report============================
    Input Packet Rate (pps): $(add $(in_ctr1.rate) $(in_ctr2.rate)) 
    Output Packet Rate(pps): $(add $(out_ctr1.rate) $(in_ctr2.rate))

    Total # of input packets: $(add $(in_ctr1.count) $(in_ctr2.count)) 
    Total # of output packets: $(add $(out_ctr1.count) $(in_ctr2.count)) 
    Total # of malicious packets(dropped): $(dropped_ctr.count)
   ========================================================= " ,
stop);


