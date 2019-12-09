# Wireless Sleep Monitoring System
### _No Strings Attached!_  


### System Overview

Codewise currently there are 2 sections, the on-patient micrcontroller and the Raspberry Pi.
We plan on replacing the current bare metal mircocontroller with an arm-M7 running FreeRTOS in the spring.

The microcontroller is an Arduino Uno r3, and it converts analog sensor data to digital data using
`Analogread` inside a timer ISR that happens every 2ms aka sampling at 500Hz. This digital data is then passed
to an XBee module using serial port connection where it is transmitted OTA.

The Raspberry Pi has its own XBee module that it uses to capture the incoming XBee data and display it graphically.
In the future it will capture all different types of sensor data and format them into an EDF file.


### Arduino Code
The main driving force in the Arduino code is a timer `ISR` that triggers once every 2 ms (corresponding to 500 hz). 
This section of the code under the function name `ISR(TIMER1_COMPA_vect)` reads the new sample of data, then sets the status 
variable to let the control loop know that there is a new data point to transmit. In the off-time between the ISRs, 
the portion of the code featured in `void loop()` runs. This code simply transmits the data captured, along with a special char
for formatting(see Packet Formatting), then sets the status to 0 and waits for the next sample to be read. At the moment we have
support for sampling two channels of data at 500 hertz, along with a special i2c channel at 1 sample per second. This is accomplished
by having two `Analogreads` that occur in the `ISR` along with a counter that counts up to 500. When it reaches 500, status is set to 3,
and the control loop knows it needs to read and transmit an I2C sensor value along with the normal values it sends

### Packet Formatting
At the moment we are using a transmission mode called transparent trasmission that allows us to simply input 
the data we would like to send and then the wireless module formats it for us. If possible I would like to stay in this mode
since it is a lot easier to implement. The downside of this is that sometimes a sample right on the edge of two packets might have
its data split between the two packets. You can think of this like reading a book and a sentence is split between the end of one 
page and the start of the next. To deal with this what I did was have a special charector be trasmitted at the end of every sensor value, where each different type of value corresponds to a different charector. The reader I wrote reads number by number until it reaches one of these chars, which indicates that the value is complete and can be added to its respective array data
structure.

### Raspberry Pi Code
The Raspberry Pi code is currently in 2 stages that happen one after another that will eventually happen at the same time.
These 2 parts are packet reading and packet processing. For now for ease of use I just test on my personal linux computer.

#### Packet Reading
Packet reading takes place inside of the try block in the main function in `xbee.py`. What it does is that it takes the function
that I wrote called `data_receive_callback` and it has it run whenever a new packet arrives on the Pi. `data_receive_callback` 
takes the incoming xbee message and stores its contents in a list called `raw_data`. This code runs until the enter key is pressed, after which the `finally` section of the code is run. My computer updating to python3.8 from 3.7 has made this enter command method to
have a several second delay, which is kinda annoying. 

#### Packet Processing
Packet processing is done using a class I wrote called `data` that has a dictonary of arrays for all of the different types of sensor values called `self.dict`. A value holding the current data being processed is called `self.sample`. First the function called 
`data_stream` is run on all of the raw data from the packets we recieved earlier. This function reads the raw data letter by letter (the data is stored as strings at the moment) and concatenates it to the `self.sample` string until it reaches a special char indicating that the whole data sample has been read. When it reaches a special char it transforms `self.sample` into its original number between 0-3.3 and adds it to its respective dictonary based on the special char following the value. Once all values have been read, `graph_data` is run which makes a plot of voltage vs time of the samples we captured.

#### Sending Email via Python 
**This is no longer a valid method of sending patient data since it violates HIPAA unless under certain conditions** 
Following a guide I found [online](https://stackabuse.com/how-to-send-emails-with-gmail-using-python/) I figured out how to send 
an email via python. The code I have included doesn't have the user name and password since it stores the password as plaintext, 
so we will need to only write that in locally. The code at the moment sends `message.txt` to the addresses stored in `mycontacts.txt`,
along with attaching `psk.png` I'm using gmail at the email service for now, but it doesn't play nice with SMTP messages at first,
so to get it to work you need to go into your gmail account and [allow less secure apps to access your account](https://support.google.com/accounts/answer/6010255) to get it to work at first. The libaries used for this are native to python's
base install so there is nothing special that you would need to get this to work. I would not reccomend using your real account 
for doing this.

### Running the system

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
