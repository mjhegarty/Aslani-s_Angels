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
        #Badass dictionary of arrays(no idea if this works tbh
        self.dict = {"EKG": [], "EEG":[], "PulseOX": [], "BodyX":[], "BodyZ":[]}
        self.sample=''
        self.v = v
    def data_stream(self,packet):
        for i in packet:  
            if(i!='$' and i!='\n' and i!='' and i!='~'):
                self.sample = self.sample+i
            elif(i=='$'):
                if self.sample!='':
                    self.add_data(int(self.sample), "EKG")
                self.sample=''
            #TODO Sprint: make use cases for other header chars 
    def add_data(self,data, key):
        #TODO Sprint: make 5 into whatever our ref voltage is
        self.dict[key].append((5*data)/1023)
    def graph_data(self):
        #Super sick generator for converting to time from sample count
        plt.subplot(3,1,1)
        plt.plot([x/500 for x in range(len(self.dict["EKG"]))],self.dict["EKG"])
        plt.title("Data over time")
        plt.xlabel("Time(s)")
        plt.ylabel("Voltage(V)")
        plt.subplot(3,1,2)
        plt.plot([x/500 for x in range(len(self.dict["EKG"]))],self.dict["EKG"])
        plt.title("Data over time")
        plt.xlabel("Time(s)")
        plt.ylabel("Voltage(V)")
        plt.subplot(3,1,2)
        plt.plot([x/500 for x in range(len(self.dict["EKG"]))],self.dict["EKG"])
        plt.title("Data over time")
        plt.xlabel("Time(s)")
        plt.ylabel("Voltage(V)")
        plt.show()
        #TODO Sprint: export into edf file
        


    #Sounds good doesn't work lol
    def data_spectrum(self):
        f = np.fft.fft(self.dict["EKG"])
        freq = np.fft.fftfreq(f.shape[-1], d=.002)
        plt.plot(freq,abs(f))
        plt.title("spectrum of data")
        plt.show()
    def data_avg(self):
        data_sum = 0
        for i in self.dict["EKG"]:
            data_sum+=i
        self.avg = data_sum/len(self.dict["EKG"])
        print("Avg value per sample is:")
        print(self.avg)
    def sampling_test_squarewave(self):
        last_sample = None
        #TODO make sure avg is defined
        last_index = None
        sample_count = 0
        n_samples = 0
        sample_sum = 0
        for i,sample in enumerate(self.dict["EKG"]):
            if last_sample!=None:
                #Next if checks if sample is an 'edge'
                if sample>self.avg and last_sample<self.avg :
                    if last_index != None:
                        n_samples = i-last_index
                        sample_count += 1
                        sample_sum += n_samples
                    last_index = i
            last_sample = sample
        avg_n_samples = sample_sum/sample_count
        fs = avg_n_samples*20 #TODO freq wave
        print("Actual Measured sampling frequency is")
        print(fs)
        
        



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
            grapher.data_avg()
            grapher.graph_data()
            grapher.sampling_test_squarewave()


if __name__ == '__main__':
    main()
