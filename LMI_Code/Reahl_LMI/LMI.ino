/* -----------------------------------------------------------------------------------------
Lidar Mapping Instrument (LMI; pronounced "Lemmy")
  
  By Jocelyn Reahl '19, Wellesley College
  
  Adapted from LidarTurret.ino by Charles Grassin
    Code and project found here: http://www.charleslabs.fr/en/project-3D+Lidar+Scanner
  
  Professor Wes Watters
    ASTR 202: Hands-On Planetary Exploration; Spring 2018

--------------------------------------------------------------

Some Considerations:
  The Altitude (ALT) motor can only reach an angle of 75°
  The Azimuth (AZ) motor can only rotate 180° (as of 5/21/2018 it is a standard servo motor)
    Future paths for the Azimuth motor involve implementing either:
      Parallax Feedback 360°™ continuous rotation servo motor with feedback pin (aka encoder) @ pin A0
        or
      Standard continuous rotation servo with timestamps
        or
      Bidirectional Stepper motor with 0.9° full step increments

--------------------------------------------------------------

Instructions for Use (with already constructed LMI):
  1) Download the Arduino IDE: https://www.arduino.cc/en/Main/Software
    (you've probably already completed this step)
    
  2) Download the following libraries (Make sure to reboot the IDE when you download them):
    How to Download Libraries: https://learn.sparkfun.com/tutorials/installing-an-arduino-library
    Servo.h (Runs your servos; typically already comes w/IDE): https://github.com/arduino-libraries/Servo
    Wire.h (Allows Arduino to communicate w/I2C devices; typically already comes w/IDE): https://github.com/esp8266/Arduino/tree/master/libraries/Wire
    LIDARLite.h (Allows you to run your LIDARLite v3): https://github.com/garmin/LIDARLite_v3_Arduino_Library
    
  3) Plug in LMI's attached USB cord to your computer
  
  4) Check "Tools" tab on Arduino IDE and check that:
    Board = Arduino Nano
    Processor = ATmega328P
    Port = Something that has "usbserial" in it with a string of letters and numbers after it; nothing with "Bluetooth" in it
      If you are running Mac OS X, you'll need to download FTDI drivers
        Tutorial from SparkFun: https://learn.sparkfun.com/tutorials/how-to-install-ftdi-drivers/mac
        
  5) Click "Upload" (the button on that looks like an arrow pointing to the right)
  
  6) Open up Serial Monitor (button is on top right; looks like a magnifying glass) and make sure it's set to 115200 baud
  
  7) Data! Columns from left to right: x, y, and z coordinates; these are computed by the program from Range (r), theta, and phi angles.

  8) When scanner reaches the end of its scanning cycle, deselect "Autoscroll" on the Serial Monitor and hit Control (or "Command" if you're using Mac) + A to select all the data in the window

  9) Copy these data into a text file and save it.

  10) Plot these data in your favorite 3D plotting software after removing "> nack" values from the data set (these are random "hiccup" values)

  Can also use this program in conjunction with LidarViewer by Charles Grassin, which uses the Processing program
  This program is a great resource for demonstration and presentation, but don't expect to be able to save these results
    Download Processing here: https://processing.org/download/
    After uploading the Arduino code, upload the Processing LidarViewer code
    DO NOT open the Serial Monitor when you are using the Processing code - it's using the serial monitor and it'll get confused if both Processing and the serial monitor are open

-----------------------------------------------------------
General troubleshooting (Future Users: please add any other troubleshooting solutions you have! - Jocelyn Reahl)

"When in doubt, reboot!" - Jocelyn Reahl's dad

Still seeing the "Bluetooth" ports even after downloading FTDI drivers (this only applies if you've gotten this to work before)
  Reboot Arduino and reopen with LMI's USB cord UNPLUGGED

LMI stopped scanning in the middle of its scan! What the heck?!
  Check the Serial Monitor; if the last measurement was "> nack" then it got stuck there instead of recovering. Upload an empty Arduino sketch, wait for ~30 sec, and then re-upload this sketch.

(If using a continuous rotation servo for the Azimuth motor)
I told my continuous rotation servo to move from x degree to y degree in a for loop and it's just moving around like crazy! What did I do wrong?
  Continuous rotation servos, while able to run on the Servo.h library, interpret Servo.write(0) as rotating at full speed in one direction, Servo.write(180) as moving at full speed in the other direction, and Servo.write(90) as stationary
          
----------------------------------------------------------------------------------------- */
//Include Libraries downloaded in Step 2:
#include <Servo.h>
#include <Wire.h>
#include <LIDARLite.h>

#define DELAY_BETWEEN_SAMPLES 100 //Delay between each sample to avoid mechanical wobble

//Defining the size of the steps that AZ/ALT make in degrees (1 = full resolution); change the number after AZ_STEP/ALT_STEP in order to change the step size
#define AZ_STEP 1
#define ALT_STEP 1
#define MATH_PI 3.1415f //defining what pi is (for use in later calculations)

//Variables
LIDARLite myLidarLite;
Servo servoAz,servoAlt; //defines the Azimuth servo (servoAz) and Altitude servo (servoAlt)
char s[15];
int azAngle,altAngle; //defines the angles from the Alt/Az servos as integers for use in later calculations (the units for these angles are in radians)
int x,y,z,r; //sets x, y, z, and r as integers for use in later calculations
float theta,phi; //sets theta and phi as numbers that can have decimals for use in calculations that convert azAngle and altAngle from radians to degrees

void setup() {
  // Initialize Serial Monitor to display distance readings
  Serial.begin(115200); //Set serial monitor to 115200 baud

  //Servo initialization
  servoAz.attach(9); //attaches the Azimuth servo to digital pin 9 on Arduino Nano (D9)
  servoAlt.attach(10); //attaches the Altitude servo to digital pin 10 on Arduino Nano (D10)
  
  //Set Alt and Az servos to starting position 0°
  servoAz.write(0); 
  servoAlt.write(0);

  //Lidar Lite v3 initialization 
  //(details on the different settings can be found in the "GetDistanceI2C" example that comes with the LIDARLite library; using 0 (standard setting) is probably best for our purposes)
  myLidarLite.begin(0, true);
  myLidarLite.configure(0);
}

void loop() {
  delay(5000); //delay 5 seconds so you can open the Serial Monitor or start running the Processing program
  //Sweep Az servomotor
  for (azAngle = 0; azAngle <= 180; azAngle += AZ_STEP) //Don't change this unless you're using a different Az motor
  {
    servoAz.write(azAngle);
    
    //Sweep Alt servomotor. The direction depends on the current directory
    if(altAngle < 23) //This is the max altAngle that is swept divided by 2 (and rounded up for numbers ending in .5); note that the max altAngle is 75)
    {
      for (altAngle = 0; altAngle <= 45;altAngle+= ALT_STEP){
        servoAlt.write(altAngle);
        sendMeasurement();
      }
    } else {
      for (altAngle = 45; altAngle >= 0;altAngle-= ALT_STEP){
        servoAlt.write(altAngle);
        sendMeasurement();
      }
    }
  }
}

// Function to acquire, convert and send the measurement.
void sendMeasurement(){
  delay(DELAY_BETWEEN_SAMPLES);
  
  // Compute spherical coordinates
  r = myLidarLite.distance(false);
  theta = (float)azAngle * PI / 180.0f;
  phi = (float)altAngle * PI / 180.0f;

  // Convert and send them to the Serial Monitor
  sprintf(s,"%d %d %d\n\0",(int)(r*cos(phi)*cos(theta)),(int)(r*cos(phi)*sin(theta)),(int)(r*sin(phi)));
  Serial.print(s);
}

