from digi.xbee.devices import XBeeDevice
import matplotlib
import matplotlib.pyplot as plt



PORT = "/dev/ttyUSB0"
BAUD_RATE= 230400



#! /usr/bin/python

class data():
    def __init__(self):
        self.arr = []
    def add_data(self,data):
        #print(int.from_bytes(data.rstrip(),"big"))
        print(data)
        #print(5*int(data.decode('UTF-8'))/1023)
        #self.arr.append(5*int(data.decode('UTF-8'))/1023)
        self.arr.append(data/1023)
    def graph_data(self):
        print(self.arr)
        plt.plot(range(len(self.arr)),self.arr)
        plt.show()
        






def main():
    print(" +-----------------------------------------+")
    print(" | XBee Python Library Receive Data Sample |")
    print(" +-----------------------------------------+\n")

    device = XBeeDevice(PORT, BAUD_RATE)
    grapher = data()

    try:
        device.open()
        def data_receive_callback(xbee_message):
            data = ord(xbee_message.data.decode())
            grapher.add_data(data)
        device.add_data_received_callback(data_receive_callback)

        print("Waiting for data...\n")
        input()
        


    finally:
        if device is not None and device.is_open():
            device.close()
            grapher.graph_data()


if __name__ == '__main__':
    main()
