from digi.xbee.devices import XBeeDevice
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

#Parameters
PORT = "/dev/ttyUSB0"
BAUD_RATE= 230400



#! /usr/bin/python

class data():
    def __init__(self, v):
        self.arr = []
        #TODO make array of arrays for different sample types
        self.sample=''
        self.v = v
    def data_stream(self,packet):
        for i in packet:  
            #TODO make a dictionary of special chars that will be used for different sample types
            if(i!='$' and i!='\n' and i!=''):
                self.sample = self.sample+i
            elif(i=='$'):
                if self.sample!='':
                    self.add_data(int(self.sample))
                self.sample=''
    def add_data(self,data):
        #TODO make 5 into whatever our ref voltage is
        self.arr.append((5*data)/1023)
    def graph_data(self):
        #TODO export into csv file
        #Super sick generator for converting to time from sample count
        plt.plot([x/500 for x in range(len(self.arr))],self.arr)
        plt.title("Data over time")
        plt.xlabel("Time(s)")
        plt.ylabel("Voltage(V)")
        plt.show()
    def data_spectrum(self):
        #TODO test this
        f = np.fft.fft(self.arr)
        freq = np.fft.fftfreq(f.shape[-1], d=.002)
        plt.plot(freq,abs(f))
        plt.title("spectrum of data")
        plt.show()


raw_data=[]

def main():
    print(" +-----------------------------------------+")
    print(" |       Wireless Sleep Monitoring         |")
    print(" |         \"No Strings Attached!\"          |")
    print(" +-----------------------------------------+\n")
    inp = input("Press enter to start!\nPress enter a second time to stop!")
    #ignore this for now
    if inp=='v':
        Verbose = True
    else:
        Verbose = False

    #declaring device and grapher
    device = XBeeDevice(PORT, BAUD_RATE)
    grapher = data(Verbose)
    try:
        #Opening device
        device.open()
        device.flush_queues()

        #Honestly no idea what a callback is. 
        def data_receive_callback(xbee_message):
                print(xbee_message.data.decode())
                raw_data.append(xbee_message.data.decode())


        #Think that this function basically runs this code A$AP when it gets a packet
        device.add_data_received_callback(data_receive_callback)

        print("Waiting for data...\n")
        #This just has the device capture data until an input is entered
        input()
    #Finally block triggers after input ends
    finally:
        if device is not None and device.is_open():
            #Closing device stops callbacks
            device.close()
            #For now I graph here, but I might have a second thread do this in parallel to the other thread
            for j in raw_data:    
                grapher.data_stream(j)
            grapher.graph_data()


if __name__ == '__main__':
    main()
