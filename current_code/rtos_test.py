import csv
from digi.xbee.devices import XBeeDevice
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

#Parameters
PORT = "/dev/ttyUSB0"
BAUD_RATE= 230400



#! /usr/bin/python
raw_data=[]

def main():
    print(" +-----------------------------------------+")
    print(" |       Wireless Sleep Monitoring         |")
    print(" |         \"No Strings Attached!\"          |")
    print(" +-----------------------------------------+\n")
    inp = input("Press enter to start!\nPress enter a second time to stop!")

    #declaring device and grapher
    device = XBeeDevice(PORT, BAUD_RATE)
    try:
        #Opening device
        device.open()
        device.flush_queues()

        def data_receive_callback(xbee_message):
                print(xbee_message.data.decode())


        device.add_data_received_callback(data_receive_callback)

        print("Waiting for data...\n")
        input()

    #For some reason python 3.8 causes delay here
    finally:
        if device is not None and device.is_open():
            #Closing device stops callbacks
            device.close()
            #For now I graph here, but I might have a second thread do this in parallel to the other thread


if __name__ == '__main__':
    main()
