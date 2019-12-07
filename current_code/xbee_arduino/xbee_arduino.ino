//TODO Sprint: Include wire.h and init it and stuff
#include <SoftwareSerial.h>
#include <stdio.h>
#include <stdlib.h>
SoftwareSerial XBee(2,3);
int sensorPin0 = A0;
volatile int data=0;
volatile int data1=50;
volatile int data2=200;
volatile int data3=400;
volatile int status;
int counter = 0;
void setup()
{
    //Serial.begin(19200);
    XBee.begin(230400);
    pinMode(A0, INPUT);
    pinMode(A1, INPUT);

    // initialize Timer1
    cli(); // disable global interrupts
    TCCR1A = 0; // set entire TCCR1A register to 0
    TCCR1B = 0; // same for TCCR1B
    TCNT0 = 0;

    // set compare match register to desired timer count:
    OCR1A = 31999; // = 16000000 / (1 * 500) - 1 (must be <65536)
    // turn on CTC mode:
    TCCR1B |= (1 << WGM12);
    // Set CS10 and CS12 bits for 1 prescaler:
    //TCCR1B |= (1 << CS10);
    //TCCR1B |= (1 << CS12);
    TCCR1B |= (0 << CS12) | (0 << CS11) | (1 << CS10);
    // enable timer compare interrupt:
    TIMSK1 |= (1 << OCIE1A);
    sei(); // enable global interrupts
}


void loop(){
    //TODO Sprint: add logic for different header cases based on the value in status.
    //Switch case?
    cli();
    switch(status){
      //Normal just ekg
      case 1:
        XBee.print(data);
        XBee.print("$");
        break;
      //ekg and pulse ox
      case 2:
          XBee.print(data);
          XBee.print("$");
          XBee.print(data1);
          XBee.print("%");
          break;
      //ekg pulse ox and bdy pos
      case 3: 
          XBee.print(data);
          XBee.print("$");
          XBee.print(data1);
          XBee.print("%");
          XBee.print(data2);
          XBee.print("#");
          XBee.print(data3);
          XBee.print("@");
          break;      
    }
    status = 0;
    sei();
}
ISR(TIMER1_COMPA_vect)
{
    data = analogRead(A0);
    //TODO Sprint: add logic for I2C sampling here
    //TODO Sprint: add modulo logic for counters to go off based on when we want pulse ox
    //Different cases change status to a different value
    counter++;
    if(counter%500 == 0){
      status = 3;
      counter = 0;
    }
    else if(counter%20 == 0){
      status = 2;
    }
    else {
      status = 1;
    }
}
