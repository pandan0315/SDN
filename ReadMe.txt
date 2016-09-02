

Running the topology for different tasks:

Go to the topology directory.
For running task1 topology use the command "make topo_task1"
For running task2 topolody use the command "make topo_task2"
For running task 3 topology use the command "make topo_task3"
For performing clean operation use the command "make clean" 

Go to the application directory
For running the task1 controller use the command "make app_task1"
For running the task1 controller use the command "make app_task2"
For running the task1 controller use the command "make app_task3"
For performing clean operation use the command "make clean"

N.B: Please Note that the controller should be first started and then the topology for conductiong sucessful testing as the testing fuction is present within the topology file. The test results will be saved in a .log file.

For example, if you want to get task3 testing results, please follow the steps as follows:

1. go to application directory, use “make app_task3”

2. go to topology directory, use “make topo_task3”

3. after testing in mininet is done, use “ctrl c” to exit controller and “ctrl d ” to exit mininet.

4. click reports will be generated under the application directory. 
   task3.log and insp.pcap will be generated under the topology directory.







