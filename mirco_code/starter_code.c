#include <SoftwareSerial.h>
//Default password is 1234 
//Wiring: GND of HC-05 to GND Arduino, VCC of HC-05 to VCC Arduino, TX HC-05 to Arduino Pin 10 (RX) RX HC-05 to Arduino Pin 11 (TX) 
SoftwareSerial bt (1, 0); // RX | TX

int sensorPin = A0;

int sensorValue = 0;

void setup() {
  bt.begin(9600);           //  setup serial
  pinMode(A0, INPUT);
}

void loop() {
    sensorValue = analogRead(sensorPin);  // read the input pin
    //values need to be seperated by commas and end in semicolon

    bt.print(String(sensorValue) + " was sent"); //message to the receiving device
    bt.print("\n");
    
    delay(1000);//delay is related to the sampling rate
}
