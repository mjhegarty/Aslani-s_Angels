#include <Wire.h>
#include <SPI.h>
#include <Adafruit_LSM9DS1.h>
#include <Adafruit_Sensor.h>  // not used in this demo but required!

// i2c
Adafruit_LSM9DS1 lsm = Adafruit_LSM9DS1();

#define LSM9DS1_SCK A5
#define LSM9DS1_MISO 12
#define LSM9DS1_MOSI A4
#define LSM9DS1_XGCS 6
#define LSM9DS1_MCS 5




//TODO Sprint: Include wire.h and init it and stuff
#include <SoftwareSerial.h>
#include <stdio.h>
#include <stdlib.h>
SoftwareSerial XBee(2,3);
int sensorPin0 = A0;
int sensorPin1 = A1;
volatile int data=0;
volatile int data1=50;
volatile int data2=200;
volatile int data3=400;
volatile int status;
int counter = 0;



void setupSensor()
{
  // 1.) Set the accelerometer range
  lsm.setupAccel(lsm.LSM9DS1_ACCELRANGE_2G);
  //lsm.setupAccel(lsm.LSM9DS1_ACCELRANGE_4G);
  //lsm.setupAccel(lsm.LSM9DS1_ACCELRANGE_8G);
  //lsm.setupAccel(lsm.LSM9DS1_ACCELRANGE_16G);
  
  // 2.) Set the magnetometer sensitivity
  lsm.setupMag(lsm.LSM9DS1_MAGGAIN_4GAUSS);
  //lsm.setupMag(lsm.LSM9DS1_MAGGAIN_8GAUSS);
  //lsm.setupMag(lsm.LSM9DS1_MAGGAIN_12GAUSS);
  //lsm.setupMag(lsm.LSM9DS1_MAGGAIN_16GAUSS);

  // 3.) Setup the gyroscope
  lsm.setupGyro(lsm.LSM9DS1_GYROSCALE_245DPS);
  //lsm.setupGyro(lsm.LSM9DS1_GYROSCALE_500DPS);
  //lsm.setupGyro(lsm.LSM9DS1_GYROSCALE_2000DPS);
}







void setup()
{


    //Gyro stuff
    lsm.begin();
    lsm.setupAccel(lsm.LSM9DS1_ACCELRANGE_2G);
    setupSensor();
   
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
        XBee.print(data1);
        XBee.print("%");
        break;
      //ekg and pulse ox
      /*
      case 2:
          XBee.print(data);
          XBee.print("$");
          XBee.print(data1);
          XBee.print("%");
          break;
      //ekg pulse ox and bdy pos
      */
      case 3:
          sei();  
          lsm.read();  
              /* ask it to read in the data */ 
              /* Get a new sensor event */ 
          sensors_event_t a;
          lsm.getEvent(&a,0,0,0);
          data2 = a.acceleration.x;
          data3 = a.acceleration.z;
          cli();
        
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
    asm("nop");
    data1 = analogRead(A1);
    //TODO Sprint: add logic for I2C sampling here
    //TODO Sprint: add modulo logic for counters to go off based on when we want pulse ox
    //Different cases change status to a different value
    counter++;
    if(counter%500 == 0){
      status = 3;
      counter = 0;

    }
    //else if(counter%20 == 0){
     // status = 2;
    //}
    else {
      status = 1;
    }
}
