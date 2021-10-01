//Stepper-Servo library includes, initialization and setting pins
#include <AccelStepper.h>

AccelStepper stepper1Upper(AccelStepper::DRIVER,5,6);
AccelStepper stepper2Lower(AccelStepper::DRIVER,7,8);
AccelStepper mainDriveServo(AccelStepper::DRIVER,9,10);

//stepper motor constants
int stepperMotorMaxSpeed = 10000; 
int motorAccel = 10000; 

//init stepper variables
int speedStepper = 0;
int speedVal = 0;
float stepper1UpperSpeedTweak = 0;
float stepper2LowerPositionTweak = 0;
 
void setup() {
  Serial.begin(9600);             // start serial port
  //myServo.attach(servoPin);       // declare to which pin is the servo connected
  step2.setMaxSpeed (stepperMotorMaxSpeed);  
  step2.setSpeed(stepperMotorMaxSpeed/10);
  step2.setAcceleration(motorAccel);
}
 
void loop() {
  while(Serial.available()==0){}; // wait until information is received from the serial port
    speedStepper = Serial.read(); // read the speed from the OSC control and server
    Serial.println("speedStepper: " + String(speedStepper));
    finalSpeed = int(abs(speedStepper + stepper1UpperSpeedTweak));
    finalAccel = motorAccel;
    mainDriveServo.setSpeed(speedStepper);
    stepper1Upper.setSpeed(finalSpeed);
    stepper2Lower.setSpeed(-finalSpeed);
    mainDriveServo.runSpeed();
    stepper1Upper.runSpeed();
    stepper2Lower.runSpeed();
}
