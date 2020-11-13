#include "VarSpeedServo_Mock.h"

//mock includes
#include <chrono>
#include <thread>

//Mocked Definitions
int A0 = 0;
int A1 = 1;
int A4 = 4;
int LOW = 0;
int HIGH = 1000;
int INPUT = 1;
int OUTPUT = 1;

//Control and Feedback Pins
//regular 180 servos
int leftBasePin = 9;
int leftBaseFeedback = A0;

//360 servo
int turnTablePin = 3;
int turnTableFeedback  = 11;

//180 mini servo
int phoneMountPin =6;
int phoneMountFeedback = A4;

int ledPin = 2;

// Position constants
const int LEFT_BASE_DOWN = 110; //GOOD LW
const int LEFT_BASE_UP = 40; //GOOD LW
const int PHONEMOUNT_LANDSCAPE = 98;
const int PHONEMOUNT_MAX_TILT = 20; //NEED CONSTANT LW
const int TABLETOP_OFFSET = 65; //GOOD LW
const int TABLETOP_FRONT = 90; //GOOD LW
const int TABLETOP_LEFT = 180+TABLETOP_OFFSET; //GOOD LW
const int TABLETOP_RIGHT = 0+TABLETOP_OFFSET; //GOOD LW

// Feedback constants
const int LEFT_BASE_FB_DOWN = 415; //NEED CONSTANT LW
const int LEFT_BASE_FB_UP = 235; //NEED CONSTANT LW
const int PHONEMOUNT_FB_PORTRAIT = 0; //REDUNDANT LW
const int PHONEMOUNT_FB_LANDSCAPE = 0; //NEED CONSTANT LW


//Create VarSpeedServo objects
VarSpeedServo_Mock leftBaseServo;
VarSpeedServo_Mock tabletopServo;
VarSpeedServo_Mock phoneMountServo;
Serial serial;

enum Command {PITCH, YAW, ROLL, CLOSE, OPEN, PORTRAIT,
              LANDSCAPE, NOD, SHAKE, TILT, SHUTDOWN};

//Mocked Functions
long map(long x, long in_min, long in_max, long out_min, long out_max) {
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

void delay(int val){
  std::this_thread::sleep_for(std::chrono::milliseconds(val));
}

void digitalWrite(int x, int y){
  //do nothing
}

int analogRead(int x){
  return (x + 1);
}

void pinMode(int x, int y){
  //do nothing
}

int pulseIn(int x, int y){
  return (x + y);
}

int setRoll_tester() {
  return phoneMountServo.write_3_input;
}

int setPitchLeft_tester() {
  return leftBaseServo.write_2_input;
}

/*******************************************************************/
/*Phone Mount Functions*/
void landscape(){ //phoneMountServo moves phone to landscape position
    phoneMountServo.write(PHONEMOUNT_LANDSCAPE, 40, true);
}

void tilt() {
  int currAngle = phoneMountServo.read();
  for(int i =0; i < 3; i++){
    phoneMountServo.write(PHONEMOUNT_LANDSCAPE+PHONEMOUNT_MAX_TILT, 60, true);
    delay(500);
    phoneMountServo.write(PHONEMOUNT_LANDSCAPE-PHONEMOUNT_MAX_TILT, 60, true);
    delay(500);
  }
  phoneMountServo.write(currAngle, 60, true);
}

/*
 * Get current position of Phone Mount Servo
*/
int getPositionPM(){
  int potVal = analogRead(phoneMountFeedback);
  return map(potVal, PHONEMOUNT_FB_PORTRAIT, PHONEMOUNT_FB_LANDSCAPE, 0, 90);
}
/*******************************************************************/
/*Base Motor Functions*/
/*
 * Get current position of Base Servos
*/
int getPositionBM(){
  int potValLeft = analogRead(leftBaseFeedback);
  int leftAngle = map(potValLeft, LEFT_BASE_FB_DOWN, LEFT_BASE_FB_UP, 0, 90);
  return leftAngle;
}

// 360 parallax constants
const unsigned long unitsFC = 360; // 360 degrees in a circle
const unsigned long dcMin = 29;
const unsigned long dcMax = 971;
const unsigned long dutyScale = 1000;
// not constants, but don't want to have to declare them a lot
unsigned long tCycle, tHigh, tLow, dc;
unsigned long theta;

int getPositionTabletop(int theta){
  // int tCycle = 0;
  // int tHigh, tLow, theta, dc;
  // while (1) {
  //   tHigh = pulseIn(turnTableFeedback, HIGH);
  //   tLow = pulseIn(turnTableFeedback, LOW);
  //   tCycle = tHigh + tLow;
  //   if ((tCycle > 1000) && (tCycle < 1200)) {
  //     break;
  //   }
  // }
  // dc = (dutyScale * tHigh) / tCycle;
  // theta = ((dc - dcMin) * unitsFC) / (dcMax - dcMin + 1);
  // if (theta < 0) {
  //   theta = 0;
  // }
  // else if (theta > (unitsFC - 1)) {
  //   theta = unitsFC - 1;
  // }

  if(theta < 180){
      theta = map(theta, TABLETOP_RIGHT, 0, 0, TABLETOP_RIGHT);
      if( theta < 0){
        theta = 0;
      }
      if( theta > TABLETOP_RIGHT){
        theta = TABLETOP_RIGHT;
      }
  }
  else if (theta > 180){
    theta = map(theta, 359, TABLETOP_LEFT, TABLETOP_RIGHT+1, 180);
    if(theta < TABLETOP_RIGHT +1){
      theta = TABLETOP_RIGHT +1;
    }
    if( theta > 180)
      theta = 180;
  }

  return theta;
}

void up(){
  leftBaseServo.write(LEFT_BASE_UP, 40);
  leftBaseServo.wait();
}
void down(){
  leftBaseServo.write(LEFT_BASE_DOWN, 40);
  leftBaseServo.wait();
}
void nod(){
  //up down, arm nods twice
  int currAngleLeft = leftBaseServo.read();
  leftBaseServo.write(LEFT_BASE_UP, 60);
  leftBaseServo.wait();
  delay(100);
  leftBaseServo.write(70, 60);
  leftBaseServo.wait();
  delay(100);
  leftBaseServo.write(LEFT_BASE_UP, 60);
  leftBaseServo.wait();
  delay(100);
  leftBaseServo.write(70, 60);
  leftBaseServo.wait();
  delay(100);
  leftBaseServo.write(LEFT_BASE_UP, 60);
  leftBaseServo.wait();
  leftBaseServo.write(currAngleLeft, 60, true);
}
/*******************************************************************/
/*Turn Table Motor Functions*/
int setYaw(int val, int currPos) {
//  int offset = 0;
  //int currPos = getPositionTabletop();
  if (val > currPos) {
    //testing solution
    return 1;
    //
    tabletopServo.writeMicroseconds(1555);
    while (val > currPos + 10) {
      currPos = getPositionTabletop(0);
    }
    tabletopServo.writeMicroseconds(1540);
    while (val > currPos+2) {
      currPos = getPositionTabletop(0);
    }
  }
  else if (val < currPos) {
    // testing solution
    return 2;
    //
    tabletopServo.writeMicroseconds(1430);
    while (val < currPos - 10) {
      currPos = getPositionTabletop(0);
    }
    tabletopServo.writeMicroseconds(1440);
    while (val < currPos-2) {
      currPos = getPositionTabletop(0);
    }
  }
  return 0;
  tabletopServo.writeMicroseconds(1500);
}

void shake(){
  int currPos = getPositionTabletop(0);
  for(int i = 0; i < 3; i++){
    setYaw(45,0);
    delay(100);
    setYaw(45+90,0);
    delay(100);
  }
  setYaw(currPos,0);
}

std::vector<int> sendPosition(int x) {
  char pos[3]; // [pitch, yaw, roll]
  pos[0] = map(leftBaseServo.read(), LEFT_BASE_DOWN, LEFT_BASE_UP, 0, 90);
  pos[1] = map(getPositionTabletop(x), 0, 180, 0, 180); //[REDUNDANT]
  pos[2] = map(phoneMountServo.read(), PHONEMOUNT_LANDSCAPE-PHONEMOUNT_MAX_TILT, PHONEMOUNT_LANDSCAPE+PHONEMOUNT_MAX_TILT, 0, 90);
  serial.write(pos, 3);
  std::vector<int> vect;

  vect.push_back(+(pos[0]));
  vect.push_back(+(pos[1]));
  vect.push_back(+(pos[2]));
  return vect;
}

void _shutdown() {
  setYaw(TABLETOP_FRONT,0);
  landscape();
  delay(100);
  down();
  delay(100);
  // blink LED then off
  for (int i = 0; i < 3; i++) {
    digitalWrite(ledPin, LOW);
    delay(500);
    digitalWrite(ledPin, HIGH);
    delay(500);
  }
  sendPosition(0);
  //stop all motor movement. will need to unplug and plug back in to move again
  //while(true) {}
}

/*Emergency Shut Down*/
void emergencyShutdown(){
  //stop all motor movement. will need to unplug and plug back in to move again
  while(true) {}
}

void setPitch(char val) {
  int leftVal = map(val, 0, 90, LEFT_BASE_DOWN, LEFT_BASE_UP);
  leftBaseServo.write(leftVal, 40);
}

void setRoll(char val) {
  int pos = map(val, 0, 90, PHONEMOUNT_LANDSCAPE - PHONEMOUNT_MAX_TILT, PHONEMOUNT_LANDSCAPE + PHONEMOUNT_MAX_TILT);
  phoneMountServo.write(pos, 40, true);
}

void test() {
  shake();
  delay(1000);
}

/*******************************************************************/
void setup() {
  serial.begin(9600);
  serial.setTimeout(100);

  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);

  // feedback pins
  pinMode(leftBaseFeedback, INPUT);
  pinMode(turnTableFeedback, INPUT);
  pinMode(phoneMountFeedback, INPUT);

  // attaches the servo on pin to the servo object
  tabletopServo.attach(turnTablePin);
  setYaw(TABLETOP_FRONT,0);
  leftBaseServo.attach(leftBasePin);
  leftBaseServo.write(LEFT_BASE_DOWN, 60, true);
  phoneMountServo.attach(phoneMountPin);
  phoneMountServo.write(PHONEMOUNT_LANDSCAPE);
}

//Serial Data
unsigned char serialData[128];
unsigned long numLoops = 0;
int lastYaw = TABLETOP_FRONT;

void loop() {
  // try to keep tabletopServo from jerking
//  setYaw(lastYaw);
//  tabletopServo.writeMicroseconds(1510);
//  test();

  numLoops++;
  if (serial.available() > 0) {//serial is reading stuff
    serial.readBytes(serialData, 2);
    if (serialData[0] == 0x00) { // set pitch
      if (0 <= serialData[1] && serialData[1] <= 90) {
        setPitch(serialData[1]);
      }
    }
    else if (serialData[0] == 0x01) { // set yaw
      if (0 <= serialData[1] && serialData[1] <= 180) {
        lastYaw = map(serialData[1], 0, 180, 0, 180); //#####REDUNDANT#####
        setYaw(lastYaw,0);
      }
    }
    else if (serialData[0] == 0x02) { // set roll
      if (0 <= serialData[1] && serialData[1] <= 90) {
        setRoll(serialData[1]);
      }
    }
    else if(serialData[0] == 0x03){ // close
      down();
    }
    else if (serialData[0] == 0x04){ // open
      up();
    }
    else if (serialData[0] == 0x06){ // landscape
      landscape();
    }
    else if(serialData[0] == 0x07){ // nod
      nod();
    }
    else if (serialData[0] == 0x08){ // shake
      lastYaw = TABLETOP_FRONT;
      shake();
    }
    else if(serialData[0] == 0x09){ // tilt
      tilt();
    }
    else if (serialData[0] == 0x10) { // shutdown
      _shutdown();
    }
  }
  if (numLoops % 100 == 0) {
    setYaw(lastYaw,0);
    sendPosition(0);
    numLoops = 0;
  }

  delay(10);
} //end loop

//void loop() {
//  //setYaw(0);
//  Serial.print(" ");
//  Serial.print(getPositionTabletop());
//  delay(2000);
//}
