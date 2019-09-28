
#include <SoftwareSerial.h>                                                                                                                                                 
#include <stdio.h>                                                                                                                                                          
#include <stdlib.h> 
SoftwareSerial bt (0, 1);                                                                                                                                    
int sensorPin0 = A0;                                                                                                                                                        
int sensorPin1 = A1;          
void setup()
{
  bt.begin(9600);
  pinMode(A0, INPUT);                                                                                                                                                     
  pinMode(A1, INPUT);

  // initialize Timer1
  cli(); // disable global interrupts
  TCCR1A = 0; // set entire TCCR1A register to 0
  TCCR1B = 0; // same for TCCR1B
  TCNT0 = 0;

  // set compare match register to desired timer count:
  OCR1A = 15;
  //OCR1A = 200;
  // turn on CTC mode:
  TCCR1B |= (1 << WGM12);
  // Set CS10 and CS12 bits for 1024 prescaler:
  TCCR1B |= (1 << CS10);
  TCCR1B |= (1 << CS12);
  // enable timer compare interrupt:
  TIMSK1 |= (1 << OCIE1A);
  sei(); // enable global interrupts
}

void loop(){
}

ISR(TIMER1_COMPA_vect)
{
  int data = analogRead(A0);
  bt.print(String(data));
  bt.print("\n");
}
