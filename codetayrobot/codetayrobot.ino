#include <Servo.h> 
//khai bao chan 
#define NGONGIUA_PIN 8
#define NGONCAI_PIN 9
#define NGONTRO_PIN 10
#define NGONUT_PIN 11
#define KHOPCAI_PIN 12
//khai bao servo
Servo giua;
Servo cai;
Servo tro;
Servo ut;
Servo khopcai;

void setup()
{
  giua.attach(NGONGIUA_PIN);
  cai.attach(NGONCAI_PIN);
  tro.attach(NGONTRO_PIN);
  ut.attach(NGONUT_PIN);
  khopcai.attach(KHOPCAI_PIN);
}

void loop()
{
 dung();
 delay(1000);
 hello();
 delay(1000);
 dung();
 delay(1000);
 ok();
 delay(1000);
 dung();
 delay(1000);
 numbeone();
 delay(1000);
 dung();
 delay(1000);
 namtay();
 delay(1000);
 dung();
 delay(1000);
 motngon();
 delay(1000);
 thatungngon();
 
}

void namtay()
{
  giua.write(0);
  cai.write(180);
  tro.write(0);
  ut.write(180);
  khopcai.write(70);
  delay(1000);
}

void hello()
{
  khopcai.write(70);
  cai.write(180);
  ut.write(180);
  delay(1000);
  tro.write(180);
  giua.write(180);
  delay(1000);
}

void numbeone()
{
  giua.write(0);
  cai.write(0);
  tro.write(0);
  ut.write(180);
  khopcai.write(170);
  delay(1000);
}

void ok()
{
  khopcai.write(70);
  cai.write(180);
  ut.write(0);
  tro.write(180);
  giua.write(0);
  delay(1000);
}

void motngon()
{
  khopcai.write(70);
  cai.write(180);
  delay(1000);
  tro.write(0);
  delay(1000);
  giua.write(0);
  delay(1000);
  ut.write(180);
  delay(1000);
}

void thatungngon()
{
  ut.write(0);
  delay(1000);
  giua.write(180);
  delay(1000);
  tro.write(180);
  delay(1000);
  khopcai.write(170);
  cai.write(0);
  delay(1000);
}

void dung()
{
  giua.write(180);
  cai.write(0);
  tro.write(180);
  ut.write(0);
  khopcai.write(170);
}

