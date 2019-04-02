#include <SoftwareSerial.h>
//Default password is 1234 
//Wiring: GND of HC-05 to GND Arduino, VCC of HC-05 to VCC Arduino, TX HC-05 to Arduino Pin 10 (RX) RX HC-05 to Arduino Pin 11 (TX) 
SoftwareSerial bt (1, 0); // RX | TX

pinMode(A3, INPUT);
int sensorPin = A3;

//int sensorValue = 0;
int btdata;

void setup() {
  bt.begin(9600);           //  setup serial
}

void loop() {
    btdata = analogRead(sensorPin);  // read the input pin
    //values need to be seperated by commas and end in semicolon

    bt.print(String(btdata) + " was sent");
    bt.print("\n");
    //digitalWrite(";");
    //bt.println ("worked!\n");
    //message to the receiving device
    delay(20);//delay is related to the sampling rate
}
