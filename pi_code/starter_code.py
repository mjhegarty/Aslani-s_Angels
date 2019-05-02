#http://www.uugear.com/portfolio/bluetooth-communication-between-raspberry-pi-and-arduino/
#link that seems useful for the pairing process
#to pair: 
#1hcitool scan
#2sudo bluez-simple-agent hci# xx:xx:xx:xx:xx:xx
#where number is the hci number and the x's are the device location

#3edit the rfcomm config file  sudo vim /etc/bluetooth/rfcomm.conf and add the following:

#rfcomm1 {
#    bind yes;
#    device xx:xx:xx:xx:xx:xx;
#    channel 1;
#    comment "Connection to Bluetooth serial module";
#}

#4  sudo apt-get install python-serial 


#! /usr/bin/python

import serial
from time import sleep

bluetoothSerial = serial.Serial( "/dev/rfcomm0", baudrate=9600, timeout=1 )
print (bluetoothSerial.name)
while (True):
    try:
        print (bluetoothSerial.read(20))
        #in_Blue = bluetoothSerial.readline()
        #print_blue = float(in_Blue)* 5 / 1023
        #print (bluetoothSerial.readline())
        sleep(.5)
    except IOError:
        pass
