#include <SoftwareSerial.h>
//Default password is 1234 
//Wiring: GND of HC-05 to GND Arduino, VCC of HC-05 to VCC Arduino, TX HC-05 to Arduino Pin 10 (RX) RX HC-05 to Arduino Pin 11 (TX) 
SoftwareSerial BTserial(10, 11); // RX | TX

int sensorPin = A0;

int sensorValue = 0;


void setup() {
  Serial.begin(9600);           //  setup serial
}

void loop() {
    val = analogRead(analogPin);  // read the input pin
    //values need to be seperated by commas and end in semicolon
    BTserial.print(val);
    BTserial.print(";");
    //message to the receiving device
    delay(20);//delay is related to the sampling rate
}
