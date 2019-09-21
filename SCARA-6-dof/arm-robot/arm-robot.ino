/*This code is free to use,not for sale, you can ou can redistribute it and/or modify it */
/*Written by Hieu Pham, email: pha.mr3998@gmail.com*/
/*This code is written for 6-dof SCARA
 * Stepper has 4 wires control (A+,A-,B+,B-)
 * Servo has 1 wire control
 * Use Arduino Mega 2560
 * 6 limit switch
 * This code don't use any arduino library so you dont need to include anything
 */
/*------------------------------------------------------------------*/
/* Pin connect: 
 * Servo control pin - A1 (on Board)
 * Stepper 1 pin: CLK-2,CW-3 ..... Stepper 6 pin: CLK-12,CW-13
 * Limit switch 1 - 6 : Pin 14-19
*/
/*------------------------------------------------------------------*/
/* If you want to receive data from computer by COM port, you need send variables:
 *stepper_rot
 *stepper_dir
 *and any variables you think it may be need to board
*/
/*------------------------------------------------------------------*/
/* Define output pin of stepper
 * On TB6560 board, connect CW+,CLK+,EN+ to 5V ...
   CLK_Pin (CLK- port on driver) is control pulse out Pin, 
   CW_Pin (CW- port on driver) is direction pin
 */

#define CLK_Pin1 2
#define CW_Pin1 3
#define CLK_Pin2 4
#define CW_Pin2 5
#define CLK_Pin3 6
#define CW_Pin3 7
#define CLK_Pin4 8
#define CW_Pin4 9
#define CLK_Pin5 10
#define CW_Pin5 11
#define CLK_Pin6 12
#define CW_Pin6 13
/* Define output pin of servo*/
#define servoPin A0
/* Define input pin from limit switch*/
#define limit_sw1 14
#define limit_sw2 15
#define limit_sw3 16
#define limit_sw4 17
#define limit_sw5 18
#define limit_sw6 19
/*------------------------------------------------------------------*/
/* Show variable */
/* Variables are used for stepper*/
int stepper_dir;
int stepper_rot;
int CLK_Pin;
int CW_Pin;
int num_step;
int i;
float standart_step;
float trans_ratio; /*Transmission ratio*/
/* Variables are used for Servo*/
byte pos;
unsigned int pulse_duration;
/* Variables are used for find limit switch subroutine*/
int limit_sw;
int half_round;
/*------------------------------------------------------------------*/
/* Stepper control subroutine
 * This code for full-step mode, if you want change to half-step,1/8 or 1/16 please change variable i

*/
/*How to use this subroutine?
 *Variables define:
 *stepper_dir : Direction rotate of stepper => input 0 or 1
 *stepper_rot : Rotation of stepper => input 0-360 degree, example: stepper_rot=90
 *CLK_Pin,CW_Pin: name of pin which connected with stepper, check #define part
 *standart_step: minium step of stepper (degree)
 *trans_ratio: Transmisson ratio of stepper
*/
void stepper_control(int stepper_dir,int stepper_rot,int CLK_Pin,int CW_Pin,float standart_step,float trans_ratio)
{
  /*Convert rotation to step*/
  num_step = (int) (stepper_rot/standart_step)*trans_ratio;
  /*Stepper direction*/
  if(stepper_dir == 1)
  {
  digitalWrite(CW_Pin,HIGH);
  } else
  {
    digitalWrite(CW_Pin,LOW);
    }
  /*Stepper run*/
  /*Due to we connect CLK+ port,CW+ port to 5V so CLK-,CW- are control port and /CKL-,/CW-
   *If you want to change the speed of stepper, please increase or decrease variable of delayMicroseconds(variable) function
   *When CLK_Pin is pulled up from LOW to HIGH, Stepper will rotation 1 step
   *Num_step is numbers of step which stepper must rotation to complete the rotation input (from stepper_rot variable)
    */
  for (i=0;i<num_step;i++)
  {
    digitalWrite(CLK_Pin,LOW);                         
    delay(5)
    digitalWrite(CLK_Pin,HIGH);
    delay(5);
    }
  }
/*------------------------------------------------------------------*/
/*This subroutine help stepper can find the limit switch to come back to start position*/
/*half_round variable is number of each stepper must rotate to complete 180 degree*/
/*How to use thí subroutine?
 *limit_sw: number of pin which connected to limit switch
 *CLK_Pin,CW_Pin same as stepper_control subroutine
 *half_round: numbers of step which stepper must rotate to complete 180 degree, dont forget multiplication with transmisson ratio
 */
void findmygirl(int limit_sw,int CLK_Pin,int CW_Pin,int half_round)
{
  int num_step = 0;
  if (digitalRead(limit_sw)==LOW)
  {
    digitalWrite (CW_Pin,HIGH);
    while (num_step <= half_round || digitalRead(limit_sw) == HIGH)
    {
    digitalWrite(CLK_Pin,LOW);                         
    delay(5);
    digitalWrite(CLK_Pin,HIGH);
    delay(5); 
    num_step++;     
      }
    if (digitalRead(limit_sw)==LOW)
    {
      digitalWrite(CW_Pin,LOW);
      while (num_step <= half_round || digitalRead(limit_sw) == HIGH)
    {
        digitalWrite(CLK_Pin,LOW);                         
        delay(5);
        digitalWrite(CLK_Pin,HIGH);
        delay(5); 
        num_step++;     
      }
    }
    if (digitalRead(limit_sw) == HIGH)
      {
        Serial.print("Limit switch connected is on");
        }
        else
        {
          Serial.print("Limit switch connected is off");
          }
    } else 
    {
      Serial.print("Limit switch connected is on");
      }
  }
/*------------------------------------------------------------------*/
/*Servo control subroutine*/
/*This function will convert from rotation input to pulse duration*/
/* Pulse duration:
 * 600 <=> 0 degree, 1450 <=> 90 degree, 2300 <=> 180 degree
 * Pulse duration = (2300-600)/180 * rotation +600
  */
/*How to use this subroutine
 *pos: rotation of servo (degree), example 60 degree
 */
/*void servo_control(unsigned int pos)
{
 pulse_duration = (unsigned int) (85/9)*pos + 600;
/*A pulse each 20ms*/
  /*
  digitalWrite(servoPin,HIGH);
  delayMicroseconds(pulse_duration); //Duration of the pulse in microseconds
  digitalWrite(servoPin,LOW);
  delayMicroseconds(20000-pulse_duration); //20ms-duration of the pulse
  }
/*------------------------------------------------------------------*/
/*Test led of limit switch - NOT NECESSARY*/ 
/* 
void test_led()
 {
  if (digitalRead(limit_sw1)==HIGH && digitalRead(limit_sw2)==HIGH && digitalRead(limit_sw3)==HIGH && digitalRead(limit_sw4)==HIGH && digitalRead(limit_sw5)==HIGH && digitalRead(limit_sw6)==HIGH)
  {}
  else {
   for (int j = 0,j<5, j++)
   {
    servo_control(180);
    delay(500);
    servo_control(90);
    delay(500);
  }
    }
  }
  */
/*------------------------------------------------------------------*/
  void setup()
  {
    Serial.begin(9600);
    /* Configuration stepper pin is OUTPUT*/
    pinMode(CLK_Pin1,OUTPUT);
    pinMode(CW_Pin1,OUTPUT);
    pinMode(CLK_Pin2,OUTPUT);
    pinMode(CW_Pin2,OUTPUT);
    pinMode(CLK_Pin3,OUTPUT);
    pinMode(CW_Pin3,OUTPUT);
    pinMode(CLK_Pin4,OUTPUT);
    pinMode(CW_Pin4,OUTPUT);
    pinMode(CLK_Pin5,OUTPUT);
    pinMode(CW_Pin5,OUTPUT);
    pinMode(CLK_Pin6,OUTPUT);
    pinMode(CW_Pin6,OUTPUT);
    /*Configuration servo pin is OUTPUT*/
    pinMode(servoPin,OUTPUT);
    /*Configuration limit switchs pin is INPUT*/
    pinMode(limit_sw1,INPUT);
    pinMode(limit_sw2,INPUT);
    pinMode(limit_sw3,INPUT);
    pinMode(limit_sw4,INPUT);
    pinMode(limit_sw5,INPUT);
    pinMode(limit_sw6,INPUT);
    /*This part will rotate all stepper back to start posion (find limit switch)  */
    /*215365=4615*46.656 (= numbers of stepper to rotate 1 round * transmission ratio)*/
 /*
    findmygirl(14,2,3,100);   
    delayMicroseconds(500);
    findmygirl(15,4,5,215365);   
    delayMicroseconds(500);
    findmygirl(16,6,7,36749);   
    delayMicroseconds(500);
    findmygirl(17,8,9,2668);   
    delayMicroseconds(500);
    findmygirl(18,10,11,100); 
    delayMicroseconds(500);
    findmygirl(19,12,13,100); 
    delayMicroseconds(1000);
    /*Open gripper*/
   /* servo_control(180);
    delayMicroseconds(1000);
    */
    }
  void loop()
  {
    /*Rotate to ...
     *This part is demo, we must re-calculation step_rot variables by Henhavit-Hatenberg table or input from COM
    */
    /*Stepper 1 rot 90 degree*/
    /*
    stepper_control(1,45,2,3,1.8,1);
    /*delayMicroseconds(1000);*/
    /*Stepper 2 rot  18 degree*/
    stepper_control(1,18,4,5,0.039,46.656);
    /*delayMicroseconds(1000);*/
    /*Stepper 3 rot  36 degree*/
    /*stepper_control(1,36,6,7,0.094,19.19);
    /*delayMicroseconds(1000);*/
    /*Stepper 4 rot  36 degree*/
    /*stepper_control(1,36,8,9,0.35,5.18);
    /*delayMicroseconds(1000);*/
    /*Stepper 5 rot  36 degree*/
    /*stepper_control(1,36,10,11,1.8,1);
    /*delayMicroseconds(1000);*/
    /*Stepper 6 rot  90 degree*/
    /*stepper_control(1,36,12,13,1.8,1);
    /*delayMicroseconds(1000);*/
    /*Close Gripper*/
    /*servo_control(90);
    delayMicroseconds(1000);
    /*Back*/
    /*
    stepper_control(0,36,12,13,1.8,1);
    /*delayMicroseconds(1000);*/
    /* 
    stepper_control(0,36,10,11,1.8,1);
    /*delayMicroseconds(1000);*/
    /*
    stepper_control(0,36,8,9,0.35,5.18);
    /*delayMicroseconds(1000);*/
    /*
    stepper_control(0,36,6,7,0.094,19.19);
    /*delayMicroseconds(1000);*/
    /*
    stepper_control(0,18,4,5,0.039,46.656);
    /*delayMicroseconds(1000);*/
    /*
    stepper_control(0,90,2,3,1.8,1);
    /*delayMicroseconds(1000);*/
    /*
    servo_control(180);
    delayMicroseconds(1000); */
    }
  /*------------------------------END------------------------------------*/
