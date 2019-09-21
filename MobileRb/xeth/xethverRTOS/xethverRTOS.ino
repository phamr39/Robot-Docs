#include <Arduino_FreeRTOS.h>
#include "SPI.h"
// Khai báo nhiệm vụ:
void TaskBlink( void *pvParameters );
void TaskAnalogRead( void *pvParameters );
 
// the setup function runs once when you press reset or power the board
void setup() {
  
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB, on LEONARDO, MICRO, YUN, and other 32u4 based boards.
  }
 
  // Thiết lập nhiệm vụ để chạy độc lập
  xTaskCreate(
    Task1
    ,  (const portCHAR *)"Task1"   // A name just for humans
    ,  128  // Bộ nhớ RAM để cho tiến trình hoạt động >= 64byte
    ,  NULL
    ,  2  // Mức độ ưu tiên 
    ,  NULL );
 
  xTaskCreate(
    Task2
    ,  (const portCHAR *) "Task2"
    ,  128  // Stack size
    ,  NULL
    ,  1  // Priority
    ,  NULL );
 
  // Now the task scheduler, which takes over control of scheduling individual tasks, is automatically started.
 
}
 
void loop()
{
  // Chương trình chính đã được thực hiện trong các Task nên loop() trống 
}
 
/*--------------------------------------------------*/
/*---------------------- Tasks ---------------------*/
/*--------------------------------------------------*/
 
void Task1(void *pvParameters)  // This is a task.
{
  (void) pvParameters;
  //Code được đặt ở đây sẽ chạy 1 lần giống void setup()
for (;;)
  {
   //Code được đặt trong đây sẽ tương đương với hàm void loop()
  }
}
void Task2(void *pvParameters)  // This is a task.
{
  (void) pvParameters;
  for (;;)
  {
  }
}
