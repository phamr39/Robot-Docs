/*Chương trình điều khiển mobile robot*/
//-------------------------------------

//Định nghĩa các chân điều khiển 2 động cơ:
#define vr1 12
#define vr2 13
#define vl1 10
#define vl2 11
//Định nghĩa chân tín hiệu encoder:
#define er1 18
#define er2 22
#define el1 19
#define el2 24
//
#define trig 50
#define echo 51
//
#define ena 53
#define enb 52
//
float R = 0.04;
float L = 0.19;
int v = 10;
float phi_d = 0, phi = 0, e = 0, w = 0, vr = 0, vl = 0, Dl = 0, Dr = 0, Dc = 0, x = 0, y = 0, xg = 0, yg = 0, P = 0, I = 0, D = 0;
int delta_tickl = 0, delta_tickr = 0, pr = 0, pr_old = 0, pl = 0, pl_old = 0, N = 100, time = 0;
const float Pi = 3.14;
int i = 0, j = 0;
//
float table1[4][2] =
{
  {0, 1},
  {1, 1},
  {1, 0},
  {0, 0},
};

void setup() {
  //Các chân điều khiển động cơ là các chân phát tín hiệu
  pinMode(vr1, OUTPUT);
  pinMode(vr2, OUTPUT);
  pinMode(vl1, OUTPUT);
  pinMode(vl2, OUTPUT);
  //Các chân tín hiệu encoder là các chân nhận tín hiệu
  pinMode(er1, INPUT);
  pinMode(er2, INPUT);
  pinMode(el1, INPUT);
  pinMode(el2, INPUT);
  //
  Serial.begin(9600);
  //Định nghĩa ngắt ngoài
  attachInterrupt(digitalPinToInterrupt(18), ReadEncoder_right, RISING);
  attachInterrupt(digitalPinToInterrupt(19), ReadEncoder_left, RISING);
  pinMode(trig, OUTPUT);
  pinMode(echo, INPUT);
}

void loop() {
  //test 1 di chuyển giữa 2 điểm
  //go_to_goal(0, 1);
  //test 2 di chuyển nhiều điểm, tránh vật cản
  for (i = 0; i <= 3; i++) {
    if (x == table1[1][0]) && y == table1[1][1]) Turn_right(phi);
      if (x == table1[2][0]) && y == table1[2][1]) Turn_right(phi);
        if (x == table1[3][0]) && y == table1[3][1]) Turn_right(phi);
        while (1) {
          long distance = getDistance();
            if (distance <= 20) Delay();
            else {
              go_to_goal(table1[i][0], table1[i][1]);
            }
            if (x == xg && y == yg) break;
          }
  }
}

//Hàm tìm đường đến đích
void go_to_goal(double xg, double yg) {
  //Thực hiện thuật toán tìm đường
  phi_d = atan2((yg - y), (xg - x));
  e = phi_d - phi;
  w = PID(e);
  vr = (2 * v + w * L) / (2 * R);
  vl = (2 * v - w * L) / (2 * R);
  if (vr > 255) vr = 255;
  if (vl > 255) vl = 255;
  if (x == xg && y == yg) {
    digitalWrite(ena, LOW);
    digitalWrite(enb, LOW);
  }
  digitalWrite(ena, HIGH);
  digitalWrite(enb, HIGH);
  analogWrite(vr1, vr);
  analogWrite(vr2, 0);
  analogWrite(vl1, vl);
  analogWrite(vl2, 0);

  //Xử lí tín hiệu từ encoder
  if (millis() - time >= 50) {
    time = millis();
    delta_tickl = pl - pl_old;
    delta_tickr = pr - pr_old;
    pl_old = pl;
    pr_old = pr;
    Dl = 2 * Pi * R * delta_tickl / N;
    Dr = 2 * Pi * R * delta_tickr / N;
    Dc = (Dr + Dl) / 2;
    //Cập nhật vị trí và hướng
    x += Dc * cos(phi);
    y += Dc * sin(phi);
    phi += (Dr - Dl) / 2;
  }
}

//Hàm PID
float PID(float e) {
  float w;
  float kp = 1.255, kd = 0.055, ki = 0.023;
  float e_old;
  P = kp * e;
  I += ki * e;
  D = kd * (e - e_old);
  w = P + I + D;
  e_old = e;
  return w;
}

//Hàm đọc tín hiệu encoder
void ReadEncoder_right()
{
  if (digitalRead(er2))
    pr++;
  else
    pr--;
}

void ReadEncoder_left()
{
  if (digitalRead(el2))
    pl++;
  else
    pl--;
}

int getDistance()
{
  unsigned long duration; // biến đo thời gian
  int distance;           // biến lưu khoảng cách

  /* Phát xung từ chân trig */
  digitalWrite(trig, 0);  // tắt chân trig
  delayMicroseconds(2);
  digitalWrite(trig, 1);  // phát xung từ chân trig
  delayMicroseconds(5);   // xung có độ dài 5 microSeconds
  digitalWrite(trig, 0);  // tắt chân trig

  /* Tính toán thời gian */
  // Đo độ rộng xung HIGH ở chân echo.
  duration = pulseIn(echo, HIGH);
  // Tính khoảng cách đến vật.
  distance = int(duration / 2 / 29.412);

  /* In kết quả ra Serial Monitor */
  //Serial.print(distance);
  //Serial.println("cm");
  //delay(200);
  return distance;
}


void Delay() {
  digitalWrite(ena, LOW);
  digitalWrite(enb, LOW);
}

void Turn_right() {
  float temp = abs(phi);
  while (abs(phi) - temp < Pi / 2) {
    if (millis() - time >= 50) {
      time = millis();
      delta_tickl = pl - pl_old;
      delta_tickr = pr - pr_old;
      pl_old = pl;
      pr_old = pr;
      Dl = 2 * Pi * R * delta_tickl / N;
      Dr = 2 * Pi * R * delta_tickr / N;
      Dc = (Dr + Dl) / 2;
      //Cập nhật vị trí và hướng
      x += Dc * cos(phi);
      y += Dc * sin(phi);
      phi += (Dr - Dl) / 2;
      //
      digitalWrite(ena, HIGH);
      digitalWrite(enb, HIGH);
      analogWrite(vr1, 0);
      analogWrite(vr2, 255);
      analogWrite(vl1, 255);
      analogWrite(vl2, 0);
    }
  }
}

void Turn_left() {
  float temp = abs(phi);
  while (abs(phi) - temp < Pi / 2) {
    if (millis() - time >= 50) {
      time = millis();
      delta_tickl = pl - pl_old;
      delta_tickr = pr - pr_old;
      pl_old = pl;
      pr_old = pr;
      Dl = 2 * Pi * R * delta_tickl / N;
      Dr = 2 * Pi * R * delta_tickr / N;
      Dc = (Dr + Dl) / 2;
      //Cập nhật vị trí và hướng
      x += Dc * cos(phi);
      y += Dc * sin(phi);
      phi += (Dr - Dl) / 2;
      //
      digitalWrite(ena, HIGH);
      digitalWrite(enb, HIGH);
      analogWrite(vr1, 255);
      analogWrite(vr2, 0);
      analogWrite(vl1, 0);
      analogWrite(vl2, 255);
    }
  }
}
