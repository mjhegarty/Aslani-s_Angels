# Wireless Sleep Monitoring System
### _No Strings Attached!_  


### System Overview

Codewise ATM there are only 2 segements, the on-patient mircocontroller and the Raspberry Pi.

The mircocontroller is an Arduino Uno r3, and it converts analog sensor data to digital data using
`Analogread` inside a timer ISR that happens every 2ms aka sampling at 500Hz. This digital data is then passed
to an XBee module using serial port connection where it is transmitted OTA.

The Raspberry Pi has its own XBee module that it uses to capture the incoming XBee data and display it graphically.
In the future it will capture all different types of sensor data and format them into an EDF file.


#### Packet Formatting

At the moment we are using a transmission mode called transparent trasmission that allows us to simply input 
the data we would like to send and then the wireless module formats it for us. If possible I would like to stay in this mode
since it is a lot easier to implement. The downside of this is that sometimes a sample right on the edge of two packets might have
its data split between the two packets. You can think of this like reading a book and a sentence is split between the end of one 
page and the start of the next. To deal with this what I did was have a $ be trasmitted at the end of every sensor value. The reader I wrote reads number by number until it reaches a $, which indicates that the value is complete and can be added to the data
structure. In the future this will be useful when we need to differentiate between different types of data samples, so we can just
have each sample have a unique stop character.

### Running the system

#### Mircocontroller

* Copy the code written under in current_code/xbee_arduino/xbee_arduino.ino and write it to your device.
* Attach wires from the arduino to the XBee for power(5V) and ground
* Attach the Arduino's digital pin #3 to the XBee's DIN pin

#### Raspberry Pi / Linux
##### Installation
* On the device run `git clone https://github.com/mjhegarty/WirelessSleepMonitoring.git` to get the code
* Run `sudo apt install python3` & `sudo apt install python3-pip` to get python and the pip, a python package manager
* Run `pip3 install matplotlib numpy digi-xbee --user` To get the python packages you need
* `cd WirelessSleepMonitoring/current_code/`
* `python3 xbee.py`
