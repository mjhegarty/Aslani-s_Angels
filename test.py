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
import matplotlib
import matplotlib.pyplot as plt

class data():
    def __init__(self):
        self.arr = []
    def add_data(self,data):
        #print(int.from_bytes(data.rstrip(),"big"))
        print(data)
        print(int(data.decode('UTF-8')))
        self.arr.append(int(data.decode('UTF-8')))
        #  self.arr.append(data)
    def graph_data(self):
        print(self.arr)
        plt.plot(range(len(self.arr)),self.arr)
        plt.show()
        


import serial
bluetoothSerial = serial.Serial( "/dev/rfcomm0", baudrate=9600, timeout=1 )
data = data()
for x in range(1000):
    print(x)
    try:
        print(bluetoothSerial.readline())
    except IOError:
        pass
