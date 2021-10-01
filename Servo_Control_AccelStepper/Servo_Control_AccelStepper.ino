#include <Servo.h>
#include <AccelStepper.h>

int pos = 0;                        // declare initial position of the servo
int servoPin = 5;                  // declare pin for the servo
int servoDelay = 10;                // delay to allow the servo to reach position;
int Stepper2Pulse = 5;
int Stepper2Direction = 6;
int Motor2position = 0;
int speedmin = 0; //pulses per second
int speedmax = 1000;  //pulses per second
int positionmax = 1600;
AccelStepper step2(1, Stepper2Pulse, Stepper2Direction);

Servo myServo;                    // create a servo object called myServo
 
void setup() {
  Serial.begin(9600);             // start serial port
  //myServo.attach(servoPin);       // declare to which pin is the servo connected
  step2.setMaxSpeed (10000);  
  step2.setSpeed(10000);
  step2.setAcceleration(10000);
  pinMode(Stepper2Pulse, OUTPUT);
  pinMode(Stepper2Direction, OUTPUT);
  digitalWrite(Stepper2Pulse, LOW);
  digitalWrite(Stepper2Direction, HIGH);
}
 
void loop() {
  while(Serial.available()==0){}; // wait until information is received from the serial port
  pos = Serial.read();            // read the position from the OSC control and server
  //myServo.write(pos);             // write the position into the servo
  Motor2position = pos;
  delay(servoDelay);              // give time to the servo to reach the position
  step2.moveTo(Motor2position);
  step2.run();
  //Serial.println(pos);
  //while (step2.currentPosition() != step2.targetPosition()) { 
  //    step2.runSpeedToPosition(); 
  //}
}
