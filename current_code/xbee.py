from digi.xbee.devices import XBeeDevice
import matplotlib
import matplotlib.pyplot as plt
import numpy as np



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
                #print(self.sample)
            elif(i=='$'):
                self.add_data(int(self.sample))
                if(self.v==True):
                    print(self.sample)
                    print("\n")
                self.sample=''
    def add_data(self,data):
        self.arr.append(data/1023)
    def graph_data(self):
        #TODO add axis
        #TODO export into csv file
        plt.plot(range(len(self.arr)),self.arr)
        plt.title("Data over time")
        plt.show()
    def data_spectrum(self):
        #TODO test this
        f = np.fft.fft(self.arr)
        freq = np.fft.fftfreq(f.shape[-1], d=.002)
        plt.plot(freq,abs(f))
        plt.title("spectrum of data")
        plt.show()




def main():
    print(" +-----------------------------------------+")
    print(" |       Wireless Sleep Monitoring         |")
    print(" |         \"No Strings Attached!\"          |")
    print(" +-----------------------------------------+\n")
    inp = input("Press any key to start! \nIf you want to see print statements hit v")
    if inp=='v':
        Verbose = True
    else:
        Verbose = False

    device = XBeeDevice(PORT, BAUD_RATE)
    grapher = data(Verbose)
    i=0
    device.open()
    device.flush_queues()
    def data_receive_callback(xbee_message,sample): 
        data = xbee_message.data.decode()
        print(data)
        for i in data:
            print(i)
    while i<30:
        message = device.read_data()
        if message!=None:
            i+=1
            try:
                grapher.data_stream(message.data.decode())
                #TODO do something about failed packets
            except(ValueError,RuntimeError,TypeError):
                print("Yikes checksome error look into this")
    device.close()
    grapher.graph_data()
    grapher.data_spectrum()


if __name__ == '__main__':
    main()
