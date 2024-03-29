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

int pos_vai=45;    // 45->90
int pos_ctay=30;    // 30->105
int pos_btay=50;    // 20->50
int pos_than=90;    // 30->150

int Alg_than=3;
int Alg_vai=2;
int Alg_Ctay=1;
int Alg_Btay=0;

int POS_VAI[3];
int POS_BTAY[3];
int POS_CTAY[3];
int POS_THAN[3];

int button1=2;
int button2=4;

int STEP=0;
void setup() 
  {
        Serial.begin(9600);
        pinMode(button1, INPUT);
        pinMode(button2, INPUT);
        vai.attach(9);  // attaches the servo on pin 9 to the servo object
        ctay.attach(10);  // attaches the servo on pin 9 to the servo object
        bantay.attach(6); 
        than.attach(5); 
        POS_VAI[0]=45;
        POS_BTAY[0]=50;
        POS_CTAY[0]=30;
        POS_THAN[0]=90;
  }

void loop() 
  {
      while(true)
      {
          POS_VAI[0]  = map(analogRead(Alg_vai),0,1023,10,100);
          POS_CTAY[0] = map(analogRead(Alg_Ctay),0,1023,0 ,105);
          POS_BTAY[0] = map(analogRead(Alg_Btay),0,1023,20,50);
          POS_THAN[0] = map(analogRead(Alg_than),0,1023,30,150);
          vai.write(POS_VAI[0]);              // tell servo to go to position in variable 'pos'
          ctay.write(POS_CTAY[0]);
          bantay.write(POS_BTAY[0]);
          than.write(POS_THAN[0]);
          if(digitalRead(button1)==LOW)
          {
                delay(200);
                STEP++;
                if(STEP==3)goto RUN;
                POS_THAN[STEP]=POS_THAN[0];  
                POS_VAI[STEP] =POS_VAI[0]; 
                POS_CTAY[STEP]=POS_CTAY[0]; 
                POS_BTAY[STEP]=POS_BTAY[0];
                Serial.println(STEP);
                
          }
      }
RUN:  delay(1000); 
      Serial.print(POS_THAN[1]);
      Serial.print("->");
      Serial.println(POS_THAN[2]);
      Serial.print(POS_VAI[1]);
      Serial.print("->");
      Serial.println(POS_VAI[2]);
      Serial.print(POS_CTAY[1]);
      Serial.print("->");
      Serial.println(POS_CTAY[2]); 
      Serial.print(POS_BTAY[1]);
      Serial.print("->");
      Serial.println(POS_BTAY[2]);   
      while(true)
      {
        delay(1000);
        step2();
        mobantay();
        delay(1000);
        step1();
        dongbantay();
      }  
  }
  
void mobantay()
{
    while(pos_btay>20)
    {
        bantay.write(pos_btay--);
        delay(20);
    }
    
}

void dongbantay()
{
    while(pos_btay<50)
    {
        bantay.write(pos_btay++);
        delay(20);
    }
    
}


void BEGIN()
{
    vai.write(POS_VAI[0]);              // tell servo to go to position in variable 'pos'
    ctay.write(POS_CTAY[0]);
    bantay.write(POS_BTAY[0]);
    than.write(POS_THAN[0]);
    delay(1000);
}

void step2()
{
  while((POS_THAN[0]!=POS_THAN[1])||(POS_VAI[0]!=POS_VAI[1])||(POS_CTAY[0]!=POS_CTAY[1]))
    {
      if(POS_THAN[2]>POS_THAN[1])
      {
        if(POS_THAN[0]>POS_THAN[1])POS_THAN[0]--;
      }
      else
      {
        if(POS_THAN[0]<POS_THAN[1])POS_THAN[0]++;
      }

      if(POS_VAI[2]>POS_VAI[1])
      {
        if(POS_VAI[0]>POS_VAI[1])POS_VAI[0]--;
      }
      else
      {
        if(POS_VAI[0]<POS_VAI[1])POS_VAI[0]++;
      }

      if(POS_CTAY[2]>POS_CTAY[1])
      {
        if(POS_CTAY[0]>POS_CTAY[1])POS_CTAY[0]--;
      }
      else
      {
        if(POS_CTAY[0]<POS_CTAY[1])POS_CTAY[0]++;
      }
      vai.write(POS_VAI[0]);              // tell servo to go to position in variable 'pos'
      ctay.write(POS_CTAY[0]);
      //bantay.write(POS_BTAY[0]);
      than.write(POS_THAN[0]);
      delay(20);
  }
}


void step1()
{
  while((POS_THAN[0]!=POS_THAN[2])||(POS_VAI[0]!=POS_VAI[2])||(POS_CTAY[0]!=POS_CTAY[2]))
    {
      if(POS_THAN[2]>POS_THAN[1])
      {
        if(POS_THAN[0]<POS_THAN[2])POS_THAN[0]++;
      }
      else
      {
        if(POS_THAN[0]>POS_THAN[2])POS_THAN[0]--;
      }

      if(POS_VAI[2]>POS_VAI[1])
      {
        if(POS_VAI[0]<POS_VAI[2])POS_VAI[0]++;
      }
      else
      {
        if(POS_VAI[0]>POS_VAI[2])POS_VAI[0]--;
      }

      if(POS_CTAY[2]>POS_CTAY[1])
      {
        if(POS_CTAY[0]<POS_CTAY[2])POS_CTAY[0]++;
      }
      else
      {
        if(POS_CTAY[0]>POS_CTAY[2])POS_CTAY[0]--;
      }
      vai.write(POS_VAI[0]);              // tell servo to go to position in variable 'pos'
      ctay.write(POS_CTAY[0]);
      //bantay.write(POS_BTAY[0]);
      than.write(POS_THAN[0]);
      delay(20);
  }
}
















