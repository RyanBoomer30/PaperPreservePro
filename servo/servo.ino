// Include the library
#include <Servo.h>

// Create the servo object
Servo liftMotor;
Servo wipper;
String command;

void setup() {
  liftMotor.attach(8);
  wipper.attach(9); // attach the servo to our servo object
  liftMotor.write(90); 
  wipper.writeMicroseconds(700); 
  Serial.begin(9600); // Begin the serial connection
}

void loop() {
  if (Serial.available() > 0)
  {
    if (Serial.read() == 'X')
    {
      liftMotor.write(80); // Turn the motor counterclockwise
      delay(1500);
      liftMotor.write(91); // Stop the motor
      wipper.writeMicroseconds(700); // Turn the motor counterclockwise
      delay(1500);
      wipper.writeMicroseconds(2400); // Turn the swipper
    } 
  }
}
