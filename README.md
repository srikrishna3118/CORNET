# CORNET (Co-Simulation Middleware for Robotic Networks)

CORNET is a a co-simulation middleware for applications involving multi-robot systems like a network of Unmanned Aerial Vehicle (UAV) systems. The framework integrates ns-3 network simulator and Ardupilot based UAV simulator Software-in-the-loop (SITL) with light weight Pub/Sub based middleware. Design framework for one-to-one correspondence between UAVs in Gazebo and nodes in NS-3 is borrowed from [paper](https://arxiv.org/pdf/1808.04967.pdf). If you find this code useful in your research, please consider citing:
```
	@conference{@Srikrishna20,
		title = {CORNET: A Co-Simulation Middleware for Robot Networks},
		author = {Srikrishna Acharya; Amrutur Bharadwaj; Yogesh Simmhan; Aditya Gopalan; Parimal Parag; Himanshu,Tyagi},
		year = {2020},
		date = {2020-01-06},
		booktitle = {12th International Conference on COMmunication Systems & NETworkS, Bengaluru, Jan 7-11, 2019},
		keywords = {Robotics},
		pubstate = {forthcoming},
		tppubtype = {conference}
	}

```
This code was tested on an Ubuntu 16.04 and Ubuntu 18.04 system. For network simulator, ns-3.27 or ns-3.29 is used; so the dependent packages need to be installed as mentioned in ns-3 wiki page. For ubuntu/debian platform, the specific packages can be found at: https://www.nsnam.org/wiki/Installation#Ubuntu.2FDebian.2FMint . The basic packages needed are : Python2.7, pip, python-dev, gcc.

### Installation

1. Additional Dependencies for FlyNetSim:   
Install latest version of czmq, libzmq, libczmq and libxml

~~sudo apt-get install libzmq5 libzmq-dev libczmq4 libczmq-dev czmq libxml2 libxml2-dev~~
```
   sudo apt-get install libzmq5 libzmq3-dev libczmq-dev libczmq4 libxml2 libxml2-dev
```
If you get error for versions, install the latest available version.

2. Clone the Git repository:
```
```
3. Go to the network folder and run the initial script which downloads ns-3.29, applies patches, configures and builds. This script needs to be executed only once and it may take a while to finish.
```
  $ cd CORNET/network
  $ ./net_init.sh
```
4. Go to the drone folder and run the initial script for downloading and configuring Ardupilot, dronekit and sitl. his script also needs to be executed only once and it may take a longer time to finish.
```
  $ cd CORNET/drone
  $ ./drone_init.sh
```
5. Install PyQt4 for GUI.
```
  sudo apt-get install python-qt4
```

### Run Simulation

After successful installation, execute the simulation with the following command. It creates the end-to-end communication, a GUI as ground-control station to send commands and receive telemetry. The Ardupilot also creates indiviual console window for each UAV that shows the flight status. To run the simulator with default parameters: 
```
  $ cd CORNET/
  $ python CORNET.py
```
Specific parameters can be passed for different attributes in the simulation, e.g., number of UAVs, initial position of the UAV(s), network type (WiFi or LTE), external traffic load (number of contending nodes, data rates, packet size). To check the options that can be passed, use the help command:
```
$ python CORNET.py --help
```
Once the program runs, it opens one terminal for each UAV and one terminal for the ns-3 and one GUI panel with several buttons as GCS for the UAV commands. In the GUI panel, you need to follow the orders:\
i) Click only once the "CONNECT" and wait until "ARM" button is active.\
ii) Click only once the "ARM" button to arm the vehicle (with default parameters) and wait until "TAKEOFF" button becomes active.\
iii) Click only once the "TAKEOFF" button and wait until other control buttons (UP/DOWN etc.) become active. Notice that the takeoff command takes the UAV to 10m height.\
iv) click other control buttons for movements (UP/DOWN, FORWARD/BACKWARD, LEFT/RIGHT) as many times you need.\
v) Click LAND button for landing.\

If you want automated mission, you can avoid the GUI and write your own mission in drone/uav_pubsub.py or in drone/gcs_pubsub.py file.

#### Multi-UAV Scenario
For Multiple UAVs as of now, a simple positioning system with linear layout is used. It takes x-coordinate of the first UAV and places other UAVs 5 meters apart. If different layout is required, the code needs to be modified. Also, for multi-UAV scenario a single GCS gives commands to all the UAVs. The code can be extended for individual control of the vehicles.


### Fix for Possible Errors

1. While building ns-3, if you get an error for "syslog.h" in  "include/czmq_prelude.h", comment out the line in "include/czmq_prelude.h" from the include path (/usr/local/include/czmq_prelude.h or /usr/include/czmq_prelude.h ) .
```
  //#include <syslog.h>
```

2. If there is error for the path of "config.xml" file provide absolute path with FlyNetSim.py.
 
3. If the ardupilot/Tools/scripts folder does not have "install-prereqs-ubuntu.sh" , recursively update the submodules of arduplilot repository. Run the command from inside the ardupilot directory:
```
 $ git submodule update -init --recursive
```
