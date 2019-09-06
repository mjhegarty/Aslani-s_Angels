# Wireless Sleep Monitoring System



Codewise there are going to be several sections:


Micro controller:
The micro controller code will involve multiplexing between the various ADC (analog to digital) inputs and formatting these inputs to be
sent through the bluetooth module to the rasberry pi. This is where we will sample and quantize the analog sensor inputs.
This will be written in C using an Aurdino using an 8 bit adc. 


Rasberry Pi:
The R pi code will involve taking the formatted bluetooth input, making it into a format that can be received by the server and sending it to the 
server using a wifi connection. R Pi code is written in python, but I could see bash/general linux commands also being useful for automating some of these steps

Server:
The Server code will involve taking the formatted input send via wifi to the server and storing it using some sort of database platform. Depending on what the client
wants and what is easiest to implement this could either be stored on some sort of cloud server like google or amazon or on a SEAS server. This section will
be coded using some sort of database langage such as SQL


"APP":
This will be a computer program that the client will run to be able to access the data and view it remotly using a PC. It will take data from the
server and process it based on what the client wants, for example they might want to know average heartrate over the period of the expierment. Was thinking
that it would have a login page, a data request page where you essentially fill out a form of what data you want and then a data display page, with an option 
to save the graphs. It is easier to do the display and the options separately so that we don't need to use multiple threads for the GUI. This coding will be done 
in python using tkinter or another langage depnding on what works best.
