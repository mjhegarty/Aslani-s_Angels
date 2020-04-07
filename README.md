# Wireless Sleep Monitoring System
### _No Strings Attached!_  


### System Overview
Our goal is to design a wireless sleep monitoring system capable of sampling 13 different data channels and sending them to 
a database formatted into an [EDF](https://en.wikipedia.org/wiki/European_Data_Format) file. The 13 data channels each require
12 bits of data per sample and have sampling frequency requirements varying from 500 hertz to 1 hertz. With this much data required
to be sampled with the given fidelity and timing requirements, while also needing to be sent wirelessly, an RTOS(Real Time Operating 
System) is required. This RTOS will run on an arm-based microcontroller that is attached to the patient and sampled data is transmitted
to an off-patient Raspberry Pi, where it will then be converted to EDF files and stored on a dropbox server. 


### Running the system (needs to be updated)

#### Microcontroller

* Copy the code written under in current_code/xbee_arduino/xbee_arduino.ino and write it to your device.
* Attach wires from the arduino to the XBee for power(5V) and ground
* Attach the Arduino's digital pin #3 to the XBee's DIN pin

#### Raspberry Pi / Linux
* On the device run `git clone https://github.com/mjhegarty/WirelessSleepMonitoring.git` to get the code
* Run `sudo apt install python3` & `sudo apt install python3-pip` to get python and the pip, a python package manager
* Run `pip3 install matplotlib numpy digi-xbee --user` To get the python packages you need
* `cd WirelessSleepMonitoring/current_code/`
* `python3 xbee.py`
