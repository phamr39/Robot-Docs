/* Sweep
 by BARRAGAN <http://barraganstudio.com>
 This example code is in the public domain.

 modified 8 Nov 2013
 by Scott Fitzgerald
 http://www.arduino.cc/en/Tutorial/Sweep
*/

#include <Servo.h>

Servo ctay;  // create servo object to control a servo
Servo vai;
Servo bantay;
Servo than;
// twelve servo objects can be created on most boards

int pos_vai=45;    // variable to store the servo position
int pos_ctay=30;
int pos_btay=50;
int pos_than=90;

int incomingByte = 0;
void setup() {
  Serial.begin(9600);
  vai.attach(9);  // attaches the servo on pin 9 to the servo object
  ctay.attach(10);  // attaches the servo on pin 9 to the servo object
  bantay.attach(6); 
  than.attach(5); 
}

void loop() 
  {
       if (Serial.available() > 0) 
       {
                    incomingByte = Serial.read();
                    if(char(incomingByte)=='a')
                    {
                        if(pos_vai<90)pos_vai++;
                    }
                     if(char(incomingByte)=='q')
                    {
                        if(pos_vai>45)pos_vai--;  
                    }
                    if(char(incomingByte)=='e')
                    {
                        if(pos_ctay<105)pos_ctay++;
                    }
                     if(char(incomingByte)=='d')
                    {
                        if(pos_ctay>30)pos_ctay--;  
                    }
                    if(char(incomingByte)=='z')
                    {
                        if(pos_btay<50)pos_btay++;
                    }
                     if(char(incomingByte)=='x')
                    {
                        if(pos_btay>20)pos_btay--;  
                    }
                    if(char(incomingByte)=='v')
                    {
                        if(pos_than<150)pos_than++;
                    }
                     if(char(incomingByte)=='c')
                    {
                        if(pos_than>30)pos_than--;  
                    }
                    Serial.print(pos_vai);
                    Serial.print(':');
                    Serial.print(pos_ctay);
                    Serial.print(':');
                    Serial.print(pos_btay);
                    Serial.print(':');
                    Serial.println(pos_than);
                    
        }
        vai.write(pos_vai);              // tell servo to go to position in variable 'pos'
        ctay.write(pos_ctay);
        bantay.write(pos_btay);
        than.write(pos_than);
  }
  

