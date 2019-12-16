#!/bin/sh

#Ardupilot stack 
git clone https://github.com/ArduPilot/ardupilot
cd ardupilot
git submodule update --init --recursive

cd ardupilot
./Tools/scripts/install-prereqs-ubuntu.sh -y

~/.profile

#dronekit --control
sudo pip install dronekit

#dronekit-sitl is optional if you are using ardupilot SITL Framework
sudo pip install dronekit-sitl

#zmq python library
sudo pip install pyzmq
