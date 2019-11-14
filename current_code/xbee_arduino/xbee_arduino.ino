
#include <SoftwareSerial.h>
#include <stdio.h>
#include <stdlib.h>
SoftwareSerial XBee(2,3);
int sensorPin0 = A0;
int sensorPin1 = A1;
int data2=0;
volatile int data=0;
volatile int status;
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
    //Serial.print("test");
    if (status==1){
        cli();
        XBee.print(data);
        XBee.print("$");
        XBee.print("^^^^^^^^^^^^^^^^^^^^");
        status=0;
        sei();
    }
}
ISR(TIMER1_COMPA_vect)
{
    data = analogRead(A0);
    status=1;
}
