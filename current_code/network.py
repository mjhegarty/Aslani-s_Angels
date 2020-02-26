import csv
from digi.xbee.devices import XBeeDevice
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import ctypes

#Parameters
PORT = "/dev/ttyUSB0"
BAUD_RATE= 230400



#! /usr/bin/python

class data():
    def __init__(self, v):
        #Badass dictionary of arrays(no idea if this works tbh
        self.dict = {"EKG": [], "EEG":[], "PulseOX": [], "BodyX":[], "BodyZ":[], "SampleSquareWave":[]}
        self.sample=''
        self.data=bytearray()
        self.v = v
    def data_stream(self,stream):
        is_header = 1
        byte_count = 0
        start = 0
        #TODO fill this in actually
        byte_options = {8: 3}
        case = 0
        data_logger = ctypes.CDLL("/home/mikey/projects/WirelessSleepMonitoring/current_code/form.so")
        data_logger.format_packet.argtypes = [ctypes.POINTER(ctypes.c_char)]
        for packet in stream: 
        #Wait for starter packet
            for i in packet:  
                if start == 0:
                    if (i==255):
                        start = 1

                else:
                    if is_header == 1:
                        case = i
                        #byte_count = byte_options[i]
                        byte_count = 3
                        char_array = ctypes.c_char * (byte_count+1)
                        is_header = 0
                        self.data.append(i)

                    else:
                        #TODO might have to do something else for appending
                        self.data.append(i)
                        byte_count = byte_count -1
                        #If all the bytes are read call the c organization function and set is header back to 1
                        if byte_count == 0 :
                            print(self.data)
                            ##C function
                            data_logger.format_packet(char_array.from_buffer(self.data))
                            self.data = bytearray()
                            is_header = 1


    def add_data(self,data, key):
        if(key=="EKG" or key=="SampleSquareWave"):
            self.dict[key].append((3.3*data)/1023)
        else :
            self.dict[key].append(data)
    def graph_data(self):
        plt.subplot(3,1,1)
        #Makes our figures not look dumb
        plt.tight_layout()
        #Super sick generator for converting to time from sample count
        plt.plot([x/500 for x in range(len(self.dict["EKG"]))],self.dict["EKG"])
        plt.title("EKG")
        plt.xlabel("Time(s)")
        plt.ylabel("Voltage(V)")
        plt.subplot(3,1,2)
        plt.tight_layout()
        plt.plot([x/500 for x in range(len(self.dict["SampleSquareWave"]))],self.dict["SampleSquareWave"])
        plt.title("SampleSquareWave")
        plt.xlabel("Time(s)")
        plt.ylabel("Voltage(V)")
        plt.subplot(3,1,3)
        plt.tight_layout()
        plt.plot([x for x in range(len(self.dict["BodyX"]))],self.dict["BodyX"])
        
        #Hold on is deault in matlibplot thats sick!
        plt.plot([x for x in range(len(self.dict["BodyZ"]))],self.dict["BodyZ"])
        #TODO Sprint: spelling 
        plt.title("Body posistion")
        plt.xlabel("Time(s)")
        plt.ylabel("Voltage(V)")
        plt.legend(["X position", "Z Position"])
        plt.show()
        #TODO Sprint: export into edf file
        


    def csv_data(self):
        with open('ekg.csv', 'w') as csvfile:
            writer = csv.writer(csvfile)
            for i in self.dict["EKG"]:
                writer.writerow([i])



    #Sounds good doesn't work lol
    def data_spectrum(self):
        f = np.fft.fft(self.dict["EKG"])
        freq = np.fft.fftfreq(f.shape[-1], d=.002)
        plt.plot(freq,abs(f))
        plt.title("spectrum of data")
        plt.show()
    def data_avg(self):
        data_sum = 0
        for i in self.dict["SampleSquareWave"]:
            data_sum+=i
        self.avg = data_sum/len(self.dict["SampleSquareWave"])
        print("Avg value per sample is:")
        print(self.avg)
    def sampling_test_squarewave(self):
        last_sample = None
        #TODO make sure avg is defined
        last_index = None
        sample_count = 0
        n_samples = 0
        sample_sum = 0
        for i,sample in enumerate(self.dict["SampleSquareWave"]):
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
            ##TODO check if this is a real function
                raw_data.append(xbee_message.data)
                print(xbee_message.data)


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
            grapher.data_stream(raw_data)
            #grapher.data_avg()
            #grapher.graph_data()
            #grapher.sampling_test_squarewave()
            #grapher.csv_data()


if __name__ == '__main__':
    main()
