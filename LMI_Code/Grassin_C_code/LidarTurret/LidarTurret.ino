#include <Servo.h>
#include <Wire.h>
#include <LIDARLite.h>

//Delay between each sample to avoid mechanical wobble
#define DELAY_BETWEEN_SAMPLES 100
//Size of the steps of YAW/PITCH in degrees (1 = full res)
#define YAW_STEP 2
#define PITCH_STEP 2
#define MATH_PI 3.1415f

//Variables
LIDARLite myLidarLite;
Servo servoYaw,servoPitch;
char s[15];
int yawAngle,pitchAngle;
int x,y,z,r;
float theta,phi;

void setup() {
  // Initialize serial connection to display distance readings
  Serial.begin(115200); 

  //Servo init
  servoYaw.attach(10);
  servoPitch.attach(11);

  //Lidar Lite v3 init
  myLidarLite.begin(0, true);
  myLidarLite.configure(0);
}

void loop() {
  delay(5000);
  //Sweep Yaw servomotor
  for (yawAngle = 0; yawAngle <= 180; yawAngle += YAW_STEP) {
    servoYaw.write(yawAngle);
    
    //Sweep Pitch servomotor. The direction depends on the current directory
    if(pitchAngle < 90){
      for (pitchAngle = 0; pitchAngle <= 180;pitchAngle+= PITCH_STEP){
        servoPitch.write(pitchAngle);
        sendMeasurement();
      }
    } else {
      for (pitchAngle = 180; pitchAngle >= 0;pitchAngle-= PITCH_STEP){
        servoPitch.write(pitchAngle);
        sendMeasurement();
      }
    }
  }
}

// Function to acquire, convert and send the measurement.
void sendMeasurement(){
  delay(DELAY_BETWEEN_SAMPLES);
  
  // Get spherical coordinates
  r = myLidarLite.distance(false);
  theta = (float)yawAngle * PI / 180.0f;
  phi = (float)pitchAngle * PI / 180.0f;

  // Convert and send them
  sprintf(s,"%d %d %d\n\0",(int)(r*cos(phi)*cos(theta)),(int)(r*cos(phi)*sin(theta)),(int)(r*sin(phi)));
  Serial.print(s);
}

