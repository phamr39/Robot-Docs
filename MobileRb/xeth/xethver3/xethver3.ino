

/*Include necessarry library*/
/*Define motor control pins*/
/*Left motor: Pin chan ,Right motor: Pin left*/
int inApin[2] = { 4,7 }; //Clockwise
int inBpin[2] = { 8,9 }; //Counter Clockwise
int pwmpin[2] = { 6,5 }; //PWM pin
int motor_left = 0;
int motor_right = 1;
int i,j;
int prev;
/*Define encoder signal pins*/
#define encoder_right1 18
#define encoder_right2 22
#define encoder_left1 19
#define encoder_left2 24
/*Define SRF04 Pin*/
#define trig_pin 50
#define echo_pin 52
/*Define enable motor pins*/
#define enable_right 53
#define enable_left 52
/*Signal Receive
  Firstly, pull digital pin 20 up to 5V
  After that, transmission follow:
  ----> status of robot (0: stop, 1: move)
  ----> x_goal
  ----> y_goal
  ----> phi
*/
#define CommPin 20 
volatile float goal[10][10];
const float scale = 2.3;
volatile byte flag;
//byte sta; // sta = 0: Stop, sta = 1: Move
float signalRead()
{
  //angle = Serial.parseFloat();
  //Thu tu truyen: x1->y1->x2...
while (Serial.available() )
{ 
  Serial.println("signal read");
  goal[i][j] = scale * Serial.parseFloat();
  Serial.println(i);
  Serial.println("Return");
  Serial.println(goal[i][j]);
  i++;  // 0 - 9
  if (i>9) {j ++; i=0;}
  if (j>2){j--;}

return goal[i][j];
Serial.println("Reset");
    flag = 1; 
    Serial.print(Serial.available());
} 

}
/*PID*/
/*Variable*/
float P, I, D;
float output;
float PID_cal(float error)
{
  float output;
  float Kp = 1.255, Kd = 0.055, Ki = 0.023;
  float pre_error;
  P = Kp * error;
  I += Ki * error;
  D = Kd * (error - pre_error);
  output = P + I + D;
  pre_error = error;
  return output;
}
/*Encoder function: should use Encoder_right1 (Pin 18)
 * and Encoder_left1 (Pin 19)
*/
int tick;
int ReadEncoder(uint8_t encoder_pin)
{
  if (digitalRead(encoder_pin) == 1)
  {
    tick++;
  }
  else
  {
    tick--;
  }
  return tick;
}
int time = 0;
int delta_tick_left, delta_tick_right, pre_tick_left, pre_tick_right, tick_left, tick_right;
const float pi = 3.14;
float D_left, D_right, D_c;
int N = 100;
float R = 0.04;
float L = 0.19;
float phi = 0, x =0, y=0, x_goal, y_goal, phi_d;
float vel_left, vel_right; // Velocity of left and right wheels
float omega;
int vel = 10; // the velocity be set, 0-255
int error;
/* motorGo() will set a motor going in a specific direction
 the motor will continue going in that direction, at that speed
 until told to do otherwise.

 motor: this should be either 0 or 1, will selet which of the two
 motors to be controlled

 direct: Should be between 0 and 3, with the following result
 1: Clockwise
 2: CounterClockwise

 pwm: should be a value between ? and 1023, higher the number, the faster
 it'll go
 */
void motorGo(uint8_t motor, uint8_t direct, uint8_t pwm)
{
  if (motor <= 1)
  {
    if (direct == 1 || direct == 2)
    {
      // Set inA[motor]
      if (direct <= 1)
      {
        digitalWrite(inApin[motor], HIGH);
        digitalWrite(inBpin[motor], LOW);
      }
      else
      {
        digitalWrite(inApin[motor], LOW);
        digitalWrite(inBpin[motor], HIGH);
      }
      analogWrite(pwmpin[motor], pwm);
    }
  }
}
void go_to_goal( float x_goal, float y_goal)
{
  /*if (phi_d == 3.5)
  {
    digitalWrite(13,HIGH);;
    }*/
  
 // float   distance = getDistance();
  // float distance = 40;
  //if (distance >= 30)
  //while(D_c <= 30)
  //{
    // go to goal
    phi_d = atan2((y_goal - y), (x_goal - x));
    error = phi_d - phi;
    omega = PID_cal(error);
    vel_left = (2 * vel - omega * L) / (2 * R);
    vel_right = (2 * vel + omega * L) / (2 * R);
    if (vel_left > 255)
    {
      vel_left = 255;
    }
    if (vel_right > 255)
    {
      vel_right = 255;
    }
    if (x == x_goal, y == y_goal)
    {
      digitalWrite(enable_left, HIGH);
      digitalWrite(enable_right, HIGH);
    }
    // Motor wheel on clockwise (go forward)
    digitalWrite(enable_left, LOW);
    digitalWrite(enable_right, LOW);
    motorGo(motor_left, 1, vel_left);
    motorGo(motor_right, 1, vel_right);
    // Update position and direct 
    tick_left = ReadEncoder(encoder_left1);
    tick_right = ReadEncoder(encoder_right1);
    if (millis() - time >= 50)
    {
      time = millis();
      delta_tick_left = tick_left - pre_tick_left;
      delta_tick_right = tick_right - pre_tick_right;
      pre_tick_right = tick_right;
      pre_tick_left = tick_left;
      D_left = 2 * pi*R*delta_tick_left / N;
      D_right = 2 * pi*R*delta_tick_right / N;
      D_c = (D_left + D_right) / 2;
      // update position and direct
      x += D_c * cos(phi);
      y += D_c * sin(phi);
      phi += (D_right - D_left) / L;
     // Feedback signal to Pi
     //Serial.println(x);
     //Serial.println(y);
     //Serial.println(phi);
    }
  //}
  /*else
  //{
    stop_now();
  }*/
}
int getDistance()
{
  unsigned long duration;
  int distance;

  digitalWrite(trig_pin, HIGH);  // turn off trig pin
  delayMicroseconds(2);
  digitalWrite(trig_pin, HIGH);  // pulse out
  delayMicroseconds(5);   // pulse duration is 5us
  digitalWrite(trig_pin, LOW);  // turn of trig pin
  duration = pulseIn(echo_pin, HIGH);
  distance = int(duration / 2 / 29.412); //Centimeter
  return distance;
}
void setup()
{
  Serial.begin(9600);
  /*Pins còniguration*/
  for (int i = 0; i < 2; i++)
  {
    pinMode(inApin[i], OUTPUT);
    pinMode(inBpin[i], OUTPUT);
    pinMode(pwmpin[i], OUTPUT);
  }
  pinMode(encoder_right1, INPUT);
  pinMode(encoder_right2, INPUT);
  pinMode(encoder_left1, INPUT);
  pinMode(encoder_left2, INPUT);

  pinMode(13,OUTPUT);
  
  pinMode(enable_right, OUTPUT);
  pinMode(enable_left, OUTPUT);
  // Interrupt define
  attachInterrupt(digitalPinToInterrupt(encoder_left1), ReadEncoder(encoder_left1), RISING);
  attachInterrupt(digitalPinToInterrupt(encoder_right1), ReadEncoder(encoder_right1), RISING);
  attachInterrupt(digitalPinToInterrupt(CommPin), signalRead, RISING);

}
void motorOff(int motor)
{
  for (int i = 0; i < 2; i++)
  {
    digitalWrite(inApin[i], LOW);
    digitalWrite(inBpin[i], LOW);
  }
  analogWrite(pwmpin[motor], 0);
}
void stop_now()
{
  digitalWrite(enable_right, HIGH);
  digitalWrite(enable_left, HIGH);
}
void continue_now()
{
  digitalWrite(enable_right, LOW);
  digitalWrite(enable_left, LOW);
}
/**/
void loop()
{
  
  signalRead();
  if (flag == 1)
  {
    for (i = 0; i<10;i++)
    {
        go_to_goal(goal[i][0],goal[i][1]);
      }
      flag = 0;
    }
//go_to_goal(5.4,5.6);
//go_to_goal(6.5,6.6);
//go_to_goal(7.5,8.2);


}
