//Face Tracker using OpenCV and Arduino
//by Shubham Santosh

#include<Servo.h>

Servo x;
void setup() {
  Serial.begin(9600);
  x.attach(6);
}

void loop() {
  if (Serial.available() > 0)
  {
    if (Serial.read() == 'X')
    {
      x_mid = Serial.parseInt();  // read center x-coordinate
    }
  }
}
