#define encoderPinA      2                     // Quadrature encoder A pin
#define encoderPinB      3                     // Quadrature encoder B pin
#define M1              9                      // PWM outputs to L298N H-Bridge motor driver module
#define M2              10
int SetPulse=334; //Set Pulse
const int Sample_time = 50; //Example_time
volatile float Kp=0.039 , Ki=0.007 , Kd=0.003;
volatile float P,I,D;
volatile long int count = 0; 
volatile int pulse_out;
volatile float error=0,pre_error=0; //error
int Sum_error=0; //Khoi tao ham tinh tong cac error phuc vu tinh tich phan
/*------------------------*/
void PulseOut(int count) // PID
{
  int pre_count;
  int error = count - pre_count;
  int pre_error = error;
  P = Kp * error;
  I += Ki*error*Sample_time/1000;
  D = Kd*(error - pre_error)*1000/Sample_time;
  int output =(int) P+I+D;
  if (output > 255)
  {
    output = 255;
    }
  if (output < 0)
  {
    output = 0; 
    }
  pre_count = count;
  pulse_out = 34*60*1000*output/(SetPulse*Sample_time); 
  }
/*------------------------*/
void count_pulse()  //Hàm đếm xung
{
    if(digitalRead(encoderPinB) == LOW)
      count++;
    else
      count--;
}

void Motor_control(int output, bool rot ) //rot dung de doi chieu quay dong co
{
  analogWrite(M1,(rot)? output:0);
  analogWrite(M2,(rot)? 0:output);
}

void setup()
{
    Serial.begin(9600);
    pinMode(encoderPinA,INPUT);
    pinMode(encoderPinB,INPUT);
    pinMode(M1,OUTPUT);
    pinMode(M2,OUTPUT);
    attachInterrupt(0,count_pulse,RISING);
    analogWrite(M1,0);
    analogWrite(M2,0);
}

void loop()
{
  count_pulse();
  PulseOut(count);
  //Serial.println(count);
  Motor_control(pulse_out,0);
  //Serial.println(pulse_out);
}   
