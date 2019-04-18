#include <SoftwareSerial.h>
//Default password is 1234 
//Wiring: GND of HC-05 to GND Arduino, VCC of HC-05 to VCC Arduino, TX HC-05 to Arduino Pin 10 (RX) RX HC-05 to Arduino Pin 11 (TX) 
SoftwareSerial bt (1, 0); // RX | TX
int sensorPin0 = A0;
int sensorPin1 = A1;

int sensorValue0 = 0;
int sensorValue1 = 0;
//int btdata;

void setup() {
  bt.begin(9600);           //  setup serial
  pinMode(A0, INPUT);
  pinMode(A1, INPUT);
}

void loop() {
    sensorValue0 = analogRead(sensorPin0);  // read the input pin
    sensorValue0 = analogRead(sensorPin0);
    //values need to be seperated by commas and end in semicolon
    sensorValue1 = analogRead(sensorPin1);
    sensorValue1 = analogRead(sensorPin1);
    bt.print(String(sensorValue0) + " was sent from 0");
    bt.print("\n");
    delay(1000);//delay is related to the sampling rate
    bt.print(String(sensorValue1) + " was sent from 1");
    bt.print("\n");
    delay(1000);
}
